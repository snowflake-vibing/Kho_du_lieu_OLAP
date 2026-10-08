# BẢNG CHIỀU: DIM_PLAYER (THÔNG TIN CẦU THỦ)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Player` đóng vai trò là bảng chiều (Dimension Table) lưu trữ toàn bộ thông tin tiểu sử, nhân trắc học và vị trí thi đấu chuyên môn của cầu thủ bóng đá. 

* **Tên bảng:** `dbo.DIM_Player`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Player_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Player_ID` (Natural Key từ hệ thống Transfermarkt)
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Player_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Player_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Player_ID` | `INT` | `NOT NULL` | Mã định danh cầu thủ duy nhất từ nguồn Transfermarkt |
| Thuộc tính | `Player_Name` | `NVARCHAR(200)` | `NULL` | Họ và tên đầy đủ của cầu thủ |
| Thuộc tính | `Date_Of_Birth` | `NVARCHAR(50)` | `NULL` | Ngày tháng năm sinh (Định dạng chuẩn `YYYY-MM-DD`) |
| Thuộc tính | `Age` | `INT` | `CHECK (Age BETWEEN 15 AND 50)` | Tuổi thực tế của cầu thủ tại thời điểm thu thập dữ liệu |
| Thuộc tính | `Country_Of_Citizenship` | `NVARCHAR(150)` | `NULL` | Quốc tịch chính thức đăng ký thi đấu |
| Thuộc tính | `Main_Position` | `NVARCHAR(50)` | `NULL` | Vị trí thi đấu tổng quát (*Goalkeeper, Defender, Midfield, Attack*) |
| Thuộc tính | `Sub_Position` | `NVARCHAR(100)` | `NULL` | Vị trí chi tiết (*Centre-Back, Right Winger, Centre-Forward...*) |
| Thuộc tính | `Foot` | `NVARCHAR(20)` | `NULL` | Chân thuận (*Left, Right, Both*) |
| Thuộc tính | `Height_In_Cm` | `INT` | `CHECK (Height_In_Cm BETWEEN 150 AND 220)` | Chiều cao thực tế tính bằng centimet |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

* **Tệp CSV nguồn gốc từ Kaggle:** `players.csv` (Tổng cộng **26 cột thuộc tính gốc**).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### 3.1. Các cột được giữ lại và chuyển thành thuộc tính DW (Maintained & Mapped)

| Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Đánh giá & Quy tắc chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `player_id` | `Int64` | `Player_ID` | `INT` | **Giữ nguyên:** Làm khóa nghiệp vụ (BK) chính xác 100% |
| `name` | `string` | `Player_Name` | `NVARCHAR(200)` | **Giữ nguyên:** Đã gộp chuẩn họ tên đầy đủ, ép kiểu Unicode UTF-8 |
| `date_of_birth` | `string` | `Date_Of_Birth` | `NVARCHAR(50)` | **Giữ nguyên:** Chuẩn hóa ngày dạng `YYYY-MM-DD` |
| Calculated | - | `Age` | `INT` | **Thêm mới:** Tính tuổi `DATEDIFF(YEAR, date_of_birth, GETDATE())` phục vụ phân tích lứa tuổi |
| `country_of_citizenship` | `string` | `Country_Of_Citizenship` | `NVARCHAR(150)` | **Giữ nguyên:** Quốc tịch chính thức dùng trong các bài toán so sánh nội/ngoại binh |
| `position` | `string` | `Main_Position` | `NVARCHAR(50)` | **Giữ nguyên:** Chuẩn hóa thành 4 nhóm chính (*Goalkeeper, Defender, Midfield, Attack*) |
| `sub_position` | `string` | `Sub_Position` | `NVARCHAR(100)` | **Giữ nguyên:** Vị trí thi đấu chi tiết |
| `foot` | `string` | `Foot` | `NVARCHAR(20)` | **Giữ nguyên:** Chân thuận (*Left, Right, Both*) |
| `height_in_cm` | `float64` | `Height_In_Cm` | `INT` | **Giữ nguyên:** Chiều cao tính bằng cm |

### 3.2. Các cột Khóa (Key/FK) trong Kaggle BỊ BỎ QUA trong DIM_Player và lý do (Omitted Keys)

| Cột Khóa nguồn (Kaggle) | Loại Khóa | Lý do bỏ qua không đưa vào `DIM_Player` |
| :--- | :--- | :--- |
| `current_club_id` | Foreign Key | **Lý do thiết kế OLAP:** Mã CLB hiện tại của cầu thủ. Không đưa vào `DIM_Player` vì trong Star Schema, mối liên kết Cầu thủ - CLB biến động theo thời gian/trận đấu và được lưu vết động trong `FACT_Player_Match_Perf` qua `Club_SK`. Việc cố định `current_club_id` trong DIM sẽ làm sai lệch thông tin lịch sử khi cầu thủ chuyển nhượng. |
| `current_national_team_id` | Foreign Key | **Lý do phạm vi:** Mã đội tuyển quốc gia hiện tại. Phạm vi đồ án tập trung vào các giải VĐQG và Cúp CLB Châu Âu, không phân tích giải cấp ĐTQG. |
| `current_club_domestic_competition_id` | Foreign Key | **Dư thừa tham chiếu:** Mã giải đấu của CLB hiện tại. Đã được quản lý thông qua liên kết `Club_SK` $\rightarrow$ `Competition_SK` trong Fact. |

### 3.3. Các cột DƯ THỪA / KHÔNG CẦN THIẾT trong Kaggle (Surplus & Redundant Columns)

| Cột Dư thừa (Kaggle) | Kiểu dữ liệu | Lý do xác định dư thừa & Loại bỏ |
| :--- | :--- | :--- |
| `first_name`, `last_name` | `string` | **Tách biệt dư thừa:** Đã có cột `name` lưu trữ tên đầy đủ chuẩn hóa. |
| `player_code` | `string` | **Chuỗi định danh dư thừa:** Đoạn mã chuỗi của web Transfermarkt (VD: `cristiano-ronaldo`), dư thừa vì đã có `player_id` làm số nguyên chuẩn. |
| `image_url`, `url` | `string` | **Dữ liệu giao diện Web:** Đường dẫn ảnh và URL bài viết, hoàn toàn không có giá trị tính toán phân tích OLAP. |
| `agent_name` | `string` | **Thông tin ngoài phạm vi:** Tên người đại diện/công ty quản lý, không phục vụ phân tích hiệu suất chuyên môn trên sân. |
| `country_of_birth`, `city_of_birth` | `string` | **Dữ liệu tiểu sử phụ:** Nơi sinh và thành phố sinh không quan trọng bằng `country_of_citizenship` (quốc tịch thi đấu chính thức). |
| `contract_expiration_date` | `string` | **Thông tin biến động ngắn hạn:** Ngày hết hạn hợp đồng, không thuộc phạm vi đo lường năng suất thi đấu. |
| `last_season` | `Int64` | **Thông tin hệ thống nguồn:** Mùa giải gần nhất cập nhật trong Kaggle, không có giá trị đa chiều. |
| `international_caps`, `international_goals` | `Int64` | **Nằm ngoài phạm vi:** Thống kê số trận/bàn thắng cho ĐTQG, không phản ánh diễn biến từng trận đấu giải CLB. |
| `market_value_in_eur`, `highest_market_value_in_eur` | `float64` | **Chuyển đổi vị trí lưu trữ:** Giá trị thị trường biến động theo mốc thời gian, đã được chuyển sang bảng Fact (`FACT_Player_Match_Perf.Market_Value_In_EUR`) hoặc tra cứu theo mốc thời gian thay vì lưu tĩnh trong DIM. |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp dữ liệu đã qua tiền xử lý `cleaned_players.csv` (hoặc `players.csv`).
2. **Data Conversion Component:**
   * Ép kiểu chuỗi ký tự UTF-8 sang Unicode (`DT_WSTR`) cho các trường văn bản (`name`, `country_of_citizenship`, `position`, `sub_position`, `foot`).
   * Ép kiểu số nguyên (`DT_I4`) cho `player_id`, `height_in_cm`, `age`.
3. **Derived Column Component (Xử lý NULL & Gán mặc định):**
   * Trường hợp `Player_Name` bị NULL: `ISNULL(name) ? "Unknown Player" : TRIM(name)`
   * Trường hợp `Foot` bị NULL: `ISNULL(foot) ? "Unknown" : foot`
   * Trường hợp `Height_In_Cm` ngoài khoảng `[150, 220]`: gán giá trị mặc định `175`.
4. **Bản ghi đặc biệt (Unknown Record Key = -1):**
   * Trong bước khởi tạo Database, chèn 1 dòng mặc định với `Player_SK = -1` (`Player_ID = -1`, `Player_Name = 'Unknown Player'`) để phục vụ các lượt ra sân không tra cứu được mã cầu thủ trong bảng Fact.
5. **OLE DB Destination:** Đẩy dữ liệu sạch vào bảng `dbo.DIM_Player`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Khử trùng lặp (Deduplication):** Đảm bảo mỗi `Player_ID` chỉ xuất hiện duy nhất 1 lần trong `DIM_Player`.
* **Kiểm tra tham chiếu FK:** 100% mã `Player_SK` xuất hiện trong `FACT_Player_Match_Perf` đều tham chiếu hợp lệ tới `DIM_Player` (nếu không khớp sẽ gán về `-1`).
* **Độ chính xác thuộc tính:** Đã đối chiếu các vị trí chính (`position`) và phụ (`sub_position`) khớp với phân loại tiêu chuẩn trên Kaggle Transfermarkt.
