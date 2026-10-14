# MDX Query 07: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu thuộc Nước Anh

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Đo lường sự đóng góp chuyên môn của lực lượng cầu thủ nội địa Anh so với các làn sóng cầu thủ ngoại binh (phân theo quốc tịch `Country_Of_Citizenship`) tại toàn bộ các giải đấu diễn ra ở xứ sở sương mù (`Country_Name = 'England'` bao gồm Premier League, FA Cup, EFL Cup...).
* **Đối tượng phân tích:** Quốc tịch cầu thủ (`DIM_Player`), Quốc gia tổ chức giải đấu (`DIM_Competition`), Hiệu suất ghi bàn (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Player].[Country Of Citizenship]`, `[DIM Competition].[Country Name]`
  * Cube Measures: `[Measures].[Goals]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    p.Country_Of_Citizenship,
    c.Country_Name,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
WHERE c.Country_Name = 'England' AND p.Country_Of_Citizenship IS NOT NULL
GROUP BY p.Country_Of_Citizenship, c.Country_Name
ORDER BY Total_Goals DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt thước đo `[Measures].[Goals]` để thể hiện tổng số bàn thắng.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Lấy tập hợp các quốc tịch cầu thủ `[DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS`.
   * Sử dụng hàm `NONEMPTY()` với điều kiện ngữ cảnh tại giải đấu Nước Anh để loại trừ các quốc gia không có cầu thủ ghi bàn tại Anh.
   * Áp dụng `ORDER(..., [Measures].[Goals], BDESC)` để xếp hạng các quốc gia ghi nhiều bàn nhất từ trên xuống dưới (ví dụ: England, France, Brazil, Spain...).
3. **Xác định Lát cắt (Slicer Axis / WHERE Clause):**
   * Giới hạn giải đấu tại nước Anh: `[DIM Competition].[Country Name].[England]`.
4. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, mở cửa sổ truy vấn MDX vào Cube `DW Football Transfermarkt`.
   * Dán câu lệnh và thực thi để quan sát bảng xếp hạng quốc tịch.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 07: Bàn thắng theo quốc tịch cầu thủ tại các giải đấu ở Nước Anh
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Danh sách quốc tịch có bàn thắng tại Anh, xếp giảm dần
    ORDER(
        NONEMPTY(
            EXCEPT(
                [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                { [DIM Player].[Country Of Citizenship].[All] }
            ),
            (
                [Measures].[Goals],
                [DIM Competition].[Country Name].[England]
            )
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Các giải đấu thuộc Nước Anh
WHERE (
    [DIM Competition].[Country Name].[England]
);
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`NONEMPTY`** | `NONEMPTY(Set, Tuple)` | Lọc bỏ toàn bộ các quốc gia không có bàn thắng nào tại các giải đấu ở Anh, thu nhỏ không gian duyệt dữ liệu. |
| **`EXCEPT`** | `EXCEPT(Set1, Set2)` | Loại bỏ phần tử cấp tổng thể `[All]` của chiều `Country Of Citizenship`. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Xếp hạng các quốc gia theo tổng bàn thắng giảm dần tuyệt đối, không phân cấp. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Số lượng quốc gia trên thế giới:** Khoảng 190 đến 210 quốc tịch trong cơ sở dữ liệu quốc tế.
* **Số dòng thực tế:** Sau khi lọc qua giải đấu tại Anh, chỉ còn khoảng 70 đến 90 quốc gia có cầu thủ từng ghi bàn tại các giải đấu Anh.
* **Bộ nhớ ma trận trả về:** Dưới $5\text{ KB}$ RAM.

### Độ phức tạp thời gian (Time Complexity)
* **Thời gian tổng hợp:** Với $C \approx 90$ quốc gia hợp lệ, chi phí sắp xếp $O(C \log C) \approx 90 \times \log_2(90) \approx 580$ phép so sánh.
* **Truy xuất MOLAP:** Nhờ chiều `DIM Competition` liên kết trực tiếp với `FACT_Player_Match_Perf`, SSAS lọc các block sự kiện theo `Country Name = 'England'` qua bitmap index với tốc độ $O(1)$ block-lookup.
* **Thời gian phản hồi:** Khoảng $10 - 20\text{ ms}$.
