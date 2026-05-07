from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str = ""
    supabase_service_role_key: str = ""
    cors_origins: str = "http://localhost:3000"
    llm_provider: str = "stub"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    kite_api_key: str = ""
    kite_access_token: str = ""


settings = Settings()
