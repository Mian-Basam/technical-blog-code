from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str
    model: str = "gpt-4o-mini"
    max_history: int = 20
    system_prompt: str = (
        "You are a concise, friendly technical assistant. "
        "Prefer short answers with code examples when relevant."
    )


settings = Settings()
