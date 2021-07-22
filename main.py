import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.HTTP_PORT, log_level="info")