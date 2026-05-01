# Hướng dẫn vận hành / Usage Guide

## Tiếng Việt

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

---

## English

Follow this sequence to ensure the system operates correctly:

### Step 1: Initialize Database (First time only)
```powershell
python server/init_db.py
```

### Step 2: Start the Backend Server
Open a new terminal and run:
```powershell
python server/app.py
```

### Step 3: Start the Monitoring Dashboard
Open another terminal and run:
```powershell
streamlit run server/dashboard.py
```

### Step 4: Run Security Tests
Open a final terminal to simulate device data transmissions and security attacks:
```powershell
python server/main_test.py
```
