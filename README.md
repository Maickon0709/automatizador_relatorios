# Automatizador de Relatórios de Vendas

Pipeline em Python que lê uma planilha de vendas (.xlsx), processa os
dados, persiste em um banco SQLite e gera um relatório final em Excel
e em imagem — com uma interface gráfica simples para quem não quer usar
o terminal.

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
   - uma imagem `.png` com um resumo visual estilo dashboard
     (indicadores, gráfico de barras por vendedor e tabela por produto).
5. **`main.py`** — orquestra o pipeline inteiro, do arquivo de entrada
   ao relatório final, com tratamento de erros.
6. **`interface.py`** — interface gráfica (Tkinter): a pessoa escolhe a
   planilha e clica em um botão, sem precisar do terminal. Os relatórios
   são salvos automaticamente em uma pasta `Relatorios de Vendas` na
   Área de Trabalho.

## Como rodar

Antes de tudo, clone o repositório e abra o terminal **dentro da pasta
do projeto** (onde estão os arquivos `.py`):

```bash
pip install -r requirements.txt
```

### Opção 1 — Interface gráfica (recomendado para uso do dia a dia)

Ainda dentro da pasta do projeto, rode:

```bash
python interface.py
```

Uma janela vai abrir. Clique em **Selecionar Planilha...** e escolha o
arquivo `.xlsx` — ele pode estar em qualquer pasta do computador, não
precisa estar junto do projeto. Depois clique em **Gerar Relatório**.

Os arquivos gerados (`.xlsx` e `.png`) são salvos automaticamente em uma
pasta chamada `Relatorios de Vendas`, dentro da Área de Trabalho
(Desktop). Essa pasta **é criada sozinha pelo programa** na primeira vez
que você gera um relatório — você não precisa criar ela na mão antes.

### Opção 2 — Linha de comando

```bash
python main.py vendas_agosto_exemplo.xlsx
```

O nome do arquivo no final do comando é a planilha que você quer
processar. Diferente da interface gráfica, aqui o caminho é relativo à
pasta onde você está rodando o comando — ou seja, a planilha precisa
estar **na mesma pasta do projeto** (ou você informa o caminho completo
até ela, ex: `C:\Users\seu_usuario\Desktop\vendas.xlsx`).

O terminal mostra o progresso de cada etapa e, ao final, o caminho dos
arquivos gerados (`.xlsx` e `.png`).

### Formato esperado da planilha de entrada

A planilha deve ter uma aba chamada `vendas`, com as colunas:

| data | vendedor | numero_produto | nome_produto | quantidade | valor_unitario |
|------|----------|-----------------|----------------|------------|-----------------|

## Testes

O projeto tem cobertura de testes automatizados com **Pytest** para os
5 módulos principais (20 testes no total), incluindo casos de erro
(arquivo inexistente, coluna faltando, dado inválido). Os testes já
estão neste repositório, dentro da pasta `tests/` — não precisa criar
nada, só rodar:

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Gerando um executável (.exe)

Para distribuir o programa sem exigir Python instalado no computador de
quem for usar, você pode empacotar tudo em um único arquivo `.exe`.

**Passo 1 — Instalar a ferramenta de empacotamento.** No terminal,
dentro da pasta do projeto:

```bash
pip install pyinstaller
```

**Passo 2 — Gerar o executável.** Ainda no terminal, dentro da pasta do
projeto:

```bash
pyinstaller --onefile --windowed --name "Relatorio de Vendas" interface.py
```

Isso pode demorar um pouco (às vezes mais de um minuto) — é normal, ele
está empacotando o Python inteiro junto com as bibliotecas usadas.

**Passo 3 — Encontrar o executável gerado.** O comando acima cria
algumas pastas novas dentro da pasta do projeto: `build`, `dist`, e um
arquivo terminado em `.spec`. O que importa é a pasta **`dist`** — abra
ela (pelo Explorador de Arquivos do Windows, ou pelo próprio PyCharm no
menu lateral esquerdo) e você vai encontrar o arquivo:

```
Relatorio de Vendas.exe
```

**Passo 4 — Levar o executável para a Área de Trabalho.** Se quiser um
ícone fácil de achar, sem precisar entrar na pasta do projeto toda vez:

1. Abra o Explorador de Arquivos do Windows (tecla Windows + E)
2. Navegue até a pasta `dist` dentro da pasta do projeto (o caminho
   completo é algo como
   `C:\Users\SEU_USUARIO\PycharmProjects\NOME_DO_PROJETO\dist`)
3. Clique com o botão direito no arquivo `Relatorio de Vendas.exe`
4. Clique em **Copiar** (ou aperte `Ctrl + C`)
5. Vá até a Área de Trabalho (clique em "Área de Trabalho" no menu
   lateral esquerdo do Explorador de Arquivos, ou minimize todas as
   janelas pra ver o Desktop)
6. Clique com o botão direito em um espaço vazio da Área de Trabalho e
   clique em **Colar** (ou aperte `Ctrl + V`)

Pronto — agora existe um ícone na Área de Trabalho, e basta dar duplo
clique nele para abrir o programa, sem precisar de terminal, PyCharm ou
Python instalado.

> **Nota:** o `.exe` gerado não fica no GitHub (o `.gitignore` do
> projeto ignora as pastas `build`, `dist` e o arquivo `.spec` de
> propósito) — cada pessoa que quiser usar o programa como executável
> precisa gerar o seu próprio `.exe` seguindo os passos acima. O que
> fica no GitHub é só o código-fonte.

## Tecnologias

- Python 3
- pandas — leitura e processamento dos dados
- openpyxl — leitura/escrita de arquivos Excel
- matplotlib — geração da imagem do relatório
- SQLite (biblioteca padrão `sqlite3`) — persistência
- Tkinter — interface gráfica
- Pytest — testes automatizados
- PyInstaller — empacotamento em executável

## Possíveis melhorias futuras

- Arquitetura em camadas (repository/service) para separar melhor a
  lógica de acesso a dados da lógica de negócio
- Controle de duplicidade mais fino no banco (hoje o pipeline limpa a
  tabela antes de cada execução)
- Suporte a múltiplos arquivos de entrada em uma única execução
