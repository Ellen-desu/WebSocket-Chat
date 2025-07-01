from starlette.config import Config
from typing import Literal

_config: Config = Config(".env")

debug: bool = _config("DEBUG", cast=bool, default=False)
log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = _config("LOG_LEVEL", default="INFO").upper()
database_echo: bool = _config("DATABASE_ECHO", cast=bool, default=False)
zone_info: str = _config("ZONE_INFO", default="UTC")


__all__: list[str] = ["debug", "log_level", "database_echo"]