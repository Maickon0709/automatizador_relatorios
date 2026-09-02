"""
relatorio.py

Gera o relatório final em .xlsx a partir dos dados já processados
(vindos de processador.processar()). O arquivo final tem 3 abas:
vendas detalhadas, resumo por vendedor e resumo por produto.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica, só pra gerar arquivo
import matplotlib.pyplot as plt


def gerar_imagem_relatorio(resultado: dict, pasta_saida: str = ".") -> str:
    """
    Gera uma imagem (.png) com um resumo visual do relatório:
    tabela de totais por vendedor + gráfico de barras de faturamento.

    Parâmetros:
        resultado: dict retornado por processador.processar()
        pasta_saida: pasta onde a imagem será salva

    Retorna:
        Caminho completo da imagem gerada.
    """
    por_vendedor = resultado["por_vendedor"]
    por_produto = resultado["por_produto"]
    vendas_detalhadas = resultado["vendas_detalhadas"]

    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    caminho_imagem = pasta / f"relatorio_vendas_{timestamp}.png"

    faturamento_total = vendas_detalhadas["valor_total"].sum()
    total_vendas = len(vendas_detalhadas)
    ticket_medio = faturamento_total / total_vendas if total_vendas else 0

    # paleta de cores
    COR_FUNDO = "#F7F8FA"
    COR_CARD = "#FFFFFF"
    COR_TEXTO_PRINCIPAL = "#1D2433"
    COR_TEXTO_SECUNDARIO = "#6B7280"
    COR_DESTAQUE = "#2E5EAA"
    COR_BARRAS = ["#2E5EAA", "#5B8DEF", "#8FB4F5", "#C3D9FA"]
    COR_LINHA_GRID = "#E5E7EB"

    def formatar_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    fig = plt.figure(figsize=(12, 8), facecolor=COR_FUNDO)
    grade = fig.add_gridspec(
        2, 2, height_ratios=[1, 3.2],
        left=0.06, right=0.96, top=0.90, bottom=0.10,
        hspace=0.35, wspace=0.18,
    )

    # --- título ---
    fig.text(0.06, 0.965, "Relatório de Vendas", fontsize=20, fontweight="bold", color=COR_TEXTO_PRINCIPAL)
    fig.text(0.06, 0.935, datetime.now().strftime("Gerado em %d/%m/%Y às %H:%M"),
              fontsize=9, color=COR_TEXTO_SECUNDARIO)

    # --- cartões de indicadores (topo, ocupando as duas colunas) ---
    eixo_resumo = fig.add_subplot(grade[0, :])
    eixo_resumo.axis("off")
    eixo_resumo.set_facecolor(COR_FUNDO)

    indicadores = [
        ("Faturamento total", formatar_moeda(faturamento_total)),
        ("Vendas registradas", f"{total_vendas}"),
        ("Ticket médio", formatar_moeda(ticket_medio)),
        ("Vendedores / Produtos", f"{por_vendedor.shape[0]} / {por_produto.shape[0]}"),
    ]
    largura_cartao = 1 / len(indicadores)
    for i, (rotulo, valor) in enumerate(indicadores):
        x0 = i * largura_cartao + 0.01
        largura = largura_cartao - 0.02
        eixo_resumo.add_patch(plt.Rectangle(
            (x0, 0.05), largura, 0.9,
            transform=eixo_resumo.transAxes,
            facecolor=COR_CARD, edgecolor=COR_LINHA_GRID, linewidth=1,
            zorder=1,
        ))
        eixo_resumo.text(x0 + largura / 2, 0.62, valor, transform=eixo_resumo.transAxes,
                          ha="center", va="center", fontsize=15, fontweight="bold",
                          color=COR_DESTAQUE, zorder=2)
        eixo_resumo.text(x0 + largura / 2, 0.26, rotulo, transform=eixo_resumo.transAxes,
                          ha="center", va="center", fontsize=9.5,
                          color=COR_TEXTO_SECUNDARIO, zorder=2)
    eixo_resumo.set_xlim(0, 1)
    eixo_resumo.set_ylim(0, 1)

    # --- gráfico de barras: faturamento por vendedor ---
    eixo_grafico = fig.add_subplot(grade[1, 0])
    eixo_grafico.set_facecolor(COR_CARD)
    cores_barras = [COR_BARRAS[i % len(COR_BARRAS)] for i in range(len(por_vendedor))]
    barras = eixo_grafico.bar(
        por_vendedor["vendedor"], por_vendedor["valor_total"],
        color=cores_barras, edgecolor="none", width=0.6, zorder=3,
    )
    for barra in barras:
        altura = barra.get_height()
        eixo_grafico.text(
            barra.get_x() + barra.get_width() / 2, altura,
            formatar_moeda(altura), ha="center", va="bottom",
            fontsize=9, color=COR_TEXTO_PRINCIPAL, fontweight="bold",
        )

    eixo_grafico.set_title("Faturamento por Vendedor", fontsize=12, fontweight="bold",
                            color=COR_TEXTO_PRINCIPAL, loc="left", pad=12)
    eixo_grafico.tick_params(axis="x", rotation=20, colors=COR_TEXTO_SECUNDARIO, labelsize=9.5)
    eixo_grafico.tick_params(axis="y", colors=COR_TEXTO_SECUNDARIO, labelsize=9)
    eixo_grafico.set_ylabel("")
    eixo_grafico.grid(axis="y", color=COR_LINHA_GRID, linewidth=0.8, zorder=0)
    eixo_grafico.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        eixo_grafico.spines[lado].set_visible(False)
    eixo_grafico.spines["bottom"].set_color(COR_LINHA_GRID)
    eixo_grafico.set_yticklabels([])
    margem = por_vendedor["valor_total"].max() * 0.15
    eixo_grafico.set_ylim(0, por_vendedor["valor_total"].max() + margem)

    # --- tabela: totais por produto ---
    eixo_tabela = fig.add_subplot(grade[1, 1])
    eixo_tabela.axis("off")
    eixo_tabela.set_title("Total por Produto", fontsize=12, fontweight="bold",
                           color=COR_TEXTO_PRINCIPAL, loc="left", pad=12)

    dados_tabela = por_produto[["nome_produto", "quantidade_vendida", "valor_total"]].assign(
        valor_total=lambda d: d["valor_total"].map(formatar_moeda)
    )
    tabela = eixo_tabela.table(
        cellText=dados_tabela.values,
        colLabels=["Produto", "Qtd.", "Total"],
        loc="center",
        cellLoc="center",
        colWidths=[0.5, 0.2, 0.3],
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(9.5)
    tabela.scale(1, 2.0)

    for (linha, _coluna), celula in tabela.get_celld().items():
        celula.set_edgecolor(COR_LINHA_GRID)
        if linha == 0:
            celula.set_facecolor(COR_DESTAQUE)
            celula.get_text().set_color("white")
            celula.get_text().set_fontweight("bold")
        else:
            celula.set_facecolor(COR_CARD if linha % 2 else COR_FUNDO)
            celula.get_text().set_color(COR_TEXTO_PRINCIPAL)

    fig.savefig(caminho_imagem, dpi=150, facecolor=COR_FUNDO)
    plt.close(fig)

    return str(caminho_imagem)


def gerar_relatorio(resultado: dict, pasta_saida: str = ".") -> str:
    """
    Gera o arquivo .xlsx do relatório com base no dicionário retornado
    por processador.processar().

    Parâmetros:
        resultado: dict com as chaves "vendas_detalhadas", "por_vendedor"
            e "por_produto" (formato de processador.processar())
        pasta_saida: pasta onde o relatório será salvo

    Retorna:
        Caminho completo do arquivo gerado.
    """
    chaves_necessarias = {"vendas_detalhadas", "por_vendedor", "por_produto"}
    faltando = chaves_necessarias - set(resultado.keys())
    if faltando:
        raise ValueError(f"Faltam chaves no resultado do processamento: {faltando}")

    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    nome_arquivo = f"relatorio_vendas_{timestamp}.xlsx"
    caminho_completo = pasta / nome_arquivo

    with pd.ExcelWriter(caminho_completo, engine="openpyxl") as writer:
        resultado["vendas_detalhadas"].to_excel(
            writer, sheet_name="Vendas Detalhadas", index=False
        )
        resultado["por_vendedor"].to_excel(
            writer, sheet_name="Resumo por Vendedor", index=False
        )
        resultado["por_produto"].to_excel(
            writer, sheet_name="Resumo por Produto", index=False
        )

        # ajusta a largura das colunas em cada aba, pra não sair com
        # tudo cortado quando abrir no Excel
        for aba in writer.sheets.values():
            for coluna in aba.columns:
                maior_valor = max(
                    (len(str(celula.value)) for celula in coluna if celula.value is not None),
                    default=10,
                )
                letra_coluna = coluna[0].column_letter
                aba.column_dimensions[letra_coluna].width = maior_valor + 2

    return str(caminho_completo)


if __name__ == "__main__":
    from leitor import ler_planilha_vendas
    from processador import processar

    df_vendas = ler_planilha_vendas("vendas_agosto_exemplo.xlsx")
    resultado = processar(df_vendas)

    caminho_xlsx = gerar_relatorio(resultado)
    caminho_imagem = gerar_imagem_relatorio(resultado)
    print(f"Relatório (Excel) gerado em: {caminho_xlsx}")
    print(f"Relatório (imagem) gerado em: {caminho_imagem}")
