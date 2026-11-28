# MDX Query 15: Bàn thắng và thẻ phạt của cầu thủ trẻ sinh từ 01/01/2004 theo ngày thi đấu
## (Truy vấn nhóm ngày sinh `Date_Of_Birth >= 2004-01-01` bằng `WITH SET` + `CDate` / `Is_Youth_2004`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 15. Thống kê số lượng bàn thắng (Goals) và thẻ phạt (Yellow_Cards, Red_Cards) của các cầu thủ trẻ sinh từ ngày 01/01/2004 (Date_Of_Birth) theo ngày thi đấu cụ thể (Full_Date)
  *[Thuộc tính: Date_Of_Birth, Full_Date, Goals, Yellow_Cards, Red_Cards]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` (Lượt ra sân)
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player.Date_Of_Birth`, `Is_Youth_2004`), Ngày thi đấu (`DIM_Time.Full_Date`), Lượt ra sân (`FACT_Player_Match_Perf`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Player].[Date Of Birth]`, `[DIM Player].[Is Youth 2004]`, `[DIM Time].[Full Date]`, `[Measures].[Goals]`, `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    t.Full_Date,
    COUNT(f.Appearance_ID) AS Youth_Appearances,
    SUM(f.Goals)           AS Goals,
    SUM(f.Yellow_Cards)    AS Yellow_Cards,
    SUM(f.Red_Cards)       AS Red_Cards
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Player AS p ON f.Player_ID = p.Player_ID
JOIN dbo.DIM_Time   AS t ON f.Time_ID   = t.Time_ID
WHERE p.Date_Of_Birth >= '2004-01-01'
GROUP BY t.Full_Date
ORDER BY Goals DESC, Yellow_Cards DESC, t.Full_Date DESC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Player → Is Youth 2004`, Operator = `Equal`, chọn `1` (tương đương `Date_Of_Birth >= 2004-01-01`).
- Kéo `DIM Time → Full Date` vào **Rows**; kéo `Goals`, `Yellow Cards`, `Red Cards` vào **Values** → bấm **Click to execute the query**.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$BV$3`.
- Kéo `DIM Player → Is Youth 2004` vào **Filters** (`1`); kéo `DIM Time → Full Date` vào **Rows**; kéo `Goals`, `Yellow Cards`, `Red Cards` vào **Values**.
- Sắp xếp giảm dần theo `Goals` (hoặc tăng dần theo ngày thi đấu).

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_15.mdx`)
- `WITH SET [YouthPlayers2004]` dùng `CDate("2004-01-01")` lọc trực tiếp các ngày sinh hợp lệ từ 01/01/2004 trở đi.
- Truy vấn con `FROM (SELECT [YouthPlayers2004] ON COLUMNS ...)` áp dụng tập lọc lên toàn bộ trục (cho kết quả đồng nhất tuyệt đối với `WHERE ([DIM Player].[Is Youth 2004].&[1])`).

```mdx
WITH
    SET [YouthPlayers2004] AS
        FILTER(
            EXCEPT(
                [DIM Player].[Date Of Birth].[Date Of Birth].MEMBERS,
                { [DIM Player].[Date Of Birth].[Unknown] }
            ),
            CDate([DIM Player].[Date Of Birth].CURRENTMEMBER.NAME)
                >= CDate("2004-01-01")
        )
SELECT
    {
        [Measures].[Goals],
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            [DIM Time].[Full Date].[Full Date].MEMBERS,
            [Measures].[Appearance Count]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS
FROM (
    SELECT [YouthPlayers2004] ON COLUMNS
    FROM [DW Football Transfermarkt]
);
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Full_Date | Lượt ra sân trẻ | Goals | Yellow_Cards | Red_Cards |
| :---: | ---: | ---: | ---: | ---: |
| 2024-05-19 | 95 | 9 | 6 | 0 |
| 2024-02-04 | 64 | 9 | 3 | 0 |
| 2024-02-25 | 71 | 8 | 6 | 0 |
| 2023-10-22 | 52 | 8 | 4 | 0 |
| 2024-02-03 | 68 | 6 | 10 | 0 |
| 2024-05-12 | 83 | 6 | 7 | 0 |
| 2023-10-08 | 56 | 6 | 6 | 0 |
| 2023-12-13 | 18 | 6 | 2 | 0 |
| 2024-02-18 | 66 | 5 | 12 | 0 |
| 2023-10-01 | 40 | 5 | 6 | 1 |

> **Nhận xét đối chiếu:** Nhóm cầu thủ sinh từ 01/01/2004 gồm **676 cầu thủ**, thực hiện **6.566 lượt ra sân** trong **441 ngày thi đấu**, ghi 403 bàn, 682 thẻ vàng và 14 thẻ đỏ. Hai ngày bùng nổ nhất là `2024-05-19` và `2024-02-04` (cùng 9 bàn).

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian sau lọc:** $488 \text{ ngày thi đấu} \rightarrow M = 441$ ngày có cầu thủ trẻ ra sân.
* **Độ phức tạp thời gian:** $O(D_{\text{dob}} + M \log M)$ với $D_{\text{dob}} \le 7.069$ ngày sinh duy nhất trong `DIM_Player`.
