# HƯỚNG DẪN SSAS - PHẦN 2: DATA SOURCE VIEW (DSV) & 6 DIMENSIONS

---

## 1. MỤC TIÊU

Tạo **Data Source View (`DW_Football_Transfermarkt.dsv`)** chứa 6 bảng vật lý từ `DW_Football_Transfermarkt` cùng các **Named Calculations** và **Named Queries** cần thiết để đồng bộ với lược đồ mới của Chương 1, sau đó xây dựng đầy đủ **6 Database Dimensions** phục vụ khối Cube đa chiều.

---

## 2. TẠO DATA SOURCE VIEW (`DW_Football_Transfermarkt.dsv`)

### Bước 1: Đưa 6 bảng vật lý vào DSV
1. Trong Solution Explorer, bấm chuột phải vào **Data Source Views** $\rightarrow$ chọn **New Data Source View...** $\rightarrow$ nhấn **Next >**.
2. Chọn Data Source **`DW_Football_Transfermarkt`** $\rightarrow$ nhấn **Next >**.
3. Tại màn hình **Select Tables and Views**, chuyển cả 6 bảng sang cột *Included objects*:
   - `FACT_Player_Match_Perf` (210.747 dòng)
   - `DIM_Player` (7.069 dòng)
   - `DIM_Club` (272 dòng)
   - `DIM_Competition` (13 dòng)
   - `DIM_Game` (7.280 dòng)
   - `DIM_Time` (488 dòng)
4. Đặt tên DSV là **`DW_Football_Transfermarkt`** $\rightarrow$ nhấn **Finish**.
5. Kiểm tra các đường nối khóa ngoại tự động nhận diện từ DDL (`schema_warehouse.sql`), bao gồm:
   - `FACT_Player_Match_Perf` nối tới `DIM_Player`, `DIM_Club` (`Club_ID` và `Opponent_Club_ID`), `DIM_Competition`, `DIM_Game`, `DIM_Time`.
   - `DIM_Game` nối tới `DIM_Competition` và `DIM_Club` (`Home_Club_ID`, `Away_Club_ID`).

---

### Bước 2: Bổ sung Named Calculations trên các bảng chiều
Bấm chuột phải vào bảng tương ứng trên sơ đồ DSV $\rightarrow$ **New Named Calculation...** để thêm các cột dẫn xuất sau:

```sql
-- 1) Trên bảng DIM_Game:
-- Time_ID (INT) - dùng để nối DIM_Game sang DIM_Time:
YEAR([Date]) * 10000 + MONTH([Date]) * 100 + DAY([Date])

-- Total_Match_Goals (INT) - tổng bàn thắng chính thức của trận (Câu 14):
ISNULL([Home_Club_Goals], 0) + ISNULL([Away_Club_Goals], 0)

-- Season_Label (VARCHAR(9)) - nhãn hiển thị mùa giải (2022/2023, 2023/2024):
CAST([Season] AS VARCHAR(4)) + '/' + CAST([Season] + 1 AS VARCHAR(4))

-- 2) Trên bảng DIM_Player:
-- Is_Youth_2004 (INT) - đánh dấu cầu thủ sinh từ 01/01/2004 (Câu 15):
CASE WHEN [Date_Of_Birth] >= '2004-01-01' THEN 1 ELSE 0 END

-- 3) Trên bảng DIM_Time:
-- Year_Quarter_Key (INT) - khóa phân biệt quý theo từng năm (Câu 10):
[Year] * 10 + [Quarter]

-- Year_Month_Key (INT) - khóa phân biệt tháng theo từng năm (Câu 12):
[Year] * 100 + [Month]
```

Hai thuộc tính `Year_Quarter_Key` và `Year_Month_Key` được tính trong DSV để phục vụ phân cấp lịch (`Calendar Hierarchy`) và các câu truy vấn 10, 12.

Sau khi tạo `DIM_Game.Time_ID`, kéo thả cột `DIM_Game.Time_ID` sang `DIM_Time.Time_ID` để thiết lập **Logical Relationship** giữa cấp trận đấu và chiều thời gian.

---

### Bước 3: Chuyển `FACT_Player_Match_Perf` sang Named Query mở rộng
Do lược đồ mới đã bỏ cột tĩnh `DIM_Player.Age` và `DIM_Club.Coach_Name`, ta bấm chuột phải vào `FACT_Player_Match_Perf` trong DSV $\rightarrow$ **Replace Table** $\rightarrow$ **With New Named Query...** để tính động tuổi cầu thủ tại ngày thi đấu (`Player_Age_At_Match`) và tên HLV của CLB tại trận (`Club_Manager_Name`) mà vẫn giữ nguyên grain **210.747 lượt ra sân** (đặt Logical Primary Key là `Appearance_ID`):

```sql
SELECT
    f.Appearance_ID,
    f.Player_ID,
    f.Club_ID,
    f.Opponent_Club_ID,
    f.Competition_ID,
    f.Game_ID,
    f.Time_ID,
    f.Minutes_Played,
    f.Goals,
    f.Assists,
    f.Yellow_Cards,
    f.Red_Cards,
    f.Is_Home_Game,
    CASE
        WHEN p.Date_Of_Birth IS NULL THEN NULL
        ELSE DATEDIFF(YEAR, p.Date_Of_Birth, g.[Date])
             - CASE
                   WHEN MONTH(p.Date_Of_Birth) > MONTH(g.[Date])
                     OR (MONTH(p.Date_Of_Birth) = MONTH(g.[Date])
                         AND DAY(p.Date_Of_Birth) > DAY(g.[Date]))
                   THEN 1 ELSE 0
               END
    END AS Player_Age_At_Match,
    CASE
        WHEN f.Club_ID = g.Home_Club_ID THEN g.Home_Club_Manager_Name
        WHEN f.Club_ID = g.Away_Club_ID THEN g.Away_Club_Manager_Name
        ELSE NULL
    END AS Club_Manager_Name
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player AS p ON p.Player_ID = f.Player_ID
JOIN dbo.DIM_Game   AS g ON g.Game_ID   = f.Game_ID;
```

---

### Bước 4: Tạo Named Query `FACT_Club_Match_Official` (cấp đội – trận cho Câu 10)
Bấm chuột phải vùng trống trong DSV $\rightarrow$ **New Named Query...**, đặt tên **`FACT_Club_Match_Official`** (`14.560` dòng = `7.280` trận $\times$ 2 đội), đặt Logical Primary Key là `Club_Match_Key` và nối khóa ngoại logic tới `DIM_Club` (`Club_ID`, `Opponent_Club_ID`), `DIM_Competition`, `DIM_Game`, `DIM_Time`:

```sql
SELECT
    CAST(g.Game_ID AS VARCHAR(20)) + '_H' AS Club_Match_Key,
    g.Game_ID,
    g.Competition_ID,
    YEAR(g.[Date]) * 10000 + MONTH(g.[Date]) * 100 + DAY(g.[Date]) AS Time_ID,
    g.Home_Club_ID AS Club_ID,
    g.Away_Club_ID AS Opponent_Club_ID,
    1 AS Is_Home_Game,
    g.Home_Club_Goals AS Official_Team_Goals,
    g.Away_Club_Goals AS Official_Goals_Conceded
FROM dbo.DIM_Game AS g
UNION ALL
SELECT
    CAST(g.Game_ID AS VARCHAR(20)) + '_A' AS Club_Match_Key,
    g.Game_ID,
    g.Competition_ID,
    YEAR(g.[Date]) * 10000 + MONTH(g.[Date]) * 100 + DAY(g.[Date]) AS Time_ID,
    g.Away_Club_ID AS Club_ID,
    g.Home_Club_ID AS Opponent_Club_ID,
    0 AS Is_Home_Game,
    g.Away_Club_Goals AS Official_Team_Goals,
    g.Home_Club_Goals AS Official_Goals_Conceded
FROM dbo.DIM_Game AS g;
```

---

## 3. KHỞI TẠO 6 DATABASE DIMENSIONS

Bấm phải thư mục **Dimensions** $\rightarrow$ **New Dimension...** $\rightarrow$ **Use an existing table**:

### 1. `DIM_Club` (`DIM_Club.dim`)
- **Main table**: `DIM_Club` | **Key column**: `Club_ID` | **Name column**: `Club_Name`
- **Attributes**: `Club ID` (hiển thị `Club_Name`), `Club Name`, `Stadium Name`, `Stadium Seats`, `Squad Size`.
- **Lưu ý**: Không còn `Coach_Name`. Đặt `UnknownMember = Visible` (`Unknown`) để tương thích với `Opponent_Club_ID` cho phép NULL.

### 2. `DIM_Competition` (`DIM_Competition.dim`)
- **Main table**: `DIM_Competition` | **Key column**: `Competition_ID` | **Name column**: `Competition_ID`
- **Attributes**: `Competition ID`, `Competition Name`, `Country Name`, `Competition Type`.

### 3. `DIM_Game` (`DIM_Game.dim`)
- **Main table**: `DIM_Game` | **Key column**: `Game_ID` | **Name column**: `Game_ID`
- **Attributes**: `Game ID`, `Competition ID`, `Season` (`KeyColumns = Season`, `NameColumn = Season_Label`), `Round`, `Date`, `Home Club ID`, `Away Club ID`, `Home Club Goals`, `Away Club Goals`, `Total Match Goals`, `Stadium`, `Home Club Manager Name`, `Away Club Manager Name`.

### 4. `DIM_Player` (`DIM_Player.dim`)
- **Main table**: `DIM_Player` | **Key column**: `Player_ID` | **Name column**: `Player_Name`
- **Attributes**: `Player ID` (hiển thị `Player_Name` nhưng giữ định danh duy nhất theo `Player_ID` để tránh gộp nhầm 51 tên bị trùng trên 108 hồ sơ), `Player Name`, `Date Of Birth`, `Is Youth 2004`, `Country Of Citizenship`, `Main Position`, `Sub Position`, `Foot`, `Height In Cm`.
- **Lưu ý**: Không còn cột `Age`.

### 5. `DIM_Time` (`DIM_Time.dim`)
- **Main table**: `DIM_Time` | **Key column**: `Time_ID` | **Name column**: `Full_Date`
- **Attributes**: `Time ID`, `Full Date`, `Year`, `Quarter`, `Year Quarter Key`, `Month`, `Year Month Key`, `Day`, `Day Of Week`, `Is Weekend`.
- **Lưu ý**: Không còn thuộc tính `Season` (đã chuyển sang `DIM_Game`).

### 6. `DIM_Appearance_Context` (`DIM_Appearance_Context.dim` — Fact Dimension)
- **Main table**: `FACT_Player_Match_Perf` | **Key column**: `Appearance_ID` | **Name column**: `Appearance_ID`
- **Attributes**: `Appearance ID` (đặt `AttributeHierarchyVisible = False` để tránh phình cây metadata 210.747 mã), `Is Home Game`, `Player Age At Match`, `Club Manager Name`.

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] DSV `DW_Football_Transfermarkt.dsv` chứa đủ 6 bảng gốc + 6 Named Calculations + `FACT_Club_Match_Official`.
- [x] Đã tạo đủ 6 tệp `.dim` khớp chính xác cột của `schema_warehouse.sql` và Chương 1.
- [x] Thuộc tính khóa `Player ID` của `DIM_Player` dùng `NameColumn = Player_Name` chống gộp cầu thủ trùng tên.
