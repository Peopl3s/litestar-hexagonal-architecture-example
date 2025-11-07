from advanced_alchemy.extensions.litestar import AsyncSessionConfig, SQLAlchemyAsyncConfig

from travelexhibition.config import PostgresConfig


def get_sqlalchemy_config(psql_config: PostgresConfig) -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=(
            f"{psql_config.postgres_schema}://{psql_config.postgres_user}:{psql_config.postgres_password}"
            f"@{psql_config.postgres_server}:{psql_config.postgres_port}/{psql_config.postgres_db}"
        ),
        session_config=AsyncSessionConfig(
            autoflush=False,
            expire_on_commit=False,
        ),
        before_send_handler="autocommit",
    )
