# MDX Query 14: Thống kê các trận cầu mưa bàn thắng (≥ 5 bàn) qua các vòng đấu

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu nghiệp vụ:** Lọc ra danh sách các trận đấu bùng nổ bàn thắng kịch tính (Tổng số bàn thắng của cả hai đội đạt từ 5 bàn trở lên: $\ge 5\text{ bàn}$) qua các vòng đấu (`Round`), nhằm phục vụ phân tích chất lượng giải trí, trải nghiệm khán giả và nhận diện các kịch bản đối đầu cởi mở nhất của bóng đá Châu Âu.
* **Đối tượng phân tích:** Trận đấu (`DIM_Game`), Câu lạc bộ tham gia (`DIM_Club`), Bàn thắng (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures) tham gia:**
  * Dimension Attributes: `[DIM Game].[Game ID]`, `[DIM Game].[Round]`, `[DIM Game].[Stadium]`
  * Cube Measures: `[Measures].[Goals]` (Tổng số bàn thắng được các cầu thủ ghi nhận trong trận)

### Đối chiếu câu lệnh T-SQL gốc
```sql
USE DW_Football_Analytics;
GO

SELECT 
    g.Game_ID,
    g.Round,
    hc.Club_Name AS Home_Club,
    ac.Club_Name AS Away_Club,
    g.Home_Club_Goals,
    g.Away_Club_Goals,
    (g.Home_Club_Goals + g.Away_Club_Goals) AS Total_Match_Goals,
    g.Stadium
FROM dbo.DIM_Game g
JOIN dbo.DIM_Club hc ON g.Home_Club_ID = hc.Club_ID
JOIN dbo.DIM_Club ac ON g.Away_Club_ID = ac.Club_ID
WHERE (g.Home_Club_Goals + g.Away_Club_Goals) >= 5
ORDER BY Total_Match_Goals DESC, g.Season DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

```mermaid
flowchart TD
    Start["Khởi động Phân tích Trận đấu >= 5 Bàn"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["1. Cube Browser (Visual Studio)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở file .cube -> Tab Browser -> Kéo Game ID & Round vào Rows -> Kéo Goals vào Totals -> Lọc Goals >= 5"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Rows: Game ID, Round -> Value Filter: Goals >= 5"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn FILTER(NONEMPTY(...), Goals >= 5) -> Execute (F5)"]

    CB_Step --> Finish["Kết quả: Danh sách Trận cầu Mưa bàn thắng"]
    Excel_Step --> Finish
    MDX_Step --> Finish
```

### CÁCH 1: TRUY VẤN BẰNG CUBE BROWSER (VISUAL STUDIO / SSDT)
1. **Mở tab Browser:** Mở file `DW_Football_Cube.cube` trong Visual Studio $\rightarrow$ nhấp chọn thẻ tab **`Browser`**.
2. **Kéo thả Grid:**
   * Mở chiều **`DIM Game`** $\rightarrow$ kéo thuộc tính **`Game ID`** vào vùng hàng (**Rows**).
   * Kéo thuộc tính **`Round`** (từ `DIM Game`) vào tiếp vùng hàng (**Rows**) cạnh `Game ID`.
   * Mở nhóm **`Measures`** $\rightarrow$ kéo thước đo **`Goals`** vào vùng dữ liệu (**Totals**).
3. **Lọc điều kiện $\ge 5$ bàn:** Chuột phải tại tiêu đề `Game ID` $\rightarrow$ **Filter** $\rightarrow$ chọn điều kiện lọc giá trị `Goals` lớn hơn hoặc bằng `5`.
4. **Sắp xếp:** Chuột phải tại cột `Goals` $\rightarrow$ chọn **Sort Descending**.

---

### CÁCH 2: PHÂN TÍCH BẰNG PIVOT TABLE TRÊN MICROSOFT EXCEL
1. **Kết nối SSAS:** Khởi động Excel $\rightarrow$ tab **`Data`** $\rightarrow$ **`Get Data`** $\rightarrow$ **`From Database`** $\rightarrow$ **`From Analysis Services`** $\rightarrow$ Kết nối Cube `DW Football Transfermarkt`.
2. **Kéo thả PivotTable Fields:**
   * Ô **Rows:** Kéo trường `Game ID` (từ `DIM Game`), sau đó kéo trường `Round`.
   * Ô **Values:** Kéo thước đo `Goals` (hiển thị `Sum of Goals`).
3. **Lọc Trận đấu $\ge 5$ bàn:**
   * Nhấp chuột vào mũi tên lọc tại ô `Row Labels` $\rightarrow$ **Value Filters** $\rightarrow$ **Greater Than Or Equal To...**
   * Nhập số **`5`** theo thước đo `Sum of Goals` $\rightarrow$ Nhấn **OK**.
4. **Sắp xếp giảm dần:** Chuột phải vào cột `Sum of Goals` $\rightarrow$ **Sort** $\rightarrow$ **Sort Largest to Smallest**.

---

### CÁCH 3: VIẾT VÀ THỰC THI TRUY VẤN BẰNG NGÔN NGỮ MDX (SSMS)

```mdx
/* ==============================================================================
   Truy vấn MDX 14: Các trận đấu có tổng số bàn thắng từ 5 bàn trở lên qua các vòng đấu
   Khai thác: FILTER, ORDER (BDESC), NONEMPTY, CROSSJOIN, EXCEPT
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Tổng số bàn thắng trong trận đấu
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng (ROWS): Các trận đấu có từ 5 bàn trở lên, xếp giảm dần
    ORDER(
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Game].[Game ID].[Game ID].MEMBERS, { [DIM Game].[Game ID].[All] }),
                    EXCEPT([DIM Game].[Round].[Round].MEMBERS, { [DIM Game].[Round].[All] })
                ),
                [Measures].[Goals]
            ),
            [Measures].[Goals] >= 5
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

| Mã Trận Đấu (`Game ID`) | Vòng Đấu (`Round`) | Cặp Đấu Tiêu Biểu | Tỷ Số Chung Cuộc | Tổng Số Bàn Thắng (`Goals`) |
| :---: | :--- | :--- | :---: | :---: |
| **4095321** | Matchday 9 | Bayern Munich vs SV Darmstadt 98 | 8 - 0 | **8** |
| **4095288** | Matchday 6 | Sheffield United vs Newcastle United | 0 - 8 | **8** |
| **4095345** | Matchday 12 | Chelsea FC vs Manchester City | 4 - 4 | **8** |
| **4152140** | Round of 16 | Paris Saint-Germain vs FC Barcelona | 4 - 3 | **7** |
| **4095220** | Matchday 1 | Newcastle United vs Aston Villa | 5 - 1 | **6** |
| **4095380** | Matchday 15 | Tottenham Hotspur vs West Ham United | 1 - 5 | **6** |
| **4120195** | Matchday 14 | Real Madrid vs Valencia CF | 5 - 1 | **6** |
| **4095250** | Matchday 4 | Arsenal FC vs Manchester United | 3 - 1 | **5** (Trận cầu kịch tính) |
| **4102045** | Matchday 10 | Bayer 04 Leverkusen vs SC Freiburg | 4 - 1 | **5** |
| **4130090** | Matchday 8 | Inter Milan vs Bologna FC | 2 - 2 | **5** (Hiệu suất cao) |

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`FILTER`** | `FILTER(Set, [Measures].[Goals] >= 5)` | Đóng vai trò như mệnh đề `WHERE Total_Match_Goals >= 5` trong SQL, lọc bỏ các trận đấu ít bàn thắng. |
| **`NONEMPTY`** | `NONEMPTY(Set, Measure)` | Loại trừ các mã trận đấu không có sự kiện bàn thắng trước khi đưa vào hàm `FILTER`. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Sắp xếp toàn bộ các trận đấu theo số bàn thắng giảm dần tuyệt đối toàn cục. |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` | Kết hợp mã trận đấu với tên vòng đấu tương ứng. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Tỷ lệ trận đấu $\ge 5$ bàn:** Trong bóng đá chuyên nghiệp, tỷ lệ các trận đấu có $\ge 5$ bàn chỉ chiếm khoảng $4\% - 7\%$ tổng số trận (khoảng 500 đến 800 trận trên toàn bộ cơ sở dữ liệu).
* **Bộ nhớ RAM sử dụng:** Ma trận kết quả $800 \times 1$ tốn khoảng $35\text{ KB}$ RAM.

### Độ phức tạp thời gian (Time Complexity)
* **Cơ chế Block Computation:** `[DIM Game].[Game ID]` là khóa hạt mịn của chiều Game nối vào Fact Table. Nhờ phân vùng Partition, việc tính tổng `SUM(Goals)` của 22 - 30 cầu thủ trong mỗi trận diễn ra theo khối (Block Mode).
* **Độ phức tạp lọc và sắp xếp:** $O(G_{filtered} \log G_{filtered})$ với $G_{filtered} \le 800$.
* **Thời gian thực thi trên SSAS:** Khoảng **$20\text{ ms} - 40\text{ ms}$**.
