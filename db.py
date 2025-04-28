import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # إنشاء جدول المستخدمين
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            phone TEXT
        )
    ''')

    # إنشاء جدول العروض
    cur.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,  -- بيع أو شراء
            price REAL,
            min_amount REAL,
            max_amount REAL,
            payments TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # إنشاء جدول المعاملات
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER,
            buyer_id INTEGER,
            seller_id INTEGER,
            amount REAL,
            status TEXT,  -- pending, completed, expired, refunded
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(offer_id) REFERENCES offers(id),
            FOREIGN KEY(buyer_id) REFERENCES users(user_id),
            FOREIGN KEY(seller_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()
