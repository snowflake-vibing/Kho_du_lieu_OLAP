# BẢNG CHIỀU: DIM_GAME (THÔNG TIN TRẬN ĐẤU)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Game` lưu trữ chi tiết bối cảnh tổ chức trận đấu, bao gồm mùa giải, vòng đấu, mã hai đội bóng đối đầu (Đội nhà vs Đội khách), tỷ số kết quả trận đấu và tên sân vận động diễn ra.

* **Tên bảng:** `dbo.DIM_Game`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Game_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Game_ID` (Natural Key từ hệ thống Transfermarkt)
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Game_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Game_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Game_ID` | `INT` | `NOT NULL` | Mã định danh trận đấu duy nhất từ Transfermarkt |
| Thuộc tính | `Season` | `INT` | `CHECK (Season BETWEEN 2000 AND 2030)` | Mùa giải bóng đá (*2022, 2023, 2024*) |
| Thuộc tính | `Round` | `NVARCHAR(100)` | `NULL` | Vòng đấu hoặc giai đoạn thi đấu (*Matchday 1, Quarter-Finals, Final...*) |
| Thuộc tính | `Home_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội chủ nhà |
| Thuộc tính | `Away_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội khách |
| Thuộc tính | `Home_Club_Goals` | `INT` | `CHECK (Home_Club_Goals >= 0)` | Số bàn thắng ghi được của đội chủ nhà |
| Thuộc tính | `Away_Club_Goals` | `INT` | `CHECK (Away_Club_Goals >= 0)` | Số bàn thắng ghi được của đội khách |
| Thuộc tính | `Stadium` | `NVARCHAR(200)` | `NULL` | Tên sân vận động diễn ra trận đấu |

---

## 3. ĐỐI CHIẾU & MAPPING VỚI BỘ DỮ LIỆU KAGGLE (TRANSFERMARKT)

* **Tệp CSV nguồn gốc từ Kaggle:** `games.csv` (Tổng cộng 23 cột thuộc tính gốc).
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### Bảng Ma Trận Ánh Xạ (Mapping Matrix Kaggle $\rightarrow$ DW)

| Tệp CSV Nguồn | Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Quy tắc chuyển đổi ETL & Xử lý dữ liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `games.csv` | `game_id` | `Int64` | `Game_ID` | `INT` | Ép kiểu `(DT_I4)` giữ nguyên mã định danh |
| `games.csv` | `season` | `Int64` | `Season` | `INT` | Ép kiểu `(DT_I4)` năm bắt đầu mùa giải |
| `games.csv` | `round` | `string` | `Round` | `NVARCHAR(100)` | Ép kiểu `(DT_WSTR, 100)` định dạng vòng đấu |
| `games.csv` | `home_club_id` | `Int64` | `Home_Club_ID` | `INT` | Ép kiểu `(DT_I4)` mã đội nhà |
| `games.csv` | `away_club_id` | `Int64` | `Away_Club_ID` | `INT` | Ép kiểu `(DT_I4)` mã đội khách |
| `games.csv` | `home_club_goals` | `Int64` | `Home_Club_Goals` | `INT` | Ép kiểu `(DT_I4)`, thay NULL bằng `0` |
| `games.csv` | `away_club_goals` | `Int64` | `Away_Club_Goals` | `INT` | Ép kiểu `(DT_I4)`, thay NULL bằng `0` |
| `games.csv` | `stadium` | `string` | `Stadium` | `NVARCHAR(200)` | Chuẩn hóa Unicode `(DT_WSTR)`, điền `'Unknown Stadium'` nếu NULL |

---

## 4. QUY TRÌNH BIẾN ĐỔI SSIS ETL (TRANSFORMATION LOGIC)

1. **Flat File Source:** Đọc tệp dữ liệu đã qua tiền xử lý `cleaned_games.csv` (hoặc `games.csv`).
2. **Data Conversion Component:**
   * Ép kiểu số nguyên (`DT_I4`) cho: `game_id`, `season`, `home_club_id`, `away_club_id`, `home_club_goals`, `away_club_goals`.
   * Ép kiểu chuỗi ký tự Unicode (`DT_WSTR`) cho: `round`, `stadium`.
3. **Derived Column Component:**
   * Thay thế giá trị NULL của `Stadium`: `ISNULL(stadium) ? "Unknown Stadium" : TRIM(stadium)`
   * Tỷ số mặc định nếu khuyết: `ISNULL(home_club_goals) ? 0 : home_club_goals`
4. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Khởi tạo bản ghi mặc định `Game_SK = -1`, `Game_ID = -1`, `Round = 'Unknown Round'` cho các trường hợp tra cứu Lookup không tìm thấy trận đấu trong Fact.
5. **OLE DB Destination:** Đẩy dữ liệu vào bảng `dbo.DIM_Game`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính duy nhất:** Đảm bảo `Game_ID` không bị lặp lại trong `DIM_Game`.
* **Toàn vẹn tham chiếu:** Kiểm tra mọi `game_id` trong `appearances.csv` đều tồn tại trong `DIM_Game` để phục vụ join dữ liệu chính xác.
