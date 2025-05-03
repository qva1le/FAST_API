from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.hotels import router as router_hotels
from src.config import settings
from src.database import engine
from src.config import settings
print(f"{settings.DB_URL=}")


app = FastAPI()

app.include_router(router_hotels)


if __name__ == '__main__':
    uvicorn.run("main:app" ,reload=True)