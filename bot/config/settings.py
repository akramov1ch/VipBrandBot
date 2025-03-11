import os


BASE_SERVER_URL = os.getenv("BASE_SERVER_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_TG_ID = int(os.getenv("OWNER_TG_ID"))
BASE_CHANNEL_ID = int(os.getenv("BASE_CHANNEL_ID"))

DEFAULT_LANGUAGE = "uz"
LANGUAGES = {
    "En 🇺🇸": "en",
    "Ru 🇷🇺": "ru",
    "Uz 🇺🇿": "uz",
}

REDIS_EXPIRE_SECONDS = 10 * 24 * 60 * 60
