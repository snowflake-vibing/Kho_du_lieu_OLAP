# MDX Query 14: Thống kê các trận đấu kịch tính có tổng bàn thắng từ 5 bàn trở lên
## (Truy vấn cấp trận đấu trên `DIM Game` với `DIM Home Club` và `DIM Away Club`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 14. Liệt kê các trận có tổng số bàn thắng từ 5 trở lên trong thời gian thi đấu, kể cả hiệp phụ. Loại bàn luân lưu. Hiển thị đội chủ nhà, đội khách, tỷ số, sân vận động và vòng đấu.
  *[Thuộc tính: Home_Club_ID, Away_Club_ID, Home_Club_Goals, Away_Club_Goals, Stadium, Round, Game_ID]*
* **Cấp độ dữ liệu (Grain):** `DIM Game` Measure Group (Trận đấu: 7.280 dòng)
* **Đối tượng phân tích:** Trận đấu (`DIM_Game` Measure Group), Đội chủ nhà (`DIM_Home_Club`), Đội khách (`DIM_Away_Club`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Game].[Game ID]`, `[DIM Game].[Round]`, `[DIM Game].[Stadium]`, `[DIM Home Club].[Club ID]`, `[DIM Away Club].[Club ID]`, `[Measures].[Home Club Goals]`, `[Measures].[Away Club Goals]`, `[Measures].[Total Match Goals]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    g.Game_ID,
    g.Round,
    g.Stadium,
    hc.Club_ID   AS Home_Club_ID,
    hc.Club_Name AS Home_Club_Name,
    ac.Club_ID   AS Away_Club_ID,
    ac.Club_Name AS Away_Club_Name,
    g.Home_Club_Goals,
    g.Away_Club_Goals,
    (g.Home_Club_Goals + g.Away_Club_Goals) AS Total_Match_Goals
FROM dbo.DIM_Game AS g
JOIN dbo.DIM_Club AS hc ON g.Home_Club_ID = hc.Club_ID
JOIN dbo.DIM_Club AS ac ON g.Away_Club_ID = ac.Club_ID
WHERE (g.Home_Club_Goals + g.Away_Club_Goals) >= 5
ORDER BY Total_Match_Goals DESC, g.Game_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Game → Game ID`, Operator = `Custom`, dán biểu thức `FILTER(..., Total Match Goals >= 5)` bên dưới.
- Kéo `Game ID`, `Round`, `Stadium`, `DIM Home Club → Club ID` và `DIM Away Club → Club ID` vào **Rows**; kéo `Home Club Goals`, `Away Club Goals`, `Total Match Goals` vào **Values** → bấm **Click to execute the query**.

```mdx
FILTER(
    [DIM Game].[Game ID].[Game ID].MEMBERS,
    [Measures].[Total Match Goals] >= 5
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$BQ$3`.
- Kéo `Game ID`, `Round`, `Stadium`, `DIM Home Club → Club ID` và `DIM Away Club → Club ID` vào **Rows**; kéo `Home Club Goals`, `Away Club Goals`, `Total Match Goals` vào **Values**.
- Trên `Game ID`, chọn **Value Filters → Greater Than Or Equal To…** → `Total Match Goals >= 5`, sắp xếp giảm dần.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_14.mdx`)
- Lọc trước tập `Game ID` thỏa `Total Match Goals >= 5` từ Measure Group `DIM Game` (giảm từ 7.280 xuống còn 1.196 trận sau khi loại bàn luân lưu).
- Bọc `NONEMPTY(..., [Measures].[Official Match Count])` quanh phép nhân thuộc tính `*` giúp SSAS chỉ giữ duy nhất 1 tổ hợp thuộc tính thực của mỗi trận.

```mdx
SELECT
    {
        [Measures].[Home Club Goals],
        [Measures].[Away Club Goals],
        [Measures].[Total Match Goals]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            FILTER(
                [DIM Game].[Game ID].[Game ID].MEMBERS,
                [Measures].[Total Match Goals] >= 5
            )
            * [DIM Game].[Round].[Round].MEMBERS
            * [DIM Game].[Stadium].[Stadium].MEMBERS
            * EXCEPT(
                [DIM Home Club].[Club ID].[Club ID].MEMBERS,
                { [DIM Home Club].[Club ID].[Unknown] }
              )
            * EXCEPT(
                [DIM Away Club].[Club ID].[Club ID].MEMBERS,
                { [DIM Away Club].[Club ID].[Unknown] }
              ),
            [Measures].[Official Match Count]
        ),
        [Measures].[Total Match Goals],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Mã trận | Round | Stadium | Đội nhà | Đội khách | Tỷ số | Tổng bàn |
| ---: | :--- | :--- | :--- | :--- | :---: | ---: |
| 3844906 | 18. Matchday | Gewiss Stadium | Atalanta BC | US Salernitana 1919 | 8–2 | 10 |
| 3851241 | 17. Matchday | Elindus Arena | Zulte Waregem | KAS Eupen | 5–5 | 10 |
| 3852668 | 19. Matchday | AFAS Stadion | AZ Alkmaar | FC Utrecht | 5–5 | 10 |
| 3837849 | 4. Matchday | Anfield | Liverpool FC | AFC Bournemouth | 9–0 | 9 |
| 3838015 | 9. Matchday | Etihad Stadium | Manchester City | Manchester United | 6–3 | 9 |
| 3840411 | 34. Matchday | Groupama Stadium | Olympique Lyon | Montpellier HSC | 5–4 | 9 |
| 3851135 | 5. Matchday | AFAS Stadion | KV Mechelen | KVC Westerlo | 5–4 | 9 |
| 3860259 | 9. Matchday | Ülker Stadyumu FB Şükrü Saraçoğlu Spor Kompleksi | Fenerbahce | Fatih Karagümrük | 5–4 | 9 |
| 3890054 | 5. Matchday | Tannadice Park | Dundee United FC | Celtic FC | 0–9 | 9 |
| 3913740 | Group H | Parc des Princes | Paris Saint-Germain | Maccabi Haifa | 7–2 | 9 |

> **Nhận xét đối chiếu:** Có **1.196 trận** có từ 5 bàn trở lên sau khi loại luân lưu, gồm 582 trận mùa 2022/2023 và 614 trận mùa 2023/2024. Tổng cao nhất là 10 bàn (`3844906` Atalanta BC 8–2 US Salernitana 1919, `3851241` Zulte Waregem 5–5 KAS Eupen, `3852668` AZ Alkmaar 5–5 FC Utrecht).

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Tối ưu tránh bùng nổ tích Descartes:** `FILTER` thu hẹp trước tập `Game ID` từ $7.280$ xuống $M = 1.196$ trận trước khi kết hợp `NONEMPTY` với `Official Match Count`.
* **Độ phức tạp thời gian:** $O(N_{\text{games}} + M \log M)$ với $N_{\text{games}} = 7.280$.
