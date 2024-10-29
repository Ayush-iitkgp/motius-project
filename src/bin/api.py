import uvicorn

from src import settings

if __name__ == "__main__":
    uvicorn.run("src.routes.chat_router:app", host=settings.HOST, port=settings.PORT)
