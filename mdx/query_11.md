# MDX Query 11: Đếm số trận sân nhà của các CLB có sức chứa sân nhà trên 60.000 chỗ
## (Truy vấn cấp trận trên `DIM Game` kết hợp Role-Playing `DIM Home Club`)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn (Mục 1.3 Chương 1):** 11. Đếm số trận sân nhà của các CLB có sức chứa sân nhà theo hồ sơ CLB trên 60.000 chỗ.
  *[Thuộc tính: Game_ID, Home_Club_ID, Club_ID, Club_Name, Stadium_Name, Stadium_Seats]*
* **Cấp độ dữ liệu (Grain):** `DIM Game` Measure Group (Trận đấu: 7.280 dòng)
* **Đối tượng phân tích:** Trận đấu (`DIM_Game` Measure Group), CLB chủ nhà (`DIM_Home_Club`).
* **Thuộc tính & Thước đo trong Cube:** `[DIM Home Club].[Club ID]`, `[DIM Home Club].[Stadium Name]`, `[DIM Home Club].[Stadium Seats]`, `[Measures].[Stadium Seats Value]`, `[Measures].[Official Match Count]`.

### Truy vấn T-SQL đối chiếu trên `DW_Football_Transfermarkt`
```sql
USE DW_Football_Transfermarkt;
GO

SELECT
    c.Club_ID,
    c.Club_Name,
    c.Stadium_Name,
    c.Stadium_Seats,
    COUNT(g.Game_ID) AS Home_Games
FROM dbo.DIM_Club AS c
JOIN dbo.DIM_Game AS g ON g.Home_Club_ID = c.Club_ID
WHERE c.Stadium_Seats > 60000
GROUP BY c.Club_ID, c.Club_Name, c.Stadium_Name, c.Stadium_Seats
ORDER BY c.Stadium_Seats DESC, Home_Games DESC;
```

---

## 2. Hướng dẫn thực thi đồng quy trên 3 công cụ

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)
- Mở tab **Browser** ở chế độ **Design Mode**.
- Filter Pane: `DIM Home Club → Stadium Seats`, Operator = `Custom` (không dùng toán tử không tồn tại trong SSDT), dán biểu thức `FILTER` `> 60000` bên dưới.
- Kéo `DIM Home Club → Club ID` và `Stadium Name` vào **Rows**; kéo `Stadium Seats Value` và `Official Match Count` vào **Values** → bấm **Click to execute the query**.

```mdx
FILTER(
    EXCEPT(
        [DIM Home Club].[Stadium Seats].[Stadium Seats].MEMBERS,
        { [DIM Home Club].[Stadium Seats].[Unknown] }
    ),
    [DIM Home Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE > 60000
)
```

### 2.2. Sử dụng PivotTable trong Microsoft Excel
> **Kết nối chuẩn:** Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**, chọn server `localhost`, database `SSAS_Football_Transfermarkt`, Cube `DW Football Transfermarkt`.

- Đặt PivotTable tại `Sheet1!$BB$3`.
- Kéo `DIM Home Club → Club ID` và `Stadium Name` vào **Rows**; kéo `Stadium Seats Value` và `Official Match Count` vào **Values**.
- Trên `Club ID`, chọn **Value Filters → Greater Than…** → `Stadium Seats Value > 60000`, sắp xếp giảm dần theo `Stadium Seats Value`.

### 2.3. Sử dụng ngôn ngữ MDX trong SSMS (`query_11.mdx`)
- Measure `[Measures].[Official Match Count]` thuộc Measure Group `DIM Game` đếm mỗi trận đúng 1 lần theo khóa `Home_Club_ID`.
- Calculated Measure `[Measures].[Stadium Seats Value]` trích xuất sức chứa dạng số học qua `EXISTING EXCEPT(..., {[Unknown]})` mà không bao giờ trả về chuỗi `'All'`.

```mdx
SELECT
    {
        [Measures].[Stadium Seats Value],
        [Measures].[Official Match Count]
    } ON COLUMNS,
    ORDER(
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT(
                        [DIM Home Club].[Club ID].[Club ID].MEMBERS,
                        { [DIM Home Club].[Club ID].[Unknown] }
                    ),
                    EXCEPT(
                        [DIM Home Club].[Stadium Name].[Stadium Name].MEMBERS,
                        { [DIM Home Club].[Stadium Name].[Unknown] }
                    )
                ),
                [Measures].[Official Match Count]
            ),
            [Measures].[Stadium Seats Value] > 60000
        ),
        [Measures].[Stadium Seats Value],
        BDESC
    ) ON ROWS
FROM [DW Football Transfermarkt];
```

---

## 3. Bảng số liệu đối chiếu thực tế & Nhận xét

| STT | Club_ID | Club_Name | Stadium_Name | Stadium_Seats | Official_Match_Count |
| :---: | ---: | :--- | :--- | ---: | ---: |
| 1 | 418 | Real Madrid | Santiago Bernabéu | 83.186 | 50 |
| 2 | 16 | Borussia Dortmund | SIGNAL IDUNA PARK | 81.365 | 45 |
| 3 | 6646 | Fatih Karagümrük | Atatürk Olimpiyat | 77.563 | 37 |
| 4 | 5 | AC Milan | Giuseppe Meazza | 75.923 | 50 |
| 5 | 46 | Inter Milan | Giuseppe Meazza | 75.923 | 48 |
| 6 | 27 | Bayern Munich | Allianz Arena | 75.000 | 45 |
| 7 | 985 | Manchester United | Old Trafford | 74.879 | 47 |
| 8 | 44 | Hertha BSC | Olympiastadion Berlin | 74.667 | 17 |
| 9 | 150 | Real Betis Balompié | La Cartuja | 71.374 | 46 |
| 10 | 12 | Associazione Sportiva Roma | Olimpico di Roma | 70.634 | 52 |

> **Nhận xét đối chiếu:** Có đúng **23 CLB** có sân nhà `> 60.000` chỗ với tổng **993 trận sân nhà** (Real Madrid dẫn đầu sức chứa 83.186 chỗ; AS Roma nhiều trận sân nhà nhất: 52 trận). Dùng `DIM Home Club` đảm bảo tách đúng các CLB dùng chung sân như AC Milan/Inter Milan hay AS Roma/Lazio.

---

## 4. Đánh giá hiệu năng & Độ phức tạp thuật toán

* **Không gian sau lọc:** $272 \text{ CLB} \rightarrow M = 23$ CLB đạt ngưỡng `> 60.000` chỗ.
* **Độ phức tạp thời gian:** $O(N_{\text{clubs}} + M \log M)$ trên `DIM Game` Measure Group; bộ nhớ kết quả $O(23)$.
