from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, CommandHandler
from db import get_connection

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # التحقق من وجود المستخدم في قاعدة البيانات
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT phone_number FROM users WHERE user_id = ?", (user.id,))
    result = cur.fetchone()
    conn.close()

    if result:
        update.message.reply_text("مرحبًا بك مرة أخرى!")
    else:
        # طلب رقم الهاتف
        keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📞 مشاركة رقم الهاتف", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        update.message.reply_text("مرحبًا! الرجاء مشاركة رقم هاتفك للمتابعة.", reply_markup=keyboard)

def register(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
