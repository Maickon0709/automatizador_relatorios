# Automatizador de Relatórios de Vendas

Pipeline em Python que lê uma planilha de vendas (.xlsx), processa os
dados, persiste em um banco SQLite e gera um relatório final em Excel
e em imagem (.png).

## O que o projeto faz

```
vendas.xlsx  →  leitor.py  →  processador.py  →  banco.py  →  relatorio.py
                (lê e valida)  (calcula totais)  (SQLite)     (Excel + PNG)
```

1. **`leitor.py`** — lê a planilha de vendas, remove linhas vazias, valida
   se as colunas esperadas existem e garante os tipos de dado corretos.
2. **`processador.py`** — calcula o valor total de cada venda
   (`quantidade_vendida × valor_unitario`) e gera agregações de
   faturamento por vendedor e por produto.
3. **`banco.py`** — salva os dados processados em um banco SQLite local
   (`vendas.db`), usando queries parametrizadas.
4. **`relatorio.py`** — gera o relatório final em dois formatos:
   - um `.xlsx` com 3 abas (vendas detalhadas, resumo por vendedor,
     resumo por produto);
   - uma imagem `.png` com um resumo visual (faturamento total, gráfico
     de barras por vendedor e tabela por produto).
5. **`main.py`** — orquestra o pipeline inteiro, do arquivo de entrada
   ao relatório final, com tratamento de erros.

## Exemplo de saída

![Exemplo de relatório gerado](relatorio_exemplo.png)

## Como rodar

```bash
pip install -r requirements.txt
python main.py vendas_agosto_exemplo.xlsx
```

O terminal mostra o progresso de cada etapa e, ao final, o caminho dos
arquivos gerados (`.xlsx` e `.png`).

### Formato esperado da planilha de entrada

A planilha deve ter uma aba chamada `vendas`, com as colunas:

| data | vendedor | numero_produto | nome_produto | quantidade | valor_unitario |
|------|----------|-----------------|----------------|------------|-----------------|

## Testes

O projeto tem cobertura de testes automatizados com **Pytest** para os
5 módulos (20 testes no total), incluindo casos de erro (arquivo
inexistente, coluna faltando, dado inválido):

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Tecnologias

- Python 3
- pandas — leitura e processamento dos dados
- openpyxl — leitura/escrita de arquivos Excel
- matplotlib — geração da imagem do relatório
- SQLite (biblioteca padrão `sqlite3`) — persistência
- Pytest — testes automatizados

## Possíveis melhorias futuras

- Arquitetura em camadas (repository/service) para separar melhor a
  lógica de acesso a dados da lógica de negócio
- Controle de duplicidade mais fino no banco (hoje o pipeline limpa a
  tabela antes de cada execução)
- Suporte a múltiplos arquivos de entrada em uma única execução
