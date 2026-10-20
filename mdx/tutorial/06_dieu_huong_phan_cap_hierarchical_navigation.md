# CHƯƠNG 06: ĐIỀU HƯỚNG PHÂN CẤP & QUAN HỆ CÂY (HIERARCHICAL NAVIGATION)

---

## 1. MÔ HÌNH HÌNH HỌC CÂY PHÂN CẤP TRONG MDX

Một trong những ưu thế tuyệt đối của MDX so với SQL là khả năng định vị và di chuyển tự nhiên giữa các nút trên cây phân cấp dữ liệu mà không cần biết trước khóa chính hay viết các câu lệnh đệ quy (`Recursive CTE`).

```
                              [All Time]  (Cấp độ gốc - Root)
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
                 [2022]                        [2023]  <--- .Parent của [Q1 2023]
                   │                             │
             ┌─────┴─────┐                 ┌─────┴─────┐
             ▼           ▼                 ▼           ▼
           [Q1]         [Q2]             [Q1]         [Q2]  <--- .Siblings với nhau
                                           │
                                     ┌─────┴─────┐
                                     ▼           ▼
                                 [Tháng 1]   [Tháng 2]  <--- .Children của [Q1]
```

---

## 2. BẢNG TỔNG HỢP CÁC HÀM ĐIỀU HƯỚNG CÂY PHÂN CẤP

| Hàm / Thuộc tính | Cú pháp chuẩn | Ý nghĩa hình học & toán học |
| :--- | :--- | :--- |
| **`.Members`** | `Hierarchy.Members` hoặc `Level.Members` | Trả về tập hợp tất cả các phần tử thuộc cây hoặc cấp độ. |
| **`.Children`** | `Member.Children` | Tập hợp các phần tử con trực tiếp cấp dưới (+1 bậc). |
| **`.Parent`** | `Member.Parent` | Phần tử cha trực tiếp cấp trên (-1 bậc). |
| **`.FirstChild`** | `Member.FirstChild` | Phần tử con đầu tiên theo thứ tự định nghĩa. |
| **`.LastChild`** | `Member.LastChild` | Phần tử con cuối cùng theo thứ tự định nghĩa. |
| **`.Siblings`** | `Member.Siblings` | Tập hợp tất cả các anh/chị/em cùng cấp và cùng một cha trực tiếp. |
| **`.FirstSibling`** | `Member.FirstSibling` | Phần tử anh/chị/em đầu tiên cùng cha. |
| **`.LastSibling`** | `Member.LastSibling` | Phần tử anh/chị/em cuối cùng cùng cha. |
| **`.Lag(n)`** | `Member.Lag(n)` | Lùi lại $n$ phần tử cùng cấp độ trên cây. |
| **`.Lead(n)`** | `Member.Lead(n)` | Tiến tới $n$ phần tử cùng cấp độ trên cây. |
| **`Ancestor()`** | `Ancestor(Member, Level / Distance)` | Trả về duy nhất một phần tử tổ tiên ở cấp chỉ định. |
| **`Descendants()`** | `Descendants(Member, Level, [Flags])` | Trả về tập hợp toàn bộ con cháu ở độ sâu bên dưới theo cờ lọc. |

---

## 3. CHUYÊN SÂU HÀM `DESCENDANTS()` VÀ CÁC CỜ LỌC (FLAGS)

Cú pháp: `Descendants(Member, Level_or_Distance, [Flags])`. Các cờ lọc xác định phạm vi lấy nút:

- **`SELF` (Mặc định)**: Chỉ lấy các phần tử tại đúng cấp độ chỉ định.
- **`BEFORE`**: Chỉ lấy các phần tử ở các cấp độ nằm giữa Member gốc và cấp độ chỉ định (không bao gồm Member gốc và cấp chỉ định).
- **`AFTER`**: Lấy các phần tử nằm bên dưới cấp độ chỉ định.
- **`SELF_AND_BEFORE`**: Lấy cả cấp chỉ định và tất cả các cấp trung gian bên trên lên tới Member gốc.
- **`SELF_AND_AFTER`**: Lấy cấp chỉ định và toàn bộ các cấp con cháu sâu hơn bên dưới.
- **`SELF_BEFORE_AFTER`**: Lấy toàn bộ cây gia phả xuất phát từ Member gốc.
- **`LEAVES`**: Chỉ lấy các phần tử lá (Leaf Members - cấp thấp nhất không có con) trong nhánh cây.

```
       Member Gốc: [Năm 2023]
            │
       [Quý 1, Quý 2...]       <--- BEFORE
            │
       [Tháng 1, Tháng 2...]   <--- SELF (nếu Level chỉ định là Month)
            │
       [Ngày 1, Ngày 2...]     <--- AFTER / LEAVES
```

---

## 4. VÍ DỤ PHỨC TẠP: KẾT HỢP ĐIỀU HƯỚNG ĐA TẦNG PHÂN CẤP THỜI GIAN VÀ VỊ TRÍ THI ĐẤU

> **Đề bài nghiệp vụ**: Ban huấn luyện cần theo dõi biểu đồ bàn thắng đa cấp độ trong năm 2023:
> 1. Trục Dòng: Sử dụng hàm `Descendants()` với cờ `SELF_AND_BEFORE` để bóc tách từ **Cấp Năm 2023** $\to$ **Cấp Quý (`Quarter`)** $\to$ **Cấp Tháng (`Month`)** của giải đấu Ngoại Hạng Anh.
> 2. Trục Cột: Lấy toàn bộ các vị trí con chi tiết (`Sub Position`) thuộc tuyến Tiền đạo (`Attack`) bằng thuộc tính `.Children`.
> 3. Thêm một cột đo lường so sánh tỷ lệ bàn thắng của tháng hiện tại so với **Tháng đầu tiên của Quý (`FirstChild`)**.

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Tính số bàn thắng của tháng đầu tiên trong Quý (FirstChild của Quý cha)
MEMBER [Measures].[First Month In Quarter Goals] AS
    ([DIM Time].[Hierarchy].CurrentMember.Parent.FirstChild, [Measures].[Goals]),
    FORMAT_STRING = '#,##0'

-- 2. Tỷ lệ so sánh với tháng đầu quý
MEMBER [Measures].[Ratio Vs First Month] AS
    IIF(
        [Measures].[First Month In Quarter Goals] = 0,
        NULL,
        [Measures].[Goals] / [Measures].[First Month In Quarter Goals]
    ),
    FORMAT_STRING = '0.00%'

SELECT 
    -- TRỤC CỘT: Các vị trí con của tuyến Tấn công kèm các độ đo
    CROSSJOIN(
        [DIM Player].[Position Hierarchy].[Main Position].[Attack].Children,
        {[Measures].[Goals], [Measures].[Ratio Vs First Month]}
    ) ON AXIS(0),

    -- TRỤC DÒNG: Toàn bộ phân cấp thời gian từ Năm -> Quý -> Tháng bằng Descendants
    NON EMPTY 
    Hierarchize(
        Descendants(
            [DIM Time].[Hierarchy].[Year].[2023],
            [DIM Time].[Hierarchy].[Month],
            SELF_AND_BEFORE
        )
    ) ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định tại giải Ngoại Hạng Anh (GB1)
WHERE ([DIM Competition].[Competition ID].[GB1])
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh đầy đủ cây phân cấp được dàn phẳng có thứ bậc:

| Cây Thời Gian (`DIM Time Hierarchy`) | Centre-Forward (Goals) | CF (Ratio Vs M1) | Left Winger (Goals) | LW (Ratio Vs M1) | Right Winger (Goals) | RW (Ratio Vs M1) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **2023 (Cả Năm)** | **318** | - | **194** | - | **182** | - |
| ├── **Q1 2023** | **78** | - | **48** | - | **45** | - |
| │   ├── **Tháng 1** | 24 | 100.00% | 15 | 100.00% | 14 | 100.00% |
| │   ├── **Tháng 2** | 26 | 108.33% | 16 | 106.67% | 15 | 107.14% |
| │   └── **Tháng 3** | 28 | 116.67% | 17 | 113.33% | 16 | 114.29% |
| ├── **Q2 2023** | **85** | - | **52** | - | **49** | - |
| │   ├── **Tháng 4** | 30 | 100.00% | 18 | 100.00% | 17 | 100.00% |
| │   ├── **Tháng 5** | 35 | 116.67% | 22 | 122.22% | 20 | 117.65% |
| │   └── **Tháng 6** | 20 | 66.67% | 12 | 66.67% | 12 | 70.59% |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp mở rộng đa cấp độ (`SELF_AND_BEFORE`)**:
   - Trục dòng đồng thời hiển thị cả phần tử ông bà (`2023`), phần tử cha (`Q1 2023`, `Q2 2023`) và các phần tử cháu chắt (`Tháng 1` $\to$ `Tháng 6`), tạo nên một bảng phân rã Roll-up / Drill-down kinh điển.
2. **Trường hợp điều hướng con cái (`.Children`)**:
   - Tuyến `Attack` tự động phân rã thành đúng 3 vị trí thi đấu thực tế: `Centre-Forward` (Tiền đạo cắm), `Left Winger` (Tiền đạo cánh trái) và `Right Winger` (Tiền đạo cánh phải).
3. **Trường hợp tính toán động theo phần tử đầu tiên (`.Parent.FirstChild`)**:
   - Tại Tháng 1 (tháng đầu Quý 1), tỷ lệ so sánh là $24 / 24 = 100\%$.
   - Tại Tháng 2, số bàn tăng lên 26 bàn $\to$ tỷ lệ đạt $108.33\%$ so với tháng đầu quý.
   - Tại Tháng 6, do mùa giải kết thúc vào đầu tháng 6 nên số trận ít hơn, số bàn sụt giảm còn 20 bàn $\to$ tỷ lệ còn $66.67\%$.
