import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings and configuration.
    Reads from a .env file at the project root.
    """
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set in .env file.")

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    STATIC_DIR = BASE_DIR / "static"
    VIDEO_DIR = STATIC_DIR / "videos"
    TEMP_SCRIPT_DIR = BASE_DIR / "temp_scripts"

    @staticmethod
    def setup_directories():
        """Creates necessary directories if they don't exist."""
        Settings.STATIC_DIR.mkdir(exist_ok=True)
        Settings.VIDEO_DIR.mkdir(exist_ok=True)
        Settings.TEMP_SCRIPT_DIR.mkdir(exist_ok=True)

settings = Settings()
