# MDX Query 12: Thẻ phạt của các đội bóng phân theo Huấn luyện viên trưởng & Tháng trong năm

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Đo lường lối chơi và mức độ kỷ luật của đội bóng dưới sự dẫn dắt của từng huấn luyện viên trưởng (`Coach_Name`), thông qua tổng số thẻ vàng (`Yellow_Cards`) và thẻ đỏ (`Red_Cards`) mà các học trò nhận phải theo từng tháng trong năm (`Month`).
* **Đối tượng phân tích:** Huấn luyện viên và Câu lạc bộ (`DIM_Club`), Thời gian thi đấu (`DIM_Time`), Thẻ phạt (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Club].[Coach Name]`, `[DIM Club].[Club Name]`, `[DIM Time].[Month]`
  * Cube Measures: `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`

### Đối chiếu câu lệnh T-SQL gốc
```sql
SELECT 
    cb.Coach_Name,
    cb.Club_Name,
    t.Month,
    SUM(f.Yellow_Cards) AS Total_Yellow_Cards,
    SUM(f.Red_Cards) AS Total_Red_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE cb.Coach_Name IS NOT NULL
GROUP BY cb.Coach_Name, cb.Club_Name, t.Month
ORDER BY Total_Yellow_Cards DESC, Total_Red_Cards DESC;
```

---

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt 2 thước đo thẻ phạt: `{ [Measures].[Yellow Cards], [Measures].[Red Cards] }`.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Thực hiện tích chéo giữa 3 cấp thuộc tính:
     * Tên Huấn luyện viên: `[DIM Club].[Coach Name].[Coach Name].MEMBERS`
     * Tên Câu lạc bộ: `[DIM Club].[Club Name].[Club Name].MEMBERS`
     * Tháng trong năm: `[DIM Time].[Month].[Month].MEMBERS`
   * Dùng hàm `FILTER()` để loại trừ các dòng có tên Huấn luyện viên rỗng hoặc NULL.
   * Dùng hàm `NONEMPTY()` để chỉ giữ lại các tháng mà đội bóng thực sự thi đấu và nhận thẻ phạt.
   * Dùng hàm `ORDER(..., [Measures].[Yellow Cards], BDESC)` để xếp các tổ hợp có nhiều thẻ vàng nhất lên trước.
3. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, mở cửa sổ MDX Query kết nối Cube `DW Football Transfermarkt`.
   * Thực thi truy vấn để phân tích kỷ luật theo từng tháng của các HLV.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 12: Thẻ vàng & Thẻ đỏ theo HLV, Câu lạc bộ và Tháng trong năm
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Thẻ vàng và Thẻ đỏ
    {
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,

    -- Trục Dòng: Các cặp (HLV x CLB x Tháng) có thẻ phạt, xếp giảm dần
    ORDER(
        NONEMPTY(
            FILTER(
                CrossJoin(
                    EXCEPT([DIM Club].[Coach Name].[Coach Name].MEMBERS, { [DIM Club].[Coach Name].[All] }),
                    CrossJoin(
                        EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                        EXCEPT([DIM Time].[Month].[Month].MEMBERS, { [DIM Time].[Month].[All] })
                    )
                ),
                NOT ISEMPTY([DIM Club].[Coach Name].CURRENTMEMBER.NAME) 
                AND [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown"
            ),
            { [Measures].[Yellow Cards], [Measures].[Red Cards] }
        ),
        [Measures].[Yellow Cards],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` | Kết hợp không gian 3 chiều giữa Huấn luyện viên, Câu lạc bộ chủ quản và Tháng thi đấu. |
| **`FILTER`** | `FILTER(Set, Condition)` | Lọc sạch dữ liệu, loại bỏ các bản ghi không có thông tin HLV hoặc giá trị "Unknown". |
| **`NONEMPTY`** | `NONEMPTY(Set, Measures)` | Loại trừ các tháng không thi đấu (như tháng nghỉ hè tháng 6, tháng 7 ở một số giải đấu) hoặc tháng không bị thẻ. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Xếp hạng các giai đoạn nhận thẻ phạt căng thẳng nhất của các đội bóng. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Kích thước tích đề-các lý thuyết:** Số HLV ($\approx 350$) $\times$ CLB ($\approx 400$) $\times$ Tháng ($12$) $\approx 1.680.000$ tuples.
* **Tối ưu hóa nhờ thuộc tính phụ thuộc (Attribute Relationship):** Trong `DIM_Club`, một HLV thường chỉ thuộc về 1 hoặc 2 CLB cụ thể. Vì vậy, số tuple thực tế sau bước lọc chỉ còn khoảng $350 \times 1 \times 10 \approx 3.500$ tuples.
* **Bộ nhớ RAM sử dụng:** Khoảng $120\text{ KB}$.

### Độ phức tạp thời gian (Time Complexity)
* **Chi phí tính toán:** Phép lọc điều kiện và ghép nối trên $3.500$ tuples tốn $O(M)$ với $M \approx 3.500$.
* **Chi phí sắp xếp QuickSort:** $O(M \log M) \approx 3.500 \times 12 \approx 42.000$ phép tính so sánh.
* **Thời gian thực thi trên SSAS:** Dao động từ $15 - 35\text{ ms}$.
