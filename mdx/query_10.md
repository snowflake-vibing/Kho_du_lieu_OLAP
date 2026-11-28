# MDX Query 10: Bàn thắng chính thức của Real Madrid (Club_ID = 418) trước từng đối thủ theo quý
## (Truy vấn cấp đội – trận trên Measure Group `FACT Club Match Official` và `DIM Opponent Club`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 10. Thống kê tổng số bàn thắng của Real Madrid (Club_ID = 418) trước từng đối thủ theo quý của từng năm. Dùng tỷ số sau thời gian thi đấu, kể cả hiệp phụ, và loại bàn luân lưu. Tính mỗi trận một lần theo vai trò sân nhà hoặc sân khách của Real Madrid.
  *[Thuộc tính: Game_ID, Club_ID, Club_Name, Home_Club_ID, Away_Club_ID, Home_Club_Goals, Away_Club_Goals, Date, Full_Date, Year_Quarter_Key]*
* **Cấp độ dữ liệu (Grain):** `FACT Club Match Official` (Đội – Trận: 14.560 dòng)
* **Đối tượng phân tích:** Named Query `FACT_Club_Match_Official` (từ `DIM_Game`), CLB chính (`DIM_Club`), CLB đối thủ (`DIM_Opponent_Club`), Thời gian (`DIM_Time.Year_Quarter_Key` tính trong DSV).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Club].[Club ID]`, `[DIM Opponent Club].[Club ID]`, `[DIM Time].[Year Quarter Key]`, `[Measures].[Official Team Match Count]`, `[Measures].[Official Team Goals]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

WITH Official_Team_Games AS (
    SELECT
        g.Game_ID,
        YEAR(g.[Date]) * 10000 + MONTH(g.[Date]) * 100 + DAY(g.[Date]) AS Time_ID,
        g.Home_Club_ID AS Club_ID,
        g.Away_Club_ID AS Opponent_Club_ID,
        g.Home_Club_Goals AS Official_Team_Goals
    FROM dbo.DIM_Game AS g
    WHERE g.Home_Club_ID = 418
    UNION ALL
    SELECT
        g.Game_ID,
        YEAR(g.[Date]) * 10000 + MONTH(g.[Date]) * 100 + DAY(g.[Date]) AS Time_ID,
        g.Away_Club_ID AS Club_ID,
        g.Home_Club_ID AS Opponent_Club_ID,
        g.Away_Club_Goals AS Official_Team_Goals
    FROM dbo.DIM_Game AS g
    WHERE g.Away_Club_ID = 418
)
SELECT
    t.[Year] * 10 + t.[Quarter] AS Year_Quarter_Key,
    opp.Club_ID                  AS Opponent_Club_ID,
    opp.Club_Name                AS Opponent_Name,
    COUNT(o.Game_ID)             AS Matches,
    SUM(o.Official_Team_Goals)   AS Official_Team_Goals
FROM Official_Team_Games AS o
JOIN dbo.DIM_Club AS opp ON o.Opponent_Club_ID = opp.Club_ID
JOIN dbo.DIM_Time AS t   ON o.Time_ID          = t.Time_ID
GROUP BY t.[Year] * 10 + t.[Quarter], opp.Club_ID, opp.Club_Name
ORDER BY Official_Team_Goals DESC, Year_Quarter_Key ASC, opp.Club_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Club → Club ID`, Operator = `Equal`, tìm chọn `Real Madrid` (`418`).
- Kéo `DIM Time → Year Quarter Key` và `DIM Opponent Club → Club ID` vào **Rows**; kéo `Official Team Match Count` và `Official Team Goals` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$AW$3`.
- Kéo `DIM Club → Club ID` vào **Filters** (`Real Madrid`); kéo `Year Quarter Key` và `DIM Opponent Club → Club ID` vào **Rows**; kéo `Official Team Match Count` và `Official Team Goals` vào **Values**.
- Chỉnh **Report Layout → Show in Tabular Form** và sắp xếp giảm dần theo `Official Team Goals`.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_10.mdx`)
- Truy vấn trực tiếp trên Measure Group `FACT Club Match Official` để không bị trùng theo lượt ra sân và dùng đúng tỷ số sau thời gian thi đấu (kể cả hiệp phụ, loại bàn luân lưu).
- Dùng `NONEMPTY(CrossJoin([Year Quarter Key], [DIM Opponent Club]), ...)` kết hợp `WHERE ([DIM Club].[Club ID].&[418])`.

```mdx
SELECT
    {
        [Measures].[Official Team Match Count],
        [Measures].[Official Team Goals]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            CrossJoin(
                [DIM Time].[Year Quarter Key].[Year Quarter Key].MEMBERS,
                EXCEPT(
                    [DIM Opponent Club].[Club ID].[Club ID].MEMBERS,
                    { [DIM Opponent Club].[Club ID].[Unknown] }
                )
            ),
            (
                [Measures].[Official Team Match Count],
                [DIM Club].[Club ID].&[418]
            )
        ),
        [Measures].[Official Team Goals],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Club].[Club ID].&[418] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Year_Quarter_Key | Opponent_Club_ID | Opponent_Name | Số trận | Official_Team_Goals |
| ---: | ---: | :--- | ---: | ---: |
| 20234 | 6195 | SSC Napoli | 2 | 7 |
| 20231 | 31 | Liverpool FC | 2 | 6 |
| 20232 | 366 | Real Valladolid CF | 1 | 6 |
| 20224 | 371 | Celtic FC | 1 | 5 |
| 20234 | 1049 | Valencia CF | 1 | 5 |
| 20234 | 1075 | SC Braga | 2 | 5 |
| 20242 | 1108 | Deportivo Alavés | 1 | 5 |
| 20223 | 237 | RCD Mallorca | 1 | 4 |
| 20223 | 940 | Celta de Vigo | 1 | 4 |
| 20231 | 1531 | Elche CF | 1 | 4 |

> **Nhận xét đối chiếu:** Real Madrid ghi **216 bàn** trong **101 trận**, phân bổ trên 92 cặp quý và đối thủ (sau khi loại bàn luân lưu và dùng tỷ số sau thời gian thi đấu, kể cả hiệp phụ). Trong quý II/2024 (`20242`), Real ghi 4 bàn qua hai trận gặp Manchester City (tỷ số trận lượt về là 1–1 sau hiệp phụ).

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian Descartes:** $8 \text{ quý} \times 272 \text{ đối thủ} = 2.176 \text{ tuples}$, co hẹp xuống $M = 92$ cặp thực tế nhờ `NONEMPTY`.
* **Độ phức tạp thời gian:** $O(M \log M)$ trên 101 bản ghi cấp đội – trận của Real Madrid.
