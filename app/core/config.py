from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    NOTES_DATA_SERVICE_PORT: int = 8003
    APP_NAME: str = 'NoteFlow Notes Data Service'
    APP_VERSION: str = '0.1.0'
    DEBUG: bool = False

    DATABASE_HOST: str = '127.0.0.1'
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = 'noteflow'
    DATABASE_USER: str = 'noteflow_user'
    DATABASE_PASSWORD: str = 'noteflow_pass'

    @property
    def DATABASE_URL(self) -> str:
        return (
            f'postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )


settings = Settings()
