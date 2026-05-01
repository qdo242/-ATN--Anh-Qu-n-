import sqlite3
import os

DB_NAME = 'iot_security.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Bảng quản lý thiết bị (Mỗi thiết bị một khóa riêng)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        node_key TEXT NOT NULL,
        gateway_key TEXT NOT NULL,
        last_seq INTEGER DEFAULT -1,
        description TEXT
    )
    ''')
    
    # 2. Bảng lưu trữ dữ liệu cảm biến và nhật ký bảo mật
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        status TEXT,
        error_msg TEXT,
        FOREIGN KEY (device_id) REFERENCES devices (device_id)
    )
    ''')
    
    # Thêm thiết bị mẫu nếu chưa có
    cursor.execute("INSERT OR IGNORE INTO devices VALUES (?, ?, ?, ?, ?)", 
                   ('ESP32_NODE_X', '1234567890123456', 'gateway_secret_k', -1, 'Thiết bị tại phòng Lab'))
    
    conn.commit()
    conn.close()
    print(f"Khởi tạo Database {DB_NAME} thành công.")

if __name__ == "__main__":
    init_db()
