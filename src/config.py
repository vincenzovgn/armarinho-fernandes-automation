from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
  APP_ENV: str = Field(alias='APP_ENV', default='local')
  LOG_LEVEL: str = Field(alias='LOG_LEVEL', default='DEBUG')

  SELENIUM_WAIT_TIME: int = Field(alias='SELENIUM_WAIT_TIME', default= 10)

  ARMARINHO_FERNANDES_CODIGO_ACESSO: str = Field(alias='ARMARINHO_FERNANDES_CODIGO_ACESSO', default='AF')
  ARMARINHO_FERNANDES_URL: str = Field(alias='ARMARINHO_FERNANDES_URL', default='https://portalfornecedor.armarinhos-fernando.com.br/login')
  ARMARINHO_FERNANDES_USUARIO: str = Field(alias='ARMARINHO_FERNANDES_USUARIO')
  ARMARINHO_FERNANDES_PASSWORD: str = Field(alias='ARMARINHO_FERNANDES_PASSWORD')

  model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore"
  )