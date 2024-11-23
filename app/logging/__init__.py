import logging
from logging.handlers import TimedRotatingFileHandler
from app.settings import LOG_FILE_LOCATION
from uvicorn.logging import ColourizedFormatter


client_logger = logging.getLogger("client_logger")
client_logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_formatter = ColourizedFormatter(
    "%(levelprefix)s CLIENT CALL - %(message)s",
    use_colors=True
)
console_handler.setFormatter(console_formatter)

# File Handler
file_handler = TimedRotatingFileHandler(LOG_FILE_LOCATION)
file_formatter = logging.Formatter(
    "time: %(asctime)s, %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)


client_logger.addHandler(console_handler)
client_logger.addHandler(file_handler)