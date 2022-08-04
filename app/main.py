from fastapi import FastAPI
from bot.api.v1 import router as bot_router

from bot import utils as bot_utils


def configure_app(application: FastAPI) -> None:

    application.include_router(bot_router)


app = FastAPI()
configure_app(app)


@app.on_event('startup')
async def startup():
    await bot_utils.initialize_bot()
