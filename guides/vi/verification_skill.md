# Phuong phap Kiem dinh va Xac thuc He thong

Tai lieu nay mo ta quy trinh ky thuat de dam bao he thong hoat dong on dinh, an toan va chinh xac truoc khi trien khai thuc te.

## 1. Quy trinh Xac thuc da diem (Multi-point Verification)

### 1.1. Kiem thu don vi (Unit Testing)
- **Muc tieu:** Xac minh tinh dung dan cua tung ham ma hoa va giai ma.
- **Thuc thi:** Kiem tra dau ra cua AES-GCM voi cac chuoi ky tu mau de dam bao trung khop voi ket qua tinh toan ly thuyet.

### 1.2. Kiem thu tich hop (Integration Testing)
- **Muc tieu:** Dam bao su phoi hop nhip nhang giua Node, Gateway va Server.
- **Thuc thi:** Su dung script `main_test.py` de mo phong toan bo luong du lieu tu luc duoc ma hoa tai Node den khi duoc luu tru vao Database tai Server.

### 1.3. Kiem thu an ninh thuc chung (Empirical Security Testing)
- **Muc tieu:** Chung minh kha nang phong thu truoc cac kieu tan cong muc tieu.
- **Kich ban thuc thi:**
    - **Gia mao Gateway:** Sửa doi Gateway ID hoac chu ky HMAC de xac nhan Server tu choi ket noi.
    - **Tan cong phat lai (Replay):** Gui lai goi tin hop le da ghi nhan de xac nhan co che Sequence Number hoat dong.
    - **Sua doi du lieu (Tampering):** Dao bit trong Ciphertext de xac nhan lop AES-GCM phat hien sai lech toan ven (MAC check fail).

## 2. Tieu chuan danh gia Hieu nang
- **Do tre xu ly (Latency):** Do luong thoi gian thuc thi tai Server tu khi nhan du lieu den khi hoan tat giai ma. Muc tieu dat duoi 50ms cho moi ban tin.
- **Tinh on dinh Database:** Kiem tra kha nang ghi du lieu lien tuc va tinh nhat quan cua du lieu Telemetry.

## 3. Quy trinh dọn dep moi truong
Moi lan kiem thu deu phai bat dau tu mot "trang thai sach":
1. Dung cac tien trinh cu dang chiem dung file Database.
2. Dat lai trang thai thiet bi ve `active`.
3. Reset so thu tu `last_seq` ve -1.
