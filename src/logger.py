import logging
from configs import log_level

class Formatter(logging.Formatter):
    COLORS: dict[str, str] = {
        "DEBUG": "\x1b[1;34m",  # Light Blue
        "INFO": "\x1b[1;32m",  # Light Green
        "WARNING": "\x1b[1;33m",  # Yellow
        "ERROR": "\x1b[1;91m",  # Light Red
        "CRITICAL": "\x1b[0;31m",  # Red
    }
    
    RESET: str = "\x1b[0m"
        
    def format(self, record) -> str:
        record.msg = f"{self.RESET}{record.msg}"
        color: str = self.COLORS.get(record.levelname, self.RESET)
        formatter: str = super().format(record)
        
        return f"{color}{formatter}"
        
        
def create_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("WebSocket Chat")
    logger.setLevel(log_level)
    
    formatter: Formatter = Formatter(
        fmt="[{asctime}] {levelname}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )
    
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    logger.addHandler(file_handler)
    
    return logger
        
        
logger: logging.Logger = create_logger()



