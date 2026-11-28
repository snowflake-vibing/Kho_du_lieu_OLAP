# MDX Query 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024
## (Ứng dụng `TOPCOUNT`, `NONEMPTY` và thuộc tính khóa `Player ID` chống gộp cầu thủ trùng tên)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 1. Thống kê 10 cầu thủ có số bàn thắng nhiều nhất tại giải đấu có mã giải Competition_ID = 'GB1' (Giải Ngoại Hạng Anh - Competition_Name) trong mùa giải Season 2023/2024.
  *[Thuộc tính: Player_Name, Goals, Competition_ID, Competition_Name, Season]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Giải đấu (`DIM_Competition`), Trận đấu/Mùa giải (`DIM_Game`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Player ID]`, `[DIM Competition].[Competition ID]`, `[DIM Game].[Season]`, `[Measures].[Goals]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT TOP 10
    p.Player_ID,
    p.Player_Name,
    c.Competition_ID,
    c.Competition_Name,
    g.Season,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player      AS p ON f.Player_ID      = p.Player_ID
JOIN dbo.DIM_Competition AS c ON f.Competition_ID = c.Competition_ID
JOIN dbo.DIM_Game        AS g ON f.Game_ID        = g.Game_ID
WHERE c.Competition_ID = N'GB1'
  AND g.Season = 2023
GROUP BY p.Player_ID, p.Player_Name, c.Competition_ID, c.Competition_Name, g.Season
ORDER BY Total_Goals DESC, p.Player_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở Cube `DW Football Transfermarkt.cube` → tab **Browser** → bật **Design Mode**.
- Dòng 1 Filter Pane: Dimension = `DIM Competition`, Hierarchy = `Competition ID`, Operator = `Equal`, tích chọn `GB1`.
- Dòng 2 Filter Pane: Dimension = `DIM Game`, Hierarchy = `Season`, Operator = `Equal`, tích chọn `2023/2024`.
- Dòng 3 Filter Pane: Dimension = `DIM Player`, Hierarchy = `Player ID`, Operator = `Custom`, dán biểu thức `TOPCOUNT` bên dưới vào Expression Builder.
- Kéo `DIM Player → Player ID` (hiển thị `Player_Name`) và `DIM Competition → Competition Name` vào **Rows**; kéo `Measures → Goals` vào **Values** → bấm **Click to execute the query**.

```mdx
TOPCOUNT(
    NONEMPTY(
        [DIM Player].[Player ID].[Player ID].MEMBERS,
        (
            [Measures].[Goals],
            [DIM Competition].[Competition ID].&[GB1],
            [DIM Game].[Season].&[2023]
        )
    ),
    10,
    (
        [Measures].[Goals],
        [DIM Competition].[Competition ID].&[GB1],
        [DIM Game].[Season].&[2023]
    )
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Kết nối Excel tới `SSAS_Football_Transfermarkt` → Cube `DW Football Transfermarkt`, đặt PivotTable tại `Sheet1!$A$3`.
- Kéo `DIM Competition → Competition ID` và `DIM Game → Season` vào **Filters**; kéo `DIM Player → Player ID` vào **Rows**; kéo `Goals` vào **Values**.
- Chọn `Competition ID = GB1` và `Season = 2023/2024`.
- Tại `Row Labels` → **Value Filters → Top 10…** → `Top 10 Items by Goals`, sắp xếp giảm dần theo `Goals` (dùng **Create Set Using MDX…** nếu cần cắt đúng 10 dòng khi có đồng hạng).

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_01.mdx`)
- Trục `COLUMNS`: xuất độ đo `[Measures].[Goals]`.
- Trục `ROWS`: dùng `TOPCOUNT` trên tập cầu thủ có phát sinh bàn thắng đã lọc trước bằng `NONEMPTY`.
- Mệnh đề `WHERE`: cắt lát theo giải `GB1` và mùa `Season = 2023` trên `DIM Game`.

```mdx
SELECT
    { [Measures].[Goals] } ON COLUMNS,
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player ID].[Player ID].MEMBERS,
            (
                [Measures].[Goals],
                [DIM Competition].[Competition ID].&[GB1],
                [DIM Game].[Season].&[2023]
            )
        ),
        10,
        [Measures].[Goals]
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE (
    [DIM Competition].[Competition ID].&[GB1],
    [DIM Game].[Season].&[2023]
);
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Hạng | Player_ID | Player_Name | Goals |
| :---: | ---: | :--- | ---: |
| 1 | 418560 | Erling Haaland | 27 |
| 2 | 568177 | Cole Palmer | 22 |
| 3 | 349066 | Alexander Isak | 21 |
| 4 | 258889 | Dominic Solanke | 19 |
| 5 | 324358 | Ollie Watkins | 19 |
| 6 | 406635 | Phil Foden | 19 |
| 7 | 148455 | Mohamed Salah | 18 |
| 8 | 91845 | Heung-min Son | 17 |
| 9 | 314875 | Jarrod Bowen | 16 |
| 10 | 420002 | Jean-Philippe Mateta | 16 |

> **Nhận xét đối chiếu:** Kết quả MDX và Cube Browser trả về đúng 10 dòng, dẫn đầu là **Erling Haaland** (27 bàn), **Cole Palmer** (22 bàn), **Alexander Isak** (21 bàn). Do có 3 cầu thủ đồng hạng 16 bàn (Bukayo Saka, Jean-Philippe Mateta, Jarrod Bowen), Excel Top 10 mặc định hiển thị 11 dòng giữ đồng hạng còn `TOPCOUNT` cắt đúng 10 dòng.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian lý thuyết:** $7.069 \text{ cầu thủ} \times 13 \text{ giải} \times 2 \text{ mùa} = 183.794 \text{ cells}$.
* **Sau tối ưu `NONEMPTY`:** Storage Engine quét Bitmap Index co hẹp xuống $M \approx 260$ cầu thủ ghi bàn ở GB1 mùa 2023/2024; bộ nhớ kết quả $O(10)$.
* **Độ phức tạp thời gian:** $O(M \log 10)$ nhờ Min-Heap của `TOPCOUNT`, nhanh hơn sắp xếp toàn phần $O(M \log M)$.
