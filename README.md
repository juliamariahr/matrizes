# Operacoes Basicas com Matrizes

Este projeto em Python realiza operacoes basicas com matrizes por meio de um menu interativo no terminal.

## Funcionalidades

O arquivo `matrizes.py` permite:

- Soma de duas matrizes
- Multiplicacao de uma matriz por um escalar
- Multiplicacao de duas matrizes
- Calculo da transposta de uma matriz
- Calculo da inversa de uma matriz quadrada (metodo de Gauss-Jordan)

## Como executar

No terminal, dentro da pasta do projeto, rode:

```bash
python matrizes.py
```

Depois, escolha uma opcao no menu e informe os dados solicitados.

## Formato de entrada das matrizes

Para cada matriz, o programa solicita:

1. Quantidade de linhas
2. Quantidade de colunas
3. Cada linha da matriz com valores separados por espaco

Exemplo de uma linha com 3 colunas:

```text
1 2 3
```

## Observacoes importantes

- Para soma, as matrizes devem ter a mesma dimensao.
- Para multiplicacao entre matrizes, o numero de colunas da matriz A deve ser igual ao numero de linhas da matriz B.
- A inversa so existe para matrizes quadradas e inversiveis.
- Em caso de entrada invalida, o programa mostra mensagens de erro e permite tentar novamente.