# Вибираємо базовий образ
FROM python:3.10-slim

# Встановлюємо залежності
RUN pip install pyTelegramBotAPI requests prometheus_client

# Копіюємо файли бота в контейнер
COPY . /app
WORKDIR /app

EXPOSE 8000

# Вказуємо команду для запуску бота
CMD ["python", "rybot.py"]
