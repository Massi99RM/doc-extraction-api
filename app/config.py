from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    elastic_src: str
    claude_api_key: str
    azure_url: str
    azure_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()