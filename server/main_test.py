import requests
import time
import sqlite3
import os
from simulator import simulate_node_to_server
from dotenv import load_dotenv

SERVER_URL = "http://127.0.0.1:5000/receive-data"
DB_NAME = 'iot_security.db'

def reset_db_state():
    """Dọn dẹp trạng thái thiết bị để bắt đầu bài test mới"""
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        # Mở khóa thiết bị, đặt lại số thứ tự và xóa nhật ký tấn công cũ
        conn.execute("UPDATE devices SET status = 'active', last_seq = -1 WHERE device_id = 'ESP32_NODE_X'")
        conn.execute("DELETE FROM attack_logs")
        conn.commit()
        conn.close()
        print("[*] Đã đặt lại trạng thái Database sạch để kiểm thử.\n")

def run_comprehensive_test():
    reset_db_state()
    print("=== BẮT ĐẦU KIỂM THỬ KIẾN TRÚC: NODE -> GATEWAY -> SERVER ===\n")

    # 1. Test Gửi dữ liệu Hợp lệ
    print("[1] Gửi bản tin hợp lệ (Đầy đủ HMAC + AES-GCM)...")
    packet = simulate_node_to_server(temp=28.5, humidity=55, seq=1)
    payload_json = {"payload": packet.hex()}
    try:
        r = requests.post(SERVER_URL, json=payload_json)
        print(f"Phản hồi từ Server: {r.status_code} - {r.json()}")
    except Exception as e:
        print(f"Lỗi kết nối tới Server: {e}")
        return

    # 2. Test Tấn công Gateway giả mạo (Sai HMAC)
    print("\n[2] Tấn công Gateway giả mạo (Sai chữ ký HMAC)...")
    tampered_gw_packet = bytearray(packet)
    tampered_gw_packet[0] = 0xFF # Đổi ID Gateway trái phép
    r = requests.post(SERVER_URL, json={"payload": tampered_gw_packet.hex()})
    print(f"Phản hồi từ Server: {r.status_code} - {r.json()}")

    # 3. Test Tấn công phát lại (Replay Attack)
    print("\n[3] Tấn công phát lại (Gửi lại gói tin cũ)...")
    r = requests.post(SERVER_URL, json=payload_json)
    print(f"Phản hồi từ Server: {r.status_code} - {r.json()}")

    # 4. Test Tấn công sửa đổi dữ liệu (Tampering)
    print("\n[4] Tấn công sửa đổi dữ liệu Node (Sai mã xác thực Tag)...")
    valid_packet = simulate_node_to_server(temp=30.0, humidity=50, seq=10)
    tampered_payload = bytearray(valid_packet[:-32])
    tampered_payload[20] = tampered_payload[20] ^ 0xFF # Đảo bit trong ciphertext
    
    from Cryptodome.Hash import HMAC, SHA256
    import os
    from dotenv import load_dotenv
    load_dotenv()
    GATEWAY_KEY = os.getenv('GATEWAY_KEY', 'default_gw_key_').encode('utf-8')
    h = HMAC.new(GATEWAY_KEY, digestmod=SHA256)
    h.update(tampered_payload)
    final_tampered = bytes(tampered_payload) + h.digest()
    
    r = requests.post(SERVER_URL, json={"payload": final_tampered.hex()})
    print(f"Phản hồi từ Server: {r.status_code} - {r.json()}")

if __name__ == "__main__":
    run_comprehensive_test()
