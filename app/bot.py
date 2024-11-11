import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Токен вашего бота
API_TOKEN = "7955201672:AAFQK31GYD4cLahmk91iSD_0htMzCepEIA0"

# Список слов для угадывания
WORDS = [
    "привет", "море", "яблоко", "собака", "кот", "дом", "машина", "книга",
    "город", "дерево", "животное", "время", "день", "ночь", "зима", "лето",
    "весна", "осень", "река", "гора", "небо", "облако", "цветок", "трава",
    "лес", "птица", "рыба", "звезда", "луна", "солнце", "дождь", "снег",
    "ветер", "гроза", "радуга", "месяц", "год", "час", "минута", "секунда",
    "деньги", "карта", "телефон", "компьютер", "интернет", "школа",
    "университет", "работа", "отдых", "путешествие", "гостиница", "ресторан",
    "магазин", "рынок", "банк", "аптека", "полиция", "больница", "парк", "сад",
    "озеро", "пруд", "океан", "пляж", "порт", "аэропорт", "вокзал", "автобус",
    "поезд", "самолет", "велосипед", "мотоцикл", "лодка", "корабль", "яхта",
    "спорт", "футбол", "хоккей", "баскетбол", "теннис", "плавание", "бег",
    "йога", "пилатес", "бодибилдинг", "здоровье", "питание", "тренировка",
    "сон"
]

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения состояния игры
games = {}


def get_word_state(word, guessed_letters):
    """Возвращает текущее состояние слова с угаданными буквами."""
    return "".join(letter if letter in guessed_letters else "_"
                   for letter in word)


@dp.message(Command("start"))
async def start_game(message: types.Message):
    """Запускает новую игру для пользователя."""
    word = random.choice(WORDS)
    games[message.chat.id] = {
        "word": word,
        "guessed_letters": set(),
        "attempts": 10
    }

    await message.answer(
        f"Я загадал слово из {len(word)} букв. У вас есть 10 попыток, чтобы угадать его. Введите букву или слово:"
    )


@dp.message()
async def guess_letter(message: types.Message):
    """Обрабатывает попытки пользователя угадать букву или слово."""
    chat_id = message.chat.id
    guess = message.text.lower()

    if chat_id not in games:
        await message.answer(
            "Игра не начата. Введите /start, чтобы начать новую игру.")
        return

    game = games[chat_id]
    word = game["word"]

    # Полное слово угадано
    if guess == word:
        await message.answer(
            f"Поздравляем! Вы угадали слово '{word}'! Введите /start для новой игры."
        )
        del games[chat_id]
        return

    # Проверка на одиночную букву
    if len(guess) != 1 or not guess.isalpha():
        await message.answer("Введите одну букву или слово.")
        return

    # Буква уже была угадана
    if guess in game["guessed_letters"]:
        await message.answer("Эту букву вы уже называли.")
        return

    # Проверка, есть ли буква в слове
    game["guessed_letters"].add(guess)
    if guess in word:
        await message.answer(f"Буква '{guess}' есть в слове!")
    else:
        game["attempts"] -= 1
        await message.answer(
            f"Буквы '{guess}' нет в слове. Осталось попыток: {game['attempts']}"
        )

    # Проверка на победу
    if set(word) == game["guessed_letters"]:
        await message.answer(
            f"Поздравляем! Вы угадали слово '{word}'! Введите /start для новой игры."
        )
        del games[chat_id]
        return

    # Проверка на проигрыш
    if game["attempts"] == 0:
        await message.answer(
            f"Вы проиграли. Загаданное слово было '{word}'. Введите /start для новой игры."
        )
        del games[chat_id]
        return

    # Отправляем текущее состояние слова
    await message.answer(
        f"Слово: {get_word_state(word, game['guessed_letters'])}")


async def main():
    """Запускает бота."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
