import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext

# URL to send data
URL = "http://localhost:8000/create-character-list"

gender = ['M', 'W']
races = {
    "Дварф": 'dwarf',
    "Эльф": 'elves',
    'Полурослик': "halfling",
    'Человек': "human",
    'Драконорожденный': "dragonborn",
    'Гном': "gnom",
    'Полуэльф': "halfelf",
    'Полуорк': "halforc",
    'Тифлинг': "tiefling"
}

# State definitions for the conversation
CHOOSING_RACE, CHOOSING_CLASS, CHOOSING_GENDER = range(3)

def get_key_by_value(dictionary, value):
    result = next((key for key, val in dictionary.items() if val == value), None)
    return result


def start(update: Update, context: CallbackContext) -> int:
    """Handles the /start command and asks user to choose a race."""
    keyboard = [[InlineKeyboardButton(r, callback_data=r)] for r in races.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите расу для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_RACE

def choosing_race(update: Update, context: CallbackContext) -> int:
    """Handles the choice of race by the user."""
    query = update.callback_query
    query.answer()

    chosen_race = query.data
    context.user_data['race'] = races[chosen_race]

    # Provide class options for the chosen race
    with open(f"not_in_use/race/{races[chosen_race]}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    class_options = data.get('class_options', [])

    keyboard = [[InlineKeyboardButton(c, callback_data=c)] for c in class_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите класс для вашего персонажа:")
    query.message.reply_text("Выберите класс:", reply_markup=reply_markup)
    
    return CHOOSING_CLASS

def choosing_class(update: Update, context: CallbackContext) -> int:
    """Handles the choice of class by the user."""
    query = update.callback_query
    query.answer()

    chosen_class = query.data
    context.user_data['class'] = chosen_class

    # Ask for gender
    keyboard = [[InlineKeyboardButton(g, callback_data=g)] for g in gender]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите пол для вашего персонажа:")
    query.message.reply_text("Выберите пол:", reply_markup=reply_markup)
    
    return CHOOSING_GENDER

def choosing_gender(update: Update, context: CallbackContext) -> None:
    """Handles the choice of gender by the user."""
    query = update.callback_query
    query.answer()

    chosen_gender = query.data
    context.user_data['gender'] = chosen_gender

    # All choices have been made, send the data to the server
    data = {
        "gender": context.user_data['gender'],
        "rac": get_key_by_value(races, context.user_data['race']),
        "clas": context.user_data['class']
    }

    print(data)

    try:
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            result = response.text
            if len(result) > 4000:
                result1 = result[:4000]
                query.message.reply_text(f"Запрос успешно отправлен! Ответ сервера: {result1}")
                result2 = result.replace(result1, '')[:4000]
                query.message.reply_text(result2)
                result3 = result2[4000:]
                # query.message.reply_text(result3)
            else:
                query.message.reply_text(f"Запрос успешно отправлен! Ответ сервера: {result}")
        else:
            query.message.reply_text(f"Ошибка при отправке запроса. Код ответа: {response.status_code}")
    except Exception as e:
        query.message.reply_text(f"Произошла ошибка: {str(e)}")

    return ConversationHandler.END

def main():
    """Main function to run the bot."""
    updater = Updater("8154427178:AAEJPcc0xXiRt43YgCNs_hKKqVmibGoyAAA")

    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_RACE: [CallbackQueryHandler(choosing_race)],
            CHOOSING_CLASS: [CallbackQueryHandler(choosing_class)],
            CHOOSING_GENDER: [CallbackQueryHandler(choosing_gender)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conversation_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
