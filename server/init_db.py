import sqlite3
import os

DB_NAME = 'iot_security.db'

def init_db():
    # Xoa file DB cu de dam bao cau truc moi nhat (Cach triet de nhat cho dev)
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            print(f"Da xoa file {DB_NAME} cu de cap nhat cau truc moi.")
        except Exception as e:
            print(f"Khong the xoa file DB: {e}. Hay dam bao ban da tat tat ca terminal dang chay app.py")
            return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Bang quan ly thiet bi
    cursor.execute('''
    CREATE TABLE devices (
        device_id TEXT PRIMARY KEY,
        node_key TEXT NOT NULL,
        gateway_key TEXT NOT NULL,
        last_seq INTEGER DEFAULT -1,
        status TEXT DEFAULT 'active',
        description TEXT
    )
    ''')
    
    # 2. Bang luu tru telemetry
    cursor.execute('''
    CREATE TABLE telemetry (
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
    
    # 3. Bang nhat ky tan cong
    cursor.execute('''
    CREATE TABLE attack_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        ip_address TEXT,
        attack_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    )
    ''')
    
    # Them thiet bi mau
    cursor.execute("INSERT INTO devices (device_id, node_key, gateway_key, description) VALUES (?, ?, ?, ?)", 
                   ('ESP32_NODE_X', '1234567890123456', 'gateway_secret_k', 'Thiet bi tai phong Lab'))
    
    conn.commit()
    conn.close()
    print(f"Khoi tao Database {DB_NAME} phien ban moi thanh cong.")

if __name__ == "__main__":
    init_db()
