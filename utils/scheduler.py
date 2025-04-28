from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from db import get_connection
from config import TRANSACTION_TIMEOUT_HOURS

def expire_old_transactions():
    conn = get_connection()
    cur = conn.cursor()
    timeout_threshold = datetime.utcnow() - timedelta(hours=TRANSACTION_TIMEOUT_HOURS)
    cur.execute("UPDATE transactions SET status = 'expired' WHERE status = 'pending' AND created_at < ?", (timeout_threshold.isoformat(),))
    conn.commit()
    conn.close()
    print(f"[{datetime.utcnow()}] تم تحديث المعاملات المنتهية الصلاحية.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(expire_old_transactions, 'interval', hours=1)
    scheduler.start()
