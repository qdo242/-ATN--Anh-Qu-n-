# Phân tích hiệu năng và tính khả thi của giải pháp

## 1. Hạn chế của các giao thức bảo mật lớp dưới
Việc triển khai các giao thức bảo mật tiêu chuẩn (như TLS) trên thiết bị nhúng ESP32 thường gặp các rào cản kỹ thuật:
- **Tài nguyên bộ nhớ:** Quá trình thiết lập kết nối (Handshake) yêu cầu dung lượng RAM lớn cho các chứng chỉ số và bộ đệm.
- **Tiêu thụ năng lượng:** Các phép toán mã hóa bất đối xứng tiêu tốn chu kỳ xử lý của CPU, ảnh hưởng đến thời lượng pin.
- **Băng thông:** Tiêu đề (Header) của các giao thức này thường lớn so với kích thước thực tế của dữ liệu cảm biến.

## 2. Đặc điểm của giải pháp mã hóa tầng ứng dụng
Giải pháp thiết kế tập trung vào mã hóa đối xứng tại lớp ứng dụng, sử dụng các tham số định lượng sau để đánh giá:
- **Dung lượng Payload:** Kích thước gói tin sau mã hóa tăng thêm cố định 28 bytes (12 bytes Nonce + 16 bytes Tag) so với dữ liệu gốc.
- **Chi phí tính toán:** Đo lường bằng chu kỳ CPU hoặc thời gian thực thi (ms) trên vi điều khiển ESP32.
- **Năng lượng tiêu thụ:** Ước tính dựa trên dòng điện trung bình khi vi điều khiển hoạt động trong chế độ có và không có bộ tăng tốc AES phần cứng.

## 3. Phân tích so sánh thực nghiệm

| Tiêu chí | Giải pháp mã hóa ứng dụng (Đề xuất) | Giao thức truyền thống (TLS 1.2/1.3) |
| :--- | :--- | :--- |
| **Dung lượng Header/Overhead** | ~60-80 bytes | > 2000 bytes (Handshake) |
| **Độ trễ thiết lập (Latency)** | < 10 ms (Không handshake) | 100-500 ms (Handshake) |
| **Yêu cầu RAM tối thiểu** | < 10 KB | 30-50 KB |
| **Độ phức tạp thuật toán** | O(n) | O(n^2) trong giai đoạn handshake |
