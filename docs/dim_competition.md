# BẢNG CHIỀU: DIM_COMPETITION (THÔNG TIN GIẢI ĐẤU)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Competition` phân loại các giải đấu bóng đá chuyên nghiệp trên toàn thế giới, phân biệt giữa các giải Vô địch Quốc gia (`domestic_league`) và các Cúp Châu Âu / Cúp Quốc gia (`international_cup`).

* **Tên bảng:** `dbo.DIM_Competition`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Competition_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Competition_ID` (Mã giải đấu chuỗi ký tự như `GB1`, `ES1`, `CL`...)
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Competition_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Competition_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Competition_ID` | `NVARCHAR(50)` | `NOT NULL` | Mã ngắn giải đấu (VD: `'GB1'` - Premier League, `'ES1'` - La Liga) |
| Thuộc tính | `Competition_Name` | `NVARCHAR(200)` | `NULL` | Tên thương hiệu chính thức của giải đấu |
| Thuộc tính | `Country_Name` | `NVARCHAR(200)` | `NULL` | Quốc gia hoặc khu vực địa lý đăng cai giải đấu |
| Thuộc tính | `Competition_Type` | `NVARCHAR(100)` | `NULL` | Phân loại giải đấu (*domestic_league, international_cup*) |

---

## 3. ĐỐI CHIẾU & MAPPING VỚI BỘ DỮ LIỆU KAGGLE (TRANSFERMARKT)

* **Tệp CSV nguồn gốc từ Kaggle:** `competitions.csv` (Tổng cộng 11 cột thuộc tính gốc).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### Bảng Ma Trận Ánh Xạ (Mapping Matrix Kaggle $\rightarrow$ DW)

| Tệp CSV Nguồn | Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Quy tắc chuyển đổi ETL & Xử lý dữ liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `competitions.csv` | `competition_id` | `string` | `Competition_ID` | `NVARCHAR(50)` | Ép kiểu `(DT_WSTR, 50)`, giữ nguyên mã ký tự nguồn |
| `competitions.csv` | `name` | `string` | `Competition_Name` | `NVARCHAR(200)` | Chuẩn hóa Unicode UTF-8 (`DT_WSTR`), loại bỏ khoảng trắng thừa |
| `competitions.csv` | `country_name` | `string` | `Country_Name` | `NVARCHAR(200)` | Chuẩn hóa tên quốc gia đăng cai (`England`, `Spain`, `Germany`...) |
| `competitions.csv` | `type` | `string` | `Competition_Type` | `NVARCHAR(100)` | Chuẩn hóa phân loại giải đấu (`domestic_league`, `domestic_cup`, `international_cup`) |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp `cleaned_competitions.csv` (hoặc `competitions.csv`).
2. **Data Conversion Component:**
   * Ép kiểu chuỗi ký tự Unicode (`DT_WSTR`) cho tất cả thuộc tính: `competition_id`, `name`, `country_name`, `type`.
3. **Derived Column Component:**
   * Xử lý khoảng trắng: `TRIM(name)`
   * Xử lý trường hợp `Country_Name` rỗng hoặc dành cho cúp liên quốc gia (VD: UEFA Champions League): gán `'Europe'` hoặc `'International'`.
4. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Chèn bản ghi mặc định `Competition_SK = -1`, `Competition_ID = 'UNKNOWN'`, `Competition_Name = 'Unknown Competition'` để phục vụ trích xuất Lookup Fact.
5. **OLE DB Destination:** Đẩy dữ liệu vào bảng `dbo.DIM_Competition`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính nhất quán mã giải đấu:** Mã `Competition_ID` ngắn gọn giúp tối ưu hóa tra cứu Lookup trong SSIS ETL.
* **Toàn vẹn tham chiếu:** Đảm bảo mọi mã giải đấu xuất hiện trong `appearances.csv` và `games.csv` đều tồn tại trong `DIM_Competition`.
