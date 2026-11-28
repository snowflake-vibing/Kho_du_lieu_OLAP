# MDX Query 06: Chiều cao trung bình, bàn thắng và thẻ vàng theo vị trí thi đấu chính
## (Tính chiều cao trên tập cầu thủ duy nhất bằng `EXISTING` + `CrossJoin`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 6. Thống kê chiều cao trung bình (Height_In_Cm), tổng bàn thắng (Goals) và tổng số thẻ vàng (Yellow_Cards) của các cầu thủ theo từng vị trí thi đấu chính (Main_Position).
  *[Thuộc tính: Height_In_Cm, Main_Position, Goals, Yellow_Cards]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` + Tập cầu thủ duy nhất
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player.Main_Position`, `Height_In_Cm`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Main Position]`, `[Measures].[Avg Height Cm]`, `[Measures].[Max Height Cm]`, `[Measures].[Min Height Cm]`, `[Measures].[Goals]`, `[Measures].[Yellow Cards]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

WITH Height_By_Pos AS (
    SELECT
        Main_Position,
        COUNT(Height_In_Cm)                 AS Valid_Height_Players,
        AVG(CAST(Height_In_Cm AS FLOAT))    AS Avg_Height_Cm,
        MAX(Height_In_Cm)                   AS Max_Height_Cm,
        MIN(Height_In_Cm)                   AS Min_Height_Cm
    FROM dbo.DIM_Player
    WHERE Main_Position <> N'Missing'
    GROUP BY Main_Position
),
Perf_By_Pos AS (
    SELECT
        p.Main_Position,
        SUM(f.Goals)        AS Total_Goals,
        SUM(f.Yellow_Cards) AS Total_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf AS f
    JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
    WHERE p.Main_Position <> N'Missing'
    GROUP BY p.Main_Position
)
SELECT
    h.Main_Position,
    h.Valid_Height_Players,
    ROUND(h.Avg_Height_Cm, 2) AS Avg_Height_Cm,
    h.Max_Height_Cm,
    h.Min_Height_Cm,
    pr.Total_Goals,
    pr.Total_Yellow_Cards
FROM Height_By_Pos AS h
JOIN Perf_By_Pos   AS pr ON h.Main_Position = pr.Main_Position
ORDER BY pr.Total_Goals DESC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Player → Main Position`, Operator = `Not Equal`, chọn `Missing`.
- Kéo `Main Position` vào **Rows**; kéo `Avg Height Cm`, `Max Height Cm`, `Min Height Cm`, `Goals`, `Yellow Cards` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$AC$3`.
- Kéo `Main Position` vào **Rows**; kéo 5 độ đo `Avg Height Cm`, `Max Height Cm`, `Min Height Cm`, `Goals`, `Yellow Cards` vào **Values**.
- Bỏ tích `Missing` trên `Row Labels` và sắp xếp giảm dần theo `Goals`.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_06.mdx`)
- Các độ đo `Avg/Max/Min Height Cm` đã định nghĩa trong tab `Calculations` dùng `EXISTING CrossJoin([Player ID], [Height In Cm])` nên luôn tính trung bình theo **từng cầu thủ duy nhất**, không bị nhân bản theo số lần ra sân và tự động bỏ qua `NULL/Unknown`.
- Loại trừ thành viên `Missing` trên `Main Position` và sắp xếp giảm dần theo `Goals`.

```mdx
SELECT
    {
        [Measures].[Avg Height Cm],
        [Measures].[Max Height Cm],
        [Measures].[Min Height Cm],
        [Measures].[Goals],
        [Measures].[Yellow Cards]
    } ON COLUMNS,
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].&[Missing] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Main_Position | Cầu thủ có chiều cao | Avg Height | Max | Min | Goals | Yellow_Cards |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Attack | 2.079 | 180,89 | 201 | 160 | 11.561 | 6.292 |
| Midfield | 2.045 | 180,19 | 202 | 160 | 5.000 | 10.050 |
| Defender | 2.283 | 183,96 | 206 | 163 | 2.610 | 11.551 |
| Goalkeeper | 539 | 190,53 | 206 | 179 | 2 | 801 |

> **Nhận xét đối chiếu:** Thủ môn (`Goalkeeper`) có chiều cao trung bình cao nhất (190,53 cm) nhưng chỉ ghi 2 bàn thắng; tiền đạo (`Attack`) ghi nhiều bàn nhất (11.561 bàn); hậu vệ (`Defender`) nhận nhiều thẻ vàng nhất (11.551 thẻ). Hai hồ sơ `Missing` không có bàn thắng hay thẻ phạt nào.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian đánh giá:** $4 \text{ tuyến} \times 7.069 \text{ cầu thủ}$.
* **Độ phức tạp thời gian:** $O(N_{\text{players}})$ nhờ `EXISTING` thu hẹp tập cầu thủ theo từng vị trí hiện hành trên Formula Engine; bộ nhớ kết quả $O(4)$.
