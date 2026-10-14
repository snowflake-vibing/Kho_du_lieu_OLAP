# MDX Query 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Thống kê số lượng trận đấu (`COUNT(DISTINCT Game_ID)`) đã được tổ chức tại các sân vận động quy mô lớn ("Thánh địa" bóng đá có sức chứa `Stadium_Seats > 60.000` khán giả như Camp Nou, Santiago Bernabéu, Old Trafford, San Siro...).
* **Đối tượng phân tích:** Sân vận động và Câu lạc bộ (`DIM_Club`), Trận đấu (`DIM_Game`), Lượt thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Club].[Club Name]`, `[DIM Club].[Stadium Name]`, `[DIM Club].[Stadium Seats]`, `[DIM Game].[Game ID]`
  * Calculated Measure: `[Measures].[Total Matches Played]` (Đếm phân biệt số trận đấu)

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    cb.Club_Name,
    cb.Stadium_Name,
    cb.Stadium_Seats,
    COUNT(DISTINCT f.Game_ID) AS Total_Matches_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
WHERE cb.Stadium_Seats > 60000
GROUP BY cb.Club_Name, cb.Stadium_Name, cb.Stadium_Seats
ORDER BY cb.Stadium_Seats DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Định nghĩa Thành viên Tính toán (Calculated Measure):**
   * Trong một trận đấu, có khoảng 22 - 30 cầu thủ ra sân (tương ứng 22 - 30 dòng fact). Vì vậy, phép đếm tổng số dòng sự kiện `[Measures].[FACT Player Match Perf Count]` không phản ánh số trận đấu.
   * Ta dùng hàm `DISTINCTCOUNT` để đếm số lượng trận đấu không trùng lặp:
     `DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`.
2. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt thước đo đếm số trận đấu: `{ [Measures].[Total Matches Played] }`.
3. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Kết hợp tổ hợp: Câu lạc bộ $\times$ Tên sân vận động.
   * Dùng hàm `FILTER()` để lọc điều kiện số chỗ ngồi: `[DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE > 60000`.
   * Dùng hàm `ORDER()` sắp xếp theo sức chứa sân vận động giảm dần.
4. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, mở cửa sổ MDX Query kết nối Cube `DW Football Transfermarkt`.
   * Thực thi mã script để trích xuất danh sách các sân vận động khổng lồ nhất Châu Âu.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 11: Số trận đấu tại các sân vận động có sức chứa trên 60.000 chỗ
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- Tính số lượng trận đấu duy nhất (Distinct Count Game_ID)
    MEMBER [Measures].[Total Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Số lượng trận đấu
    { [Measures].[Total Matches Played] } ON COLUMNS,

    -- Trục Dòng: Các CLB và Sân vận động có sức chứa > 60.000 chỗ, xếp giảm dần
    ORDER(
        FILTER(
            CrossJoin(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] })
            ),
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE > 60000
            AND [Measures].[Total Matches Played] > 0
        ),
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE,
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`DISTINCTCOUNT`** | `DISTINCTCOUNT(Set_Expression)` | Đếm số lượng phần tử duy nhất (Distinct Game ID) trong không gian trận đấu thực tế. |
| **`EXISTING`** | `EXISTING Set` | Giới hạn tập hợp `Game ID` chỉ bao gồm những trận đấu thuộc về câu lạc bộ và sân bãi đang xét tại dòng hiện hành. |
| **`FILTER`** | `FILTER(Set, Condition)` | Lọc các sân có sức chứa lớn hơn $60.000$ ghế và có ít nhất 1 trận đấu diễn ra. |
| **`MEMBERVALUE`** | `Member.MEMBERVALUE` | Trích xuất giá trị số học nguyên thủy của thuộc tính `Stadium Seats` để so sánh với ngưỡng $60.000$. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Số lượng sân vận động thỏa điều kiện:** Ở Châu Âu chỉ có khoảng 20 đến 30 sân vận động có sức chứa trên 60.000 chỗ (Wembley, Camp Nou, Bernabéu, Allianz Arena, San Siro, Signal Iduna Park...).
* **Kích thước ma trận kết quả:** $25 \text{ dòng} \times 1 \text{ cột} = 25 \text{ cells}$.
* **Bộ nhớ RAM tiêu thụ:** Dưới $2\text{ KB}$.

### Độ phức tạp thời gian (Time Complexity)
* **Độ phức tạp phép đếm `DISTINCTCOUNT`:** Trong SSAS, `DISTINCTCOUNT` đòi hỏi quét qua các khóa định danh trận đấu. Nhờ liên kết quan hệ trực tiếp `FACT_Player_Match_Perf` $\leftrightarrow$ `DIM_Game`, chi phí là $O(G)$ với $G$ là số trận của CLB đó ($\approx 50 - 100$ trận/mùa).
* **Thời gian lọc và sắp xếp:** $O(S \log S)$ với $S \le 30$, diễn ra trong $0.1\text{ ms}$.
* **Tổng thời gian phản hồi:** Khoảng $20 - 40\text{ ms}$.
