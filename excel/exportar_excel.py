import pandas as pd
import logging

# Inicializa Configuração do Logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
except:
    pass

def exportar_para_excel(dictResultados:dict, strCaminhoExcel:str):
    """
    Exporta os resultados de pesquisa (um dict de DataFrames) para um arquivo Excel,
    com cada pesquisa em uma aba (sheet) diferente.

    Parâmetros:
        dictResultados (dict): Dicionário onde cada chave é o nome da aba
                               e cada valor é um pandas.DataFrame com resultados.
        strCaminhoExcel (str): Caminho de saída do arquivo Excel (.xlsx).

    Retorna:
        None
    """
    try:
        with pd.ExcelWriter(strCaminhoExcel) as writer:
            for aba, df in dictResultados.items():
                df.to_excel(writer, sheet_name=aba, index=False)
        logging.info("Dados Exportados para o Excel com Sucesso.")
    except Exception as erro:
        logging.error(f'Erro ao Exportar Dados para o Excel. Motivo: {erro}')