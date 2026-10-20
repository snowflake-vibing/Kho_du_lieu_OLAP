# CHƯƠNG 05: THÀNH VIÊN TÍNH TOÁN & TẬP HỢP ĐẶT TÊN (`WITH MEMBER` & `WITH SET`)

---

## 1. KHÁI NIỆM VÀ PHẠM VI (SCOPE) CỦA MỆNH ĐỀ `WITH`

Trong các bài toán phân tích thực tế, các chỉ số lưu sẵn trong bảng FACT thường chỉ là các giá trị đếm hoặc tổng thô (như số bàn thắng, số phút thi đấu). Các chuyên gia BI luôn cần các chỉ số phái sinh bậc cao như: tỷ lệ chuyển hóa, hiệu suất trên 90 phút, điểm kỷ luật quy đổi hoặc gom nhóm các thực thể logic.

Mệnh đề `WITH` trong MDX cho phép người dùng định nghĩa hai loại thực thể động tại thời gian chạy (Runtime):
1. **`WITH MEMBER`**: Khai báo thành viên tính toán (Calculated Member).
2. **`WITH SET`**: Khai báo tập hợp đặt tên (Named Set).

```
                            PHẠM VI CỦA CALCULATED MEMBER
  ┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
  │ 1. QUERY-SCOPED (MDX)   │ 2. SESSION-SCOPED       │ 3. CUBE-SCOPED (GLOBAL) │
  │ Khai báo qua mệnh đề    │ Tạo bằng lệnh           │ Khai báo trong tab      │
  │ WITH MEMBER trong câu   │ CREATE MEMBER trong một │ Calculations của Visual │
  │ truy vấn. Chỉ tồn tại   │ phiên kết nối XMLA      │ Studio SSDT và deploy   │
  │ trong lần chạy đó.      │ duy nhất.               │ vĩnh viễn lên Cube.     │
  └─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## 2. CHUYÊN SÂU `WITH MEMBER`: THUỘC TÍNH VÀ GIẢI QUYẾT XUNG ĐỘT THỨ TỰ TÍNH (`SOLVE_ORDER`)

### 2.1. Các thuộc tính chuẩn của `WITH MEMBER`
Khi khai báo một `MEMBER`, ta có thể gắn kèm các thuộc tính định dạng:
- **`FORMAT_STRING`**: Định dạng hiển thị chuỗi (Số nguyên `'#,##0'`, Số thực `'0.00'`, Phần trăm `'0.00%'`, Tiền tệ `'$#,##0'`).
- **`SOLVE_ORDER`**: Số nguyên xác định thứ tự ưu tiên tính toán khi hai thành viên tính toán giao nhau tại một ô (Cell).
- **`NON_EMPTY_BEHAVIOR`**: Chỉ định Measure cơ sở để tối ưu hóa việc bỏ qua ô rỗng ở tầng Storage Engine.

### 2.2. Vấn đề xung đột thứ tự tính toán và giải pháp `SOLVE_ORDER`
Giả sử ta có 2 Calculated Member:
1. `[Measures].[Profit Margin]` trên chiều Measure = `Profit / Sales` (Tỷ lệ phần trăm).
2. `[DIM Time].[Year].[Growth YoY]` trên chiều Time = `CurrentYear - PrevYear` (Độ biến thiên).

Tại ô giao điểm giữa `[Growth YoY]` và `[Profit Margin]`, SSAS sẽ tính cái nào trước?
- **Nếu tính Margin trước rồi mới tính Growth**: Kết quả là hiệu số giữa 2 tỷ lệ (Ví dụ: $20\% - 15\% = +5\%$).
- **Nếu tính Growth trước rồi mới tính Margin**: Kết quả là tỷ lệ giữa Growth Profit và Growth Sales.

Để kiểm soát hành vi này, ta dùng **`SOLVE_ORDER`**: Phép tính có chỉ số `SOLVE_ORDER` cao hơn sẽ được tính toán sau cùng (ghi đè kết quả của phép tính có `SOLVE_ORDER` thấp hơn).

---

## 3. CHUYÊN SÂU `WITH SET`: TẬP HỢP TĨNH VS TẬP HỢP ĐỘNG

- **Tập hợp tĩnh (Static Set)**: Được tính toán một lần duy nhất tại ngữ cảnh khối toàn cục khi truy vấn khởi chạy.
- **Tập hợp động (Dynamic Set)**: Sử dụng từ khóa `DYNAMIC SET`, được lượng giá lại mỗi khi ngữ cảnh trục hoặc lát cắt thay đổi, giúp câu truy vấn linh hoạt thích ứng với các bộ lọc phân cấp con.

---

## 4. VÍ DỤ PHỨC TẠP: HỆ THỐNG ĐÁNH GIÁ "CẦU THỦ TOÀN DIỆN" VÀ CHỈ SỐ KỶ LUẬT QUY ĐỔI

> **Đề bài nghiệp vụ**: Xây dựng báo cáo toàn diện đánh giá hiệu quả tấn công và mức độ kỷ luật của các ngôi sao hàng đầu:
> 1. Tính **Điểm kỷ luật quy đổi (`Disciplinary Points`)**: Mỗi thẻ vàng $= 1$ điểm, mỗi thẻ đỏ $= 3$ điểm.
> 2. Tính **Hiệu suất đóng góp trên 90 phút thi đấu (`Contributions Per 90 Mins`)**: $(Goals + Assists) \times 90 / Minutes$.
> 3. Tạo một **Thành viên tính toán trên Dimension** đại diện cho nhóm liên minh 2 CLB thành Manchester: `[Manchester Combined] = [Manchester City] + [Manchester United]`.
> 4. Định nghĩa một **Named Set** động lọc ra các cầu thủ có trên 1500 phút thi đấu.
> 5. Sử dụng `SOLVE_ORDER` để tính tỷ số giữa Hiệu suất bàn thắng và Điểm phạt tại ô giao điểm.

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Thành viên tính toán trên Measure: Điểm kỷ luật quy đổi
MEMBER [Measures].[Disciplinary Points] AS
    ([Measures].[Yellow Cards] * 1) + ([Measures].[Red Cards] * 3),
    FORMAT_STRING = '#,##0',
    SOLVE_ORDER = 1

-- 2. Thành viên tính toán trên Measure: Đóng góp bàn thắng trên 90 phút (P90)
MEMBER [Measures].[Contributions Per 90] AS
    IIF(
        [Measures].[Minutes Played] = 0, 
        NULL,
        (([Measures].[Goals] + [Measures].[Assists]) * 90.0) / [Measures].[Minutes Played]
    ),
    FORMAT_STRING = '0.00',
    SOLVE_ORDER = 1

-- 3. Thành viên tính toán trên DIMENSION: Liên minh Manchester
MEMBER [DIM Club].[Club Name].[Manchester Combined] AS
    AGGREGATE(
        {
            [DIM Club].[Club Name].[Manchester City],
            [DIM Club].[Club Name].[Manchester United]
        }
    ),
    SOLVE_ORDER = 2

-- 4. Định nghĩa Named Set: Danh sách các cầu thủ trụ cột ra sân nhiều
SET [Regular_Players_Set] AS
    FILTER(
        {
            [DIM Player].[Player Name].[Erling Haaland],
            [DIM Player].[Player Name].[Phil Foden],
            [DIM Player].[Player Name].[Bruno Fernandes],
            [DIM Player].[Player Name].[Marcus Rashford],
            [DIM Player].[Player Name].[Casemiro]
        },
        [Measures].[Minutes Played] >= 1200
    )

SELECT 
    -- TRỤC CỘT: 5 Thước đo phản ánh hiệu năng và kỷ luật
    {
        [Measures].[Minutes Played],
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Contributions Per 90],
        [Measures].[Disciplinary Points]
    } ON AXIS(0),

    -- TRỤC DÒNG: Tích Đề-các giữa CLB (bao gồm cả Member tính toán) và Cầu thủ
    NON EMPTY 
    CROSSJOIN(
        {
            [DIM Club].[Club Name].[Manchester City],
            [DIM Club].[Club Name].[Manchester United],
            [DIM Club].[Club Name].[Manchester Combined]
        },
        [Regular_Players_Set]
    ) ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định tại Mùa giải 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh sự tính toán chuẩn xác của các Calculated Member và Named Set:

| Câu lạc bộ (`DIM Club`) | Cầu thủ (`DIM Player`) | Phút thi đấu | Bàn thắng | Kiến tạo | Đóng góp / 90 phút | Điểm kỷ luật |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | **Erling Haaland** | 2,558 | 27 | 5 | **1.13** | 2 |
| **Manchester City** | **Phil Foden** | 2,860 | 19 | 8 | **0.85** | 2 |
| **Manchester United** | **Bruno Fernandes** | 3,120 | 10 | 8 | **0.52** | 9 |
| **Manchester United** | **Marcus Rashford** | 2,012 | 7 | 2 | **0.40** | 4 |
| **Manchester United** | **Casemiro** | 1,710 | 1 | 2 | **0.16** | **11** |
| **Manchester Combined**| **Erling Haaland** | 2,558 | 27 | 5 | 1.13 | 2 |
| **Manchester Combined**| **Phil Foden** | 2,860 | 19 | 8 | 0.85 | 2 |
| **Manchester Combined**| **Bruno Fernandes** | 3,120 | 10 | 8 | 0.52 | 9 |
| **Manchester Combined**| **Marcus Rashford** | 2,012 | 7 | 2 | 0.40 | 4 |
| **Manchester Combined**| **Casemiro** | 1,710 | 1 | 2 | 0.16 | 11 |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp tính toán chỉ số chuẩn hóa 90 phút (`Contributions Per 90`)**:
   - Mặc dù Bruno Fernandes có số phút thi đấu cao nhất (3,120 phút), nhưng hiệu suất trên 90 phút của Erling Haaland đạt tới **1.13** (trung bình cứ mỗi 90 phút có mặt trên sân, Haaland đóng góp hơn 1.1 bàn thắng/kiến tạo).
2. **Trường hợp thành viên tính toán trên Dimension (`Manchester Combined`)**:
   - Member nhân tạo này gom nhóm toàn bộ cầu thủ của cả 2 đội bóng thành Manchester. Khi chiếu lên từng cầu thủ, giá trị của họ được giữ nguyên; nhưng nếu tính tổng trên toàn đội, SSAS sẽ tự động tổng hợp toàn bộ các chỉ số của hai CLB lại với nhau một cách nhất quán.
3. **Trường hợp quy đổi điểm kỷ luật (`Disciplinary Points`)**:
   - Cầu thủ Casemiro nhận 8 thẻ vàng ($8 \times 1 = 8$) và 1 thẻ đỏ ($1 \times 3 = 3$), mang về tổng cộng **11 điểm kỷ luật**, thể hiện rõ mức độ căng thẳng trong lối chơi phòng ngự đánh chặn.
