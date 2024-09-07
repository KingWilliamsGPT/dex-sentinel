'''Settings file for the project.'''


from telegram.constants import MessageLimit

from environs import Env
from logging import INFO, WARNING, basicConfig, getLogger



# Load environment variables from .env file
env = Env()
env.read_env()



# Create a class for storing settings
class Settings:
    PORT: int = env.int("PORT")
    HOST: str = env.str("HOST", "0.0.0.0")
    DEBUG: bool = env.bool("DEBUG", False)
    LOG_LEVEL: int = INFO if DEBUG else WARNING

    SECRET_TOKEN: str = env.str("SECRET_TOKEN")
     
    BOT_WEB_URL: str = env.str("BOT_WEB_URL")
    HEALTH_URL: str= env.str("HEALTH_URL", "/health/")
    WEBHOOK_URL: str = env.str("WEBHOOK_URL", "/webhook/")

    LOG_CHAT_IDS: list[int] = [ int(i.strip()) for i in env.list("LOG_CHAT_IDS", []) ]
    DEVELOPER_CHAT_IDS: list[int] = [ int(i.strip()) for i in env.list("DEVELOPER_CHAT_IDS", []) ]

    MIN_MESSAGE_LENGTH: int = MessageLimit.MIN_TEXT_LENGTH
    MAX_MESSAGE_LENGTH: int = MessageLimit.MAX_TEXT_LENGTH
    ALLOWED_TAGS = [ "a", "b", "code", "i", "pre" ]




def get_settings() -> Settings:
    settings = Settings()
    return settings


# Setup logging
basicConfig( format = "%(asctime)s - %(name)s -%(levelname)s - %(message)s", level = Settings.LOG_LEVEL )


def get_logger(name: str):
    logger = getLogger(name)
    return logger
logger = get_logger(__name__)

