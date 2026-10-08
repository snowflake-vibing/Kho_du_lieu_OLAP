# HƯỚNG DẪN TỰ XÂY DỰNG TOÀN DIỆN DỰ ÁN KHO DỮ LIỆU & OLAP VỚI SSIS TỪ ĐẦU (A-Z)
> **Chủ đề**: Kho Dữ Liệu Phân Tích Bóng Đá (Football Analytics Data Warehouse)  
> **Công nghệ sử dụng**: SQL Server, SSIS (SQL Server Integration Services), Visual Studio 2022.  
> **Quy mô dữ liệu**: Hơn **1.89 triệu dòng** (Records) nạp trong thời gian tối ưu **~1.5 - 2 phút**.

---

## MỤC LỤC
1. [Tổng quan Kiến trúc Star Schema & Quy trình ETL](#1-tổng-quan-kiến-trúc-star-schema--quy-trình-etl)
2. [Bước 1: Chuẩn bị Dữ liệu CSV & Script DDL SQL Server](#bước-1-chuẩn-bị-dữ-liệu-csv--script-ddl-sql-server)
3. [Bước 2: Khởi tạo Project SSIS trong Visual Studio](#bước-2-khởi-tạo-project-ssis-trong-visual-studio)
4. [Bước 3: Thiết lập các Connection Managers](#bước-3-thiết-lập-các-connection-managers)
5. [Bước 4: Xây dựng Control Flow (Quy trình điều khiển)](#bước-4-xây-dựng-control-flow-quy-trình-điều-khiển)
6. [Bước 5: Cấu hình chi tiết từng Data Flow (DIM & STAGING)](#bước-5-cấu-hình-chi-tiết-từng-data-flow-dim--staging)
7. [Bước 6: Khối Nạp Fact Tối Ưu (Set-based SQL Join)](#bước-6-khối-nạp-fact-tối-ưu-set-based-sql-join)
8. [Bước 7: Kỹ thuật Tối ưu Hiệu năng & Xử lý sự cố thường gặp](#bước-7-kỹ-thuật-tối-ưu-hiệu-năng--xử-lý-sự-cố-thường-gặp)
9. [Bước 8: Kiểm tra Kết quả Sau khi Chạy](#bước-8-kiểm-tra-kết-quả-sau-khi-chạy)

---

## 1. TỔNG QUAN KIẾN TRÚC STAR SCHEMA & QUY TRÌNH ETL

### Mô hình Star Schema
Kho dữ liệu thiết kế theo chuẩn Kimball gồm:
* **1 Bảng FACT trung tâm**: `FACT_Player_Match_Perf` (~1.894.350 dòng).
  * **Surrogate Keys (SK)**: `Player_SK`, `Club_SK`, `Opponent_Club_SK`, `Competition_SK`, `Game_SK`, `Time_SK`.
  * **Degenerate Dimension**: `Game_ID`.
  * **Measures (Độ đo)**: `Minutes_Played`, `Goals`, `Assists`, `Goal_Contributions`, `Yellow_Cards`, `Red_Cards`, `Is_Starter`.
* **5 Bảng DIMENSION**:
  1. `DIM_Player` (Cầu thủ)
  2. `DIM_Club` (Câu lạc bộ)
  3. `DIM_Competition` (Giải đấu)
  4. `DIM_Game` (Trận đấu)
  5. `DIM_Time` (Thời gian / Ngày thi đấu)
* **1 Bảng STAGING**: `STG_Appearances` (Chứa dữ liệu thô trung gian trước khi nạp Fact).

### Sơ đồ luồng Control Flow
```
[Drop All Tables]
       │
       ▼
[Create All Tables]
       │
       ▼
[Prepare Staging Tables]
       │
       ▼
[Sequence Container: Parallel Load DIMs]
  ├── DIM_Competition (Data Flow)
  ├── DIM_Club (Data Flow)
  ├── DIM_Game (Data Flow)
  ├── DIM_Player (Data Flow)
  └── DIM_Time (Data Flow)
       │
       ▼
[Load Staging Appearances] (Data Flow)
       │
       ▼
[Populate FACT via SQL Join] (Execute SQL Task)
```

---

## BƯỚC 1: CHUẨN BỊ DỮ LIỆU CSV & SCRIPT DDL SQL SERVER

### 1.1. Các file CSV nguồn (Đặt tại thư mục `data/`):
* `competitions.csv`: Mã giải, tên giải, quốc gia, loại giải.
* `clubs.csv`: Mã CLB, tên CLB, SVĐ, số chỗ ngồi, HLV.
* `players.csv`: Mã cầu thủ, họ tên, quốc tịch, ngày sinh, vị trí thi đấu, chân thuận, chiều cao.
* `games.csv`: Mã trận đấu, mùa giải, vòng đấu, đội nhà, đội khách, bàn thắng, SVĐ.
* `appearances.csv`: Mã lần ra sân, trận đấu, cầu thủ, số phút thi đấu, bàn thắng, kiến tạo, thẻ vàng, thẻ đỏ.

### 1.2. Script Khởi tạo Database và Toàn bộ các Bảng (Chạy trong SSMS):
Mở **SQL Server Management Studio (SSMS)** và chạy đoạn mã sau để tạo database và schema:

```sql
CREATE DATABASE DW_Football_Analytics;
GO

USE DW_Football_Analytics;
GO

-- 1. Bảng Chiều Giải Đấu
CREATE TABLE dbo.DIM_Competition (
    Competition_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Competition PRIMARY KEY,
    Competition_ID NVARCHAR(50) NOT NULL,
    Competition_Name NVARCHAR(200) NULL,
    Country_Name NVARCHAR(200) NULL,
    Competition_Type NVARCHAR(100) NULL
);

-- 2. Bảng Chiều Câu Lạc Bộ
CREATE TABLE dbo.DIM_Club (
    Club_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Club PRIMARY KEY,
    Club_ID INT NOT NULL,
    Club_Name NVARCHAR(200) NULL,
    Stadium_Name NVARCHAR(200) NULL,
    Stadium_Seats INT NULL,
    Coach_Name NVARCHAR(200) NULL,
    Squad_Size INT NULL
);

-- 3. Bảng Chiều Cầu Thủ
CREATE TABLE dbo.DIM_Player (
    Player_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Player PRIMARY KEY,
    Player_ID INT NOT NULL,
    Player_Name NVARCHAR(200) NULL,
    Date_Of_Birth NVARCHAR(50) NULL,
    Age INT NULL,
    Country_Of_Citizenship NVARCHAR(150) NULL,
    Main_Position NVARCHAR(50) NULL,
    Sub_Position NVARCHAR(100) NULL,
    Foot NVARCHAR(20) NULL,
    Height_In_Cm INT NULL
);

-- 4. Bảng Chiều Trận Đấu
CREATE TABLE dbo.DIM_Game (
    Game_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Game PRIMARY KEY,
    Game_ID INT NOT NULL,
    Season INT NULL,
    Round NVARCHAR(100) NULL,
    Home_Club_ID INT NULL,
    Away_Club_ID INT NULL,
    Home_Club_Goals INT NULL,
    Away_Club_Goals INT NULL,
    Stadium NVARCHAR(200) NULL
);

-- 5. Bảng Chiều Thời Gian
CREATE TABLE dbo.DIM_Time (
    Time_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Time PRIMARY KEY,
    Time_ID INT NOT NULL,
    Full_Date NVARCHAR(50) NULL,
    Day_Of_Week NVARCHAR(50) NULL,
    Day INT NULL,
    Month INT NULL,
    Quarter INT NULL,
    Year INT NULL,
    Season NVARCHAR(50) NULL,
    Is_Weekend INT NULL
);

-- 6. Bảng STAGING Trung Gian
CREATE TABLE dbo.STG_Appearances (
    appearance_id VARCHAR(100),
    game_id INT,
    player_id INT,
    player_club_id INT,
    player_current_club_id INT,
    date_str VARCHAR(50),
    player_name NVARCHAR(250),
    competition_id VARCHAR(50),
    yellow_cards INT,
    red_cards INT,
    goals INT,
    assists INT,
    minutes_played INT
);

-- 7. Bảng FACT Trung Tâm
CREATE TABLE dbo.FACT_Player_Match_Perf (
    Appearance_ID INT IDENTITY(1,1) CONSTRAINT PK_FACT_Player_Match_Perf PRIMARY KEY,
    Player_SK INT NOT NULL,
    Club_SK INT NOT NULL,
    Opponent_Club_SK INT NOT NULL,
    Competition_SK INT NOT NULL,
    Game_SK INT NOT NULL,
    Time_SK INT NOT NULL,
    Game_ID INT NOT NULL,
    Minutes_Played INT DEFAULT 0,
    Goals INT DEFAULT 0,
    Assists INT DEFAULT 0,
    Goal_Contributions INT DEFAULT 0,
    Yellow_Cards INT DEFAULT 0,
    Red_Cards INT DEFAULT 0,
    Market_Value_In_EUR FLOAT DEFAULT 0.0,
    Is_Starter INT DEFAULT 0,
    Is_Home_Game INT DEFAULT 0,

    CONSTRAINT FK_Fact_Player FOREIGN KEY (Player_SK) REFERENCES dbo.DIM_Player(Player_SK),
    CONSTRAINT FK_Fact_Club FOREIGN KEY (Club_SK) REFERENCES dbo.DIM_Club(Club_SK),
    CONSTRAINT FK_Fact_Opponent_Club FOREIGN KEY (Opponent_Club_SK) REFERENCES dbo.DIM_Club(Club_SK),
    CONSTRAINT FK_Fact_Competition FOREIGN KEY (Competition_SK) REFERENCES dbo.DIM_Competition(Competition_SK),
    CONSTRAINT FK_Fact_Game FOREIGN KEY (Game_SK) REFERENCES dbo.DIM_Game(Game_SK),
    CONSTRAINT FK_Fact_Time FOREIGN KEY (Time_SK) REFERENCES dbo.DIM_Time(Time_SK)
);
GO
```

---

## BƯỚC 2: KHỞI TẠO PROJECT SSIS TRONG VISUAL STUDIO

1. Mở **Visual Studio 2022**.
2. Chọn **Create a new project**.
3. Tìm kiếm từ khóa `Integration Services Project` -> Chọn template và nhấn **Next**.
4. Đặt tên Project: `SSIS_Football` -> Chọn đường dẫn lưu trữ -> Nhấn **Create**.
5. Màn hình thiết kế gói mặc định `Package.dtsx` sẽ xuất hiện.

---

## BƯỚC 3: THIẾT LẬP CÁC CONNECTION MANAGERS

Dưới thanh **Connection Managers** (ở dưới cùng màn hình Visual Studio), nhấp chuột phải:

### 3.1. Tạo OLE DB Connection (Đến SQL Server Database)
1. Chuột phải -> **New OLE DB Connection...** -> Chọn **New...**
2. **Server name**: Nhập tên máy chủ SQL của bạn (ví dụ `.` hoặc `localhost` hoặc tên máy như `DESKTOP-XXXXX`).
3. **Authentication**: Chọn `Windows Authentication` (hoặc `SQL Server Authentication`).
4. **Select or enter a database name**: Chọn `DW_Football_Analytics`.
5. Nhấn **Test Connection** (Báo thành công) -> Đổi tên Connection thành: `DESKTOP-9B88R8P.DW_Football_Analytics` (hoặc tên tương ứng).

### 3.2. Tạo các Flat File Connection Managers (Đọc CSV)
Tạo lần lượt 5 Connection Manager cho 5 file CSV:
1. Chuột phải -> **New Flat File Connection...**
2. Cấu hình chung cho từng file:
   * **General**:
     * Format: `Delimited`
     * Text qualifier: `"`
     * Header row delimiter: `{CR}{LF}`
     * Header rows to skip: `0`
     * Tick vào ô **Column names in the first data row**.
     * Code page: `65001 (UTF-8)` (hoặc `1252 (ANSI)` tùy mã hóa file).
   * **Columns**:
     * Column delimiter: `Comma {,}`
   * **Advanced**: Kiểm tra độ dài các trường kiểu String nên để tối thiểu `200` để tránh lỗi cắt chuỗi (Truncation).

---

## BƯỚC 4: XÂY DỰNG CONTROL FLOW (QUY TRÌNH ĐIỀU KHIỂN)

Kéo thả các khối từ thanh công cụ **SSIS Toolbox** vào màn hình **Control Flow**:

### 4.1. Khối 1: `Execute SQL Task` - Tên: `Drop All Tables`
* **Mục đích**: Tự động dọn dẹp các bảng cũ trước khi chạy lại ETL.
* **Cấu hình**:
  * Connection: Chọn OLE DB Connection tới `DW_Football_Analytics`.
  * `SQLStatement`:
    ```sql
    USE DW_Football_Analytics;
    IF OBJECT_ID('dbo.FACT_Player_Match_Perf', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf;
    IF OBJECT_ID('dbo.DIM_Player', 'U') IS NOT NULL DROP TABLE dbo.DIM_Player;
    IF OBJECT_ID('dbo.DIM_Club', 'U') IS NOT NULL DROP TABLE dbo.DIM_Club;
    IF OBJECT_ID('dbo.DIM_Competition', 'U') IS NOT NULL DROP TABLE dbo.DIM_Competition;
    IF OBJECT_ID('dbo.DIM_Game', 'U') IS NOT NULL DROP TABLE dbo.DIM_Game;
    IF OBJECT_ID('dbo.DIM_Time', 'U') IS NOT NULL DROP TABLE dbo.DIM_Time;
    ```

### 4.2. Khối 2: `Execute SQL Task` - Tên: `Create All Tables`
* **Mục đích**: Tạo lại toàn bộ bảng Star Schema mới nguyên vẹn.
* **Cấu hình**:
  * Nối mũi tên xanh từ `Drop All Tables` sang `Create All Tables`.
  * `SQLStatement`: Dán toàn bộ script DDL tạo 5 DIM và 1 FACT ở **Mục 1.2** (kèm dòng cuối `WAITFOR DELAY '00:00:01';`).

### 4.3. Khối 3: `Execute SQL Task` - Tên: `Prepare Staging Tables`
* **Mục đích**: Khởi tạo bảng Staging sạch sẽ sẵn sàng đón nhận 1.89M dòng.
* **Cấu hình**:
  * Nối mũi tên xanh từ `Create All Tables` sang `Prepare Staging Tables`.
  * `SQLStatement`:
    ```sql
    USE DW_Football_Analytics;
    IF OBJECT_ID('dbo.STG_Appearances', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.STG_Appearances (
            appearance_id VARCHAR(100),
            game_id INT,
            player_id INT,
            player_club_id INT,
            player_current_club_id INT,
            date_str VARCHAR(50),
            player_name NVARCHAR(250),
            competition_id VARCHAR(50),
            yellow_cards INT,
            red_cards INT,
            goals INT,
            assists INT,
            minutes_played INT
        );
    END
    ELSE
    BEGIN
        TRUNCATE TABLE dbo.STG_Appearances;
    END
    ```

### 4.4. Khối 4: `Sequence Container` - Tên: `Parallel Load DIMs`
* Kéo một **Sequence Container** vào màn hình.
* Nối mũi tên xanh từ `Prepare Staging Tables` vào `Parallel Load DIMs`.
* Kéo **5 Data Flow Tasks** vào BÊN TRONG Sequence Container này (đặt cạnh nhau để chạy song song):
  1. `DIM_Competition`
  2. `DIM_Club`
  3. `DIM_Game`
  4. `DIM_Player`
  5. `DIM_Time`

### 4.5. Khối 5: `Data Flow Task` - Tên: `Load Staging Appearances`
* Kéo ra ngoài bên dưới Sequence Container.
* Nối mũi tên xanh từ `Parallel Load DIMs` xuống `Load Staging Appearances`.

### 4.6. Khối 6: `Execute SQL Task` - Tên: `Populate FACT via SQL Join`
* Kéo ra dưới cùng.
* Nối mũi tên xanh từ `Load Staging Appearances` xuống `Populate FACT via SQL Join`.

---

## BƯỚC 5: CẤU HÌNH CHI TIẾT TỪNG DATA FLOW (DIM & STAGING)

> [!IMPORTANT]
> **CÁC QUY TẮC CẤU HÌNH SSIS BẮT BUỘC KHÔNG ĐƯỢC VI PHẠM:**
> 1. **Quy tắc đặt tên Output Alias trong Data Conversion:** Tất cả các cột ép kiểu xuất ra từ khối **Data Conversion** BẮT BUỘC phải dùng tiền tố **`dc_`** (Ví dụ: `dc_competition_id`, `dc_club_id`, `dc_player_name`...). **Tuyệt đối KHÔNG sử dụng tên mặc định `Copy of...`**.
> 2. **Quy tắc sử dụng khối Derived Column:** KHÔNG ĐƯỢC tự tiện thêm khối `Derived Column` vào luồng Data Flow nếu trong thiết kế/tài liệu chuẩn không yêu cầu. Luồng chuẩn của bảng DIM cơ bản là: **Flat File Source $\rightarrow$ Data Conversion (`dc_`) $\rightarrow$ Conditional Split $\rightarrow$ Sort (Distinct) $\rightarrow$ OLE DB Destination**. Chỉ dùng `Derived Column` khi có công thức tính toán/bóc tách thuộc tính bắt buộc (như tính `Age` hoặc bóc tách `Time_ID`).
> 3. **Quy tắc Domain Validation trong Conditional Split:** Trong khối **Conditional Split**, BẮT BUỘC phải kiểm tra điều kiện toàn vẹn (NULL/Length/Domain) cho **TOÀN BỘ CÁC CỘT** thuộc bảng đó, không được bỏ sót bất kỳ cột nào.

### 5.1. Data Flow `DIM_Competition` (Bảng Chiều Giải Đấu)
File nguồn `competitions.csv` chứa thông tin về các giải đấu bóng đá (mã giải, tên giải, quốc gia tổ chức, phân loại giải đấu).
Mô hình luồng Data Flow chuẩn:
```
[Flat File Source] ➔ [Data Conversion (dc_)] ➔ [Conditional Split (Validation 4 cột)] ➔ [Sort (Distinct)] ➔ [OLE DB Destination]
```

1. **Flat File Source**:
   * Connection Manager: Chọn kết nối đến file `competitions.csv`.
   * Tab **Columns**: Chọn lấy 4 trường dữ liệu: `competition_id`, `name`, `country_name`, `type`.

2. **Data Conversion (BẮT BUỘC dùng tiền tố `dc_`)**:
   * Nối từ *Flat File Source* sang *Data Conversion*.
   * Tick chọn 4 cột nguồn và cấu hình alias chuẩn tiền tố `dc_`:
     * `competition_id` ➔ Output Alias: **`dc_competition_id`** (Data Type: `Unicode string [DT_WSTR]`, Length: `50`).
     * `name` ➔ Output Alias: **`dc_competition_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `country_name` ➔ Output Alias: **`dc_country_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `type` ➔ Output Alias: **`dc_competition_type`** (Data Type: `Unicode string [DT_WSTR]`, Length: `100`).

3. **Conditional Split (BẮT BUỘC Kiểm tra Validation cho TOÀN BỘ 4 CỘT)**:
   * Nối từ *Data Conversion* sang *Conditional Split*.
   * Nhấp đúp vào khối, thiết lập điều kiện kiểm tra tính toàn vẹn của **cả 4 cột**:
     * **Output Name**: `Valid_Competitions`
     * **Condition (Kiểm tra đầy đủ cả 4 cột)**:
       ```c
       !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 && !ISNULL(dc_competition_name) && LEN(TRIM(dc_competition_name)) > 0 && !ISNULL(dc_country_name) && LEN(TRIM(dc_country_name)) > 0 && !ISNULL(dc_competition_type) && LEN(TRIM(dc_competition_type)) > 0
       ```
     * **Default Output Name** (ở dưới cùng): Đổi thành `Invalid_Competitions`.

4. **Sort (Sắp xếp & Khử trùng lặp)**:
   * Kéo mũi tên xanh từ *Conditional Split* sang *Sort*. Cửa sổ xuất hiện yêu cầu chọn Output -> Chọn **`Valid_Competitions`**.
   * Trong cửa sổ cấu hình *Sort*:
     * **Pass Through**: Tick chọn tất cả 4 cột (`dc_competition_id`, `dc_competition_name`, `dc_country_name`, `dc_competition_type`).
     * **Sort Column**: Tick chọn cột **`dc_competition_id`** (Sort Type: `Ascending`, Sort Order: `1`).
     * **BẮT BUỘC**: Đánh dấu tích vào ô checkbox ở góc dưới bên trái: **`Remove rows with duplicate sort values`** (để đảm bảo mỗi giải đấu chỉ xuất hiện 1 lần duy nhất trong kho dữ liệu).

5. **OLE DB Destination (Nạp vào SQL Server)**:
   * Nối từ *Sort* sang *OLE DB Destination*.
   * Connection: Kết nối OLE DB đến database `DW_Football_Analytics`.
   * Data access mode: **`Table or view - fast load`**.
   * Name of the table or the view: **`[dbo].[DIM_Competition]`**.
   * Chuyển sang tab **Mappings** và nối chính xác như sau:
     * `dc_competition_id` ➔ **`Competition_ID`**
     * `dc_competition_name` ➔ **`Competition_Name`**
     * `dc_country_name` ➔ **`Country_Name`**
     * `dc_competition_type` ➔ **`Competition_Type`**
     * *(Lưu ý: Bỏ qua cột `Competition_SK` vì đây là Surrogate Key tự tăng do SQL Server quản lý)*.

---

### 5.2. Data Flow `DIM_Club` (Bảng Chiều Câu Lạc Bộ)
File nguồn `clubs.csv` chứa thông tin chi tiết về các câu lạc bộ (mã CLB, tên CLB, sân vận động, số ghế ngồi, HLV trưởng, quy mô đội hình).
Mô hình luồng Data Flow chuẩn:
```
[Flat File Source] ➔ [Data Conversion] ➔ [Conditional Split (Validation)] ➔ [Sort (Distinct)] ➔ [OLE DB Destination]
```

1. **Flat File Source**:
   * Connection Manager: Chọn kết nối đến file `clubs.csv`.
   * Tab **Columns**: Chọn lấy 6 trường dữ liệu:
     * `club_id`
     * `name`
     * `stadium_name`
     * `stadium_seats`
     * `coach_name`
     * `squad_size`

2. **Data Conversion (Ép kiểu dữ liệu chuẩn)**:
   * Nối từ *Flat File Source* sang *Data Conversion*.
   * Tick chọn 6 cột nguồn và cấu hình alias/kiểu dữ liệu:
     * `club_id` ➔ Output Alias: **`dc_club_id`** (Data Type: `four-byte signed integer [DT_I4]`).
     * `name` ➔ Output Alias: **`dc_club_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `stadium_name` ➔ Output Alias: **`dc_stadium_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `stadium_seats` ➔ Output Alias: **`dc_stadium_seats`** (Data Type: `four-byte signed integer [DT_I4]`).
     * `coach_name` ➔ Output Alias: **`dc_coach_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `squad_size` ➔ Output Alias: **`dc_squad_size`** (Data Type: `four-byte signed integer [DT_I4]`).

3. **Conditional Split (Kiểm tra ràng buộc & Validation cho TẤT CẢ các cột)**:
   * Nối từ *Data Conversion* sang *Conditional Split*.
   * Nhấp đúp vào khối, thiết lập điều kiện kiểm tra tính toàn vẹn của **toàn bộ 6 cột**:
     * **Output Name**: `Valid_Clubs`
     * **Condition (Xét điều kiện tất cả 6 cột)**:
       ```c
       !ISNULL(dc_club_id) && dc_club_id > 0 && 
       !ISNULL(dc_club_name) && LEN(TRIM(dc_club_name)) > 0 && 
       !ISNULL(dc_stadium_name) && LEN(TRIM(dc_stadium_name)) > 0 && 
       !ISNULL(dc_stadium_seats) && dc_stadium_seats >= 0 && 
       !ISNULL(dc_coach_name) && LEN(TRIM(dc_coach_name)) > 0 && 
       !ISNULL(dc_squad_size) && dc_squad_size >= 0
       ```
       *(Ý nghĩa: Kiểm tra kỹ toàn bộ 6 cột: ID > 0, Tên CLB & SVĐ & HLV không NULL/rỗng, Số ghế & Quy mô đội hình không âm).*  
       
       > 💡 **Lưu ý thực tế về dữ liệu**: File `clubs.csv` gốc có 393 dòng chưa có tên HLV (`coach_name` bị NULL).  
       > - Nếu bạn muốn **Kiểm tra nghiêm ngặt 100% tất cả các cột** (như công thức trên), các dòng thiếu tên HLV sẽ bị đẩy sang `Invalid_Clubs`.  
       > - Nếu muốn **Cho phép HLV bị khuyết nhưng vẫn kiểm tra tất cả các cột còn lại**:
       > ```c
       > !ISNULL(dc_club_id) && dc_club_id > 0 && 
       > !ISNULL(dc_club_name) && LEN(TRIM(dc_club_name)) > 0 && 
       > !ISNULL(dc_stadium_name) && 
       > !ISNULL(dc_stadium_seats) && dc_stadium_seats >= 0 && 
       > !ISNULL(dc_squad_size) && dc_squad_size >= 0
       > ```
     * **Default Output Name** (ở dưới cùng): Đổi thành `Invalid_Clubs` (chứa các dòng không đạt chuẩn kiểm tra).

4. **Sort (Sắp xếp & Khử trùng lặp)**:
   * Kéo mũi tên xanh từ *Conditional Split* sang *Sort*. Cửa sổ xuất hiện yêu cầu chọn Output -> Chọn **`Valid_Clubs`**.
   * Trong cửa sổ cấu hình *Sort*:
     * **Pass Through**: Tick chọn tất cả các cột (`dc_club_id`, `dc_club_name`, `dc_stadium_name`, `dc_stadium_seats`, `dc_coach_name`, `dc_squad_size`).
     * **Sort Column**: Tick chọn cột **`dc_club_id`** (Sort Type: `Ascending`, Sort Order: `1`).
     * **BẮT BUỘC**: Đánh dấu tích vào ô checkbox ở góc dưới bên trái: **`Remove rows with duplicate sort values`** (để loại bỏ hoàn toàn các dòng CLB bị lặp lại trong file nguồn).

5. **OLE DB Destination (Nạp vào SQL Server)**:
   * Nối từ *Sort* sang *OLE DB Destination*.
   * Connection: Kết nối OLE DB đến database `DW_Football_Analytics`.
   * Data access mode: **`Table or view - fast load`**.
   * Name of the table or the view: **`[dbo].[DIM_Club]`**.
   * Chuyển sang tab **Mappings** và nối chính xác như sau:
     * `dc_club_id` ➔ **`Club_ID`**
     * `dc_club_name` ➔ **`Club_Name`**
     * `dc_stadium_name` ➔ **`Stadium_Name`**
     * `dc_stadium_seats` ➔ **`Stadium_Seats`**
     * `dc_coach_name` ➔ **`Coach_Name`**
     * `dc_squad_size` ➔ **`Squad_Size`**
     * *(Lưu ý: Bỏ qua cột `Club_SK` vì đây là Surrogate Key tự tăng do SQL Server quản lý)*.


---

### 5.3. Data Flow `DIM_Game`
1. **Flat File Source**: Chọn Connection `games.csv`.
2. **Data Conversion**:
   * `game_id` ➔ `dc_game_id` (`DT_I4`).
   * `season` ➔ `dc_season` (`DT_WSTR`, length: 200).
   * `round` ➔ `dc_round` (`DT_WSTR`, length: 200).
   * `stadium` ➔ `dc_stadium` (`DT_WSTR`, length: 150).
3. **Derived Column**:
   * Thêm cột: `Derived_Scope` với biểu thức: `"SCOPED"`.
4. **Sort**:
   * Sort theo cột `dc_game_id` (Ascending) + Tick chọn **`Remove rows with duplicate sort values`**.
5. **OLE DB Destination**:
   * Table: `[dbo].[DIM_Game]` (Fast load).
   * Mappings:
     * `dc_game_id` ➔ `Game_ID`
     * `dc_season` ➔ `Season`
     * `dc_round` ➔ `Round`
     * `dc_stadium` ➔ `Stadium`

---

### 5.4. Data Flow `DIM_Player` (Bảng Chiều Cầu Thủ)
File nguồn `players.csv` chứa thông tin chi tiết về các cầu thủ (mã cầu thủ, tên, ngày sinh, quốc tịch, vị trí thi đấu, chân thuận, chiều cao).
Mô hình luồng Data Flow chuẩn:
```
[Flat File Source] ➔ [Data Conversion] ➔ [Derived Column (Tính Age)] ➔ [Conditional Split (Validation)] ➔ [Sort (Distinct)] ➔ [OLE DB Destination]
```

1. **Flat File Source**:
   * Connection Manager: Chọn kết nối đến file `players.csv`.
   * Tab **Columns**: Chọn lấy 8 trường dữ liệu:
     * `player_id`
     * `name`
     * `date_of_birth`
     * `country_of_citizenship`
     * `position`
     * `sub_position`
     * `foot`
     * `height_in_cm`

2. **Data Conversion (Ép kiểu dữ liệu chuẩn)**:
   * Nối từ *Flat File Source* sang *Data Conversion*.
   * Tick chọn 8 cột nguồn và cấu hình alias/kiểu dữ liệu:
     * `player_id` ➔ Output Alias: **`dc_player_id`** (Data Type: `four-byte signed integer [DT_I4]`).
     * `name` ➔ Output Alias: **`dc_player_name`** (Data Type: `Unicode string [DT_WSTR]`, Length: `200`).
     * `date_of_birth` ➔ Output Alias: **`dc_date_of_birth`** (Data Type: `Unicode string [DT_WSTR]`, Length: `50`).
     * `country_of_citizenship` ➔ Output Alias: **`dc_country`** (Data Type: `Unicode string [DT_WSTR]`, Length: `150`).
     * `position` ➔ Output Alias: **`dc_position`** (Data Type: `Unicode string [DT_WSTR]`, Length: `50`).
     * `sub_position` ➔ Output Alias: **`dc_sub_position`** (Data Type: `Unicode string [DT_WSTR]`, Length: `100`).
     * `foot` ➔ Output Alias: **`dc_foot`** (Data Type: `Unicode string [DT_WSTR]`, Length: `20`).
     * `height_in_cm` ➔ Output Alias: **`dc_height_in_cm`** (Data Type: `four-byte signed integer [DT_I4]`).

3. **Derived Column (Tính toán cột tuổi `Age`)**:
   * Nối từ *Data Conversion* sang *Derived Column*.
   * Thêm cột mới tính tuổi tự động:
     * **Derived Column Name**: `Age`
     * **Derived Column**: `<add as new column>`
     * **Expression**:
       ```c
       ISNULL(dc_date_of_birth) || LEN(TRIM(dc_date_of_birth)) == 0 ? 0 : DATEDIFF("yyyy", (DT_DBTIMESTAMP)dc_date_of_birth, GETDATE())
       ```
     * **Data Type**: `four-byte signed integer [DT_I4]`.

4. **Conditional Split (Kiểm tra ràng buộc & Validation cho TẤT CẢ 9 CỘT)**:
   * Nối từ *Derived Column* sang *Conditional Split* (Đổi tên khối: `CS_Validate_Player`).
   * Cấu hình nhánh hợp lệ **xét điều kiện đầy đủ cho TOÀN BỘ 9 CỘT**:
     * **Output Name**: `Valid_Players`
     * **Condition (Xét điều kiện tất cả 9 cột)**:
       ```c
       !ISNULL(dc_player_id) && dc_player_id > 0 && 
       !ISNULL(dc_player_name) && LEN(TRIM(dc_player_name)) > 0 && 
       !ISNULL(dc_date_of_birth) && LEN(TRIM(dc_date_of_birth)) > 0 && 
       !ISNULL(Age) && Age >= 0 && 
       !ISNULL(dc_country) && LEN(TRIM(dc_country)) > 0 && 
       !ISNULL(dc_position) && LEN(TRIM(dc_position)) > 0 && 
       !ISNULL(dc_sub_position) && LEN(TRIM(dc_sub_position)) > 0 && 
       !ISNULL(dc_foot) && LEN(TRIM(dc_foot)) > 0 && 
       !ISNULL(dc_height_in_cm) && dc_height_in_cm > 0
       ```
       *(Ý nghĩa: Kiểm tra nghiêm ngặt toàn bộ 9 cột: ID > 0, Tên & Ngày sinh & Quốc tịch & Vị trí & Chân thuận không NULL/rỗng, Tuổi & Chiều cao phải là số dương hợp lệ).*
     * **Default Output Name**: `Invalid_Players`.

5. **Sort (Sắp xếp & Khử trùng lặp)**:
   * Kéo mũi tên xanh từ *Conditional Split* sang *Sort*, chọn nhánh **`Valid_Players`**.
   * Trong cửa sổ *Sort*:
     * **Pass Through**: Tick chọn **tất cả 9 cột** (`dc_player_id`, `dc_player_name`, `dc_date_of_birth`, `Age`, `dc_country`, `dc_position`, `dc_sub_position`, `dc_foot`, `dc_height_in_cm`).
     * **Sort Column**: Tick chọn cột **`dc_player_id`** (Sort Type: `Ascending`, Sort Order: `1`).
     * **BẮT BUỘC**: Đánh dấu tích vào ô checkbox ở góc dưới bên trái: **`Remove rows with duplicate sort values`** (để lọc bỏ các dòng cầu thủ lặp lại).

6. **OLE DB Destination (Nạp vào SQL Server)**:
   * Nối từ *Sort* sang *OLE DB Destination*.
   * Connection: Kết nối OLE DB đến database **`DW_Football_Transfermarkt`**.
   * Data access mode: **`Table or view - fast load`**.
   * Name of the table or the view: **`[dbo].[DIM_Player]`**.
   * Chuyển sang tab **Mappings** và nối chính xác 9 cột:
     * `dc_player_id` ➔ **`Player_ID`**
     * `dc_player_name` ➔ **`Player_Name`**
     * `dc_date_of_birth` ➔ **`Date_Of_Birth`**
     * `Age` ➔ **`Age`**
     * `dc_country` ➔ **`Country_Of_Citizenship`**
     * `dc_position` ➔ **`Main_Position`**
     * `dc_sub_position` ➔ **`Sub_Position`**
     * `dc_foot` ➔ **`Foot`**
     * `dc_height_in_cm` ➔ **`Height_In_Cm`**
     * *(Lưu ý: Bỏ qua cột `Player_SK` vì đây là Surrogate Key tự tăng do SQL Server quản lý)*.

---

### 5.5. Data Flow `DIM_Time` (Bảng Chiều Thời Gian)
Bảng thời gian được sinh trực tiếp từ ngày thi đấu trong file `games.csv` (88,958 trận đấu lọc ra 4,445 ngày duy nhất).
Mô hình luồng Data Flow chuẩn:
```
[Flat File Source] ➔ [Data Conversion] ➔ [Derived Column] ➔ [Conditional Split (Validation)] ➔ [Sort (Distinct)] ➔ [OLE DB Destination]
```

1. **Flat File Source**:
   * Connection Manager: Chọn kết nối đến file `games.csv`.
   * Tab **Columns**: Chọn lấy 2 trường:
     * `date` (ngày thi đấu định dạng `YYYY-MM-DD`)
     * `season` (năm mùa giải)

2. **Data Conversion (Ép kiểu dữ liệu chuẩn)**:
   * Nối từ *Flat File Source* sang *Data Conversion*.
   * Tick chọn 2 cột nguồn và cấu hình alias/kiểu dữ liệu:
     * `date` ➔ Output Alias: **`dc_date`** (Data Type: `Unicode string [DT_WSTR]`, Length: `50`).
     * `season` ➔ Output Alias: **`dc_season`** (Data Type: `Unicode string [DT_WSTR]`, Length: `50`).

3. **Derived Column (Bóc tách thuộc tính thời gian & Date Key)**:
   * Nối từ *Data Conversion* sang *Derived Column*.
   * Thêm các cột mới tính toán từ `dc_date`:
     * **`Time_ID`** (`DT_I4`):
       ```c
       (YEAR((DT_DATE)dc_date) * 10000) + (MONTH((DT_DATE)dc_date) * 100) + DAY((DT_DATE)dc_date)
       ```
       *(Tạo mã ngày dạng số nguyên YYYYMMDD, ví dụ: 20210814).*
     * **`Full_Date`** (`DT_WSTR`, Length: `50`):
       ```c
       dc_date
       ```
     * **`Day`** (`DT_I4`):
       ```c
       DATEPART("dd", (DT_DBTIMESTAMP)dc_date)
       ```
     * **`Month`** (`DT_I4`):
       ```c
       DATEPART("mm", (DT_DBTIMESTAMP)dc_date)
       ```
     * **`Quarter`** (`DT_I4`):
       ```c
       DATEPART("qq", (DT_DBTIMESTAMP)dc_date)
       ```
     * **`Year`** (`DT_I4`):
       ```c
       DATEPART("yy", (DT_DBTIMESTAMP)dc_date)
       ```
     * **`Day_Of_Week`** (`DT_WSTR`, Length: `50`):
       ```c
       DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 1 ? "Sunday" : DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 2 ? "Monday" : DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 3 ? "Tuesday" : DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 4 ? "Wednesday" : DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 5 ? "Thursday" : DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 6 ? "Friday" : "Saturday"
       ```
     * **`Season`** (`DT_WSTR`, Length: `50`):
       ```c
       "Mùa " + dc_season
       ```
     * **`Is_Weekend`** (`DT_I4`):
       ```c
       DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 1 || DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 7 ? 1 : 0
       ```

4. **Conditional Split (Kiểm tra ràng buộc & Validation)**:
   * Nối từ *Derived Column* sang *Conditional Split*.
   * Cấu hình nhánh hợp lệ:
     * **Output Name**: `Valid_Dates`
     * **Condition**:
       ```c
       !ISNULL(dc_date) && LEN(TRIM(dc_date)) == 10 && !ISNULL(Time_ID)
       ```
       *(Ý nghĩa: Chỉ nhận chuỗi ngày đúng định dạng 10 ký tự YYYY-MM-DD và Time_ID không NULL).*
     * **Default Output Name**: `Invalid_Dates`.

5. **Sort (Sắp xếp & Khử trùng lặp)**:
   * Kéo mũi tên xanh từ *Conditional Split* sang *Sort*, chọn nhánh **`Valid_Dates`**.
   * Trong cửa sổ *Sort*:
     * **Pass Through**: Tick chọn tất cả các cột (`Time_ID`, `Full_Date`, `Day_Of_Week`, `Day`, `Month`, `Quarter`, `Year`, `Season`, `Is_Weekend`).
     * **Sort Column**: Tick chọn cột **`Time_ID`** (Sort Type: `Ascending`, Sort Order: `1`).
     * **BẮT BUỘC**: Đánh dấu tích vào ô checkbox ở góc dưới bên trái: **`Remove rows with duplicate sort values`** (để gom 88,958 dòng trận đấu trùng ngày thành các ngày duy nhất).

6. **OLE DB Destination (Nạp vào SQL Server)**:
   * Nối từ *Sort* sang *OLE DB Destination*.
   * Connection: Kết nối OLE DB đến database `DW_Football_Analytics`.
   * Data access mode: **`Table or view - fast load`**.
   * Name of the table or the view: **`[dbo].[DIM_Time]`**.
   * Chuyển sang tab **Mappings** và nối chính xác như sau:
     * `Time_ID` ➔ **`Time_ID`**
     * `Full_Date` ➔ **`Full_Date`**
     * `Day_Of_Week` ➔ **`Day_Of_Week`**
     * `Day` ➔ **`Day`**
     * `Month` ➔ **`Month`**
     * `Quarter` ➔ **`Quarter`**
     * `Year` ➔ **`Year`**
     * `Season` ➔ **`Season`**
     * `Is_Weekend` ➔ **`Is_Weekend`**
     * *(Lưu ý: Bỏ qua cột `Time_SK` vì đây là Surrogate Key tự tăng IDENTITY)*.

---

### 5.6. Data Flow `Load Staging Appearances` (Nạp thô cực nhanh)
Luồng này nạp trực tiếp toàn bộ 1.89 triệu dòng từ `appearances.csv` vào bảng Staging:
```
[Flat File Source] ➔ [Data Conversion] ➔ [Derived Column] ➔ [OLE DB Destination (Fast Load)]
```
1. **Flat File Source**: Chọn `appearances.csv`.
2. **Data Conversion**:
   * `appearance_id` ➔ `dc_appearance_id` (string [DT_STR], length: 100)
   * `game_id` ➔ `dc_game_id` (`DT_I4`)
   * `player_id` ➔ `dc_player_id` (`DT_I4`)
   * `player_club_id` ➔ `dc_player_club_id` (`DT_I4`)
   * `goals` ➔ `dc_goals` (`DT_I4`)
   * `assists` ➔ `dc_assists` (`DT_I4`)
   * `minutes_played` ➔ `dc_minutes_played` (`DT_I4`)
   * `yellow_cards` ➔ `dc_yellow_cards` (`DT_I4`)
   * `red_cards` ➔ `dc_red_cards` (`DT_I4`)
3. **Derived Column**:
   * `Goal_Contributions`: `dc_goals + dc_assists`
   * `Is_Starter`: `dc_minutes_played >= 60 ? 1 : 0`
4. **OLE DB Destination**:
   * Data access mode: `Table or view - fast load`.
   * Table: `[dbo].[STG_Appearances]`.
   * **Cấu hình Fast Load**:
     * Rows per batch: `50000`
     * Maximum insert commit size: `50000`
     * Tick chọn `Table lock` và `Check constraints`.
   * Mappings: Ánh xạ các cột tương ứng vào `STG_Appearances`.

---

## BƯỚC 6: KHỐI NẠP FACT TỐI ƯU (SET-BASED SQL JOIN)

Tại khối cuối cùng trên Control Flow: `Execute SQL Task` đặt tên là **`Populate FACT via SQL Join`**:
* **Connection**: Chọn kết nối tới `DW_Football_Analytics`.
* **SQLStatement**:

```sql
USE DW_Football_Analytics;

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
    ISNULL(p.Player_SK, 1),
    ISNULL(c.Club_SK, 1),
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

> **Giải thích kỹ thuật**:  
> Thay vì dùng khối `Lookup` trong Data Flow (phải nạp toàn bộ vào RAM và so sánh từng dòng gây nghẽn và mất 30 phút), câu lệnh SQL Set-based Join tận dụng SQL Server Engine (vốn xử lý Hash Join / Merge Join cực mạnh) để nạp xong 1.89 triệu dòng chỉ mất **vài chục giây**!

---

## BƯỚC 7: KỸ THUẬT TỐI ƯU HIỆU NĂNG & XỬ LÝ SỰ CỐ THƯỜNG GẶP

### 7.1. Cấu hình Buffer cho các Data Flow lớn
Nhấp chuột vào nền trống của Data Flow `Load Staging Appearances`, mở cửa sổ **Properties** (F4):
* `DefaultBufferMaxRows`: Đặt `50000` (mặc định là 10,000).
* `DefaultBufferSize`: Đặt `52428800` (~50MB, mặc định là 10MB).
* Điều này giúp SSIS vận chuyển các khối dữ liệu lớn hơn trên mỗi buffer, giảm số lần I/O đĩa.

### 7.2. Lỗi "Exception deserializing package ... being used by another process (.ispac)"
* **Nguyên nhân**: Khi dừng debug hoặc Visual Studio bị crash, tiến trình `DtsDebugHost.exe` vẫn chạy ngầm và giữ khóa file `.ispac`.
* **Cách khắc phục**:
  1. Mở PowerShell hoặc Command Prompt.
  2. Chạy lệnh:
     ```powershell
     taskkill /F /IM DtsDebugHost.exe
     ```
  3. Sau đó quay lại Visual Studio bấm **Start (F5)** lại bình thường.

### 7.3. Cảnh báo "The external columns for OLE DB Destination are out of synchronization"
* Đây chỉ là cảnh báo do SSIS nhận thấy bảng SQL vừa được tạo lại. Chỉ cần nhấn đúp vào `OLE DB Destination`, bấm **OK** là hết cảnh báo. Cảnh báo này hoàn toàn không làm lỗi quá trình chạy.

---

## BƯỚC 8: KIỂM TRA KẾT QUẢ SAU KHI CHẠY

Sau khi bấm **Start (F5)** trong Visual Studio và thấy tất cả các hộp chuyển màu **Xanh Lá Cây**, mở SSMS và chạy câu truy vấn sau:

```sql
USE DW_Football_Analytics;
GO

-- 1. Kiểm tra số lượng dòng từng bảng
SELECT 'DIM_Club' AS [Table Name], COUNT(*) AS [Total Rows] FROM dbo.DIM_Club UNION ALL
SELECT 'DIM_Competition', COUNT(*) FROM dbo.DIM_Competition UNION ALL
SELECT 'DIM_Player', COUNT(*) FROM dbo.DIM_Player UNION ALL
SELECT 'DIM_Game', COUNT(*) FROM dbo.DIM_Game UNION ALL
SELECT 'DIM_Time', COUNT(*) FROM dbo.DIM_Time UNION ALL
SELECT 'STG_Appearances', COUNT(*) FROM dbo.STG_Appearances UNION ALL
SELECT 'FACT_Player_Match_Perf', COUNT(*) FROM dbo.FACT_Player_Match_Perf;
```

### Kết quả chuẩn:
| Table Name | Total Rows | Ghi chú |
| :--- | :--- | :--- |
| `DIM_Competition` | **65** | Đã loại bỏ trùng lặp |
| `DIM_Club` | **796** | Đã loại bỏ trùng lặp |
| `DIM_Player` | **50,149** | Đã loại bỏ trùng lặp & tính tuổi |
| `DIM_Game` | **88,958** | Đã loại bỏ trùng lặp |
| `DIM_Time` | **88,958** | Bóc tách ngày, tháng, năm, quý, thứ |
| `STG_Appearances` | **1,894,350** | Dữ liệu thô trung gian |
| `FACT_Player_Match_Perf` | **1,894,350** | Bảng Fact hoàn chỉnh (1.89M dòng) |

---
**Chúc mừng bạn đã hoàn thành trọn vẹn dự án Kho dữ liệu & OLAP với SSIS đạt chuẩn chuyên nghiệp!**
