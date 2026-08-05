from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_uri: str
    elastic_src: str
    claude_api_key: str
    azure_url: str
    azure_key: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()