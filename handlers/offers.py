from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from db import get_connection

def view_offers(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT offer_id, description, price FROM offers")
    offers = cur.fetchall()
    conn.close()

    if not offers:
        query.edit_message_text("لا توجد عروض متاحة حاليًا.")
        return

    for offer_id, description, price in offers:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("شراء", callback_data=f"buy_{offer_id}")]
        ])
        query.message.reply_text(f"{description}\nالسعر: {price} ريال", reply_markup=keyboard)

def register(dispatcher):
    from telegram.ext import CallbackQueryHandler
    dispatcher.add_handler(CallbackQueryHandler(view_offers, pattern="^view_offers$"))
