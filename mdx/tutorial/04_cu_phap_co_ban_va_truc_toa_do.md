# CHƯƠNG 04: CẤU TRÚC CÚ PHÁP CƠ BẢN VÀ CÁC TRỤC TỌA ĐỘ (AXES & SLICER)

---

## 1. CÚ PHÁP TỔNG QUÁT VÀ NGUYÊN TẮC CÁC TRỤC TRUY VẤN (AXES)

Một câu truy vấn MDX chuẩn mực có cấu trúc cú pháp tổng quát như sau:

```mdx
[WITH <calculated_members_and_named_sets>]
SELECT 
    [NON EMPTY] <set_expression_0> ON AXIS(0), -- hoặc ON COLUMNS
    [NON EMPTY] <set_expression_1> ON AXIS(1), -- hoặc ON ROWS
    [NON EMPTY] <set_expression_2> ON AXIS(2)  -- hoặc ON PAGES
    ...
FROM [<cube_specification>]
[WHERE (<slicer_specification>)]
```

### 1.1. Các quy tắc vàng khi định nghĩa trục tọa độ
1. **Quy tắc liên tục của chỉ số trục**: Trong MDX, các trục phải được khai báo tuần tự bắt đầu từ `AXIS(0)`. Bạn không thể định nghĩa `AXIS(1)` (ROWS) nếu chưa khai báo `AXIS(0)` (COLUMNS).
2. **Tên định danh chuẩn**:
   - `AXIS(0)` tương đương với từ khóa `COLUMNS`.
   - `AXIS(1)` tương đương với từ khóa `ROWS`.
   - `AXIS(2)` tương đương với từ khóa `PAGES`.
   - `AXIS(3)` tương đương với từ khóa `SECTIONS`.
   - `AXIS(4)` tương đương với từ khóa `CHAPTERS`.
3. **Tính độc lập không gian**: Các tập hợp đặt trên mỗi trục phải độc lập với nhau. Bạn không thể đặt cùng một chiều dữ liệu lên cả hai trục `COLUMNS` và `ROWS` cùng một lúc.

```
                     TRỤC COLUMNS (AXIS 0)
                     ┌──────────────────────────────────────────────┐
                     │ [Measures].[Goals]  │ [Measures].[Assists]   │
┌────────────────────┼─────────────────────┼────────────────────────┤
│ Haaland            │ 36                  │ 8                      │
│ Saka               │ 14                  │ 11                     │
│ Salah              │ 19                  │ 12                     │
└────────────────────┴─────────────────────┴────────────────────────┘
▲
│
TRỤC ROWS (AXIS 1)
```

---

## 2. TRỤC CẮT LÁT (SLICER AXIS - MỆNH ĐỀ `WHERE`)

Mệnh đề `WHERE` trong MDX không làm thay đổi các phần tử xuất hiện trên trục `ROWS` hay `COLUMNS`, mà có nhiệm vụ ấn định **Tọa độ ngữ cảnh lát cắt (Slicer Coordinate)** cho toàn bộ siêu khối.

### 2.1. Cắt lát bằng một Tuple đơn lẻ
```mdx
-- Cắt lát không gian dữ liệu cố định tại Mùa giải 2023 và Quốc gia thi đấu là Nước Anh
WHERE (
    [DIM Time].[Hierarchy].[Year].[2023],
    [DIM Competition].[Country Name].[England]
)
```

### 2.2. Cắt lát đa phần tử (Multi-Select Slicer)
Nếu cần cắt lát trên nhiều Member của cùng một chiều (ví dụ: chỉ tính dữ liệu của 2 mùa giải 2022 và 2023), ta sử dụng tập hợp `{...}` bên trong mệnh đề `WHERE`. SSAS sẽ tự động tổng hợp (`AGGREGATE`) giá trị của các phần tử này:
```mdx
WHERE (
    {[DIM Time].[Hierarchy].[Year].[2022], [DIM Time].[Hierarchy].[Year].[2023]},
    [DIM Competition].[Country Name].[England]
)
```

---

## 3. TỐI ƯU HÓA Ô THƯA: TỪ KHÓA `NON EMPTY` VS HÀM `NONEMPTY()`

Trong cơ sở dữ liệu phân tích bóng đá, số lượng kết hợp giữa Cầu thủ, CLB và Thời gian lên tới hàng triệu cell, nhưng phần lớn không có phát sinh dữ liệu (ô mang giá trị `NULL`). Nếu không xử lý, câu truy vấn sẽ trả về hàng ngàn dòng trống, gây quá tải bộ nhớ client.

```
       Ma trận Dữ liệu Thô (Có ô NULL)              Sau khi áp dụng NON EMPTY trên ROWS
    ┌────────────┬───────┬─────────┐               ┌────────────┬───────┬─────────┐
    │ Cầu thủ    │ Goals │ Assists │               │ Cầu thủ    │ Goals │ Assists │
    ├────────────┼───────┼─────────┤               ├────────────┼───────┼─────────┤
    │ Haaland    │ 36    │ 8       │      ───►     │ Haaland    │ 36    │ 8       │
    │ Thủ môn A  │ (null)│ (null)  │  (Loại bỏ)    │ Salah      │ 19    │ 12      │
    │ Hậu vệ B   │ (null)│ (null)  │  (Loại bỏ)    └────────────┴───────┴─────────┘
    │ Salah      │ 19    │ 12      │
    └────────────┴───────┴─────────┘
```

### So sánh giữa từ khóa `NON EMPTY` và hàm `NonEmpty()`

| Đặc điểm | Từ khóa `NON EMPTY` | Hàm `NonEmpty(Set1, Set2)` |
| :--- | :--- | :--- |
| **Vị trí cú pháp** | Đặt ngay trước biểu thức Set trên trục: `NON EMPTY <Set> ON ROWS` | Là một hàm tập hợp độc lập bọc bên ngoài Set: `NonEmpty(Set1, [Measures])` |
| **Thời điểm thực thi**| Thực thi ở bước cuối cùng sau khi ma trận kết quả đã được Formula Engine tính toán xong. | Thực thi sớm ngay tại tầng Storage Engine trước khi đưa vào các hàm lọc/sắp xếp khác. |
| **Ứng dụng tối ưu** | Sử dụng cho việc hiển thị bảng kết quả cuối cùng. | Tối ưu hóa khi kết hợp với `TOPCOUNT`, `FILTER`, `ORDER` để giảm kích thước tập hợp đầu vào. |

---

## 4. VÍ DỤ PHỨC TẠP: KẾT HỢP ĐA TRỤC, SLICER ĐA CHIỀU VÀ XỬ LÝ Ô THƯA

> **Đề bài nghiệp vụ**: Lập báo cáo ma trận phân tích chuyên sâu hiệu suất tấn công và kỷ luật thi đấu của các Tiền đạo (`Attack`) và Tiền vệ (`Midfield`) thuộc các CLB hàng đầu London (**Arsenal FC, Chelsea FC, Tottenham Hotspur**).
> - **Trục Cột (`COLUMNS`)**: Gồm 4 thước đo: Bàn thắng (`Goals`), Kiến tạo (`Assists`), Thẻ vàng (`Yellow Cards`) và Tổng số phút thi đấu (`Minutes Played`).
> - **Trục Dòng (`ROWS`)**: Kết hợp đa chiều giữa **Câu lạc bộ** $\times$ **Tuyến thi đấu** $\times$ **Cầu thủ tiêu biểu**.
> - **Trục Cắt lát (`WHERE`)**: Giới hạn cố định tại Mùa giải 2023 của giải Ngoại Hạng Anh (`GB1`).
> - **Yêu cầu kỹ thuật**: Áp dụng `NON EMPTY` để loại trừ triệt để các cầu thủ không có phút thi đấu hoặc chỉ số bằng rỗng.

### Mã truy vấn MDX:
```mdx
WITH 
-- Định nghĩa tập hợp các cầu thủ khảo sát thuộc 3 CLB London
SET [Selected_London_Players] AS
    {
        [DIM Player].[Player Name].[Bukayo Saka],
        [DIM Player].[Player Name].[Martin Odegaard],
        [DIM Player].[Player Name].[Cole Palmer],
        [DIM Player].[Player Name].[Nicolas Jackson],
        [DIM Player].[Player Name].[Son Heung-min],
        [DIM Player].[Player Name].[James Maddison],
        -- Cầu thủ dự bị ít ra sân để kiểm chứng ô thưa (Edge Case)
        [DIM Player].[Player Name].[Alfie Devine]
    }

SELECT 
    -- TRỤC CỘT (AXIS 0): Danh sách 4 Thước đo
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Yellow Cards],
        [Measures].[Minutes Played]
    } ON AXIS(0),

    -- TRỤC DÒNG (AXIS 1): Tích 3 chiều: CLB x Tuyến x Cầu thủ
    NON EMPTY 
    CROSSJOIN(
        {[DIM Club].[Club Name].[Arsenal FC], [DIM Club].[Club Name].[Chelsea FC], [DIM Club].[Club Name].[Tottenham Hotspur]},
        {[DIM Player].[Main Position].[Attack], [DIM Player].[Main Position].[Midfield]},
        [Selected_London_Players]
    ) ON AXIS(1)

FROM [DW Football Transfermarkt]
-- TRỤC CẮT LÁT (SLICER AXIS): Mùa giải 2023 tại giải Premier League (GB1)
WHERE (
    [DIM Time].[Hierarchy].[Year].[2023],
    [DIM Competition].[Competition ID].[GB1]
)
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh đầy đủ hoạt động của các trục và cơ chế loại bỏ ô thưa:

| Câu lạc bộ (`DIM Club`) | Tuyến thi đấu | Tên cầu thủ (`DIM Player`) | Bàn thắng (`Goals`) | Kiến tạo (`Assists`) | Thẻ vàng (`Yellow Cards`) | Số phút thi đấu (`Minutes Played`) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Arsenal FC** | **Attack** | **Bukayo Saka** | 16 | 9 | 4 | 2,938 |
| **Arsenal FC** | **Midfield** | **Martin Odegaard** | 8 | 10 | 2 | 3,095 |
| **Chelsea FC** | **Midfield** | **Cole Palmer** | 22 | 11 | 7 | 2,618 |
| **Chelsea FC** | **Attack** | **Nicolas Jackson** | 14 | 5 | 10 | 2,804 |
| **Tottenham Hotspur** | **Attack** | **Son Heung-min** | 17 | 10 | 1 | 2,945 |
| **Tottenham Hotspur** | **Midfield** | **James Maddison** | 4 | 9 | 4 | 2,143 |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp loại trừ ô thưa hợp lệ (`NON EMPTY`)**:
   - Cầu thủ trẻ `Alfie Devine` (Tottenham) trong năm 2023 tại giải `GB1` không có phút thi đấu chính thức (toàn bộ các Measure đều trả về `NULL`). Nhờ có từ khóa `NON EMPTY` trên trục `ROWS`, dòng dữ liệu của cầu thủ này bị triệt tiêu hoàn toàn, không hiển thị làm rác báo cáo.
2. **Trường hợp tự động triệt tiêu các kết hợp sai lệch hình học (Cross-Dimensional Inconsistency)**:
   - Phép `CROSSJOIN` về mặt toán học sẽ sinh ra cặp `(Arsenal FC, Cole Palmer)`. Tuy nhiên, do Cole Palmer thi đấu cho Chelsea chứ không đá cho Arsenal, ô dữ liệu tại giao điểm này mang giá trị `NULL`. `NON EMPTY` đã tự động loại bỏ tất cả các tổ hợp không có thật này.
3. **Trường hợp Slicer độc lập**: Mệnh đề `WHERE ([Year].[2023], [Competition ID].[GB1])` hoạt động ngầm định ở tầng dưới; kết quả thống kê hoàn toàn chỉ phản ánh các trận đấu thuộc giải Ngoại Hạng Anh trong năm 2023.
