# HƯỚNG DẪN CẤU HÌNH CONTROL FLOW MASTER PACKAGE: SSIS_MAIN (LUỒNG NẠP TRỰC TIẾP KHÔNG QUA STAGING)

> **Package chính:** `Master_ETL_Pipeline.dtsx` (hoặc `Main.dtsx`)  
> **Mô hình kiến trúc:** **Master Control Flow Architecture (Visual Studio SSIS)**  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Kiểu Khóa:** **Natural Keys (ID trực tiếp)** - Không sử dụng Surrogate Keys (`*_SK`).  
> **Phương pháp nạp:** **Nạp trực tiếp từ CSV vào Data Warehouse (Bỏ qua các bảng đệm Staging `STG_*`)** để tối ưu dung lượng đệm và tăng tốc độ xử lý gấp 2 lần.  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ QUY TRÌNH TOÀN CẢNH CONTROL FLOW (MASTER ETL FLOWCHART)

```text
               ┌─────────────────────────────────────────┐
               │    Execute SQL Task: Drop All Tables    │
               │   (Xóa bảng Fact trước, xóa 5 Dim sau)  │
               └────────────────────┬────────────────────┘
                                    │ (Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Create All Tables   │
               │  (Tạo lại cấu trúc 6 bảng với Natural PK/FK) │
               └────────────────────┬────────────────────┘
                                    │ (Success)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            SEQUENCE CONTAINER: LOAD DIMENSIONS (CHẠY 5 DIM)            │
│                                                                        │
│ ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────┐ │
│ │  Data Flow Task:     │   │  Data Flow Task:     │   │Data Flow Task│ │
│ │  Load DIM_Competition│   │  Load DIM_Club       │   │Load DIM_Time │ │
│ └──────────┬───────────┘   └──────────┬───────────┘   ──────┬───────┘ │
│            │                          │                      │         │
│            │                          ▼                      │         │
│            │               ┌──────────────────────┐          │         │
│            │               │  Data Flow Task:     │          │         │
│            │               │  Load DIM_Player     │          │         │
│            │               └──────────┬───────────┘          │         │
│            │                          │                      │         │
│            │                          ▼                      │         │
│            │               ┌──────────────────────┐          │         │
│            │               │  Data Flow Task:     │          │         │
│            │               │  Load DIM_Game       │          │         │
│            │               └──────────┬───────────┘          │         │
│            │                          │                      │         │
│            └──────────────────────────┼──────────────────────┘         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │ Data Flow Task: Load Fact Direct CSV    │
               │ (Nạp trực tiếp appearances.csv -> Fact) │
               └─────────────────────────────────────────┘
```

---

## 2. CHI TIẾT CÁC BƯỚC CẤU HÌNH TRONG CONTROL FLOW

### Bước 1: Khối `Execute SQL Task: Drop All Tables`
* **Loại khối**: `Execute SQL Task`
* **Mục đích**: Xóa sạch toàn bộ các bảng trong CSDL theo đúng thứ tự tham chiếu ràng buộc Khóa ngoại (xóa bảng Fact trước, xóa 5 bảng Dimension sau) để chuẩn bị cho chu trình nạp mới.
* **SQLStatement**:
  ```sql
  USE DW_Football_Analytics; -- Hoặc DW_Football_Transfermarkt
  GO

  -- 1. Xóa các VIEWS trước
  IF OBJECT_ID('dbo.v_FACT_Player_Match_Perf', 'V') IS NOT NULL DROP VIEW dbo.v_FACT_Player_Match_Perf;
  IF OBJECT_ID('dbo.v_DIM_Competition', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Competition;
  IF OBJECT_ID('dbo.v_DIM_Club', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Club;
  IF OBJECT_ID('dbo.v_DIM_Player', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Player;
  IF OBJECT_ID('dbo.v_DIM_Time', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Time;

  -- 2. Xóa các ràng buộc khóa ngoại (Foreign Keys)
  EXEC sp_msforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';

  -- 3. Xóa bảng Fact trước
  IF OBJECT_ID('dbo.FACT_Player_Match_Perf', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf;
  IF OBJECT_ID('dbo.FACT_Player_Match_Perf_Error', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf_Error;

  -- 4. Xóa 5 bảng Dimension sau
  IF OBJECT_ID('dbo.DIM_Game', 'U') IS NOT NULL DROP TABLE dbo.DIM_Game;
  IF OBJECT_ID('dbo.DIM_Player', 'U') IS NOT NULL DROP TABLE dbo.DIM_Player;
  IF OBJECT_ID('dbo.DIM_Club', 'U') IS NOT NULL DROP TABLE dbo.DIM_Club;
  IF OBJECT_ID('dbo.DIM_Competition', 'U') IS NOT NULL DROP TABLE dbo.DIM_Competition;
  IF OBJECT_ID('dbo.DIM_Time', 'U') IS NOT NULL DROP TABLE dbo.DIM_Time;
  GO
  ```

---

### Bước 2: Khối `Execute SQL Task: Create All Tables`
* **Loại khối**: `Execute SQL Task`
* **Precedence Constraint**: Nối từ `Drop All Tables` (Success).
* **Mục đích**: Khởi tạo lại toàn bộ cấu trúc CSDL kho dữ liệu OLAP (bao gồm 5 bảng Dimension và bảng Fact) sử dụng Natural Keys (ID trực tiếp) với đầy đủ các thuộc tính, kiểu dữ liệu và ràng buộc Khóa chính (PK), Khóa ngoại (FK).
* **SQLStatement**:
  ```sql
  USE DW_Football_Analytics; -- Hoặc DW_Football_Transfermarkt
  GO

  -- 1. Bảng DIM_Competition
  CREATE TABLE dbo.DIM_Competition (
      Competition_ID NVARCHAR(100) CONSTRAINT PK_DIM_Competition PRIMARY KEY,
      Competition_Name NVARCHAR(200) NULL,
      Country_Name NVARCHAR(200) NULL,
      Competition_Type NVARCHAR(100) NULL
  );

  -- 2. Bảng DIM_Club
  CREATE TABLE dbo.DIM_Club (
      Club_ID INT CONSTRAINT PK_DIM_Club PRIMARY KEY,
      Club_Name NVARCHAR(200) NULL,
      Stadium_Name NVARCHAR(200) NULL,
      Stadium_Seats INT NULL,
      Coach_Name NVARCHAR(200) NULL,
      Squad_Size INT NULL
  );

  -- 3. Bảng DIM_Player
  CREATE TABLE dbo.DIM_Player (
      Player_ID INT CONSTRAINT PK_DIM_Player PRIMARY KEY,
      Player_Name NVARCHAR(200) NULL,
      Date_Of_Birth NVARCHAR(100) NULL,
      Age INT NULL,
      Country_Of_Citizenship NVARCHAR(200) NULL,
      Main_Position NVARCHAR(100) NULL,
      Sub_Position NVARCHAR(100) NULL,
      Foot NVARCHAR(100) NULL,
      Height_In_Cm INT NULL
  );

  -- 4. Bảng DIM_Game
  CREATE TABLE dbo.DIM_Game (
      Game_ID INT CONSTRAINT PK_DIM_Game PRIMARY KEY,
      Round NVARCHAR(100) NULL,
      Home_Club_ID INT NULL,
      Away_Club_ID INT NULL,
      Home_Club_Goals INT NULL,
      Away_Club_Goals INT NULL,
      Stadium NVARCHAR(200) NULL
  );

  -- 5. Bảng DIM_Time
  CREATE TABLE dbo.DIM_Time (
      Time_ID INT CONSTRAINT PK_DIM_Time PRIMARY KEY,
      Full_Date NVARCHAR(100) NULL,
      Day_Of_Week NVARCHAR(100) NULL,
      Day INT NULL,
      Month INT NULL,
      Quarter INT NULL,
      Year INT NULL,
      Season NVARCHAR(100) NULL,
      Is_Weekend INT NULL
  );

  -- 6. Bảng FACT_Player_Match_Perf (Natural Foreign Keys: Player_ID, Club_ID, Competition_ID, Game_ID, Time_ID)
  CREATE TABLE dbo.FACT_Player_Match_Perf (
      Appearance_ID INT IDENTITY(1,1) CONSTRAINT PK_FACT_Player_Match_Perf PRIMARY KEY,
      Player_ID INT NOT NULL,
      Club_ID INT NOT NULL,
      Opponent_Club_ID INT NULL,
      Competition_ID NVARCHAR(100) NOT NULL,
      Game_ID INT NOT NULL,
      Time_ID INT NOT NULL,
      Minutes_Played INT DEFAULT 0,
      Goals INT DEFAULT 0,
      Assists INT DEFAULT 0,
      Goal_Contributions INT DEFAULT 0,
      Yellow_Cards INT DEFAULT 0,
      Red_Cards INT DEFAULT 0,
      Is_Starter INT DEFAULT 0,
      Is_Home_Game INT DEFAULT 0,

      CONSTRAINT FK_Fact_Player FOREIGN KEY (Player_ID) REFERENCES dbo.DIM_Player(Player_ID),
      CONSTRAINT FK_Fact_Club FOREIGN KEY (Club_ID) REFERENCES dbo.DIM_Club(Club_ID),
      CONSTRAINT FK_Fact_Competition FOREIGN KEY (Competition_ID) REFERENCES dbo.DIM_Competition(Competition_ID),
      CONSTRAINT FK_Fact_Game FOREIGN KEY (Game_ID) REFERENCES dbo.DIM_Game(Game_ID),
      CONSTRAINT FK_Fact_Time FOREIGN KEY (Time_ID) REFERENCES dbo.DIM_Time(Time_ID)
  );

  -- 7. Bảng FACT_Player_Match_Perf_Error
  CREATE TABLE dbo.FACT_Player_Match_Perf_Error (
      Error_ID INT IDENTITY(1,1) PRIMARY KEY,
      Appearance_ID VARCHAR(100),
      Player_ID INT,
      Club_ID INT,
      Competition_ID NVARCHAR(100),
      Game_ID INT,
      Time_ID INT,
      Error_Reason NVARCHAR(500),
      Error_Timestamp DATETIME DEFAULT GETDATE()
  );
  GO

  -- 8. Tạo Views hỗ trợ truy vấn (v_*)
  CREATE VIEW dbo.v_DIM_Competition AS SELECT Competition_ID, Competition_Name, Country_Name, Competition_Type FROM dbo.DIM_Competition;
  CREATE VIEW dbo.v_DIM_Club AS SELECT Club_ID, Club_Name, Stadium_Name, Stadium_Seats, Coach_Name, Squad_Size FROM dbo.DIM_Club;
  CREATE VIEW dbo.v_DIM_Player AS SELECT Player_ID, Player_Name, Date_Of_Birth, Age, Country_Of_Citizenship, Main_Position, Sub_Position, Foot, Height_In_Cm FROM dbo.DIM_Player;
  CREATE VIEW dbo.v_DIM_Time AS SELECT Time_ID, Full_Date, Day_Of_Week, Day, Month, Quarter, Year, Season, Is_Weekend FROM dbo.DIM_Time;
  CREATE VIEW dbo.v_FACT_Player_Match_Perf AS SELECT Appearance_ID, Player_ID, Club_ID, Opponent_Club_ID, Competition_ID, Game_ID, Time_ID, Minutes_Played, Goals, Assists, Goal_Contributions, Yellow_Cards, Red_Cards, Is_Starter, Is_Home_Game FROM dbo.FACT_Player_Match_Perf;
  GO
  ```

---

### Bước 3: Khối `Sequence Container: Load Dimensions` (Chứa 5 Data Flow Tasks)
* **Loại khối**: `Sequence Container`
* **Precedence Constraint**: Nối từ `Create All Tables` (Success).
* **Mục đích**: Nhóm 5 tiến trình Data Flow Task nạp dữ liệu vào 5 bảng Dimension thành một cụm thực thi tập trung:

1. **`DFT - Load DIM_Competition`**: Đọc `competitions.csv` $\rightarrow$ Nạp vào `dbo.DIM_Competition` ([Chi tiết ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md)).
2. **`DFT - Load DIM_Club`**: Đọc `clubs.csv` $\rightarrow$ Nạp vào `dbo.DIM_Club` ([Chi tiết ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md)).
3. **`DFT - Load DIM_Player`**: Đọc `players.csv` $\rightarrow$ Nạp vào `dbo.DIM_Player` ([Chi tiết ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md)).
4. **`DFT - Load DIM_Time`**: Đọc `games.csv` / `appearances.csv` $\rightarrow$ Nạp vào `dbo.DIM_Time` ([Chi tiết ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md)).
5. **`DFT - Load DIM_Game`**: Đọc `games.csv` $\rightarrow$ Nạp vào `dbo.DIM_Game` ([Chi tiết ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md)).

---

### Bước 4: Khối `Data Flow Task: Load Fact Direct CSV` (`FACT_Player_Match_Perf`)
* **Loại khối**: `Data Flow Task` (`Load Fact`)
* **Precedence Constraint**: Nối từ **`Sequence Container: Load Dimensions`** (Success).
* **Mục đích**: Đọc TRỰC TIẾP từ `appearances.csv` (không qua bảng Staging), nạp vào `dbo.FACT_Player_Match_Perf` qua chuỗi 9 khối tối ưu (Data Conversion, Validation, Lookup Player, Lookup Club, Lookup Competition, Lookup Game Info, 1 Derived Column duy nhất tính `Time_ID`, `Is_Starter`, `Is_Home_Game`, `Opponent_Club_ID`, và OLE DB Destination Fast Load) ([Chi tiết ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md)).

---

## 3. DANH MỤC CÁC TỆP HƯỚNG DẪN TRONG HỆ THỐNG SSIS

| STT | Tên Tệp Hướng Dẫn | Thành Phần Control / Data Flow | Nhiệm Vụ SSIS |
| :---: | :--- | :--- | :--- |
| 1 | [ssis_main.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_main.md) | **Control Flow Master** | `Drop All Tables` $\rightarrow$ `Create All Tables` $\rightarrow$ `Sequence Container (5 DIMs)` $\rightarrow$ `Load Fact Direct CSV` |
| 2 | [ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md) | Data Flow Task | Nạp `dbo.DIM_Competition` từ `competitions.csv` |
| 3 | [ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md) | Data Flow Task | Nạp `dbo.DIM_Club` từ `clubs.csv` |
| 4 | [ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md) | Data Flow Task | Nạp `dbo.DIM_Player` từ `players.csv` |
| 5 | [ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md) | Data Flow Task | Nạp `dbo.DIM_Time` từ `games.csv` / `appearances.csv` |
| 6 | [ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md) | Data Flow Task | Nạp `dbo.DIM_Game` từ `games.csv` |
| 7 | [ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md) | Data Flow Task | Nạp `dbo.FACT_Player_Match_Perf` trực tiếp từ `appearances.csv` qua Luồng Tối Ưu 9 Khối |
| 8 | [ssis_stg_appearances.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_stg_appearances.md) | Data Flow Task | *(Tùy chọn/Đã bỏ qua)* Nạp Staging đệm |
