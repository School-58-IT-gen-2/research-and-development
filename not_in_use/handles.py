from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext
from tg_bot.utils import format_character_card, escape_markdown_v2, get_key_by_value
from db.db_source import DBSource
from config import SUPABASE_URL, SUPABASE_KEY
import requests

CHOOSING_CLASS, CHOOSING_RACE, CHOOSING_CHARACTERISTICS, CHOOSING_SKILLS, CHOOSING_GENDER = range(5)
URL = "https://rnd.questhub.pro/create-character-list"
db = DBSource(SUPABASE_URL, SUPABASE_KEY)
db.connect()

RACES = {
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

CLASSES = {
    'Следопыт': 'pathfinder',
    "Варвар": "barbarian",
    "Бард": "bard",
    "Плут": "dodger",
    "Друид": "druid",
    "Колдун": "magician",
    "Монах": "monk",
    "Паладин": "paladin",
    "Жрец": "priest",
    "Маг": "warlock",
    "Воин": "warrior",
    "Волшебник": "wizzard"
}

GENDER_OPTIONS = ['M', 'W']

def start(update: Update, context: CallbackContext) -> int:

    keyboard = [[InlineKeyboardButton(class_, callback_data=class_)] for class_ in CLASSES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите класс для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_CLASS


def choosing_class(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    context.user_data['class'] = query.data

    keyboard = [[InlineKeyboardButton(race, callback_data=race)] for race in RACES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите расу для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_RACE

def choosing_race(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    chosen_race = query.data
    context.user_data['race'] = RACES[chosen_race]

    race_data = db.get_race_data_by_name(RACES[chosen_race])
    class_options = race_data.get('class_options', [])

    keyboard = []
    for cls in CLASSES.keys():
        label = f"⭐ {cls} (Рекомендуется)" if cls in class_options else cls
        keyboard.append([InlineKeyboardButton(label, callback_data=cls)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите класс для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_CHARACTERISTICS
def choosing_characteristics(update: Update, context: CallbackContext) -> int:
    """Обработка выбора хара��теристик."""
    query = update.callback_query
    query.answer()
    context.user_data['characteristics'] = query.data


    return CHOOSING_SKILLS

def choosing_skills(update: Update, context: CallbackContext) -> int:
    """Обработка выбора навыков."""
    query = update.callback_query
    query.answer()
    context.user_data['skills'] = query.data

    return CHOOSING_GENDER

def choosing_gender(update: Update, context: CallbackContext) -> None:
    """Handles gender selection and submits the data to the server."""
    query = update.callback_query
    query.answer()
    context.user_data['gender'] = query.data

    data = {
        "gender": context.user_data['gender'],
        "race": get_key_by_value(RACES, context.user_data['race']),
        "character_class": context.user_data['class']
    }

    try:
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            character_data = response.json()
            # print("Character data from server:", character_data)  # Отладка
            formatted_response = format_character_card(character_data)
            formatted_response = escape_markdown_v2(formatted_response)  # Экранируем текст
            query.message.reply_text(formatted_response, parse_mode='MarkdownV2')
        else:
            query.message.reply_text(f"Ошибка сервера: {response.status_code}")
    except Exception as e:
        query.message.reply_text(f"Произошла ошибка: {str(e)}")

    query.message.reply_text("Если хотите создать нового персонажа, введите /start.")


    return ConversationHandler.END



def get_conversation_handler():
    """Возвращает ConversationHandler для бота."""
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_CLASS: [CallbackQueryHandler(choosing_class)],
            CHOOSING_RACE: [CallbackQueryHandler(choosing_race)],
            CHOOSING_CHARACTERISTICS: [CallbackQueryHandler(choosing_characteristics)],
            CHOOSING_SKILLS: [choosing_skills],
            CHOOSING_GENDER: [CallbackQueryHandler(choosing_gender)]
        },
        fallbacks=[]
    )