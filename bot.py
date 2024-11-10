import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Токен вашего бота
API_TOKEN = '7955201672:AAFQK31GYD4cLahmk91iSD_0htMzCepEIA0'

# Список слов для угадывания
WORDS = ['hello', 'world', 'python', 'aiogram', 'bot', 'game', 'hangman', 'word', 'guess', 'play']

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения состояния игры
games = {}

# Клавиатура с кнопками для ввода букв
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for letter in 'abcdefghijklmnopqrstuvwxyz':
    keyboard.add(KeyboardButton(letter))

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    # Выбираем случайное слово
    word = random.choice(WORDS)
    # Создаем состояние игры
    games[message.chat.id] = {
        'word': word,
        'guessed_letters': set(),
        'attempts': 6,
    }
    # Отправляем сообщение с приглашением начать игру
    await message.answer(f"Я загадал слово из {len(word)} букв. У вас есть {games[message.chat.id]['attempts']} попыток, чтобы угадать его. Введите букву:", reply_markup=keyboard)

@dp.message_handler()
async def guess_letter(message: types.Message):
    chat_id = message.chat.id
    letter = message.text.lower()

    # Проверяем, что введена буква
    if len(letter) != 1 or not letter.isalpha():
        await message.answer("Пожалуйста, введите одну букву.")
        return

    # Проверяем, что буква еще не была угадана
    if letter in games[chat_id]['guessed_letters']:
        await message.answer("Вы уже угадывали эту букву.")
        return

    # Добавляем букву в множество угаданных
    games[chat_id]['guessed_letters'].add(letter)

    # Проверяем, есть ли буква в слове
    if letter in games[chat_id]['word']:
        await message.answer(f"Буква '{letter}' есть в слове!")
    else:
        games[chat_id]['attempts'] -= 1
        await message.answer(f"Буквы '{letter}' нет в слове. Осталось попыток: {games[chat_id]['attempts']}")

    # Проверяем, выиграл ли игрок
    if set(games[chat_id]['word']) == games[chat_id]['guessed_letters']:
        await message.answer(f"Поздравляем! Вы угадали слово '{games[chat_id]['word']}'!")
        del games[chat_id]
        return

    # Проверяем, проиграл ли игрок
    if games[chat_id]['attempts'] == 0:
        await message.answer(f"К сожалению, вы проиграли. Загаданное слово было '{games[chat_id]['word']}'.")
        del games[chat_id]
        return

    # Отправляем текущее состояние слова
    word_state = ''.join([letter if letter in games[chat_id]['guessed_letters'] else '_' for letter in games[chat_id]['word']])
    await message.answer(f"Слово: {word_state}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)