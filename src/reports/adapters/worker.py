from os import environ

from hatchet_sdk import Hatchet
from hatchet_sdk.config import ClientConfig
from pydantic import BaseModel, Field


class HatchetConfig(BaseModel):
    api_key: str = Field(alias="HATCHET_API_KEY")


HATCHET = Hatchet(
    debug=True,
    config=ClientConfig(
        token=HatchetConfig(**environ).api_key,
    ),
)
