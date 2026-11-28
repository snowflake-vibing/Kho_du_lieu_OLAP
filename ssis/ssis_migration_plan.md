# KẾ HOẠCH CHỈNH SỬA SSIS TRONG VISUAL STUDIO (TỪ BẢN CŨ V3 SANG BẢN MỚI)

> **Tài liệu đối chiếu:**
> - **Bản cũ:** `OLAP version 3 (1).docx` (Chương 2) — dùng `Data Conversion` (`dc_*`), `Ignore failure`, điền giả `0`, thiếu khóa ngoại `DIM_Game`, `DIM_Time` không tách quý/tháng kèm năm, `FACT` chứa `Goal_Contributions`, `Is_Starter`, `Market_Value_In_EUR`.
> - **Bản mới:** `Chuong_2_SSIS.docx` — tham chiếu chi tiết từng luồng trong [ssis_main.md](ssis_main.md), [ssis_dim_club.md](ssis_dim_club.md), [ssis_dim_player.md](ssis_dim_player.md), [ssis_dim_competition.md](ssis_dim_competition.md), [ssis_dim_game.md](ssis_dim_game.md), [ssis_dim_time.md](ssis_dim_time.md) và [ssis_fact_player_match_perf.md](ssis_fact_player_match_perf.md).

---

## 1. TỔNG QUAN THAY ĐỔI (BẢN CŨ V3 $\rightarrow$ BẢN MỚI)

| Hạng mục | Bản cũ (`OLAP version 3`) | Bản mới (`Chuong_2_SSIS`) | Hành động trong Visual Studio / SQL |
| :--- | :--- | :--- | :--- |
| **Chuẩn bị DB** | Dùng Wizard `Configure Management Data Warehouse` & `Data Collection` | Tạo DB `DW_Football_Transfermarkt` trực tiếp bằng `New Database…` | Bỏ toàn bộ bước cấu hình MDW/Data Collection |
| **Kết nối & Tham số** | Connection Manager `DESKTOP-9B88R8P.DW_Football_Transfermarkt`, đường dẫn CSV cứng | `CM_DW_Football`, Package Parameter `InputFolder` + Expression `ConnectionString` | Đổi tên CM, thêm Parameter `InputFolder` trỏ tới `football/cleaned_data/ssis_input` |
| **Control Flow** | `Drop All Tables` (thiếu `IF EXISTS`, xóa `Club/Competition` trước `Game`), `Create All Tables` (có `USE`/`GO`, không transaction), `Sequence Container` chạy 5 DIM song song | `Drop All Tables` (`DROP TABLE IF EXISTS` xóa `DIM_Game` trước `Club/Competition`), `Create All Tables` (1 transaction), `Load Dimensions` dùng **Logical AND** vào `DIM_Game` | Sửa SQL của 2 `Execute SQL Task` và bổ sung ràng buộc ưu tiên vào `DIM_Game` |
| **Ép kiểu nguồn** | Đọc CSV dạng mặc định rồi dùng khối `Data Conversion` (`dc_*`) | Khai báo kiểu trực tiếp ở `FF_* → Advanced`, giữ nguyên tên cột CSV | Xóa toàn bộ khối `Data Conversion`, bật `Retain null values...` và `Error Output = Redirect row` |
| **Xử lý trùng lặp** | `Sort` chỉ theo khóa chính + tự xóa trùng âm thầm | `Sort` theo khóa chính + toàn bộ cột nạp + `Script Component` tách trùng khác nội dung | Cập nhật cấu hình `Sort` và thêm `Script Component` ở các luồng |
| **`DIM_Club`** | 6 cột (`Coach_Name`), chỉ nạp `clubs.csv` (247 CLB) | 5 cột (bỏ `Coach_Name`), giữ `NULL`, bổ sung **25 CLB** từ `cleaned_games.csv` | Sửa luồng chính + thêm nhánh/task bổ sung 25 CLB $\rightarrow$ **272 CLB** |
| **`DIM_Player`** | 9 cột (`Age`, `Date_Of_Birth NVARCHAR(100)`), loại dòng thiếu ngày sinh/chiều cao | 8 cột (bỏ `Age`, `Date_Of_Birth DATE`), chỉ kiểm tra `player_id > 0` và `height_in_cm > 0` (hoặc `NULL`) | Đổi biểu thức `Derived Column` sang `Birth_Date`, nới `Valid_Player` $\rightarrow$ **7.069 cầu thủ** |
| **`DIM_Competition`** | Loại bỏ dòng có `country_name` rỗng, bảng đích gõ nhầm `DIM_Competiton` | Chỉ kiểm tra `competition_id` không rỗng, giữ `NULL` cho giải quốc tế | Sửa `Valid_Competition`, sửa tên bảng đích `[dbo].[DIM_Competition]` $\rightarrow$ **13 giải** |
| **`DIM_Game`** | 7 cột, không có FK, không Lookup | 12 cột (thêm `Competition_ID`, `Season`, `Date`, `Home/Away_Club_Manager_Name`), 3 `Lookup` xác nhận FK | Cấu hình lại `FF_Game` (14 cột), thêm 3 `Lookup`, map 12 cột $\rightarrow$ **7.280 trận** |
| **`DIM_Time`** | Dùng `FF_Game`, có `Season`, `Day_Of_Week` chuỗi, `Sort` đặt cuối luồng | Dùng `FF_Time` (`cleaned_time.csv`), bỏ `Season`, `Sort` trước `Derived Column`, 2 `Derived Column` (`Year_Quarter_Key`, `Year_Month_Key`, `Day_Of_Week INT`) | Đổi tên CM, đổi thứ tự khối, thay 1 khối thành 2 khối `Derived Column` $\rightarrow$ **488 ngày** |
| **`FACT_Player_Match_Perf`** | `Appearance_ID NVARCHAR(100)` PK, 4 Lookup `Ignore failure` (bước Competition nối nhầm `dc_player_club_id`), tính `Time_ID`/`Goal_Contributions`/`Is_Starter` | `Appearance_ID INT IDENTITY` + `Source_Appearance_ID VARCHAR(100) UNIQUE`, thêm `Sort`+`Script`, 5 Lookup (`Redirect rows`), thêm `Lookup Time` + nhánh đối chiếu `DIM_Game`, bỏ `Goal_Contributions`/`Is_Starter`/`Market_Value_In_EUR` | Cập nhật DDL, sửa chuỗi 5 Lookup, thêm đối chiếu, sửa `Derived Column` và Destination $\rightarrow$ **210.747 lượt** |

---

## 2. CHUẨN BỊ TRƯỚC KHI MỞ VISUAL STUDIO

1. **Xuất lại 6 tệp CSV đầu vào cho SSIS**:
   - Mở `pre_processing.ipynb`, chạy các cell lọc 13 giải đấu và 2 mùa `2022`, `2023`, đặt `EXPORT_FILES = True` và chạy cell xuất tệp vào `football/cleaned_data/ssis_input`.
   - Đối chiếu đủ 6 tệp: `cleaned_competitions.csv` (13 dòng, 4 cột), `cleaned_clubs.csv` (247 dòng, 6 cột), `cleaned_players.csv` (7.069 dòng, 8 cột), `cleaned_games.csv` (7.280 dòng, 14 cột), `cleaned_time.csv` (7.280 dòng, 1 cột `date`), `cleaned_appearances.csv` (210.747 dòng, 11 cột).
2. **Tạo cơ sở dữ liệu đích đơn giản trong SSMS**:
   - Mở SQL Server Management Studio, kết nối **Database Engine**.
   - Bấm phải **Databases → New Database…**, nhập tên `DW_Football_Transfermarkt` và bấm **OK** *(bỏ hoàn toàn các bước `Configure Management Data Warehouse` và `Configure Data Collection` ở bản cũ)*.
3. **Sao lưu project SSIS cũ**:
   - Sao chép tệp `Package.dtsx` hiện tại sang một bản dự phòng (ví dụ `Package_v3_backup.dtsx`) trước khi chỉnh sửa trực tiếp trên `Package.dtsx` trong Visual Studio 2022.

---

## 3. THIẾT LẬP CẤP PACKAGE VÀ CONNECTION MANAGERS

1. **Đổi tên OLE DB Connection Manager**:
   - Trong vùng **Connection Managers** ở đáy màn hình, bấm phải kết nối cũ (`DESKTOP-9B88R8P.DW_Football_Transfermarkt`), chọn **Rename** thành **`CM_DW_Football`**, kiểm tra lại Server name, xác thực và Database `DW_Football_Transfermarkt` rồi bấm **Test Connection**.
2. **Tạo Package Parameter `InputFolder`**:
   - Mở tab **Parameters** của `Package.dtsx`, bấm nút thêm parameter:
     - **Name**: `InputFolder`
     - **Data Type**: `String`
     - **Value**: đường dẫn tới thư mục `football\cleaned_data\ssis_input` trên máy.
3. **Gắn Expression động cho các Flat File Connection Manager**:
   - Với từng kết nối `FF_Competition`, `FF_Club`, `FF_Player`, `FF_Game`, `FF_Time`, `FF_Appearances`: mở **Properties → Expressions (`...`)**, chọn Property `ConnectionString` và ghép `@[$Package::InputFolder] + "\\<ten_tep>.csv"` (giữ một đường dẫn mẫu hợp lệ ở thuộc tính `ConnectionString` gốc để thiết lập metadata và Preview).

---

## 4. CHỈNH SỬA CONTROL FLOW

### 4.1. Sửa `Execute SQL Task: Drop All Tables`

- Đảm bảo **Connection** trỏ về `CM_DW_Football`, **ResultSet** = `None`, **SQLSourceType** = `Direct input`.
- **Thay đổi SQLStatement** (bỏ `USE DW_Football_Transfermarkt;`, dùng `DROP TABLE IF EXISTS` và đưa `DIM_Game` lên trước `DIM_Club`/`DIM_Competition` vì bản mới bổ sung 3 khóa ngoại trên `DIM_Game`):

```sql
DROP TABLE IF EXISTS dbo.FACT_Player_Match_Perf;
DROP TABLE IF EXISTS dbo.DIM_Game;
DROP TABLE IF EXISTS dbo.DIM_Player;
DROP TABLE IF EXISTS dbo.DIM_Club;
DROP TABLE IF EXISTS dbo.DIM_Competition;
DROP TABLE IF EXISTS dbo.DIM_Time;
```

### 4.2. Sửa `Execute SQL Task: Create All Tables`

- Kiểm tra **Precedence Constraint** từ `Drop All Tables` đến `Create All Tables`: `Evaluation operation = Constraint`, `Value = Success`.
- Chọn **Connection** = `CM_DW_Football`, **ResultSet** = `None`, **SQLSourceType** = `Direct input`.
- **Xóa sạch SQLStatement cũ** (bỏ `USE`, bỏ mọi lệnh `GO`, bỏ khối `DROP TABLE` lặp lại ở đầu) và thay bằng DDL 6 bảng trong một transaction duy nhất (chi tiết các thay đổi lược đồ: `DIM_Club` bỏ `Coach_Name`; `DIM_Player` bỏ `Age` và đổi `Date_Of_Birth` thành `DATE`; `DIM_Game` mở rộng lên 12 cột + 3 FK; `DIM_Time` bỏ `Season`, đổi `Full_Date` sang `DATE UNIQUE`, `Day_Of_Week` sang `INT`, thêm `Year_Quarter_Key`, `Year_Month_Key`; `FACT_Player_Match_Perf` đổi `Appearance_ID` sang `INT IDENTITY(1,1) PK`, thêm `Source_Appearance_ID VARCHAR(100) UNIQUE`, các FK thành `NOT NULL` trừ `Opponent_Club_ID`, bỏ `Goal_Contributions`, `Market_Value_In_EUR`, `Is_Starter` và bỏ `DEFAULT 0`):

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

### 4.3. Sửa `Sequence Container` $\rightarrow$ `Load Dimensions`

- Đổi tên `Sequence Container` thành **`Load Dimensions`**.
- **Không để 5 Data Flow chạy song song tự do như bản cũ**: kéo mũi tên xanh (`Success`) từ `DIM_Club` $\rightarrow$ `DIM_Game` và từ `DIM_Competition` $\rightarrow$ `DIM_Game` *(nếu tách nhánh bổ sung 25 CLB thành task riêng `DIM_Club_Supplement`, nối `DIM_Club` $\rightarrow$ `DIM_Club_Supplement` $\rightarrow$ `DIM_Game`)*.
- Double-click vào cả hai đường nối đi vào `DIM_Game`, chọn **`Logical AND`** (`Multiple constraints: Logical AND. All constraints must evaluate to True`).
- Giữ `DIM_Player` và `DIM_Time` chạy song song độc lập bên trong container; nối `Load Dimensions` $\rightarrow$ `FACT_Player_Match_Perf` bằng `Success`.

---

## 5. QUY TẮC CHỈNH SỬA LẶP LẠI TRÊN CẢ 6 DATA FLOW

Thực hiện nhất quán 4 thao tác chung này khi vào từng tab Data Flow:

1. **Xóa khối `Data Conversion` và bỏ mọi tiền tố `dc_*`**:
   - Nối trực tiếp từ `Flat File Source` sang thành phần kế tiếp (`Derived Column` hoặc `Conditional Split`).
   - Sau khi nối lại, mở lần lượt các khối phía sau (`Conditional Split`, `Derived Column`, `Sort`, `Lookup`, `OLE DB Destination`) để thay tên cột `dc_*` thành tên cột gốc từ CSV.
2. **Khai báo kiểu ở `FF_* → Advanced` và giữ `NULL` ở `Flat File Source`**:
   - Trong `Flat File Connection Manager Editor`: kiểm tra `Format = Delimited`, `Code page = 65001 (UTF-8)`, `Text qualifier = "`, bật `Column names in the first data row`, `{Comma}` và `{CR}{LF}`; sang tab **Advanced** đặt đúng `DataType` và `OutputColumnWidth`.
   - Mở lại `Flat File Source Editor`: xác nhận đồng bộ metadata nếu SSIS hỏi; tick **`Retain null values from the source as null values in the data flow`**; vào **Error Output** đặt `Error` và `Truncation` thành **`Redirect row`** nối ra đích ghi lỗi (ví dụ Flat File hoặc bảng log lỗi).
3. **Nâng cấp xử lý trùng lặp (`Sort` + `Script Component`)**:
   - Thay cấu hình `Sort` chỉ sắp theo 1 cột khóa chính ở bản cũ bằng: sắp xếp tăng dần theo cột khóa chính và đưa **toàn bộ các cột dùng để nạp** vào tập khóa sắp xếp, bật **`Remove rows with duplicate sort values`** (kiểm tra tùy chọn so sánh chuỗi nếu khóa là chuỗi để tránh gộp nhầm mã chỉ khác chữ hoa/thường).
   - Sau `Sort`, thêm **`Script Component`** kiểu **Transformation** với 2 đầu ra không đồng bộ: gom các dòng liên tiếp theo khóa chính, chuyển nhóm 1 dòng sang bước kế tiếp và nhóm nhiều dòng (cùng khóa nhưng khác nội dung) sang nhánh rà soát; nhớ xử lý nhóm cuối khi luồng kết thúc.
4. **Chuẩn hóa `OLE DB Destination`**:
   - Chọn Connection Manager **`CM_DW_Football`**, `Data access mode = Table or view - fast load`, bật **`Keep nulls`** và **`Check constraints`**; vào **Error Output** cấu hình chuyển dòng lỗi sang nhánh ghi lỗi.

---

## 6. KẾ HOẠCH CHỈNH SỬA CHI TIẾT TỪNG DATA FLOW

### 6.1. `DIM_Club` (từ 247 CLB thành 272 CLB)

1. **Xóa**: Khối `Data Conversion`.
2. **Sửa `FF_Club` & `Flat File Source`**:
   - Tab `Advanced`: `club_id` (`DT_I4`), `name` (`DT_WSTR 200`), `stadium_name` (`DT_WSTR 200`), `stadium_seats` (`DT_I4`), `coach_name` (`DT_WSTR 200`), `squad_size` (`DT_I4`).
   - Tab `Columns` của `Flat File Source`: **bỏ chọn `coach_name`** (HLV theo trận đã chuyển sang `DIM_Game`).
3. **Sửa `Conditional Split`**:
   - Đổi biểu thức của `Valid_Club` thành:
     ```c
     !ISNULL(club_id) && club_id > 0
     && (ISNULL(stadium_seats) || stadium_seats >= 0)
     && (ISNULL(squad_size) || squad_size >= 0)
     ```
   - Đặt Default Output là **`Rejected_Rows`** nối ra nhánh ghi lỗi.
4. **Sửa `Sort` & Thêm `Script Component`**: cấu hình theo Mục 5 (khóa `club_id` + 4 cột nạp còn lại).
5. **Sửa `OLE DB Destination` (`[dbo].[DIM_Club]`)**: ánh xạ 5 cột (`club_id → Club_ID`, `name → Club_Name`, `stadium_name → Stadium_Name`, `stadium_seats → Stadium_Seats`, `squad_size → Squad_Size`).
6. **Thêm mới luồng bổ sung 25 CLB từ `cleaned_games.csv`** *(khuyến nghị tạo Data Flow Task riêng chạy `Success` sau `DIM_Club` và nối `Success` vào `DIM_Game`)*:
   - Kéo `Flat File Source` dùng **`FF_Game`** $\rightarrow$ **`Multicast`** chia 2 nhánh:
     - Nhánh 1: giữ `home_club_id`, `home_club_name`, `date`, `game_id`.
     - Nhánh 2: giữ `away_club_id`, `away_club_name`, `date`, `game_id`.
   - Nối vào **`Union All`**, đổi tên ngay cột đầu ra thành `Club_ID`, `Club_Name`, `Match_Date`, `Game_ID`.
   - Nối **`Derived Column`** tạo cột cờ ưu tiên dòng có tên CLB (không `NULL`/rỗng).
   - Nối **`Sort`** sắp theo: `Club_ID ASC`, cờ có tên `DESC`, `Match_Date DESC`, `Game_ID DESC`.
   - Nối **`Script Component`** (Transformation, đầu ra đồng bộ kiểu loại trừ): chọn `Club_ID` làm cột chỉ đọc, lưu mã vừa gặp và chỉ gọi `DirectRowTo...` cho dòng đầu của mỗi `Club_ID` (giữ mã kể cả khi dữ liệu trận thiếu tên).
   - Nối **`Lookup`** (`Full cache`, `CM_DW_Football`) tra `Club_ID` vào `dbo.DIM_Club`, lấy **`Lookup No Match Output`**.
   - Nối **`Derived Column`** tạo 3 cột thiếu:
     - `Stadium_Name`: `NULL(DT_WSTR,200)`
     - `Stadium_Seats`: `NULL(DT_I4)`
     - `Squad_Size`: `NULL(DT_I4)`
   - Nối **`OLE DB Destination`** (`[dbo].[DIM_Club]`, `CM_DW_Football`, `Table or view - fast load`, bật `Keep nulls` và `Check constraints`), ánh xạ 5 cột (`Club_ID`, `Club_Name`, `Stadium_Name`, `Stadium_Seats`, `Squad_Size`).

### 6.2. `DIM_Player`

1. **Xóa**: Khối `Data Conversion`.
2. **Sửa `FF_Player → Advanced`**:
   - `player_id` (`DT_I4`), `name` (`DT_WSTR 200`), **`date_of_birth` (`DT_DBTIMESTAMP`)**, `country_of_citizenship` (`DT_WSTR 200`), `position` (`DT_WSTR 100`), `sub_position` (`DT_WSTR 100`), `foot` (`DT_WSTR 100`), `height_in_cm` (`DT_I4`).
3. **Sửa `Derived Column`**:
   - Xóa dòng tính cột `age` cũ; thêm cột mới **`Birth_Date`** (`<add as new column>`):
     ```c
     ISNULL(date_of_birth) ? NULL(DT_DBDATE) : (DT_DBDATE)date_of_birth
     ```
4. **Sửa `Conditional Split`**:
   - Thay điều kiện `Valid_Player` quá chặt ở bản cũ (vốn loại mất cầu thủ thiếu ngày sinh/vị trí/chiều cao) bằng:
     ```c
     !ISNULL(player_id) && player_id > 0
     && (ISNULL(height_in_cm) || height_in_cm > 0)
     ```
   - Đặt Default Output là **`Rejected_Rows`**.
5. **Sửa `Sort` & Thêm `Script Component`**: nối từ `Valid_Player` *(lưu ý bản cũ ghi nhầm `Valid_Club`)*, cấu hình theo Mục 5.
6. **Sửa `OLE DB Destination` (`[dbo].[DIM_Player]`)**: ánh xạ 8 cột (`player_id → Player_ID`, `name → Player_Name`, **`Birth_Date → Date_Of_Birth`**, `country_of_citizenship → Country_Of_Citizenship`, `position → Main_Position`, `sub_position → Sub_Position`, `foot → Foot`, `height_in_cm → Height_In_Cm`), bỏ `Age`.

### 6.3. `DIM_Competition`

1. **Xóa**: Khối `Data Conversion`.
2. **Sửa `FF_Competition → Advanced`**: `competition_id` (`DT_WSTR 100`), `name` (`DT_WSTR 200`), `country_name` (`DT_WSTR 200`), `type` (`DT_WSTR 100`).
3. **Sửa `Conditional Split`**:
   - Sửa `Valid_Competition` thành:
     ```c
     !ISNULL(competition_id) && LEN(TRIM(competition_id)) > 0
     ```
     *(khắc phục lỗi bản cũ yêu cầu `dc_country_name` không rỗng nên làm mất các giải quốc tế `CL`, `EL`, `UCOL`)*.
   - Đặt Default Output là **`Rejected_Rows`**.
4. **Sửa `Sort` & Thêm `Script Component`**: cấu hình theo Mục 5 (lưu ý bật tùy chọn so sánh chuỗi phân biệt chữ hoa/thường ở `Sort` nếu cần).
5. **Sửa `OLE DB Destination`**: sửa lỗi chính tả tên bảng cũ `[dbo].[DIM_Competiton]` thành **`[dbo].[DIM_Competition]`** và ánh xạ 4 cột (`competition_id → Competition_ID`, `name → Competition_Name`, `country_name → Country_Name`, `type → Competition_Type`).

### 6.4. `DIM_Game`

1. **Xóa**: Khối `Data Conversion`.
2. **Sửa `FF_Game → Advanced` (mở rộng đủ 14 cột)**:
   - `game_id` (`DT_I4`), `competition_id` (`DT_WSTR 100`), `season` (`DT_I4`), `round` (`DT_WSTR 100`), `date` (`DT_DBDATE`), `home_club_id` (`DT_I4`), `away_club_id` (`DT_I4`), `home_club_goals` (`DT_I4`), `away_club_goals` (`DT_I4`), `stadium` (`DT_WSTR 200`), `home_club_name` (`DT_WSTR 200`), `away_club_name` (`DT_WSTR 200`), `home_club_manager_name` (`DT_WSTR 200`), `away_club_manager_name` (`DT_WSTR 200`).
3. **Sửa `Conditional Split`**:
   - Thay `Valid_Game` thành:
     ```c
     !ISNULL(game_id) && game_id > 0
     && !ISNULL(competition_id) && LEN(TRIM(competition_id)) > 0
     && !ISNULL(season) && !ISNULL(date)
     && !ISNULL(home_club_id) && home_club_id > 0
     && !ISNULL(away_club_id) && away_club_id > 0
     && home_club_id != away_club_id
     && (ISNULL(home_club_goals) || home_club_goals >= 0)
     && (ISNULL(away_club_goals) || away_club_goals >= 0)
     ```
   - Đặt Default Output là **`Rejected_Rows`**.
4. **Sửa `Sort` & Thêm `Script Component`**: chọn khóa `game_id` + 11 cột nạp (khắc phục lỗi bản cũ ghi nhầm `dc_player_id`), thêm `Script Component` tách trùng theo Mục 5.
5. **Thêm mới 3 khối `Lookup` nối tiếp sau `Script Component`**:
   - Thiết lập chung cả 3: `Cache mode = Full cache`, `Connection type = OLE DB connection manager` (`CM_DW_Football`), `No matching entries = Redirect rows to no match output`:
     1. **`Lookup Game Competition`** (`dbo.DIM_Competition`): `competition_id → Competition_ID`.
     2. **`Lookup Home Club`** (`dbo.DIM_Club`): `home_club_id → Club_ID`.
     3. **`Lookup Away Club`** (`dbo.DIM_Club`): `away_club_id → Club_ID`.
   - Nối tất cả **Lookup No Match Output** sang nhánh ghi lỗi (lưu `game_id`, mã đang tra và tên phép tra cứu).
6. **Sửa `OLE DB Destination` (`[dbo].[DIM_Game]`)**: nối từ `Match Output` của `Lookup Away Club`, ánh xạ 12 cột (`game_id`, `competition_id`, `season`, `round`, `date`, `home_club_id`, `away_club_id`, `home_club_goals`, `away_club_goals`, `stadium`, `home_club_manager_name`, `away_club_manager_name`), **để trống ánh xạ `home_club_name` và `away_club_name`**.

### 6.5. `DIM_Time`

1. **Xóa**: Khối `Data Conversion`, ngắt toàn bộ dây nối cũ để sắp xếp lại thứ tự khối.
2. **Sửa `Flat File Connection Manager`**: tạo mới (hoặc đổi từ `FF_Game` sang) **`FF_Time`** trỏ tới `cleaned_time.csv` (1 cột `date`, đặt kiểu **`DT_DBDATE`** ở tab `Advanced`). *(Nếu tệp CSV thực tế còn cột `Time_ID`, bỏ chọn cột này ở tab `Columns` của `Flat File Source`)*.
3. **Đổi thứ tự pipeline** (`Conditional Split` + `Sort` lên trước `Derived Column`):
   - `Flat File Source` $\rightarrow$ **`Conditional Split`** (`Valid_Time`: `!ISNULL(date)`, Default Output: `Rejected_Rows`) $\rightarrow$ **`Sort`** (`date` Ascending, bật `Remove rows with duplicate sort values`, gộp 7.280 dòng thành **488 ngày duy nhất**).
4. **Thay 1 khối `Derived Column` cũ bằng 2 khối `Derived Column` nối tiếp** (`<add as new column>`):
   - **Khối `Derived Column 1`** (nối sau `Sort`):
     - `Time_ID`: `YEAR([date]) * 10000 + MONTH([date]) * 100 + DAY([date])`
     - `Year`: `YEAR([date])`
     - `Quarter`: `DATEPART("qq", [date])`
     - `Month`: `MONTH([date])`
     - `Day`: `DAY([date])`
     - `Day_Of_Week`: `((DATEDIFF("dd", (DT_DBDATE)"1900-01-01", [date]) % 7 + 7) % 7) + 1` *(kiểu số `1..7`, Thứ Hai = 1)*
   - **Khối `Derived Column 2`** (nối sau `Derived Column 1`):
     - `Year_Quarter_Key`: `[Year] * 10 + [Quarter]`
     - `Year_Month_Key`: `[Year] * 100 + [Month]`
     - `Is_Weekend`: `[Day_Of_Week] >= 6 ? 1 : 0`
5. **Sửa `OLE DB Destination` (`[dbo].[DIM_Time]`)**: ánh xạ 10 cột (`date → Full_Date` cùng 9 cột vừa tạo ở hai khối `Derived Column`, bỏ `Season`).

### 6.6. `FACT_Player_Match_Perf`

1. **Xóa**: Khối `Data Conversion`.
2. **Sửa `FF_Appearances → Advanced`**:
   - `appearance_id` (`DT_STR 100`), `game_id` (`DT_I4`), `player_id` (`DT_I4`), `player_club_id` (`DT_I4`), `date` (`DT_DBDATE`), `competition_id` (`DT_WSTR 100`), `goals` (`DT_I4`), `assists` (`DT_I4`), `minutes_played` (`DT_I4`), `yellow_cards` (`DT_I4`), `red_cards` (`DT_I4`).
3. **Sửa `Conditional Split`**:
   - Đổi `Valid_Appearances` thành:
     ```c
     !ISNULL(appearance_id) && LEN(TRIM(appearance_id)) > 0
     && !ISNULL(game_id) && game_id > 0
     && !ISNULL(player_id) && player_id > 0
     && !ISNULL(player_club_id) && player_club_id > 0
     && (ISNULL(minutes_played) || minutes_played >= 0)
     && (ISNULL(goals) || goals >= 0)
     && (ISNULL(assists) || assists >= 0)
     && (ISNULL(yellow_cards) || yellow_cards >= 0)
     && (ISNULL(red_cards) || red_cards >= 0)
     ```
   - Đặt Default Output là **`Rejected_Rows`**.
4. **Thêm mới `Sort` & `Script Component` sau `Valid_Appearances`**:
   - `Sort` theo `appearance_id` (Ascending) + toàn bộ cột đầu vào, bật `Remove rows with duplicate sort values`.
   - `Script Component` gom liên tiếp theo `appearance_id`: nhóm 1 dòng $\rightarrow$ `Lookup Player`, nhóm nhiều dòng $\rightarrow$ nhánh rà soát.
5. **Sửa chuỗi Lookup (đổi `Ignore failure` $\rightarrow$ `Redirect rows to no match output`, đảo thứ tự và sửa lỗi nối nhầm)**:
   - Thiết lập chung cả 5 khối: `Full cache`, `CM_DW_Football`, **`Redirect rows to no match output`** nối sang nhánh ghi lỗi:
     1. **`Lookup Player`** (`dbo.DIM_Player`): `player_id → Player_ID`, alias **`FK_Player_ID`**.
     2. **`Lookup Club`** (`dbo.DIM_Club`): `player_club_id → Club_ID`, alias **`FK_Club_ID`**.
     3. **`Lookup Game`** (`dbo.DIM_Game`) — **chuyển lên trước `Lookup Competition`**: `game_id → Game_ID`, lấy 6 cột với alias `FK_Game_ID`, `Game_Competition_ID`, `Game_Date`, `Game_Season`, `Game_Home_Club_ID`, `Game_Away_Club_ID`.
     4. **`Lookup Competition`** (`dbo.DIM_Competition`): **`Game_Competition_ID → Competition_ID`**, alias **`FK_Competition_ID`** *(sửa triệt để lỗi bản cũ ở Bước 21 nối nhầm `dc_player_club_id → Club_ID`)*.
     5. **Thêm mới `Lookup Time`** (`dbo.DIM_Time`): **`Game_Date → Full_Date`**, alias **`FK_Time_ID`**.
6. **Thêm mới nhánh đối chiếu ngày & mã giải với `DIM_Game`**:
   - Nối **`Multicast`** sau `Lookup Time`: 1 nhánh tiếp tục nạp chính, 1 nhánh đưa vào **`Conditional Split`** kiểm tra các dòng có `date` hoặc `competition_id` trên nguồn `appearances` bị thiếu hoặc lệch so với `Game_Date` / `Game_Competition_ID`.
7. **Sửa `Derived Column`**:
   - **Xóa** 3 cột cũ: `Time_ID` (đã lấy từ `Lookup Time`), `Goal_Contributions`, `Is_Starter`.
   - **Sửa** 2 cột còn lại để xử lý đủ 3 trường hợp (không gán nhầm sân khách nếu `FK_Club_ID` khác cả đội nhà và đội khách):
     - **`Opponent_Club_ID`**: `FK_Club_ID == Game_Home_Club_ID ? Game_Away_Club_ID : (FK_Club_ID == Game_Away_Club_ID ? Game_Home_Club_ID : NULL(DT_I4))`
     - **`Is_Home_Game`**: `FK_Club_ID == Game_Home_Club_ID ? 1 : (FK_Club_ID == Game_Away_Club_ID ? 0 : NULL(DT_I4))`
8. **Thêm `Row Count` & Sửa `OLE DB Destination` (`[dbo].[FACT_Player_Match_Perf]`)**:
   - Đặt **`Row Count`** trước đích và ở các nhánh lỗi để đối soát số lượng.
   - Trong `OLE DB Destination`: chọn `CM_DW_Football`, `Table or view - fast load`, bật **`Keep nulls`** và **`Check constraints`**, **tắt `Keep identity`**.
   - Trong **Mappings (13 cột)**: **để trống ánh xạ `Appearance_ID`** (SQL Server tự sinh `IDENTITY`), nối **`appearance_id → Source_Appearance_ID`**, `FK_Player_ID → Player_ID`, `FK_Club_ID → Club_ID`, `Opponent_Club_ID → Opponent_Club_ID`, `FK_Competition_ID → Competition_ID`, `FK_Game_ID → Game_ID`, `FK_Time_ID → Time_ID`, `minutes_played → Minutes_Played`, `goals → Goals`, `assists → Assists`, `yellow_cards → Yellow_Cards`, `red_cards → Red_Cards`, `Is_Home_Game → Is_Home_Game`.

---

## 7. CHECKLIST CHẠY THỬ, CHẠY LẠI LÔ VÀ ĐỐI SOÁT SQL SERVER

1. **Kiểm tra trong Visual Studio 2022**:
   - [ ] Mở lại toàn bộ 6 Data Flow, bảo đảm không còn dấu `X` đỏ hoặc cảnh báo lệch kiểu/mất cột `dc_*`.
   - [ ] Bấm **Start** chạy toàn bộ package, kiểm tra tab **Progress / Execution Results** xác nhận thứ tự chạy: `Drop All Tables` $\rightarrow$ `Create All Tables` $\rightarrow$ `Load Dimensions` (`DIM_Club` & `DIM_Competition` xong mới chạy `DIM_Game`) $\rightarrow$ `FACT_Player_Match_Perf`.
   - [ ] Kiểm tra số dòng đi qua từng nhánh loại/nhánh lỗi (`Row Count`) khớp với số dòng đầu vào.
2. **Kiểm tra chế độ chạy lại cùng một lô (giữ dữ liệu)**:
   - [ ] Khi chạy lại không xóa/tạo bảng: tra khóa chính ở các chiều để chèn mới/cập nhật; ở fact dùng `Lookup Source_Appearance_ID` vào `dbo.FACT_Player_Match_Perf` đưa mã đã tồn tại sang nhánh đếm riêng và chỉ chèn mã chưa có.
3. **Đối soát mốc số dòng và tổng độ đo trong SSMS (`DW_Football_Transfermarkt`)**:

| Bảng / Chỉ tiêu đối soát | Mốc tham chiếu chuẩn |
| :--- | :--- |
| `dbo.DIM_Club` | **272** dòng (247 CLB từ CSV + 25 CLB bổ sung giữ `NULL` ở sân, sức chứa, quy mô) |
| `dbo.DIM_Player` | **7.069** dòng (`Date_Of_Birth` kiểu `DATE`, thuộc tính thiếu giữ `NULL`) |
| `dbo.DIM_Competition` | **13** dòng (`Country_Name` của giải quốc tế giữ `NULL` theo nguồn) |
| `dbo.DIM_Game` | **7.280** dòng (mùa `2022`, `2023`, đủ mã giải và 2 mã CLB hợp lệ) |
| `dbo.DIM_Time` | **488** ngày duy nhất (`Time_ID` dạng `YYYYMMDD`, `Is_Weekend = 1` cho ngày `6`, `7`) |
| `dbo.FACT_Player_Match_Perf` | **210.747** lượt ra sân (`Source_Appearance_ID` không trùng, `Appearance_ID` tự sinh) |
| **Tổng độ đo trên 210.747 lượt** | **13.562.727** phút · **19.173** bàn · **14.739** kiến tạo · **28.694** thẻ vàng · **827** thẻ đỏ |
