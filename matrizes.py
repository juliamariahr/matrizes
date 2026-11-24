from typing import List, Optional, Tuple

Matriz = List[List[float]]

CLASSIFICACOES_SISTEMA = {
    "SPD": "Sistema Possivel e Determinado (SPD)",
    "SPI": "Sistema Possivel e Indeterminado (SPI)",
    "SI": "Sistema Impossivel (SI)",
}


def nome_classificacao_sistema(sigla: str) -> str:
    return CLASSIFICACOES_SISTEMA.get(sigla, sigla)


def validar_matriz(m: Matriz) -> None:
    if not m or not m[0]:
        raise ValueError("A matriz nao pode ser vazia.")
    colunas = len(m[0])
    for linha in m:
        if len(linha) != colunas:
            raise ValueError("Todas as linhas da matriz devem ter o mesmo tamanho.")


def soma_matrizes(a: Matriz, b: Matriz) -> Matriz:
    validar_matriz(a)
    validar_matriz(b)

    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("As matrizes devem ter a mesma dimensao para soma.")

    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def multiplicar_por_escalar(m: Matriz, escalar: float) -> Matriz:
    validar_matriz(m)
    return [[elemento * escalar for elemento in linha] for linha in m]


def multiplicar_matrizes(a: Matriz, b: Matriz) -> Matriz:
    validar_matriz(a)
    validar_matriz(b)

    if len(a[0]) != len(b):
        raise ValueError("Numero de colunas de A deve ser igual ao numero de linhas de B.")

    linhas_a = len(a)
    colunas_b = len(b[0])
    comum = len(a[0])

    resultado = [[0.0 for _ in range(colunas_b)] for _ in range(linhas_a)]

    for i in range(linhas_a):
        for j in range(colunas_b):
            soma = 0.0
            for k in range(comum):
                soma += a[i][k] * b[k][j]
            resultado[i][j] = soma

    return resultado


def transposta(m: Matriz) -> Matriz:
    validar_matriz(m)
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def identidade(n: int) -> Matriz:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def inversa(m: Matriz) -> Matriz:
    validar_matriz(m)

    n = len(m)
    if n != len(m[0]):
        raise ValueError("A inversa so existe para matrizes quadradas.")

    # Copias para nao alterar a matriz original.
    a = [linha[:] for linha in m]
    inv = identidade(n)

    for i in range(n):
        pivo = a[i][i]

        if pivo == 0:
            linha_troca = -1
            for r in range(i + 1, n):
                if a[r][i] != 0:
                    linha_troca = r
                    break
            if linha_troca == -1:
                raise ValueError("A matriz nao e inversivel (determinante zero).")

            a[i], a[linha_troca] = a[linha_troca], a[i]
            inv[i], inv[linha_troca] = inv[linha_troca], inv[i]
            pivo = a[i][i]

        fator = pivo
        for j in range(n):
            a[i][j] /= fator
            inv[i][j] /= fator

        for r in range(n):
            if r == i:
                continue
            fator = a[r][i]
            for c in range(n):
                a[r][c] -= fator * a[i][c]
                inv[r][c] -= fator * inv[i][c]

    return inv


def classificar_sistema(a: Matriz, b: List[float]) -> str:
    """Classifica Ax = b como SPD, SPI ou SI usando os postos das matrizes."""
    validar_matriz(a)

    linhas = len(a)
    variaveis = len(a[0])
    if len(b) != linhas:
        raise ValueError("O vetor de termos independentes deve ter uma entrada por equacao.")

    matriz = [linha[:] + [b[i]] for i, linha in enumerate(a)]
    tolerancia = 1e-10
    linha_pivo = 0
    colunas_pivo: List[int] = []

    for coluna in range(variaveis):
        linha_escolhida = max(
            range(linha_pivo, linhas),
            key=lambda r: abs(matriz[r][coluna]),
            default=linha_pivo,
        )

        if abs(matriz[linha_escolhida][coluna]) < tolerancia:
            continue

        matriz[linha_pivo], matriz[linha_escolhida] = (
            matriz[linha_escolhida],
            matriz[linha_pivo],
        )
        pivo = matriz[linha_pivo][coluna]
        matriz[linha_pivo] = [valor / pivo for valor in matriz[linha_pivo]]

        for linha in range(linhas):
            if linha == linha_pivo:
                continue
            fator = matriz[linha][coluna]
            if abs(fator) >= tolerancia:
                matriz[linha] = [
                    matriz[linha][j] - fator * matriz[linha_pivo][j]
                    for j in range(variaveis + 1)
                ]

        colunas_pivo.append(coluna)
        linha_pivo += 1
        if linha_pivo == linhas:
            break

    posto_a = len(colunas_pivo)
    posto_ampliada = posto_a
    for linha in matriz:
        if (
            all(abs(linha[coluna]) < tolerancia for coluna in range(variaveis))
            and abs(linha[variaveis]) >= tolerancia
        ):
            posto_ampliada = posto_a + 1
            break

    if posto_ampliada != posto_a:
        return "SI"
    if posto_a == variaveis:
        return "SPD"
    return "SPI"


def resolver_sistema(a: Matriz, b: List[float]) -> Tuple[str, Optional[List[float]]]:
    """Resolve Ax = b e informa se o sistema e SPD, SPI ou SI."""
    classificacao = classificar_sistema(a, b)
    if classificacao != "SPD":
        return classificacao, None

    linhas = len(a)
    variaveis = len(a[0])
    matriz = [linha[:] + [b[i]] for i, linha in enumerate(a)]
    tolerancia = 1e-10
    linha_pivo = 0
    colunas_pivo: List[int] = []

    for coluna in range(variaveis):
        linha_escolhida = max(
            range(linha_pivo, linhas),
            key=lambda r: abs(matriz[r][coluna]),
            default=linha_pivo,
        )
        if abs(matriz[linha_escolhida][coluna]) < tolerancia:
            continue

        matriz[linha_pivo], matriz[linha_escolhida] = (
            matriz[linha_escolhida],
            matriz[linha_pivo],
        )
        pivo = matriz[linha_pivo][coluna]
        matriz[linha_pivo] = [valor / pivo for valor in matriz[linha_pivo]]

        for linha in range(linhas):
            if linha == linha_pivo:
                continue
            fator = matriz[linha][coluna]
            if abs(fator) >= tolerancia:
                matriz[linha] = [
                    matriz[linha][j] - fator * matriz[linha_pivo][j]
                    for j in range(variaveis + 1)
                ]

        colunas_pivo.append(coluna)
        linha_pivo += 1

    solucao = [0.0] * variaveis
    for linha, coluna in enumerate(colunas_pivo):
        solucao[coluna] = matriz[linha][variaveis]
    return classificacao, solucao


def ler_matriz(nome: str) -> Matriz:
    print(f"\nDigite a matriz {nome}.")
    linhas = int(input("Quantidade de linhas: "))
    colunas = int(input("Quantidade de colunas: "))
    if linhas <= 0 or colunas <= 0:
        raise ValueError("A quantidade de linhas e colunas deve ser maior que zero.")

    matriz: Matriz = []
    for i in range(linhas):
        while True:
            entrada = input(
                f"Linha {i + 1} (digite {colunas} numeros separados por espaco): "
            ).strip()
            partes = entrada.split()

            if len(partes) != colunas:
                print("Quantidade de valores invalida. Tente novamente.")
                continue

            try:
                linha = [float(x) for x in partes]
                matriz.append(linha)
                break
            except ValueError:
                print("Valor invalido. Use apenas numeros.")

    return matriz


def ler_sistema() -> Tuple[Matriz, List[float]]:
    print("\nDigite o sistema linear Ax = b.")
    linhas = int(input("Quantidade de equacoes: "))
    variaveis = int(input("Quantidade de variaveis: "))
    if linhas <= 0 or variaveis <= 0:
        raise ValueError("A quantidade de equacoes e variaveis deve ser maior que zero.")

    coeficientes: Matriz = []
    termos_independentes: List[float] = []

    for i in range(linhas):
        while True:
            entrada = input(
                f"Equacao {i + 1} "
                f"(digite {variaveis} coeficientes e o termo independente separados por espaco): "
            ).strip()
            partes = entrada.split()
            if len(partes) != variaveis + 1:
                print("Quantidade de valores invalida. Tente novamente.")
                continue
            try:
                valores = [float(x) for x in partes]
                coeficientes.append(valores[:variaveis])
                termos_independentes.append(valores[variaveis])
                break
            except ValueError:
                print("Valor invalido. Use apenas numeros.")

    return coeficientes, termos_independentes


def solucao_parametrica(a: Matriz, b: List[float]) -> List[str]:
    """Representa uma solucao SPI em funcao de parametros livres."""
    matriz = [linha[:] + [b[i]] for i, linha in enumerate(a)]
    linhas = len(matriz)
    variaveis = len(a[0])
    tolerancia = 1e-10
    linha_pivo = 0
    colunas_pivo: List[int] = []

    for coluna in range(variaveis):
        linha_escolhida = max(
            range(linha_pivo, linhas),
            key=lambda r: abs(matriz[r][coluna]),
            default=linha_pivo,
        )
        if abs(matriz[linha_escolhida][coluna]) < tolerancia:
            continue

        matriz[linha_pivo], matriz[linha_escolhida] = (
            matriz[linha_escolhida],
            matriz[linha_pivo],
        )
        pivo = matriz[linha_pivo][coluna]
        matriz[linha_pivo] = [valor / pivo for valor in matriz[linha_pivo]]

        for linha in range(linhas):
            if linha == linha_pivo:
                continue
            fator = matriz[linha][coluna]
            if abs(fator) >= tolerancia:
                matriz[linha] = [
                    matriz[linha][j] - fator * matriz[linha_pivo][j]
                    for j in range(variaveis + 1)
                ]

        colunas_pivo.append(coluna)
        linha_pivo += 1
        if linha_pivo == linhas:
            break

    livres = [i for i in range(variaveis) if i not in colunas_pivo]
    nomes_livres = {coluna: f"t{indice + 1}" for indice, coluna in enumerate(livres)}
    resultado: List[str] = []

    for coluna in range(variaveis):
        if coluna in nomes_livres:
            resultado.append(f"x{coluna + 1} = {nomes_livres[coluna]}")
            continue

        linha = colunas_pivo.index(coluna)
        expressao = f"{matriz[linha][variaveis]:.4f}"
        for livre in livres:
            coeficiente = -matriz[linha][livre]
            if abs(coeficiente) >= tolerancia:
                sinal = "+" if coeficiente >= 0 else "-"
                magnitude = abs(coeficiente)
                expressao += f" {sinal} {magnitude:.4f}*{nomes_livres[livre]}"
        resultado.append(f"x{coluna + 1} = {expressao}")

    return resultado


def imprimir_matriz(m: Matriz, titulo: str = "Resultado") -> None:
    print(f"\n{titulo}:")
    for linha in m:
        print(" ".join(f"{valor:10.4f}" for valor in linha))


def menu() -> None:
    while True:
        print("\n=== OPERACOES COM MATRIZES ===")
        print("1. Soma de matrizes")
        print("2. Multiplicacao por escalar")
        print("3. Multiplicacao de duas matrizes")
        print("4. Transposta")
        print("5. Inversa")
        print("6. Resolver sistema linear")
        print("0. Sair")

        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                a = ler_matriz("A")
                b = ler_matriz("B")
                r = soma_matrizes(a, b)
                imprimir_matriz(r)

            elif opcao == "2":
                m = ler_matriz("M")
                escalar = float(input("Digite o valor do escalar: "))
                r = multiplicar_por_escalar(m, escalar)
                imprimir_matriz(r)

            elif opcao == "3":
                a = ler_matriz("A")
                b = ler_matriz("B")
                r = multiplicar_matrizes(a, b)
                imprimir_matriz(r)

            elif opcao == "4":
                m = ler_matriz("M")
                r = transposta(m)
                imprimir_matriz(r)

            elif opcao == "5":
                m = ler_matriz("M")
                r = inversa(m)
                imprimir_matriz(r, "Inversa")

            elif opcao == "6":
                a, b = ler_sistema()
                classificacao, solucao = resolver_sistema(a, b)
                print(
                    "\nClassificacao: "
                    f"{nome_classificacao_sistema(classificacao)}"
                )

                if classificacao == "SPD" and solucao is not None:
                    print("Solucao unica:")
                    for i, valor in enumerate(solucao):
                        print(f"x{i + 1} = {valor:.10g}")
                elif classificacao == "SPI":
                    print("Solucao geral:")
                    for expressao in solucao_parametrica(a, b):
                        print(expressao)
                else:
                    print("O sistema nao possui solucao.")

            elif opcao == "0":
                print("Encerrando...")
                break

            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    menu()
