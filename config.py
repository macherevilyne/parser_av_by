user_id = 861022438


from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')