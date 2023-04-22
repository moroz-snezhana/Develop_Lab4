import os
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
bot = Bot(token='5929263683:AAGsa7CoomaIXZOyA0CBQPlwU48922Uswl8')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот, который умеет конвертировать валюты! Если тебе нужна помощь, напиши /help")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я помогу тебе конвертировать в рубли любую валюту. Если ты хочешь задать новый курс, введи /save_currency")

class States(StatesGroup):
    Cur_name = State()
    Exchange_to_ruble = State()
    Name_of_cur = State()
    Summa = State()

save_curr = {}

@dp.message_handler(commands=['save_currency'])
async def process_save_input(message: types.Message):
    await message.reply("Введи название валюты, курс которой хочешь задать:")
    await States.Cur_name.set()

@dp.message_handler(state=States.Cur_name)
async def currency_process(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await message.answer("Теперь введи курс к рублю:")
    await States.Exchange_to_ruble.set()

@dp.message_handler(state=States.Exchange_to_ruble)
async def rate_process(message: Message, state: FSMContext):
    currency = await state.get_data()
    name_currency = currency['currency']
    save_curr[name_currency]=message.text
    await state.finish()

@dp.message_handler(commands=['convert'])
async def currency_name(message: Message):
    await States.Name_of_cur.set()
    await message.answer("Введи название валюты:")

@dp.message_handler(state=States.Name_of_cur)
async def summa_process(message: Message, state: FSMContext):
    await state.update_data(our_currency=message.text)
    await message.answer("Введи сумму в указанной валюте:")
    await States.Summa.set()

@dp.message_handler(state=States.Summa)
async def convert_proc(message: Message, state: FSMContext):
    summ = message.text
    our_currency = await state.get_data()
    new_currency = our_currency['our_currency']
    result = int(save_curr[new_currency]) * int(summ)
    await message.answer(result)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


