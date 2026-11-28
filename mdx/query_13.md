# MDX Query 13: Tổng số lượt ra sân và số lượng cầu thủ của các CLB theo quy mô đội hình
## (Kết hợp `Appearance Count` và `Distinct Player Count` (`DistinctCount` Measure Group))

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 13. Thống kê tổng số lượt ra sân thi đấu (Appearance_ID) và số lượng cầu thủ (Player_ID) của các câu lạc bộ (Club_Name) phân theo quy mô số lượng cầu thủ đăng ký trong đội hình (Squad_Size).
  *[Thuộc tính: Appearance_ID, Player_ID, Squad_Size, Club_Name]*
* **Cấp độ dữ liệu (Grain):** `FACT Player Match Perf` + `FACT Player Distinct`
* **Đối tượng phân tích:** CLB (`DIM_Club.Club_ID`, `Squad_Size`), Lượt ra sân (`FACT_Player_Match_Perf`, `FACT Player Distinct`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Club].[Club ID]`, `[DIM Club].[Squad Size]`, `[Measures].[Appearance Count]`, `[Measures].[Distinct Player Count]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    c.Club_ID,
    c.Club_Name,
    c.Squad_Size,
    COUNT(f.Appearance_ID)      AS Appearance_Count,
    COUNT(DISTINCT f.Player_ID) AS Distinct_Player_Count
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Club AS c ON f.Club_ID = c.Club_ID
GROUP BY c.Club_ID, c.Club_Name, c.Squad_Size
ORDER BY Appearance_Count DESC, c.Club_ID ASC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Kéo `DIM Club → Squad Size` và `DIM Club → Club ID` vào **Rows**; kéo `Appearance Count` và `Distinct Player Count` vào **Values** → bấm **Click to execute the query**.
- (Tùy chọn) Nếu chỉ phân tích các CLB có `Squad_Size` từ CSV gốc, lọc `DIM Club → Squad Size Not Equal Unknown`.

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$BL$3`.
- Kéo `DIM Club → Squad Size` và `Club ID` vào **Rows**; kéo `Appearance Count` và `Distinct Player Count` vào **Values**.
- Bật Tabular Form và sắp xếp giảm dần theo `Appearance Count`.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_13.mdx`)
- `[Measures].[Appearance Count]` đếm dòng trên `FACT Player Match Perf`, còn `[Measures].[Distinct Player Count]` thực thi `DistinctCount(Player_ID)` trên Measure Group `FACT Player Distinct`.
- Dùng `NONEMPTY(CrossJoin([Club ID], [Squad Size]), [Appearance Count])` giữ đủ 235 CLB có lượt ra sân (bao gồm 8 CLB bổ sung mang `Squad Size = Unknown`).

```mdx
SELECT
    {
        [Measures].[Appearance Count],
        [Measures].[Distinct Player Count]
    } ON COLUMNS,
    ORDER(
        NONEMPTY(
            CrossJoin(
                EXCEPT(
                    [DIM Club].[Club ID].[Club ID].MEMBERS,
                    { [DIM Club].[Club ID].[Unknown] }
                ),
                [DIM Club].[Squad Size].[Squad Size].MEMBERS
            ),
            [Measures].[Appearance Count]
        ),
        [Measures].[Appearance Count],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| Club_ID | Club_Name | Squad_Size | Appearance_Count | Distinct_Player_Count |
| ---: | :--- | ---: | ---: | ---: |
| 12 | Associazione Sportiva Roma | 27 | 1.622 | 46 |
| 5 | AC Milan | 32 | 1.562 | 49 |
| 46 | Inter Milan | 25 | 1.549 | 41 |
| 418 | Real Madrid | 30 | 1.526 | 35 |
| 368 | Sevilla FC | 27 | 1.505 | 48 |
| 6195 | SSC Napoli | 41 | 1.471 | 35 |
| 31 | Liverpool FC | 29 | 1.453 | 43 |
| 15 | Bayer 04 Leverkusen | 36 | 1.452 | 40 |
| 681 | Real Sociedad | 28 | 1.445 | 43 |
| 131 | FC Barcelona | 28 | 1.440 | 42 |

> **Nhận xét đối chiếu:** Có **235 CLB** có lượt ra sân (227 CLB có `Squad_Size` hợp lệ và 8 CLB bổ sung từ `games.csv` có `Squad_Size = Unknown` với 76 lượt ra sân). **AS Roma** sử dụng tổng cộng 1.622 lượt ra sân từ 46 cầu thủ khác nhau.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian sau lọc:** $M = 235$ CLB (trên 272 CLB trong `DIM_Club`).
* **Độ phức tạp thời gian:** Storage Engine tính sẵn các khối bitmap cho `DistinctCount(Player_ID)` trên từng `Club_ID`, chi phí sắp xếp $O(M \log M)$.
