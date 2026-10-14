# MDX Query 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Xác định danh sách 10 chân sút ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh (Premier League - Mã giải đấu: `GB1`) trong mùa giải 2023/2024.
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Giải đấu (`DIM_Competition`), Thời gian (`DIM_Time`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[DIM Competition].[Competition ID]`, `[DIM Time].[Season]`
  * Cube Measures: `[Measures].[Goals]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT TOP 10
    p.Player_Name,
    c.Competition_ID,
    c.Competition_Name,
    t.Season,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE c.Competition_ID = 'GB1' 
  AND (t.Season = '2023/2024' OR t.Year = 2023 OR t.Year = 2024)
GROUP BY p.Player_Name, c.Competition_ID, c.Competition_Name, t.Season
ORDER BY Total_Goals DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

Để chuyển đổi từ tư duy quan hệ (Relational SQL) sang tư duy đa chiều (OLAP MDX), quy trình thiết kế gồm 4 bước:

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt thước đo `[Measures].[Goals]` lên trục cột để hiển thị tổng số bàn thắng ghi được.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Lấy danh sách thành viên cấp thuộc tính `[DIM Player].[Player Name].[Player Name].MEMBERS`.
   * Sử dụng hàm `NONEMPTY()` để loại bỏ trước các cầu thủ không ghi bàn nhằm thu nhỏ tập hợp.
   * Áp dụng hàm `TOPCOUNT()` để xếp hạng giảm dần theo `[Measures].[Goals]` và lấy đúng 10 cầu thủ đứng đầu.
3. **Xác định Lát cắt (Slicer Axis / WHERE Clause):**
   * Cắt dữ liệu (Slicing) tại giải Ngoại Hạng Anh: `[DIM Competition].[Competition ID].[GB1]`.
   * Cắt dữ liệu tại mùa giải 2023/2024: `[DIM Time].[Season].[2023/2024]`.
   * Tuple lát cắt: `([DIM Competition].[Competition ID].[GB1], [DIM Time].[Season].[2023/2024])`.
4. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SQL Server Management Studio (SSMS), kết nối tới **Analysis Services**.
   * Chọn database chứa Cube **`DW Football Transfermarkt`**.
   * Nhấn nút **New MDX Query**, dán mã truy vấn bên dưới và nhấn **Execute (F5)**.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 01: Top 10 cầu thủ ghi nhiều bàn nhất tại Ngoại Hạng Anh mùa 23/24
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Top 10 cầu thủ ghi nhiều bàn nhất sau khi loại bỏ dữ liệu rỗng
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player Name].[Player Name].MEMBERS,
            (
                [Measures].[Goals],
                [DIM Competition].[Competition ID].[GB1],
                [DIM Time].[Season].[2023/2024]
            )
        ),
        10,
        [Measures].[Goals]
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Ngoại Hạng Anh (GB1) và Mùa giải 2023/2024
WHERE (
    [DIM Competition].[Competition ID].[GB1],
    [DIM Time].[Season].[2023/2024]
);
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`TOPCOUNT`** | `TOPCOUNT(Set_Expression, Count, [Numeric_Expression])` | Sắp xếp tập hợp cầu thủ theo thứ tự giảm dần của `[Measures].[Goals]` và trích xuất đúng 10 phần tử dẫn đầu. Khắc phục nhược điểm phải dùng cả `ORDER` + `HEAD`. |
| **`NONEMPTY`** | `NONEMPTY(Set_Expression1 [, Set_Expression2])` | Lọc bỏ những cầu thủ không có dữ liệu sự kiện bàn thắng trong mùa giải và giải đấu đã chỉ định trước khi thực hiện sắp xếp Top 10. |
| **`MEMBERS`** | `Level_Or_Hierarchy.MEMBERS` | Trả về tập hợp tất cả các thành viên của thuộc tính tên cầu thủ (`Player Name`). |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Không gian gốc (Cell Space):** Nếu quét toàn bộ cầu thủ ($N \approx 30.000$) kết hợp với tất cả các mùa giải và giải đấu, không gian tìm kiếm sẽ rất lớn.
* **Bộ nhớ sử dụng thực tế:** Nhờ hàm `NONEMPTY` kết hợp tuple ngữ cảnh trong bộ nhớ SSAS, số lượng tuple nạp vào không gian làm việc giảm từ $\approx 30.000$ xuống còn khoảng $\approx 500$ cầu thủ từng thi đấu tại Ngoại Hạng Anh mùa 2023/2024.
* **Độ phức tạp lưu trữ kết quả:** $O(k)$ với $k = 10$ tuples trên trục ROWS và 1 measure trên trục COLUMNS.

### Độ phức tạp thời gian (Time Complexity)
* **Chi phí lọc và kết xuất:** $O(N)$ để duyệt qua các cầu thủ thi đấu tại mùa giải $2023/2024$.
* **Chi phí thuật toán TOPCOUNT:** Sử dụng cấu trúc Min-Heap kích thước $k=10$, chi phí là $O(N \log k)$ thay vì $O(N \log N)$ như việc dùng lệnh `ORDER(...)` toàn bộ bảng.
* **Tổng thời gian tính toán:** Cực nhanh (dưới 50ms) trên nền tảng SSAS MOLAP do đã có sẵn các cấu trúc chỉ mục Bitmap Index và Aggregations tính trước.

### Điểm tối ưu cần lưu ý
* Đặt điều kiện lọc trong `NONEMPTY(..., (Measure, Slicer_Tuples))` giúp SSAS kích hoạt chế độ **Block Computation**, bỏ qua hàng ngàn cell rỗng (empty cells) mà không cần duyệt tuần tự từng cell (cell-by-cell).
