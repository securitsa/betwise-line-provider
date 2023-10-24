from enum import Enum
from typing import Any
from urllib.parse import quote_plus

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    environment: EnvironmentTypes = Field(EnvironmentTypes.prod, validation_alias="API_ENVIRONMENT")
    debug: bool = True
    title: str = "Betwise Line Provider service"
    version: str = "0.1.0"
    db_driver_name: str = "postgresql+asyncpg"
    db_host: str = Field("btw-postgres-line-provider", validation_alias="DATABASE_HOST")
    db_username: str = Field("betwise", validation_alias="DATABASE_USERNAME")
    db_password: SecretStr = Field("betwise", validation_alias="DATABASE_PASSWORD")
    db_database: str = Field("betwise", validation_alias="DATABASE_NAME")
    valid_jwt_secret: str = Field("jwt_secret_key", validation_alias="JWT_SECRET_KEY")
    events_queue: str = "events-queue-dev"
    test_sqs_config: dict = {
        "endpoint_url": "http://sqs:9324",
        "region_name": "elasticmq",
        "aws_secret_access_key": "x",
        "aws_access_key_id": "x",
        "use_ssl": False,
    }

    @field_validator("db_password")
    @classmethod
    def parse_db_password(cls, v):
        return SecretStr(quote_plus(v.get_secret_value()))

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

    @property
    def db_creds(self):
        return {
            "drivername": self.db_driver_name,
            "username": self.db_username,
            "host": self.db_host,
            "database": self.db_database,
            "password": self.db_password.get_secret_value(),
        }


class TestSettings(BaseAppSettings):
    title: str = "Test environment - Betwise Line Provider service"
    db_host: str = Field("btw-postgres-line-provider-test", validation_alias="DATABASE_HOST")
    db_username: str = Field("betwise", validation_alias="DATABASE_USERNAME")
    db_password: SecretStr = Field("betwise", validation_alias="DATABASE_PASSWORD")
    db_database: str = Field("betwise", validation_alias="DATABASE_NAME")


class LocalSettings(BaseAppSettings):
    title: str = "Local environment - Betwise Line Provider service"


class DevelopmentSettings(BaseAppSettings):
    title: str = "Development environment - Betwise Line Provider service"


class ProductionSettings(BaseAppSettings):
    debug: bool = False
    events_queue: str = "events-queue"
