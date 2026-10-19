import platform
from logging import Logger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

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
