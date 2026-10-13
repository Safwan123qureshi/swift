import sys
from pathlib import Path
import uvicorn

# Ensure the backend directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

if __name__ == "__main__":
    print("=" * 60)
    print(" Swift Sign Group AI Chatbot Platform Backend")
    print(" Endpoint: http://127.0.0.1:8000")
    print(" Docs:     http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(BACKEND_DIR)
    )
