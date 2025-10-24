from typing import final

from pydantic_settings import BaseSettings


@final
class PostgresConfig(BaseSettings):
    login: str
    password: str
    database: str
    port: str
    host: str
