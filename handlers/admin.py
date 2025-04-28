from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from config import ADMIN_IDS
from db import get_connection

def is_admin(user_id):
    return user_id in ADMIN_IDS

def admin(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("ليس لديك صلاحية الوصول إلى هذه الأوامر.")
        return

    update.message.reply_text("مرحبًا بك في لوحة الإدارة. استخدم الأوامر التالية:\n/broadcast <message>\n/pending\n/refund <tx_id>")

def broadcast(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("ليس لديك صلاحية الوصول إلى هذه الأوامر.")
        return

    message = ' '.join(context.args)
    if not message:
        update.message.reply_text("يرجى تحديد الرسالة للإرسال.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    conn.close()

    for (uid,) in users:
        try:
            context.bot.send_message(chat_id=uid, text=message)
        except Exception as e:
            print(f"خطأ في إرسال الرسالة إلى {uid}: {e}")

    update.message.reply_text("تم إرسال الرسالة إلى جميع المستخدمين.")

def pending(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("ليس لديك صلاحية الوصول إلى هذه الأوامر.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tx_id, user_id, offer_id FROM transactions WHERE status = 'pending'")
    transactions = cur.fetchall()
    conn.close()

    if not transactions:
        update.message.reply_text("لا توجد معاملات معلقة.")
        return

    message = "📋 المعاملات المعلقة:\n"
    for tx_id, uid, offer_id in transactions:
        message += f"- معاملة رقم {tx_id} للمستخدم {uid} على العرض {offer_id}\n"

    update.message.reply_text(message)

def refund(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("ليس لديك صلاحية الوصول إلى هذه الأوامر.")
        return

    if not context.args:
        update.message.reply_text("يرجى تحديد رقم المعاملة.")
        return

    tx_id = context.args[0]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE transactions SET status = 'refunded' WHERE tx_id = ?", (tx_id,))
    conn.commit()
    conn.close()

    update.message.reply_text(f"تم رد المبلغ للمعاملة رقم {tx_id}.")

def register(dispatcher):
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast))
    dispatcher.add_handler(CommandHandler("pending", pending))
    dispatcher.add_handler(CommandHandler("refund", refund))
