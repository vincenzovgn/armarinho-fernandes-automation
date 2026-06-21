from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class BrowserOptions(ABC):
  @abstractmethod
  def get_options(self) -> Options:
    pass

class ChromeAutomationOptions(BrowserOptions):
  def get_options(self) -> Options:
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1000")

    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    return options
  
class WebDriveFactory:
  @staticmethod
  def create_chrome_driver(browse_options: BrowserOptions) -> webdriver.Chrome:
    options = browse_options.get_options()
    return webdriver.Chrome(options)

class WebAutomation:
  def __init__(self, driver: webdriver.Chrome):
    self.driver = driver

  def navigate_to(self, url: str):
    print(f'Navegando para: {url}')
    self.driver.get(url)

  def close(self):
    self.driver.quit()

chrome_config = ChromeAutomationOptions()
driver_instance = WebDriveFactory.create_chrome_driver(chrome_config)