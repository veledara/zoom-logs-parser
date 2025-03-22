from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    input_dir: str = "logs"
    output_dir: str = "output"
    output_csv_file: str = "full_report.csv"
    output_xlsx_file: str = "full_report.xlsx"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
