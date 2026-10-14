# MDX Query 04: Bàn thắng, kiến tạo & số phút thi đấu trung bình phân theo độ tuổi năm 2023

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Khảo sát sự phân bố hiệu suất (bàn thắng `Goals`, kiến tạo `Assists`) và độ bền thể lực (số phút thi đấu trung bình mỗi trận `Avg Minutes Played`) theo từng nhóm độ tuổi (`Age`) trong năm dương lịch 2023.
* **Đối tượng phân tích:** Độ tuổi cầu thủ (`DIM_Player`), Thời gian (`DIM_Time`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Age]`, `[DIM Time].[Year]`
  * Measures gốc: `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Minutes Played]`, `[Measures].[FACT Player Match Perf Count]`
  * Calculated Measure: `[Measures].[Avg Minutes Played]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    p.Age,
    t.Year,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Assists) AS Total_Assists,
    AVG(CAST(f.Minutes_Played AS FLOAT)) AS Avg_Minutes_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Year = 2023 AND p.Age IS NOT NULL
GROUP BY p.Age, t.Year
ORDER BY p.Age ASC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Định nghĩa Thành viên Tính toán (Calculated Member - WITH MEMBER):**
   * Số phút trung bình mỗi trận = `[Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count]`.
   * Sử dụng hàm `IIF()` để kiểm tra mẫu số khác 0 nhằm ngăn ngừa lỗi chia cho 0 (`Division by Zero`).
2. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đưa 3 chỉ số lên cột: `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Avg Minutes Played]`.
3. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Lấy danh sách độ tuổi `[DIM Player].[Age].[Age].MEMBERS`.
   * Sử dụng hàm `EXCEPT` hoặc `FILTER` để loại trừ thành viên tổng quát `[All]` hoặc các giá trị độ tuổi không xác định (`NULL`).
   * Sử dụng `ORDER(..., [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE, BASC)` để sắp xếp độ tuổi tăng dần (16, 17, ..., 40).
4. **Xác định Lát cắt (Slicer Axis / WHERE Clause):**
   * Cắt dữ liệu trong năm 2023: `[DIM Time].[Year].[2023]`.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 04: Hiệu suất bàn thắng, kiến tạo & phút thi đấu trung bình theo tuổi
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- Tính số phút trung bình mỗi lần ra sân
    MEMBER [Measures].[Avg Minutes Played] AS
        IIF(
            IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
            NULL,
            ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
        ),
        FORMAT_STRING = "#,##0.00"

SELECT
    -- Trục Cột: Bàn thắng, Kiến tạo và Số phút trung bình
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng: Các độ tuổi hợp lệ, sắp xếp tăng dần từ trẻ tới lớn
    ORDER(
        FILTER(
            [DIM Player].[Age].[Age].MEMBERS,
            NOT ISEMPTY([DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE) 
            AND [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE > 0
        ),
        [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE,
        BASC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Năm dương lịch 2023
WHERE (
    [DIM Time].[Year].[2023]
);
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`WITH MEMBER`** | `WITH MEMBER CubeName.MemberName AS Expression` | Định nghĩa thước đo suy diễn `[Avg Minutes Played]` tính toán ngay trong phiên truy vấn mà không cần thay đổi cấu trúc Cube vật lý. |
| **`IIF`** | `IIF(Condition, True_Value, False_Value)` | Rẽ nhánh điều kiện: nếu số lượt ra sân bằng 0 hoặc rỗng thì trả về `NULL`, ngược lại chia lấy số trung bình. |
| **`MEMBERVALUE`** | `Member.MEMBERVALUE` | Lấy giá trị số học nguyên thủy của thuộc tính `Age` để phục vụ so sánh và sắp xếp số học thay vì sắp xếp chuỗi ký tự. |
| **`ROUND`** | `ROUND(Numeric_Expression, Decimals)` | Làm tròn số phút trung bình đến 2 chữ số thập phân. |
| **`ORDER` (BASC)** | `ORDER(Set, Value, BASC)` | Sắp xếp danh sách tuổi tăng dần (Break Hierarchy Ascending). |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Số lượng nhóm tuổi:** Khoảng 25 đến 30 mức tuổi (từ 16 đến 42 tuổi).
* **Kích thước ma trận:** $30 \text{ dòng} \times 3 \text{ cột} = 90 \text{ ô dữ liệu (cells)}$.
* **Tài nguyên bộ nhớ:** Tiêu thụ bộ nhớ không đáng kể ($< 2\text{ KB}$ RAM).

### Độ phức tạp thời gian (Time Complexity)
* **Thời gian tổng hợp:** Nhờ cơ chế lưu trữ MOLAP, các tổng `[Minutes Played]`, `[Goals]`, `[Assists]`, `[Count]` theo năm 2023 và theo độ tuổi đã được tính gộp sẵn trong các phân vùng (partitions) hoặc băm trực tiếp.
* **Độ phức tạp tính toán:** $O(A)$ với $A \approx 30$ là số lượng giá trị độ tuổi khác nhau.
* **Chi phí sắp xếp:** $O(A \log A)$ với $A = 30$, tốn dưới $0.1\text{ ms}$.
