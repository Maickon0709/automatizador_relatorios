"""
leitor.py

Responsável por ler a planilha de vendas (.xlsx) e devolver os dados
já validados como um DataFrame do pandas, pronto para o processador.py.
"""

from pathlib import Path
import pandas as pd

COLUNAS_ESPERADAS = [
    "data",
    "vendedor",
    "numero_produto",
    "nome_produto",
    "quantidade",
    "valor_unitario",
]

# a planilha original traz a coluna como "quantidade", mas isso é ambíguo
# (poderia ser estoque). Como a aba é "vendas" e cada linha representa uma
# venda de um vendedor, renomeamos para deixar explícito que é a
# quantidade vendida naquela transação.
RENOMEAR_COLUNAS = {
    "quantidade": "quantidade_vendida",
}


def ler_planilha_vendas(caminho_arquivo: str, aba: str = "vendas") -> pd.DataFrame:
    """
    Lê a planilha de vendas e retorna um DataFrame limpo.

    Parâmetros:
        caminho_arquivo: caminho para o .xlsx
        aba: nome da aba a ser lida (padrão: "vendas")

    Retorna:
        DataFrame com as colunas validadas e sem linhas vazias.

    Lança:
        FileNotFoundError: se o arquivo não existir
        ValueError: se faltar alguma coluna esperada
    """
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    df = pd.read_excel(caminho, sheet_name=aba)

    # remove linhas totalmente vazias (ex: linha em branco no meio dos dados)
    df = df.dropna(how="all")

    # valida se as colunas esperadas estão presentes
    colunas_faltando = set(COLUNAS_ESPERADAS) - set(df.columns)
    if colunas_faltando:
        raise ValueError(f"Colunas faltando na planilha: {colunas_faltando}")

    # garante os tipos corretos
    df["data"] = pd.to_datetime(df["data"])
    df["quantidade"] = df["quantidade"].astype(int)
    df["valor_unitario"] = df["valor_unitario"].astype(float)

    # renomeia para deixar explícito o significado da coluna (ver RENOMEAR_COLUNAS)
    df = df.rename(columns=RENOMEAR_COLUNAS)

    # reseta o índice depois do dropna, pra não ficar com buracos (0,1,2,4,5...)
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    # teste rápido manual
    caminho_teste = "vendas_agosto_exemplo.xlsx"
    df_vendas = ler_planilha_vendas(caminho_teste)
    print(df_vendas)
    print("\nTipos de dados:")
    print(df_vendas.dtypes)
