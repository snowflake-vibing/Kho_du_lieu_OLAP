# MDX Query 05: So sánh tổng bàn thắng giữa chân Trái, chân Phải & 2 Chân theo vị trí chi tiết

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Khảo sát xem đặc điểm chân thuận (`Foot`: Left, Right, Both) tương quan như thế nào với số lượng bàn thắng ghi được ở từng vai trò vị trí cụ thể trên sân cỏ (`Sub_Position` như Centre-Forward, Left Winger, Attacking Midfield...).
* **Đối tượng phân tích:** Vị trí chi tiết và chân thuận của cầu thủ (`DIM_Player`), Hiệu suất bàn thắng (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Sub Position]`, `[DIM Player].[Foot]`
  * Cube Measures: `[Measures].[Goals]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    p.Sub_Position,
    p.Foot,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE p.Foot IS NOT NULL AND p.Sub_Position IS NOT NULL
GROUP BY p.Sub_Position, p.Foot
ORDER BY p.Sub_Position, Total_Goals DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt các loại chân thuận lên cột: `{ [DIM Player].[Foot].[left], [DIM Player].[Foot].[right], [DIM Player].[Foot].[both] }` hoặc đưa thước đo `[Measures].[Goals]` lên cột.
   * Để tạo báo cáo dạng ma trận Pivot đa chiều (Cross-tab Matrix), ta có thể đặt `Foot` trên các cột và `Sub Position` trên các dòng, hoặc kết hợp Tuple trên dòng. Ở đây, cách thiết kế chuẩn OLAP trực quan nhất là đặt `[DIM Player].[Foot]` lên cột cùng `[Measures].[Goals]` và đặt `Sub Position` trên dòng (hoặc crossjoin trên dòng như SQL).
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Tích đề-các (Crossjoin) giữa `[DIM Player].[Sub Position]` và `[DIM Player].[Foot]`.
   * Sử dụng hàm `NONEMPTY()` để chỉ lấy những cặp vị trí - chân thuận có phát sinh bàn thắng.
   * Sử dụng hàm `ORDER()` với cờ phân cấp `DESC` (Hierarchy Descending) để nhóm theo từng vị trí chi tiết, sau đó sắp xếp số bàn thắng giảm dần trong nội bộ từng vị trí.
3. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, mở cửa sổ MDX Query kết nối Cube `DW Football Transfermarkt`.
   * Thực thi câu truy vấn để xem phân bổ bàn thắng theo chân thuận.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 05: Bàn thắng theo vị trí chi tiết và chân thuận
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Thước đo Bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Các cặp (Sub Position, Foot) có bàn thắng, sắp xếp phân cấp
    ORDER(
        NONEMPTY(
            CrossJoin(
                EXCEPT([DIM Player].[Sub Position].[Sub Position].MEMBERS, { [DIM Player].[Sub Position].[All] }),
                EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })
            ),
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        DESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` hoặc `Set1 * Set2` | Tạo tích đề-các giữa tập hợp vị trí thi đấu chi tiết và các loại chân thuận. |
| **`EXCEPT`** | `EXCEPT(Set1, Set2)` | Loại bỏ thành viên tổng hợp `[All]` để chỉ giữ lại các thành viên lá (leaf members) thực tế. |
| **`NONEMPTY`** | `NONEMPTY(Set, Measure)` | Lọc bỏ những tổ hợp không có bàn thắng (ví dụ: Thủ môn thuận 2 chân có thể không có bàn thắng nào). |
| **`ORDER` (DESC)** | `ORDER(Set, Expression, DESC)` | Sắp xếp có duy trì trật tự phân cấp nhóm (Hierarchy-preserving order), giúp gom các dòng của cùng một `Sub Position` lại gần nhau rồi xếp giảm dần theo bàn thắng. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Kích thước không gian tích đề-các:** Số vị trí chi tiết ($\approx 15$ vị trí) $\times$ Số loại chân thuận ($3$ loại: left, right, both) $= 45$ tuples.
* **Số dòng trả về:** Sau khi loại các ô rỗng (`NONEMPTY`), kết quả có khoảng 30 đến 40 dòng.
* **Bộ nhớ sử dụng:** Siêu nhẹ (dưới $2\text{ KB}$), phù hợp làm visual chart dạng Grouped Bar Chart trên Power BI / Excel Pivot.

### Độ phức tạp thời gian (Time Complexity)
* **Duyệt không gian:** Phép duyệt qua tập 45 tuples diễn ra tức thời $O(P \times F)$ với $P \le 15, F = 3$.
* **Tổng hợp MOLAP:** Engine SSAS đã gom sẵn dữ liệu theo thuộc tính cầu thủ trong các bitmap indexes. Thời gian phản hồi $< 5\text{ ms}$.
