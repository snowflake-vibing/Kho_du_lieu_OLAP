# HƯỚNG DẪN CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCKS) TRONG DIM VÀ FACT (SSIS STAR SCHEMA)

> **Dự án**: Kho Dữ Liệu Phân Tích Bóng Đá (Football Analytics Data Warehouse)  
> **Database**: `DW_Football_Transfermarkt`  
> **Chuẩn độ dài áp dụng**: Chỉ dùng chuẩn **200** hoặc **100** cho toàn bộ các thuộc tính kiểu chuỗi (`NVARCHAR`/`VARCHAR`), đảm bảo **100% SẠCH WARNING**.

---

## MỤC LỤC
1. [Chuẩn Kiến Trúc Khối Trong Data Flow](#1-chuẩn-kiến-trúc-khối-trong-data-flow)
2. [Chi Tiết Cấu Hình Blocks Trong Bảng Chiều (DIM)](#2-chi-tiết-cấu-hình-blocks-trong-bảng-chiều-dim)
   - [2.1. DIM_Competition (Chiều Giải Đấu)](#21-dim_competition-chiều-giải-đấu)
   - [2.2. DIM_Club (Chiều Câu Lạc Bộ)](#22-dim_club-chiều-câu-lạc-bộ)
   - [2.3. DIM_Player (Chiều Cầu Thủ)](#23-dim_player-chiều-cầu-thủ)
   - [2.4. DIM_Game (Chiều Trận Đấu)](#24-dim_game-chiều-trận-đấu)
   - [2.5. DIM_Time (Chiều Thời Gian)](#25-dim_time-chiều-thời-gian)
3. [Chi Tiết Cấu Hình Khối Nạp Fact (FACT_Player_Match_Perf)](#3-chi-tiết-cấu-hình-khối-nạp-fact-fact_player_match_perf)
   - [3.1. Data Flow: Load Staging Appearances](#31-data-flow-load-staging-appearances)
   - [3.2. Execute SQL Task: Populate FACT via SQL Join](#32-execute-sql-task-populate-fact-via-sql-join)
4. [Quy Tắc Vàng Triệt Tiêu 100% Warning Trong SSIS](#4-quy-tắc-vàng-triệt-tiêu-100-warning-trong-ssis)

---

## 1. CHUẨN KIẾN TRÚC KHỐI TRONG DATA FLOW

Mỗi luồng dữ liệu Dimension (DIM) tuân thủ mô hình 5-6 khối tuần tự:

```
[Flat File Source] 
       │
       ▼
[Data Conversion]  ─── (Ép kiểu chuẩn DT_I4 hoặc DT_WSTR 100/200)
       │
       ▼
[Derived Column]   ─── (Tính toán cột phụ nếu có: Age, Date Key YYYYMMDD,...)
       │
       ▼
[Conditional Split] ─── (Validation dữ liệu tất cả các cột)
       │
       ▼ (Nhánh Valid_xxx)
[Sort]             ─── (Sắp xếp theo Business Key & Distinct loại bỏ trùng)
       │
       ▼
[OLE DB Destination] ── (Nạp dữ liệu vào bảng SQL Server Fast Load)
```

---

## 2. CHI TIẾT CẤU HÌNH BLOCKS TRONG BẢNG CHIỀU (DIM)

### 2.1. DIM_Competition (Chiều Giải Đấu)

#### 1. Khối `Flat File Source` (Đọc file `cleaned_competitions.csv`)
* **Connection Manager**: `FF_Competition` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Columns**: Chọn 4 cột: `competition_id`, `name`, `country_name`, `type`.
* **Output Column Length**: Đặt `200` cho tất cả các cột chuỗi.

#### 2. Khối `Data Conversion` (Ép kiểu dữ liệu)
| Cột Nguồn | Output Alias | Data Type | Length |
| :--- | :--- | :--- | :--- |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** |
| `name` | **`dc_name`** | Unicode string `[DT_WSTR]` | **200** |
| `country_name` | **`dc_country_name`** | Unicode string `[DT_WSTR]` | **200** |
| `type` | **`dc_type`** | Unicode string `[DT_WSTR]` | **100** |

#### 3. Khối `Conditional Split` (Validation dữ liệu)
* **Input Columns**: Đưa cả 4 cột `dc_competition_id`, `dc_name`, `dc_country_name`, `dc_type` vào Input.
* **Output Name**: `Valid_Competition`
* **Condition**:
  ```c
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 && 
  !ISNULL(dc_name) && LEN(TRIM(dc_name)) > 0 && 
  !ISNULL(dc_country_name) && LEN(TRIM(dc_country_name)) > 0 && 
  !ISNULL(dc_type) && LEN(TRIM(dc_type)) > 0
  ```

#### 4. Khối `Sort` (Khử trùng lặp)
* **Input Path**: Chọn nhánh **`Valid_Competition`**.
* **Pass Through**: Tick chọn cả 4 cột.
* **Sort Column**: Tick `dc_competition_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option**: Tick chọn **`Remove rows with duplicate sort values`**.

#### 5. Khối `OLE DB Destination` (Nạp SQL Server)
* **Table**: `[dbo].[DIM_Competition]`.
* **Mappings**: Ánh xạ 4 cột tương ứng vào bảng CSDL.

---

### 2.2. DIM_Club (Chiều Câu Lạc Bộ)

#### 1. Khối `Flat File Source` (Đọc file `cleaned_clubs.csv`)
* **Connection Manager**: `FF_Club`.
* **Columns**: Chọn 6 cột: `club_id`, `name`, `stadium_name`, `stadium_seats`, `coach_name`, `squad_size`.

#### 2. Khối `Data Conversion`
| Cột Nguồn | Output Alias | Data Type | Length |
| :--- | :--- | :--- | :--- |
| `club_id` | **`dc_club_id`** | `[DT_I4]` | - |
| `name` | **`dc_club_name`** | `[DT_WSTR]` | **200** |
| `stadium_name` | **`dc_stadium_name`** | `[DT_WSTR]` | **200** |
| `stadium_seats` | **`dc_stadium_seats`** | `[DT_I4]` | - |
| `coach_name` | **`dc_coach_name`** | `[DT_WSTR]` | **200** |
| `squad_size` | **`dc_squad_size`** | `[DT_I4]` | - |

#### 3. Khối `Conditional Split` (Validation kiểm tra TOÀN BỘ 6 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 6 CỘT vào Input.
* **Output Name**: `Valid_Club`
* **Condition**:
  ```c
  !ISNULL(dc_club_id) && dc_club_id > 0 && 
  !ISNULL(dc_club_name) && LEN(TRIM(dc_club_name)) > 0 && 
  !ISNULL(dc_stadium_name) && LEN(TRIM(dc_stadium_name)) > 0 && 
  !ISNULL(dc_stadium_seats) && dc_stadium_seats >= 0 && 
  !ISNULL(dc_coach_name) && LEN(TRIM(dc_coach_name)) > 0 && 
  !ISNULL(dc_squad_size) && dc_squad_size >= 0
  ```

#### 4. Khối `Sort`
* **Pass Through**: Tick chọn cả 6 cột (`dc_club_id`, `dc_club_name`, `dc_stadium_name`, `dc_stadium_seats`, `dc_coach_name`, `dc_squad_size`).
* **Sort Column**: Tick `dc_club_id` (Ascending) + **`Remove rows with duplicate sort values`**.

#### 5. Khối `OLE DB Destination`
* **Table**: `[dbo].[DIM_Club]`.

---

### 2.3. DIM_Player (Chiều Cầu Thủ)

#### 1. Khối `Flat File Source` (Đọc file `cleaned_players.csv`)
* **Connection Manager**: `FF_Player`.
* **Columns**: Chọn 8 cột: `player_id`, `name`, `date_of_birth`, `country_of_citizenship`, `position`, `sub_position`, `foot`, `height_in_cm`.

#### 2. Khối `Data Conversion`
| Cột Nguồn | Output Alias | Data Type | Length |
| :--- | :--- | :--- | :--- |
| `player_id` | **`dc_player_id`** | `[DT_I4]` | - |
| `name` | **`dc_name`** | `[DT_WSTR]` | **200** |
| `date_of_birth` | **`dc_date_of_birth`** | `[DT_WSTR]` | **100** |
| `country_of_citizenship` | **`dc_country_of_citizenship`** | `[DT_WSTR]` | **200** |
| `position` | **`dc_position`** | `[DT_WSTR]` | **100** |
| `sub_position` | **`dc_sub_position`** | `[DT_WSTR]` | **100** |
| `foot` | **`dc_foot`** | `[DT_WSTR]` | **100** |
| `height_in_cm` | **`dc_height_in_cm`** | `[DT_I4]` | - |

#### 3. Khối `Derived Column` (Tính tuổi `age`)
* **Expression**:
  ```c
  ISNULL(dc_date_of_birth) || LEN(TRIM(dc_date_of_birth)) == 0 ? 0 : DATEDIFF("yyyy", (DT_DBTIMESTAMP)dc_date_of_birth, GETDATE())
  ```

#### 4. Khối `Conditional Split` (Validation kiểm tra TOÀN BỘ 9 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 9 CỘT vào Input.
* **Output Name**: `Valid_Player`
* **Condition**:
  ```c
  !ISNULL(dc_player_id) && dc_player_id > 0 && 
  !ISNULL(dc_name) && LEN(TRIM(dc_name)) > 0 && 
  !ISNULL(dc_date_of_birth) && LEN(TRIM(dc_date_of_birth)) > 0 && 
  !ISNULL(age) && age >= 0 && 
  !ISNULL(dc_country_of_citizenship) && LEN(TRIM(dc_country_of_citizenship)) > 0 && 
  !ISNULL(dc_position) && LEN(TRIM(dc_position)) > 0 && 
  !ISNULL(dc_sub_position) && LEN(TRIM(dc_sub_position)) > 0 && 
  !ISNULL(dc_foot) && LEN(TRIM(dc_foot)) > 0 && 
  !ISNULL(dc_height_in_cm) && dc_height_in_cm > 0
  ```

#### 5. Khối `Sort`
* **Pass Through**: Tick chọn cả 9 cột + Sort `dc_player_id` (Ascending) + **`Remove rows with duplicate sort values`**.

#### 6. Khối `OLE DB Destination`
* **Table**: `[dbo].[DIM_Player]`.

---

### 2.4. DIM_Game (Chiều Trận Đấu)

#### 1. Khối `Flat File Source` (Đọc file `cleaned_games.csv`)
* **Connection Manager**: `FF_Game` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Columns**: Chọn đầy đủ **8 trường dữ liệu**:
  1. `game_id` (Mã trận đấu)
  2. `season` (Mùa giải: 2022, 2023...)
  3. `round` (Vòng đấu: Matchday 1, Final...)
  4. `home_club_id` (Mã CLB chủ nhà)
  5. `away_club_id` (Mã CLB khách)
  6. `home_club_goals` (Bàn thắng đội nhà)
  7. `away_club_goals` (Bàn thắng đội khách)
  8. `stadium` (Tên sân vận động)

#### 2. Khối `Data Conversion` (Ép kiểu dữ liệu chuẩn)
Ánh xạ chính xác 8 cột nguồn sang kiểu dữ liệu SSIS chuẩn:
| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu (Int) |
| `season` | **`dc_season`** | Four-byte signed integer `[DT_I4]` | - | Mùa giải (Int) |
| `round` | **`dc_round`** | Unicode string `[DT_WSTR]` | **100** | Vòng đấu (Nvarchar 100) |
| `home_club_id` | **`dc_home_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã CLB chủ nhà (Int) |
| `away_club_id` | **`dc_away_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã CLB khách (Int) |
| `home_club_goals` | **`dc_home_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội nhà (Int) |
| `away_club_goals` | **`dc_away_club_goals`** | Four-byte signed integer `[DT_I4]` | - | Bàn thắng đội khách (Int) |
| `stadium` | **`dc_stadium`** | Unicode string `[DT_WSTR]` | **200** | Tên SVĐ (Nvarchar 200) |

#### 3. Khối `Conditional Split` (Validation kiểm tra TOÀN BỘ 8 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 8 CỘT (`dc_game_id`, `dc_season`, `dc_round`, `dc_home_club_id`, `dc_away_club_id`, `dc_home_club_goals`, `dc_away_club_goals`, `dc_stadium`) vào Input.
* **Output Name**: `Valid_Game`
* **Condition (Kiểm tra đầy đủ 8 cột)**:
  ```c
  !ISNULL(dc_game_id) && dc_game_id > 0 && 
  !ISNULL(dc_season) && dc_season > 0 && 
  !ISNULL(dc_round) && LEN(TRIM(dc_round)) > 0 && 
  !ISNULL(dc_home_club_id) && dc_home_club_id > 0 && 
  !ISNULL(dc_away_club_id) && dc_away_club_id > 0 && 
  !ISNULL(dc_home_club_goals) && dc_home_club_goals >= 0 && 
  !ISNULL(dc_away_club_goals) && dc_away_club_goals >= 0 && 
  !ISNULL(dc_stadium) && LEN(TRIM(dc_stadium)) > 0
  ```
* **Default Output Name**: `Invalid_Game`

#### 4. Khối `Sort` (Khử trùng lặp theo Game_ID)
* **Input Path**: Nhánh **`Valid_Game`**.
* **Pass Through**: Tick chọn cả 8 cột (`dc_game_id`, `dc_season`, `dc_round`, `dc_home_club_id`, `dc_away_club_id`, `dc_home_club_goals`, `dc_away_club_goals`, `dc_stadium`).
* **Sort Column**: Tick chọn `dc_game_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option**: Tick chọn **`Remove rows with duplicate sort values`** (Đảm bảo mỗi trận đấu chỉ xuất hiện 1 dòng duy nhất trong DIM_Game).

#### 5. Khối `OLE DB Destination` (Nạp vào SQL Server)
* **Connection**: Kết nối OLE DB đến `DW_Football_Transfermarkt`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Game]`.
* **Mappings** (Ánh xạ 8 cột):
  * `dc_game_id` $\rightarrow$ **`Game_ID`** (int)
  * `dc_season` $\rightarrow$ **`Season`** (int)
  * `dc_round` $\rightarrow$ **`Round`** (nvarchar 100)
  * `dc_home_club_id` $\rightarrow$ **`Home_Club_ID`** (int)
  * `dc_away_club_id` $\rightarrow$ **`Away_Club_ID`** (int)
  * `dc_home_club_goals` $\rightarrow$ **`Home_Club_Goals`** (int)
  * `dc_away_club_goals` $\rightarrow$ **`Away_Club_Goals`** (int)
  * `dc_stadium` $\rightarrow$ **`Stadium`** (nvarchar 200)
  * *(Bỏ qua `Game_SK` vì đây là Surrogate Key tự tăng IDENTITY(1,1))*.

---

### 2.5. DIM_Time (Chiều Thời Gian)

#### 1. Khối `Flat File Source` (Đọc file `games.csv` / `cleaned_games.csv`)
* **Columns**: `date`, `season`.

#### 2. Khối `Data Conversion`
* `date` $\rightarrow$ `dc_date` (`[DT_WSTR]`, Length: **100**)
* `season` $\rightarrow$ `dc_season` (`[DT_WSTR]`, Length: **100**)

#### 3. Khối `Derived Column` (Bóc tách thuộc tính thời gian)
* **`Time_ID`** (`[DT_I4]`): `(YEAR((DT_DATE)dc_date) * 10000) + (MONTH((DT_DATE)dc_date) * 100) + DAY((DT_DATE)dc_date)` (Mã ngày YYYYMMDD).
* **`Full_Date`** (`[DT_WSTR]`, Length: **100**): `dc_date`
* **`Day`** (`[DT_I4]`): `DATEPART("dd", (DT_DBTIMESTAMP)dc_date)`
* **`Month`** (`[DT_I4]`): `DATEPART("mm", (DT_DBTIMESTAMP)dc_date)`
* **`Quarter`** (`[DT_I4]`): `DATEPART("qq", (DT_DBTIMESTAMP)dc_date)`
* **`Year`** (`[DT_I4]`): `DATEPART("yy", (DT_DBTIMESTAMP)dc_date)`
* **`Day_Of_Week`** (`[DT_WSTR]`, Length: **100**): Tên thứ trong tuần.
* **`Season`** (`[DT_WSTR]`, Length: **100**): `"Mùa " + dc_season`
* **`Is_Weekend`** (`[DT_I4]`): `DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 1 || DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 7 ? 1 : 0`

#### 4. Khối `Sort`
* Sort theo `Time_ID` (Ascending) + Tick chọn **`Remove rows with duplicate sort values`**.

#### 5. Khối `OLE DB Destination`
* **Table**: `[dbo].[DIM_Time]`.
* **Mappings**: Ánh xạ đầy đủ các thuộc tính ngày, tháng, năm vào `DIM_Time`.

---

## 3. CHI TIẾT CẤU HÌNH KHỐI NẠP FACT (FACT_Player_Match_Perf)

Để nạp **1.89 triệu dòng** dữ liệu Fact trong thời gian tối ưu **vài chục giây**, quy trình được chia thành 2 bước tối ưu:

### 3.1. Data Flow: Load Staging Appearances

Mục đích: Nạp thô cực nhanh từ file `appearances.csv` vào bảng tạm `STG_Appearances`.

```
[Flat File Source (appearances.csv)] ➔ [Data Conversion] ➔ [OLE DB Destination (STG_Appearances)]
```

#### 1. Khối `Flat File Source`
* **File**: `appearances.csv`.
* **Columns**: `appearance_id`, `game_id`, `player_id`, `player_club_id`, `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards`.

#### 2. Khối `Data Conversion`
* `appearance_id` $\rightarrow$ `dc_appearance_id` (`[DT_STR]`, Length: **100**)
* `game_id` $\rightarrow$ `dc_game_id` (`[DT_I4]`)
* `player_id` $\rightarrow$ `dc_player_id` (`[DT_I4]`)
* `player_club_id` $\rightarrow$ `dc_player_club_id` (`[DT_I4]`)
* Các chỉ số `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards` $\rightarrow$ (`[DT_I4]`).

#### 3. Khối `OLE DB Destination` (Cấu hình Fast Load tối ưu)
* **Table**: `[dbo].[STG_Appearances]`.
* **Data Access Mode**: `Table or view - fast load`.
* **Options Fast Load**:
  * Rows per batch: `50000`
  * Maximum insert commit size: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.

---

### 3.2. Execute SQL Task: Populate FACT via SQL Join

Mục đích: Sử dụng **SQL Server Engine (Set-based JOIN)** để liên kết bảng Staging với 5 bảng Dimension và nạp thẳng vào bảng Fact.

* **Task Type**: `Execute SQL Task` (đặt trên Control Flow sau bước nạp Staging).
* **Connection**: OLE DB Connection đến `DW_Football_Transfermarkt`.
* **SQLStatement**:

```sql
USE DW_Football_Transfermarkt;
GO

TRUNCATE TABLE dbo.FACT_Player_Match_Perf;

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
    ISNULL(p.Player_SK, 1) AS Player_SK,
    ISNULL(c.Club_SK, 1) AS Club_SK,
    ISNULL(c.Club_SK, 1) AS Opponent_Club_SK,
    ISNULL(comp.Competition_SK, 1) AS Competition_SK,
    ISNULL(g.Game_SK, 1) AS Game_SK,
    1 AS Time_SK,
    s.game_id,
    ISNULL(s.minutes_played, 0),
    ISNULL(s.goals, 0),
    ISNULL(s.assists, 0),
    (ISNULL(s.goals, 0) + ISNULL(s.assists, 0)) AS Goal_Contributions,
    ISNULL(s.yellow_cards, 0),
    ISNULL(s.red_cards, 0),
    CASE WHEN ISNULL(s.minutes_played, 0) >= 60 THEN 1 ELSE 0 END AS Is_Starter
FROM dbo.STG_Appearances s
LEFT JOIN dbo.DIM_Player p ON s.player_id = p.Player_ID
LEFT JOIN dbo.DIM_Club c ON s.player_club_id = c.Club_ID
LEFT JOIN dbo.DIM_Competition comp ON s.competition_id = comp.Competition_ID
LEFT JOIN dbo.DIM_Game g ON s.game_id = g.Game_ID;
```

---

## 4. QUY TẮC VÀNG TRIỆT TIÊU 100% WARNING TRONG SSIS

Để package SSIS hoàn toàn **SẠCH WARNING (0 tam giác vàng)**, hãy luôn ghi nhớ 3 nguyên tắc kỹ thuật sau:

1. **Đồng bộ độ dài 100% (Nguồn = Đích = 200 hoặc 100)**:
   * Độ dài chuỗi tại `Data Conversion` và `Sort` phải **bằng chính xác** độ dài cột `NVARCHAR` trong CSDL SQL Server (chỉ dùng duy nhất chuẩn **200** hoặc **100**).
2. **Đưa toàn bộ các cột vào Conditional Split Input**:
   * Khi dùng `Conditional Split`, phải tick chọn **tất cả các cột** của luồng dữ liệu vào danh sách `InputColumns` để dữ liệu chảy qua đúng passthrough stream, tránh lỗi đứt đoạn `LineageID`.
3. **Lưu toàn bộ Project (`Ctrl + Shift + S`)**:
   * Sau khi chỉnh sửa UI trên Visual Studio, luôn bấm **Save All** để Visual Studio ghi nhận cấu hình từ RAM xuống đĩa `.dtsx` và làm mới Cache Validation.
