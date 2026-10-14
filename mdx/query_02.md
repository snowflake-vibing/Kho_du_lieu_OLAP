# MDX Query 02: Top 10 Vua kiến tạo khu vực Tiền vệ ở các giải VĐQG

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Thống kê danh sách 10 cầu thủ thi đấu ở vị trí tiền vệ (`Main_Position = 'Midfield'`) có tổng số pha kiến tạo thành bàn (`Assists`) cao nhất tại tất cả các giải Vô địch Quốc gia (`Competition_Type = 'domestic_league'`).
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Giải đấu (`DIM_Competition`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[DIM Player].[Main Position]`, `[DIM Competition].[Competition Type]`
  * Cube Measures: `[Measures].[Assists]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT TOP 10
    p.Player_Name,
    p.Main_Position,
    c.Competition_Type,
    SUM(f.Assists) AS Total_Assists
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
WHERE p.Main_Position LIKE '%Midfield%'
  AND c.Competition_Type = 'domestic_league'
GROUP BY p.Player_Name, p.Main_Position, c.Competition_Type
ORDER BY Total_Assists DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt thước đo `[Measures].[Assists]` để đếm tổng số đường chuyền thành bàn.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Kết hợp thuộc tính tên cầu thủ `[DIM Player].[Player Name]` và vị trí `[DIM Player].[Main Position].[Midfield]`.
   * Sử dụng hàm `NONEMPTY()` để chỉ giữ lại những tiền vệ có phát sinh dữ liệu kiến tạo tại các giải VĐQG.
   * Áp dụng `TOPCOUNT()` để chọn ra đúng 10 tiền vệ có chỉ số kiến tạo cao nhất.
3. **Xác định Lát cắt (Slicer Axis / WHERE Clause):**
   * Lọc giải đấu cấp giải quốc nội: `[DIM Competition].[Competition Type].[domestic_league]`.
4. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, kết nối Database Cube `DW Football Transfermarkt`.
   * Tạo truy vấn MDX mới, dán đoạn script bên dưới và thực thi.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 02: Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Tổng số kiến tạo
    { [Measures].[Assists] } ON COLUMNS,

    -- Trục Dòng: Top 10 tiền vệ xuất sắc nhất
    TOPCOUNT(
        NONEMPTY(
            CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                { [DIM Player].[Main Position].[Midfield] }
            ),
            (
                [Measures].[Assists],
                [DIM Competition].[Competition Type].[domestic_league]
            )
        ),
        10,
        [Measures].[Assists]
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Các giải vô địch quốc gia (domestic_league)
WHERE (
    [DIM Competition].[Competition Type].[domestic_league]
);
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`TOPCOUNT`** | `TOPCOUNT(Set, Count, [Numeric_Expression])` | Trích xuất chính xác 10 tiền vệ có số kiến tạo cao nhất theo thứ tự giảm dần. |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` hoặc toán tử `*` | Tích đề-các giữa danh sách cầu thủ và thành viên `[DIM Player].[Main Position].[Midfield]`, đảm bảo kết quả trả về vừa có tên cầu thủ vừa xác nhận vị trí thi đấu. |
| **`NONEMPTY`** | `NONEMPTY(Set1, Set2)` | Loại trừ các cặp (Player, Midfield) không có bất kỳ kiến tạo nào ở giải VĐQG trước khi sắp xếp, giảm tải triệt để tài nguyên tính toán. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Số chiều tham gia:** Cầu thủ ($N \approx 30.000$) $\times$ Vị trí ($1$ thành viên `Midfield`) $\times$ Giải đấu ($1$ loại giải `domestic_league`).
* **Không gian bộ nhớ:** Việc kết hợp trực tiếp `{ [DIM Player].[Main Position].[Midfield] }` đã thu hẹp không gian từ $30.000 \times 4$ vị trí xuống chỉ còn tập hợp các tiền vệ (khoảng $\approx 8.000$ cầu thủ).
* **Bộ nhớ kết quả:** Trả về ma trận $10 \times 1$, tiêu tốn tài nguyên dưới $1\text{ KB}$ RAM.

### Độ phức tạp thời gian (Time Complexity)
* **Duyệt và kiểm tra dữ liệu:** $O(M)$ với $M$ là số lượng tiền vệ đã từng ra sân ở giải quốc nội ($M \approx 4.000$).
* **Chi phí sắp xếp (Sorting):** Sử dụng Heap Sort trong `TOPCOUNT` đạt chi phí $O(M \log 10) \approx O(M)$, nhanh hơn nhiều so với full-scan `ORDER BY` trong SQL truyền thống ($O(N \log N)$).
* **Tối ưu hóa Engine SSAS:** SSAS tận dụng mối quan hệ thuộc tính (Attribute Hierarchy) giữa Player và Main Position để định vị trực tiếp các Block dữ liệu cần tính.
