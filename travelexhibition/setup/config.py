from typing import final

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings

from travelexhibition.setup.logging import LoggingConfig


@final
class PostgresConfig(BaseSettings):
    postgres_user: str = Field(alias="POSTGRES_USER", default="postgres")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD", default="postgres")
    postgres_server: str = Field(alias="POSTGRES_SERVER", default="localhost")
    postgres_port: int = Field(alias="POSTGRES_PORT", default=5432)
    postgres_db: str = Field(alias="POSTGRES_DB", default="postgres")
    postgres_schema: str = Field(alias="POSTGRES_SCHEMA", default="postgresql+asyncpg")

    @computed_field
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.postgres_schema,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_server,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@final
class SqlEngineConfig(BaseSettings):
    echo: bool = Field(alias="ECHO", default=True)
    echo_pool: bool = Field(alias="ECHO_POOL", default=True)
    pool_size: int = Field(alias="POOL_SIZE", default=10)
    max_overflow: int = Field(alias="MAX_OVERFLOW", default=10)


@final
class AppConfig(BaseSettings):
    postgres_config: PostgresConfig = Field(default_factory=PostgresConfig)
    sql_engine_config: SqlEngineConfig = Field(default_factory=SqlEngineConfig)
    logging_config: LoggingConfig = Field(default_factory=LoggingConfig)

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"