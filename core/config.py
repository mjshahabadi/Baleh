import os
from dotenv import load_dotenv

DB_SCHEMA = "baleh"

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("988312613:vllwDledtWgjpM1YRPpg9hycyY0jGlU4-yM")

    DB_DRIVER = os.getenv("DB_DRIVER", r"SQL Server")
    DB_SERVER = os.getenv("DB_SERVER", r"WIN-8F5G6TCFF1J\SQL2022")
    DB_NAME = os.getenv("DB_NAME", "Crypto")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    
    BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"
    DEBUG = os.getenv("DEBUG", "True") == "True"