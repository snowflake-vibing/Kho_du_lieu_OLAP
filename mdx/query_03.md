# MDX Query 03: Cầu thủ đạt trên 20 đóng góp bàn thắng (G+A > 20) mùa 2023/2024
## (Calculated Measure `Goal Contributions`, hàm `FILTER` và sắp xếp `ORDER (BDESC)`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 3. Thống kê tổng số phút thi đấu (Minutes_Played) và tổng đóng góp bàn thắng (Goal_Contributions) của các cầu thủ có trên 20 lần góp công vào bàn thắng trong mùa giải Season 2023/2024.
  *[Thuộc tính: Player_Name, Minutes_Played, Goal_Contributions, Season]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Trận đấu/Mùa (`DIM_Game`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Player ID]`, `[DIM Game].[Season]`, `[Measures].[Minutes Played]`, Calculated Measure `[Measures].[Goal Contributions]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    p.Player_ID,
    p.Player_Name,
    SUM(f.Minutes_Played)       AS Minutes_Played,
    SUM(f.Goals)                AS Goals,
    SUM(f.Assists)              AS Assists,
    SUM(f.Goals + f.Assists)    AS Goal_Contributions
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
JOIN dbo.DIM_Game   AS g ON f.Game_ID   = g.Game_ID
WHERE g.Season = 2023
GROUP BY p.Player_ID, p.Player_Name
HAVING SUM(f.Goals + f.Assists) > 20
ORDER BY Goal_Contributions DESC, Minutes_Played ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** trong Cube Designer ở chế độ **Design Mode**.
- Dòng 1 Filter Pane: `DIM Game → Season`, Operator = `Equal`, chọn `2023/2024`.
- Dòng 2 Filter Pane: `DIM Player → Player ID`, Operator = `Custom`, dán biểu thức `FILTER` bên dưới.
- Kéo `DIM Player → Player ID` vào **Rows**; kéo `Minutes Played` và `Goal Contributions` vào **Values** → bấm **Click to execute the query**.

```mdx
FILTER(
    NONEMPTY(
        [DIM Player].[Player ID].[Player ID].MEMBERS,
        ( [Measures].[Goal Contributions], [DIM Game].[Season].&[2023] )
    ),
    ( [Measures].[Goal Contributions], [DIM Game].[Season].&[2023] ) > 20
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$L$3`.
- Kéo `DIM Game → Season` vào **Filters** (`2023/2024`); kéo `DIM Player → Player ID` vào **Rows**; kéo `Minutes Played` và `Goal Contributions` vào **Values**.
- Tại `Row Labels` → **Value Filters → Greater Than…** → chọn `Goal Contributions`, nhập `20` → **OK**, sắp xếp giảm dần.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_03.mdx`)
- Trục `COLUMNS`: xuất `[Measures].[Minutes Played]` và Calculated Measure `[Measures].[Goal Contributions]` (= `Goals + Assists`).
- Trục `ROWS`: tiền lọc bằng `NONEMPTY`, lọc điều kiện `> 20` và sắp xếp phẳng toàn cục bằng `ORDER(..., BDESC)`.
- Mệnh đề `WHERE`: cố định mùa `Season = 2023`.

```mdx
SELECT
    {
        [Measures].[Minutes Played],
        [Measures].[Goal Contributions]
    } ON COLUMNS,
    ORDER(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player ID].[Player ID].MEMBERS,
                (
                    [Measures].[Goal Contributions],
                    [DIM Game].[Season].&[2023]
                )
            ),
            [Measures].[Goal Contributions] > 20
        ),
        [Measures].[Goal Contributions],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ( [DIM Game].[Season].&[2023] );
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| STT | Player_ID | Player_Name | Minutes_Played | Goals | Assists | Goal_Contributions |
| :---: | ---: | :--- | ---: | ---: | ---: | ---: |
| 1 | 132098 | Harry Kane | 3.908 | 44 | 12 | 56 |
| 2 | 72522 | Luuk de Jong | 3.406 | 32 | 15 | 47 |
| 3 | 325443 | Viktor Gyökeres | 3.537 | 34 | 11 | 45 |
| 4 | 342229 | Kylian Mbappé | 3.239 | 35 | 7 | 42 |
| 5 | 68863 | Mauro Icardi | 3.555 | 28 | 11 | 39 |
| 6 | 418560 | Erling Haaland | 3.337 | 33 | 5 | 38 |
| 7 | 58864 | Pierre-Emerick Aubameyang | 3.659 | 27 | 11 | 38 |
| 8 | 148455 | Mohamed Salah | 2.935 | 23 | 14 | 37 |
| 9 | 368887 | Loïs Openda | 3.274 | 28 | 7 | 35 |
| 10 | 406635 | Phil Foden | 3.555 | 24 | 11 | 35 |

> **Nhận xét đối chiếu:** Có đúng **99 cầu thủ** đạt trên 20 đóng góp bàn thắng mùa 2023/2024 (dẫn đầu là **Harry Kane** với 56 G+A trong 3.908 phút). Dùng khóa `[DIM Player].[Player ID]` là bắt buộc vì nếu nhóm theo `Player_Name` sẽ gộp nhầm tên trùng thành 101 dòng.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian lý thuyết:** $7.069 \text{ cầu thủ} \times 2 \text{ mùa} = 14.138 \text{ cells}$.
* **Sau lọc `NONEMPTY` & `FILTER`:** Còn $M = 99$ cầu thủ đạt ngưỡng `G+A > 20`; bộ nhớ kết quả $O(99)$.
* **Độ phức tạp thời gian:** $O(N_{2023}) + O(M \log M)$ với $N_{2023} = 4.832$ cầu thủ ra sân trong mùa 2023/2024.
