import telebot
from app.core.config import settings
from .enums import BotCommands

bot = None


async def initialize_bot_function(_bot: telebot.TeleBot) -> None:
    @_bot.message_handler(commands=['start'])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for command in BotCommands:

            button = telebot.types.KeyboardButton(str(command.value))
            markup.add(button)

        _bot.send_message(message.chat.id, "Привет, я бот для получения комплиментов", reply_markup=markup)

    @_bot.message_handler(content_types=["text"])
    def handle_text(message):
        if message.text == "👋 Поздороваться":
            _bot.send_message(message.chat.id, "Привет, я бот для получения комплиментов")
        elif message.text == "❓ Задать вопрос":
            _bot.send_message(message.chat.id, "Напишите ваш вопрос")
        else:
            _bot.send_message(message.chat.id, "Я не знаю такой команды")


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
