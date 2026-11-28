# MDX Query 08: Top 10 cầu thủ có số bàn thắng trên 90 phút cao nhất mùa 2023/24 (tối thiểu 900 phút)
## (Calculated Measure `Goals Per 90`, kết hợp `FILTER (≥ 900)` và `TOPCOUNT`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 8. Xếp hạng 10 cầu thủ có số bàn thắng trên 90 phút cao nhất mùa 2023/24, trong số những cầu thủ thi đấu ít nhất 900 phút. Hiển thị tổng số bàn và số phút. Xếp theo tỷ lệ chưa làm tròn.
  *[Thuộc tính: Player_ID, Player_Name, Goals, Minutes_Played, Season]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Mùa giải (`DIM_Game.Season`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Player ID]`, `[DIM Game].[Season]`, `[Measures].[Goals Per 90]`, `[Measures].[Goals]`, `[Measures].[Minutes Played]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT TOP 10
    p.Player_ID,
    p.Player_Name,
    SUM(f.Goals)          AS Total_Goals,
    SUM(f.Minutes_Played) AS Total_Minutes_Played,
    CAST(90.0 * SUM(f.Goals) / SUM(f.Minutes_Played) AS DECIMAL(6,2)) AS Goals_Per_90
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
JOIN dbo.DIM_Game   AS g ON f.Game_ID   = g.Game_ID
WHERE g.Season = 2023
GROUP BY p.Player_ID, p.Player_Name
HAVING SUM(f.Minutes_Played) >= 900
ORDER BY (90.0 * SUM(f.Goals) / SUM(f.Minutes_Played)) DESC, Total_Goals DESC, p.Player_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Dòng 1 Filter Pane: `DIM Game → Season`, Operator = `Equal`, chọn `2023/2024`.
- Dòng 2 Filter Pane: `DIM Player → Player ID`, Operator = `Custom`, dán biểu thức `TOPCOUNT(FILTER(...))` bên dưới.
- Kéo `DIM Player → Player ID` vào **Rows**; kéo `Goals Per 90`, `Goals`, `Minutes Played` vào **Values** → bấm **Click to execute the query**.

```mdx
TOPCOUNT(
    FILTER(
        NONEMPTY(
            [DIM Player].[Player ID].[Player ID].MEMBERS,
            ( [Measures].[Minutes Played], [DIM Game].[Season].&[2023] )
        ),
        ( [Measures].[Minutes Played], [DIM Game].[Season].&[2023] ) >= 900
    ),
    10,
    ( [Measures].[Goals Per 90], [DIM Game].[Season].&[2023] )
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$AM$3`.
- Vào **PivotTable Analyze → Fields, Items, & Sets → Create Set Using MDX…**, đặt tên `Top 10 Goals Per 90 Min900` và dán biểu thức `TOPCOUNT(FILTER(...))` ở trên (vì UI Excel chỉ giữ được 1 Value Filter mỗi trường hàng).
- Kéo `DIM Game → Season` vào **Filters** (`2023/2024`); kéo Set vừa tạo vào **Rows**; kéo `Goals Per 90`, `Goals`, `Minutes Played` vào **Values**.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_08.mdx`)
- Hàm `FILTER` loại bỏ các cầu thủ có tổng phút thi đấu `< 900` ở mùa 2023/2024.
- Hàm `TOPCOUNT(..., 10, [Measures].[Goals Per 90])` xếp hạng theo tỷ lệ đầy đủ chưa làm tròn trên Calculated Measure `Goals Per 90`.

```mdx
SELECT
    {
        [Measures].[Goals Per 90],
        [Measures].[Goals],
        [Measures].[Minutes Played]
    } ON COLUMNS,
    TOPCOUNT(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player ID].[Player ID].MEMBERS,
                (
                    [Measures].[Minutes Played],
                    [DIM Game].[Season].&[2023]
                )
            ),
            [Measures].[Minutes Played] >= 900
        ),
        10,
        [Measures].[Goals Per 90]
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Game].[Season].&[2023] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Hạng | Player_ID | Player_Name | Goals | Minutes_Played | Bàn/90 |
| :---: | ---: | :--- | ---: | ---: | ---: |
| 1 | 270541 | Serhou Guirassy | 28 | 2.214 | 1,14 |
| 2 | 197642 | Chuba Akpom | 14 | 1.228 | 1,03 |
| 3 | 132098 | Harry Kane | 44 | 3.908 | 1,01 |
| 4 | 342229 | Kylian Mbappé | 35 | 3.239 | 0,97 |
| 5 | 746910 | Mohamed Amoura | 19 | 1.880 | 0,91 |
| 6 | 272855 | Paul Onuachu | 15 | 1.514 | 0,89 |
| 7 | 418560 | Erling Haaland | 33 | 3.337 | 0,89 |
| 8 | 656681 | Victor Boniface | 19 | 1.934 | 0,88 |
| 9 | 324503 | Vangelis Pavlidis | 29 | 3.000 | 0,87 |
| 10 | 325443 | Viktor Gyökeres | 34 | 3.537 | 0,87 |

> **Nhận xét đối chiếu:** Có **2.960 cầu thủ** đạt ngưỡng 900 phút ở mùa 2023/2024. **Serhou Guirassy** dẫn đầu với **1,14 bàn/90 phút** (28 bàn trong 2.214 phút), tiếp theo là **Chuba Akpom** (1,03) và **Harry Kane** (1,01). Xếp hạng dùng tỷ lệ đầy đủ chưa làm tròn, còn cột hiển thị làm tròn đến hai chữ số.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian sau lọc:** Từ 4.832 cầu thủ mùa 2023/2024 lọc xuống $M = 2.960$ cầu thủ đạt $\ge 900$ phút; kết quả $O(10)$.
* **Độ phức tạp thời gian:** $O(N_{2023} + M \log 10)$ trên Formula Engine sau bước gom phút ở Storage Engine.
