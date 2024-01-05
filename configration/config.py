from pydantic_settings import BaseSettings
from datetime import date
import os


class FacultySettings(BaseSettings):
    application: str = "Faculty Management System"
    webmaster: str = "dshivendra"
    created: date = "2024-01-05"


class ServerSettings(BaseSettings):
    production_server: str
    prod_port: int
    development_server: str
    dev_port: int

    class Config:
        env_file = os.getcwd() + "/configuration/erp_settings.properties"
