import requests
import time
import sqlite3
import os
from simulator import simulate_node_to_server
from dotenv import load_dotenv

SERVER_URL = "http://127.0.0.1:5000/receive-data"
DB_NAME = 'iot_security.db'

def reset_db_state():
    """Don dep trang thai thiet bi de bat dau bai test moi"""
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("UPDATE devices SET status = 'active', last_seq = -1 WHERE device_id = 'ESP32_NODE_X'")
        conn.execute("DELETE FROM attack_logs")
        conn.execute("DELETE FROM telemetry")
        conn.commit()
        conn.close()
        print("[*] Da thiet lap trang thai he thong sach.\n")

def run_comprehensive_test():
    reset_db_state()
    print("=== BAT DAU KIEM THU AN NINH CHUYEN SAU ===\n")

    # 1. Giao dich hop le
    print("[1] Gui ban tin hop le (Seq 1)...")
    packet = simulate_node_to_server(temp=25.0, humidity=60, seq=1)
    r = requests.post(SERVER_URL, json={"payload": packet.hex()})
    print(f"Phan hoi: {r.status_code} - {r.json()}\n")

    # 2. Tan cong vao HMAC (Sai khoa Gateway)
    print("[2] Tan cong mạo danh Gateway (Sai HMAC)...")
    tampered_hmac = bytearray(packet)
    tampered_hmac[-1] = tampered_hmac[-1] ^ 0x01
    requests.post(SERVER_URL, json={"payload": bytes(tampered_hmac).hex()})
    print("-> Da ghi nhan no luc tan cong HMAC.\n")

    # 3. Tan cong vao Nonce (AES-GCM Integrity)
    print("[3] Tan cong vao Nonce (Sua doi vector khoi tao)...")
    tampered_nonce = bytearray(packet)
    tampered_nonce[5] = tampered_nonce[5] ^ 0xFF
    # Phai ky lai HMAC de vuot qua lop 1
    from Cryptodome.Hash import HMAC, SHA256
    import os
    load_dotenv()
    GATEWAY_KEY = os.getenv('GATEWAY_KEY', 'gateway_secret_k').encode('utf-8')
    h = HMAC.new(GATEWAY_KEY, digestmod=SHA256)
    h.update(tampered_nonce[:-32])
    final_packet = bytes(tampered_nonce[:-32]) + h.digest()
    r = requests.post(SERVER_URL, json={"payload": final_packet.hex()})
    print(f"Phan hoi: {r.status_code} - {r.json()}\n")

    # 4. Tan cong Replay (Gui lai Seq 1)
    print("[4] Tan cong phat lai (Replay Seq 1)...")
    requests.post(SERVER_URL, json={"payload": packet.hex()})
    print("-> Da ghi nhan no luc Replay.\n")

    # 5. Tan cong dồn dập de kich hoat Blacklist
    print("[5] Mo phong tan cong dồn dập (Brute Force)...")
    for i in range(2):
        fake_packet = os.urandom(64).hex()
        requests.post(SERVER_URL, json={"payload": fake_packet})
    print("-> Thiet bi hien tai se bi tu dong dua vao Blacklist.\n")

    # 6. Kiem tra trang thai Blacklist
    print("[6] Kiem tra sau khi bi chan (Gui lai ban tin hop le Seq 2)...")
    valid_packet_2 = simulate_node_to_server(temp=26.0, humidity=59, seq=2)
    r = requests.post(SERVER_URL, json={"payload": valid_packet_2.hex()})
    print(f"Phan hoi: {r.status_code} - {r.json()}")
    if r.status_code == 403:
        print("=> Ket qua: He thong da chan thiet bi vi pham thanh cong.")

if __name__ == "__main__":
    run_comprehensive_test()
