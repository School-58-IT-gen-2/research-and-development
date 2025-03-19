from telegram.ext import Updater
from config import BOT_TOKEN
from tg_bot.handlers import get_conversation_handler

def main():
    """Запуск Telegram-бота."""
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = get_conversation_handler()
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()