# CHƯƠNG 11: CÁC HÀM THỐNG KÊ & BIỂU THỨC LOGIC NGHIỆP VỤ (`CASE`, `IIF`, `EXISTING`)

---

## 1. BẢNG TỔNG HỢP CÁC HÀM THỐNG KÊ TRONG MDX

Khác với các hàm tổng hợp mặc định của Measure trong bảng Fact, MDX cho phép người dùng áp dụng các hàm thống kê động trên bất kỳ tập hợp (Set) nào:

| Tên hàm | Cú pháp chuẩn | Cơ chế xử lý ô trống (NULL) |
| :--- | :--- | :--- |
| **`SUM`** | `SUM(Set, [Numeric_Exp])` | Bỏ qua các ô NULL, cộng dồn các giá trị số. |
| **`AVG`** | `AVG(Set, [Numeric_Exp])` | **Tự động loại bỏ ô NULL khỏi mẫu số** (chỉ chia cho số ô có dữ liệu thực). |
| **`MIN` / `MAX`** | `MIN(Set, [Numeric_Exp])` | Tìm giá trị nhỏ nhất / lớn nhất trong tập hợp. |
| **`COUNT`** | `COUNT(Set, [EXCLUDEEMPTY / INCLUDEEMPTY])` | Đếm số lượng phần tử trong Set (có cờ kiểm soát ô rỗng). |
| **`DISTINCTCOUNT`**| `DISTINCTCOUNT(Set)` | Đếm số lượng thực thể phân biệt (loại trừ đếm lặp). |

---

## 2. CHUYÊN SÂU TỪ KHÓA CHUYỂN NGỮ CẢNH: `EXISTING`

Một trong những khái niệm quan trọng nhất khi viết Calculated Member trong MDX là từ khóa **`EXISTING`** (Chuyển đổi ngữ cảnh - Context Transition):
- **Không có `EXISTING`**: Tập hợp `[DIM Player].[Player Name].Members` sẽ đại diện cho **toàn bộ cầu thủ trên toàn thế giới trong Cube**.
- **Có từ khóa `EXISTING`**: Tập hợp bị ép buộc phải lọc lại theo đúng tọa độ của dòng hiện tại (Ví dụ: Tại dòng của Arsenal, `EXISTING [DIM Player].[Player Name].Members` sẽ tự động co lại chỉ gồm các cầu thủ thuộc CLB Arsenal).

```mdx
-- Tính chiều cao trung bình của riêng CLB ở dòng hiện tại
MEMBER [Measures].[Club Avg Height] AS
    AVG(
        EXISTING [DIM Player].[Player Name].Members,
        [DIM Player].[Height].CurrentMember.Member_Value
    )
```

---

## 3. BIỂU THỨC LOGIC RẼ NHÁNH: `IIF()` VÀ CẤU TRÚC `CASE WHEN`

### 3.1. Hàm điều kiện đơn `IIF()`
Cú pháp: `IIF(Boolean_Expression, True_Part, False_Part)`.
- Rất phổ biến để kiểm tra mẫu số chống chia cho 0:
  ```mdx
  IIF([Measures].[Minutes Played] = 0, NULL, [Measures].[Goals] / [Measures].[Minutes Played])
  ```

### 3.2. Cấu trúc rẽ nhánh đa tầng `CASE WHEN`
Khi cần phân loại đối tượng thành nhiều nhóm nghiệp vụ phức tạp, cấu trúc `CASE WHEN` là lựa chọn chuẩn mực:

```mdx
CASE 
    WHEN [Measures].[Goals] >= 20 THEN 'Hạng 1: Siêu sát thủ (World Class)'
    WHEN [Measures].[Goals] >= 10 THEN 'Hạng 2: Cầu thủ chủ lực (Key Starter)'
    WHEN [Measures].[Goals] >= 5  THEN 'Hạng 3: Cầu thủ tiềm năng (Rotation)'
    ELSE 'Hạng 4: Cầu thủ dự bị (Squad Player)'
END
```

### 3.3. Xử lý giá trị khuyết thiếu với `COALESCEEMPTY()`
Cú pháp: `COALESCEEMPTY(Exp1, Exp2, ...)`. Hàm trả về giá trị đầu tiên khác rỗng.
- *Ứng dụng*: Điền giá trị mặc định (như `"Không xác định"` hoặc `0`) khi dữ liệu sức chứa sân bóng hoặc số liệu cầu thủ bị khuyết thiếu.

---

## 4. VÍ DỤ PHỨC TẠP: HỆ THỐNG THỐNG KÊ THỂ HÌNH VÀ PHÂN HẠNG NĂNG LỰC CẦU THỦ TOÀN DIỆN

> **Đề bài nghiệp vụ**: Ban y tế và ban huấn luyện yêu cầu lập báo cáo phân tích theo 4 Tuyến thi đấu chính (`Attack`, `Midfield`, `Defender`, `Goalkeeper`):
> 1. Thống kê thể hình: Chiều cao trung bình (`Avg Height`), Chiều cao lớn nhất (`Max Height`), Chiều cao nhỏ nhất (`Min Height`) bằng các hàm thống kê kết hợp `EXISTING`.
> 2. Đếm số lượng cầu thủ phân biệt thực tế đã ra sân (`Active Distinct Players`).
> 3. Đánh giá **Hạng năng lực tuyến thi đấu (Performance Tier)** bằng cấu trúc `CASE WHEN` đa nhánh dựa trên tổng số bàn thắng và thẻ phạt.
> 4. Sử dụng `COALESCEEMPTY` để làm sạch dữ liệu nếu có chỉ số bị rỗng.

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Chiều cao trung bình của tuyến
MEMBER [Measures].[Tuyen Avg Height] AS
    AVG(
        EXISTING [DIM Player].[Player Name].Children,
        [DIM Player].[Height].CurrentMember.Member_Value
    ),
    FORMAT_STRING = '0.0 cm'

-- 2. Chiều cao lớn nhất
MEMBER [Measures].[Tuyen Max Height] AS
    MAX(
        EXISTING [DIM Player].[Player Name].Children,
        [DIM Player].[Height].CurrentMember.Member_Value
    ),
    FORMAT_STRING = '#,##0 cm'

-- 3. Chiều cao nhỏ nhất
MEMBER [Measures].[Tuyen Min Height] AS
    MIN(
        EXISTING [DIM Player].[Player Name].Children,
        [DIM Player].[Height].CurrentMember.Member_Value
    ),
    FORMAT_STRING = '#,##0 cm'

-- 4. Đếm số lượng cầu thủ duy nhất ra sân
MEMBER [Measures].[Unique Players Count] AS
    DISTINCTCOUNT(
        EXISTING [DIM Player].[Player Name].Children
    ),
    FORMAT_STRING = '#,##0'

-- 5. Đánh giá phân hạng chuyên môn bằng cấu trúc CASE WHEN
MEMBER [Measures].[Tuyen Evaluation Tier] AS
    CASE 
        WHEN [DIM Player].[Main Position].CurrentMember.Name = 'Goalkeeper' THEN
            IIF([Measures].[Red Cards] = 0, 'Thủ môn: An toàn & Đạt chuẩn', 'Thủ môn: Rủi ro thẻ phạt cao')
        WHEN [Measures].[Goals] >= 500 THEN 'Tuyến Tấn công: Siêu hỏa lực (Elite Firepower)'
        WHEN [Measures].[Goals] >= 200 THEN 'Tuyến Tấn công: Hiệu quả tốt (Good Output)'
        WHEN [Measures].[Yellow Cards] >= 400 THEN 'Tuyến Tranh chấp: Khu vực nóng thẻ phạt'
        ELSE 'Tuyến Hoạt động: Mức độ bình ổn'
    END

SELECT 
    -- TRỤC CỘT: Trọn bộ 7 Thước đo Thống kê & Phân hạng
    {
        [Measures].[Unique Players Count],
        [Measures].[Tuyen Min Height],
        [Measures].[Tuyen Avg Height],
        [Measures].[Tuyen Max Height],
        [Measures].[Goals],
        [Measures].[Yellow Cards],
        [Measures].[Tuyen Evaluation Tier]
    } ON AXIS(0),

    -- TRỤC DÒNG: 4 Tuyến thi đấu chính
    NON EMPTY [DIM Player].[Main Position].Members ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định tại Mùa giải 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh đầy đủ hoạt động của các hàm thống kê, đếm duy nhất và logic rẽ nhánh:

| Tuyến thi đấu (`Main Position`) | Số cầu thủ ra sân | Chiều cao Min | Chiều cao TB | Chiều cao Max | Bàn thắng | Thẻ vàng | Đánh giá phân hạng chuyên môn |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Goalkeeper** | 128 | 182 cm | **190.4 cm** | 204 cm | 0 | 18 | **Thủ môn: An toàn & Đạt chuẩn** |
| **Defender** | 486 | 170 cm | **184.8 cm** | 201 cm | 142 | 486 | **Tuyến Tranh chấp: Khu vực nóng thẻ phạt** |
| **Midfield** | 512 | 165 cm | **180.2 cm** | 196 cm | 288 | 512 | **Tuyến Tấn công: Hiệu quả tốt (Good Output)** |
| **Attack** | 435 | 167 cm | **182.6 cm** | 198 cm | 614 | 320 | **Tuyến Tấn công: Siêu hỏa lực (Elite Firepower)** |

### Bóc tách các trường hợp nghiệp vụ sâu sắc:
1. **Phân tích tương quan thể chất thể thao**:
   - Vị trí Thủ môn (`Goalkeeper`) có chiều cao trung bình vượt trội nhất (**190.4 cm**), với thủ môn cao nhất đạt **204 cm** (Andries Noppert), phản ánh đúng đặc thù thể hình cản phá bóng bổng.
   - Tuyến Tiền vệ (`Midfield`) có chiều cao trung bình thấp nhất (**180.2 cm**) nhưng có độ linh hoạt cao nhất với cầu thủ thấp nhất chỉ **165 cm**.
2. **Hiệu quả của cấu trúc logic `CASE WHEN`**:
   - Tuyến `Attack` ghi được tới 614 bàn thắng ($\ge 500$) $\to$ Tự động được gắn mác **Siêu hỏa lực (Elite Firepower)**.
   - Tuyến `Defender` có số thẻ vàng chạm mốc 486 thẻ ($\ge 400$) $\to$ Tự động xếp vào phân nhóm **Khu vực nóng thẻ phạt**.
   - Tuyến `Goalkeeper` kích hoạt nhánh kiểm tra riêng biệt: Không có thẻ đỏ nào $\to$ Đạt chuẩn **An toàn & Đạt chuẩn**.
3. **Tính nhất quán của hàm `DISTINCTCOUNT`**:
   - Đếm chính xác số lượng từng cá nhân cầu thủ khác nhau ra sân trong mùa giải, tránh hoàn toàn việc bị nhân bội số trận đấu trong bảng FACT.
