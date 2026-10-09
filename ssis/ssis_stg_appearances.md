# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: LOAD STAGING APPEARANCES (STG_APPEARANCES)

> **Bảng đích:** `[dbo].[STG_Appearances]`  
> **Tệp dữ liệu nguồn:** `appearances.csv` (hoặc `cleaned_appearances.csv` - 1.89 triệu bản ghi)  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Mục đích:** Nạp thô siêu tốc dữ liệu lượt ra sân vào bảng đệm trung gian, ép kiểu dữ liệu chuẩn, và lọc loại bỏ bản ghi không hợp lệ. (Lưu ý: `Time_ID` dạng số nguyên `YYYYMMDD` sẽ được tính toán qua Derived Column tại luồng nạp **Fact** `FACT_Player_Match_Perf`).  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU DATA FLOW (STAGING PIPELINE)

```text
[1. Flat File Source (appearances.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4, DT_WSTR 100/200)]
       │
       ▼
[3. Conditional Split (Validation kiểm tra dữ liệu hợp lệ)]
       │
       ▼ (Output: Valid_Appearance)
[4. OLE DB Destination (dbo.STG_Appearances - Fast Load 50.000 rows/batch, Table Lock)]
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
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu |
| `player_id` | **`dc_player_id`** | Four-byte signed integer `[DT_I4]` | - | Mã cầu thủ |
| `player_club_id` | **`dc_player_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã câu lạc bộ |
| `date` / `date_str` | **`dc_date_str`** | Unicode string `[DT_WSTR]` | **100** | Chuỗi ngày đấu (`YYYY-MM-DD`) |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** | Mã giải đấu |
| `goals` | **`dc_goals`** | Four-byte signed integer `[DT_I4]` | - | Số bàn thắng |
| `assists` | **`dc_assists`** | Four-byte signed integer `[DT_I4]` | - | Số đường kiến tạo |
| `minutes_played` | **`dc_minutes_played`** | Four-byte signed integer `[DT_I4]` | - | Phút thi đấu |
| `yellow_cards` | **`dc_yellow_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ vàng |
| `red_cards` | **`dc_red_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ đỏ |

---

### Khối 3: `Conditional Split` (Validation kiểm tra dữ liệu hợp lệ)
* **Input Columns**: Tick chọn 11 cột (`dc_appearance_id`, `dc_game_id`, `dc_player_id`, `dc_player_club_id`, `dc_date_str`, `dc_competition_id`, `dc_goals`, `dc_assists`, `dc_minutes_played`, `dc_yellow_cards`, `dc_red_cards`).
* **Output Name**: `Valid_Appearance`
* **Condition Expression**:
  ```c
  !ISNULL(dc_appearance_id) && LEN(TRIM(dc_appearance_id)) > 0 &&
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_player_id) && dc_player_id > 0 &&
  !ISNULL(dc_player_club_id) && dc_player_club_id > 0 &&
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 &&
  !ISNULL(dc_date_str) && LEN(TRIM(dc_date_str)) >= 10 &&
  !ISNULL(dc_goals) && dc_goals >= 0 &&
  !ISNULL(dc_assists) && dc_assists >= 0 &&
  !ISNULL(dc_minutes_played) && dc_minutes_played >= 0 &&
  !ISNULL(dc_yellow_cards) && dc_yellow_cards >= 0 &&
  !ISNULL(dc_red_cards) && dc_red_cards >= 0
  ```
* **Default Output Name**: `Invalid_Appearance`

---

### Khối 4: `OLE DB Destination` (Nạp dữ liệu vào STG_Appearances)
* **Connection Manager**: OLE DB Connection đến CSDL `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[STG_Appearances]`.
* **Cấu hình Fast Load quan trọng**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.
* **Mappings (Ánh xạ cột luồng SSIS với CSDL)**:

| Cột Luồng SSIS (Input Column) | Cột Đích SQL Server (Target Column) | Kiểu Dữ Liệu CSDL |
| :--- | :--- | :--- |
| `dc_appearance_id` | **`appearance_id`** | `VARCHAR(100)` |
| `dc_game_id` | **`game_id`** | `INT` |
| `dc_player_id` | **`player_id`** | `INT` |
| `dc_player_club_id` | **`player_club_id`** | `INT` |
| `dc_date_str` | **`date_str`** | `VARCHAR(100)` |
| `dc_competition_id` | **`competition_id`** | `VARCHAR(100)` |
| `dc_goals` | **`goals`** | `INT` |
| `dc_assists` | **`assists`** | `INT` |
| `dc_minutes_played` | **`minutes_played`** | `INT` |
| `dc_yellow_cards` | **`yellow_cards`** | `INT` |
| `dc_red_cards` | **`red_cards`** | `INT` |

---

## 3. VỊ TRÍ KHỦNG CỦA BIẾN ĐỔI TIME_ID (YYYYMMDD)

Đúng như thiết kế chuẩn Data Warehouse:
1. Bảng **Staging** `dbo.STG_Appearances` giữ nguyên cấu trúc dữ liệu nguồn thô (bao gồm chuỗi ngày `date_str`).
2. Biến đổi `Time_ID` (dạng `YYYYMMDD` int) sẽ được thực hiện trong **Derived Column** thuộc package SSIS nạp bảng Fact **`FACT_Player_Match_Perf`**:
   ```c
   ISNULL(date_str) || LEN(TRIM(date_str)) < 10 ? 19000101 : (DT_I4)(SUBSTRING(date_str, 1, 4) + SUBSTRING(date_str, 6, 2) + SUBSTRING(date_str, 9, 2))
   ```
