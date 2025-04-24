from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from tg_bot.utils import format_character_card, escape_markdown_v2, get_key_by_value
from db.db_source import DBSource
from config import SUPABASE_URL, SUPABASE_KEY
from model.char_constructor import CharConstructor
import random

bot = Bot(token="8154427178:AAEJPcc0xXiRt43YgCNs_hKKqVmibGoyAAA")
dp = Dispatcher()

db = DBSource(SUPABASE_URL, SUPABASE_KEY)
db.connect()

class CharacterStates(StatesGroup):
    CHOOSING_CLASS = State()
    CHOOSING_RACE = State()
    CHOOSING_CHARACTERISTICS = State()
    CHOOSING_SKILLS = State()
    CHOOSING_INVENTORY = State()
    CHOOSING_GENDER = State()
    CHOOSING_AGE = State()
    CHOOSING_STORY = State()
    CHOOSING_NAME = State()

constructor = CharConstructor()

def back_button(callback_data: str):
    return [InlineKeyboardButton(text="⬅ Назад", callback_data=callback_data)]

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сгенерировать случайного персонажа", callback_data="random")],
            [InlineKeyboardButton(text="Конструктор персонажа", callback_data="constructor")]
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.callback_query(F.data == "constructor")
async def constructor_start(callback: CallbackQuery, state: FSMContext):
    constructor.reset()
    classes = constructor.get_classes()
    keyboard = InlineKeyboardBuilder()
    for char_class in classes:
        keyboard.button(text=char_class, callback_data=f"class_{char_class}")
    keyboard.button(text="Выбрать случайную", callback_data="class_random")
    await callback.message.edit_text("Выберите класс:", reply_markup=keyboard.as_markup())
    await state.set_state(CharacterStates.CHOOSING_CLASS)

@dp.callback_query(F.data.startswith("class_"))
async def choosing_class(callback: CallbackQuery, state: FSMContext):
    char_class = callback.data.split("_")[1]
    constructor.set_class(char_class)
    races = constructor.get_races()
    keyboard = InlineKeyboardBuilder()
    for race in races:
        keyboard.button(text=race, callback_data=f"race_{race}")
    keyboard.button(text="Выбрать случайную", callback_data="race_random")
    keyboard.row(*back_button("constructor"))
    await callback.message.edit_text("Выберите расу:", reply_markup=keyboard.as_markup())
    await state.set_state(CharacterStates.CHOOSING_RACE)

# Аналогично добавляются обработчики для других этапов

@dp.callback_query(F.data.startswith("back_"))
async def go_back(callback: CallbackQuery, state: FSMContext):
    previous_state = callback.data.split("_")[1]
    if previous_state == "constructor":
        await constructor_start(callback, state)
    elif previous_state == "class":
        await choosing_class(callback, state)
    elif previous_state == "race":
        return
        await choosing_race(callback, state)
    # Добавить аналогично для всех состояний

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
