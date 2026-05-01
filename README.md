# Nghiên cứu và Triển khai Mã hóa Payload cho Hệ thống IoT

## 1. Giới thiệu (Bối cảnh nghiên cứu)
Đồ án tập trung nghiên cứu giải pháp **Mã hóa tầng ứng dụng (Application Layer Encryption)** cho các thiết bị IoT tài nguyên hạn chế (ESP32). Dự án đi sâu vào việc thiết kế và triển khai một giao thức bảo mật nhẹ, tối ưu cho Payload dữ liệu, đảm bảo an toàn từ đầu cuối (End-to-End).

**Trọng tâm nghiên cứu:**
- Nghiên cứu thuật toán mã hóa đối xứng **AES-GCM** và ưu điểm của nó trong việc xác thực dữ liệu (AEAD).
- Thiết kế cơ chế xác thực nguồn gốc và chống giả mạo sử dụng **HMAC-SHA256**.
- Thiết kế giao thức chống tấn công phát lại (Replay Attack) và đảm bảo tính toàn vẹn (Integrity).
- Nghiên cứu cơ chế quản lý và trao đổi khóa an toàn cho thiết bị đầu cuối.

## 2. Phân chia trách nhiệm
- **Phần Nghiên cứu & Phần mềm (Bạn phụ trách):**
    - Thiết kế giao thức bảo mật (Cấu trúc gói tin, quy trình mã hóa/giải mã).
    - Triển khai Backend Server để xử lý các phép tính mật mã phức tạp.
    - Phân tích hiệu năng và độ an toàn của thuật toán.
- **Phần IoT & Hardware (Cộng sự phụ trách):**
    - Triển khai các thư viện mật mã lên phần cứng ESP32 theo thiết kế giao thức.
    - Thu thập dữ liệu cảm biến và thực thi mã hóa phần cứng.

## 3. Giao thức bảo mật đề xuất
Hệ thống sử dụng **AES-128-GCM** kết hợp **HMAC-SHA256**:
- **AES-GCM:** Mã hóa và xác thực dữ liệu giữa Node và Server.
- **HMAC-SHA256:** Xác thực quyền truy cập của Gateway.
- **Nonce/IV:** 12 bytes (Đảm bảo tính duy nhất cho mỗi bản tin).
- **Auth Tag:** 16 bytes (Xác thực dữ liệu và tiêu đề).

## 4. Công nghệ sử dụng
- **Ngôn ngữ:** Python (Phía Server) để thực hiện các phân tích mật mã.
- **Thư viện:** `PyCryptodome` (Python), `mbedtls` (C++ cho ESP32).
- **Mô phỏng:** Công cụ mô phỏng để kiểm tra giao thức trước khi nạp lên phần cứng.
