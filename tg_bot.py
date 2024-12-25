import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext
import re



# Constants
URL = "http://localhost:8000/create-character-list"
GENDER_OPTIONS = ['M', 'W']
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

clases = {
    'Следопыт':'pathfinder',
    "Варвар":"barbarian",
    "Бард":"bard",
    "Плут":"dodger",
    "Друид":"druid",
    "Колдун":"magician",
    "Монах":"monk",
    "Паладин":"paladin",
    "Жрец":"priest",
    "Маг":"warlock",
    "Воин":"warrior",
    "Волшебник":"wizzard"
}


TRANSLATIONS = {
    "type": "Тип",
    "damage": "Урон",
    "damage_type": "Тип урона",
    "properties": "Свойства",
    "weight": "Вес",
    "cost": "Цена",
    "ac_base": "Базовая защита (AC)",
    "dex_bonus": "Бонус Ловкости",
    "max_dex_bonus": "Макс. бонус Ловкости",
    "stealth_disadvantage": "Помеха скрытности",
    "weapons": "Оружие",
    "armor": "Броня",
    "name": "Имя",
    "surname": "Фамилия",
    "race": "Раса",
    "character_class": "Класс",
    "lvl": "Уровень",
    "hp": "Хиты",
    "speed": "Скорость",
    "worldview": "Мировоззрение",
    "initiative": "Инициатива",
    "inspiration": "Вдохновение",
    "stats": "Характеристики",
    "stat_modifiers": "Модификаторы характеристик",
    "skills": "Навыки",
    "traits_and_abilities": "Черты и способности",
    "inventory": "Инвентарь",
    "languages": "Языки",
    "backstory": "Предыстория"
}

def translate_key(key):
    """Translates a key using the TRANSLATIONS dictionary."""
    return TRANSLATIONS.get(key, key)


def escape_markdown_v2(text):
    # Экранируем все специальные символы MarkdownV2
    return re.sub(r'([._()[\]~`>#+-=|{}.!])', r'\\\1', text)


max_message_length = 4096  # Максимальная длина сообщения в Telegram

def send_long_message(update, text):
    """Sends a long message by splitting it into parts."""
    for i in range(0, len(text), max_message_length):
        update.message.reply_text(text[i:i+max_message_length], parse_mode='MarkdownV2')



# Conversation states
CHOOSING_RACE, CHOOSING_CLASS, CHOOSING_GENDER = range(3)

# Utility functions
def get_key_by_value(dictionary, value):
    """Finds the key for a given value in a dictionary."""
    return next((key for key, val in dictionary.items() if val == value), None)

def format_character_card(data):
    """Formats character data into a readable text response."""
    card = (
        f"*Карточка персонажа:*\n"
        f"👤 *Имя:* {data.get('name', 'Безымянный')} {data.get('surname', '')}\n"
        f"🎂 *Возраст:* {data.get('age', 'Не указан')}\n"
        f"🌍 *Раса:* {data.get('race', 'Не указана')}\n"
        f"⚔️ *Класс:* {data.get('character_class', 'Не указан')}\n"
        f"🌟 *Уровень:* {data.get('lvl', 'Не указан')}\n"
        f"💓 *Хиты:* {data.get('hp', 'Не указаны')}\n"
        f"👁️ *Пассивное восприятие:* {data.get('passive_perception', 'Не указано')}\n"
        f"🏃 *Скорость:* {data.get('speed', 'Не указана')} футов\n"
        f"⚖️ *Мировоззрение:* {data.get('worldview', 'Не указано')}\n"
        f"🎲 *Инициатива:* {data.get('initiative', 'Не указана')}\n"
        f"💡 *Вдохновение:* {'Да' if data.get('inspiration', False) else 'Нет'}\n"
        f"*📜 Предыстория:*\n{data.get('backstory', 'Нет данных')}\n\n"
    )

    if 'stats' in data:
        stats = data['stats']
        card += "*⚙️ Характеристики:*\n"
        card += "\n".join(f"  - {translate_stat(stat)}: {value}" for stat, value in stats.items())  # Перевод характеристик

    if 'stat_modifiers' in data:
        modifiers = data['stat_modifiers']
        card += "\n\n*📊 Модификаторы характеристик:*\n"
        card += "\n".join(f"  - {translate_stat(stat)}: {value}" for stat, value in modifiers.items())

    if 'skills' in data:
        skills = data['skills']
        card += "\n\n*🛠️ Навыки:*\n"
        card += ", ".join(skills)

    if 'traits_and_abilities' in data:
        traits = data['traits_and_abilities']
        card += "\n\n*🧬 Черты и способности:*\n"
        card += "\n".join(f"  - *{trait}:* {desc}" for trait, desc in traits.items())

    # Форматируем оружие и броню перед инвентарём
    card += f'\n\n {format_weapons_and_armor(data)}'

    # Инвентарь
    if 'inventory' in data:
        inventory = data['inventory']
        card += "\n\n*🎒 Инвентарь:*\n"
        card += ", ".join(inventory)

    if 'languages' in data:
        languages = data['languages']
        card += "\n\n*🗣️ Языки:*\n"
        card += ", ".join(languages)
        
    return card

# Модификация функции для перевода характеристик на русский
def translate_stat(stat):
    """Translates stat keys into Russian."""
    stat_translations = {
        'strength': 'Сила',
        'dexterity': 'Ловкость',
        'constitution': 'Выносливость',
        'intelligence': 'Интеллект',
        'wisdom': 'Мудрость',
        'charisma': 'Харизма'
    }
    return stat_translations.get(stat, stat.capitalize())  # Возвращаем название характеристики на русском

# Модификация функции format_weapons_and_armor для оружия и брони
def format_weapons_and_armor(data):
    """Formats weapons and armor data into a readable text response with translation."""
    card = ""

    # Форматирование оружия и снаряжения
    if "weapons_and_equipment" in data:
        weapons_and_equipment = data["weapons_and_equipment"]
        card += f"*🛡️ Амуниция:*\n"
        for name, details in weapons_and_equipment.items():
            card += f"  - *{name}:*\n"
            for key, value in details.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                # Преобразуем типы данных
                card += f"    - {translate_key(key)}: {value}\n"
            card += "\n"
    else:
        card += "*🛡️ Амуниция: Нет данных*\n"

    # Форматирование брони
    if "armor" in data:
        armor = data["armor"]
        card += ""
        for name, details in armor.items():
            card += f"  - *{name}:*\n"
            for key, value in details.items():
                if key == "dex_bonus":
                    value = "Да" if value else "Нет"
                elif key == "stealth_disadvantage":
                    value = "Да" if value else "Нет"
                if isinstance(value, list):
                    value = ", ".join(value)
                card += f"    - {translate_key(key)}: {value}\n"
            card += "\n"
    else:
        card += ""

    return card



# Handlers
def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation by showing race options."""
    keyboard = [[InlineKeyboardButton(race, callback_data=race)] for race in RACES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите расу для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_RACE

def choosing_race(update: Update, context: CallbackContext) -> int:
    """Handles race selection and shows class options."""
    query = update.callback_query
    query.answer()
    chosen_race = query.data
    context.user_data['race'] = RACES[chosen_race]

    try:
        # Чтение данных о расе
        with open(f"C:/Users/Artem/Desktop/RnD/research-and-development/not_in_use/race/{RACES[chosen_race]}.json", "r", encoding="utf-8") as file:
            race_data = json.load(file)
            class_options = race_data.get('class_options', [])  # Рекомендуемые классы
            print(f"Данные для расы {chosen_race}: Рекомендуемые классы - {class_options}")  # Логирование данных
    except FileNotFoundError:
        query.message.reply_text("Ошибка: файл с данными расы не найден.")
        return ConversationHandler.END

    # Создание кнопок, выделяя рекомендуемые классы
    keyboard = []
    for cls in clases.keys():
        if cls in class_options:
            label = f"⭐ {cls} (Рекомендуется)"  # Добавляем метку к рекомендуемым
        else:
            label = cls
        keyboard.append([InlineKeyboardButton(label, callback_data=cls)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите класс для вашего персонажа:", reply_markup=reply_markup)
    

    return CHOOSING_CLASS






def choosing_class(update: Update, context: CallbackContext) -> int:
    """Handles class selection and shows gender options."""
    query = update.callback_query
    query.answer()
    context.user_data['class'] = query.data

    keyboard = [[InlineKeyboardButton(g, callback_data=g)] for g in GENDER_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите пол для вашего персонажа:")
    query.message.reply_text("Выберите пол:", reply_markup=reply_markup)
    return CHOOSING_GENDER

def choosing_gender(update: Update, context: CallbackContext) -> None:
    """Handles gender selection and submits the data to the server."""
    query = update.callback_query
    query.answer()
    context.user_data['gender'] = query.data

    data = {
        "gender": context.user_data['gender'],
        "rac": get_key_by_value(RACES, context.user_data['race']),
        "clas": context.user_data['class']
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





# Main function
def main():
    """Runs the bot."""
    updater = Updater("teg")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_RACE: [CallbackQueryHandler(choosing_race)],
            CHOOSING_CLASS: [CallbackQueryHandler(choosing_class)],
            CHOOSING_GENDER: [CallbackQueryHandler(choosing_gender)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

