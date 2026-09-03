"""
test_processador.py

Testes do módulo processador.py: cálculo de valor_total e agregações
por vendedor e por produto.
"""

import pandas as pd
import pytest

from processador import (
    calcular_valor_total,
    total_por_vendedor,
    total_por_produto,
    processar,
)


@pytest.fixture
def df_vendas():
    """DataFrame de vendas de exemplo, já no formato pós-leitor.py."""
    return pd.DataFrame({
        "data": pd.to_datetime(["2026-08-01", "2026-08-01", "2026-08-02"]),
        "vendedor": ["João Silva", "Maria Souza", "João Silva"],
        "numero_produto": ["PRD-1023", "PRD-1050", "PRD-1050"],
        "nome_produto": ["Cadeira Gamer", "Mouse Sem Fio", "Mouse Sem Fio"],
        "quantidade_vendida": [3, 5, 2],
        "valor_unitario": [450.0, 90.0, 90.0],
    })


def test_calcular_valor_total(df_vendas):
    resultado = calcular_valor_total(df_vendas)

    assert list(resultado["valor_total"]) == [1350.0, 450.0, 180.0]


def test_calcular_valor_total_nao_modifica_original(df_vendas):
    calcular_valor_total(df_vendas)

    assert "valor_total" not in df_vendas.columns  # original não foi alterado


def test_total_por_vendedor(df_vendas):
    df_com_total = calcular_valor_total(df_vendas)
    resumo = total_por_vendedor(df_com_total)

    joao = resumo[resumo["vendedor"] == "João Silva"].iloc[0]
    assert joao["quantidade_vendida"] == 5  # 3 + 2
    assert joao["valor_total"] == 1530.0  # 1350 + 180


def test_total_por_vendedor_ordenado_por_faturamento(df_vendas):
    df_com_total = calcular_valor_total(df_vendas)
    resumo = total_por_vendedor(df_com_total)

    valores = list(resumo["valor_total"])
    assert valores == sorted(valores, reverse=True)


def test_total_por_produto(df_vendas):
    df_com_total = calcular_valor_total(df_vendas)
    resumo = total_por_produto(df_com_total)

    mouse = resumo[resumo["numero_produto"] == "PRD-1050"].iloc[0]
    assert mouse["quantidade_vendida"] == 7  # 5 + 2
    assert mouse["valor_total"] == 630.0  # 450 + 180


def test_processar_retorna_todas_as_chaves(df_vendas):
    resultado = processar(df_vendas)

    assert set(resultado.keys()) == {"vendas_detalhadas", "por_vendedor", "por_produto"}
    assert "valor_total" in resultado["vendas_detalhadas"].columns
