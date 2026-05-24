import platform

from chrome_automation import driver_instance

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from config import Config

class BasePage:
  def __init__(self, driver, config: Config):
    self.driver = driver
    self.config = config
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

  def close(self):
    self.driver.quit()

class PortalFornecedor(BasePage):

  BUTTON_COOKIE_CONFIRM_ID = "rcc-confirm-button"

  def __init__(self, driver, config: Config):
    self.config = config
    super().__init__(driver, config)

  def load(self):
    return self.driver.get(self.config.ARMARINHO_FERNANDES_URL)

  def confirm_cookie(self):
    element = self.find_element((By.ID, self.BUTTON_COOKIE_CONFIRM_ID))
    element.click()

  def envia_codigo_acesso(self):
    XPATH_INPUT_CODIGO_ACESSO = '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/form/div[1]/div/div/div/input'
    XPATH_BUTTON_CODIGO_ACESSO = '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/form/div[2]/button'
    CODIGO_ACESSO = self.config.ARMARINHO_FERNANDES_CODIGO_ACESSO
    self.inserir_texto((By.XPATH, XPATH_INPUT_CODIGO_ACESSO), 'AF')
    
    self.wait.until(EC.text_to_be_present_in_element_value((By.XPATH, XPATH_INPUT_CODIGO_ACESSO), CODIGO_ACESSO))
    self.click((By.XPATH, XPATH_BUTTON_CODIGO_ACESSO))
  
  def login(self):
    XPATH_USUARIO = '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/input'
    XPATH_PASSWORD = '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/input'
    XPATH_BUTTON_LOGIN = '//*[@id="fuse-main"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/form/button'
    
    USUARIO = self.config.ARMARINHO_FERNANDES_USUARIO
    PASSWORD = self.config.ARMARINHO_FERNANDES_PASSWORD
    self.inserir_texto((By.XPATH, XPATH_USUARIO), USUARIO)
    self.inserir_texto((By.XPATH, XPATH_PASSWORD), PASSWORD)

    self.click((By.XPATH, XPATH_BUTTON_LOGIN))

  def requisicoes(self):
    XPATH_MENU_REQUISICOES = '//*[@id="fuse-layout"]/div/div/div/div/ul/ul[3]/li'
    XPATH_MENU_SOLICITACOES = '//*[@id="fuse-layout"]/div/div/div/div/ul/ul[3]/div/div/div/a'
    self.click((By.XPATH, XPATH_MENU_REQUISICOES))
    self.click((By.XPATH, XPATH_MENU_SOLICITACOES))

  def solicitar_relatorio_entrada_vs_venda_saldo_estoque_lojas(self):
    XPATH_BUTTON_SOLICITAR = '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/button'
    self.click((By.XPATH, XPATH_BUTTON_SOLICITAR))

    XPATH_DATA_INICIO = '//*[@id="questions[0].date"]'
    XPATH_DATA_FIM = '//*[@id="questions[1].date"]'

    self.limpar_text_comandos_teclados_simulados((By.XPATH, XPATH_DATA_INICIO),'20/05/2026')
    self.limpar_text_comandos_teclados_simulados((By.XPATH, XPATH_DATA_FIM), '23/05/2026')

    XPATH_SELECT_TIPO_SOLICITACAO = '/html/body/div[4]/div[3]/div/div[2]/div/form/div[1]/div[2]/div/div/div/div[1]/div/div[4]/div'

    self.click((By.XPATH, XPATH_SELECT_TIPO_SOLICITACAO))
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

    ITEM_ESTOQUE_SETA = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[2]/div[1]/div[2]')
    ITEM_ESTOQUE_BUTTON_EXCLUIR = (By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/form/div[2]/div[2]/div/div/div/div/button')

    element_seta = self.wait.until(EC.element_to_be_clickable(ITEM_ESTOQUE_SETA))

    try:
      element_seta.click()
    except ElementClickInterceptedException:
      print(self.driver.execute_script)
      self.driver.execute_script("arguments[0].click();", element_seta)

    self.wait.until(EC.visibility_of_element_located(ITEM_ESTOQUE_BUTTON_EXCLUIR))

if __name__ == "__main__":
  config = Config()
  try:
    portal_fornecedor = PortalFornecedor(driver_instance, config)
    portal_fornecedor.load()
    portal_fornecedor.confirm_cookie()
    portal_fornecedor.envia_codigo_acesso()
    portal_fornecedor.login()
    portal_fornecedor.requisicoes()
    portal_fornecedor.solicitar_relatorio_entrada_vs_venda_saldo_estoque_lojas()
  
  except Exception as error:
    print(f'Erro: ${error}')

  finally:
    portal_fornecedor.close()
    # automation.close()