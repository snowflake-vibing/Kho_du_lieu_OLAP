# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_GAME (TRẬN ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Game]`  
> **Tệp dữ liệu nguồn:** `cleaned_games.csv` (hoặc `games.csv`)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Chỉ sử dụng duy nhất chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```
[1. Flat File Source (games.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4 & DT_WSTR 100/200)]
       │
       ▼
[3. Derived Column (Xử lý NULL Stadium & Tỷ số bàn thắng)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ 8 cột)]
       │
       ▼ (Output: Valid_Game)
[5. Sort (Sort Ascending theo Game_ID & Distinct loại trùng)]
       │
       ▼
[6. OLE DB Destination (dbo.DIM_Game - Table lock, Fast Load)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc file `cleaned_games.csv`)
* **Connection Manager**: `FF_Game` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (8 cột): `game_id`, `season`, `round`, `home_club_id`, `away_club_id`, `home_club_goals`, `away_club_goals`, `stadium`.
* **Output Column Length**: Đặt **200** cho tất cả các cột chuỗi.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu (BK) |
| `season` | **`dc_season`** | Four-byte signed integer `[DT_I4]` | - | Mùa giải (Năm bắt đầu) |
| `round` | **`dc_round`** | Unicode string `[DT_WSTR]` | **100** | Vòng đấu (*Matchday 1...*) |
| `home_club_id` | **`dc_home_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã đội chủ nhà |
| `away_club_id` | **`dc_away_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã đội khách |
| `home_club_goals` | **`dc_home_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội nhà |
| `away_club_goals` | **`dc_away_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội khách |
| `stadium` | **`dc_stadium`** | Unicode string `[DT_WSTR]` | **200** | Tên SVĐ diễn ra trận đấu |

### Khối 3: `Derived Column` (Xử lý NULL & Gán mặc định)

* **`der_stadium`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_stadium) || LEN(TRIM(dc_stadium)) == 0 ? "Unknown Stadium" : TRIM(dc_stadium)`
* **`der_home_goals`** (`[DT_I4]`): `ISNULL(dc_home_club_goals) ? 0 : dc_home_club_goals`
* **`der_away_goals`** (`[DT_I4]`): `ISNULL(dc_away_club_goals) ? 0 : dc_away_club_goals`

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 8 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 8 CỘT (`dc_game_id`, `dc_season`, `dc_round`, `dc_home_club_id`, `dc_away_club_id`, `der_home_goals`, `der_away_goals`, `der_stadium`) vào Input.
* **Output Name**: `Valid_Game`
* **Condition Expression**:
  ```c
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_season) && dc_season > 0 &&
  !ISNULL(dc_round) && LEN(TRIM(dc_round)) > 0 &&
  !ISNULL(dc_home_club_id) && dc_home_club_id > 0 &&
  !ISNULL(dc_away_club_id) && dc_away_club_id > 0 &&
  !ISNULL(der_home_goals) && der_home_goals >= 0 &&
  !ISNULL(der_away_goals) && der_away_goals >= 0 &&
  !ISNULL(der_stadium)
  ```
* **Default Output Name**: `Invalid_Game`

### Khối 5: `Sort` (Khử trùng lặp theo Game_ID)
* **Input Path**: Chọn nhánh **`Valid_Game`**.
* **Pass Through Columns**: Tick chọn cả 8 cột.
* **Sort Column**: Tick chọn `dc_game_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Game]`.
* **Mappings**:
  * `dc_game_id` $\rightarrow$ **`Game_ID`** (`int`)
  * `dc_season` $\rightarrow$ **`Season`** (`int`)
  * `dc_round` $\rightarrow$ **`Round`** (`nvarchar(100)`)
  * `dc_home_club_id` $\rightarrow$ **`Home_Club_ID`** (`int`)
  * `dc_away_club_id` $\rightarrow$ **`Away_Club_ID`** (`int`)
  * `der_home_goals` $\rightarrow$ **`Home_Club_Goals`** (`int`)
  * `der_away_goals` $\rightarrow$ **`Away_Club_Goals`** (`int`)
  * `der_stadium` $\rightarrow$ **`Stadium`** (`nvarchar(200)`)
