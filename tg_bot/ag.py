import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY
from model.char_constructor import CharConstructor
from db.db_source import DBSource

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = DBSource(SUPABASE_URL, SUPABASE_KEY)
db.connect()

class CharacterCreation(StatesGroup):
    CONSTRUCTOR_START = State()
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
long_callback = {}

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сгенерировать случайного персонажа", callback_data="random")],
            [InlineKeyboardButton(text="Конструктор персонажа", callback_data="constructor")]
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CONSTRUCTOR_START)

@dp.callback_query(F.data == "random")
@dp.callback_query(F.data == "constructor")
async def constructor_start(callback: CallbackQuery, state: FSMContext):
    global constructor
    constructor = CharConstructor()
    if callback.data == 'random':
        result = constructor.generate_random_char()
        await callback.message.edit_text(f"*Тут выводится случайный персонаж {str(result)}*", reply_markup=None)
        await state.clear()
        return
    
    classes = constructor.get_classes()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cls, callback_data=cls)] for cls in classes] +
                        [[InlineKeyboardButton(text='Выбрать случайную', callback_data='random')]]
    )
    await callback.message.edit_text("Выберите класс для вашего персонажа:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSE_CLASS)

@dp.callback_query()
async def choosing_class(callback: CallbackQuery, state: FSMContext):
    constructor.set_class(callback.data)
    races = constructor.get_races()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=race, callback_data=race)] for race in races] +
                        [[InlineKeyboardButton(text='Выбрать случайную', callback_data='random')]]
    )
    await callback.message.edit_text("Выберите расу для вашего персонажа:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSE_RACE)

@dp.callback_query()
async def choosing_race(callback: CallbackQuery, state: FSMContext):
    constructor.set_race(callback.data)
    characteristic, characteristics_btns, recommended = constructor.get_characteristics()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=skill, callback_data=skill)] for skill in characteristics_btns] +
                        [[InlineKeyboardButton(text='Выбрать случайную', callback_data='random')]]
    )
    await callback.message.edit_text(f"Выберите характеристику {characteristic.upper()} для вашего персонажа:", reply_markup=keyboard)
    await state.set_state(CharacterCreation.CHOOSE_CHARACTERISTICS)

# ... остальные хендлеры аналогично ...

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
