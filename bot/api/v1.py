from fastapi import APIRouter, Body
from ..utils import get_bot

from telebot import types

router = APIRouter()


@router.post("/bot")
async def webhook(body=Body(...)):
    bot = await get_bot()
    updates = types.Update.de_json(body)
    bot.process_new_updates([updates])
    return 200
