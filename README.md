# Automacao Busca Dados Estabelecimentos

## Objetivo

Automação para coleta de dados de estabelecimentos no Google Maps, parametrizando buscas via JSON e exportando resultados para Excel.

## Como executar

1. Versão do Python utilizado no Desenvolvimento -> 3.13.3

2. Instale as dependências:
pip install -r requirements.txt

3. Ajuste suas buscas em `dados/input.json`.

4. Execute:
python main.py

5. O arquivo Excel no final da execução estará em `dados/resultado_dados_DATA_HORA.xlsx`.

## Estrutura

- `main.py`: Fluxo principal
- `assets.py`: Arquivo que define os principais caminhos e constantes utilizadas na Automação
- `killProcess.py`: Fecha processos abertos, de acordo informado no arquivo assets.py
- `scraper.py`: Funções para realizar Coleta de Dados dos Estabelecimentos.
- `excel_utils.py`: Exportação Excel