"""
banco.py

Responsável por persistir os dados processados em um banco SQLite.
Cria a tabela de vendas (se não existir) e insere os registros vindos
do processador.py.
"""

import sqlite3
from pathlib import Path
import pandas as pd

CAMINHO_BANCO_PADRAO = "vendas.db"

CRIAR_TABELA_VENDAS = """
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    vendedor TEXT NOT NULL,
    numero_produto TEXT NOT NULL,
    nome_produto TEXT NOT NULL,
    quantidade_vendida INTEGER NOT NULL,
    valor_unitario REAL NOT NULL,
    valor_total REAL NOT NULL
);
"""


def conectar(caminho_banco: str = CAMINHO_BANCO_PADRAO) -> sqlite3.Connection:
    """
    Abre (ou cria, se não existir) o arquivo do banco SQLite e retorna
    a conexão já com a tabela 'vendas' garantida.
    """
    conn = sqlite3.connect(caminho_banco)
    conn.execute(CRIAR_TABELA_VENDAS)
    conn.commit()
    return conn


def salvar_vendas(df: pd.DataFrame, conn: sqlite3.Connection, limpar_antes: bool = True) -> int:
    """
    Insere as vendas detalhadas (com valor_total já calculado) no banco.

    Parâmetros:
        df: DataFrame vindo de processador.calcular_valor_total()
            (precisa ter a coluna valor_total)
        conn: conexão sqlite3 já aberta (ver conectar())
        limpar_antes: se True, apaga os dados antigos da tabela antes de
            inserir — evita duplicar vendas ao reprocessar o mesmo arquivo.
            Numa versão futura isso pode virar um controle mais fino
            (ex: por data ou por id de importação).

    Retorna:
        Quantidade de linhas inseridas.
    """
    colunas_necessarias = {
        "data", "vendedor", "numero_produto",
        "nome_produto", "quantidade_vendida",
        "valor_unitario", "valor_total",
    }
    faltando = colunas_necessarias - set(df.columns)
    if faltando:
        raise ValueError(f"DataFrame não tem as colunas necessárias: {faltando}")

    cursor = conn.cursor()

    if limpar_antes:
        cursor.execute("DELETE FROM vendas")

    registros = [
        (
            row.data.strftime("%Y-%m-%d"),
            row.vendedor,
            row.numero_produto,
            row.nome_produto,
            int(row.quantidade_vendida),
            float(row.valor_unitario),
            float(row.valor_total),
        )
        for row in df.itertuples(index=False)
    ]

    cursor.executemany(
        """
        INSERT INTO vendas
            (data, vendedor, numero_produto, nome_produto,
             quantidade_vendida, valor_unitario, valor_total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        registros,
    )
    conn.commit()

    return cursor.rowcount if not limpar_antes else len(registros)


def buscar_todas_vendas(conn: sqlite3.Connection) -> pd.DataFrame:
    """Lê todas as vendas gravadas no banco e retorna como DataFrame."""
    return pd.read_sql_query("SELECT * FROM vendas", conn, parse_dates=["data"])


if __name__ == "__main__":
    from leitor import ler_planilha_vendas
    from processador import calcular_valor_total

    df_vendas = ler_planilha_vendas("vendas_agosto_exemplo.xlsx")
    df_com_total = calcular_valor_total(df_vendas)

    conn = conectar()
    linhas_inseridas = salvar_vendas(df_com_total, conn)
    print(f"{linhas_inseridas} linha(s) inserida(s) em '{CAMINHO_BANCO_PADRAO}'.")

    print("\n=== Conferindo o que está no banco ===")
    print(buscar_todas_vendas(conn))

    conn.close()
