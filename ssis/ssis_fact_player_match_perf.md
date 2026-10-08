# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: FACT_PLAYER_MATCH_PERF

> **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`  
> **Tệp dữ liệu nguồn:** `appearances.csv` (1.89 triệu lượt ra sân)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`).

---

## 1. MÔ HÌNH NẠP FACT 2 BƯỚC (TWO-STAGE FACT ETL ARCHITECTURE)

```
[BƯỚC 1: Data Flow Task - Load Staging Appearances]
   Flat File Source (appearances.csv) ──➔ Data Conversion ──➔ OLE DB Destination (STG_Appearances - Fast Load 50.000 rows/batch)

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
* **Selected Columns** (9 cột): `appearance_id`, `game_id`, `player_id`, `player_club_id`, `competition_id`, `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards`.

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

### Khối 3: `OLE DB Destination` (Cấu hình Fast Load tối ưu cho 1.89M dòng)
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
```
