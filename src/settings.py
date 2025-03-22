from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    input_dir: str = "logs"
    output_dir: str = "output"
    output_file: str = "full_report.csv"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
