import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DB_PATH = os.getenv('DB_PATH', 'bot.db')
TRANSACTION_TIMEOUT_HOURS = int(os.getenv('TRANSACTION_TIMEOUT_HOURS', 24))
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
