# Nghiên cứu: Cơ chế xác thực Gateway bằng HMAC-SHA256

## 1. Vai trò của Gateway trong kiến trúc
Trong hệ thống IoT, Gateway thường là thiết bị trung gian chuyển tiếp dữ liệu từ mạng nội bộ (Zigbee/LoRa/BLE) lên Internet. Do Gateway tiếp xúc trực tiếp với môi trường Internet, nó trở thành mục tiêu của các cuộc tấn công giả mạo.

## 2. Giải pháp HMAC-SHA256
HMAC (Hash-based Message Authentication Code) cung cấp cơ chế xác nhận rằng bản tin thực sự đến từ Gateway được cấp phép.

### Công thức tính toán:
`HMAC = SHA256( (K XOR opad) || SHA256( (K XOR ipad) || Message ) )`
Trong đó:
- `K`: Khóa bí mật dùng chung giữa Gateway và Server.
- `Message`: Toàn bộ gói tin (bao gồm cả Ciphertext của Node).

## 3. Tại sao không mã hóa lại tại Gateway?
- **Tiết kiệm tài nguyên:** Gateway chỉ cần thực hiện 1 lần băm (Hash), nhanh hơn nhiều so với việc giải mã và mã hóa lại.
- **Bảo mật đầu cuối (End-to-End):** Gateway không được phép biết nội dung dữ liệu của Node. Nếu Gateway bị chiếm quyền, kẻ tấn công cũng không thể đọc được dữ liệu cảm biến (vì không có Node Key).

## 4. Khả năng chống tấn công
- **Chống giả mạo:** Nếu kẻ tấn công không có `Gateway Key`, chúng không thể tạo ra mã HMAC hợp lệ.
- **Xác thực nguồn gốc:** Mỗi Gateway có một ID và Key riêng, giúp Server quản lý chính xác từng thiết bị.
