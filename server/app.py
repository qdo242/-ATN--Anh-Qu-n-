import os
import sqlite3
import time
from flask import Flask, request, jsonify
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
DB_NAME = 'iot_security.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def log_attack(device_id, ip, attack_type, details):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO attack_logs (device_id, ip_address, attack_type, details)
        VALUES (?, ?, ?, ?)
    ''', (device_id, ip, attack_type, details))
    
    # Kiem tra neu thiet bi nay tan cong qua nhieu thi Block
    count = conn.execute('SELECT COUNT(*) FROM attack_logs WHERE device_id = ?', (device_id,)).fetchone()[0]
    if count >= 3:
        conn.execute("UPDATE devices SET status = 'blocked' WHERE device_id = ?", (device_id,))
        print(f"[!] Thiet bi {device_id} da bi dua vao Blacklist do vi pham qua 3 lan.")
        
    conn.commit()
    conn.close()

def verify_and_decrypt(raw_data, client_ip):
    start_time = time.time()
    
    if len(raw_data) < 4 + 12 + 16 + 32:
        return None, "Packet too short", None, 0
        
    gateway_id_hex = raw_data[:4].hex()
    hmac_received = raw_data[-32:]
    data_to_verify = raw_data[:-32]
    encrypted_payload = raw_data[4:-32]

    conn = get_db_connection()
    # Tim thiet bi bat ky (Trong thuc te se tim theo Gateway ID)
    device = conn.execute('SELECT * FROM devices WHERE status = "active" LIMIT 1').fetchone()
    
    if not device:
        # Kiem tra xem co phai thiet bi dang bi block khong
        blocked_device = conn.execute('SELECT * FROM devices WHERE status = "blocked" LIMIT 1').fetchone()
        if blocked_device:
            conn.close()
            return None, "Device is Blacklisted", blocked_device['device_id'], 0
        conn.close()
        return None, "No active device found", None, 0

    gateway_key = device['gateway_key'].encode('utf-8')
    
    # 1. Kiem tra HMAC
    h = HMAC.new(gateway_key, digestmod=SHA256)
    h.update(data_to_verify)
    try:
        h.verify(hmac_received)
    except ValueError:
        log_attack(device['device_id'], client_ip, "HMAC_MISMATCH", "Sai chu ky Gateway")
        conn.close()
        return None, "Gateway HMAC Mismatch", device['device_id'], 0

    # 2. Giai ma AES-GCM
    nonce = encrypted_payload[:12]
    tag = encrypted_payload[-16:]
    ciphertext = encrypted_payload[12:-16]

    try:
        node_key = device['node_key'].encode('utf-8')
        cipher = AES.new(node_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        data = json.loads(plaintext.decode('utf-8'))
        
        # 3. Kiem tra Replay
        if data['seq'] <= device['last_seq']:
            log_attack(device['device_id'], client_ip, "REPLAY_ATTACK", f"Goi tin cu (seq {data['seq']})")
            conn.close()
            return None, "Replay Attack Detected", device['device_id'], 0
        
        # Thanh cong
        conn.execute('UPDATE devices SET last_seq = ? WHERE device_id = ?', (data['seq'], device['device_id']))
        conn.commit()
        conn.close()
        
        latency = time.time() - start_time
        return data, None, device['device_id'], latency
        
    except Exception as e:
        log_attack(device['device_id'], client_ip, "DECRYPTION_FAILED", str(e))
        conn.close()
        return None, f"Decryption failed: {str(e)}", device['device_id'], 0

def log_telemetry(device_id, data, status, latency, error_msg=None):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO telemetry (device_id, temperature, humidity, latency, status, error_msg)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (device_id, data.get('temp') if data else None, 
          data.get('humi') if data else None, latency, status, error_msg))
    conn.commit()
    conn.close()

@app.route('/receive-data', methods=['POST'])
def receive_data():
    json_data = request.get_json()
    if not json_data or 'payload' not in json_data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    try:
        raw_data = bytes.fromhex(json_data['payload'])
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid Hex"}), 400

    data, error, dev_id, latency = verify_and_decrypt(raw_data, request.remote_addr)
    
    if error:
        log_telemetry(dev_id, None, "Canh bao bao mat", latency, error)
        return jsonify({"status": "security_alert", "reason": error}), 403

    log_telemetry(dev_id, data, "An toan", latency)
    return jsonify({"status": "success", "latency": f"{latency:.4f}s"}), 200

if __name__ == "__main__":
    print("=== BACKEND SERVER SECURE EDITION V2 IS RUNNING ===")
    app.run(host='0.0.0.0', port=5000)
