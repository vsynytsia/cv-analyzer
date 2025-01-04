from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    API_V1_STR: str = "/v1"

    PROJECT_NAME: str = "CV Analysis Platform"
    PROJECT_DESCRIPTION: str = "CV Analysis Platform made by Vlad & Katyushka"
    PROJECT_VERSION: str = "0.1"

    DOU_VACANCIES_BASE_URL: str = "https://jobs.dou.ua/vacancies/"
    DJINNI_VACANCIES_BASE_URL: str = "https://djinni.co/jobs/"
    MAX_VACANCIES_PER_SOURCE: int = 25

    MAX_UPLOAD_FILE_SIZE_BYTES: int = 1_000_000

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    GOOGLE_GENAI_API_KEY: str


settings = Settings()
