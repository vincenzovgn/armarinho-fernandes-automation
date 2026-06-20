import platform

from logging import Logger
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from time import sleep

from chrome_automation import driver_instance

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

from config import Config
from logger import logger

class BasePage:
  def __init__(self, driver, config: Config, logger: Logger):
    self.driver = driver
    self.config: Config = config
    self.logger: Logger = logger
    self.wait = WebDriverWait(driver, self.config.SELENIUM_WAIT_TIME)

  def aguarda_pagina_completar(self) -> bool:
    is_complete = self.wait.until(lambda drive: drive.execute_script("return document.readyState") == "complete")
    return is_complete

  def get_drive(self):
    return self.driver
  
  def find_element(self, locator: tuple):
    return self.wait.until(EC.presence_of_element_located(locator))
  
  def click(self, locator):
    self.wait.until(EC.element_to_be_clickable(locator)).click()

  def inserir_texto(self, locator: tuple, text: str):
    element = self.wait.until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text)

  def select_dropdown_by_text(self, locator: tuple, text: str):
    element = self.wait.until(EC.visibility_of_element_located(locator))
    dropdown = Select(element)
    dropdown.select_by_visible_text(text)

  def limpar_text_comandos_teclados_simulados(self, locator: tuple, text: str):
    element = self.wait.until(EC.visibility_of_element_located(locator))
    element.click()
    element.clear()

    modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
    element.send_keys(modifier_key + "a")
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(text)

  def garantir_clicar(self, locator: tuple):
        elemento_clicavel = self.wait.until(EC.element_to_be_clickable(locator))
        try:
          elemento_clicavel.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", elemento_clicavel)

  def close(self):
    self.driver.quit()

class PortalFornecedor(BasePage):

  def __init__(self, driver, config: Config, logger):
    self.config = config
    self.logger = logger
    super().__init__(driver, config, self.logger)

  def load(self):
    return self.driver.get(self.config.ARMARINHO_FERNANDES_URL)

  def confirm_cookie(self):
    BUTTON_COOKIE_CONFIRM_ID = (By.ID, "rcc-confirm-button")
    element = self.find_element(BUTTON_COOKIE_CONFIRM_ID)
    element.click()

  def envia_codigo_acesso(self):
    self.logger.info('Inserindo código de acesso.')
    XPATH_INPUT_CODIGO_ACESSO = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/form/div[1]/div/div/div/input')
    XPATH_BUTTON_CODIGO_ACESSO = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/form/div[2]/button')
    CODIGO_ACESSO = self.config.ARMARINHO_FERNANDES_CODIGO_ACESSO
    self.inserir_texto(XPATH_INPUT_CODIGO_ACESSO, CODIGO_ACESSO)
    
    self.wait.until(EC.text_to_be_present_in_element_value(XPATH_INPUT_CODIGO_ACESSO, CODIGO_ACESSO))
    self.click(XPATH_BUTTON_CODIGO_ACESSO)
    self.logger.info('código de acesso, inserido com sucesso.')
  
  def login(self):
    XPATH_USUARIO = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/input')
    XPATH_PASSWORD = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/input')
    XPATH_BUTTON_LOGIN = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/button')
    
    USUARIO = self.config.ARMARINHO_FERNANDES_USUARIO
    PASSWORD = self.config.ARMARINHO_FERNANDES_PASSWORD

    self.logger.info(f'Login com o usuário {USUARIO}')
    self.inserir_texto(XPATH_USUARIO, USUARIO)
    self.inserir_texto(XPATH_PASSWORD, PASSWORD)

    self.click(XPATH_BUTTON_LOGIN)

    self.logger.info(f'login efetuado com sucesso.')

  def requisicoes(self):
    self.logger.info(f'Acessando painel de requisições, opção solicitações')

    XPATH_MENU_REQUISICOES = (By.XPATH, '//*[@id="fuse-layout"]/div/div/div/div/ul/ul[3]/li')
    XPATH_MENU_SOLICITACOES = (By.XPATH, '//*[@id="fuse-layout"]/div/div/div/div/ul/ul[3]/div/div/div/a')
    self.click(XPATH_MENU_REQUISICOES)
    self.click(XPATH_MENU_SOLICITACOES)

    self.logger.info(f'painel de solicitações acessado com sucesso')

  def solicitar_relatorio_entrada_vs_venda_saldo_estoque_lojas(self):
    periodos_em_dias = self.config.ARMARINHO_FERNANDES_RELATORIO_ENTRADA_VENDAS_SALDO_STOQUE_PERIODO_DIAS
    data_inicio = datetime.now(timezone.utc) - timedelta(days=periodos_em_dias)
    data_inicio_formatada = data_inicio.strftime("%d/%m/%Y")
    data_fim_formatada = datetime.now(timezone.utc).strftime("%d/%m/%Y")

    self.logger.info(f'solicitar relatorio de entrada vs venda e saldo estoque lojas, data de: {data_inicio_formatada} até {data_fim_formatada} - periodo: {periodos_em_dias} dias')
    XPATH_BUTTON_SOLICITAR = (By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/button')
    self.click(XPATH_BUTTON_SOLICITAR)

    self.logger.info('preenchendo o formulário para solicitar o relatório')
    XPATH_DATA_INICIO = (By.XPATH, '//*[@id="questions[0].date"]')
    XPATH_DATA_FIM = (By.XPATH, '//*[@id="questions[1].date"]')

    self.limpar_text_comandos_teclados_simulados(XPATH_DATA_INICIO, data_inicio_formatada)
    self.limpar_text_comandos_teclados_simulados(XPATH_DATA_FIM, data_fim_formatada)

    XPATH_SELECT_TIPO_SOLICITACAO = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[1]/div[2]/div/div/div/div[1]/div/div[4]/div')

    self.click(XPATH_SELECT_TIPO_SOLICITACAO)
    tipo_solicitacao = {
      'LOJA': 'Loja',
      'CD': 'CD',
      'ABDO': 'ABDO',
      'LOJA_03': 'Loja 03'
    }
    OPICOES_DE_TIPO_SOLICITACAO = '//*[@id="menu-questions[3].option"]/div[3]/ul'
    tipo_solicitacao_disponiveis = self.wait.until(EC.presence_of_element_located((By.XPATH, OPICOES_DE_TIPO_SOLICITACAO)))
    lista = tipo_solicitacao_disponiveis.find_elements(By.TAG_NAME, 'li')

    XPATH_LI_BY_TEXT = None    
    for li in lista:
      if li.text == tipo_solicitacao['LOJA']:
        XPATH_LI_BY_TEXT = f'{OPICOES_DE_TIPO_SOLICITACAO}/li[text()="{li.text}"]'
        continue

    element_li = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_LI_BY_TEXT)))
    element_li.click()
    self.logger.info(f'Tipo de solicitação: {tipo_solicitacao['LOJA']}')
    sleep(3)
    self.logger.info(f'Removendo itens de estoque do relatório')
    ITEM_ESTOQUE_SETA = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[2]/div[1]/div[2]')
    ITEM_ESTOQUE_BUTTON_EXCLUIR = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[2]/div[2]/div/div/div/div/button')
    self.garantir_clicar(ITEM_ESTOQUE_SETA)

    item_estoque_button_excluir = self.wait.until(EC.visibility_of_element_located(ITEM_ESTOQUE_BUTTON_EXCLUIR))
    item_estoque_button_excluir.click()
    self.logger.info(f'Removido opção itens de estoque')

    self.logger.info('Enviar solicitação de relatório.')
    # TO-DO criar fallback para o xpath abaixo, quando não exclui o botão de estoque o elemento button fica na div[4] conforme abaixo
    # XPATH_BUTTON_ENVIAR_SOLICITACAO = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[4]/div/button')
    XPATH_BUTTON_ENVIAR_SOLICITACAO = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[3]/div/button')
    self.logger.info(f' DEBUG: {XPATH_BUTTON_ENVIAR_SOLICITACAO}')
    # self.garantir_clicar(XPATH_BUTTON_ENVIAR_SOLICITACAO)
    self.logger.info('Solicitação de relatório enviado com sucesso')
    sleep(3)

if __name__ == "__main__":
  config = Config()
  tracing_id = uuid4()
  logger.info(f'[{tracing_id}] - start automation')
  try:
    portal_fornecedor = PortalFornecedor(driver_instance, config, logger)
    portal_fornecedor.load()
    portal_fornecedor.confirm_cookie()
    portal_fornecedor.envia_codigo_acesso()
    portal_fornecedor.login()
    portal_fornecedor.requisicoes()
    portal_fornecedor.solicitar_relatorio_entrada_vs_venda_saldo_estoque_lojas()
  except Exception as error:
    print(f'Erro: ${error}')
    logger.info(f'[{tracing_id}] - houve um erro no momento da automação')
    logger.debug(f'[{tracing_id}] - Erro automation {error}')

  finally:
    logger.info(f'[{tracing_id}] - fechando navegador')
    portal_fornecedor.close()
    logger.info(f'[{tracing_id}] - automação concluida.')