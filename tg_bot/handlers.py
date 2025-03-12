from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from tg_bot.utils import format_character_card, escape_markdown_v2, get_key_by_value
from db.db_source import DBSource
from config import SUPABASE_URL, SUPABASE_KEY
from model.char_constructor import CharConstructor
import requests

CONSTRUCTOR_START, CHOOSING_CLASS, CHOOSING_RACE, CHOOSING_CHARACTERISTICS, CHOOSING_SKILLS, CHOOSING_INVENTORY, CHOOSING_GENDER, CHOOSING_AGE, CHOOSING_STORY = range(9)
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
    """Начало диалога: """
    keyboard = [[InlineKeyboardButton('Сгенерировать случайного персонажа', callback_data='random')], [InlineKeyboardButton('Конструктор персонажа', callback_data='constructor')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return CONSTRUCTOR_START

def constructor_start(update: Update, context: CallbackContext) -> int:


    query = update.callback_query
    if query.data == 'random':
        query.edit_message_text("*Тут выводится случайный персонаж", reply_markup=InlineKeyboardMarkup([]))
        return ConversationHandler.END
    global constructor
    constructor = CharConstructor()
    query.answer()
    classes = constructor.get_classes()
    keyboard = [[InlineKeyboardButton(race, callback_data=race)] for race in classes] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите класс для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_CLASS


def choosing_class(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    
    constructor.set_class(query.data)

    races = constructor.get_races()
    keyboard = [[InlineKeyboardButton(race, callback_data=race)] for race in races] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

    query.answer()
    


    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите расу для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_RACE

def choosing_race(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    constructor.set_race(query.data)

    characteristic, characteristics_btns, recomended = constructor.get_characteristics()

    btns = characteristics_btns
    keyboard = [[InlineKeyboardButton(skill + '⭐(Рекомендуется)' if skill in recomended else skill, callback_data=skill)] for skill in btns] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

    

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"Выберите характеристику {characteristic.upper()} для вашего персонажа:", reply_markup=reply_markup)
    return CHOOSING_CHARACTERISTICS

def choosing_characteristics(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    
    constructor.set_characteristics(query.data)
    characteristic, characteristics_btns, recomended = constructor.get_characteristics()
    
    if characteristics_btns != None:
        keyboard = [[InlineKeyboardButton(skill + '⭐(Рекомендуется)' if skill in recomended else skill, callback_data=skill)] for skill in characteristics_btns] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Выберите характеристику {characteristic.upper()} для вашего персонажа:", reply_markup=reply_markup)
        return CHOOSING_CHARACTERISTICS

    
    skills_body = constructor.get_skills()
    skills = skills_body["skills_list"]
    
    keyboard = [[InlineKeyboardButton(skill, callback_data=skill)] for skill in skills] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"Выберите навыки для вашего персонажа [{skills_body['skills_count']+1}/{skills_body['skills_limit']}]:", reply_markup=reply_markup)

    return CHOOSING_SKILLS

def choosing_skills(update: Update, context: CallbackContext) -> int:
    """Обработка выбора навыков."""
    query = update.callback_query
    query.answer()
    lim = constructor.add_skill(query.data)
    if lim == 'more':
        skills_body = constructor.get_skills()
        skills = skills_body["skills_list"]

        keyboard = [[InlineKeyboardButton(skill, callback_data=skill)] for skill in skills] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]


        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Выберите навыки для вашего персонажа [{skills_body['skills_count']+1}/{skills_body['skills_limit']}]:", reply_markup=reply_markup)

        return CHOOSING_SKILLS

    inventory_body = constructor.get_inventory()[constructor.inventory_counter]
    inventory_strs = []#[' + '.join(i)[:28] + '...' if len(' + '.join(i)) > 32 else ' + '.join(i) for i in inventory_body]
    for i in inventory_body:
        if len(i) == 1:
            inventory_strs.append(i[0])
        else:
            options_m = []
            for j in list(set(i)):
                if i.count(j) > 1:
                    options_m.append(j + f'({i.count(j)})')
                else:
                    options_m.append(j)
            inventory_strs.append('+'.join(options_m))

    print(1111111111111, inventory_strs)
    keyboard = [[InlineKeyboardButton(option if len(option) < 32 else '...', callback_data=option)] for option in inventory_strs] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"Выберите опцию для инвентаря вашего персонажа [{constructor.inventory_counter + 1}/{constructor.inventory_lim}]:", reply_markup=reply_markup)
    return CHOOSING_INVENTORY

def choosing_inventory(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    
    constructor.add_inventory(query.data)

    if constructor.inventory_counter != constructor.inventory_lim:
        inventory_body = constructor.get_inventory()[constructor.inventory_counter]
        inventory_strs = []#[' + '.join(i)[:28] + '...' if len(' + '.join(i)) > 32 else ' + '.join(i) for i in inventory_body]
        for i in inventory_body:
            if len(i) == 1:
                inventory_strs.append(i[0])
            else:
                options_m = []
                for j in list(set(i)):
                    if i.count(j) > 1:
                        options_m.append(j + f'({i.count(j)})')
                    else:
                        options_m.append(j)
                inventory_strs.append(' + '.join(options_m))
    
        keyboard = [[InlineKeyboardButton(option if len(option) < 32 else option[:28] + '...', callback_data=option)] for option in inventory_strs] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Выберите опцию для инвентаря вашего персонажа [{constructor.inventory_counter + 1}/{constructor.inventory_lim}]:", reply_markup=reply_markup)
        return CHOOSING_INVENTORY

    keyboard = [[InlineKeyboardButton('Мужской', callback_data='male')], [InlineKeyboardButton('Женский', callback_data='female')], [InlineKeyboardButton('Выбрать случайный', callback_data='random')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите пол персонажа:", reply_markup=reply_markup)


    return CHOOSING_GENDER


# def choosing_weapon(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     query.answer()
#     lim = constructor.add_weapon(query.data)
#     if lim =='more':
#         weapons = constructor.get_weapons()
#         weapons_list = weapons['weapons_list']
#         keyboard = [[InlineKeyboardButton(weapon, callback_data=weapon) for weapon in weapons_list]] + [[InlineKeyboardButton('Выбрать случайную', callback_data='random')]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         query.edit_message_text(f"Выберите оружие для вашего персонажа [{weapons['weapons_count']+1}/{weapons['weapons_limit']}]:", reply_markup=reply_markup)
#         return CHOOSING_WEAPON

#     keyboard = [[InlineKeyboardButton('Выбрать случайный', callback_data='random')]]

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text("Введите возраст персонажа:", reply_markup=reply_markup)
#     return CHOOSING_AGE

def choosing_age(update: Update, context: CallbackContext) -> None:
    """Handles age selection and submits the data to the server."""
    return CHOOSING_STORY
    query = update.callback_query
    query.answer()
    print(query.data)
    if query.data == 'random':
        constructor.set_age(query.data)
    else:
        constructor.set_age(update.message.text)

    keyboard = [[InlineKeyboardButton('Выбрать случайный', callback_data='random')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Введите предысторию персонажа:", reply_markup=reply_markup)


def choosing_story(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    # data = {
    #     "gender": context.user_data['gender'],
    #     "race": get_key_by_value(RACES, context.user_data['race']),
    #     "character_class": context.user_data['class']
    # }

    # try:
    #     response = requests.post(URL, json=data)
    #     if response.status_code == 200:
    #         character_data = response.json()
    #         # print("Character data from server:", character_data)  # Отладка
    #         formatted_response = format_character_card(character_data)
    #         formatted_response = escape_markdown_v2(formatted_response)  # Экранируем текст
    #         query.message.reply_text(formatted_response, parse_mode='MarkdownV2')
    #     else:
    #         query.message.reply_text(f"Ошибка сервера: {response.status_code}")
    # except Exception as e:
    #     query.message.reply_text(f"Произошла ошибка: {str(e)}")

    query.message.reply_text("Если хотите создать нового персонажа, введите /start.")
    
    return ConversationHandler.END
    
    if query.data == 'random':
        constructor.set_story(query.data)
    else:
        constructor.set_story(update.message.text)

    keyboard = [[InlineKeyboardButton('Выбрать случайный', callback_data='random')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Введите имя персонажа:", reply_markup=reply_markup)
    

def choosing_name(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'random':
        constructor.set_name(query.data)
    else:
        constructor.set_name(update.message.text)

    keyboard = [[InlineKeyboardButton('Мужской', callback_data='male')], [InlineKeyboardButton('Женский', callback_data='female')], [InlineKeyboardButton('Выбрать случайный', callback_data='random')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите пол персонажа:", reply_markup=reply_markup)


    return CHOOSING_GENDER

def choosing_gender(update: Update, context: CallbackContext) -> None:
    """Handles gender selection and submits the data to the server."""
    query = update.callback_query
    query.answer()
    context.user_data['gender'] = query.data

    return CHOOSING_AGE

def get_conversation_handler():
    """Возвращает ConversationHandler для бота."""
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONSTRUCTOR_START: [CallbackQueryHandler(constructor_start)],
            CHOOSING_CLASS: [CallbackQueryHandler(choosing_class)],
            CHOOSING_RACE: [CallbackQueryHandler(choosing_race)],
            CHOOSING_CHARACTERISTICS: [CallbackQueryHandler(choosing_characteristics)],
            CHOOSING_SKILLS: [CallbackQueryHandler(choosing_skills)],
            CHOOSING_INVENTORY: [CallbackQueryHandler(choosing_inventory)],
            CHOOSING_GENDER: [CallbackQueryHandler(choosing_gender)],
            CHOOSING_AGE: [CallbackQueryHandler(choosing_age)],
            CHOOSING_STORY: [CallbackQueryHandler(choosing_story)]
        },
        fallbacks=[]
    )