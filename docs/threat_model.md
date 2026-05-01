# Mô hình hiểm họa và Phân tích an ninh

## 1. Giả định hệ thống
- **Thực thể tin cậy:** Node đầu cuối (ESP32) và Backend Server.
- **Thực thể không tin cậy:** Đường truyền mạng Internet và thiết bị Gateway trung gian.
- **Khả năng của kẻ tấn công:** Có khả năng nghe lén, thu chặn, chỉnh sửa và phát lại các gói tin trên đường truyền.

## 2. Các kịch bản tấn công mục tiêu
- **Eavesdropping (Nghe lén):** Kẻ tấn công thu thập dữ liệu thô trên đường truyền Internet.
- **Data Tampering (Sửa đổi dữ liệu):** Kẻ tấn công hoặc Gateway thay đổi nội dung giá trị cảm biến.
- **Replay Attack (Tấn công phát lại):** Kẻ tấn công gửi lại các gói tin hợp lệ đã thu thập được từ trước để làm sai lệch trạng thái hệ thống.
- **Impersonation (Mạo danh):** Thiết bị giả mạo gửi dữ liệu đến Server.

## 3. Phân tích cơ chế phòng chống
- **Tính bí mật (Confidentiality):** Đảm bảo bởi thuật toán AES-128-GCM. Dữ liệu cảm biến được mã hóa trước khi ra khỏi Node.
- **Tính toàn vẹn (Integrity):** Đảm bảo bởi Authentication Tag của GCM và Chữ ký HMAC của Gateway. Bất kỳ sự thay đổi bit nào cũng sẽ dẫn đến sai lệch mã xác thực.
- **Xác thực thực thể (Authentication):** Sử dụng hệ thống khóa đối xứng đa lớp. Server xác thực Gateway qua `GATEWAY_KEY` và xác thực Node qua `NODE_KEY`.
- **Chống tấn công phát lại:** Thực thi thông qua Sequence Number đơn điệu tăng được bảo vệ bên trong lớp mã hóa.
