"""
processador.py

Recebe o DataFrame já limpo (vindo de leitor.py) e aplica as
transformações de negócio: cálculo de valor total por venda e
agregações por vendedor e por produto, prontas para o relatorio.py.
"""

import pandas as pd


def calcular_valor_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona a coluna 'valor_total' (quantidade_vendida * valor_unitario)
    ao DataFrame de vendas.

    Não modifica o DataFrame original — retorna uma cópia.
    """
    df = df.copy()
    df["valor_total"] = df["quantidade_vendida"] * df["valor_unitario"]
    return df


def total_por_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa as vendas por vendedor, somando quantidade vendida e valor total.

    Retorna um DataFrame ordenado do maior para o menor faturamento.
    """
    resumo = (
        df.groupby("vendedor")
        .agg(
            quantidade_vendida=("quantidade_vendida", "sum"),
            valor_total=("valor_total", "sum"),
        )
        .reset_index()
        .sort_values("valor_total", ascending=False)
        .reset_index(drop=True)
    )
    return resumo


def total_por_produto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa as vendas por produto (numero_produto + nome_produto),
    somando quantidade vendida e valor total.

    Retorna um DataFrame ordenado do maior para o menor faturamento.
    """
    resumo = (
        df.groupby(["numero_produto", "nome_produto"])
        .agg(
            quantidade_vendida=("quantidade_vendida", "sum"),
            valor_total=("valor_total", "sum"),
        )
        .reset_index()
        .sort_values("valor_total", ascending=False)
        .reset_index(drop=True)
    )
    return resumo


def processar(df: pd.DataFrame) -> dict:
    """
    Roda o pipeline completo de processamento e retorna um dicionário
    com tudo o que o relatorio.py vai precisar.

    Retorna:
        {
            "vendas_detalhadas": DataFrame com valor_total por linha,
            "por_vendedor": DataFrame agregado por vendedor,
            "por_produto": DataFrame agregado por produto,
        }
    """
    df_com_total = calcular_valor_total(df)

    return {
        "vendas_detalhadas": df_com_total,
        "por_vendedor": total_por_vendedor(df_com_total),
        "por_produto": total_por_produto(df_com_total),
    }


if __name__ == "__main__":
    from leitor import ler_planilha_vendas

    df_vendas = ler_planilha_vendas("vendas_agosto_exemplo.xlsx")
    resultado = processar(df_vendas)

    print("=== Vendas detalhadas ===")
    print(resultado["vendas_detalhadas"])

    print("\n=== Total por vendedor ===")
    print(resultado["por_vendedor"])

    print("\n=== Total por produto ===")
    print(resultado["por_produto"])
