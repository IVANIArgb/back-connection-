import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os

logging.basicConfig(level=logging.INFO)

API_TOKEN = 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

menu_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Выбор проблемы')],
        [KeyboardButton(text='Описать проблему')],
        [KeyboardButton(text='Предложения по проекту')],
    ]
)

def load_problems_count():
    problems_count = {}
    if os.path.exists('problems_count.txt'):
        with open('problems_count.txt', 'r', encoding='utf-8') as f:
            for line in f:
                problem, count = line.strip().split(': ')
                problems_count[problem] = int(count)
    else:
        problems_count = {'Проблема 1': 0, 'Проблема 2': 0, 'Проблема 3': 0} # Добавить новую проблему
    return problems_count

problems_count = load_problems_count()

current_mode = None

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    global current_mode
    current_mode = None
    await message.answer("Добро пожаловать! Выбирете действие:", reply_markup=menu_keyboard)

@dp.message(lambda message: message.text == 'Выбор проблемы')
async def choose_problem(message: types.Message):
    global current_mode
    current_mode = None
    problem_buttons = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Проблема 1')],
            [KeyboardButton(text='Проблема 2')],
            [KeyboardButton(text='Проблема 3')], # Добавить новую проблему
        ]
    )
    await message.answer("Выберите проблему:", reply_markup=problem_buttons)

@dp.message(lambda message: message.text in ['Проблема 1', 'Проблема 2', 'Проблема 3']) # Добавить новую проблему
async def specific_problem_chosen(message: types.Message):
    problem = message.text
    problems_count[problem] += 1
    with open('problems_count.txt', 'w', encoding='utf-8') as f:
        for p, count in problems_count.items():
            f.write(f'{p}: {count}\n')
    await message.answer(f"Проблема {problem} выбрана. Спасибо за ваш вклад!", reply_markup=menu_keyboard)

@dp.message(lambda message: message.text == 'Описать проблему')
async def describe_problem(message: types.Message):
    global current_mode
    current_mode = 'problem'
    await message.answer("Пожалуйста опишите вашу проблему:", reply_markup=types.ReplyKeyboardRemove())

@dp.message(lambda message: message.text == 'Предложения по проекту')
async def project_suggestions(message: types.Message):
    global current_mode
    current_mode = 'suggestion'
    await message.answer("Пожалуйста напишите ваше предложение по дополнению проекта:", reply_markup=types.ReplyKeyboardRemove())

@dp.message(lambda message: current_mode is not None and message.text not in ['Описать проблему', 'Предложения по проекту'])
async def handle_input(message: types.Message):
    global current_mode
    if current_mode == 'problem':
        with open('described_problems.txt', 'a', encoding='utf-8') as f:
            f.write(f"{message.text}\n")
        await message.answer("Ваша проблема записана. Спасибо!", reply_markup=menu_keyboard)
        current_mode = None
    elif current_mode == 'suggestion':
        with open('project_suggestions.txt', 'a', encoding='utf-8') as f:
            f.write(f"{message.text}\n")
        await message.answer("Спасибо за ваше предложение!", reply_markup=menu_keyboard)
        current_mode = None

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
