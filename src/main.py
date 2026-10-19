import platform
import traceback
import tracemalloc

from logging import Logger
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from time import sleep, perf_counter

from chrome_automation import driver_instance

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

from config import Config
from logger import logger
from portal_fornecedor import PortalFornecedor
   
if __name__ == "__main__":
  tracemalloc.start()
  config = Config()
  tracing_id = uuid4()
  inicio = perf_counter()
  logger.info(f'[{tracing_id}] - start automation {config.APP_ENV} - {config.ARMARINHO_FERNANDES_USUARIO}')
  try:
    
    portal_fornecedor = PortalFornecedor(driver_instance, config, logger)
    portal_fornecedor.load()
    portal_fornecedor.confirm_cookie()
    portal_fornecedor.envia_codigo_acesso()
    portal_fornecedor.login()
    portal_fornecedor.extrair_relatorio_por_empresa()
    # portal_fornecedor.requisicoes()
    # portal_fornecedor.solicitar_relatorio_entrada_vs_venda_saldo_estoque_lojas()
  except Exception as error:
    logger.info(f'[{tracing_id}] - houve um erro no momento da automação')
    logger.debug(f'[{tracing_id}] - Erro automation {error}')
  finally:
    logger.info(f'[{tracing_id}] - fechando navegador')
    portal_fornecedor.close()
    fim = perf_counter()
    logger.info(f'[{tracing_id}] - automação concluida. tempo de execução: {(fim - inicio):.3f}s')
    atual, pico = tracemalloc.get_traced_memory()
    logger.info(f"Uso atual de memória: {atual / 1024 / 1024:.2f} MB")
    logger.info(f"Pico de memória: {pico / 1024 / 1024:.2f} MB")