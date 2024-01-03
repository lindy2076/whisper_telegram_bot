from os import environ, path
from dotenv import load_dotenv


dotenv_path = path.join(path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


class Config:
    """default config"""
    BOT_TOKEN: str = environ.get("BOT_TOKEN", "")
    ADMIN_ID: str = environ.get("ADMIN_ID", "")
    DEBUG: str = environ.get("DEBUG", "True")
