import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command

# Токен вашего бота
API_TOKEN = "7955201672:AAFQK31GYD4cLahmk91iSD_0htMzCepEIA0"

# Список слов для угадывания
WORDS = [
    "привет"
    # ,"море", "яблоко", "собака", "кот", "дом", "машина", "книга", "город",
    # "дерево", "животное", "время", "день", "ночь", "зима", "лето", "весна", "осень", "река",
    # "гора", "небо", "облако", "цветок", "трава", "лес", "птица", "рыба", "звезда", "луна",
    # "солнце", "дождь", "снег", "ветер", "гроза", "радуга", "месяц", "год", "час",
    # "минута", "секунда", "деньги", "карта", "телефон", "компьютер", "интернет", "школа", 
    # "университет", "работа", "отдых", "путешествие", "гостиница", "ресторан", "магазин", "рынок",
    # "банк", "аптека", "полиция", "больница", "парк", "сад", "озеро", "пруд", "река", "море",
    # "океан", "пляж", "порт", "аэропорт", "вокзал", "автобус", "поезд", "самолет", 
    # "велосипед", "мотоцикл", "лодка", "корабль", "яхта", "спорт", "футбол", "хоккей", "баскетбол",
    # "теннис", "плавание", "бег", "йога", "пилатес", "бодибилдинг", "здоровье", "питание",
    # "тренировка", "отдых", "сон"
]

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения состояния игры
games = {}

@dp.message(Command("start"))
async def start_game(message: types.Message):
    # Выбираем случайное слово
    word = random.choice(WORDS)
    # Создаем состояние игры
    games[message.chat.id] = {
        "word": word,
        "guessed_letters": set(),
        "attempts": 10,
    }
    # Отправляем сообщение с приглашением начать игру
    await message.answer(
        f"Я загадал слово из {len(word)} букв. У вас есть {games[message.chat.id]['attempts']} попыток, чтобы угадать его. Введите букву или слово:",
    )

@dp.message()
async def guess_letter(message: types.Message):
    chat_id = message.chat.id
    guess = message.text.lower()

    # Проверяем, что игра начата
    if chat_id not in games:
        await message.answer("Игра не начата. Введите /start, чтобы начать новую игру.")
        return

    # Проверяем, введено ли слово
    if guess == games[chat_id]["word"]:
        await message.answer(
            f"Поздравляем! Вы угадали слово '{games[chat_id]['word']}'! Чтобы попробовать ещё раз, введите /start."
        )
        del games[chat_id]
        return

    # Проверяем, что введена буква
    if len(guess) != 1 or not guess.isalpha():
        await message.answer("Пожалуйста, введите одну букву или слово.")
        return

    # Проверяем, что буква еще не была угадана
    if guess in games[chat_id]["guessed_letters"]:
        await message.answer("Вы уже называли эту букву.")
        return

    # Добавляем букву в множество угаданных
    games[chat_id]["guessed_letters"].add(guess)

    # Проверяем, есть ли буква в слове
    if guess in games[chat_id]["word"]:
        await message.answer(f"Буква '{guess}' есть в слове!")
    else:
        games[chat_id]["attempts"] -= 1
        await message.answer(
            f"Буквы '{guess}' нет в слове. Осталось попыток: {games[chat_id]['attempts']}"
        )

    # Проверяем, выиграл ли игрок
    if set(games[chat_id]["word"]) == games[chat_id]["guessed_letters"]:
        await message.answer(
            f"Поздравляем! Вы угадали слово '{games[chat_id]['word']}'! Чтобы попробовать ещё раз, введите /start."
        )
        del games[chat_id]
        return

    # Проверяем, проиграл ли игрок
    if games[chat_id]["attempts"] == 0:
        await message.answer(
            f"К сожалению, вы проиграли. Загаданное слово было '{games[chat_id]['word']}'. Чтобы начать новую игру, введите /start."
        )
        del games[chat_id]
        return

    # Отправляем текущее состояние слова
    word_state = "".join(
        [
            letter if letter in games[chat_id]["guessed_letters"] else "_"
            for letter in games[chat_id]["word"]
        ]
    )
    await message.answer(f"Слово: {word_state}")

    if all(guess in "guessed_letters" for guess in "word"):
        await message.answer(
            f"Поздравляем! Вы угадали слово '{games[chat_id]['word']}'! Чтобы попробовать ещё раз, введите /start."
        )
        del games[chat_id]
        return

async def main():
    # Удаляем вебхук, если он установлен
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())