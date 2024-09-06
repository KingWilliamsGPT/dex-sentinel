'''Settings file for the project.'''

from dotenv import load_dotenv
import os

from bot import bot

# Load environment variables from .env file
ENVIRONMENT_LOADED = load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')