import random
import asyncio
import requests
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

API_TOKEN = "7955201672:AAFQK31GYD4cLahmk91iSD_0htMzCepEIA0"

WORDS = [
    "привет", "море", "яблоко", "собака", "кот", "дом", "машина", "книга", "город",
    "дерево", "животное", "время", "день", "ночь", "зима", "лето", "весна", "осень", "река",
    "гора", "небо", "облако", "цветок", "трава", "лес", "птица", "рыба", "звезда", "луна",
    "солнце", "дождь", "снег", "ветер", "гроза", "радуга", "месяц", "год", "час",
    "минута", "секунда", "деньги", "карта", "телефон", "компьютер", "интернет", "школа", "университет", "работа",
    "отдых", "путешествие", "гостиница", "ресторан", "магазин", "рынок", "банк", "аптека", "полиция", "больница",
    "парк", "сад", "озеро", "пруд", "река", "море", "океан", "пляж", "порт", "аэропорт",
    "вокзал", "автобус", "поезд", "самолет", "машина", "велосипед", "мотоцикл", "лодка", "корабль", "яхта",
    "спорт", "футбол", "хоккей", "баскетбол", "теннис", "плавание", "бег", "йога", "пилатес", "бодибилдинг",
    "здоровье", "питание", "тренировка", "отдых", "сон"
]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

games = {}

@dp.message(Command("start"))
async def start_game(message: types.Message):
    word = random.choice(WORDS)
    if len(word) > 10:
        valueword = 10
    elif len(word) <= 10 and len(word) >= 5:
        valueword = 7
    else:
        valueword = 5
    games[message.chat.id] = {
        "word": word,
        "guessed_letters": set(),
        "attempts": valueword,
    }
    await message.answer(
        f"Я загадал слово из {len(word)} букв. У вас есть {games[message.chat.id]['attempts']} попыток, чтобы угадать его. Введите букву:",
    )

@dp.message()
async def guess_letter(message: types.Message):
    chat_id = message.chat.id
    letter = message.text.lower()

    # Проверяем, что введена буква
    if len(letter) != 1 or not letter.isalpha():
        await message.answer("Пожалуйста, введите одну букву.")
        return

    # Проверяем, что буква еще не была угадана
    if letter in games[chat_id]["guessed_letters"]:
        await message.answer("Вы уже угадывали эту букву.")
        return

    # Добавляем букву в множество угаданных
    games[chat_id]["guessed_letters"].add(letter)

    # Проверяем, есть ли буква в слове
    if letter in games[chat_id]["word"]:
        await message.answer(f"Буква '{letter}' есть в слове!")
    else:
        games[chat_id]["attempts"] -= 1
        await message.answer(
            f"Буквы '{letter}' нет в слове. Осталось попыток: {games[chat_id]['attempts']}"
        )

    # Создаем текущее состояние слова
    word_state = "".join(
        [
            letter if letter in games[chat_id]["guessed_letters"] else "_"
            for letter in games[chat_id]["word"]
        ]
    )

    # Проверяем, выиграл ли игрок
    if word_state == games[chat_id]["word"]:
        await message.answer(f"Поздравляем! Вы угадали слово '{games[chat_id]['word']}'! Напиши команду /start чтобы начать новую игру.")
        del games[chat_id]
        return

    # Проверяем, проиграл ли игрок
    if games[chat_id]["attempts"] == 0:
        await message.answer(f"К сожалению, вы проиграли. Загаданное слово было '{games[chat_id]['word']}'. Напиши команду /start чтобы начать новую игру.")
        del games[chat_id]
        return

    # Отправляем текущее состояние слова
    await message.answer(f"Слово: {word_state}")

# Инициализация Flask
app = Flask(__name__)

@app.route("/setwebhook/")
def setwebhook():
    TELEGRAM_URL = f'https://api.telegram.org/bot{API_TOKEN}'
    WEBHOOK_URL = 'https://Pakistan1703.pythonanywhere.com'
    s = requests.get(f"{TELEGRAM_URL}/setWebhook?url={WEBHOOK_URL}")
    if s.status_code == 200:
        return "Success"
    else:
        return "Fail"

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = types.Update(**request.json)
    await dp.feed_update(bot, update)
    return "ok"

if __name__ == "__main__":
    app.run()