import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    app_name: str = "Catalog Service"
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./app.db")
    )


settings = Settings()
