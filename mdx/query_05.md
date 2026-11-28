# MDX Query 05: So sánh bàn thắng theo chân thuận (Foot) và vị trí chi tiết (Sub_Position)
## (Ma trận xoay chiều hai thuộc tính `Sub_Position` × `Foot`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 5. So sánh tổng số bàn thắng ghi được (Goals) giữa các cầu thủ thuận chân Trái, chân Phải và Hai chân (Foot) theo từng vị trí thi đấu chi tiết (Sub_Position).
  *[Thuộc tính: Foot, Sub_Position, Goals]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player.Foot`, `DIM_Player.Sub_Position`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Foot]`, `[DIM Player].[Sub Position]`, `[Measures].[Goals]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    p.Sub_Position,
    SUM(CASE WHEN p.Foot = N'left'  THEN f.Goals ELSE 0 END) AS Left_Goals,
    SUM(CASE WHEN p.Foot = N'right' THEN f.Goals ELSE 0 END) AS Right_Goals,
    SUM(CASE WHEN p.Foot = N'both'  THEN f.Goals ELSE 0 END) AS Both_Goals,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
WHERE p.Foot IS NOT NULL
  AND p.Sub_Position IS NOT NULL
GROUP BY p.Sub_Position
ORDER BY Total_Goals DESC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Dòng 1 Filter Pane: `DIM Player → Foot`, Operator = `In`, tích chọn `left`, `right`, `both`.
- Dòng 2 Filter Pane: `DIM Player → Sub Position`, Operator = `Not Equal`, chọn `Unknown`.
- Kéo `Sub Position` vào **Rows**, `Foot` vào **Columns** và `Goals` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$X$3`.
- Kéo `Sub Position` vào **Rows**, `Foot` vào **Columns**, `Goals` vào **Values**.
- Lọc cột `Foot` giữ `left`, `right`, `both`; lọc `Sub Position` bỏ `Unknown`, sắp xếp giảm dần theo Grand Total.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_05.mdx`)
- Trục `COLUMNS`: liệt kê ba thành viên chân thuận `{left, right, both}`.
- Trục `ROWS`: giữ toàn bộ 13 vị trí chi tiết hợp lệ (loại `[Unknown]`) và sắp xếp giảm dần theo tổng bàn thắng.

```mdx
SELECT
    {
        [DIM Player].[Foot].&[left],
        [DIM Player].[Foot].&[right],
        [DIM Player].[Foot].&[both]
    } ON COLUMNS,
    NON EMPTY ORDER(
        EXCEPT(
            [DIM Player].[Sub Position].[Sub Position].MEMBERS,
            { [DIM Player].[Sub Position].[Unknown] }
        ),
        ( [Measures].[Goals], [DIM Player].[Foot].[All] ),
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Sub_Position | left | right | both | Tổng bàn thắng |
| :--- | ---: | ---: | ---: | ---: |
| Centre-Forward | 1.114 | 5.457 | 273 | 6.844 |
| Left Winger | 186 | 2.015 | 79 | 2.280 |
| Right Winger | 1.207 | 783 | 76 | 2.066 |
| Attacking Midfield | 667 | 1.308 | 59 | 2.034 |
| Central Midfield | 356 | 1.518 | 90 | 1.964 |
| Centre-Back | 422 | 977 | 24 | 1.423 |
| Defensive Midfield | 102 | 655 | 17 | 774 |
| Right-Back | 0 | 629 | 16 | 645 |
| Left-Back | 518 | 19 | 3 | 540 |
| Second Striker | 93 | 242 | 0 | 335 |
| Right Midfield | 34 | 90 | 8 | 132 |
| Left Midfield | 48 | 43 | 0 | 91 |
| Goalkeeper | 0 | 2 | 0 | 2 |
| **Tổng hợp hợp lệ** | **4.747** | **13.738** | **645** | **19.130** |

> **Nhận xét đối chiếu:** Đủ 13 vị trí chi tiết cho tổng 19.130 bàn thắng hợp lệ (còn 43 bàn trên 824 lượt ra sân thiếu thông tin `Foot`). Nổi bật tính nghịch chân chiến thuật: `Left Winger` ghi chủ yếu bằng chân phải (2.015 bàn), còn `Right Winger` ghi phần lớn bằng chân trái (1.207 bàn).

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian ma trận:** $13 \text{ vị trí} \times 3 \text{ chân thuận} = 39 \text{ cells}$.
* **Bộ nhớ & Thời gian:** $O(13 \log 13) + O(39)$, phản hồi gần như tức thì do toàn bộ tính trên cấp tổng hợp sẵn.
