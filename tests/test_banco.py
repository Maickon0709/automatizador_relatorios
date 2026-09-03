"""
test_banco.py

Testes do módulo banco.py: criação da tabela, inserção e leitura de
vendas no SQLite. Usa um banco temporário (tmp_path) para não sujar
o banco real do projeto.
"""

import pandas as pd
import pytest

from banco import conectar, salvar_vendas, buscar_todas_vendas


@pytest.fixture
def df_vendas_com_total():
    return pd.DataFrame({
        "data": pd.to_datetime(["2026-08-01", "2026-08-02"]),
        "vendedor": ["João Silva", "Maria Souza"],
        "numero_produto": ["PRD-1023", "PRD-1050"],
        "nome_produto": ["Cadeira Gamer", "Mouse Sem Fio"],
        "quantidade_vendida": [3, 5],
        "valor_unitario": [450.0, 90.0],
        "valor_total": [1350.0, 450.0],
    })


@pytest.fixture
def banco_temporario(tmp_path):
    caminho_banco = tmp_path / "vendas_teste.db"
    conn = conectar(str(caminho_banco))
    yield conn
    conn.close()


def test_conectar_cria_tabela(banco_temporario):
    cursor = banco_temporario.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='vendas'"
    )
    assert cursor.fetchone() is not None


def test_salvar_vendas_insere_linhas(banco_temporario, df_vendas_com_total):
    linhas_inseridas = salvar_vendas(df_vendas_com_total, banco_temporario)

    assert linhas_inseridas == 2


def test_buscar_todas_vendas_retorna_dados_corretos(banco_temporario, df_vendas_com_total):
    salvar_vendas(df_vendas_com_total, banco_temporario)
    df_do_banco = buscar_todas_vendas(banco_temporario)

    assert len(df_do_banco) == 2
    assert df_do_banco["valor_total"].sum() == 1800.0


def test_salvar_vendas_limpa_antes_por_padrao(banco_temporario, df_vendas_com_total):
    salvar_vendas(df_vendas_com_total, banco_temporario)
    salvar_vendas(df_vendas_com_total, banco_temporario)  # roda de novo

    df_do_banco = buscar_todas_vendas(banco_temporario)
    assert len(df_do_banco) == 2  # não duplicou


def test_salvar_vendas_coluna_faltando_gera_erro(banco_temporario):
    df_incompleto = pd.DataFrame({"vendedor": ["João Silva"]})

    with pytest.raises(ValueError):
        salvar_vendas(df_incompleto, banco_temporario)
