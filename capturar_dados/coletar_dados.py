from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.assets import GOOGLEMAPS_URL
import pandas as pd
import logging
import time

# Inicializa Configuração do Logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
except:
    pass

class ColetaDadosMaps:
    """
    Classe responsável por automatizar a coleta de dados de estabelecimentos no Google Maps usando Selenium.
    Permite abertura do navegador, busca e extração de dados para múltiplas pesquisas.
    """

    def __init__(self):
        """
        Inicializa as variáveis de navegador e página.
        """
        self.navegador = None
        self.wait = None

    def _abrir_googlemaps(self):
        """
        Inicializa o Selenium WebDriver, abre o navegador e acessa o Google Maps.

        Parâmetros:
            Nenhum

        Retorna:
            None
        """
        try:
            logging.info("Abrindo navegador")
            
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            
            service = Service()
            service.log_output = False
            
            self.navegador = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.navegador, 20)
            self.navegador.get(GOOGLEMAPS_URL)
            
            logging.info("Acesso ao Google Maps realizado com sucesso!")
        except Exception as erro:
            raise Exception(f"Erro ao abrir site do Google Maps. Motivo: {erro}")

    def _buscar_coletar(self, in_strTipoEstabelicmento:str, in_strCidade:str,in_intQtde: int) -> list:
        """
        Realiza a busca pelo termo informado e coleta os dados dos estabelecimentos desejados.

        Parâmetros:
            in_strTipoEstabelicmento (str): Tipo do estabelecimento a ser buscado.
            in_strCidade (str): Cidade onde realizar a busca.
            in_intQtde (int): Quantidade de estabelecimentos a coletar.

        Retorna:
            list: Lista de dicionários com os dados dos estabelecimentos encontrados.
        """
        try:
            strPesquisa = f"{in_strTipoEstabelicmento} em {in_strCidade}"
            logging.info(f"Iniciando busca: '{strPesquisa}' com limite de {in_intQtde} resultados.")

            # Realiza a busca no Google Maps pelo termo informado no JSON
            inputBusca = self.wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
            inputBusca.clear()
            inputBusca.send_keys(strPesquisa)
            time.sleep(2)
            inputBusca.send_keys(Keys.ENTER)
            time.sleep(5)
            
            try:
                # Tenta focar na lista de resultados
                self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]')))
            except:
                pass
            
            try:
                painel = self.navegador.find_elements(By.XPATH, '//div[contains(@class, "m6QErb DxyBCb")]')
                painel = painel[1] if len(painel) > 1 else painel[0]
            except:
                pass
            
            logging.info("Busca realizada. Rolando resultados para encontrar os estabelecimentos...")

            # Percorre os resultados da barra lateral até obter a quantidade desejada
            intQuantAnterior = 0
            listCards = []
            
            while True:
                # Simula a rolagem para baixo
                self.navegador.execute_script("arguments[0].scrollBy(0, 10000);", painel)
                time.sleep(2)
                
                cards = self.navegador.find_elements(By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]')
                intNumResultados = len(cards)
                
                if intNumResultados >= in_intQtde:
                    listCards = cards[:in_intQtde]
                    logging.info(f"Quantidade ideal de estabelecimentos encontrados: {len(listCards)}")
                    break
                elif intNumResultados == intQuantAnterior:
                    listCards = cards
                    logging.info(f"Quantidade máxima possível atingida: {len(listCards)}")
                    break
                else:
                    intQuantAnterior = intNumResultados

            listEmpresas = []
            
            # Conjunto utilizado para armazenar uma "chave única" de cada estabelecimentp já extraído.
            setEmpresasVistas = set()

            # Acessa cada estabelecimento na lista e extrai as informações desejadas
            for idx, card in enumerate(listCards):
                try:
                    logging.info(f"Capturando dados do estabelecimento {idx+1} de {len(listCards)}...")
                    self.navegador.execute_script("arguments[0].click();", card)
                    time.sleep(2)

                    try:
                        strNome = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))).text.strip()
                    except:
                        strNome = ""
                        
                    try:
                        strEndereco = self.navegador.find_element(By.XPATH, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').text
                    except:
                        strEndereco = ""
                        
                    try:
                        strDominio = self.navegador.find_element(By.XPATH, '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').text
                    except:
                        strDominio = ""
                        
                    strSite = f"https://www.{strDominio}" if strDominio else ""
                    try:
                        strTelefone = self.navegador.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').text
                    except:
                        strTelefone = ""
                        
                    try:
                        strQtdeAval = self.navegador.find_element(By.XPATH, '//div[@jsaction="pane.reviewChart.moreReviews"]//span').text
                        intQtdeAvaliacoes = int(strQtdeAval.split()[0].replace('.', '').replace(',', '')) if strQtdeAval else ""
                    except:
                        intQtdeAvaliacoes = ""
                        
                    try:
                        nota_elem = self.navegador.find_element(By.XPATH, '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]')
                        floatNota = float(nota_elem.get_attribute('aria-label').split()[0].replace(',', '.'))
                    except:
                        floatNota = ""

                    # Verifica se o estabelecimento já foi extraído, evitando duplicidade
                    tplChave = (strNome, strTelefone, strSite)
                    if tplChave not in setEmpresasVistas:
                        dictEmpresa = {
                            "Nome": strNome,
                            "Nota": floatNota,
                            "Qtde Avaliações": intQtdeAvaliacoes,
                            "Endereço": strEndereco,
                            "Telefone": strTelefone,
                            "Site": strSite,
                        }
                        
                        listEmpresas.append(dictEmpresa)
                        setEmpresasVistas.add(tplChave)
                        
                        logging.info(f"Dados capturados com sucesso para: {strNome if strNome else '(sem nome)'}")
                    else:
                        logging.info(f"Estabelecimento já foi capturado (duplicidade evitada).")
                except Exception as erro:
                    logging.error(f'Erro ao extrair dados do estabelecimento {idx+1}: {erro}')

            return listEmpresas
        except Exception as erro:
            raise Exception(f"Erro ao buscar e coletar dados. Motivo: {erro}")

    def coletar_dados_pesquisas(self, in_listEntradas:list) -> dict:
        """
        Fluxo geral: abre navegador, executa busca e coleta para cada entrada,
        fecha navegador e retorna resultado.

        Parâmetros:
            in_listEntradas (list): Lista de dicionários com as pesquisas a serem realizadas.

        Retorna:
            dict: Dicionário onde cada chave é o nome da aba para Excel e cada valor
                  é um pandas.DataFrame com os dados extraídos dessa pesquisa.
        """
        try:
            logging.info("Iniciando automação de consultas no Google Maps.")
            
            dictResultados = {}
            self._abrir_googlemaps()

            # Para cada entrada de pesquisa faz uma busca e processa os resultados
            for entrada in in_listEntradas:
                strTipo = entrada["tipo_estabelecimento"]
                strCidade = entrada["cidade"]
                intQtde = entrada.get("quantidade", 10)

                # Busca e coleta para uma entrada
                listEmpresas = self._buscar_coletar(strTipo, strCidade, intQtde)

                # Cria uma nova aba no Excel para os resultados desta busca
                strNomeAba = f"{strTipo}_{strCidade}".replace(' ', '_').replace(',', '')[:31]
                dictResultados[strNomeAba] = pd.DataFrame(listEmpresas)
                
                logging.info(f"Busca finalizada: '{strTipo} in {strCidade}'. Estabelecimentos capturados: {len(listEmpresas)}")
            
            # Finaliza o navegador
            logging.info("Finalizando o navegador.")
            
            self.navegador.quit()
            logging.info("Processo de coleta finalizado.")
            
            return dictResultados
        except Exception as erro:
            logging.error(f"Erro ao coletar dados pesquisas. Motivo: {erro}")
            raise