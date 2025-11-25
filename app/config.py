# from pydantic import BaseSettings
# class Settings(BaseSettings): DATABASE_URL:str; IMAP_HOST:str; IMAP_USER:str; IMAP_PASS:str; SECRET_KEY:str='secret'; class Config: env_file='.env'
# settings=Settings()
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    IMAP_HOST: str
    IMAP_PORT: int = 993
    IMAP_USER: str
    IMAP_PASS: str
    DOCUMENT_STORAGE: str = "./data/documents"
    EMAIL_POLL_INTERVAL: int = 120
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
