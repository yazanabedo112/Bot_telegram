from telegram import Update
from telegram.ext import CallbackContext
from db import get_connection

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data.startswith("buy_"):
        offer_id = int(data.split("_")[1])
        user_id = query.from_user.id

        # إنشاء معاملة جديدة
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (user_id, offer_id, status) VALUES (?, ?, ?)", (user_id, offer_id, "pending"))
        conn.commit()
        conn.close()

        query.edit_message_text(f"تم إنشاء معاملة للعرض رقم {offer_id}. الحالة: قيد الانتظار.")

def register(dispatcher):
    from telegram.ext import CallbackQueryHandler
    dispatcher.add_handler(CallbackQueryHandler(handle_callback, pattern="^buy_\\d+$"))
