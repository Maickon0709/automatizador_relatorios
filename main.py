"""
main.py

Ponto de entrada do pipeline de automação de relatórios de vendas.
Amarra os 4 módulos na ordem: leitor -> processador -> banco -> relatorio.

Uso:
    python main.py <caminho_da_planilha.xlsx>
"""

import sys

from leitor import ler_planilha_vendas
from processador import processar
from banco import conectar, salvar_vendas
from relatorio import gerar_relatorio, gerar_imagem_relatorio


def executar_pipeline(caminho_planilha: str) -> None:
    """
    Executa o pipeline completo:
      1. Lê a planilha de vendas (leitor.py)
      2. Processa e calcula os totais (processador.py)
      3. Salva no banco SQLite (banco.py)
      4. Gera o relatório final em Excel e imagem (relatorio.py)
    """
    print(f"1/4 Lendo planilha: {caminho_planilha}")
    df_vendas = ler_planilha_vendas(caminho_planilha)
    print(f"    {len(df_vendas)} venda(s) lida(s).")

    print("2/4 Processando dados...")
    resultado = processar(df_vendas)
    print(f"    {resultado['por_vendedor'].shape[0]} vendedor(es), "
          f"{resultado['por_produto'].shape[0]} produto(s).")

    print("3/4 Salvando no banco de dados...")
    conn = conectar()
    try:
        linhas_inseridas = salvar_vendas(resultado["vendas_detalhadas"], conn)
        print(f"    {linhas_inseridas} linha(s) gravada(s) no banco.")
    finally:
        conn.close()

    print("4/4 Gerando relatório final...")
    caminho_xlsx = gerar_relatorio(resultado)
    caminho_imagem = gerar_imagem_relatorio(resultado)
    print(f"    Excel : {caminho_xlsx}")
    print(f"    Imagem: {caminho_imagem}")

    print("\nPipeline concluído com sucesso.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_da_planilha.xlsx>")
        sys.exit(1)

    try:
        executar_pipeline(sys.argv[1])
    except (FileNotFoundError, ValueError) as erro:
        print(f"Erro no pipeline: {erro}")
        sys.exit(1)
