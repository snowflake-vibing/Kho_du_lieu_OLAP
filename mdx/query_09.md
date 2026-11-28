# MDX Query 09: So sánh bàn thắng, thẻ vàng, số trận và trung bình mỗi trận Sân nhà vs Sân khách cuối tuần
## (Cắt lát `Is_Weekend = 1` với `Covered Match Count`, `Goals Per Match` và `Yellow Cards Per Match`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 9. So sánh bàn thắng và thẻ vàng của từng CLB giữa sân nhà và sân khách vào cuối tuần. Hiển thị tổng số, số trận có dữ liệu lượt ra sân và số bàn, số thẻ vàng trung bình mỗi trận theo từng vai trò.
  *[Thuộc tính: Game_ID, Club_ID, Club_Name, Is_Home_Game, Goals, Yellow_Cards, Is_Weekend]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` + `DIM Appearance Context`
* **Đối tượng phân tích:** CLB (`DIM_Club`), Trận đấu (`DIM_Game`), Ngữ cảnh sân nhà/khách (`DIM_Appearance_Context.Is_Home_Game`), Thời gian (`DIM_Time.Is_Weekend`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Club].[Club ID]`, `[DIM Appearance Context].[Is Home Game]`, `[DIM Time].[Is Weekend]`, `[Measures].[Goals]`, `[Measures].[Yellow Cards]`, `[Measures].[Covered Match Count]`, `[Measures].[Goals Per Match]`, `[Measures].[Yellow Cards Per Match]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    c.Club_ID,
    c.Club_Name,
    f.Is_Home_Game,
    COUNT(DISTINCT f.Game_ID) AS Covered_Match_Count,
    SUM(f.Goals)              AS Total_Goals,
    SUM(f.Yellow_Cards)       AS Total_Yellow_Cards,
    CAST(1.0 * SUM(f.Goals) / NULLIF(COUNT(DISTINCT f.Game_ID), 0) AS DECIMAL(6,2))        AS Goals_Per_Match,
    CAST(1.0 * SUM(f.Yellow_Cards) / NULLIF(COUNT(DISTINCT f.Game_ID), 0) AS DECIMAL(6,2)) AS Yellow_Cards_Per_Match
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Club AS c ON f.Club_ID = c.Club_ID
JOIN dbo.DIM_Time AS t ON f.Time_ID = t.Time_ID
WHERE t.Is_Weekend = 1
GROUP BY c.Club_ID, c.Club_Name, f.Is_Home_Game
ORDER BY Total_Goals DESC, c.Club_ID ASC, f.Is_Home_Game DESC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Time → Is Weekend`, Operator = `Equal`, tích chọn `1`.
- Kéo `DIM Club → Club ID` vào **Rows**, `DIM Appearance Context → Is Home Game` vào **Columns**; kéo `Goals`, `Yellow Cards`, `Covered Match Count`, `Goals Per Match` và `Yellow Cards Per Match` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$AR$3`.
- Kéo `DIM Time → Is Weekend` vào **Filters** (`1`); `DIM Club → Club ID` vào **Rows**; `Is Home Game` vào **Columns**; kéo 5 độ đo `Goals`, `Yellow Cards`, `Covered Match Count`, `Goals Per Match` và `Yellow Cards Per Match` vào **Values**.
- Sắp xếp CLB giảm dần theo tổng bàn thắng cuối tuần.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_09.mdx`)
- Trục `COLUMNS`: tích `CrossJoin` giữa 5 thước đo (`Goals`, `Yellow Cards`, `Covered Match Count`, `Goals Per Match`, `Yellow Cards Per Match`) và `{Is Home Game = 1, Is Home Game = 0}`.
- Trục `ROWS`: lọc các CLB có lượt ra sân cuối tuần qua `NONEMPTY`, sắp xếp giảm dần bằng `ORDER(..., BDESC)`.

```mdx
SELECT
    CrossJoin(
        {
            [Measures].[Goals],
            [Measures].[Yellow Cards],
            [Measures].[Covered Match Count],
            [Measures].[Goals Per Match],
            [Measures].[Yellow Cards Per Match]
        },
        {
            [DIM Appearance Context].[Is Home Game].&[1],
            [DIM Appearance Context].[Is Home Game].&[0]
        }
    ) ON COLUMNS,
    ORDER(
        NONEMPTY(
            EXCEPT(
                [DIM Club].[Club ID].[Club ID].MEMBERS,
                { [DIM Club].[Club ID].[Unknown] }
            ),
            ( [Measures].[Appearance Count], [DIM Time].[Is Weekend].&[1] )
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Time].[Is Weekend].&[1] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| CLB | Sân | Số trận | Bàn | Thẻ vàng | Bàn/trận | Thẻ vàng/trận |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: |
| PSV Eindhoven | Nhà | 30 | 92 | 26 | 3,07 | 0,87 |
| PSV Eindhoven | Khách | 30 | 79 | 44 | 2,63 | 1,47 |
| Manchester City | Nhà | 32 | 84 | 36 | 2,63 | 1,13 |
| Manchester City | Khách | 28 | 55 | 40 | 1,96 | 1,43 |
| Real Madrid | Nhà | 31 | 71 | 52 | 2,29 | 1,68 |
| Real Madrid | Khách | 30 | 57 | 56 | 1,90 | 1,87 |

> **Nhận xét đối chiếu:** Có **207 CLB** với dữ liệu lượt ra sân cuối tuần (`Is_Weekend = 1`). Số trận (`Covered Match Count`) đếm theo mã trận duy nhất của từng CLB và vai trò; tổng bàn thắng sân nhà đạt 7.592 bàn so với 6.048 bàn sân khách (thẻ vàng sân nhà: 9.523 vs sân khách: 10.791). **PSV Eindhoven** dẫn đầu về tổng bàn cuối tuần với 171 bàn (3,07 bàn/trận sân nhà và 2,63 bàn/trận sân khách).

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian ma trận:** $272 \text{ CLB} \times 2 \text{ trạng thái} \times 5 \text{ độ đo} = 2.720 \text{ cells}$, co hẹp xuống $M = 207$ CLB thực tế.
* **Độ phức tạp thời gian:** $O(M \log M)$ với $M = 207$; `Covered Match Count` dùng `EXISTING` trên `DIM Game.Game ID` nên đếm nhanh theo từng CLB và vai trò.
