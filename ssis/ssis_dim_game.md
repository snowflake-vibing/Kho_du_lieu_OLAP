# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_GAME (TRẬN ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Game]`  
> **Tệp dữ liệu nguồn:** `cleaned_games.csv` (hoặc `games.csv`)  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Chỉ sử dụng duy nhất chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (games.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4 & DT_WSTR 100/200)]
       │
       ▼
[3. Derived Column (Xử lý NULL Stadium & Tỷ số bàn thắng)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ 7 cột)]
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
* **Selected Columns** (7 cột): `game_id`, `round`, `home_club_id`, `away_club_id`, `home_club_goals`, `away_club_goals`, `stadium`.
* **Output Column Length**: Đặt **200** cho tất cả các cột chuỗi.

---

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu (PK) |
| `round` | **`dc_round`** | Unicode string `[DT_WSTR]` | **100** | Vòng đấu (*Matchday 1...*) |
| `home_club_id` | **`dc_home_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã đội chủ nhà |
| `away_club_id` | **`dc_away_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã đội khách |
| `home_club_goals` | **`dc_home_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội nhà |
| `away_club_goals` | **`dc_away_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội khách |
| `stadium` | **`dc_stadium`** | Unicode string `[DT_WSTR]` | **200** | Tên SVĐ diễn ra trận đấu |

---

### Khối 3: `Derived Column` (Xử lý NULL & Gán mặc định trực tiếp)
* **Mục đích**: Xử lý làm sạch tên sân vận động và giá trị mặc định cho số bàn thắng.

| Derived Column Name | Derived Column | Expression | Data Type | Length |
| :--- | :--- | :--- | :--- | :--- |
| **`Stadium`** | Add as new column | `ISNULL(dc_stadium) \|\| LEN(TRIM(dc_stadium)) == 0 ? "Unknown Stadium" : TRIM(dc_stadium)` | `[DT_WSTR]` | **200** |
| **`Home_Club_Goals`** | Add as new column | `ISNULL(dc_home_club_goals) ? 0 : dc_home_club_goals` | `[DT_I4]` | - |
| **`Away_Club_Goals`** | Add as new column | `ISNULL(dc_away_club_goals) ? 0 : dc_away_club_goals` | `[DT_I4]` | - |

---

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 7 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 7 CỘT (`dc_game_id`, `dc_round`, `dc_home_club_id`, `dc_away_club_id`, `Home_Club_Goals`, `Away_Club_Goals`, `Stadium`) vào Input.
* **Output Name**: `Valid_Game`
* **Condition Expression**:
  ```c
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_round) && LEN(TRIM(dc_round)) > 0 &&
  !ISNULL(dc_home_club_id) && dc_home_club_id > 0 &&
  !ISNULL(dc_away_club_id) && dc_away_club_id > 0 &&
  !ISNULL(Home_Club_Goals) && Home_Club_Goals >= 0 &&
  !ISNULL(Away_Club_Goals) && Away_Club_Goals >= 0 &&
  !ISNULL(Stadium) && LEN(TRIM(Stadium)) > 0
  ```
* **Default Output Name**: `Invalid_Game`

---

### Khối 5: `Sort` (Khử trùng lặp theo Game_ID)
* **Input Path**: Chọn nhánh **`Valid_Game`**.
* **Pass Through Columns**: Tick chọn cả 7 cột.
* **Sort Column**: Tick chọn `dc_game_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

---

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Game]`.
* **Mappings**:
  * `dc_game_id` $\rightarrow$ **`Game_ID`** (`INT`)
  * `dc_round` $\rightarrow$ **`Round`** (`NVARCHAR(100)`)
  * `dc_home_club_id` $\rightarrow$ **`Home_Club_ID`** (`INT`)
  * `dc_away_club_id` $\rightarrow$ **`Away_Club_ID`** (`INT`)
  * `Home_Club_Goals` $\rightarrow$ **`Home_Club_Goals`** (`INT`)
  * `Away_Club_Goals` $\rightarrow$ **`Away_Club_Goals`** (`INT`)
  * `Stadium` $\rightarrow$ **`Stadium`** (`NVARCHAR(200)`)
