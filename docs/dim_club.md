# BẢNG CHIỀU: DIM_CLUB (THÔNG TIN CÂU LẠC BỘ)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Club` quản lý thông tin hồ sơ của các câu lạc bộ bóng đá chuyên nghiệp, bao gồm tên sân vận động, sức chứa khán đài, danh tính Huấn luyện viên trưởng và quy mô lực lượng cầu thủ.

* **Tên bảng:** `dbo.DIM_Club`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Club_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Club_ID` (Natural Key từ hệ thống Transfermarkt)
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua 2 vai trò khóa ngoại:
  1. `Club_SK` (Câu lạc bộ chủ quản của cầu thủ)
  2. `Opponent_Club_SK` (Câu lạc bộ đối thủ trong trận đấu)

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Club_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Club_ID` | `INT` | `NOT NULL` | Mã định danh câu lạc bộ duy nhất từ Transfermarkt |
| Thuộc tính | `Club_Name` | `NVARCHAR(200)` | `NULL` | Tên chính thức của câu lạc bộ |
| Thuộc tính | `Stadium_Name` | `NVARCHAR(200)` | `NULL` | Tên sân vận động nhà |
| Thuộc tính | `Stadium_Seats` | `INT` | `CHECK (Stadium_Seats BETWEEN 0 AND 150000)` | Sức chứa tối đa khán đài sân vận động |
| Thuộc tính | `Coach_Name` | `NVARCHAR(150)` | `NULL` | Họ tên Huấn luyện viên trưởng đương nhiệm |
| Thuộc tính | `Squad_Size` | `INT` | `CHECK (Squad_Size BETWEEN 10 AND 60)` | Số lượng cầu thủ đăng ký trong đội hình 1 |

---

## 3. ĐỐI CHIẾU & MAPPING VỚI BỘ DỮ LIỆU KAGGLE (TRANSFERMARKT)

* **Tệp CSV nguồn gốc từ Kaggle:** `clubs.csv` (Tổng cộng 17 cột thuộc tính gốc).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### Bảng Ma Trận Ánh Xạ (Mapping Matrix Kaggle $\rightarrow$ DW)

| Tệp CSV Nguồn | Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Quy tắc chuyển đổi ETL & Xử lý dữ liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `clubs.csv` | `club_id` | `Int64` | `Club_ID` | `INT` | Ép kiểu `(DT_I4)` giữ nguyên mã định danh |
| `clubs.csv` | `name` | `string` | `Club_Name` | `NVARCHAR(200)` | Ép kiểu `(DT_WSTR, 200)`, chuẩn hóa tên CLB |
| `clubs.csv` | `stadium_name` | `string` | `Stadium_Name` | `NVARCHAR(200)` | Chuẩn hóa Unicode `(DT_WSTR)`, điền `'Unknown Stadium'` nếu NULL |
| `clubs.csv` | `stadium_seats` | `Int64 / float64` | `Stadium_Seats` | `INT` | Ép kiểu `(DT_I4)`, thay NULL bằng `0` |
| `clubs.csv` | `coach_name` | `string` | `Coach_Name` | `NVARCHAR(150)` | Ép kiểu Unicode `(DT_WSTR, 150)`, thay NULL bằng `'Unknown Coach'` |
| `clubs.csv` | `squad_size` | `Int64` | `Squad_Size` | `INT` | Ép kiểu `(DT_I4)`, kiểm tra phạm vi số lượng cầu thủ |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp dữ liệu đã qua làm sạch `cleaned_clubs.csv` (hoặc `clubs.csv`).
2. **Data Conversion Component:**
   * Ép kiểu các trường văn bản Unicode (`DT_WSTR`): `name` $\rightarrow$ `Club_Name`, `stadium_name` $\rightarrow$ `Stadium_Name`, `coach_name` $\rightarrow$ `Coach_Name`.
   * Ép kiểu các trường số nguyên (`DT_I4`): `club_id`, `stadium_seats`, `squad_size`.
3. **Derived Column Component (Xử lý NULL):**
   * `Stadium_Name`: `ISNULL(stadium_name) ? "Unknown Stadium" : TRIM(stadium_name)`
   * `Coach_Name`: `ISNULL(coach_name) ? "Unknown Coach" : TRIM(coach_name)`
   * `Stadium_Seats`: `ISNULL(stadium_seats) ? 0 : stadium_seats`
4. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Khởi tạo dòng mặc định `Club_SK = -1`, `Club_ID = -1`, `Club_Name = 'Unknown Club'` để phục vụ tra cứu Lookup trong SSIS khi cầu thủ hoặc đối thủ không có mã CLB hợp lệ.
5. **OLE DB Destination:** Đẩy dữ liệu vào bảng `dbo.DIM_Club`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính duy nhất (Uniqueness):** Mỗi `Club_ID` là duy nhất trong `DIM_Club`.
* **Tra cứu Lookup 2 chiều trong Fact:** Bảng `FACT_Player_Match_Perf` thực hiện 2 bước Lookup riêng biệt vào `DIM_Club` để lấy `Club_SK` (Đội nhà/Đội chủ quản) và `Opponent_Club_SK` (Đội đối thủ).
* **Đổi tên CLB & HLV:** Áp dụng mô hình SCD Type 1 cập nhật ghi đè các thông tin đổi tên HLV hoặc tên sân vận động mới nhất.
