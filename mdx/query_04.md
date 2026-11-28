# MDX Query 04: Hiệu suất ghi bàn, kiến tạo và phút thi đấu trung bình theo độ tuổi năm 2023
## (Thuộc tính tuổi động `Player Age At Match` và `Avg Minutes Played`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 4. Thống kê tổng số bàn thắng (Goals), số đường kiến tạo (Assists) và tổng số phút thi đấu trung bình (Minutes_Played) của các cầu thủ phân theo từng độ tuổi (Age) trong năm 2023 (Year).
  *[Thuộc tính: Age, Goals, Assists, Minutes_Played, Year]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` + `DIM Appearance Context`
* **Đối tượng phân tích:** Ngữ cảnh ra sân (`DIM_Appearance_Context.Player_Age_At_Match`), Thời gian (`DIM_Time.Year`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Appearance Context].[Player Age At Match]`, `[DIM Time].[Year]`, `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Avg Minutes Played]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

WITH Perf_Age AS (
    SELECT
        f.Goals,
        f.Assists,
        f.Minutes_Played,
        DATEDIFF(YEAR, p.Date_Of_Birth, g.[Date])
        - CASE
              WHEN MONTH(p.Date_Of_Birth) > MONTH(g.[Date])
                OR (MONTH(p.Date_Of_Birth) = MONTH(g.[Date])
                    AND DAY(p.Date_Of_Birth) > DAY(g.[Date]))
              THEN 1 ELSE 0
          END AS Age_At_Match
    FROM dbo.FACT_Player_Match_Perf AS f
    JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
    JOIN dbo.DIM_Game   AS g ON f.Game_ID   = g.Game_ID
    JOIN dbo.DIM_Time   AS t ON f.Time_ID   = t.Time_ID
    WHERE t.[Year] = 2023
      AND p.Date_Of_Birth IS NOT NULL
)
SELECT
    Age_At_Match,
    COUNT(*)                         AS Appearances,
    SUM(Goals)                       AS Total_Goals,
    SUM(Assists)                     AS Total_Assists,
    AVG(CAST(Minutes_Played AS FLOAT)) AS Avg_Minutes_Played
FROM Perf_Age
GROUP BY Age_At_Match
ORDER BY Age_At_Match ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Dòng 1 Filter Pane: `DIM Time → Year`, Operator = `Equal`, chọn `2023`.
- Dòng 2 Filter Pane: `DIM Appearance Context → Player Age At Match`, Operator = `Not Equal`, chọn `Unknown` (loại 33 lượt ra sân thiếu `Date_Of_Birth`).
- Kéo `DIM Appearance Context → Player Age At Match` vào **Rows**; kéo `Goals`, `Assists`, `Avg Minutes Played` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$S$3`.
- Kéo `DIM Time → Year` vào **Filters** (`2023`); kéo `DIM Appearance Context → Player Age At Match` vào **Rows**; kéo `Goals`, `Assists`, `Avg Minutes Played` vào **Values**.
- Tại `Row Labels`, bỏ tích `Unknown` và sắp xếp **Sort Smallest to Largest** theo độ tuổi.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_04.mdx`)
- Dùng `WITH SET [ValidAgeMembers]` loại trừ `[Unknown]` trên `Player Age At Match`.
- Lọc `NOT ISEMPTY(...MEMBER_VALUE)` và `MEMBER_VALUE > 0`, sắp xếp tăng dần bằng `ORDER(..., BASC)` trong lát cắt năm `2023`.

```mdx
WITH SET [ValidAgeMembers] AS
    EXCEPT(
        [DIM Appearance Context].[Player Age At Match]
            .[Player Age At Match].MEMBERS,
        { [DIM Appearance Context].[Player Age At Match].[Unknown] }
    )
SELECT
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,
    ORDER(
        FILTER(
            NONEMPTY(
                [ValidAgeMembers],
                ( [Measures].[Appearance Count], [DIM Time].[Year].&[2023] )
            ),
            NOT ISEMPTY(
                [DIM Appearance Context].[Player Age At Match]
                    .CURRENTMEMBER.MEMBER_VALUE
            )
            AND [DIM Appearance Context].[Player Age At Match]
                    .CURRENTMEMBER.MEMBER_VALUE > 0
        ),
        [DIM Appearance Context].[Player Age At Match]
            .CURRENTMEMBER.MEMBER_VALUE,
        BASC
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Time].[Year].&[2023] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Độ tuổi | Lượt ra sân | Goals | Assists | Avg Minutes Played |
| ---: | ---: | ---: | ---: | ---: |
| 21 | 6.569 | 560 | 465 | 59,34 |
| 22 | 8.272 | 740 | 637 | 60,95 |
| 23 | 9.405 | 872 | 679 | 62,68 |
| 24 | 9.699 | 992 | 713 | 64,98 |
| 25 | 10.222 | 961 | 715 | 66,58 |
| 26 | 9.581 | 857 | 676 | 66,10 |
| 27 | 7.813 | 754 | 530 | 66,24 |
| 28 | 7.914 | 693 | 548 | 67,08 |
| 29 | 6.997 | 656 | 484 | 69,58 |
| 30 | 6.783 | 632 | 480 | 69,21 |

> **Nhận xét đối chiếu:** Năm 2023 ghi nhận đúng **28 độ tuổi hợp lệ** từ 15 đến 42 tuổi (loại 33 lượt ra sân của 2 cầu thủ thiếu ngày sinh). Nhóm tuổi 24–25 ghi nhiều bàn thắng và kiến tạo nhất, trong khi số phút trung bình mỗi trận tăng ổn định ở nhóm cầu thủ chín muồi 25–35 tuổi.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian lý thuyết:** ~30 mức tuổi $\times$ 3 năm = 90 cells.
* **Sau lọc:** $M = 28$ độ tuổi hợp lệ; bộ nhớ kết quả $O(28)$.
* **Độ phức tạp thời gian:** $O(M \log M)$ sau khi Storage Engine gom nhóm theo tuổi tại trận ở năm 2023.
