import os
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
import json
import secrets

# Nap bien moi truong
load_dotenv()

# Khoa bi mat (Lay tu file .env)
NODE_KEY = os.getenv('NODE_KEY', 'default_node_key_').encode('utf-8')
GATEWAY_KEY = os.getenv('GATEWAY_KEY', 'default_gw_key_').encode('utf-8')
GATEWAY_ID = b'\x00\x00\x00\x01' # ID của Gateway (4 bytes)

def simulate_node_to_server(temp, humidity, seq):
    """
    Quy trình:
    1. Node mã hóa dữ liệu (AES-GCM)
    2. Gateway bọc thêm ID và ký HMAC (Xác thực nguồn gốc)
    """
    # --- PHẦN NODE (ESP32 X) ---
    data = {"id": "ESP32_NODE_X", "temp": temp, "humi": humidity, "seq": seq}
    plaintext = json.dumps(data).encode('utf-8')
    nonce = secrets.token_bytes(12)
    cipher = AES.new(NODE_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # Payload từ Node gửi cho Gateway
    node_payload = nonce + ciphertext + tag
    
    # --- PHẦN GATEWAY (ESP32 GW) ---
    # Gateway thêm ID của mình vào đầu
    packet_to_sign = GATEWAY_ID + node_payload
    
    # Gateway ký HMAC bằng GATEWAY_KEY
    h = HMAC.new(GATEWAY_KEY, digestmod=SHA256)
    h.update(packet_to_sign)
    hmac_sig = h.digest() # 32 bytes SHA256
    
    # Gói tin cuối cùng gửi lên Server
    final_packet = packet_to_sign + hmac_sig
    return final_packet

if __name__ == "__main__":
    p = simulate_node_to_server(25.0, 60, 1)
    print(f"Generated Secure Packet: {p.hex()}")
