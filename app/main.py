from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from bot.api.v1 import router as bot_router

from bot import utils as bot_utils


def configure_app(application: FastAPI) -> None:

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(bot_router)


app = FastAPI()
configure_app(app)


@app.on_event('startup')
async def startup():
    await bot_utils.initialize_bot()
