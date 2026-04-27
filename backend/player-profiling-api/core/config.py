from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Player Profiling System"
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]
    data_mode: str = "mock-first"


settings = Settings()
