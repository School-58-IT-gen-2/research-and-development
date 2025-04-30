from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
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
    "Следопыт"
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
    CHOOSING_SKILLS = State()
    CHOOSING_INVENTORY = State()
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
        race = user_data.get("chosen_race")
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
        params = data
        async with session.get("http://localhost:8000/character-list-options", params=params) as resp:
            if resp.status == 200:
                json_data = await resp.json()
                print(json_data)
                await callback.message.edit_text(f"Сводка персонажа:\n{json_data['options']}")
            else:
                await callback.message.edit_text("Произошла ошибка при получении данных с сервера.")

# --- Main ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
