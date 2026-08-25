from typing import List

Matrix = List[List[float]]


def validar_matriz(m: Matrix) -> None:
    if not m or not m[0]:
        raise ValueError("A matriz nao pode ser vazia.")
    colunas = len(m[0])
    for linha in m:
        if len(linha) != colunas:
            raise ValueError("Todas as linhas da matriz devem ter o mesmo tamanho.")


def soma_matrizes(a: Matrix, b: Matrix) -> Matrix:
    validar_matriz(a)
    validar_matriz(b)

    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("As matrizes devem ter a mesma dimensao para soma.")

    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def multiplicar_por_escalar(m: Matrix, escalar: float) -> Matrix:
    validar_matriz(m)
    return [[elemento * escalar for elemento in linha] for linha in m]


def multiplicar_matrizes(a: Matrix, b: Matrix) -> Matrix:
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


def transposta(m: Matrix) -> Matrix:
    validar_matriz(m)
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def identidade(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def inversa(m: Matrix) -> Matrix:
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


def ler_matriz(nome: str) -> Matrix:
    print(f"\nDigite a matriz {nome}.")
    linhas = int(input("Quantidade de linhas: "))
    colunas = int(input("Quantidade de colunas: "))

    matriz: Matrix = []
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


def imprimir_matriz(m: Matrix, titulo: str = "Resultado") -> None:
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

            elif opcao == "0":
                print("Encerrando...")
                break

            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    menu()
