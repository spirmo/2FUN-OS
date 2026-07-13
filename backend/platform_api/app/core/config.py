from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
JWT_SECRET = os.getenv("JWT_SECRET", "")
API_BASE_URL = os.getenv("API_BASE_URL", "")
APP_SCHEME = os.getenv("APP_SCHEME", "twofun")
