# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: FACT_PLAYER_MATCH_PERF (SỬ DỤNG LOOKUP TRANSFORMATIONS)

> **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`  
> **Tệp dữ liệu nguồn:** `appearances.csv` (1.89 triệu lượt ra sân)  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Phương pháp ETL:** Pure Data Flow Task (Nạp trực tiếp qua chuỗi **Lookup Transformations** trong Data Flow, không dùng `Execute SQL Task` hay câu lệnh SQL JOIN).  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU DATA FLOW (LOOKUP CHAIN ARCHITECTURE)

```text
[1. Flat File Source (appearances.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4, DT_WSTR 100/200)]
       │
       ▼
[3. Derived Column - Prep Time ID (Tạo der_time_id dạng YYYYMMDD)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra dữ liệu 11 cột)]
       │
       ▼ (Output: Valid_Appearance)
[5. Lookup Player (Tra cứu DIM_Player lấy Player_ID / Player_SK)]
       │
       ▼
[6. Lookup Club (Tra cứu DIM_Club lấy Club_ID / Club_SK)]
       │
       ▼
[7. Lookup Competition (Tra cứu DIM_Competition lấy Competition_ID / Competition_SK)]
       │
       ▼
[8. Lookup Time (Tra cứu DIM_Time lấy Time_ID / Time_SK)]
       │
       ▼
[9. Lookup Game Info (Tra cứu DIM_Game lấy Home_Club_ID & Away_Club_ID)]
       │
       ▼
[10. Derived Column - Fact Measures & Dynamic Flags (Tính Goals, Assists, Goal_Contributions, Is_Starter, Is_Home_Game, Opponent_Club_ID)]
       │
       ▼
[11. OLE DB Destination (dbo.FACT_Player_Match_Perf - Table Lock, Fast Load 50.000 rows/batch)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc tệp `appearances.csv`)
* **Connection Manager**: `FF_Appearances` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (11 cột): `appearance_id`, `game_id`, `player_id`, `player_club_id`, `date` (hoặc `date_str`), `competition_id`, `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards`.
* **Output Column Length**: Thiết lập **100** cho tất cả các cột kiểu chuỗi (`appearance_id`, `date`, `competition_id`).

---

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `appearance_id` | **`dc_appearance_id`** | Unicode string `[DT_WSTR]` | **100** | Mã lượt ra sân |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu (BK) |
| `player_id` | **`dc_player_id`** | Four-byte signed integer `[DT_I4]` | - | Mã cầu thủ (BK) |
| `player_club_id` | **`dc_player_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã câu lạc bộ (BK) |
| `date` / `date_str` | **`dc_date_str`** | Unicode string `[DT_WSTR]` | **100** | Chuỗi ngày đấu (`YYYY-MM-DD`) |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** | Mã giải đấu (BK) |
| `goals` | **`dc_goals`** | Four-byte signed integer `[DT_I4]` | - | Số bàn thắng |
| `assists` | **`dc_assists`** | Four-byte signed integer `[DT_I4]` | - | Số đường kiến tạo |
| `minutes_played` | **`dc_minutes_played`** | Four-byte signed integer `[DT_I4]` | - | Phút thi đấu trên sân |
| `yellow_cards` | **`dc_yellow_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ vàng |
| `red_cards` | **`dc_red_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ đỏ |

---

### Khối 3: `Derived Column` - Chuẩn bị khóa Thời gian (`Prep Time ID`)
* **Tên khối**: `Derived Column - Prep Time ID`
* **Mục đích**: Chuyển đổi chuỗi ngày `YYYY-MM-DD` (`dc_date_str`) thành số nguyên `YYYYMMDD` (`[DT_I4]`) để tra cứu với khóa `Time_ID` trong `DIM_Time`.

| Derived Column Name | Derived Column | Expression | Data Type |
| :--- | :--- | :--- | :--- |
| **`der_time_id`** | Add as new column | `ISNULL(dc_date_str) \|\| LEN(TRIM(dc_date_str)) < 10 ? 19000101 : (DT_I4)(SUBSTRING(dc_date_str, 1, 4) + SUBSTRING(dc_date_str, 6, 2) + SUBSTRING(dc_date_str, 9, 2))` | `[DT_I4]` |

---

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 11 CỘT)
* **Input Columns**: Tick ĐẦY ĐỦ 11 CỘT (`dc_appearance_id`, `dc_game_id`, `dc_player_id`, `dc_player_club_id`, `dc_date_str`, `der_time_id`, `dc_competition_id`, `dc_goals`, `dc_assists`, `dc_minutes_played`, `dc_yellow_cards`, `dc_red_cards`).
* **Output Name**: `Valid_Appearance`
* **Condition Expression**:
  ```c
  !ISNULL(dc_appearance_id) && LEN(TRIM(dc_appearance_id)) > 0 &&
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_player_id) && dc_player_id > 0 &&
  !ISNULL(dc_player_club_id) && dc_player_club_id > 0 &&
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 &&
  !ISNULL(der_time_id) && der_time_id > 0 &&
  !ISNULL(dc_goals) && dc_goals >= 0 &&
  !ISNULL(dc_assists) && dc_assists >= 0 &&
  !ISNULL(dc_minutes_played) && dc_minutes_played >= 0 &&
  !ISNULL(dc_yellow_cards) && dc_yellow_cards >= 0 &&
  !ISNULL(dc_red_cards) && dc_red_cards >= 0
  ```
* **Default Output Name**: `Invalid_Appearance`

---

### Khối 5: `Lookup Player` (Tra cứu Cầu thủ - DIM_Player)
* **Tab General**:
  * **Cache mode**: Chọn **`Full cache`** (Nạp bảng DIM_Player vào bộ nhớ RAM).
  * **Connection type**: **`OLE DB connection manager`**.
  * **Specify how to handle rows with no matching entries**: Chọn **`Ignore failure`** *(Không ngắt luồng khi không thấy cầu thủ; trả về NULL)*.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Player]`** (SQL: `SELECT Player_ID FROM dbo.DIM_Player`).
* **Tab Columns**:
  * Nối đường kẻ từ cột đầu vào **`dc_player_id`** sang cột Lookup **`Player_ID`**.
  * Tích chọn ô **`Player_ID`** ở bảng bên phải.
  * **Output Alias**: Nhập **`lk_player_id`** *(hoặc `Player_SK` nếu dùng mô hình Surrogate Key)*.

---

### Khối 6: `Lookup Club` (Tra cứu Câu lạc bộ Cầu thủ - DIM_Club)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Club]`** (SQL: `SELECT Club_ID FROM dbo.DIM_Club`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_player_club_id`** sang cột Lookup **`Club_ID`**.
  * Tích chọn ô **`Club_ID`**.
  * **Output Alias**: Nhập **`lk_club_id`** *(hoặc `Club_SK` nếu dùng mô hình Surrogate Key)*.

---

### Khối 7: `Lookup Competition` (Tra cứu Giải đấu - DIM_Competition)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Competition]`** (SQL: `SELECT Competition_ID FROM dbo.DIM_Competition`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_competition_id`** sang cột Lookup **`Competition_ID`**.
  * Tích chọn ô **`Competition_ID`**.
  * **Output Alias**: Nhập **`lk_competition_id`** *(hoặc `Competition_SK` nếu dùng mô hình Surrogate Key)*.

---

### Khối 8: `Lookup Time` (Tra cứu Thời gian - DIM_Time)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Time]`** (SQL: `SELECT Time_ID FROM dbo.DIM_Time`).
* **Tab Columns**:
  * Nối cột đầu vào **`der_time_id`** sang cột Lookup **`Time_ID`**.
  * Tích chọn ô **`Time_ID`**.
  * **Output Alias**: Nhập **`lk_time_id`** *(hoặc `Time_SK` nếu dùng mô hình Surrogate Key)*.

---

### Khối 9: `Lookup Game Info` (Tra cứu Trận đấu & Lấy Đội nhà / Đội khách)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn tùy chọn **Use results of an SQL query**:
  ```sql
  SELECT Game_ID, Home_Club_ID, Away_Club_ID 
  FROM dbo.DIM_Game
  ```
* **Tab Columns**:
  * Nối cột đầu vào **`dc_game_id`** sang cột Lookup **`Game_ID`**.
  * Tích chọn ô **`Home_Club_ID`** $\rightarrow$ Output Alias: **`lk_home_club_id`**.
  * Tích chọn ô **`Away_Club_ID`** $\rightarrow$ Output Alias: **`lk_away_club_id`**.

---

### Khối 10: `Derived Column` - Fact Measures & Dynamic Flags
* **Tên khối**: `Derived Column - Fact Measures`
* **Mục đích**: Tính toán các chỉ số độ đo (Measures), xử lý giá trị mặc định cho dữ liệu tra cứu Lookup không khớp (`NULL`), và tính toán cờ nhận diện trận đấu sân nhà / sân khách cũng như đội đối thủ.

| Derived Column Name | Derived Column | Expression | Data Type | Length |
| :--- | :--- | :--- | :--- | :--- |
| **`Goal_Contributions`** | Add as new column | `dc_goals + dc_assists` | `[DT_I4]` | - |
| **`Is_Starter`** | Add as new column | `dc_minutes_played >= 45 ? 1 : 0` | `[DT_I4]` | - |
| **`Is_Home_Game`** | Add as new column | `!ISNULL(lk_home_club_id) && dc_player_club_id == lk_home_club_id ? 1 : 0` | `[DT_I4]` | - |
| **`Opponent_Club_ID`** | Add as new column | `!ISNULL(lk_home_club_id) && dc_player_club_id == lk_home_club_id ? lk_away_club_id : lk_home_club_id` | `[DT_I4]` | - |
| **`Player_ID_Final`** | Add as new column | `ISNULL(lk_player_id) ? -1 : lk_player_id` | `[DT_I4]` | - |
| **`Club_ID_Final`** | Add as new column | `ISNULL(lk_club_id) ? -1 : lk_club_id` | `[DT_I4]` | - |
| **`Competition_ID_Final`** | Add as new column | `ISNULL(lk_competition_id) \|\| LEN(TRIM(lk_competition_id)) == 0 ? "UNKNOWN" : lk_competition_id` | `[DT_WSTR]` | **100** |
| **`Time_ID_Final`** | Add as new column | `ISNULL(lk_time_id) ? 19000101 : lk_time_id` | `[DT_I4]` | - |

---

### Khối 11: `OLE DB Destination` (Nạp dữ liệu vào bảng FACT_Player_Match_Perf)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[FACT_Player_Match_Perf]`.
* **Cấu hình Fast Load quan trọng**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.
* **Mappings (Ánh xạ cột đầu vào với CSDL)**:

| Cột Luồng SSIS (Input Column) | Cột Đích SQL Server (Target Column) | Kiểu Dữ Liệu CSDL |
| :--- | :--- | :--- |
| `Player_ID_Final` *(hoặc Player_SK)* | **`Player_ID`** *(hoặc Player_SK)* | `INT` |
| `Club_ID_Final` *(hoặc Club_SK)* | **`Club_ID`** *(hoặc Club_SK)* | `INT` |
| `Opponent_Club_ID` | **`Opponent_Club_ID`** | `INT` |
| `Competition_ID_Final` | **`Competition_ID`** | `NVARCHAR(100)` |
| `dc_game_id` | **`Game_ID`** | `INT` |
| `Time_ID_Final` | **`Time_ID`** | `INT` |
| `dc_minutes_played` | **`Minutes_Played`** | `INT` |
| `dc_goals` | **`Goals`** | `INT` |
| `dc_assists` | **`Assists`** | `INT` |
| `Goal_Contributions` | **`Goal_Contributions`** | `INT` |
| `dc_yellow_cards` | **`Yellow_Cards`** | `INT` |
| `dc_red_cards` | **`Red_Cards`** | `INT` |
| `Is_Starter` | **`Is_Starter`** | `INT` |
| `Is_Home_Game` | **`Is_Home_Game`** | `INT` |

---

## 3. QUY TRÌNH XỬ LÝ DÒNG KHÔNG KHỚP LOOKUP (LOOKUP NO-MATCH HANDLING)

Trong SSIS Data Flow, có 2 chiến lược xử lý khi tra cứu Lookup không tìm thấy dòng dữ liệu trong bảng Dimension:

### Tùy chọn A: Fast Load với giá trị Mặc định (Khuyến nghị - 0 ngắt luồng)
1. Trong tất cả các khối Lookup (`Lookup Player`, `Lookup Club`, `Lookup Competition`, `Lookup Time`, `Lookup Game Info`), đặt cấu hình:
   * **Specify how to handle rows with no matching entries**: Chọn **`Ignore failure`**.
2. Tại khối **`Derived Column - Fact Measures`**, sử dụng hàm kiểm tra `ISNULL(...)` để gán giá trị mặc định cho các dòng không tìm thấy (ví dụ: `-1` cho `INT` hoặc `"UNKNOWN"` cho string).
3. Luồng dữ liệu đi thẳng mượt mà vào `OLE DB Destination` với tốc độ Fast Load tối đa (50.000 rows/batch).

### Tùy chọn B: Ghi vết Audit lỗi vào Bảng Error (FACT_Player_Match_Perf_Error)
1. Trong khối Lookup, chọn **`Redirect rows to No Match Output`**.
2. Nối nhánh đầu ra **`Lookup No Match Output`** sang khối `Derived Column` gán mô tả lỗi `Error_Reason` (ví dụ: `"Player_ID missing in DIM_Player"`).
3. Đẩy nhánh lỗi vào bảng **`[dbo].[FACT_Player_Match_Perf_Error]`** để phục vụ kiểm tra dữ liệu thiếu sót.

---

## 4. TỔNG HỢP NGUYÊN TẮC VÀNG VỀ HIỆU NĂNG & TRIỆT TIÊU WARNING

1. **Full Cache Optimization**:
   * Cấu hình **`Full cache`** trên tất cả 5 khối Lookup giúp SSIS nạp toàn bộ các bảng Dimension vào RAM 1 lần duy nhất ngay khi khởi chạy task, giúp tra cứu 1.89 triệu dòng ra sân chỉ trong vài giây.
2. **Không lệch kiểu dữ liệu (Data Type Matching)**:
   * Cột nối trong Lookup phải khớp chính xác kiểu dữ liệu với bảng DIM:
     * `dc_game_id` `[DT_I4]` $\leftrightarrow$ `DIM_Game.Game_ID` `[DT_I4]`
     * `dc_competition_id` `[DT_WSTR, 100]` $\leftrightarrow$ `DIM_Competition.Competition_ID` `[DT_WSTR, 100]`
3. **Triệt tiêu Warning 100% (0 tam giác vàng)**:
   * Giữ chuẩn độ dài chuỗi **100/200** thống nhất từ Source $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ OLE DB Destination.
