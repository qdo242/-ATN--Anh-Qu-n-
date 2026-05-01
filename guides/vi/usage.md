# Quy trình Vận hành Hệ thống

Tài liệu này mô tả trình tự các bước thực thi để duy trì tính nhất quán của dữ liệu và các kiểm tra an ninh.

## 1. Khởi tạo Cơ sở dữ liệu
Thực thi script khởi tạo để thiết lập cấu trúc bảng SQLite và các giá trị mặc định cho thiết bị.
```powershell
python server/init_db.py
```

## 2. Triển khai Backend Server
Khởi chạy Flask Server để mở các API endpoint tiếp nhận Payload dưới định dạng JSON.
```powershell
python server/app.py
```

## 3. Khởi chạy Dashboard Giám sát
Sử dụng Streamlit để truy vấn và hiển thị dữ liệu từ cơ sở dữ liệu theo thời gian thực.
```powershell
streamlit run server/dashboard.py
```

## 4. Kiểm thử và Mô phỏng
Thực thi script kiểm thử để đánh giá khả năng phản hồi của hệ thống trước các kịch bản:
- Giao dịch hợp lệ.
- Tấn công mạo danh Gateway (Sai HMAC).
- Tấn công phát lại (Replay Attack).
- Tấn công sửa đổi dữ liệu (Tag mismatch).
```powershell
python server/main_test.py
```
