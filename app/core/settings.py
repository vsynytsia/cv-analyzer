from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    PROJECT_NAME: str = "CV Analysis Platform"
    PROJECT_DESCRIPTION: str = "CV Analysis Platform made by Vlad & Katyushka"
    PROJECT_VERSION: str = "0.1"

    MAX_UPLOAD_FILE_SIZE_BYTES: int = 1_000_000

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    GOOGLE_GENAI_API_KEY: str


settings = Settings()
