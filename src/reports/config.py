from importlib.resources import files
from os import environ

from alembic.config import Config as AlembicConfig
from pydantic import BaseModel, ConfigDict, Field

from reports.adapters.worker import HatchetConfig


def get_alembic_config() -> AlembicConfig:
    config_object = AlembicConfig()
    script_location = str(files("reports.adapters.persistence.alembic.migrations"))
    config_object.set_main_option("script_location", script_location)
    config_object.set_main_option("sqlalchemy.url", PostgresConfig(**environ).dsn)
    return config_object


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: str = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def dsn(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RabbitConfig(BaseModel):
    host: str = Field(alias="RABBIT_HOST")
    port: str = Field(alias="RABBIT_PORT")
    user: str = Field(alias="RABBIT_USER")
    password: str = Field(alias="RABBIT_PASSWORD")

    @property
    def dsn(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class UvicornConfig(BaseModel):
    app_path: str = Field(
        alias="UVICORN_APP_PATH", default="reports.http_app:get_fastapi_app"
    )
    server_host: str = Field(alias="UVICORN_SERVER_HOST")
    server_port: int = Field(alias="UVICORN_SERVER_PORT")


class WorkerAppConfig(BaseModel):
    app_path: str = Field(
        alias="WORKER_APP_PATH", default="reports.worker_app:get_hathcet_app"
    )


class ApiConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**environ))
    hatchet: HatchetConfig = Field(default_factory=lambda: HatchetConfig(**environ))


class WorkerConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**environ))
    rabbit: RabbitConfig = Field(default_factory=lambda: RabbitConfig(**environ))
    hatchet: HatchetConfig = Field(default_factory=lambda: HatchetConfig(**environ))


class CliConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    alembic: AlembicConfig = Field(default_factory=get_alembic_config)
    uvicorn: UvicornConfig = Field(default_factory=lambda: UvicornConfig(**environ))
    worker: WorkerAppConfig = Field(default_factory=lambda: WorkerAppConfig(**environ))
