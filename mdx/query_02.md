# MDX Query 02: Top 10 tiền vệ kiến tạo nhiều nhất tại các giải Vô địch Quốc gia
## (Lọc đa điều kiện trên 2 chiều độc lập kết hợp `TOPCOUNT`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 2. Liệt kê 10 cầu thủ ở vị trí Tiền vệ (Main_Position) có số đường kiến tạo (Assists) nhiều nhất tại các giải đấu thuộc phân loại giải Vô địch Quốc gia (Competition_Type = 'domestic_league').
  *[Thuộc tính: Player_Name, Assists, Main_Position, Competition_Type]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Giải đấu (`DIM_Competition`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Player ID]`, `[DIM Player].[Main Position]`, `[DIM Competition].[Competition Type]`, `[Measures].[Assists]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT TOP 10
    p.Player_ID,
    p.Player_Name,
    p.Main_Position,
    c.Competition_Type,
    SUM(f.Assists) AS Total_Assists
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player      AS p ON f.Player_ID      = p.Player_ID
JOIN dbo.DIM_Competition AS c ON f.Competition_ID = c.Competition_ID
WHERE p.Main_Position = N'Midfield'
  AND c.Competition_Type = N'domestic_league'
GROUP BY p.Player_ID, p.Player_Name, p.Main_Position, c.Competition_Type
ORDER BY Total_Assists DESC, p.Player_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở Cube `DW Football Transfermarkt.cube` → tab **Browser** → bật **Design Mode**.
- Dòng 1 Filter Pane: `DIM Player → Main Position`, Operator = `Equal`, chọn `Midfield`.
- Dòng 2 Filter Pane: `DIM Competition → Competition Type`, Operator = `Equal`, chọn `domestic_league`.
- Dòng 3 Filter Pane: `DIM Player → Player ID`, Operator = `Custom`, dán biểu thức `TOPCOUNT` bên dưới.
- Kéo `DIM Player → Player ID` vào **Rows** và `Measures → Assists` vào **Values** → bấm **Click to execute the query**.

```mdx
TOPCOUNT(
    NONEMPTY(
        [DIM Player].[Player ID].[Player ID].MEMBERS,
        (
            [Measures].[Assists],
            [DIM Player].[Main Position].&[Midfield],
            [DIM Competition].[Competition Type].&[domestic_league]
        )
    ),
    10,
    (
        [Measures].[Assists],
        [DIM Player].[Main Position].&[Midfield],
        [DIM Competition].[Competition Type].&[domestic_league]
    )
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$G$3`.
- Kéo `DIM Player → Main Position` và `DIM Competition → Competition Type` vào **Filters**; kéo `DIM Player → Player ID` vào **Rows**; kéo `Assists` vào **Values**.
- Chọn `Main Position = Midfield` và `Competition Type = domestic_league`.
- Tại `Row Labels` → **Value Filters → Top 10…** → `Top 10 Items by Assists`, sắp xếp giảm dần.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_02.mdx`)
- Trục `COLUMNS`: xuất `[Measures].[Assists]`.
- Trục `ROWS`: dùng `TOPCOUNT(..., 10, [Measures].[Assists])` trên tập tiền vệ có kiến tạo tại các giải VĐQG.
- Mệnh đề `WHERE`: cắt lát đồng thời theo `Midfield` và `domestic_league`.

```mdx
SELECT
    { [Measures].[Assists] } ON COLUMNS,
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player ID].[Player ID].MEMBERS,
            (
                [Measures].[Assists],
                [DIM Player].[Main Position].&[Midfield],
                [DIM Competition].[Competition Type].&[domestic_league]
            )
        ),
        10,
        [Measures].[Assists]
    ) ON ROWS
FROM [DW Football Transfermarkt]
WHERE (
    [DIM Player].[Main Position].&[Midfield],
    [DIM Competition].[Competition Type].&[domestic_league]
);
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Hạng | Player_ID | Player_Name | Assists |
| :---: | ---: | :--- | ---: |
| 1 | 88755 | Kevin De Bruyne | 28 |
| 2 | 408574 | Joey Veerman | 26 |
| 3 | 406634 | Matt O'Riley | 22 |
| 4 | 566931 | Xavi Simons | 22 |
| 5 | 381963 | Mike Tresor | 21 |
| 6 | 7161 | Jonas Hofmann | 20 |
| 7 | 187492 | Julian Brandt | 20 |
| 8 | 580195 | Jamal Musiala | 19 |
| 9 | 82873 | Pascal Groß | 18 |
| 10 | 215592 | Haris Hajradinovic | 18 |

> **Nhận xét đối chiếu:** **Kevin De Bruyne** dẫn đầu toàn hệ thống VĐQG với 28 kiến tạo, kế tiếp là **Joey Veerman** (26), **Matt O'Riley** (22) và **Xavi Simons** (22). Ở mốc 18 kiến tạo có 7 tiền vệ đồng hạng (trong đó Pascal Groß và Haris Hajradinovic đứng vị trí 9–10 theo thứ tự `Player_ID`), nên Excel Top 10 mặc định giữ 15 dòng trong khi `TOPCOUNT` trả đúng 10 dòng.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian lý thuyết:** $2.091 \text{ tiền vệ} \times 3 \text{ loại giải} = 6.273 \text{ cells}$ (nằm trên tổng 7.069 cầu thủ).
* **Sau tối ưu `NONEMPTY`:** Giảm xuống tập con $M$ các tiền vệ có ít nhất 1 kiến tạo ở 10 giải VĐQG; bộ nhớ kết quả $O(10)$.
* **Độ phức tạp thời gian:** $O(M \log 10)$ trên Formula Engine kết hợp quét phân vùng ở Storage Engine.
