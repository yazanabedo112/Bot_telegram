from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler

def menu(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 عرض العروض", callback_data="view_offers")],
        [InlineKeyboardButton("📦 معاملاتي", callback_data="my_transactions")]
    ])
    update.message.reply_text("اختر من القائمة:", reply_markup=keyboard)

def register(dispatcher):
    dispatcher.add_handler(CommandHandler("menu", menu))
