# MDX Query 03: Tổng phút thi đấu & đóng góp bàn thắng cho cầu thủ > 20 G+A mùa 2023/2024

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Đo lường khối lượng thời gian thi đấu (`Minutes_Played`) và hiệu quả tạo dấu ấn lên bàn thắng (`Goal_Contributions = Goals + Assists`) đối với những cầu thủ xuất sắc có trên 20 đóng góp bàn thắng trong mùa giải 2023/2024.
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Thời gian (`DIM_Time`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[DIM Time].[Season]`
  * Cube Measures: `[Measures].[Minutes Played]`, `[Measures].[Goal Contributions]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    p.Player_Name,
    t.Season,
    SUM(f.Minutes_Played) AS Total_Minutes_Played,
    SUM(f.Goal_Contributions) AS Total_Goal_Contributions
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Season = '2023/2024' OR t.Year = 2023
GROUP BY p.Player_Name, t.Season
HAVING SUM(f.Goal_Contributions) > 20
ORDER BY Total_Goal_Contributions DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Hiển thị đồng thời hai thước đo: `[Measures].[Minutes Played]` và `[Measures].[Goal Contributions]`.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Lấy danh sách thành viên `[DIM Player].[Player Name].[Player Name].MEMBERS`.
   * Sử dụng hàm `FILTER()` để giữ lại các cầu thủ thỏa mãn điều kiện `[Measures].[Goal Contributions] > 20` (tương đương mệnh đề `HAVING` trong SQL).
   * Dùng hàm `ORDER(..., BDESC)` để sắp xếp tập hợp theo thứ tự giảm dần tuyệt đối của số đóng góp bàn thắng.
3. **Xác định Lát cắt (Slicer Axis / WHERE Clause):**
   * Lọc tại mùa giải: `[DIM Time].[Season].[2023/2024]`.
4. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, kết nối Cube `DW Football Transfermarkt`.
   * Tạo cửa sổ MDX Query, dán đoạn script bên dưới và thực thi.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 03: Cầu thủ có trên 20 đóng góp bàn thắng (G+A) mùa giải 2023/2024
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Tổng số phút thi đấu và tổng đóng góp bàn thắng (G+A)
    {
        [Measures].[Minutes Played],
        [Measures].[Goal Contributions]
    } ON COLUMNS,

    -- Trục Dòng: Các cầu thủ có G+A > 20, sắp xếp giảm dần
    ORDER(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                (
                    [Measures].[Goal Contributions],
                    [DIM Time].[Season].[2023/2024]
                )
            ),
            [Measures].[Goal Contributions] > 20
        ),
        [Measures].[Goal Contributions],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Mùa giải 2023/2024
WHERE (
    [DIM Time].[Season].[2023/2024]
);
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`FILTER`** | `FILTER(Set_Expression, Logical_Expression)` | Đánh giá từng cầu thủ và lọc ra những người có `[Measures].[Goal Contributions] > 20`. Đóng vai trò như mệnh đề `HAVING` trong SQL. |
| **`ORDER`** | `ORDER(Set, Numeric_Expression, [ASC \| DESC \| BASC \| BDESC])` | Sắp xếp tập hợp cầu thủ theo thước đo. Sử dụng cờ `BDESC` (Break Hierarchy Descending) để sắp xếp toàn cục không phụ thuộc phân cấp chiều. |
| **`NONEMPTY`** | `NONEMPTY(Set1, Set2)` | Tiền lọc để loại bỏ các cầu thủ không có dữ liệu trong mùa 2023/2024 trước khi đưa vào hàm `FILTER`, giúp tăng tốc độ xử lý gấp nhiều lần. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Số lượng Cell được đánh giá:** Chỉ có các cầu thủ đã thi đấu trong mùa 2023/2024 ($\approx 4.000$ cầu thủ) được giữ lại qua bước `NONEMPTY`.
* **Kích thước tập kết quả (Result Set):** Nhóm cầu thủ đẳng cấp cao đạt $>20$ G+A trong một mùa giải thường chỉ dao động từ 30 đến 70 cầu thủ trên toàn Châu Âu. Do đó, kích thước kết quả là ma trận nhỏ ($\approx 50 \times 2$), bộ nhớ RAM tiêu thụ $< 10\text{ KB}$.

### Độ phức tạp thời gian (Time Complexity)
* **Chi phí lọc điều kiện (`FILTER`):** Phép duyệt qua $M$ cầu thủ sau `NONEMPTY` tốn $O(M)$ thời gian.
* **Chi phí sắp xếp (`ORDER BDESC`):** Thuật toán QuickSort nội tại của Analysis Services chạy trên tập con $K \le 100$ phần tử có độ phức tạp $O(K \log K)$, hoàn thành gần như tức thì ($< 1\text{ ms}$).
* **Kỹ thuật tối ưu:** Bằng cách bọc `NONEMPTY` bên trong `FILTER`, ta tránh được việc SSAS phải duyệt qua $30.000$ cầu thủ trong toàn bộ lịch sử cơ sở dữ liệu.
