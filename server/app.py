import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
import json

# Nap bien moi truong tu file .env
load_dotenv()

app = Flask(__name__)

# Cau hinh bao mat tu file .env
NODE_KEY = os.getenv('NODE_KEY', 'default_node_key_').encode('utf-8')
GATEWAY_KEY = os.getenv('GATEWAY_KEY', 'default_gw_key_').encode('utf-8')
last_sequence = -1
LOG_FILE = 'data_log.json'


def save_to_log(data, status="Thành công"):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            try: logs = json.load(f)
            except: logs = []
    logs.insert(0, {"status": status, "data": data})
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs[:20], f, ensure_ascii=False)

def verify_and_decrypt(raw_data):
    global last_sequence
    
    # 1. Tách gói tin: [GatewayID(4)] [Nonce(12)] [Cipher(n)] [Tag(16)] [HMAC(32)]
    if len(raw_data) < 4 + 12 + 16 + 32:
        return None, "Gói tin quá ngắn"
        
    gateway_id = raw_data[:4]
    hmac_received = raw_data[-32:]
    data_to_verify = raw_data[:-32]
    encrypted_payload = raw_data[4:-32]

    # 2. Kiểm tra HMAC (Xác thực Gateway)
    h = HMAC.new(GATEWAY_KEY, digestmod=SHA256)
    h.update(data_to_verify)
    try:
        h.verify(hmac_received)
    except ValueError:
        return None, f"Xác thực Gateway thất bại (HMAC sai) từ GW: {gateway_id.hex()}"

    # 3. Giải mã Payload (AES-GCM)
    nonce = encrypted_payload[:12]
    tag = encrypted_payload[-16:]
    ciphertext = encrypted_payload[12:-16]

    try:
        cipher = AES.new(NODE_KEY, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        data = json.loads(plaintext.decode('utf-8'))
        
        # 4. Kiểm tra chống tấn công phát lại (Anti-Replay)
        if data['seq'] <= last_sequence:
            return None, "Phát hiện tấn công phát lại (Replay Attack)"
        
        last_sequence = data['seq']
        return data, None
    except Exception as e:
        return None, f"Giải mã dữ liệu Node thất bại: {str(e)}"

@app.route('/receive-data', methods=['POST'])
def receive_data():
    # Nhận dữ liệu dưới dạng JSON
    json_data = request.get_json()
    if not json_data or 'payload' not in json_data:
        return jsonify({"status": "error", "message": "JSON không hợp lệ hoặc thiếu payload"}), 400

    try:
        # Chuyển chuỗi Hex thành bytes
        raw_data = bytes.fromhex(json_data['payload'])
    except ValueError:
        return jsonify({"status": "error", "message": "Payload phải là chuỗi Hex"}), 400

    data, error = verify_and_decrypt(raw_data)
    
    if error:
        save_to_log({"error": error}, status="Cảnh báo bảo mật")
        print(f"[!] Cảnh báo: {error}")
        return jsonify({"status": "security_alert", "reason": error}), 403

    save_to_log(data, status="An toàn")
    print(f"[+] Dữ liệu sạch nhận được: {data}")
    return jsonify({"status": "success", "gw_verified": True}), 200

if __name__ == "__main__":
    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
    print("=== BACKEND SERVER ĐANG CHẠY (BẢO VỆ BỞI HMAC VÀ AES-GCM) ===")
    app.run(host='0.0.0.0', port=5000)
