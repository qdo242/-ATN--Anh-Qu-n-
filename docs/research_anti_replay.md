# Nghiên cứu: Cơ chế chống tấn công phát lại (Anti-Replay)

## 1. Định nghĩa bài toán
Tấn công phát lại (Replay Attack) xảy ra khi kẻ tấn công thu chặn một bản tin hợp lệ (ví dụ: lệnh mở cửa hoặc bản tin nhiệt độ cao) và gửi lại bản tin đó vào một thời điểm khác để đánh lừa hệ thống.

## 2. Cơ chế Sequence Number (Số thứ tự)
Mỗi bản tin được gán một số thứ tự tăng dần (`seq`).
- **Phía Node:** Tăng `seq` sau mỗi lần gửi tin thành công. Số này phải nằm trong Payload mã hóa.
- **Phía Server:** Lưu trữ giá trị `last_seq` của từng thiết bị.

### Logic kiểm tra:
`Nếu (Gói_tin_mới.seq > last_seq) -> Chấp nhận`
`Nếu (Gói_tin_mới.seq <= last_seq) -> Cảnh báo tấn công Replay`

## 3. Tại sao seq phải nằm bên trong Payload mã hóa?
Nếu `seq` nằm ngoài bản mã, kẻ tấn công có thể dễ dàng sửa đổi số thứ tự trước khi gửi lại. Khi `seq` nằm bên trong lớp mã hóa AES-GCM, bất kỳ sự thay đổi nào vào số thứ tự cũng sẽ làm hỏng `Auth Tag`, dẫn đến việc giải mã thất bại.

## 4. Ưu điểm so với Timestamp
Sử dụng Timestamp yêu cầu Node và Server phải đồng bộ thời gian thực (NTP), điều này rất khó khăn với các thiết bị IoT không có pin RTC hoặc kết nối mạng không ổn định. Sequence Number là giải pháp thay thế đơn giản và hiệu quả nhất.
