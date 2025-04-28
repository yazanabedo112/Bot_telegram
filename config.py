import os

TELEGRAM_TOKEN = os.getenv('8062347534:AAHAyTRw3EJSf6-BFWm55qTQJnISYqepDaI')
DB_PATH = os.getenv('DB_PATH', 'bot.db')
TRANSACTION_TIMEOUT_HOURS = int(os.getenv('TRANSACTION_TIMEOUT_HOURS', 24))
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
