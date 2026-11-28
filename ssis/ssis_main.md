# HƯỚNG DẪN CẤU HÌNH CONTROL FLOW MASTER PACKAGE: SSIS_MAIN

> **Package chính:** `Package.dtsx` (Visual Studio 2022 - mẫu *Integration Services Project*)  
> **Cơ sở dữ liệu đích:** `DW_Football_Transfermarkt`  
> **OLE DB Connection Manager:** `CM_DW_Football`  
> **Thư mục nguồn CSV:** `football/cleaned_data/ssis_input` (khai báo qua Package Parameter `InputFolder`)  
> **Phương pháp nạp:** Nạp trực tiếp từ 6 tệp CSV sau tiền xử lý vào 6 bảng kho (không qua bảng Staging `STG_*`), giữ nguyên `NULL` và chuyển toàn bộ dòng lỗi/không khớp khóa tham chiếu sang nhánh ghi lỗi.

---

## 1. NGUỒN DỮ LIỆU ĐẦU VÀO VÀ THAM SỐ PACKAGE

### 1.1. Danh sách 6 tệp CSV đầu vào (`ssis_input`)

Xuất từ `pre_processing.ipynb` sau khi lọc 13 giải đấu và 2 mùa `2022`, `2023` (đặt `EXPORT_FILES = True`) vào thư mục `football/cleaned_data/ssis_input`:

| Tệp đầu vào | Số dòng | Số cột | Vai trò |
| :--- | :---: | :---: | :--- |
| `cleaned_competitions.csv` | 13 | 4 | Danh mục giải đấu |
| `cleaned_clubs.csv` | 247 | 6 | Hồ sơ CLB có sẵn |
| `cleaned_players.csv` | 7.069 | 8 | Hồ sơ cầu thủ |
| `cleaned_games.csv` | 7.280 | 14 | Trận đấu và nguồn bổ sung CLB |
| `cleaned_time.csv` | 7.280 | 1 | Một giá trị ngày cho mỗi trận |
| `cleaned_appearances.csv` | 210.747 | 11 | Lượt ra sân |

### 1.2. Khai báo tham số `InputFolder` và nguyên tắc đọc Flat File

- Trong tab **Parameters** của `Package.dtsx`, tạo tham số chuỗi **`InputFolder`** trỏ tới thư mục `ssis_input`.
- Với mỗi Flat File Connection Manager (`FF_Competition`, `FF_Club`, `FF_Player`, `FF_Game`, `FF_Time`, `FF_Appearances`), cấu hình **Expressions → ConnectionString** bằng tham số `InputFolder` ghép với dấu phân cách đường dẫn và tên CSV tương ứng (dùng một đường dẫn mẫu hợp lệ khi thiết lập metadata và Preview).
- **Quy tắc chung cho tất cả Flat File Source**:
  - Định dạng `Delimited`, Code page `65001 (UTF-8)`, Text qualifier `"`, bật **Column names in the first data row**, phân cách cột `{Comma}`, dòng `{CR}{LF}`.
  - Khai báo kiểu dữ liệu và độ rộng chuỗi trực tiếp trong **Flat File Connection Manager → Advanced** (không dùng khối `Data Conversion`, giữ nguyên tên cột CSV).
  - Trong **Flat File Source Editor**, bật **Retain null values from the source as null values in the data flow**; vào **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát và nối đầu ra lỗi sang nhánh ghi lỗi của luồng.

---

## 2. SƠ ĐỒ QUY TRÌNH CONTROL FLOW

Trong chế độ nạp lại toàn phần, Control Flow thực thi tuần tự các tác vụ sau (khi khởi tạo trên CSDL trống có thể bắt đầu từ `Create All Tables`; khi giữ dữ liệu đã nạp, bỏ qua hai bước xóa/tạo bảng và chạy theo chế độ ở Mục 4):

```text
               ┌─────────────────────────────────────────┐
               │    Execute SQL Task: Drop All Tables    │
               │     (Xóa 6 bảng theo thứ tự khóa ngoại) │
               └────────────────────┬────────────────────┘
                                    │ Constraint: Success
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Create All Tables   │
               │ (Tạo 6 bảng trong 1 transaction từ DDL) │
               └────────────────────┬────────────────────┘
                                    │ Constraint: Success
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    SEQUENCE CONTAINER: Load Dimensions                  │
│                                                                         │
│  ┌─────────────────────┐  ┌─────────────────────┐                       │
│  │ Data Flow Task:     │  │ Data Flow Task:     │                       │
│  │ DIM_Club            │  │ DIM_Competition     │  ┌─────────────────┐  │
│  │ (+ bổ sung 25 CLB   │  └──────────┬──────────┘  │ Data Flow Task: │  │
│  │  nếu tách tác vụ)   │             │             │ DIM_Player      │  │
│  └──────────┬──────────┘             │             └─────────────────┘  │
│             │ (Success)              │ (Success)   ┌─────────────────┐  │
│             └───────────► Logical AND ◄─────────── │ Data Flow Task: │  │
│                               │                    │ DIM_Time        │  │
│                               ▼                    └─────────────────┘  │
│                    ┌─────────────────────┐                              │
│                    │ Data Flow Task:     │                              │
│                    │ DIM_Game            │                              │
│                    └─────────────────────┘                              │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ Constraint: Success
                                    ▼
               ┌─────────────────────────────────────────┐
               │  Data Flow Task: FACT_Player_Match_Perf │
               │  (Đọc cleaned_appearances.csv & Lookup) │
               └────────────────────┬────────────────────┘
                                    │ Constraint: Success
                                    ▼
               ┌─────────────────────────────────────────┐
               │        Kiểm tra & Đối soát SQL          │
               │  (Đối chiếu số dòng và tổng độ đo)      │
               └─────────────────────────────────────────┘
```

---

## 3. CHI TIẾT CẤU HÌNH CÁC TÁC VỤ CONTROL FLOW

### 3.1. `Execute SQL Task: Drop All Tables`

- **ConnectionType**: `OLE DB`
- **Connection**: `CM_DW_Football` (kết nối tới `DW_Football_Transfermarkt`)
- **ResultSet**: `None`
- **SQLSourceType**: `Direct input`
- **SQLStatement** (xóa fact trước, chiều trận tiếp theo, rồi các chiều còn lại để đáp ứng ràng buộc khóa ngoại):

```sql
DROP TABLE IF EXISTS dbo.FACT_Player_Match_Perf;
DROP TABLE IF EXISTS dbo.DIM_Game;
DROP TABLE IF EXISTS dbo.DIM_Player;
DROP TABLE IF EXISTS dbo.DIM_Club;
DROP TABLE IF EXISTS dbo.DIM_Competition;
DROP TABLE IF EXISTS dbo.DIM_Time;
```

### 3.2. `Execute SQL Task: Create All Tables`

- **Precedence Constraint**: Nối từ `Drop All Tables` với `Evaluation operation = Constraint`, `Value = Success`.
- **ConnectionType**: `OLE DB`, **Connection**: `CM_DW_Football`, **ResultSet**: `None`, **SQLSourceType**: `Direct input`.
- **SQLStatement** (thực thi trong một giao dịch, tạo bảng tham chiếu trước bảng có khóa ngoại):

```sql
SET XACT_ABORT ON;

BEGIN TRANSACTION;

CREATE TABLE dbo.DIM_Competition (
    Competition_ID NVARCHAR(100) NOT NULL CONSTRAINT PK_DIM_Competition PRIMARY KEY,
    Competition_Name NVARCHAR(200) NULL,
    Country_Name NVARCHAR(200) NULL,
    Competition_Type NVARCHAR(100) NULL
);

CREATE TABLE dbo.DIM_Club (
    Club_ID INT NOT NULL CONSTRAINT PK_DIM_Club PRIMARY KEY,
    Club_Name NVARCHAR(200) NULL,
    Stadium_Name NVARCHAR(200) NULL,
    Stadium_Seats INT NULL,
    Squad_Size INT NULL
);

CREATE TABLE dbo.DIM_Player (
    Player_ID INT NOT NULL CONSTRAINT PK_DIM_Player PRIMARY KEY,
    Player_Name NVARCHAR(200) NULL,
    Date_Of_Birth DATE NULL,
    Country_Of_Citizenship NVARCHAR(200) NULL,
    Main_Position NVARCHAR(100) NULL,
    Sub_Position NVARCHAR(100) NULL,
    Foot NVARCHAR(100) NULL,
    Height_In_Cm INT NULL
);

CREATE TABLE dbo.DIM_Game (
    Game_ID INT NOT NULL CONSTRAINT PK_DIM_Game PRIMARY KEY,
    Competition_ID NVARCHAR(100) NOT NULL,
    Season INT NOT NULL,
    Round NVARCHAR(100) NULL,
    [Date] DATE NOT NULL,
    Home_Club_ID INT NOT NULL,
    Away_Club_ID INT NOT NULL,
    Home_Club_Goals INT NULL,
    Away_Club_Goals INT NULL,
    Stadium NVARCHAR(200) NULL,
    Home_Club_Manager_Name NVARCHAR(200) NULL,
    Away_Club_Manager_Name NVARCHAR(200) NULL,
    CONSTRAINT FK_DIM_Game_Competition_ID FOREIGN KEY (Competition_ID) REFERENCES dbo.DIM_Competition(Competition_ID),
    CONSTRAINT FK_DIM_Game_Home_Club_ID FOREIGN KEY (Home_Club_ID) REFERENCES dbo.DIM_Club(Club_ID),
    CONSTRAINT FK_DIM_Game_Away_Club_ID FOREIGN KEY (Away_Club_ID) REFERENCES dbo.DIM_Club(Club_ID)
);

CREATE TABLE dbo.DIM_Time (
    Time_ID INT NOT NULL CONSTRAINT PK_DIM_Time PRIMARY KEY,
    Full_Date DATE NOT NULL CONSTRAINT UQ_DIM_Time_Full_Date UNIQUE,
    [Year] INT NOT NULL,
    [Quarter] INT NOT NULL,
    Year_Quarter_Key INT NOT NULL,
    [Month] INT NOT NULL,
    Year_Month_Key INT NOT NULL,
    [Day] INT NOT NULL,
    Day_Of_Week INT NOT NULL,
    Is_Weekend INT NOT NULL
);

CREATE TABLE dbo.FACT_Player_Match_Perf (
    Appearance_ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_FACT_Player_Match_Perf PRIMARY KEY,
    Source_Appearance_ID VARCHAR(100) NOT NULL CONSTRAINT UQ_FACT_Player_Match_Perf_Source_Appearance_ID UNIQUE,
    Player_ID INT NOT NULL,
    Club_ID INT NOT NULL,
    Opponent_Club_ID INT NULL,
    Competition_ID NVARCHAR(100) NOT NULL,
    Game_ID INT NOT NULL,
    Time_ID INT NOT NULL,
    Minutes_Played INT NULL,
    Goals INT NULL,
    Assists INT NULL,
    Yellow_Cards INT NULL,
    Red_Cards INT NULL,
    Is_Home_Game INT NULL,
    CONSTRAINT FK_FACT_Player_Match_Perf_Player_ID FOREIGN KEY (Player_ID) REFERENCES dbo.DIM_Player(Player_ID),
    CONSTRAINT FK_FACT_Player_Match_Perf_Club_ID FOREIGN KEY (Club_ID) REFERENCES dbo.DIM_Club(Club_ID),
    CONSTRAINT FK_FACT_Player_Match_Perf_Opponent_Club_ID FOREIGN KEY (Opponent_Club_ID) REFERENCES dbo.DIM_Club(Club_ID),
    CONSTRAINT FK_FACT_Player_Match_Perf_Competition_ID FOREIGN KEY (Competition_ID) REFERENCES dbo.DIM_Competition(Competition_ID),
    CONSTRAINT FK_FACT_Player_Match_Perf_Game_ID FOREIGN KEY (Game_ID) REFERENCES dbo.DIM_Game(Game_ID),
    CONSTRAINT FK_FACT_Player_Match_Perf_Time_ID FOREIGN KEY (Time_ID) REFERENCES dbo.DIM_Time(Time_ID)
);

COMMIT TRANSACTION;
```

**Tóm tắt khóa chính và ràng buộc tham chiếu:**

| Bảng | Khóa chính | Ràng buộc tham chiếu |
| :--- | :--- | :--- |
| `DIM_Competition` | `Competition_ID` | Khóa chính `NVARCHAR(100)` |
| `DIM_Club` | `Club_ID` | Khóa chính `INT` |
| `DIM_Player` | `Player_ID` | Khóa chính `INT`, ngày sinh kiểu `DATE` |
| `DIM_Game` | `Game_ID` | Một mã giải (`Competition_ID`) và hai mã CLB (`Home_Club_ID`, `Away_Club_ID`) |
| `DIM_Time` | `Time_ID` | `Full_Date` duy nhất (`UNIQUE`), kiểu `DATE` |
| `FACT_Player_Match_Perf` | `Appearance_ID` | `IDENTITY`, `Source_Appearance_ID` duy nhất (`UNIQUE`), khóa ngoại sang 5 bảng chiều (CLB 2 vai trò) |

### 3.3. `Sequence Container: Load Dimensions`

- **Precedence Constraint**: Nối `Success` từ `Create All Tables` vào `Sequence Container`.
- Đặt 5 Data Flow Task bên trong container: `DIM_Club`, `DIM_Competition`, `DIM_Player`, `DIM_Game`, `DIM_Time`.
- **Thứ tự ràng buộc bên trong container**:
  - Nối `DIM_Club` $\rightarrow$ `DIM_Game` và `DIM_Competition` $\rightarrow$ `DIM_Game`. Trong **Precedence Constraint Editor**, chọn **Logical AND** trên hai ràng buộc (`Value = Success`) để `DIM_Game` chỉ bắt đầu khi cả hai tác vụ nguồn đã thành công.
  - Nếu tách bước bổ sung 25 CLB từ dữ liệu trận thành một Data Flow Task riêng, nối `DIM_Club` $\rightarrow$ tác vụ bổ sung $\rightarrow$ `DIM_Game` và giữ `DIM_Competition` $\rightarrow$ `DIM_Game` (Logical AND).
  - `DIM_Player` và `DIM_Time` có thể chạy song song.

### 3.4. `Data Flow Task: FACT_Player_Match_Perf`

- Đặt bên ngoài `Sequence Container: Load Dimensions` và nối từ container bằng ràng buộc `Success` để chỉ chạy khi toàn bộ 5 bảng chiều đã nạp xong.

---

## 4. RÀNG BUỘC ƯU TIÊN, VẬN HÀNH VÀ CHẠY LẠI LÔ

1. **Chạy toàn phần và kiểm tra từng luồng**:
   - Xác nhận đúng cơ sở dữ liệu (`DW_Football_Transfermarkt`) và tham số `InputFolder`, rồi bấm **Start** trong Visual Studio.
   - Kiểm tra **Progress** hoặc **Execution Results** để xem thứ tự thực hiện và số dòng đi từ nguồn đến đích, cũng như các nhánh loại/nhánh lỗi.
   - Ghi rõ tên tệp, mã bản ghi, bước xử lý và lý do đối với mọi dòng bị từ chối. Lô đạt khi số đếm khớp và các lỗi bắt buộc đã được xử lý.
2. **Chạy lại cùng một lô khi giữ dữ liệu**:
   - Bỏ qua nhóm tác vụ `Drop All Tables` và `Create All Tables`.
   - Với các bảng chiều: tra theo khóa chính để chèn mã mới hoặc cập nhật theo chính sách của từng chiều.
   - Với bảng fact: `Lookup` theo `Source_Appearance_ID` vào bảng đích `dbo.FACT_Player_Match_Perf`, đưa các mã đã tồn tại sang nhánh đếm riêng và chỉ chèn các mã chưa có với ràng buộc `UNIQUE` ở đích. Đối chiếu lại số lượt ra sân và tổng độ đo sau lần chạy thứ hai để bảo đảm không nạp trùng.

---

## 5. KIỂM TRA VÀ ĐỐI SOÁT KẾT QUẢ TRONG SQL SERVER

Mở **New Query** trên `DW_Football_Transfermarkt` sau khi chạy package và đối chiếu các mốc sau:

| Bảng | Mốc số dòng | Điểm kiểm tra trọng tâm |
| :--- | :---: | :--- |
| `dbo.DIM_Club` | **272** | 247 CLB từ CSV + 25 CLB bổ sung từ trận đấu (`Stadium_Name`, `Stadium_Seats`, `Squad_Size` giữ `NULL`) |
| `dbo.DIM_Player` | **7.069** | Tên có dấu UTF-8, `Date_Of_Birth` kiểu `DATE`, thuộc tính thiếu giữ `NULL` |
| `dbo.DIM_Competition` | **13** | Mã giải kiểu chuỗi `NVARCHAR(100)`, `Country_Name` của các giải quốc tế giữ theo nguồn (`NULL`) |
| `dbo.DIM_Game` | **7.280** | Mùa `2022`, `2023`, mã giải và hai mã CLB hợp lệ |
| `dbo.DIM_Time` | **488** | Ngày duy nhất, `Time_ID` dạng `YYYYMMDD`, `Is_Weekend = 1` ở thứ Bảy (6) và Chủ nhật (7) |
| `dbo.FACT_Player_Match_Perf` | **210.747** | `Appearance_ID` tự sinh, mỗi `Source_Appearance_ID` chỉ xuất hiện 1 lần |

```sql
-- 1. Kiểm tra số dòng 6 bảng
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Club;
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Player;
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Competition;
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Game;
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Time;
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.FACT_Player_Match_Perf;

-- 2. Kiểm tra trùng lặp Source_Appearance_ID
SELECT Source_Appearance_ID, COUNT_BIG(*) AS So_Dong
FROM dbo.FACT_Player_Match_Perf
GROUP BY Source_Appearance_ID
HAVING COUNT_BIG(*) > 1;

-- 3. Đối chiếu lượt ra sân và tổng độ đo theo giải và mùa
SELECT f.Competition_ID, g.Season, COUNT_BIG(*) AS Luot_Ra_San,
       SUM(f.Minutes_Played) AS Phut, SUM(f.Goals) AS Ban,
       SUM(f.Assists) AS Kien_Tao, SUM(f.Yellow_Cards) AS The_Vang,
       SUM(f.Red_Cards) AS The_Do
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Game AS g ON g.Game_ID = f.Game_ID
GROUP BY f.Competition_ID, g.Season
ORDER BY f.Competition_ID, g.Season;
```

- **Tổng tham chiếu trên 210.747 lượt ra sân**: **13.562.727** phút thi đấu, **19.173** bàn thắng, **14.739** kiến tạo, **28.694** thẻ vàng và **827** thẻ đỏ. Nếu có dòng bị từ chối, dùng số liệu từ nhánh lỗi để giải thích chênh lệch.

---

## 6. DANH MỤC CÁC TỆP HƯỚNG DẪN TRONG HỆ THỐNG SSIS

| STT | Tên tệp hướng dẫn | Thành phần Control / Data Flow | Nhiệm vụ SSIS |
| :---: | :--- | :--- | :--- |
| 1 | [ssis_main.md](ssis_main.md) | **Control Flow Master** | `Drop All Tables` $\rightarrow$ `Create All Tables` $\rightarrow$ `Load Dimensions` $\rightarrow$ `FACT_Player_Match_Perf` $\rightarrow$ Đối soát |
| 2 | [ssis_dim_club.md](ssis_dim_club.md) | Data Flow Task | Nạp 247 CLB từ `cleaned_clubs.csv` và bổ sung 25 CLB từ `cleaned_games.csv` vào `dbo.DIM_Club` (272 CLB) |
| 3 | [ssis_dim_player.md](ssis_dim_player.md) | Data Flow Task | Nạp 7.069 cầu thủ từ `cleaned_players.csv` vào `dbo.DIM_Player` |
| 4 | [ssis_dim_competition.md](ssis_dim_competition.md) | Data Flow Task | Nạp 13 giải đấu từ `cleaned_competitions.csv` vào `dbo.DIM_Competition` |
| 5 | [ssis_dim_game.md](ssis_dim_game.md) | Data Flow Task | Nạp 7.280 trận đấu từ `cleaned_games.csv` kèm 3 Lookup khóa ngoại vào `dbo.DIM_Game` |
| 6 | [ssis_dim_time.md](ssis_dim_time.md) | Data Flow Task | Nạp 488 ngày duy nhất từ `cleaned_time.csv` vào `dbo.DIM_Time` |
| 7 | [ssis_fact_player_match_perf.md](ssis_fact_player_match_perf.md) | Data Flow Task | Nạp 210.747 lượt ra sân từ `cleaned_appearances.csv` qua 5 Lookup và đối chiếu vào `dbo.FACT_Player_Match_Perf` |
| 8 | [ssis_migration_plan.md](ssis_migration_plan.md) | **Kế hoạch chỉnh sửa** | Hướng dẫn nâng cấp từng bước trong Visual Studio 2022 từ bản cũ (`OLAP version 3`) sang bản mới |
