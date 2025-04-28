import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# إعدادات الاتصال بـ Google Sheets
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = '../telegram-p2p-bot-2df6dfe540a1.json'  # استبدل بالمسار الفعلي لملف الاعتماد
SPREADSHEET_NAME = 'telegramp2p'  # استبدل باسم جدول البيانات الخاص بك

def get_worksheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

def log_transaction(user_id, offer_id, status):
    sheet = get_worksheet()
    timestamp = datetime.utcnow().isoformat()
    sheet.append_row([timestamp, user_id, offer_id, status])
