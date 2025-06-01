from os import environ

from pydantic import BaseModel, Field, ConfigDict

from reports.adapters.worker import HatchetConfig


class PostgresTestConfig(BaseModel):
    host: str = Field(alias="POSTGRES_TEST_HOST")
    port: str = Field(alias="POSTGRES_TEST_PORT")
    user: str = Field(alias="POSTGRES_TEST_USER")
    password: str = Field(alias="POSTGRES_TEST_PASSWORD")
    database: str = Field(alias="POSTGRES_TEST_DB")

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )


class ApiTestConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    postgres: PostgresTestConfig = Field(default_factory=lambda: PostgresTestConfig(**environ))
    hatchet: HatchetConfig = Field(default_factory=lambda: HatchetConfig(**environ))
