import logging
import json

# Inicializa Configuração do Logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
except:
    pass

def carregar_configuracoes(strArquivoEntrada:str):
    """
    Lê e carrega o arquivo JSON de entrada com as configurações das pesquisas.

    Parâmetros:
        strArquivoEntrada (str): Caminho para o arquivo JSON contendo as pesquisas.

    Retorna:
        list: Uma lista de dicionários, cada um contendo os parâmetros de uma pesquisa.
    """
    try:
        with open(strArquivoEntrada, "r", encoding="utf-8") as f:
            return json.load(f)
        logging.info("Arquivo Input carregado com Sucesso")
    except Exception as erro:
        raise Exception(f'Erro ao Carregar Configurações do arquivo Input. Motivo: {erro}')