import telebot
from app.utils import get_db
from app.core.config import settings
from .enums import BotCommands

from content.manager import ContentManager

from chats import crud as chat_crud
from chats import schemas as chat_schemas

bot = None


async def initialize_bot_function(_bot: telebot.TeleBot) -> None:
    @_bot.message_handler(commands=['start'])
    def start_message(message):

        db = get_db()
        chat_crud.create_chat_message(
            db,
            chat_schemas.ChatMessageCreate(
                text=message.text,
                chat_id=message.chat.id,
        )
        )

        db.close()

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

        for command in BotCommands:

            button = telebot.types.KeyboardButton(str(command.value))
            markup.add(button)

        _bot.send_message(message.chat.id, "Hi, I'm LSD bot.", reply_markup=markup)

    @_bot.message_handler(content_types=["text"])
    def handle_text(message):
        db = get_db()
        chat_crud.create_chat_message(
            db,
            chat_schemas.ChatMessageCreate(
                text=message.text,
                chat_id=message.chat.id,
            )
        )

        manager = ContentManager(message.chat.id, db)

        content = manager.get_content(BotCommands(message.text).name, message.chat.id)

        _bot.send_message(message.chat.id, content)


async def initialize_bot() -> telebot.TeleBot:

    _bot = telebot.TeleBot(settings.BOT_TOKEN)

    _bot.remove_webhook()
    _bot.set_webhook(url=settings.BOT_WEB_HOOK_URL)

    await initialize_bot_function(_bot)

    return _bot


async def get_bot() -> telebot.TeleBot:
    global bot
    if bot is None:
        bot = await initialize_bot()
    return bot
