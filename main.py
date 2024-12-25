from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = 'Your Bot api'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    gender = State()
    growth = State()
    weight = State()

@dp.message_handler(text=['Calories'])
async def set_age(message):
    await message.answer(f'Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_gender(message, state):
    await state.update_data(age = message.text)
    await message.answer(f'Введите свой пол (М/Ж):')
    await UserState.gender.set()

@dp.message_handler(state= UserState.gender)
async def set_growth(message, state):
    await state.update_data(gender = message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()
    
@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    
    data = await state.get_data()
    
    # Используется упрощенный вариант формулы Миффлина-Сан Жеора
    if data['gender'] == 'М':
        print(data['growth'])
        calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5

    elif data['gender'] == 'Ж':
        calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 161
    else:
        await message.answer(f' Страшно! Очень страшно! Мы не знаем что это такое, если бы мы знали, что это такое, но мы не знаем, что это такое!')
    
    try:
        await message.answer(f'Ваша норма калорий: {calories}')
    except Exception as exc:
        print(f'Exception: {exc}')
        await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    await message.answer(f'Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)