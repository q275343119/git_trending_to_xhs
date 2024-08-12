"""
Some configurations for the project
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    config of url
    """

    url_github_trending: str = ""

    openai_app_key: str = ""
    openai_base_url: str = ""
    openai_model: str = ""

    download_dir: str = ""

    font_path: str = ""

    log_dir: str = ""
    log_file: str = ""
    log_level: str = ""
    log_to_console: bool = ""

    cookies: str = ""
    url_sign_a1: str = ""
    url_sign_sign: str = ""

    model_config = SettingsConfigDict(env_file=str(Path(__file__).parent / ".env"), env_file_encoding="utf-8",
                                      env_ignore_empty=True)


config_settings = Settings()
