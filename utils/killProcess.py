import subprocess
import logging

def kill_processes(listNomesProcessos:list):
    """
    Fecha (força o encerramento) de todos os processos cujos nomes estão na lista fornecida.

    Parâmetros:
    - listNomesProcessos (list): lista com os nomes dos executáveis, ex: ["EXCEL.EXE", "chrome.exe"]
    """
    listNomesProcessos = list(listNomesProcessos)
    for strNomeProcesso in listNomesProcessos:
        try:
            # Comando para matar por nome (Windows)
            resultado = subprocess.run(['taskkill', '/f', '/im', strNomeProcesso],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if resultado.returncode == 0:
                logging.info(f"Processo {strNomeProcesso} finalizado com sucesso.")
            else:
                if "não foi encontrado" in resultado.stderr or "not found" in resultado.stderr:
                    logging.info(f"Processo {strNomeProcesso} não estava aberto.")
                else:
                    logging.error(f"Erro ao tentar finalizar {strNomeProcesso}: {resultado.stderr.strip()}")
        except Exception as erro:
            logging.error(f"Erro ao finalizar Processo {strNomeProcesso}. Motivo: {erro}")