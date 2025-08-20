from dotenv import load_dotenv; load_dotenv()
import os

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    PHANTOMBUSTER_API_KEY: str | None = os.getenv("PHANTOMBUSTER_API_KEY")

def get_settings() -> Settings:
    return Settings()
