# MDX Query 14: Thống kê các trận cầu mưa bàn thắng (≥ 5 bàn) qua các vòng đấu

---

## 1. Mục tiêu nghiệp vụ & Bối cảnh phân tích

* **Mục tiêu:** Lọc ra danh sách các trận đấu bùng nổ bàn thắng kịch tính (Tổng số bàn thắng của cả hai đội từ 5 bàn trở lên) qua các vòng đấu (`Round`), nhằm phục vụ phân tích chất lượng giải trí, trải nghiệm khán giả và tìm kiếm các cặp đấu cởi mở nhất.
* **Đối tượng phân tích:** Trận đấu (`DIM_Game`), Câu lạc bộ tham gia (`DIM_Club`), Bàn thắng (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo (Measures):**
  * Dimension Attributes: `[DIM Game].[Game ID]`, `[DIM Game].[Round]`, `[DIM Game].[Stadium]`
  * Cube Measures: `[Measures].[Goals]` (Tổng số bàn thắng được các cầu thủ ghi nhận trong trận)

### Đối chiếu câu lệnh T-SQL gốc
```sql
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

## 2. Quy trình thực hiện & Tư duy thiết kế MDX

Trong mô hình OLAP hình sao, tổng số bàn thắng của trận đấu có thể được tổng hợp trực tiếp từ bảng sự kiện (`FACT_Player_Match_Perf`) theo chiều `[DIM Game]`:
1. **Xác định Trục Cột (Axis 0 - COLUMNS):**
   * Đặt thước đo bàn thắng: `{ [Measures].[Goals] }`. Khi hội tụ tại cấp độ `Game_ID`, `[Measures].[Goals]` chính là tổng số bàn thắng của cả hai đội trong trận đấu đó.
2. **Xác định Trục Dòng (Axis 1 - ROWS):**
   * Kết hợp mã trận đấu và vòng đấu: `[DIM Game].[Game ID] * [DIM Game].[Round]`.
   * Sử dụng hàm `FILTER()` với điều kiện `[Measures].[Goals] >= 5` để chỉ giữ lại các trận cầu có từ 5 bàn thắng trở lên.
   * Sử dụng hàm `ORDER(..., [Measures].[Goals], BDESC)` để xếp các trận đấu có số bàn thắng kỷ lục lên đầu bảng (ví dụ: 8-2, 7-0, 5-3...).
3. **Quy trình triển khai trên SSAS / SSMS:**
   * Mở SSMS, kết nối Analysis Services Cube `DW Football Transfermarkt`.
   * Mở MDX Query Editor, dán đoạn script và chạy câu lệnh.

---

## 3. Mã truy vấn MDX chuẩn (Full Script)

```mdx
/* ==============================================================================
   Truy vấn MDX 14: Các trận đấu có tổng số bàn thắng từ 5 bàn trở lên qua các vòng đấu
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Tổng số bàn thắng trong trận đấu
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Các trận đấu có từ 5 bàn trở lên, xếp giảm dần theo số bàn thắng
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

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`FILTER`** | `FILTER(Set, [Measures].[Goals] >= 5)` | Đóng vai trò như mệnh đề `WHERE Total_Match_Goals >= 5` trong SQL, lọc bỏ các trận đấu ít bàn thắng. |
| **`NONEMPTY`** | `NONEMPTY(Set, Measure)` | Loại trừ các mã trận đấu không có sự kiện bàn thắng trước khi đưa vào hàm `FILTER`. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Sắp xếp toàn bộ các trận đấu theo số bàn thắng giảm dần tuyệt đối. |

---

## 5. Đánh giá độ phức tạp & Tối ưu hóa hiệu năng

### Độ phức tạp không gian (Space Complexity)
* **Tỷ lệ các trận mưa bàn thắng ($\ge 5$ bàn):** Trong bóng đá chuyên nghiệp, tỷ lệ các trận đấu có $\ge 5$ bàn chỉ chiếm khoảng $4\% - 7\%$ tổng số trận (khoảng 500 đến 1.000 trận trên toàn bộ lịch sử cơ sở dữ liệu).
* **Kích thước kết quả:** Khoảng $800 \text{ dòng} \times 1 \text{ cột} = 800 \text{ cells}$.
* **Bộ nhớ RAM sử dụng:** Khoảng $40\text{ KB}$.

### Độ phức tạp thời gian (Time Complexity)
* **Tổng hợp theo Game ID:** Trong SSAS, `[DIM Game].[Game ID]` là khóa hạt mịn (Granularity Key) của chiều Game nối vào Fact Table. Nhờ phân vùng dữ liệu theo Partition, việc tính tổng `SUM(Goals)` của 22 - 30 cầu thủ trong mỗi trận diễn ra theo khối (Block Computation).
* **Độ phức tạp lọc và sắp xếp:** $O(G_{filtered} \log G_{filtered})$ với $G_{filtered} \le 1.000$.
* **Thời gian thực thi:** Khoảng $30 - 60\text{ ms}$.
