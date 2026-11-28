# MDX Query 12: Thống kê thẻ vàng, thẻ đỏ, số trận và trung bình mỗi trận của từng CLB theo HLV tại trận và tháng
## (Kết hợp `DIM Club`, `Club Manager Name`, `Year Month Key` (DSV) và `Covered Match Count`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 12. Thống kê tổng số thẻ vàng và thẻ đỏ của từng CLB theo HLV phụ trách tại trận và theo tháng của từng năm. Hiển thị số trận có dữ liệu lượt ra sân và tên HLV, cùng số thẻ vàng và thẻ đỏ trung bình mỗi trận.
  *[Thuộc tính: Game_ID, Club_ID, Club_Name, Home_Club_ID, Away_Club_ID, Home_Club_Manager_Name, Away_Club_Manager_Name, Time_ID, Year_Month_Key, Yellow_Cards, Red_Cards]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` + `DIM Appearance Context`
* **Đối tượng phân tích:** CLB (`DIM_Club`), Ngữ cảnh HLV tại trận (`DIM_Appearance_Context.Club_Manager_Name`), Thời gian (`DIM_Time.Year_Month_Key` tính trong DSV), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Club].[Club ID]`, `[DIM Appearance Context].[Club Manager Name]`, `[DIM Time].[Year Month Key]`, `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`, `[Measures].[Covered Match Count]`, `[Measures].[Yellow Cards Per Match]`, `[Measures].[Red Cards Per Match]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    c.Club_ID,
    c.Club_Name,
    CASE
        WHEN f.Club_ID = g.Home_Club_ID THEN g.Home_Club_Manager_Name
        WHEN f.Club_ID = g.Away_Club_ID THEN g.Away_Club_Manager_Name
    END AS Club_Manager_Name,
    t.[Year] * 100 + t.[Month] AS Year_Month_Key,
    COUNT(DISTINCT f.Game_ID)  AS Covered_Match_Count,
    SUM(f.Yellow_Cards)        AS Total_Yellow_Cards,
    SUM(f.Red_Cards)           AS Total_Red_Cards,
    CAST(1.0 * SUM(f.Yellow_Cards) / NULLIF(COUNT(DISTINCT f.Game_ID), 0) AS DECIMAL(6,2)) AS Yellow_Cards_Per_Match,
    CAST(1.0 * SUM(f.Red_Cards) / NULLIF(COUNT(DISTINCT f.Game_ID), 0) AS DECIMAL(6,2))    AS Red_Cards_Per_Match
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Club AS c ON f.Club_ID = c.Club_ID
JOIN dbo.DIM_Game AS g ON f.Game_ID = g.Game_ID
JOIN dbo.DIM_Time AS t ON f.Time_ID = t.Time_ID
WHERE (CASE
           WHEN f.Club_ID = g.Home_Club_ID THEN g.Home_Club_Manager_Name
           WHEN f.Club_ID = g.Away_Club_ID THEN g.Away_Club_Manager_Name
       END) IS NOT NULL
GROUP BY
    c.Club_ID,
    c.Club_Name,
    CASE
        WHEN f.Club_ID = g.Home_Club_ID THEN g.Home_Club_Manager_Name
        WHEN f.Club_ID = g.Away_Club_ID THEN g.Away_Club_Manager_Name
    END,
    t.[Year] * 100 + t.[Month]
ORDER BY Total_Yellow_Cards DESC, Total_Red_Cards DESC, Year_Month_Key ASC, c.Club_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Appearance Context → Club Manager Name`, Operator = `Not Equal`, chọn `Unknown` (loại 58 lượt ra sân của 2 trận thiếu tên HLV).
- Kéo `DIM Club → Club ID`, `DIM Appearance Context → Club Manager Name` và `DIM Time → Year Month Key` vào **Rows**; kéo `Yellow Cards`, `Red Cards`, `Covered Match Count`, `Yellow Cards Per Match` và `Red Cards Per Match` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$BG$3`.
- Kéo `DIM Club → Club ID`, `Club Manager Name` và `Year Month Key` vào **Rows**; kéo `Yellow Cards`, `Red Cards`, `Covered Match Count`, `Yellow Cards Per Match` và `Red Cards Per Match` vào **Values**.
- Bỏ tích `Unknown` ở `Club Manager Name`, bật Tabular Form và sắp xếp giảm dần theo `Yellow Cards`.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_12.mdx`)
- `WITH SET [ValidManagers]` loại bỏ thành viên `[Unknown]` do 2 trận thiếu tên HLV.
- Trục `COLUMNS` xuất tổng thẻ vàng/đỏ, số trận có lượt ra sân (`Covered Match Count`) và tỷ lệ thẻ vàng/đỏ mỗi trận.
- `NONEMPTY(CrossJoin(...), [Measures].[Appearance Count])` giữ chính xác các tổ hợp `(CLB × HLV × Year_Month_Key)` có thi đấu thực tế.

```mdx
WITH SET [ValidManagers] AS
    EXCEPT(
        [DIM Appearance Context].[Club Manager Name]
            .[Club Manager Name].MEMBERS,
        { [DIM Appearance Context].[Club Manager Name].[Unknown] }
    )
SELECT
    {
        [Measures].[Yellow Cards],
        [Measures].[Red Cards],
        [Measures].[Covered Match Count],
        [Measures].[Yellow Cards Per Match],
        [Measures].[Red Cards Per Match]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            CrossJoin(
                EXCEPT(
                    [DIM Club].[Club ID].[Club ID].MEMBERS,
                    { [DIM Club].[Club ID].[Unknown] }
                ),
                CrossJoin(
                    [ValidManagers],
                    [DIM Time].[Year Month Key].[Year Month Key].MEMBERS
                )
            ),
            [Measures].[Appearance Count]
        ),
        [Measures].[Yellow Cards],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| CLB | HLV | Tháng | Trận | Vàng | Đỏ | Vàng/trận | Đỏ/trận |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Atlético de Madrid | Diego Simeone | 202210 | 9 | 27 | 0 | 3,00 | 0,00 |
| Sevilla FC | Jorge Sampaoli | 202210 | 7 | 25 | 1 | 3,57 | 0,14 |
| Zulte Waregem | Mbaye Leye | 202210 | 6 | 25 | 1 | 4,17 | 0,17 |
| Real Sociedad | Imanol Alguacil | 202210 | 9 | 25 | 0 | 2,78 | 0,00 |
| Associazione Sportiva Roma | José Mourinho | 202305 | 8 | 25 | 0 | 3,13 | 0,00 |
| Manchester United | Erik ten Hag | 202312 | 8 | 25 | 0 | 3,13 | 0,00 |
| Sevilla FC | José Luis Mendilibar | 202305 | 9 | 24 | 2 | 2,67 | 0,22 |
| Sevilla FC | José Luis Mendilibar | 202304 | 7 | 24 | 1 | 3,43 | 0,14 |
| FC Augsburg | Enrico Maaßen | 202210 | 5 | 24 | 0 | 4,80 | 0,00 |
| 1.FC Union Berlin | Urs Fischer | 202210 | 8 | 23 | 1 | 2,88 | 0,13 |

> **Nhận xét đối chiếu:** Có **3.967 tổ hợp** CLB, HLV và tháng. Loại 58 lượt ra sân thuộc 2 trận thiếu tên HLV. **Atlético de Madrid** dưới thời **Diego Simeone** có 27 thẻ vàng trong 9 trận tháng 10/2022 (`202210`), tương đương 3,00 thẻ vàng mỗi trận.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian lý thuyết:** $272 \text{ CLB} \times 490 \text{ HLV} \times 23 \text{ tháng} \approx 3,07 \times 10^6 \text{ tuples}$.
* **Sau tối ưu `NONEMPTY`:** Giảm xuống đúng $M = 3.967$ tổ hợp thực tế; thời gian sắp xếp $O(M \log M)$.
