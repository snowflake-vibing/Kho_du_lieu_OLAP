# BẢNG CHIỀU: DIM_COMPETITION (THÔNG TIN GIẢI ĐẤU)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Competition` phân loại các giải đấu bóng đá chuyên nghiệp trên toàn thế giới, phân biệt giữa các giải Vô địch Quốc gia (`domestic_league`) và các Cúp Châu Âu / Cúp Quốc gia (`international_cup`).

* **Tên bảng:** `dbo.DIM_Competition`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Competition_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Competition_ID` (Mã giải đấu chuỗi ký tự như `GB1`, `ES1`, `CL`...)
* **Quy tắc độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`NVARCHAR(100)`** hoặc **`NVARCHAR(200)`** cho 100% các cột chuỗi.
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Competition_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Competition_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Competition_ID` | `NVARCHAR(100)` | `NOT NULL` | Mã ngắn giải đấu (VD: `'GB1'` - Premier League, `'ES1'` - La Liga) |
| Thuộc tính | `Competition_Name` | `NVARCHAR(200)` | `NULL` | Tên thương hiệu chính thức của giải đấu |
| Thuộc tính | `Country_Name` | `NVARCHAR(200)` | `NULL` | Quốc gia hoặc khu vực địa lý đăng cai giải đấu |
| Thuộc tính | `Competition_Type` | `NVARCHAR(100)` | `NULL` | Phân loại giải đấu (*domestic_league, international_cup*) |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

* **Tệp CSV nguồn gốc từ Kaggle:** `competitions.csv` (Tổng cộng **11 cột thuộc tính gốc**).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### 3.1. Các cột được giữ lại và chuyển thành thuộc tính DW (Maintained & Mapped)

| Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Đánh giá & Quy tắc chuyển đổi SSIS |
| :--- | :--- | :--- | :--- | :--- |
| `competition_id` | `string` | `Competition_ID` | `NVARCHAR(100)` | **Giữ nguyên:** Mã ký tự giải đấu (BK), ép kiểu `[DT_WSTR, 100]` |
| `name` | `string` | `Competition_Name` | `NVARCHAR(200)` | **Giữ nguyên:** Tên thương hiệu giải đấu, ép kiểu `[DT_WSTR, 200]` |
| `country_name` | `string` | `Country_Name` | `NVARCHAR(200)` | **Giữ nguyên:** Tên quốc gia đăng cai, ép kiểu `[DT_WSTR, 200]` |
| `type` | `string` | `Competition_Type` | `NVARCHAR(100)` | **Giữ nguyên:** Phân loại giải đấu, ép kiểu `[DT_WSTR, 100]` |

### 3.2. Các cột Khóa (Key/FK) trong Kaggle BỊ BỎ QUA trong DIM_Competition và lý do (Omitted Keys)

| Cột Khóa nguồn (Kaggle) | Loại Khóa | Lý do bỏ qua không đưa vào `DIM_Competition` |
| :--- | :--- | :--- |
| `country_id` | Foreign Key | **Dư thừa phân cấp:** Được bỏ qua vì DW dùng trực tiếp tên quốc gia `Country_Name` làm thuộc tính phân tích rõ ràng, không cần tách thành bảng chiều quốc gia riêng (tránh Snowflaking). |
| `domestic_league_code` | Foreign Key | **Trùng lặp tham chiếu:** Đã được thay thế hoàn toàn bằng thuộc tính `Competition_Type`. |

### 3.3. Các cột DƯ THỪA / KHÔNG CẦN THIẾT trong Kaggle (Surplus & Redundant Columns)

| Cột Dư thừa (Kaggle) | Kiểu dữ liệu | Lý do xác định dư thừa & Loại bỏ |
| :--- | :--- | :--- |
| `competition_code` | `string` | **Chuỗi dư thừa:** Dư thừa vì đã có `competition_id` làm khóa nghiệp vụ chuẩn gọn (`GB1`). |
| `sub_type` | `string` | **Phân loại phụ dư thừa:** Đã được chuẩn hóa về 2 dạng `domestic_league` và `international_cup`. |
| `confederation` | `string` | **Thông tin liên đoàn:** Tên liên đoàn châu lục (UEFA, CONMEBOL...). |
| `is_major_national_league` | `Int64` | **Cờ đánh dấu phụ:** Dư thừa vì có thể phân loại dễ dàng bằng `Competition_ID`. |
| `url` | `string` | **Dữ liệu giao diện Web:** Đường dẫn bài viết. |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp `cleaned_competitions.csv`.
2. **Data Conversion Component:**
   * Ép kiểu chuỗi ký tự Unicode (`[DT_WSTR]`) chuẩn **100** hoặc **200**:
     * `competition_id` $\rightarrow$ `dc_competition_id` (`[DT_WSTR, 100]`)
     * `name` $\rightarrow$ `dc_name` (`[DT_WSTR, 200]`)
     * `country_name` $\rightarrow$ `dc_country_name` (`[DT_WSTR, 200]`)
     * `type` $\rightarrow$ `dc_type` (`[DT_WSTR, 100]`)
3. **Derived Column Component:**
   * Xử lý khoảng trắng: `TRIM(name)`
   * Xử lý trường hợp `Country_Name` rỗng hoặc dành cho cúp liên quốc gia (VD: UEFA Champions League): gán `'Europe'` hoặc `'International'`.
4. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Chèn bản ghi mặc định `Competition_SK = -1`, `Competition_ID = 'UNKNOWN'`, `Competition_Name = 'Unknown Competition'` để phục vụ trích xuất Lookup Fact.
5. **OLE DB Destination:** Đẩy dữ liệu vào bảng `dbo.DIM_Competition`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính nhất quán mã giải đấu:** Mã `Competition_ID` ngắn gọn giúp tối ưu hóa tra cứu Lookup trong SSIS ETL.
* **Đồng bộ độ dài 100%:** Toàn bộ kiểu chuỗi ký tự trong SSIS (`[DT_WSTR]`) và SQL Server (`NVARCHAR`) được đồng bộ chuẩn tuyệt đối **100** hoặc **200**, triệt tiêu 100% Warning trong SSIS.
