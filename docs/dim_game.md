# BẢNG CHIỀU: DIM_GAME (THÔNG TIN TRẬN ĐẤU)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Game` lưu trữ chi tiết bối cảnh tổ chức trận đấu, bao gồm mùa giải, vòng đấu, mã hai đội bóng đối đầu (Đội nhà vs Đội khách), tỷ số kết quả trận đấu và tên sân vận động diễn ra.

* **Tên bảng:** `dbo.DIM_Game`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Game_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Game_ID` (Natural Key từ hệ thống Transfermarkt)
* **Quy tắc độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`NVARCHAR(100)`** hoặc **`NVARCHAR(200)`** cho 100% các cột chuỗi.
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Game_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Game_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Game_ID` | `INT` | `NOT NULL` | Mã định danh trận đấu duy nhất từ Transfermarkt |
| Thuộc tính | `Round` | `NVARCHAR(100)` | `NULL` | Vòng đấu hoặc giai đoạn thi đấu (*Matchday 1, Quarter-Finals, Final...*) |
| Thuộc tính | `Home_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội chủ nhà |
| Thuộc tính | `Away_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội khách |
| Thuộc tính | `Home_Club_Goals` | `INT` | `CHECK (Home_Club_Goals >= 0)` | Số bàn thắng ghi được của đội chủ nhà |
| Thuộc tính | `Away_Club_Goals` | `INT` | `CHECK (Away_Club_Goals >= 0)` | Số bàn thắng ghi được của đội khách |
| Thuộc tính | `Stadium` | `NVARCHAR(200)` | `NULL` | Tên sân vận động diễn ra trận đấu |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

* **Tệp CSV nguồn gốc từ Kaggle:** `games.csv` (Tổng cộng **23 cột thuộc tính gốc**).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### 3.1. Các cột được giữ lại và chuyển thành thuộc tính DW (Maintained & Mapped)

| Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Đánh giá & Quy tắc chuyển đổi SSIS |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | `Int64` | `Game_ID` | `INT` | **Giữ nguyên:** Mã định danh trận đấu chính xác (BK) |
| `round` | `string` | `Round` | `NVARCHAR(100)` | **Giữ nguyên:** Tên vòng đấu, ép kiểu `[DT_WSTR, 100]` |
| `home_club_id` | `Int64` | `Home_Club_ID` | `INT` | **Giữ nguyên:** Mã CLB chủ nhà |
| `away_club_id` | `Int64` | `Away_Club_ID` | `INT` | **Giữ nguyên:** Mã CLB khách |
| `home_club_goals` | `Int64` | `Home_Club_Goals` | `INT` | **Giữ nguyên:** Tỷ số bàn thắng đội nhà |
| `away_club_goals` | `Int64` | `Away_Club_Goals` | `INT` | **Giữ nguyên:** Tỷ số bàn thắng đội khách |
| `stadium` | `string` | `Stadium` | `NVARCHAR(200)` | **Giữ nguyên:** Tên sân vận động, ép kiểu `[DT_WSTR, 200]` |

### 3.2. Các cột Khóa (Key/FK) trong Kaggle BỊ BỎ QUA trong DIM_Game và lý do (Omitted Keys)

| Cột Khóa nguồn (Kaggle) | Loại Khóa | Lý do bỏ qua không đưa vào `DIM_Game` |
| :--- | :--- | :--- |
| `competition_id` | Foreign Key | **Tách biệt chiều chuẩn Star Schema:** Được đưa thành khóa ngoại `Competition_SK` độc lập trong `FACT_Player_Match_Perf`, tránh liên kết trực tiếp giữa 2 bảng Dim với nhau (`DIM_Game` $\leftrightarrow$ `DIM_Competition`). |
| `date` | Date | **Tách biệt chiều thời gian:** Được chuyển thành khóa ngoại `Time_SK` trong Fact để tham chiếu tới `DIM_Time` tập trung. |

### 3.3. Các cột DƯ THỪA / KHÔNG CẦN THIẾT trong Kaggle (Surplus & Redundant Columns)

| Cột Dư thừa (Kaggle) | Kiểu dữ liệu | Lý do xác định dư thừa & Loại bỏ |
| :--- | :--- | :--- |
| `home_club_name`, `away_club_name` | `string` | **Dư thừa văn bản:** Đã được quản lý tập trung trong bảng `DIM_Club` qua `Club_ID`. |
| `home_club_manager_name`, `away_club_manager_name` | `string` | **Dư thừa HLV:** Đã được lưu trữ trong `DIM_Club.Coach_Name`. |
| `home_club_position`, `away_club_position` | `float64` | **Thứ hạng biến động:** Khuyết nhiều dữ liệu NULL và không thuộc phạm vi bài toán. |
| `home_club_formation`, `away_club_formation` | `string` | **Sơ đồ chiến thuật:** Chứa nhiều dạng chuỗi không chuẩn hóa. |
| `referee` | `string` | **Tên trọng tài:** Không nằm trong phạm vi đo lường hiệu suất thi đấu cầu thủ/CLB. |
| `attendance` | `float64` | **Dữ liệu khuyết:** Bị khuyết giá trị NULL rất lớn trong nguồn Kaggle. |
| `url` | `string` | **Dữ liệu Web:** Link bài viết trận đấu, hoàn toàn dư thừa. |
| `aggregate` | `string` | **Tổng tỷ số 2 lượt trận:** Dư thừa đối với các trận giải VĐQG. |
| `competition_type` | `string` | **Dư thừa:** Đã được lưu trữ trong `DIM_Competition.Competition_Type`. |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp `cleaned_games.csv`.
2. **Data Conversion Component:**
   * Ép kiểu số nguyên (`[DT_I4]`) cho: `game_id`, `home_club_id`, `away_club_id`, `home_club_goals`, `away_club_goals`.
   * Ép kiểu chuỗi ký tự Unicode (`[DT_WSTR]`) chuẩn **100** hoặc **200**:
     * `round` $\rightarrow$ `dc_round` (`[DT_WSTR, 100]`)
     * `stadium` $\rightarrow$ `dc_stadium` (`[DT_WSTR, 200]`)
3. **Derived Column Component:**
   * Thay thế giá trị NULL của `Stadium`: `ISNULL(dc_stadium) || LEN(TRIM(dc_stadium)) == 0 ? "Unknown Stadium" : TRIM(dc_stadium)`
   * Tỷ số mặc định nếu khuyết: `ISNULL(dc_home_club_goals) ? 0 : dc_home_club_goals`
4. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Khởi tạo bản ghi mặc định `Game_SK = -1`, `Game_ID = -1`, `Round = 'Unknown Round'` cho các trường hợp tra cứu Lookup không tìm thấy trận đấu trong Fact.
5. **OLE DB Destination:** Đẩy dữ liệu vào bảng `dbo.DIM_Game`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính duy nhất:** Đảm bảo `Game_ID` không bị lặp lại trong `DIM_Game`.
* **Đồng bộ độ dài 100%:** Toàn bộ kiểu chuỗi ký tự trong SSIS (`[DT_WSTR]`) và SQL Server (`NVARCHAR`) được đồng bộ chuẩn tuyệt đối **100** hoặc **200**, triệt tiêu 100% Warning trong SSIS.
