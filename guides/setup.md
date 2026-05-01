# Cài đặt hệ thống / System Setup

## Tiếng Việt

### 1. Yêu cầu hệ thống
- Python phiên bản 3.9 trở lên.
- Trình quản lý gói pip.

### 2. Cài đặt thư viện
Chạy lệnh sau trong cửa sổ dòng lệnh để cài đặt các thành phần cần thiết:
```powershell
pip install pycryptodomex flask streamlit pandas plotly requests python-dotenv
```

### 3. Cấu hình tệp bảo mật (.env)
Tệp `.env` chứa các khóa bí mật không được đẩy lên GitHub để đảm bảo an toàn. Bạn cần tạo một tệp mới tên là `.env` tại thư mục gốc của dự án với nội dung:
```text
NODE_KEY=1234567890123456
GATEWAY_KEY=gateway_secret_k
```

---

## English

### 1. System Requirements
- Python version 3.9 or higher.
- pip package manager.

### 2. Library Installation
Run the following command in your terminal to install the required dependencies:
```powershell
pip install pycryptodomex flask streamlit pandas plotly requests python-dotenv
```

### 3. Security Configuration (.env)
The `.env` file containing secret keys is excluded from GitHub for security reasons. You must create a new file named `.env` in the project root directory with the following content:
```text
NODE_KEY=1234567890123456
GATEWAY_KEY=gateway_secret_k
```
