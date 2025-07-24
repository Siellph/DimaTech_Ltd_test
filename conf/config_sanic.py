from sanic.config import Config


class MySanicConfig(Config):
    FALLBACK_ERROR_FORMAT: str = 'html'
    REQUEST_TIMEOUT: int = 60
