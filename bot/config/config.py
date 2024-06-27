from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    ADD_TAPS_ON_TURBO: list[int] = [10, 15]
    AUTO_UPGRADE: bool = False
    MAX_UPGRADE_LEVEL: int = 1

    APPLY_DAILY_ENERGY: bool = True
    APPLY_DAILY_TURBO: bool = True

    TAPS_COUNT: list[int] = [5, 7]

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()
