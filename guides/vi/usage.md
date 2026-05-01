# Hướng dẫn vận hành

Thứ tự khởi chạy hệ thống để đảm bảo dữ liệu được ghi nhận chính xác:

### Bước 1: Khởi tạo cơ sở dữ liệu (Chỉ làm lần đầu)
```powershell
python server/init_db.py
```

### Bước 2: Khởi chạy Máy chủ (Backend Server)
Mở một cửa sổ dòng lệnh mới và chạy:
```powershell
python server/app.py
```

### Bước 3: Khởi chạy Giao diện giám sát (Dashboard)
Mở một cửa sổ dòng lệnh khác và chạy:
```powershell
streamlit run server/dashboard.py
```

### Bước 4: Chạy kịch bản kiểm thử
Mở cửa sổ dòng lệnh cuối cùng để giả lập các thiết bị gửi dữ liệu và tấn công:
```powershell
python server/main_test.py
```
