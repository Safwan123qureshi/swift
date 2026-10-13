import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in backend, project root, and current working directory
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
ROOT_DIR = BACKEND_DIR.parent

backend_env_path = BACKEND_DIR / ".env"
root_env_path = ROOT_DIR / ".env"
cwd_env_path = Path.cwd() / ".env"

for env_file in [backend_env_path, root_env_path, cwd_env_path]:
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)

# Fallback default search
load_dotenv(override=False)

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()