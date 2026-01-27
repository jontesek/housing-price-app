from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_token: str
    environment: str = "local"
    model_name: str = "model.joblib"
    rate_limit_per_minute: int = 10

    @computed_field
    @property
    def is_local(self) -> bool:
        return self.environment == "local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore