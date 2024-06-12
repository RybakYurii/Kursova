import telebot
import requests
from prometheus_client import start_http_server, Counter
import logging
from os import environ

# Встановлюємо логування
FORMAT = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger()


# Ваш токен від BotFather
TOKEN = environ.get("MY_TELEGRAM_BOT_TOKEN","define me")
bot = telebot.TeleBot(TOKEN)
logger.info("Bot Started")

# Google Books API URL
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

# Prometheus метрики
REQUESTS = Counter('telegram_bot_requests', 'Number of requests received')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт! Введіть назву книжки або автора, щоб знайти інформацію про книжки.")

@bot.message_handler(func=lambda message: True)
def search_books(message):
    REQUESTS.inc()
    query = message.text
    response = requests.get(GOOGLE_BOOKS_API_URL, params={'q': query, 'maxResults': 3})
    
    if response.status_code == 200:
        books = response.json().get('items', [])
        if books:
            for book in books:
                title = book['volumeInfo'].get('title', 'Немає назви')
                authors = ', '.join(book['volumeInfo'].get('authors', ['Невідомий автор']))
                description = book['volumeInfo'].get('description', 'Опису немає')
                bot.send_message(message.chat.id, f"Назва: {title}\nАвтори: {authors}\nОпис: {description}")
        else:
            bot.send_message(message.chat.id, "Не знайдено книжок за вашим запитом.")
    else:
        bot.send_message(message.chat.id, "Сталася помилка при пошуку книжок. Спробуйте ще раз пізніше.")

if __name__ == '__main__':
    start_http_server(8000)  # Відкрийте порт для Prometheus
    bot.polling()
