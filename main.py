from config.config import carregar_configuracoes
from capturar_dados.coletar_dados import ColetaDadosMaps
from excel.exportar_excel import exportar_para_excel
from config.assets import *
from datetime import datetime
from utils.killProcess import kill_processes
import logging
import os

# Inicializa Configuração do Logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
except:
    pass

def main():
    """
    Função principal.
    Responsável por carregar o arquivo de entrada,
    executar as buscas no Google Maps e exportar os dados extraídos para um arquivo Excel.
    
    Parâmetros:
        None

    Retorna:
        None
    """
    try:
        logging.info("Iniciando Processamento - Coleta de Dados Estabelecimentos")
        
        # Fecha (força o encerramento) de todos os processos.
        kill_processes(KILLPROCESS)
        
        # Lê e carrega o arquivo JSON de entrada com as configurações das pesquisas.
        listEntradas = carregar_configuracoes(CAMINHO_INPUT)

        # Realizar coleta dos dados de pesquisa 
        clssColetarDados = ColetaDadosMaps()
        dictResultados = clssColetarDados.coletar_dados_pesquisas(listEntradas)

        # Gerar e exportar excel
        os.makedirs('dados', exist_ok=True)
        strCaminhoExcel = os.path.join('dados', NOME_PLANILHA.replace("$DATA$", datetime.now().strftime("%d%m%Y_%H%M%S")))
        exportar_para_excel(dictResultados, strCaminhoExcel)
        
        logging.info(f'Arquivo Excel salvo: {strCaminhoExcel}')

    except Exception as erro: 
        raise Exception(erro)
    
if __name__ == "__main__":
    main()