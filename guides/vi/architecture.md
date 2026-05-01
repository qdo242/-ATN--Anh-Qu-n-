# Tài liệu Kiến trúc Hệ thống Bảo mật

## 1. Mô hình bảo mật đa lớp
Hệ thống thực thi cơ chế bảo mật tại tầng ứng dụng, độc lập với các giao thức truyền dẫn lớp dưới. Mô hình dựa trên sự kết hợp giữa mã hóa đối xứng xác thực (AEAD) và mã xác thực thông điệp dựa trên băm (HMAC).

### 1.1. Tầng thực thể Node (End-to-End Encryption)
- **Thuật toán:** AES-128-GCM.
- **Chức năng:** Đảm bảo tính bí mật và toàn vẹn dữ liệu từ Node đến Server. 
- **Tham số:** Sử dụng Nonce 96-bit ngẫu nhiên cho mỗi phiên truyền tin để chống lại các cuộc tấn công phân tích mật mã.

### 1.2. Tầng Gateway (Authentication Overlay)
- **Thuật toán:** HMAC-SHA256.
- **Chức năng:** Xác thực thực thể Gateway và đảm bảo tính toàn vẹn của toàn bộ gói tin khi truyền tải qua môi trường Internet.
- **Cơ chế:** Gateway thực hiện ký số trên gói tin đã mã hóa của Node, đảm bảo Server có thể nhận diện chính xác nguồn gốc dữ liệu.

## 2. Quy trình xử lý dữ liệu
1. **Khởi tạo:** Node đóng gói dữ liệu cảm biến kèm số thứ tự (Sequence Number).
2. **Mã hóa lớp 1:** Node thực hiện AES-GCM với `NODE_KEY`.
3. **Ký số lớp 2:** Gateway nhận gói tin từ Node, đính kèm `Gateway ID` và thực hiện HMAC với `GATEWAY_KEY`.
4. **Xác thực và Giải mã:** Server kiểm tra HMAC trước khi tiến hành giải mã lớp AES-GCM nội bộ.
