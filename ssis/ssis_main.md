# HƯỚNG DẪN CẤU HÌNH CONTROL FLOW MASTER PACKAGE: SSIS_MAIN

> **Package chính:** `Master_ETL_Pipeline.dtsx` (hoặc `Main.dtsx`)  
> **Mô hình kiến trúc:** **Master Control Flow Architecture** (Xâu chuỗi 5 Data Flow Task nạp Dimension và 1 Data Flow Task nạp Fact bằng Lookup Transformations).  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ TOÀN CẢNH CONTROL FLOW (MASTER ETL PIPELINE FLOWCHART)

```text
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Pre-ETL Cleanup     │
               │    (TRUNCATE TABLE dbo.FACT_Player...)  │
               └────────────────────┬────────────────────┘
                                    │ (Success)
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  Data Flow Task:     │ │  Data Flow Task:     │ │  Data Flow Task:     │
│  Load DIM_Competition│ │  Load DIM_Club       │ │  Load DIM_Time       │
│  (competitions.csv)  │ │  (clubs.csv)         │ │  (games/appearances) │
└───────────┬──────────┘ └──────────┬───────────┘ └──────────┬───────────┘
            │                       │                        │
            │                       ▼                        │
            │            ┌──────────────────────┐            │
            │            │  Data Flow Task:     │            │
            │            │  Load DIM_Player     │            │
            │            │  (players.csv)       │            │
            │            └──────────┬───────────┘            │
            │                       │                        │
            │                       ▼                        │
            │            ┌──────────────────────┐            │
            │            │  Data Flow Task:     │            │
            │            │  Load DIM_Game       │            │
            │            │  (games.csv)         │            │
            │            └──────────┬───────────┘            │
            │                       │                        │
            └───────────────────────┼────────────────────────┘
                                    │ (Tất cả 5 DIM hoàn tất Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Data Flow Task: Load FACT_Player_Match│
               │   Perf (Dùng 5 Khối Lookup Transformations)│
               │   Nguồn: appearances.csv                │
               └────────────────────┬────────────────────┘
                                    │ (Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Post-ETL Audit Log  │
               │   (Ghi nhận nhật ký hoàn tất nạp Kho)   │
               └─────────────────────────────────────────┘
```

---

## 2. CHI TIẾT QUY TRÌNH THỰC THI TRONG CONTROL FLOW

### Bước 1: Khởi tạo Dọn dẹp (`Execute SQL Task - Pre ETL Cleanup`)
* **Loại khối**: `Execute SQL Task`
* **Nhiệm vụ**: Xóa sạch dữ liệu cũ bảng Fact trước khi thực hiện luồng ETL mới để đảm bảo tính toàn vẹn dữ liệu.
* **SQLStatement**:
  ```sql
  USE DW_Football_Analytics;
  GO

  TRUNCATE TABLE dbo.FACT_Player_Match_Perf;
  GO
  ```

---

### Bước 2: Tiến trình Nạp Dữ liệu Chiều (Dimension Execution Phase - 5 Data Flow Tasks)

Dựa trên cấu hình chi tiết tại 5 tệp tài liệu SSIS Dimension trong thư mục `ssis/`:

1. **`DFT - Load DIM_Competition`** ([xem chi tiết ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md)):
   - **File nguồn:** `cleaned_competitions.csv`
   - **Bảng đích:** `[dbo].[DIM_Competition]`
   - **Luồng xử lý:** `Flat File Source` (4 cột) $\rightarrow$ `Data Conversion` (`dc_competition_id` WSTR 100, `dc_name` WSTR 200, `dc_country_name` WSTR 200, `dc_type` WSTR 100) $\rightarrow$ `Derived Column` (`der_country_name`, `der_competition_type`) $\rightarrow$ `Conditional Split` (Validation 4 cột) $\rightarrow$ `Sort` (Khử trùng theo `Competition_ID`) $\rightarrow$ `OLE DB Destination`.

2. **`DFT - Load DIM_Club`** ([xem chi tiết ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md)):
   - **File nguồn:** `cleaned_clubs.csv`
   - **Bảng đích:** `[dbo].[DIM_Club]`
   - **Luồng xử lý:** `Flat File Source` (6 cột) $\rightarrow$ `Data Conversion` (`dc_club_id` I4, `dc_club_name` WSTR 200, `dc_stadium_name` WSTR 200, `dc_stadium_seats` I4, `dc_coach_name` WSTR 200, `dc_squad_size` I4) $\rightarrow$ `Derived Column` (`der_stadium_name`, `der_coach_name`, `der_stadium_seats`) $\rightarrow$ `Conditional Split` (Validation 6 cột) $\rightarrow$ `Sort` (Khử trùng theo `Club_ID`) $\rightarrow$ `OLE DB Destination`.

3. **`DFT - Load DIM_Player`** ([xem chi tiết ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md)):
   - **File nguồn:** `cleaned_players.csv`
   - **Bảng đích:** `[dbo].[DIM_Player]`
   - **Luồng xử lý:** `Flat File Source` (8 cột) $\rightarrow$ `Data Conversion` (`dc_player_id` I4, `dc_player_name` WSTR 200, `dc_date_of_birth` WSTR 100, `dc_country` WSTR 200, `dc_main_position` WSTR 100, `dc_sub_position` WSTR 100, `dc_foot` WSTR 100, `dc_height_in_cm` I4) $\rightarrow$ `Derived Column` (`der_age`, `der_player_name`, `der_country`, `der_foot`, `der_height`) $\rightarrow$ `Conditional Split` (Validation 9 cột) $\rightarrow$ `Sort` (Khử trùng theo `Player_ID`) $\rightarrow$ `OLE DB Destination`.

4. **`DFT - Load DIM_Time`** ([xem chi tiết ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md)):
   - **File nguồn:** `games.csv` / `appearances.csv`
   - **Bảng đích:** `[dbo].[DIM_Time]`
   - **Luồng xử lý:** `Flat File Source` $\rightarrow$ `Data Conversion` (`dc_date` WSTR 100, `dc_season` WSTR 100) $\rightarrow$ `Derived Column` (Bóc tách `Time_ID` YYYYMMDD, `Full_Date`, `Day`, `Month`, `Quarter`, `Year`, `Day_Of_Week`, `Season`, `Is_Weekend`) $\rightarrow$ `Conditional Split` (Validation 9 cột) $\rightarrow$ `Sort` (Khử trùng theo `Time_ID`) $\rightarrow$ `OLE DB Destination`.

5. **`DFT - Load DIM_Game`** ([xem chi tiết ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md)):
   - **File nguồn:** `cleaned_games.csv`
   - **Bảng đích:** `[dbo].[DIM_Game]`
   - **Điều kiện nối (Precedence Constraint):** Nối đường màu xanh (`Success`) từ `DFT - Load DIM_Club` sang `DFT - Load DIM_Game`.
   - **Luồng xử lý:** `Flat File Source` (7 cột) $\rightarrow$ `Data Conversion` (`dc_game_id` I4, `dc_round` WSTR 100, `dc_home_club_id` I4, `dc_away_club_id` I4, `dc_home_club_goals` I4, `dc_away_club_goals` I4, `dc_stadium` WSTR 200) $\rightarrow$ `Derived Column` (`der_stadium`, `der_home_goals`, `der_away_goals`) $\rightarrow$ `Conditional Split` (Validation 7 cột) $\rightarrow$ `Sort` (Khử trùng theo `Game_ID`) $\rightarrow$ `OLE DB Destination`.

---

### Bước 3: Nạp Bảng Sự Kiện Trực Tiếp Qua Chuỗi Lookup (`DFT - Load FACT_Player_Match_Perf`)

Dựa trên cấu hình chi tiết tại tệp [ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md):

* **Loại khối:** `Data Flow Task`
* **File nguồn:** `appearances.csv` (1.89 triệu dòng)
* **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`
* **Điều kiện ràng buộc Control Flow (Precedence Constraints):**
  - Nối 5 đường mũi tên xanh (`Success`) từ **tất cả 5 Data Flow Task Dimension** (`DIM_Competition`, `DIM_Club`, `DIM_Player`, `DIM_Time`, `DIM_Game`) hội tụ về khối này.
  - Thiết lập **Logical AND**: Đảm bảo cả 5 bảng chiều đã nạp xong thành công 100% trước khi kích hoạt nạp Fact.
* **Luồng Data Flow 11 khối bên trong:**
  1. `Flat File Source (appearances.csv)` (11 cột).
  2. `Data Conversion`: Ép kiểu `dc_appearance_id` (WSTR 100), `dc_game_id` (I4), `dc_player_id` (I4), `dc_player_club_id` (I4), `dc_date_str` (WSTR 100), `dc_competition_id` (WSTR 100), `dc_goals` (I4), `dc_assists` (I4), `dc_minutes_played` (I4), `dc_yellow_cards` (I4), `dc_red_cards` (I4).
  3. `Derived Column - Prep Time ID`: Sinh cột `der_time_id` dạng số nguyên `YYYYMMDD` (`[DT_I4]`).
  4. `Conditional Split`: Validation kiểm tra toàn bộ 11 cột dữ liệu hợp lệ.
  5. `Lookup Player`: Tra cứu `dc_player_id` với `DIM_Player` lấy `lk_player_id`.
  6. `Lookup Club`: Tra cứu `dc_player_club_id` với `DIM_Club` lấy `lk_club_id`.
  7. `Lookup Competition`: Tra cứu `dc_competition_id` với `DIM_Competition` lấy `lk_competition_id`.
  8. `Lookup Time`: Tra cứu `der_time_id` với `DIM_Time` lấy `lk_time_id`.
  9. `Lookup Game Info`: Tra cứu `dc_game_id` với `DIM_Game` lấy `Home_Club_ID` (`lk_home_club_id`) và `Away_Club_ID` (`lk_away_club_id`).
  10. `Derived Column - Fact Measures`: Tính toán `Goal_Contributions`, `Is_Starter`, `Is_Home_Game`, `Opponent_Club_ID` và gán giá trị mặc định cho dữ liệu tra cứu NULL (`Player_ID_Final`, `Club_ID_Final`, `Competition_ID_Final`, `Time_ID_Final`).
  11. `OLE DB Destination`: Fast load 50.000 rows/batch vào `[dbo].[FACT_Player_Match_Perf]`.

---

### Bước 4: Nhật Ký Hậu Xử Lý (`Execute SQL Task - Post ETL Audit Log`)

* **Loại khối:** `Execute SQL Task`
* **Precedence Constraint:** Nối từ `DFT - Load FACT_Player_Match_Perf` (Success).
* **SQLStatement:**
  ```sql
  USE DW_Football_Analytics;
  GO

  INSERT INTO dbo.FACT_Player_Match_Perf_Error (Appearance_ID, Player_ID, Error_Reason, Error_Timestamp)
  VALUES ('AUDIT_LOG', 0, 'MASTER ETL PIPELINE COMPLETED SUCCESSFULLY', GETDATE());
  GO
  ```

---

## 3. TỔNG HỢP DANH MỤC TỆP HƯỚNG DẪN TRONG THƯ MỤC SSIS

| STT | Tên Tệp Hướng Dẫn | Loại Khối SSIS | Tệp Dữ Liệu Nguồn | Bảng Đích CSDL |
| :---: | :--- | :--- | :--- | :--- |
| 1 | [ssis_main.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_main.md) | **Control Flow Master** | - | Tiến trình Master Pipeline |
| 2 | [ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md) | Data Flow Task | `cleaned_competitions.csv` | `[dbo].[DIM_Competition]` |
| 3 | [ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md) | Data Flow Task | `cleaned_clubs.csv` | `[dbo].[DIM_Club]` |
| 4 | [ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md) | Data Flow Task | `cleaned_players.csv` | `[dbo].[DIM_Player]` |
| 5 | [ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md) | Data Flow Task | `games.csv` / `appearances.csv` | `[dbo].[DIM_Time]` |
| 6 | [ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md) | Data Flow Task | `cleaned_games.csv` | `[dbo].[DIM_Game]` |
| 7 | [ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md) | Data Flow Task | `appearances.csv` | `[dbo].[FACT_Player_Match_Perf]` |
