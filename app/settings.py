from pydantic import BaseSettings, IPvAnyAddress

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    AMOUNT_LIMIT_10SEC: int
    AMOUNT_LIMIT_1MIN: int
    MULTI: bool

    APP_PORT: int
    APP_HOST: str
    DEBUG: bool
    RELOAD: bool