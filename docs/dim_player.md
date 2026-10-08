# BẢNG CHIỀU: DIM_PLAYER (THÔNG TIN CẦU THỦ)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Player` đóng vai trò là bảng chiều (Dimension Table) lưu trữ toàn bộ thông tin tiểu sử, nhân trắc học và vị trí thi đấu chuyên môn của cầu thủ bóng đá. 

* **Tên bảng:** `dbo.DIM_Player`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Player_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Player_ID` (Natural Key từ hệ thống Transfermarkt)
* **Quy tắc độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`NVARCHAR(100)`** hoặc **`NVARCHAR(200)`** cho 100% các cột chuỗi.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Player_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Player_ID` | `INT` | `NOT NULL` | Mã định danh cầu thủ duy nhất từ nguồn Transfermarkt |
| Thuộc tính | `Player_Name` | `NVARCHAR(200)` | `NULL` | Họ và tên đầy đủ của cầu thủ |
| Thuộc tính | `Date_Of_Birth` | `NVARCHAR(100)` | `NULL` | Ngày tháng năm sinh (Định dạng chuẩn `YYYY-MM-DD`) |
| Thuộc tính | `Age` | `INT` | `CHECK (Age BETWEEN 15 AND 50)` | Tuổi thực tế của cầu thủ tại thời điểm thu thập dữ liệu |
| Thuộc tính | `Country_Of_Citizenship` | `NVARCHAR(200)` | `NULL` | Quốc tịch chính thức đăng ký thi đấu |
| Thuộc tính | `Main_Position` | `NVARCHAR(100)` | `NULL` | Vị trí thi đấu tổng quát (*Goalkeeper, Defender, Midfield, Attack*) |
| Thuộc tính | `Sub_Position` | `NVARCHAR(100)` | `NULL` | Vị trí chi tiết (*Centre-Back, Right Winger, Centre-Forward...*) |
| Thuộc tính | `Foot` | `NVARCHAR(100)` | `NULL` | Chân thuận (*Left, Right, Both*) |
| Thuộc tính | `Height_In_Cm` | `INT` | `CHECK (Height_In_Cm BETWEEN 150 AND 220)` | Chiều cao thực tế tính bằng centimet |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

* **Tệp CSV nguồn gốc từ Kaggle:** `players.csv` (Tổng cộng **26 cột thuộc tính gốc**).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### 3.1. Các cột được giữ lại và chuyển thành thuộc tính DW (Maintained & Mapped)

| Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Đánh giá & Quy tắc chuyển đổi SSIS |
| :--- | :--- | :--- | :--- | :--- |
| `player_id` | `Int64` | `Player_ID` | `INT` | **Giữ nguyên:** Mã định danh cầu thủ (BK) |
| `name` | `string` | `Player_Name` | `NVARCHAR(200)` | **Giữ nguyên:** Họ tên đầy đủ, ép kiểu `[DT_WSTR, 200]` |
| `date_of_birth` | `string` | `Date_Of_Birth` | `NVARCHAR(100)` | **Giữ nguyên:** Định dạng `YYYY-MM-DD`, ép kiểu `[DT_WSTR, 100]` |
| Calculated | - | `Age` | `INT` | **Thêm mới:** Tính tuổi `DATEDIFF(YEAR, date_of_birth, GETDATE())` |
| `country_of_citizenship` | `string` | `Country_Of_Citizenship` | `NVARCHAR(200)` | **Giữ nguyên:** Quốc tịch thi đấu, ép kiểu `[DT_WSTR, 200]` |
| `position` | `string` | `Main_Position` | `NVARCHAR(100)` | **Giữ nguyên:** 4 nhóm chính, ép kiểu `[DT_WSTR, 100]` |
| `sub_position` | `string` | `Sub_Position` | `NVARCHAR(100)` | **Giữ nguyên:** Vị trí chi tiết, ép kiểu `[DT_WSTR, 100]` |
| `foot` | `string` | `Foot` | `NVARCHAR(100)` | **Giữ nguyên:** Chân thuận, ép kiểu `[DT_WSTR, 100]` |
| `height_in_cm` | `float64` | `Height_In_Cm` | `INT` | **Giữ nguyên:** Chiều cao (cm), ép kiểu `[DT_I4]` |

### 3.2. Các cột Khóa (Key/FK) trong Kaggle BỊ BỎ QUA trong DIM_Player và lý do (Omitted Keys)

| Cột Khóa nguồn (Kaggle) | Loại Khóa | Lý do bỏ qua không đưa vào `DIM_Player` |
| :--- | :--- | :--- |
| `current_club_id` | Foreign Key | **Lý do thiết kế OLAP:** Mã CLB hiện tại. Trong Star Schema, mối liên kết Cầu thủ - CLB biến động theo từng trận đấu và được lưu vết động trong `FACT_Player_Match_Perf.Club_SK`. Việc cố định `current_club_id` trong DIM sẽ làm sai lệch lịch sử khi cầu thủ chuyển nhượng. |
| `current_national_team_id` | Foreign Key | **Lý do phạm vi:** Mã đội tuyển quốc gia. Đồ án tập trung vào giải VĐQG và Cúp CLB Châu Âu. |
| `current_club_domestic_competition_id` | Foreign Key | **Dư thừa tham chiếu:** Đã được quản lý thông qua liên kết `Club_SK` $\rightarrow$ `Competition_SK` trong Fact. |

### 3.3. Các cột DƯ THỪA / KHÔNG CẦN THIẾT trong Kaggle (Surplus & Redundant Columns)

| Cột Dư thừa (Kaggle) | Kiểu dữ liệu | Lý do xác định dư thừa & Loại bỏ |
| :--- | :--- | :--- |
| `first_name`, `last_name` | `string` | **Tách biệt dư thừa:** Đã có cột `name` lưu trữ tên đầy đủ chuẩn hóa. |
| `player_code` | `string` | **Chuỗi dư thừa:** Mã web Transfermarkt, dư thừa vì đã có `player_id` làm số nguyên. |
| `image_url`, `url` | `string` | **Dữ liệu Web UI:** Đường dẫn ảnh và URL, không có giá trị tính toán OLAP. |
| `agent_name` | `string` | **Thông tin ngoài phạm vi:** Tên người đại diện, không phục vụ phân tích chuyên môn. |
| `country_of_birth`, `city_of_birth` | `string` | **Dữ liệu phụ:** Nơi sinh không quan trọng bằng `country_of_citizenship`. |
| `contract_expiration_date` | `string` | **Thông tin biến động ngắn hạn:** Ngày hết hạn hợp đồng. |
| `last_season` | `Int64` | **Thông tin hệ thống nguồn:** Mùa giải gần nhất cập nhật. |
| `international_caps`, `international_goals` | `Int64` | **Nằm ngoài phạm vi:** Số trận/bàn thắng cấp ĐTQG. |
| `market_value_in_eur`, `highest_market_value_in_eur` | `float64` | **Loại bỏ theo yêu cầu:** Định giá thị trường biến động theo thời gian, được loại bỏ để tập trung vào hiệu suất thi đấu chuyên môn. |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp `cleaned_players.csv`.
2. **Data Conversion Component:**
   * Ép kiểu chuỗi ký tự UTF-8 sang Unicode (`[DT_WSTR]`, độ dài **100** hoặc **200**):
     * `name` $\rightarrow$ `dc_player_name` (`[DT_WSTR, 200]`)
     * `date_of_birth` $\rightarrow$ `dc_date_of_birth` (`[DT_WSTR, 100]`)
     * `country_of_citizenship` $\rightarrow$ `dc_country` (`[DT_WSTR, 200]`)
     * `position` $\rightarrow$ `dc_main_position` (`[DT_WSTR, 100]`)
     * `sub_position` $\rightarrow$ `dc_sub_position` (`[DT_WSTR, 100]`)
     * `foot` $\rightarrow$ `dc_foot` (`[DT_WSTR, 100]`)
   * Ép kiểu số nguyên (`[DT_I4]`) cho `player_id`, `height_in_cm`.
3. **Derived Column Component (Xử lý NULL & Gán mặc định):**
   * `der_age`: `ISNULL(dc_date_of_birth) ? 25 : DATEDIFF("yy", (DT_DBTIMESTAMP)dc_date_of_birth, GETDATE())`
   * `der_player_name`: `ISNULL(dc_player_name) || LEN(TRIM(dc_player_name)) == 0 ? "Unknown Player" : TRIM(dc_player_name)`
   * `der_country`: `ISNULL(dc_country) || LEN(TRIM(dc_country)) == 0 ? "Unknown" : TRIM(dc_country)`
   * `der_foot`: `ISNULL(dc_foot) || LEN(TRIM(dc_foot)) == 0 ? "Unknown" : TRIM(dc_foot)`
   * `der_height`: `ISNULL(dc_height_in_cm) || dc_height_in_cm < 150 || dc_height_in_cm > 220 ? 175 : dc_height_in_cm`
4. **Bản ghi đặc biệt (Unknown Record Key = -1):**
   * Khởi tạo dòng mặc định `Player_SK = -1`, `Player_ID = -1`, `Player_Name = 'Unknown Player'` để phục vụ tra cứu Lookup trong Fact.
5. **OLE DB Destination:** Đẩy dữ liệu sạch vào bảng `dbo.DIM_Player`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Khử trùng lặp (Deduplication):** Đảm bảo mỗi `Player_ID` chỉ xuất hiện duy nhất 1 lần trong `DIM_Player`.
* **Kiểm tra tham chiếu FK:** 100% mã `Player_SK` xuất hiện trong `FACT_Player_Match_Perf` đều tham chiếu hợp lệ tới `DIM_Player` (nếu không khớp sẽ gán về `-1`).
* **Đồng bộ độ dài 100%:** Toàn bộ kiểu chuỗi ký tự trong SSIS (`[DT_WSTR]`) và SQL Server (`NVARCHAR`) được đồng bộ chuẩn tuyệt đối **100** hoặc **200**, triệt tiêu 100% Warning trong SSIS.
