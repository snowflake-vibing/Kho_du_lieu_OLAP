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

## 3. ĐỐI CHIẾU & MAPPING VỚI BỘ DỮ LIỆU KAGGLE (TRANSFERMARKT)

* **Tệp CSV nguồn gốc từ Kaggle:** `players.csv` (Tổng cộng 26 cột thuộc tính gốc).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### Bảng Ma Trận Ánh Xạ (Mapping Matrix Kaggle $\rightarrow$ DW)

| Tệp CSV Nguồn | Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Quy tắc chuyển đổi ETL & Xử lý dữ liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `players.csv` | `player_id` | `Int64` | `Player_ID` | `INT` | Ép kiểu `(DT_I4)` dữ liệu nguyên vẹn |
| `players.csv` | `name` | `string` | `Player_Name` | `NVARCHAR(200)` | Chuẩn hóa Unicode UTF-8 (`DT_WSTR`), loại bỏ khoảng trắng thừa |
| `players.csv` | `date_of_birth` | `string (YYYY-MM-DD)` | `Date_Of_Birth` | `NVARCHAR(50)` | Ép định dạng ngày `YYYY-MM-DD`, điền `'1900-01-01'` nếu NULL |
| `players.csv` | Calculated / `date_of_birth` | `string` | `Age` | `INT` | Tính toán: `DATEDIFF(YEAR, date_of_birth, GETDATE())` hoặc giữ nguyên từ Kaggle |
| `players.csv` | `country_of_citizenship` | `string` | `Country_Of_Citizenship` | `NVARCHAR(150)` | Ép kiểu Unicode `(DT_WSTR, 150)`, thay NULL bằng `'Unknown'` |
| `players.csv` | `position` | `string` | `Main_Position` | `NVARCHAR(50)` | Gộp nhóm danh mục: *Goalkeeper, Defender, Midfield, Attack* |
| `players.csv` | `sub_position` | `string` | `Sub_Position` | `NVARCHAR(100)` | Chuẩn hóa chuỗi văn bản vị trí chi tiết |
| `players.csv` | `foot` | `string` | `Foot` | `NVARCHAR(20)` | Chuẩn hóa văn bản: *Left, Right, Both*. Thay NULL bằng `'Unknown'` |
| `players.csv` | `height_in_cm` | `float64 / Int64` | `Height_In_Cm` | `INT` | Ép kiểu số nguyên `(DT_I4)`, điền giá trị trung bình hoặc `0` nếu NULL |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp dữ liệu đã qua tiền xử lý `cleaned_players.csv` (hoặc `players.csv`).
2. **Data Conversion Component:**
   * Ép kiểu chuỗi ký tự UTF-8 sang Unicode (`DT_WSTR`) cho các trường tiếng Việt / ký tự đặc biệt (`name`, `country_of_citizenship`, `position`, `sub_position`, `foot`).
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
