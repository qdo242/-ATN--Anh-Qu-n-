# Hướng dẫn thiết lập và Kiểm thử hệ thống

Tài liệu này cung cấp quy trình từng bước để triển khai và kiểm chứng hệ thống mã hóa dữ liệu IoT sau khi tải mã nguồn từ GitHub.

## 1. Chuẩn bị môi trường
Yêu cầu: Máy tính đã cài đặt Python 3.9+.

### Bước 1: Cài đặt thư viện phụ thuộc
Mở cửa sổ dòng lệnh tại thư mục dự án và thực thi lệnh cài đặt các thư viện mật mã và giao diện:
```powershell
pip install pycryptodomex flask streamlit pandas plotly requests python-dotenv
```

### Bước 2: Thiết lập cấu hình bảo mật (.env)
Do lý do an ninh, các khóa bí mật không được lưu trữ trên Git. Bạn cần tạo một tệp tin mới tên là `.env` tại thư mục gốc của dự án với nội dung chính xác như sau:
```text
NODE_KEY=1234567890123456
GATEWAY_KEY=gateway_secret_k
```

## 2. Quy trình kiểm thử (Testing)
Để xác nhận hệ thống hoạt động chính xác, vui lòng thực hiện theo trình tự 4 bước dưới đây (mỗi bước trong một cửa sổ dòng lệnh riêng):

### Bước 1: Khởi tạo Cơ sở dữ liệu
Lệnh này sẽ tạo file `iot_security.db` để lưu trữ thông tin thiết bị và nhật ký.
```powershell
python server/init_db.py
```

### Bước 2: Chạy Backend Server
Server sẽ lắng nghe các request JSON tại cổng 5000.
```powershell
python server/app.py
```

### Bước 3: Chạy Dashboard giám sát
Lệnh này sẽ khởi chạy giao diện Web. Bạn có thể xem biểu đồ tại địa chỉ `http://localhost:8501`.
```powershell
streamlit run server/dashboard.py
```

### Bước 4: Thực thi kịch bản mô phỏng tấn công
Chạy script này để gửi dữ liệu giả lập và các kịch bản tấn công (Sai HMAC, Replay Attack).
```powershell
python server/main_test.py
```
*Kết quả:* Quan sát Dashboard để thấy các bản tin "An toàn" (màu xanh) và "Cảnh báo bảo mật" (màu đỏ).
