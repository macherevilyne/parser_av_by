# Используем базовый образ с Python
FROM python:3.10-slim


WORKDIR /app
# Копируем файл зависимостей в контейнер
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .
# Определяем команду для запуска вашего приложения
CMD ["python", "tg_bot.py"]