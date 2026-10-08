# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: FACT_PLAYER_MATCH_PERF

> **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`  
> **Tệp dữ liệu nguồn:** `appearances.csv` (1.89 triệu lượt ra sân)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`).

---

## 1. MÔ HÌNH NẠP FACT 2 BƯỚC (TWO-STAGE FACT ETL ARCHITECTURE)

```
[BƯỚC 1: Data Flow Task - Load Staging Appearances]
   Flat File Source (appearances.csv) ──➔ Data Conversion ──➔ Conditional Split (Validation 10 cột) ──➔ OLE DB Destination (STG_Appearances - Fast Load 50.000 rows/batch)

                                  │
                                  ▼
[BƯỚC 2: Execute SQL Task - Populate FACT via SQL Join]
   TRUNCATE TABLE FACT_Player_Match_Perf;
   INSERT INTO FACT_Player_Match_Perf WITH (LEFT JOIN 5 BẢNG DIM);
```

---

## 2. CHI TIẾT CẤU HÌNH BƯỚC 1: DATA FLOW LOAD STAGING (`STG_Appearances`)

### Khối 1: `Flat File Source` (Đọc file `appearances.csv`)
* **Connection Manager**: `FF_Appearances` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (10 cột): `appearance_id`, `game_id`, `player_id`, `player_club_id`, `competition_id`, `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards`.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `appearance_id` | **`dc_appearance_id`** | String `[DT_STR]` | **100** | Mã lượt ra sân |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu |
| `player_id` | **`dc_player_id`** | Four-byte signed integer `[DT_I4]` | - | Mã cầu thủ |
| `player_club_id` | **`dc_player_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã câu lạc bộ |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** | Mã giải đấu |
| `goals` | **`dc_goals`** | Four-byte signed integer `[DT_I4]` | - | Số bàn thắng |
| `assists` | **`dc_assists`** | Four-byte signed integer `[DT_I4]` | - | Số đường kiến tạo |
| `minutes_played` | **`dc_minutes_played`** | Four-byte signed integer `[DT_I4]` | - | Phút thi đấu |
| `yellow_cards` | **`dc_yellow_cards`** | Four-byte signed integer `[DT_I4]` | - | Thẻ vàng |
| `red_cards` | **`dc_red_cards`** | Four-byte signed integer `[DT_I4]` | - | Thẻ đỏ |

### Khối 3: `Conditional Split` (Validation kiểm tra TOÀN BỘ 10 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 10 CỘT (`dc_appearance_id`, `dc_game_id`, `dc_player_id`, `dc_player_club_id`, `dc_competition_id`, `dc_goals`, `dc_assists`, `dc_minutes_played`, `dc_yellow_cards`, `dc_red_cards`) vào Input.
* **Output Name**: `Valid_Appearance`
* **Condition Expression**:
  ```c
  !ISNULL(dc_appearance_id) && LEN(TRIM(dc_appearance_id)) > 0 &&
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_player_id) && dc_player_id > 0 &&
  !ISNULL(dc_player_club_id) && dc_player_club_id > 0 &&
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 &&
  !ISNULL(dc_goals) && dc_goals >= 0 &&
  !ISNULL(dc_assists) && dc_assists >= 0 &&
  !ISNULL(dc_minutes_played) && dc_minutes_played >= 0 &&
  !ISNULL(dc_yellow_cards) && dc_yellow_cards >= 0 &&
  !ISNULL(dc_red_cards) && dc_red_cards >= 0
  ```
* **Default Output Name**: `Invalid_Appearance`

### Khối 4: `OLE DB Destination` (Cấu hình Fast Load tối ưu cho 1.89M dòng)
* **Input Path**: Chọn nhánh **`Valid_Appearance`**.
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[STG_Appearances]`.
* **Cấu hình Fast Load quan trọng**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.

---

## 3. CHI TIẾT CẤU HÌNH BƯỚC 2: EXECUTE SQL TASK POPULATE FACT

Đặt 1 khối **`Execute SQL Task`** trên Control Flow nối tiếp sau Data Flow Load Staging:

* **Task Name**: `Populate FACT_Player_Match_Perf`
* **Connection**: OLE DB Connection đến `DW_Football_Analytics`.
* **SQLStatement**:

```sql
USE DW_Football_Analytics;
GO

-- 1. Xóa sạch dữ liệu cũ
TRUNCATE TABLE dbo.FACT_Player_Match_Perf;

-- 2. Nạp dữ liệu sự kiện kết hợp liên kết 5 bảng DIM và tính toán độ đo
INSERT INTO dbo.FACT_Player_Match_Perf (
    Player_SK,
    Club_SK,
    Opponent_Club_SK,
    Competition_SK,
    Game_SK,
    Time_SK,
    Game_ID,
    Minutes_Played,
    Goals,
    Assists,
    Goal_Contributions,
    Yellow_Cards,
    Red_Cards,
    Is_Starter
)
SELECT 
    ISNULL(p.Player_SK, -1) AS Player_SK,
    ISNULL(c.Club_SK, -1) AS Club_SK,
    ISNULL(c.Club_SK, -1) AS Opponent_Club_SK,
    ISNULL(comp.Competition_SK, -1) AS Competition_SK,
    ISNULL(g.Game_SK, -1) AS Game_SK,
    1 AS Time_SK,
    s.game_id,
    ISNULL(s.minutes_played, 0),
    ISNULL(s.goals, 0),
    ISNULL(s.assists, 0),
    (ISNULL(s.goals, 0) + ISNULL(s.assists, 0)) AS Goal_Contributions,
    ISNULL(s.yellow_cards, 0),
    ISNULL(s.red_cards, 0),
    CASE WHEN ISNULL(s.minutes_played, 0) >= 45 THEN 1 ELSE 0 END AS Is_Starter
FROM dbo.STG_Appearances s
LEFT JOIN dbo.DIM_Player p ON s.player_id = p.Player_ID
LEFT JOIN dbo.DIM_Club c ON s.player_club_id = c.Club_ID
LEFT JOIN dbo.DIM_Competition comp ON s.competition_id = comp.Competition_ID
LEFT JOIN dbo.DIM_Game g ON s.game_id = g.Game_ID;
GO

---

## 4. PHƯƠNG PHÁP NẠP FACT BẰNG CHUỖI LOOKUP TRANSFORMATIONS TRONG DATA FLOW

Nếu bạn muốn thực hiện tra cứu và chuyển đổi các khóa tự nhiên (`Business Keys`) thành khóa thay thế (`Surrogate Keys - *_SK`) **trực tiếp trong Data Flow Task của SSIS** thay vì dùng câu lệnh `INSERT ... SELECT LEFT JOIN` ở Execute SQL Task, bạn cấu hình chuỗi các khối theo hướng dẫn chi tiết từng khối dưới đây:

### 4.1. Sơ đồ Luồng Data Flow (Lookup Chain)
```
[Flat File Source (appearances.csv)]
       │
       ▼
[Data Conversion] (Chuẩn hóa dc_player_id, dc_player_club_id, dc_competition_id, dc_game_id, dc_date_str)
       │
       ▼
[Conditional Split] (Lọc dòng hợp lệ Valid_Appearance)
       │
       ▼
[Khối 1: Lookup Player_SK]
       │
       ▼
[Khối 2: Lookup Club_SK]
       │
       ▼
[Khối 3: Lookup Opponent_Club_SK]
       │
       ▼
[Khối 4: Lookup Competition_SK]
       │
       ▼
[Khối 5: Lookup Game_SK]
       │
       ▼
[Khối 6: Lookup Time_SK]
       │
       ▼
[Khối 7: Derived Column - Fact Measures]
       │
       ▼
[Khối 8: OLE DB Destination (dbo.FACT_Player_Match_Perf)]
```

---

### 4.2. Hướng dẫn cấu hình chi tiết từng Khối (Block-by-Block Configuration)

#### Khối 1: `Lookup Player_SK` (Tra cứu khóa Cầu thủ)
* **Tab General**:
  * **Cache mode**: Chọn **`Full cache`** (Nạp toàn bộ bảng DIM_Player vào RAM).
  * **Connection type**: Chọn **`OLE DB connection manager`**.
  * **Specify how to handle rows with no matching entries**: Chọn **`Ignore failure`** (Nếu không tìm thấy cầu thủ, trả về `NULL` cho `Player_SK`).
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Player]`** (hoặc nhập SQL query: `SELECT Player_SK, Player_ID FROM dbo.DIM_Player`).
* **Tab Columns**:
  * Đốt nối đường kẻ từ cột đầu vào **`dc_player_id`** sang cột Lookup **`Player_ID`**.
  * Tích chọn ô **`Player_SK`** ở bảng bên phải.
  * **Output Alias**: Nhập **`Player_SK`**.

---

#### Khối 2: `Lookup Club_SK` (Tra cứu khóa Câu lạc bộ của Cầu thủ)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Club]`** (hoặc SQL: `SELECT Club_SK, Club_ID FROM dbo.DIM_Club`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_player_club_id`** sang cột Lookup **`Club_ID`**.
  * Tích chọn ô **`Club_SK`**.
  * **Output Alias**: Nhập **`Club_SK`**.

---

#### Khối 3: `Lookup Opponent_Club_SK` (Tra cứu khóa Câu lạc bộ Đối thủ)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Club]`** (hoặc SQL: `SELECT Club_SK, Club_ID FROM dbo.DIM_Club`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_opponent_club_id`** (hoặc mã đội đối thủ) sang cột Lookup **`Club_ID`**.
  * Tích chọn ô **`Club_SK`**.
  * **Output Alias**: Nhập **`Opponent_Club_SK`** *(Lưu ý bắt buộc đổi tên Alias thành Opponent_Club_SK để không bị đè lên cột Club_SK đã lấy ở Khối 2)*.

---

#### Khối 4: `Lookup Competition_SK` (Tra cứu khóa Giải đấu)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Competition]`** (hoặc SQL: `SELECT Competition_SK, Competition_ID FROM dbo.DIM_Competition`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_competition_id`** sang cột Lookup **`Competition_ID`**.
  * Tích chọn ô **`Competition_SK`**.
  * **Output Alias**: Nhập **`Competition_SK`**.

---

#### Khối 5: `Lookup Game_SK` (Tra cứu khóa Trận đấu)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Game]`** (hoặc SQL: `SELECT Game_SK, Game_ID FROM dbo.DIM_Game`).
* **Tab Columns**:
  * Nối cột đầu vào **`dc_game_id`** sang cột Lookup **`Game_ID`**.
  * Tích chọn ô **`Game_SK`**.
  * **Output Alias**: Nhập **`Game_SK`**.

---

#### Khối 6: `Lookup Time_SK` (Tra cứu khóa Thời gian)
* **Tab General**:
  * **Cache mode**: **`Full cache`**.
  * **Connection type**: **`OLE DB connection manager`**.
  * **No matching entries**: **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Time]`** (hoặc SQL: `SELECT Time_SK, Time_ID FROM dbo.DIM_Time`).
* **Tab Columns**:
  * Nối cột đầu vào **`Time_ID`** (dạng số YYYYMMDD thu được từ ngày đấu) sang cột Lookup **`Time_ID`**.
  * Tích chọn ô **`Time_SK`**.
  * **Output Alias**: Nhập **`Time_SK`**.

---

#### Khối 7: `Derived Column` (Tính toán độ đo - Fact Measures)
* **Tên khối**: `Derived Column - Fact Measures`
* Cấu hình tạo các cột độ đo tính toán mới trong luồng:

| Derived Column Name | Derived Column | Expression | Data Type |
| :--- | :--- | :--- | :--- |
| **`Goal_Contributions`** | Add as new column | `dc_goals + dc_assists` | `[DT_I4]` |
| **`Is_Starter`** | Add as new column | `dc_minutes_played >= 45 ? 1 : 0` | `[DT_I4]` |

---

#### Khối 8: `OLE DB Destination` (Nạp dữ liệu vào bảng Fact)
* **Connection Manager**: OLE DB Connection đến database `DW_Football_Transfermarkt`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[FACT_Player_Match_Perf]`.
* **Cấu hình Fast Load**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.
* **Mappings (Ánh xạ cột)**:
  - `Player_SK` ➔ `Player_SK`
  - `Club_SK` ➔ `Club_SK`
  - `Opponent_Club_SK` ➔ `Opponent_Club_SK`
  - `Competition_SK` ➔ `Competition_SK`
  - `Game_SK` ➔ `Game_SK`
  - `Time_SK` ➔ `Time_SK`
  - `dc_game_id` ➔ `Game_ID`
  - `dc_minutes_played` ➔ `Minutes_Played`
  - `dc_goals` ➔ `Goals`
  - `dc_assists` ➔ `Assists`
  - `Goal_Contributions` ➔ `Goal_Contributions`
  - `dc_yellow_cards` ➔ `Yellow_Cards`
  - `dc_red_cards` ➔ `Red_Cards`
  - `Is_Starter` ➔ `Is_Starter`
