# BẢNG MA TRẬN ĐỐI CHIẾU 3 CHIỀU: DATA CLEANED CSV ↔ SSIS ETL BLOCKS ↔ DW SCHEMA DOCS

Tài liệu này cung cấp **Bảng ma trận đối chiếu 3 chiều (3-Way Cross-Checking Matrix)** kiểm tra tính đồng bộ và chính xác 100% giữa 3 lớp dữ liệu trong hệ thống Kho dữ liệu bóng đá `DW_Football_Analytics`:
1. **Lớp Dữ liệu Sạch nguồn (Data Cleaned CSV):** Thư mục `data/` (`cleaned_players.csv`, `cleaned_clubs.csv`, `cleaned_competitions.csv`, `cleaned_games.csv`, `cleaned_appearances.csv`).
2. **Lớp Biến đổi SSIS ETL (SSIS Blocks):** Thư mục `ssis/` (`ssis_dim_player.md`, `ssis_dim_club.md`, `ssis_dim_competition.md`, `ssis_dim_game.md`, `ssis_dim_time.md`, `ssis_fact_player_match_perf.md`).
3. **Lớp Kiến trúc Kho dữ liệu (DW Schema Docs):** Thư mục `docs/` (`dim_player.md`, `dim_club.md`, `dim_competition.md`, `dim_game.md`, `dim_time.md`, `fact_player_match_perf.md`).

> **Chuẩn hóa Kiểu dữ liệu Chuỗi (String Standard):** 100% thuộc tính kiểu chuỗi ký tự trên toàn hệ thống áp dụng nghiêm ngặt duy nhất 1 trong 2 chuẩn độ dài: **`NVARCHAR(100)`** hoặc **`NVARCHAR(200)`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), triệt tiêu 100% Warning trong SSIS.

---

## 1. BẢNG CHIỀU: DIM_PLAYER (CẦU THỦ)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_players.csv`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_dim_player.md`) | Thuộc tính trong DW Table Docs (`docs/dim_player.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `player_id` | `int` (VD: `10`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Sort` (Asc 1, Unique) $\rightarrow$ `OLE DB Dest` | `Player_ID` | `INT (BK)` | ✅ Khớp 100% |
| 2 | `name` | `string` (VD: `Lionel Messi`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived Column` (TRIM) | `Player_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 3 | `date_of_birth` | `string` (VD: `1987-06-24`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ Ép định dạng `YYYY-MM-DD` | `Date_Of_Birth` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 4 | *(Derived từ `date_of_birth`)* | - | `Derived Column`: `DATEDIFF("yy", date_of_birth, GETDATE())` | `Age` | `INT` | ✅ Khớp 100% |
| 5 | `country_of_citizenship` | `string` (VD: `Argentina`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived` (replace NULL = 'Unknown') | `Country_Of_Citizenship` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 6 | `position` | `string` (VD: `Attack`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ Chuẩn hóa 4 nhóm chính | `Main_Position` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 7 | `sub_position` | `string` (VD: `Right Winger`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ Position chi tiết | `Sub_Position` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 8 | `foot` | `string` (VD: `Left`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ `Derived` (replace NULL = 'Unknown') | `Foot` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 9 | `height_in_cm` | `int` (VD: `170`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Derived` (gán 175 nếu NULL/ngoài lề) | `Height_In_Cm` | `INT` | ✅ Khớp 100% |

---

## 2. BẢNG CHIỀU: DIM_CLUB (CÂU LẠC BỘ)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_clubs.csv`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_dim_club.md`) | Thuộc tính trong DW Table Docs (`docs/dim_club.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `club_id` | `int` (VD: `418`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Sort` (Asc 1, Unique) $\rightarrow$ `OLE DB Dest` | `Club_ID` | `INT (BK)` | ✅ Khớp 100% |
| 2 | `name` | `string` (VD: `Real Madrid`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived Column` (TRIM) | `Club_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 3 | `stadium_name` | `string` (VD: `Santiago Bernabéu`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived` (NULL = 'Unknown Stadium') | `Stadium_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 4 | `stadium_seats` | `int` (VD: `81044`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Derived Column` (NULL = 0) | `Stadium_Seats` | `INT` | ✅ Khớp 100% |
| 5 | `coach_name` | `string` (VD: `Carlo Ancelotti`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived` (NULL = 'Unknown Coach') | `Coach_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 6 | `squad_size` | `int` (VD: `25`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Conditional Split` (CHECK >= 0) | `Squad_Size` | `INT` | ✅ Khớp 100% |

---

## 3. BẢNG CHIỀU: DIM_COMPETITION (GIẢI ĐẤU)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_competitions.csv`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_dim_competition.md`) | Thuộc tính trong DW Table Docs (`docs/dim_competition.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `competition_id` | `string` (VD: `GB1`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ `Sort` (Asc 1, Unique) | `Competition_ID` | `NVARCHAR(100) (BK)` | ✅ Khớp 100% |
| 2 | `name` | `string` (VD: `Premier League`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived Column` (TRIM) | `Competition_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 3 | `country_name` | `string` (VD: `England`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived Column` (NULL = 'Europe') | `Country_Name` | `NVARCHAR(200)` | ✅ Khớp 100% |
| 4 | `type` | `string` (VD: `domestic_league`)| `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ Standardize `type` | `Competition_Type` | `NVARCHAR(100)` | ✅ Khớp 100% |

---

## 4. BẢNG CHIỀU: DIM_GAME (TRẬN ĐẤU)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_games.csv`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_dim_game.md`) | Thuộc tính trong DW Table Docs (`docs/dim_game.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `game_id` | `int` (VD: `2212345`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Sort` (Asc 1, Unique) | `Game_ID` | `INT (BK)` | ✅ Khớp 100% |
| 2 | `round` | `string` (VD: `Matchday 1`) | `Data Conversion` (`DT_WSTR, 100`) $\rightarrow$ `Derived Column` (TRIM) | `Round` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 3 | `home_club_id` | `int` (VD: `418`) | `Data Conversion` (`DT_I4`) $\rightarrow$ Mã CLB chủ nhà | `Home_Club_ID` | `INT` | ✅ Khớp 100% |
| 4 | `away_club_id` | `int` (VD: `131`) | `Data Conversion` (`DT_I4`) $\rightarrow$ Mã CLB khách | `Away_Club_ID` | `INT` | ✅ Khớp 100% |
| 5 | `home_club_goals` | `int` (VD: `3`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Derived Column` (NULL = 0) | `Home_Club_Goals` | `INT` | ✅ Khớp 100% |
| 6 | `away_club_goals` | `int` (VD: `1`) | `Data Conversion` (`DT_I4`) $\rightarrow$ `Derived Column` (NULL = 0) | `Away_Club_Goals` | `INT` | ✅ Khớp 100% |
| 7 | `stadium` | `string` (VD: `Camp Nou`) | `Data Conversion` (`DT_WSTR, 200`) $\rightarrow$ `Derived` (NULL = 'Unknown Stadium') | `Stadium` | `NVARCHAR(200)` | ✅ Khớp 100% |

---

## 5. BẢNG CHIỀU: DIM_TIME (THỜI GIAN)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_games.csv` / `date`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_dim_time.md`) | Thuộc tính trong DW Table Docs (`docs/dim_time.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `date` (Derived YYYYMMDD)| `string` (VD: `2023-09-24`) | `Derived Column`: `YEAR*10000 + MONTH*100 + DAY` | `Time_ID` | `INT (BK)` | ✅ Khớp 100% |
| 2 | `date` | `string` (VD: `2023-09-24`) | `Data Conversion` (`DT_WSTR, 100`) | `Full_Date` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 3 | `date` (Derived Day_Of_Week)| `string` | `Derived Column`: `DATENAME(dw, date)` | `Day_Of_Week` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 4 | `date` (Derived Day) | `string` | `Derived Column`: `DATEPART("dd", date)` | `Day` | `INT` | ✅ Khớp 100% |
| 5 | `date` (Derived Month) | `string` | `Derived Column`: `DATEPART("mm", date)` | `Month` | `INT` | ✅ Khớp 100% |
| 6 | `date` (Derived Quarter)| `string` | `Derived Column`: `DATEPART("qq", date)` | `Quarter` | `INT` | ✅ Khớp 100% |
| 7 | `date` (Derived Year) | `string` | `Derived Column`: `DATEPART("yy", date)` | `Year` | `INT` | ✅ Khớp 100% |
| 8 | `season` | `string` (VD: `2023`) | `Derived Column`: `"Mùa " + season` | `Season` | `NVARCHAR(100)` | ✅ Khớp 100% |
| 9 | `date` (Derived Is_Weekend)| `string` | `Derived Column`: `dw == 1 \|\| dw == 7 ? 1 : 0` | `Is_Weekend` | `INT` | ✅ Khớp 100% |

---

## 6. BẢNG SỰ KIỆN: FACT_PLAYER_MATCH_PERF (LƯỢT RA SÂN)

| STT | Cột trong Data Cleaned CSV (`data/cleaned_appearances.csv`) | Kiểu dữ liệu CSV & Ví dụ | Khối xử lý SSIS ETL (`ssis/ssis_fact_player_match_perf.md`) | Thuộc tính trong DW Table Docs (`docs/fact_player_match_perf.md`) | Kiểu dữ liệu DW | Trạng thái Đối chiếu |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `player_id` | `int` (VD: `10`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Player` | `Player_SK` | `INT (FK)` | ✅ Khớp 100% |
| 2 | `player_club_id` | `int` (VD: `418`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Club` | `Club_SK` | `INT (FK)` | ✅ Khớp 100% |
| 3 | `opponent_id` | `int` (VD: `131`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Club` | `Opponent_Club_SK` | `INT (FK)` | ✅ Khớp 100% |
| 4 | `competition_id` | `string` (VD: `GB1`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Competition` | `Competition_SK` | `INT (FK)` | ✅ Khớp 100% |
| 5 | `game_id` | `int` (VD: `2212345`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Game` | `Game_SK` | `INT (FK)` | ✅ Khớp 100% |
| 6 | `date` | `string` (VD: `2023-09-24`) | `Data Conversion` $\rightarrow$ `Execute SQL Task` JOIN `DIM_Time` | `Time_SK` | `INT (FK)` | ✅ Khớp 100% |
| 7 | `game_id` | `int` (VD: `2212345`) | `Data Conversion` (`DT_I4`) | `Game_ID` | `INT (BK)` | ✅ Khớp 100% |
| 8 | `minutes_played` | `int` (VD: `90`) | `Data Conversion` (`DT_I4`) $\rightarrow$ NULL = 0 | `Minutes_Played` | `INT` | ✅ Khớp 100% |
| 9 | `goals` | `int` (VD: `2`) | `Data Conversion` (`DT_I4`) $\rightarrow$ NULL = 0 | `Goals` | `INT` | ✅ Khớp 100% |
| 10 | `assists` | `int` (VD: `1`) | `Data Conversion` (`DT_I4`) $\rightarrow$ NULL = 0 | `Assists` | `INT` | ✅ Khớp 100% |
| 11 | *(Derived)* | - | `Derived Column` / SQL: `goals + assists` | `Goal_Contributions` | `INT` | ✅ Khớp 100% |
| 12 | `yellow_cards` | `int` (VD: `0`) | `Data Conversion` (`DT_I4`) $\rightarrow$ NULL = 0 | `Yellow_Cards` | `INT` | ✅ Khớp 100% |
| 13 | `red_cards` | `int` (VD: `0`) | `Data Conversion` (`DT_I4`) $\rightarrow$ NULL = 0 | `Red_Cards` | `INT` | ✅ Khớp 100% |
| 14 | `minutes_played` | `int` (VD: `90`) | SQL CASE: `minutes_played >= 45 ? 1 : 0` | `Is_Starter` | `INT (Flag)` | ✅ Khớp 100% |
