# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 1. UPDATE QUERY 09
# ==========================================
with open('mdx/query_09.md', 'r', encoding='utf-8') as f:
    q09 = f.read()

# Fix T-SQL
old_tsql_9 = """USE DW_Football_Analytics;
GO

WITH WeekendTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekend_Goals,
        SUM(f.Yellow_Cards) AS Weekend_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_SK = c.Club_SK
    JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
    WHERE t.Is_Weekend = 1
    GROUP BY c.Club_Name
    ORDER BY Weekend_Goals DESC
),
WeekdayTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekday_Goals,
        SUM(f.Yellow_Cards) AS Weekday_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_SK = c.Club_SK
    JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
    WHERE t.Is_Weekend = 0
    GROUP BY c.Club_Name
    ORDER BY Weekday_Goals DESC
)
SELECT 
    w.Club_Name,
    w.Weekend_Goals,
    w.Weekend_Yellow_Cards,
    d.Weekday_Goals,
    d.Weekday_Yellow_Cards,
    (w.Weekend_Goals + d.Weekday_Goals) AS Total_Goals
FROM WeekendTop w
INNER JOIN WeekdayTop d ON w.Club_Name = d.Club_Name
ORDER BY Total_Goals DESC;"""

new_tsql_9 = """USE DW_Football_Transfermarkt;
GO

WITH WeekendTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekend_Goals,
        SUM(f.Yellow_Cards) AS Weekend_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 1
    GROUP BY c.Club_Name
    ORDER BY Weekend_Goals DESC, c.Club_Name DESC
),
WeekdayTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekday_Goals,
        SUM(f.Yellow_Cards) AS Weekday_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 0
    GROUP BY c.Club_Name
    ORDER BY Weekday_Goals DESC, c.Club_Name DESC
)
SELECT 
    w.Club_Name,
    w.Weekend_Goals,
    w.Weekend_Yellow_Cards,
    d.Weekday_Goals,
    d.Weekday_Yellow_Cards,
    (w.Weekend_Goals + d.Weekday_Goals) AS Total_Goals
FROM WeekendTop w
INNER JOIN WeekdayTop d ON w.Club_Name = d.Club_Name
ORDER BY Total_Goals DESC;"""

q09 = q09.replace(old_tsql_9, new_tsql_9)

# Fix lines in Section 2.3 MDX explanation
old_exp_9 = """   * **Tham số thực tế trong truy vấn:**
     * `Set_1`: Tập hợp Top 30 CLB ghi bàn nhiều nhất trên Sân Nhà (kết quả từ hàm `TOPCOUNT` thứ nhất).
     * `Set_2`: Tập hợp Top 30 CLB ghi bàn nhiều nhất trên Sân Khách (kết quả từ hàm `TOPCOUNT` thứ hai)."""

new_exp_9 = """   * **Tham số thực tế trong truy vấn:**
     * `Set_1`: Tập hợp Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (`Is_Weekend = 1`, kết quả từ hàm `TOPCOUNT` thứ nhất).
     * `Set_2`: Tập hợp Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (`Is_Weekend = 0`, kết quả từ hàm `TOPCOUNT` thứ hai)."""

q09 = q09.replace(old_exp_9, new_exp_9)

# Fix Section 2.4 commentary
old_comm_9 = """| Tiêu chí so sánh | 2.1. Visual Studio SSDT (Cube Browser) | 2.2. Excel PivotTable | 2.3. SSMS MDX Query |
| :--- | :--- | :--- | :--- |
| **Giao diện thao tác** | Kéo thả trực quan, hỗ trợ Expression Builder cho INTERSECT. | Kéo thả PivotTable thân thiện với chuyên viên phân tích. | Soạn thảo lệnh truy vấn kịch bản mã nguồn mở. |
| **Tính đồng nhất** | Trả về đúng ma trận CLB $\\times$ Cuối tuần / Ngày thường. | Trả về đúng ma trận CLB $\\times$ Cuối tuần / Ngày thường. | Trả về đúng ma trận CLB $\\times$ Cuối tuần / Ngày thường. |
| **Độ phức tạp** | Trung bình (cần dán biểu thức INTERSECT vào Filter). | Đơn giản (kéo trường `Is Weekend` vào Columns). | Chuyên sâu (làm chủ cấu trúc SET và đại số tập hợp). |"""

new_comm_9 = """1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 phương thức tiếp cận (Cube Browser trong SSDT, PivotTable trong Excel, và truy vấn MDX trong SSMS) đều phân tích chính xác tập hợp 9 CLB ưu tú xuất hiện đồng thời trong cả hai nhóm Top 30 bàn thắng Cuối tuần và Ngày thường.
   * **Manchester City** thể hiện sự hủy diệt đồng đều ở mọi đấu trường với tổng cộng 245 bàn thắng (94 bàn cuối tuần, 151 bàn ngày thường; tổng cộng 129 thẻ vàng). Đứng tiếp theo là **FC Bayern Munich** (225 bàn: 115 cuối tuần, 110 ngày thường), **PSV Eindhoven** (219 bàn: 82 cuối tuần, 137 ngày thường), và **Real Madrid** (210 bàn: 76 cuối tuần, 134 ngày thường).
   * Về chỉ số kỷ luật, **Real Madrid** và **Bayer 04 Leverkusen** nhận nhiều thẻ vàng nhất giữa tuần (128 và 120 thẻ vàng), phản ánh tính chất căng thẳng khốc liệt của các lượt trận cúp châu lục (UEFA Champions League, Europa League).

2. **So sánh 3 phương thức thực hiện:**

| Tiêu chí so sánh | 2.1. Visual Studio SSDT (Cube Browser) | 2.2. Excel PivotTable | 2.3. SSMS MDX Query |
| :--- | :--- | :--- | :--- |
| **Giao diện thao tác** | Kéo thả trực quan, hỗ trợ Expression Builder cho INTERSECT. | Kéo thả PivotTable thân thiện với chuyên viên phân tích. | Soạn thảo lệnh truy vấn kịch bản mã nguồn mở. |
| **Tính đồng nhất** | Trả về đúng 9 CLB $\\times$ Cuối tuần / Ngày thường chuẩn xác. | Trả về đúng 9 CLB $\\times$ Cuối tuần / Ngày thường chuẩn xác. | Trả về đúng 9 CLB $\\times$ Cuối tuần / Ngày thường chuẩn xác. |
| **Độ phức tạp** | Trung bình (cần dán biểu thức INTERSECT vào Filter). | Đơn giản (kéo trường `Is Weekend` vào Columns). | Chuyên sâu (làm chủ cấu trúc SET và đại số tập hợp). |"""

q09 = q09.replace(old_comm_9, new_comm_9)

# Fix Section 3 Expected Output table
old_tbl_9 = """| Tên Câu Lạc Bộ (`Club Name`) | Cuối tuần - Bàn thắng | Cuối tuần - Thẻ vàng | Ngày thường - Bàn thắng | Ngày thường - Thẻ vàng |
| :--- | :---: | :---: | :---: | :---: |
| **FC Bayern Munich** | 150 | 83 | 75 | 46 |
| **Manchester City** | 139 | 76 | 106 | 53 |
| **Arsenal FC** | 134 | 93 | 65 | 52 |
| **Bayer 04 Leverkusen** | 131 | 122 | 60 | 72 |
| **Borussia Dortmund** | 128 | 101 | 49 | 64 |
| **Paris Saint-Germain** | 128 | 93 | 70 | 59 |
| **Real Madrid** | 128 | 108 | 82 | 67 |
| **FC Barcelona** | 118 | 147 | 61 | 65 |
| **SL Benfica** | 115 | 81 | 77 | 89 |
| **Fenerbahce** | 113 | 111 | 75 | 76 |"""

new_tbl_9 = """Sau khi thực thi bất kỳ phương pháp nào trong 3 cách trên, tập kết quả trả về hiển thị chuẩn xác ma trận 9 CLB ưu tú (Elite Clubs) vượt qua bộ lọc giao tập hợp `INTERSECT`:

| Tên Câu Lạc Bộ (`Club Name`) | Cuối tuần - Bàn thắng | Cuối tuần - Thẻ vàng | Ngày thường - Bàn thắng | Ngày thường - Thẻ vàng |
| :--- | :---: | :---: | :---: | :---: |
| **Manchester City** | 94 | 49 | 151 | 80 |
| **Bayern Munich** | 115 | 62 | 110 | 67 |
| **PSV Eindhoven** | 82 | 24 | 137 | 76 |
| **Real Madrid** | 76 | 47 | 134 | 128 |
| **Arsenal FC** | 75 | 42 | 124 | 103 |
| **Paris Saint-Germain** | 59 | 40 | 139 | 112 |
| **Bayer 04 Leverkusen** | 65 | 74 | 126 | 120 |
| **Celtic FC** | 75 | 43 | 111 | 62 |
| **Inter Milan** | 70 | 49 | 114 | 103 |

> *Ghi chú:* 
> * Số lượng 9 câu lạc bộ được xác định chuẩn xác thông qua phép toán `INTERSECT` giữa 2 tập hợp Top 30 CLB ghi bàn cuối tuần và Top 30 CLB ghi bàn ngày thường trong khối đa chiều SSAS.
> * Các CLB chỉ mạnh ở giải quốc nội cuối tuần mà thi đấu ít bàn ở cúp giữa tuần (hoặc ngược lại) đã được loại bỏ một cách thuyết phục."""

q09 = q09.replace(old_tbl_9, new_tbl_9)

with open('mdx/query_09.md', 'w', encoding='utf-8') as f:
    f.write(q09)

print("Updated query_09.md successfully!")

# ==========================================
# 2. UPDATE QUERY 10
# ==========================================
with open('mdx/query_10.md', 'r', encoding='utf-8') as f:
    q10 = f.read()

# Fix T-SQL
old_tsql_10 = """USE DW_Football_Analytics;
GO

WITH QuarterStats AS (
    SELECT 
        op.Club_Name AS Opponent_Club,
        t.Quarter,
        SUM(f.Goals) AS Total_Goals
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_SK = c.Club_SK
    JOIN dbo.DIM_Club op ON f.Opponent_Club_SK = op.Club_SK
    JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
    WHERE c.Club_Name = 'Real Madrid' AND t.Year = 2023
    GROUP BY op.Club_Name, t.Quarter
)
SELECT 
    Opponent_Club,
    Quarter,
    Total_Goals,
    LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter) AS Prev_Quarter_Goals,
    ROUND(
        (CAST(Total_Goals AS FLOAT) - LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter)) 
        / NULLIF(LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter), 0) * 100, 
        2
    ) AS QoQ_Goals_Growth_Pct
FROM QuarterStats
ORDER BY Opponent_Club, Quarter;"""

new_tsql_10 = """USE DW_Football_Transfermarkt;
GO

WITH QuarterStats AS (
    SELECT 
        op.Club_Name AS Opponent_Club,
        t.Quarter,
        SUM(f.Goals) AS Total_Goals
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Club op ON f.Opponent_Club_ID = op.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE c.Club_Name = 'Real Madrid' AND t.Year = 2023
    GROUP BY op.Club_Name, t.Quarter
)
SELECT 
    Opponent_Club,
    Quarter,
    Total_Goals,
    LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter) AS Prev_Quarter_Goals,
    ROUND(
        (CAST(Total_Goals AS FLOAT) - LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter)) 
        / NULLIF(LAG(Total_Goals, 1) OVER (PARTITION BY Opponent_Club ORDER BY Quarter), 0) * 100, 
        2
    ) AS QoQ_Goals_Growth_Pct
FROM QuarterStats
ORDER BY Opponent_Club, Quarter;"""

q10 = q10.replace(old_tsql_10, new_tsql_10)

# Fix Section 2.1 Calculated Measure Expressions
old_calc_10 = """   * **Thước đo 1 (`Prev Quarter Goals`):**
      * Name: `Prev Quarter Goals` | Parent hierarchy: `Measures`
      * Expression: `([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER)`
   * **Thước đo 2 (`QoQ Goals Growth`):**
      * Name: `QoQ Goals Growth` | Parent hierarchy: `Measures`
      * Expression:
        ```mdx
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND((([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100, 2)
        )
        ```
      * Format String: `0.00%`"""

new_calc_10 = """   * **Thước đo 1 (`Prev Quarter Goals`):**
      * Name: `Prev Quarter Goals` | Parent hierarchy: `Measures`
      * Expression:
        ```mdx
        IIF(
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT,
            ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER),
            NULL
        )
        ```
      * Format String: `#,##0`
   * **Thước đo 2 (`QoQ Goals Growth`):**
      * Name: `QoQ Goals Growth` | Parent hierarchy: `Measures`
      * Expression:
        ```mdx
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                ([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals],
                4
            )
        )
        ```
      * Format String: `0.00%`"""

q10 = q10.replace(old_calc_10, new_calc_10)

# Fix Section 2.3 MDX Script
old_mdx_10 = """WITH 
    -- 1. Bàn thắng của Quý liền trước (Quarter-over-Quarter Prior)
    MEMBER [Measures].[Prev Quarter Goals] AS
        (
            [Measures].[Goals],
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER
        ),
        FORMAT_STRING = "#,##0"

    -- 2. Tỷ lệ tăng trưởng so với Quý liền trước (QoQ Goals Growth %)
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                (([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100,
                2
            )
        ),
        FORMAT_STRING = "0.00%"

SELECT"""

new_mdx_10 = """WITH 
    -- 1. Bàn thắng của Quý liền trước (chỉ xét trong cùng năm phân cấp 2023)
    MEMBER [Measures].[Prev Quarter Goals] AS
        IIF(
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT,
            (
                [Measures].[Goals],
                [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER
            ),
            NULL
        ),
        FORMAT_STRING = "#,##0"

    -- 2. Tỷ lệ tăng trưởng so với Quý liền trước (QoQ Goals Growth %)
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                ([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals],
                4
            )
        ),
        FORMAT_STRING = "0.00%"

SELECT"""

q10 = q10.replace(old_mdx_10, new_mdx_10)

# Fix Section 2.3 Explanation
old_fe_exp_10 = """* **`[DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER`**: Trả về thành viên thời gian liền kề trước đó trong cùng cấp bậc phân cấp. Ví dụ: khi đang ở `Quarter 2`, hàm sẽ tự động lấy giá trị của `Quarter 1`."""
new_fe_exp_10 = """* **`[DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER`**: Trả về thành viên thời gian liền kề trước đó trong cùng cấp bậc phân cấp. Kết hợp điều kiện so sánh `.PARENT` giúp giới hạn tính toán chặt chẽ trong phạm vi năm phân tích 2023, đảm bảo Quý 1 đầu năm trả về `NULL` hoàn toàn tương thích với T-SQL và Excel PivotTable."""
q10 = q10.replace(old_fe_exp_10, new_fe_exp_10)

old_fe_iif_10 = """3. **Hàm điều kiện `IIF` tính tỷ lệ tăng trưởng Quý-trên-Quý (QoQ Growth %)**:
   * **Cơ chế:** Áp dụng công thức $\\frac{Goals_{Current} - Goals_{Prev}}{Goals_{Prev}} \\times 100\\%$. Hàm `IIF` kiểm tra nếu `Prev Quarter Goals` bị rỗng (tại Q1) hoặc bằng 0 thì gán `NULL`, triệt tiêu hoàn toàn lỗi chia cho 0."""
new_fe_iif_10 = """3. **Hàm điều kiện `IIF` tính tỷ lệ tăng trưởng Quý-trên-Quý (QoQ Growth %)**:
   * **Cơ chế:** Áp dụng công thức $\\frac{Goals_{Current} - Goals_{Prev}}{Goals_{Prev}}$. Thước đo được làm tròn 4 chữ số thập phân (`ROUND(..., 4)`) kết hợp định dạng chuẩn `FORMAT_STRING = "0.00%"` (SSAS tự động hiển thị dạng phần trăm mà không cần nhân 100 trong biểu thức, loại bỏ hoàn toàn lỗi hiển thị gấp 100 lần trên Excel). Hàm `IIF` kiểm tra nếu `Prev Quarter Goals` rỗng (như tại Q1) hoặc bằng 0 thì trả về `NULL` an toàn."""
q10 = q10.replace(old_fe_iif_10, new_fe_iif_10)

# Fix Section 2.4 narrative
old_nar_10 = """1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối: FC Barcelona là đối thủ bị Real Madrid chọc thủng lưới nhiều nhất (4 bàn ở Q1, 4 bàn ở Q2, 2 bàn ở Q3, 5 bàn ở Q4 - tăng trưởng QoQ Q4 bùng nổ $+150.00\\%$). Các đối thủ lớn tiếp theo là Atletico Madrid và Girona FC cũng cho thấy sự tăng vọt bàn thua vào giai đoạn nước rút cuối năm (Q4).
   * Điều này chứng minh hàm `PREVMEMBER` kết hợp cây phân cấp thời gian `Hierarchy Time` trong SSAS đã xử lý chuẩn xác logic điều hướng chuỗi thời gian (Time-series Navigation)."""

new_nar_10 = """1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và đồng bộ tuyệt đối:
     * **UD Almería** và **Valencia CF** là hai đối thủ bị Real Madrid chọc thủng lưới nhiều nhất trong năm 2023 với cùng **7 bàn thắng**. Trong đó, Real Madrid ghi 4 bàn vào lưới Almería ở Q2 và 3 bàn ở Q3 (tăng trưởng QoQ Q3: $-25.00\\%$). Với Valencia CF, Real Madrid ghi 2 bàn ở Q1 và bùng nổ 5 bàn ở Q4.
     * **Real Valladolid CF** nhận tới **6 bàn thua** chỉ trong Quý 2 (trận thắng giòn giã 6-0 của Real Madrid).
     * **CA Osasuna** và **Villarreal CF** cùng nhận **6 bàn thua**, trong đó Real Madrid ghi 4 bàn vào lưới cả hai đội bóng này trong Quý 4.
     * **Athletic Bilbao** (5 bàn) và **Girona FC** (5 bàn) chịu sức ép liên tục qua các Quý 2 và Quý 3 (Girona FC bị ghi 2 bàn ở Q2 và 3 bàn ở Q3, tăng trưởng $+50.00\\%$).
     * **FC Barcelona** chạm trán Real Madrid tại giải VĐQG La Liga 2023 với 0 bàn ở Q1 (thua 1-2) và 2 bàn ở Q4 (thắng 2-1 nhờ cú đúp của Jude Bellingham).
   * Điều này chứng minh hàm `PREVMEMBER` kết hợp kiểm tra cùng năm phân cấp trong SSAS đã giải quyết trọn vẹn bài toán chuỗi thời gian theo quý (QoQ Time-series Analysis)."""

q10 = q10.replace(old_nar_10, new_nar_10)

# Fix Section 3 table and footnote
old_tbl_10 = """| Câu Lạc Bộ Đối Thủ (`Opponent Club`) | Q1 Bàn Thắng | Q1 QoQ % | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **UD Almería** | - | - | 4 | - | 3 | -25.00% | - | -100.00% |
| **CA Osasuna** | 2 | +100.00% | - | -100.00% | - | - | 4 | - |
| **Cádiz CF** | - | -100.00% | 2 | - | - | -100.00% | 3 | - |
| **Girona FC** | - | -100.00% | 2 | - | 3 | +50.00% | - | -100.00% |
| **Villarreal CF** | 1 | - | 1 | 0.00% | - | -100.00% | 4 | - |
| **Celta de Vigo** | - | - | 2 | - | 1 | -50.00% | - | -100.00% |
| **Valencia CF** | 2 | - | 0 | -100.00% | - | - | 5 | - |
| **Real Valladolid CF** | - | -100.00% | 6 | - | - | -100.00% | - | - |
| **Athletic Bilbao** | 2 | - | 1 | -50.00% | 2 | +100.00% | - | -100.00% |
| **FC Barcelona** | 0 | -100.00% | - | - | - | - | 2 | - |

> *Ghi chú:* Giá trị `Q1 QoQ %` hiển thị dấu `-` (hoặc `NULL`) do Quý 1 là kỳ đầu năm, hàm `PREVMEMBER` không tìm thấy quý liền trước trong ngữ cảnh năm 2023, hàm `IIF` xử lý an toàn ngăn chặn lỗi chia cho 0."""

new_tbl_10 = """| Câu Lạc Bộ Đối Thủ (`Opponent Club`) | Q1 Bàn Thắng | Q1 QoQ % | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **UD Almería** | - | - | 4 | - | 3 | -25.00% | - | -100.00% |
| **CA Osasuna** | 2 | - | - | -100.00% | - | - | 4 | - |
| **Cádiz CF** | - | - | 2 | - | - | -100.00% | 3 | - |
| **Girona FC** | - | - | 2 | - | 3 | +50.00% | - | -100.00% |
| **Villarreal CF** | 1 | - | 1 | 0.00% | - | -100.00% | 4 | - |
| **Celta de Vigo** | - | - | 2 | - | 1 | -50.00% | - | -100.00% |
| **Valencia CF** | 2 | - | 0 | -100.00% | - | - | 5 | - |
| **Real Valladolid CF** | - | - | 6 | - | - | -100.00% | - | - |
| **Athletic Bilbao** | 2 | - | 1 | -50.00% | 2 | +100.00% | - | -100.00% |
| **FC Barcelona** | 0 | - | - | - | - | - | 2 | - |

> *Ghi chú:* 
> * Giá trị `Q1 QoQ %` hiển thị dấu `-` (hoặc `NULL`) cho toàn bộ các đối thủ vì Quý 1 là kỳ đầu năm, hàm `PREVMEMBER` khi giới hạn trong cùng năm 2023 không có quý liền trước để đối chiếu. Điều này hoàn toàn khớp với hàm `LAG` trong T-SQL và tính năng `% Difference From` trong Excel PivotTable.
> * Các ô có dấu `-` ở cột Bàn thắng biểu thị trong Quý đó Real Madrid không chạm trán đối thủ này tại giải đấu (hoặc không ghi bàn).
> * Khi Quý liền trước có số bàn thắng bằng 0 hoặc rỗng (chưa đối đầu), tỷ lệ tăng trưởng QoQ hiển thị dấu `-` nhằm tránh lỗi toán học chia cho 0."""

q10 = q10.replace(old_tbl_10, new_tbl_10)

with open('mdx/query_10.md', 'w', encoding='utf-8') as f:
    f.write(q10)

print("Updated query_10.md successfully!")
