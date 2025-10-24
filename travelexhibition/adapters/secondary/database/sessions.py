from advanced_alchemy.config import AsyncSessionConfig, SQLAlchemyAsyncConfig

from travelexhibition.config import PostgresConfig


def get_sqlalchemy_config(psql_config: PostgresConfig) -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=(
            f"postgresql+psycopg://{psql_config.login}:{psql_config.password}"
            f"@{psql_config.host}:{psql_config.port}/{psql_config.database}"
        ),
        session_config=AsyncSessionConfig(
            autoflush=False,
            expire_on_commit=False,
        ),
    )
