# Xếp thời khóa biểu bằng CSP - Bản Web (Flask)

Bản web của chương trình demo bài tập lớn môn **Trí tuệ nhân tạo (IT6094)**, đề tài số 40:
*Lập lịch thời khóa biểu bằng bài toán thỏa mãn ràng buộc (CSP)*.
Bản web dùng chung `engine.py` với bản desktop (Tkinter) nên kết quả hai bản giống hệt nhau,
và có thể deploy lên internet (Render, Railway...) để mở bằng trình duyệt ở bất cứ đâu.

Mỗi buổi học là một **biến**, miền giá trị là các cặp **(khung giờ, phòng)** khả thi,
ràng buộc gồm: không trùng giảng viên, không trùng phòng, hai buổi của cùng một lớp không trùng giờ,
phòng đủ sức chứa, giảng viên không bị xếp vào khung giờ bận. Ràng buộc mềm: ưu tiên buổi sáng.

## Thuật toán

1. **Backtracking thuần** - quay lui theo thứ tự cố định.
2. **Backtracking + MRV + Forward Checking** - chọn biến còn ít giá trị nhất (MRV),
   loại sớm giá trị xung đột khỏi miền các biến chưa gán (Forward Checking).
3. **OR-Tools CP-SAT** - bộ giải lập trình ràng buộc của Google, tối ưu trực tiếp điểm ràng buộc mềm.

Thuật toán quay lui có giới hạn an toàn 300.000 nút duyệt: vượt giới hạn chương trình sẽ dừng
và thông báo thay vì treo (minh họa hiện tượng bùng nổ tổ hợp).
Mọi lịch tạo ra đều được hàm kiểm tra độc lập (`kiem_tra` trong `engine.py`) rà soát lại.

## Dữ liệu

- **Bộ 1 - Chuẩn:** 12 lớp, 5 giảng viên, 3 phòng, 24 buổi học.
- **Bộ 2 - Mở rộng:** 16 lớp, 8 giảng viên, 5 phòng, 48 buổi học.

## Chạy trên máy cá nhân

Yêu cầu Python 3.10 trở lên.

```
pip install -r requirements.txt
python app.py
```

Mở trình duyệt tại địa chỉ **http://127.0.0.1:5000** là dùng được.
Máy chủ lắng nghe cổng trong biến môi trường `PORT` nếu có (mặc định 5000).

## Cấu trúc thư mục

| Tệp | Nội dung |
|---|---|
| `app.py` | Máy chủ Flask: trang chủ và các API JSON (xếp lịch, so sánh 3 thuật toán, dữ liệu đầu vào) |
| `engine.py` | Toàn bộ logic CSP dùng chung với bản desktop: dữ liệu, xây dựng biến/miền, bộ giải quay lui + MRV + FC, CP-SAT, kiểm tra hợp lệ |
| `templates/index.html` | Giao diện trang web |
| `static/style.css` | Định dạng giao diện |
| `static/app.js` | Xử lý phía trình duyệt: gọi API, vẽ lưới thời khóa biểu, bảng so sánh, dữ liệu đầu vào |
| `requirements.txt` | Các thư viện cần cài: flask, ortools, gunicorn |
| `render.yaml` | Cấu hình deploy tự động lên Render |

Các đầu API:

| Đường dẫn | Phương thức | Công dụng |
|---|---|---|
| `/` | GET | Trang giao diện |
| `/api/thong-tin` | GET | Danh sách bộ dữ liệu, thuật toán, khung giờ |
| `/api/du-lieu?bo=bo1` | GET | Dữ liệu đầu vào của một bộ (phòng, giảng viên, lớp) |
| `/api/xep-lich` | POST | Xếp lịch với bộ dữ liệu + thuật toán được chọn, thân JSON: `{"bo": "bo1", "thuat_toan": "mrvfc"}` |
| `/api/so-sanh` | POST | Chạy cả 3 thuật toán trên một bộ dữ liệu, thân JSON: `{"bo": "bo1"}` |

## Deploy lên Render (miễn phí)

Cách 1 - dùng sẵn tệp `render.yaml` (Blueprint):

1. Đưa thư mục này lên một kho GitHub (toàn bộ các tệp trong thư mục `web-csp-tkb` nằm ở thư mục gốc của kho).
2. Đăng nhập [render.com](https://render.com), chọn **New +** -> **Blueprint**.
3. Kết nối kho GitHub vừa tạo, Render tự đọc `render.yaml` và tạo dịch vụ web.
4. Bấm **Apply** / **Create** và chờ cài đặt xong (khoảng 2-4 phút), Render cấp một địa chỉ dạng `https://web-csp-tkb.onrender.com`.

Cách 2 - tạo thủ công (không cần `render.yaml`):

1. Đưa thư mục này lên một kho GitHub như trên.
2. Tại Render, chọn **New +** -> **Web Service**, kết nối kho GitHub.
3. Điền các mục: **Runtime**: Python 3; **Build Command**: `pip install -r requirements.txt`;
   **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300`.
4. Bấm **Create Web Service** và chờ deploy xong.

Lưu ý: gói miễn phí của Render sẽ cho máy chủ "ngủ" sau một thời gian không có người truy cập,
lần mở đầu tiên sau khi ngủ cần chờ khoảng 30-60 giây để máy chủ khởi động lại.

## Kết quả thực nghiệm (khớp với bản desktop)

| Bộ dữ liệu | Thuật toán | Nút duyệt | Điểm mềm (buổi sáng) | Kết quả |
|---|---|---|---|---|
| Bộ 1 (24 biến) | Backtracking thuần | 25 | 12/24 | Xếp đủ 24 buổi, kiểm tra đạt |
| Bộ 1 (24 biến) | MRV + Forward Checking | 25 | 14/24 | Xếp đủ 24 buổi, kiểm tra đạt |
| Bộ 1 (24 biến) | CP-SAT | - | **15/24 (tối ưu)** | Xếp đủ 24 buổi, kiểm tra đạt |
| Bộ 2 (48 biến) | Backtracking thuần | > 300.000 (dừng ở giới hạn) | - | Chưa có nghiệm |
| Bộ 2 (48 biến) | MRV + Forward Checking | 49 | 25/48 | Xếp đủ 48 buổi, kiểm tra đạt |
| Bộ 2 (48 biến) | CP-SAT | - | **25/48 (tối ưu)** | Xếp đủ 48 buổi, kiểm tra đạt |
