import os
import sqlite3
from flask import Flask, request, jsonify
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
import json

app = Flask(__name__)
DB_NAME = 'iot_security.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def verify_and_decrypt(raw_data):
    # 1. Tách gói tin thô để lấy ID Gateway
    if len(raw_data) < 4 + 12 + 16 + 32:
        return None, "Gói tin quá ngắn", None
        
    gateway_id_hex = raw_data[:4].hex()
    hmac_received = raw_data[-32:]
    data_to_verify = raw_data[:-32]
    encrypted_payload = raw_data[4:-32]

    # 2. Truy vấn thông tin thiết bị từ DB (Dựa trên Gateway ID giả định hoặc Device ID bên trong)
    # Trong kịch bản thực tế, Gateway ID sẽ giúp tìm GATEWAY_KEY
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE gateway_key IS NOT NULL LIMIT 1').fetchone()
    
    if not device:
        conn.close()
        return None, "Không tìm thấy thông tin Gateway trong Database", None

    gateway_key = device['gateway_key'].encode('utf-8')
    
    # 3. Kiểm tra HMAC (Xác thực Gateway)
    h = HMAC.new(gateway_key, digestmod=SHA256)
    h.update(data_to_verify)
    try:
        h.verify(hmac_received)
    except ValueError:
        conn.close()
        return None, f"Xác thực Gateway thất bại (HMAC sai)", device['device_id']

    # 4. Giải mã Payload (AES-GCM)
    nonce = encrypted_payload[:12]
    tag = encrypted_payload[-16:]
    ciphertext = encrypted_payload[12:-16]

    try:
        # Lấy khóa của Node tương ứng
        node_key = device['node_key'].encode('utf-8')
        cipher = AES.new(node_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        data = json.loads(plaintext.decode('utf-8'))
        
        # 5. Kiểm tra chống tấn công phát lại (Anti-Replay)
        if data['seq'] <= device['last_seq']:
            conn.close()
            return None, "Phát hiện tấn công phát lại (Replay Attack)", device['device_id']
        
        # Cập nhật Sequence Number mới vào DB
        conn.execute('UPDATE devices SET last_seq = ? WHERE device_id = ?', (data['seq'], device['device_id']))
        conn.commit()
        conn.close()
        return data, None, device['device_id']
    except Exception as e:
        conn.close()
        return None, f"Giải mã dữ liệu Node thất bại: {str(e)}", device['device_id']

def log_telemetry(device_id, data, status, error_msg=None):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO telemetry (device_id, temperature, humidity, status, error_msg)
        VALUES (?, ?, ?, ?, ?)
    ''', (device_id, data.get('temp') if data else None, 
          data.get('humi') if data else None, status, error_msg))
    conn.commit()
    conn.close()

@app.route('/receive-data', methods=['POST'])
def receive_data():
    json_data = request.get_json()
    if not json_data or 'payload' not in json_data:
        return jsonify({"status": "error", "message": "JSON không hợp lệ"}), 400

    try:
        raw_data = bytes.fromhex(json_data['payload'])
    except ValueError:
        return jsonify({"status": "error", "message": "Payload phải là chuỗi Hex"}), 400

    data, error, dev_id = verify_and_decrypt(raw_data)
    
    if error:
        log_telemetry(dev_id, None, "Cảnh báo bảo mật", error)
        print(f"[!] Cảnh báo: {error}")
        return jsonify({"status": "security_alert", "reason": error}), 403

    log_telemetry(dev_id, data, "An toàn")
    print(f"[+] Dữ liệu sạch nhận được: {data}")
    return jsonify({"status": "success", "gw_verified": True}), 200

if __name__ == "__main__":
    print("=== BACKEND SERVER SQLITE EDITION IS RUNNING ===")
    app.run(host='0.0.0.0', port=5000)
