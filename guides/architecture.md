# Kiến trúc hệ thống / System Architecture

## Tiếng Việt

### 1. Luồng dữ liệu bảo mật
- **Tại Node:** Dữ liệu cảm biến được mã hóa bằng AES-128-GCM, tạo ra Ciphertext và mã xác thực Tag.
- **Tại Gateway:** Gateway thêm mã định danh ID và ký chữ ký số HMAC-SHA256 lên toàn bộ gói tin.
- **Tại Server:** Server kiểm tra HMAC để xác thực Gateway, sau đó giải mã AES để lấy dữ liệu Node.

### 2. Các lớp bảo vệ
- **Lớp 1 (HMAC):** Xác thực nguồn gốc Gateway, chống giả mạo gói tin trên Internet.
- **Lớp 2 (AES-GCM):** Mã hóa đầu cuối dữ liệu cảm biến, đảm bảo tính bí mật ngay cả khi Gateway bị hack.
- **Lớp 3 (Sequence Number):** Chống tấn công phát lại bằng cách kiểm tra số thứ tự bản tin.

---

## English

### 1. Secure Data Flow
- **At the Node:** Sensor data is encrypted using AES-128-GCM, generating a Ciphertext and an Authentication Tag.
- **At the Gateway:** The Gateway appends its Identifier (ID) and signs the entire packet with an HMAC-SHA256 digital signature.
- **At the Server:** The Server verifies the HMAC to authenticate the Gateway, then decrypts the AES layer to retrieve the Node data.

### 2. Protection Layers
- **Layer 1 (HMAC):** Authenticates the Gateway origin and prevents packet tampering over the Internet.
- **Layer 2 (AES-GCM):** End-to-end encryption for sensor data, ensuring confidentiality even if the Gateway is compromised.
- **Layer 3 (Sequence Number):** Prevents Replay Attacks by verifying the message sequence number.
