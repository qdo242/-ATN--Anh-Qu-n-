# Kiến trúc hệ thống

### 1. Luồng dữ liệu bảo mật
- **Tại Node:** Dữ liệu cảm biến được mã hóa bằng AES-128-GCM, tạo ra Ciphertext và mã xác thực Tag.
- **Tại Gateway:** Gateway thêm mã định danh ID và ký chữ ký số HMAC-SHA256 lên toàn bộ gói tin.
- **Tại Server:** Server kiểm tra HMAC để xác thực Gateway, sau đó giải mã AES để lấy dữ liệu Node.

### 2. Các lớp bảo vệ
- **Lớp 1 (HMAC):** Xác thực nguồn gốc Gateway, chống giả mạo gói tin trên Internet.
- **Lớp 2 (AES-GCM):** Mã hóa đầu cuối dữ liệu cảm biến, đảm bảo tính bí mật ngay cả khi Gateway bị hack.
- **Lớp 3 (Sequence Number):** Chống tấn công phát lại bằng cách kiểm tra số thứ tự bản tin.
