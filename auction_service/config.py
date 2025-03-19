from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.local', extra='ignore', case_sensitive=False
    )

    # PostgreSQL database settings
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str = None  # Password can be optional

    # Other settings (optional)
    debug: bool = False

    @property
    def database_url(self) -> str:
        """Construct the async database URL."""
        if self.db_password:
            return (
                f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:'
                f'{self.db_port}/{self.db_name}'
            )
        else:
            return (
                f'postgresql://{self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}'
            )

    @property
    def async_database_url(self) -> str:
        """Construct the async database URL for asyncpg."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


settings = Settings()

if __name__ == '__main__':
    print(settings.model_dump())
    print(settings.database_url)
    print(settings.async_database_url)
