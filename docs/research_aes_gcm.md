# Nghiên cứu thuật toán AES-GCM trong hệ thống IoT

## 1. Tổng quan
AES-GCM (Galois/Counter Mode) là một chế độ vận hành của mã hóa khối AES, thuộc nhóm AEAD (Authenticated Encryption with Associated Data). Thuật toán này cung cấp đồng thời chức năng mã hóa dữ liệu và xác thực tính toàn vẹn thông qua mã xác thực (Authentication Tag).

## 2. Phân tích kỹ thuật
So với các chế độ mã hóa khác:
- **AES-CBC:** Yêu cầu thêm cơ chế xác thực bên ngoài (ví dụ HMAC) để đảm bảo tính toàn vẹn. Việc kết hợp này có thể dẫn đến các lỗ hổng bảo mật nếu triển khai không đúng cách (như lỗi Padding Oracle).
- **AES-CTR:** Chỉ cung cấp tính bí mật, không có khả năng phát hiện sự thay đổi dữ liệu trên đường truyền.
- **AES-GCM:** Tích hợp sẵn cơ chế xác thực. Quá trình giải mã sẽ đi kèm với việc kiểm tra Tag; nếu dữ liệu bị thay đổi, hệ thống sẽ phát hiện và dừng xử lý bản tin.

## 3. Cơ chế vận hành
1. **Bộ đếm (Counter):** Sử dụng giá trị Nonce kết hợp bộ đếm để tạo ra dòng khóa (Key stream) thực hiện phép XOR với dữ liệu gốc.
2. **Hàm GHASH:** Thực hiện phép nhân trên trường Galois (GF(2^128)) để tạo ra mã xác thực cho cả dữ liệu mã hóa và dữ liệu liên quan (Associated Data).
3. **Hiệu năng phần cứng:** AES-GCM có khả năng tính toán song song, phù hợp với các vi xử lý có bộ tăng tốc phần cứng AES như ESP32.

## 4. Kiểm soát Nonce
Rủi ro mật mã học của GCM xảy ra khi lặp lại cặp (Khóa, Nonce). 
- **Giải pháp:** Hệ thống thực thi việc khởi tạo Nonce ngẫu nhiên 12-byte cho mỗi phiên truyền tin và kiểm tra số thứ tự (Sequence Number) được đóng gói bên trong lớp mã hóa.
