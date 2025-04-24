from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import httpx
import uuid

API_BASE_URL = "http://localhost:8000"  # поменяй на адрес своего API если нужно


API_TOKEN = '8154427178:AAEJPcc0xXiRt43YgCNs_hKKqVmibGoyAAA'

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний
class CharacterCreation(StatesGroup):
    CHOOSING_CLASS = State()
    CHOOSING_RACE = State()
    CHOOSING_CHARACTERISTICS = State()
    SETTING_CHARACTERISTIC = State()
    CHOOSING_SKILLS = State()
    CHOOSING_INVENTORY = State()
    CHOOSING_GENDER = State()
    CHOOSING_AGE = State()
    CHOOSING_STORY = State()
    CHOOSING_NAME = State()

# Варианты классов и рас
CLASSES = ["Следопыт", "Варвар", "Бард", "Плут", "Друид", "Колдун", "Монах", "Паладин", "Жрец", "Маг", "Воин", "Волшебник"]
RACES = ["Человек", "Эльф", "Полуорк", "Гном", "Дварф", "Полурослик", "Драконорождённый", "Полуэльф", "Тифлинг"]
GENDERS = ["Мужской", "Женский"]
CHARACTERISTICS_ORDER = ["Сила", "Ловкость", "Телосложение", "Интеллект", "Мудрость", "Харизма"]
CHARACTERISTIC_VALUES = ["8", "10", "12", "13", "14", "15"]


# Генератор клавиатуры по списку
def generate_keyboard(options: list[str], prefix: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=option, callback_data=f"{prefix}:{option}")]
        for option in options
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



# Старт команды
@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(CharacterCreation.CHOOSING_CLASS)
    await message.answer(
        "Привет! Давай создадим персонажа. Выбери класс:",
        reply_markup=generate_keyboard(CLASSES, "class")
    )


# Последовательная обработка каждого состояния
@dp.callback_query(F.data.startswith("class"))
async def handle_class_choice(callback: CallbackQuery, state: FSMContext):
    chosen_class = callback.data.split(":")[1]
    await state.update_data(ch_class=chosen_class)
    await callback.message.edit_text(
        f"Класс выбран: {chosen_class}\nТеперь выбери расу:",
        reply_markup=generate_keyboard(RACES, "race")
    )
    await state.set_state(CharacterCreation.CHOOSING_RACE)
    await callback.answer()


@dp.callback_query(F.data.startswith("race"))
async def handle_race_choice(callback: CallbackQuery, state: FSMContext):
    chosen_race = callback.data.split(":")[1]
    await state.update_data(race=chosen_race)
    await callback.message.edit_text(
        f"Раса выбрана: {chosen_race}\nТеперь выбери пол персонажа:",
        reply_markup=generate_keyboard(GENDERS, "gender")
    )
    await state.set_state(CharacterCreation.CHOOSING_GENDER)
    await callback.answer()

@dp.callback_query(F.data.startswith("gender"))
async def handle_gender_choice(callback: CallbackQuery, state: FSMContext):
    chosen_gender = callback.data.split(":")[1]
    await state.update_data(gender=chosen_gender)
    await callback.message.edit_text(
        f"Пол выбран: {chosen_gender}\nСколько лет персонажу?"
    )
    await state.set_state(CharacterCreation.CHOOSING_AGE)
    await callback.answer()


@dp.message(CharacterCreation.CHOOSING_CHARACTERISTICS)
async def choose_characteristics(message: Message, state: FSMContext):
    await state.update_data(characteristics=message.text)
    await message.answer("Теперь выбери навыки:")
    await state.set_state(CharacterCreation.CHOOSING_SKILLS)

@dp.message(CharacterCreation.CHOOSING_SKILLS)
async def choose_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer("Что у него в инвентаре?")
    await state.set_state(CharacterCreation.CHOOSING_INVENTORY)

@dp.message(CharacterCreation.CHOOSING_INVENTORY)
async def choose_inventory(message: Message, state: FSMContext):
    await state.update_data(inventory=message.text)
    await message.answer("Сколько лет персонажу?")
    await state.set_state(CharacterCreation.CHOOSING_AGE)

@dp.message(CharacterCreation.CHOOSING_AGE)
async def choose_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Расскажи предысторию персонажа:")
    await state.set_state(CharacterCreation.CHOOSING_STORY)

@dp.message(CharacterCreation.CHOOSING_STORY)
async def choose_story(message: Message, state: FSMContext):
    await state.update_data(story=message.text)
    await message.answer("И наконец, как зовут твоего персонажа?")
    await state.set_state(CharacterCreation.CHOOSING_NAME)

@dp.message(CharacterCreation.CHOOSING_NAME)
async def choose_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    
    summary = (
        f"🎲 Вот твой персонаж:\n"
        f"Имя: {data.get('name')}\n"
        f"Класс: {data.get('ch_class')}\n"
        f"Раса: {data.get('race')}\n"
        f"Пол: {data.get('gender')}\n"
        f"Возраст: {data.get('age')}\n"
        f"Характеристики: {data.get('characteristics')}\n"
        f"Навыки: {data.get('skills')}\n"
        f"Инвентарь: {data.get('inventory')}\n"
        f"История: {data.get('story')}"
    )

    await message.answer(summary)
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
