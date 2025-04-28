from telegram.ext import Updater
from config import TELEGRAM_TOKEN
from db import init_db
from handlers import start, menu, offers, transactions, callbacks, admin

def main():
    init_db()
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # تسجيل المعالجات
    start.register(dp)
    menu.register(dp)
    offers.register(dp)
    transactions.register(dp)
    callbacks.register(dp)
    admin.register(dp)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
