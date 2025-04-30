from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
import random
import asyncio
import logging

API_TOKEN = "8154427178:AAEJPcc0xXiRt43YgCNs_hKKqVmibGoyAAA"

# --- Data ---
CLASSES = [
    "Варвар",
    "Бард",
    "Плут",
    "Друид",
    "Колдун",
    "Монах",
    "Паладин",
    "Следопыт",
    "Жрец",
    "Чародей",
    "Воин",
    "Колдун"
]

RACES = ["Человек", "Эльф", "Полуорк", "Гном", "Дварф", "Полурослик", "Драконорождённый", "Полуэльф", "Тифлинг"]
GENDERS = ["Мужской", "Женский"]

SUBRACES = {
    "Драконорождённый": ["Красный драконорождённый", "Синий драконорождённый"],
    "Дварф": ["Горный дворф", "Холмовой дворф"],
    "Эльф": ["Высший эльф", "Лесной эльф", "Тёмный эльф (дроу)"],
    "Гном": ["Горный гном", "Лесной гном"],
    "Полуэльф": ["Эльфийский полуэльф", "Человечий полуэльф"],
    "Полурослик": ["Ловкий полурослик", "Стойкий полурослик"]
}

# --- FSM ---
class CharacterCreation(StatesGroup):
    CHOOSING_CLASS = State()
    CHOOSING_RACE = State()
    CHOOSING_SUBRACE = State()
    CHOOSING_GENDER = State()
    CHOOSING_CHARACTERISTICS = State()
    SETTING_CHARACTERISTIC = State()
    CHOOSING_SKILLS = State()
    CHOOSING_INVENTORY = State()
    SELECTING_INVENTORY_ITEM = State()
    CHOOSING_AGE = State()
    CHOOSING_STORY = State()
    CHOOSING_NAME = State()

# --- Bot Setup ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- Helpers ---
def get_keyboard(options: list, add_random=True, add_back=True):
    builder = InlineKeyboardBuilder()
    for opt in options:
        builder.button(text=opt, callback_data=opt)
    if add_random:
        builder.button(text="🎲 Случайно", callback_data="__random__")
    if add_back:
        builder.button(text="⬅️ Назад", callback_data="__back__")
    builder.adjust(2)
    return builder.as_markup()

# --- Handlers ---
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите класс персонажа:", reply_markup=get_keyboard(CLASSES, add_back=False))
    await state.set_state(CharacterCreation.CHOOSING_CLASS)

@dp.callback_query(CharacterCreation.CHOOSING_CLASS)
async def choose_class(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(CLASSES)
    elif callback.data == "__back__":
        await callback.message.edit_text("Выберите класс персонажа:", reply_markup=get_keyboard(CLASSES, add_back=False))
        return
    else:
        selected = callback.data

    await state.update_data(char_class=selected)
    await callback.message.edit_text("Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
    await state.set_state(CharacterCreation.CHOOSING_RACE)

@dp.callback_query(CharacterCreation.CHOOSING_RACE)
async def choose_race(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(RACES)
    elif callback.data == "__back__":
        await callback.message.edit_text("Выберите класс персонажа:", reply_markup=get_keyboard(CLASSES))
        await state.set_state(CharacterCreation.CHOOSING_CLASS)
        return
    else:
        selected = callback.data

    await state.update_data(char_race=selected)

    if selected in SUBRACES:
        await callback.message.edit_text(f"Выберите подрасу для {selected}:", reply_markup=get_keyboard(SUBRACES[selected]))
        await state.set_state(CharacterCreation.CHOOSING_SUBRACE)
    else:
        await callback.message.edit_text("Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
        await state.set_state(CharacterCreation.CHOOSING_GENDER)

@dp.callback_query(CharacterCreation.CHOOSING_SUBRACE)
async def choose_subrace(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_data = await state.get_data()
    race = user_data.get("char_race")

    if callback.data == "__random__":
        selected = random.choice(SUBRACES[race])
    elif callback.data == "__back__":
        await callback.message.edit_text("Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
        await state.set_state(CharacterCreation.CHOOSING_RACE)
        return
    else:
        selected = callback.data

    await state.update_data(char_subrace=selected)
    await callback.message.edit_text("Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
    await state.set_state(CharacterCreation.CHOOSING_GENDER)

@dp.callback_query(CharacterCreation.CHOOSING_GENDER)
async def choose_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "__random__":
        selected = random.choice(GENDERS)
    elif callback.data == "__back__":
        user_data = await state.get_data()
        race = user_data.get("char_race")
        if race in SUBRACES:
            await callback.message.edit_text(f"Выберите подрасу для {race}:", reply_markup=get_keyboard(SUBRACES[race]))
            await state.set_state(CharacterCreation.CHOOSING_SUBRACE)
        else:
            await callback.message.edit_text("Выберите расу персонажа:", reply_markup=get_keyboard(RACES))
            await state.set_state(CharacterCreation.CHOOSING_RACE)
        return
    else:
        selected = callback.data

    await state.update_data(char_gender=selected)
    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/character-list-options", params=data) as resp:
            if resp.status == 200:
                json_data = await resp.json()
                json_data['inventory'] = list(filter(lambda x: isinstance(x, list), json_data['inventory']))
                await state.update_data(
                    json_data=json_data,
                    characteristics_options=json_data["options"],
                    current_stat_index=0
                )
                await ask_next_stat(callback.message, state)
                await state.set_state(CharacterCreation.SETTING_CHARACTERISTIC)
            else:
                await callback.message.edit_text("Произошла ошибка при получении данных с сервера.")

async def ask_next_stat(message: Message, state: FSMContext):
    data = await state.get_data()
    stat_names = list(data["characteristics_options"].keys())
    index = data["current_stat_index"]
    if index >= len(stat_names):
        await state.set_state(CharacterCreation.CHOOSING_SKILLS)
        await start_skills_selection(message, state)
        return

    stat = stat_names[index]
    all_values = data["characteristics_options"][stat][0]
    recommended = set(data["characteristics_options"][stat][1])
    display_values = [
        f"{val} 🌟" if val in recommended else val for val in all_values
    ]
    keyboard = get_keyboard(display_values)
    await message.edit_text(f"Выберите значение для характеристики *{stat}*:", reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(CharacterCreation.SETTING_CHARACTERISTIC)
async def set_characteristic(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    stat_names = list(data["characteristics_options"].keys())
    index = data["current_stat_index"]
    stat = stat_names[index]

    if callback.data == "__random__":
        selected = random.choice(data["characteristics_options"][stat][0])
    elif callback.data == "__back__":
        if index == 0:
            await callback.message.edit_text("Выберите гендер персонажа:", reply_markup=get_keyboard(GENDERS))
            await state.set_state(CharacterCreation.CHOOSING_GENDER)
            return
        await state.update_data(current_stat_index=index - 1)
        await ask_next_stat(callback.message, state)
        return
    else:
        selected = callback.data.replace(" 🌟", "")  # удаляем пометку рекомендации

    stats = data.get("char_stats", {})
    stats[stat] = selected
    await state.update_data(char_stats=stats, current_stat_index=index + 1)
    await ask_next_stat(callback.message, state)

async def start_skills_selection(message: Message, state: FSMContext):
    data = await state.get_data()
    skills = data["json_data"]["skils"]
    skills_list = skills["skills_list"]
    limit = skills["skills_limit"]
    await state.update_data(skills_selected=[], skills_limit=limit)
    await ask_next_skill(message, state)

async def ask_next_skill(message: Message, state: FSMContext):
    data = await state.get_data()
    selected = set(data["skills_selected"])
    skills_list = [s for s in data["json_data"]["skils"]["skills_list"] if s not in selected]
    limit = data["skills_limit"]

    if len(selected) >= limit:
        await message.edit_text(f"Вы выбрали все {limit} навыков: {', '.join(selected)}")
        await state.set_state(CharacterCreation.SELECTING_INVENTORY_ITEM)
        await state.update_data(current_inventory_index=0, inventory_selected=[])
        await ask_inventory_item(message, state)

        return

    keyboard = get_keyboard(skills_list)
    await message.edit_text(f"Выберите навык ({len(selected) + 1} из {limit}):", reply_markup=keyboard)

@dp.callback_query(CharacterCreation.CHOOSING_SKILLS)
async def choose_skill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    selected = data["skills_selected"]
    limit = data["skills_limit"]
    all_skills = data["json_data"]["skils"]["skills_list"]

    if callback.data == "__random__":
        remaining = [s for s in all_skills if s not in selected]
        selected_skill = random.choice(remaining)
    elif callback.data == "__back__":
        if not selected:
            # Возврат к характеристикам
            stat_keys = list(data["characteristics_options"].keys())
            await state.update_data(current_stat_index=len(stat_keys)-1)
            await state.set_state(CharacterCreation.SETTING_CHARACTERISTIC)
            await ask_next_stat(callback.message, state)
            return
        selected.pop()
        await state.update_data(skills_selected=selected)
        await ask_next_skill(callback.message, state)
        return
    else:
        selected_skill = callback.data

    if selected_skill not in selected:
        selected.append(selected_skill)

    await state.update_data(skills_selected=selected)
    await ask_next_skill(callback.message, state)


async def ask_inventory_item(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["current_inventory_index"]
    inventory = data["json_data"]["inventory"]

    if index >= len(inventory):
        selected_items = data["inventory_selected"]
        flat_items = [", ".join(items) for items in selected_items]
        await message.edit_text(f"Вы выбрали инвентарь:\n" + "\n".join(flat_items))
        await ask_age(message, state)
        return


    options = inventory[index]
    display = [", ".join(option) for option in options]
    keyboard = get_keyboard(display)
    await message.edit_text(f"Выберите вариант инвентаря ({index+1} из {len(inventory)}):", reply_markup=keyboard)

@dp.callback_query(CharacterCreation.SELECTING_INVENTORY_ITEM)
async def choose_inventory_item(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    index = data["current_inventory_index"]
    inventory = data["json_data"]["inventory"]
    selected_items = data["inventory_selected"]

    if callback.data == "__random__":
        choice = random.choice(inventory[index])
    elif callback.data == "__back__":
        if index == 0:
            await state.set_state(CharacterCreation.CHOOSING_SKILLS)
            await ask_next_skill(callback.message, state)
            return
        await state.update_data(current_inventory_index=index - 1)
        selected_items.pop()
        await state.update_data(inventory_selected=selected_items)
        await ask_inventory_item(callback.message, state)
        return
    else:
        choice = callback.data.split(", ")

    selected_items.append(choice)
    await state.update_data(inventory_selected=selected_items, current_inventory_index=index + 1)
    await ask_inventory_item(callback.message, state)


async def ask_age(message: Message, state: FSMContext):
    data = await state.get_data()
    age_limits = data["json_data"].get("default_age", {"min": 16, "max": 100})
    min_age = age_limits["min"]
    max_age = age_limits["max"]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайный возраст")],
            # [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(f"Введите возраст персонажа (от {min_age} до {max_age}):", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSING_AGE)

@dp.message(CharacterCreation.CHOOSING_AGE)
async def handle_age_input(message: Message, state: FSMContext):
    data = await state.get_data()
    age_limits = data["json_data"].get("default_age", {"min": 16, "max": 100})
    min_age = age_limits["min"]
    max_age = age_limits["max"]

    if message.text == "⬅️ Назад":
        await state.set_state(CharacterCreation.SELECTING_INVENTORY_ITEM)
        await ask_inventory_item(message, state)
        return

    if message.text == "🎲 Случайный возраст":
        age = random.randint(min_age, max_age)
        await state.update_data(char_age=age)
        await message.answer(f"Случайный возраст выбран: {age}", reply_markup=ReplyKeyboardRemove())
        await ask_story(message, state)
        return

    try:
        age = int(message.text)
        if not (min_age <= age <= max_age):
            raise ValueError
    except ValueError:
        await message.answer(f"Пожалуйста, введите число от {min_age} до {max_age}.")
        return

    await state.update_data(char_age=age)
    await message.answer(f"Возраст установлен: {age}", reply_markup=ReplyKeyboardRemove())
    await ask_story(message, state)


async def ask_story(message: Message, state: FSMContext):
    data = await state.get_data()
    stories = data["json_data"].get("default_story", ["Без истории"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайная предыстория")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Введите предысторию персонажа или выберите случайную:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSING_STORY)

@dp.message(CharacterCreation.CHOOSING_STORY)
async def handle_story_input(message: Message, state: FSMContext):
    data = await state.get_data()
    stories = data["json_data"].get("default_story", [])

    if message.text == "🎲 Случайная предыстория":
        selected_story = random.choice(stories)
        await message.answer(f"Случайная предыстория выбрана:\n\n{selected_story}", reply_markup=ReplyKeyboardRemove())
    else:
        selected_story = message.text
        await message.answer("Предыстория установлена.", reply_markup=ReplyKeyboardRemove())

    await state.update_data(char_story=selected_story)

    await ask_name(message, state)


async def ask_name(message: Message, state: FSMContext):
    data = await state.get_data()
    default_names = data["json_data"].get("default_names", ["Имя неизвестно"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайное имя")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Введите имя персонажа или выберите случайное:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSING_NAME)

@dp.message(CharacterCreation.CHOOSING_NAME)
async def handle_name_input(message: Message, state: FSMContext):
    data = await state.get_data()
    names = data["json_data"].get("default_names", [])

    if message.text == "🎲 Случайное имя":
        selected_name = random.choice(names) if names else "Имя неизвестно"
        await message.answer(f"Случайное имя выбрано: {selected_name}", reply_markup=ReplyKeyboardRemove())
    else:
        selected_name = message.text
        await message.answer(f"Имя установлено: {selected_name}", reply_markup=ReplyKeyboardRemove())

    await state.update_data(char_name=selected_name)

    # Здесь можно завершить создание или вывести резюме
    await message.answer("Персонаж успешно создан! 🎉")
    await show_character_summary(message, state)


async def show_character_summary(message: Message, state: FSMContext):
    data = await state.get_data()

    race = data.get("char_race", "—")
    subrace = data.get("char_subrace")
    if subrace:
        race = f"{race} ({subrace})"

    characteristics = "\n".join([f"- *{k}*: {v}" for k, v in data.get("char_stats", {}).items()])
    skills = ", ".join(data.get("skills_selected", []))
    inventory = "\n".join([f"- {', '.join(i)}" for i in data.get("inventory_selected", [])])
    story = data.get("char_story", "—")
    name = data.get("char_name", "—")

    text = (
        f"*🧝‍♂️ Лист персонажа:*\n"
        f"*Имя:* {name}\n"
        f"*Класс:* {data.get('char_class', '—')}\n"
        f"*Раса:* {race}\n"
        f"*Пол:* {data.get('char_gender', '—')}\n"
        f"*Возраст:* {data.get('char_age', '—')}\n\n"
        f"*📊 Характеристики:*\n{characteristics}\n\n"
        f"*🎯 Навыки:*\n{skills}\n\n"
        f"*🎒 Инвентарь:*\n{inventory}\n\n"
        f"*📖 Предыстория:*\n_{story}_"
    )

    await message.answer(text, parse_mode="Markdown")


# --- Main ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
