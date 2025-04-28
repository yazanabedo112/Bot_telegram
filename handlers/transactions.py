from telegram import Update
from telegram.ext import CallbackContext
from db import get_connection

def my_transactions(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tx_id, offer_id, status FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cur.fetchall()
    conn.close()

    if not transactions:
        query.edit_message_text("لا توجد معاملات حالية.")
        return

    message = "📦 معاملاتك:\n"
    for tx_id, offer_id, status in transactions:
        message += f"- معاملة رقم {tx_id} للعرض {offer_id}: الحالة {status}\n"

    query.edit_message_text(message)

def register(dispatcher):
    from telegram.ext import CallbackQueryHandler
    dispatcher.add_handler(CallbackQueryHandler(my_transactions, pattern="^my_transactions$"))
