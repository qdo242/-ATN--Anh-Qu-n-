import sqlite3
import os

DB_NAME = 'iot_security.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Bang quan ly thiet bi (Them cot status de quan ly Blacklist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        node_key TEXT NOT NULL,
        gateway_key TEXT NOT NULL,
        last_seq INTEGER DEFAULT -1,
        status TEXT DEFAULT 'active',
        description TEXT
    )
    ''')
    
    # 2. Bang luu tru telemetry (Them cot latency)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        latency REAL,
        status TEXT,
        error_msg TEXT,
        FOREIGN KEY (device_id) REFERENCES devices (device_id)
    )
    ''')
    
    # 3. Bang nhat ky tan cong chi tiet
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attack_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        ip_address TEXT,
        attack_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    )
    ''')
    
    # Them thiet bi mau neu chua co
    cursor.execute("INSERT OR IGNORE INTO devices (device_id, node_key, gateway_key, description) VALUES (?, ?, ?, ?)", 
                   ('ESP32_NODE_X', '1234567890123456', 'gateway_secret_k', 'Thiet bi tai phong Lab'))
    
    conn.commit()
    conn.close()
    print(f"Cap nhat Database {DB_NAME} thanh cong.")

if __name__ == "__main__":
    init_db()
