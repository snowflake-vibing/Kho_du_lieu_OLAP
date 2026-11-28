# MDX Query 07: Bàn thắng theo quốc tịch cầu thủ tại các giải đấu nước Anh (và phân tích Pareto 80/20)
## (Cắt lát quốc gia giải đấu `England`, hàm `ORDER`, `TOPPERCENT`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 7. Thống kê tổng số bàn thắng (Goals) của các cầu thủ theo từng quốc tịch (Country_Of_Citizenship) khi thi đấu tại các giải đấu có quốc gia đăng cai là nước Anh (Country_Name = 'England').
  *[Thuộc tính: Country_Of_Citizenship, Country_Name, Goals]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player.Country_Of_Citizenship`), Giải đấu (`DIM_Competition.Country_Name`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Country Of Citizenship]`, `[DIM Competition].[Country Name]`, `[Measures].[Goals]`, `[Measures].[Pct Of Country Goals]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

WITH Eng_Goals AS (
    SELECT
        p.Country_Of_Citizenship,
        SUM(f.Goals) AS Total_Goals
    FROM dbo.FACT_Player_Match_Perf AS f
    JOIN dbo.DIM_Player      AS p ON f.Player_ID      = p.Player_ID
    JOIN dbo.DIM_Competition AS c ON f.Competition_ID = c.Competition_ID
    WHERE c.Country_Name = N'England'
      AND p.Country_Of_Citizenship IS NOT NULL
    GROUP BY p.Country_Of_Citizenship
)
SELECT
    Country_Of_Citizenship,
    Total_Goals,
    CAST(Total_Goals * 100.0 / SUM(Total_Goals) OVER () AS DECIMAL(5,2)) AS Pct_Share,
    CAST(SUM(Total_Goals) OVER (ORDER BY Total_Goals DESC, Country_Of_Citizenship ASC)
         * 100.0 / SUM(Total_Goals) OVER () AS DECIMAL(5,2)) AS Cum_Pct
FROM Eng_Goals
ORDER BY Total_Goals DESC, Country_Of_Citizenship ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Dòng 1 Filter Pane: `DIM Competition → Country Name`, Operator = `Equal`, chọn `England`.
- Dòng 2 Filter Pane: `DIM Player → Country Of Citizenship`, Operator = `Not Equal`, chọn `Unknown` (hoặc chọn `Custom` dùng `TOPPERCENT(..., 80, ...)` nếu muốn xem riêng nhóm Pareto 80%).
- Kéo `Country Of Citizenship` vào **Rows**; kéo `Goals` và `Pct Of Country Goals` vào **Values** → bấm **Click to execute the query**.

```mdx
-- Tùy chọn Custom Filter lọc nhóm Pareto 80%:
TOPPERCENT(
    NONEMPTY(
        EXCEPT(
            [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
            { [DIM Player].[Country Of Citizenship].[Unknown] }
        ),
        ( [Measures].[Goals], [DIM Competition].[Country Name].&[England] )
    ),
    80,
    [Measures].[Goals]
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$AH$3`.
- Kéo `DIM Competition → Country Name` vào **Filters** (`England`); `Country Of Citizenship` vào **Rows** (bỏ `Unknown`); kéo `Goals` và `Pct Of Country Goals` vào **Values**.
- Sắp xếp giảm dần theo `Goals` (hoặc dùng **Value Filters → Top 10… → Top 80 Percent** để lọc nhóm Pareto 80%).

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_07.mdx`)
- Trục `COLUMNS`: hiển thị `[Measures].[Goals]` và tỷ trọng `[Measures].[Pct Of Country Goals]`.
- Trục `ROWS`: thống kê toàn bộ quốc tịch hợp lệ ghi bàn tại Anh theo thứ tự giảm dần (khi áp dụng `TOPPERCENT(..., 80, ...)` sẽ thu được đúng 18 quốc tịch Pareto 80%).

```mdx
SELECT
    {
        [Measures].[Goals],
        [Measures].[Pct Of Country Goals]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            EXCEPT(
                [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                { [DIM Player].[Country Of Citizenship].[Unknown] }
            ),
            (
                [Measures].[Goals],
                [DIM Competition].[Country Name].&[England]
            )
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Competition].[Country Name].&[England] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| STT | Country_Of_Citizenship | Goals | Tỷ trọng (%) | Tích lũy (%) |
| :---: | :--- | ---: | ---: | ---: |
| 1 | England | 714 | 31,97% | 31,97% |
| 2 | Brazil | 194 | 8,69% | 40,66% |
| 3 | Norway | 91 | 4,08% | 44,74% |
| 4 | France | 89 | 3,99% | 48,72% |
| 5 | Portugal | 86 | 3,85% | 52,58% |
| 6 | Argentina | 79 | 3,54% | 56,11% |
| 7 | Germany | 54 | 2,42% | 58,53% |
| 8 | Belgium | 53 | 2,37% | 60,90% |
| 9 | Netherlands | 52 | 2,33% | 63,23% |
| 10 | Denmark | 51 | 2,28% | 65,52% |

> **Nhận xét đối chiếu:** Các giải ở Anh ghi nhận tổng 2.236 bàn, gồm 2.233 bàn trên 75 quốc tịch hợp lệ (và 3 bàn thiếu quốc tịch). Anh dẫn đầu (714 bàn; 31,97%), Brazil thứ hai (194 bàn). Theo Pareto 80/20, chỉ 18 quốc tịch đầu đã chiếm 80,43% tổng bàn thắng.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian sau lọc:** $M = 75$ quốc tịch ghi bàn tại Anh (trên tổng ~140 quốc tịch của `DIM_Player`).
* **Độ phức tạp thời gian:** $O(M \log M)$ để sắp xếp toàn bộ 75 quốc tịch; bộ nhớ kết quả $O(M)$.
