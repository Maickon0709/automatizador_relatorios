"""
test_leitor.py

Testes do módulo leitor.py: leitura da planilha de vendas, tratamento
de linhas vazias, validação de colunas e tipos de dados.
"""

import pandas as pd
import pytest

from leitor import ler_planilha_vendas, COLUNAS_ESPERADAS


@pytest.fixture
def planilha_valida(tmp_path):
    """Cria uma planilha .xlsx válida, com uma linha vazia no meio (como no arquivo real)."""
    caminho = tmp_path / "vendas_teste.xlsx"

    linhas = [
        ["2026-08-01", "João Silva", "PRD-1023", "Cadeira Gamer", 3, 450],
        ["2026-08-01", "Maria Souza", "PRD-1050", "Mouse Sem Fio", 5, 90],
        [None, None, None, None, None, None],  # linha vazia proposital
        ["2026-08-03", "Maria Souza", "PRD-2010", "Teclado Mecânico", 1, 320],
    ]
    df = pd.DataFrame(linhas, columns=COLUNAS_ESPERADAS)
    df.to_excel(caminho, sheet_name="vendas", index=False)

    return caminho


def test_le_planilha_com_sucesso(planilha_valida):
    df = ler_planilha_vendas(str(planilha_valida))

    assert len(df) == 3  # a linha vazia não deve ser contada
    assert "quantidade_vendida" in df.columns  # coluna renomeada


def test_remove_linha_totalmente_vazia(planilha_valida):
    df = ler_planilha_vendas(str(planilha_valida))

    # índice deve estar sequencial (sem buraco por causa do dropna)
    assert list(df.index) == list(range(len(df)))


def test_tipos_de_dados_corretos(planilha_valida):
    df = ler_planilha_vendas(str(planilha_valida))

    assert pd.api.types.is_datetime64_any_dtype(df["data"])
    assert pd.api.types.is_integer_dtype(df["quantidade_vendida"])
    assert pd.api.types.is_float_dtype(df["valor_unitario"])


def test_arquivo_inexistente_gera_erro():
    with pytest.raises(FileNotFoundError):
        ler_planilha_vendas("arquivo_que_nao_existe.xlsx")


def test_coluna_faltando_gera_erro(tmp_path):
    caminho = tmp_path / "vendas_incompleta.xlsx"
    # falta a coluna "valor_unitario" de propósito
    df = pd.DataFrame({
        "data": ["2026-08-01"],
        "vendedor": ["João Silva"],
        "numero_produto": ["PRD-1023"],
        "nome_produto": ["Cadeira Gamer"],
        "quantidade": [3],
    })
    df.to_excel(caminho, sheet_name="vendas", index=False)

    with pytest.raises(ValueError):
        ler_planilha_vendas(str(caminho))
