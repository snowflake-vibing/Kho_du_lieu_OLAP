# CHƯƠNG 09: LỌC DỮ LIỆU & SẮP XẾP (FILTERING & SORTING)

---

## 1. HÀM LỌC ĐIỀU KIỆN `FILTER()` TRONG MDX

Hàm `FILTER(Set, Logical_Expression)` là công cụ mạnh mẽ nhất để tinh lọc các phần tử trong một tập hợp dựa trên các điều kiện số học, chuỗi hoặc logic phức hợp.

```
       TẬP HỢP ĐẦU VÀO                              TẬP HỢP ĐẦU RA
  ┌────────────────────────┐                    ┌────────────────────────┐
  │ Haaland (G: 27, M: 2500)│                    │ Haaland (G: 27, M: 2500)│
  │ Foden   (G: 19, M: 2800)│  ──► FILTER ──►   │ Foden   (G: 19, M: 2800)│
  │ Antony  (G: 1,  M: 1300)│   (G >= 15 AND    └────────────────────────┘
  │ Nunez   (G: 11, M: 2000)│    M >= 2000)     (Antony và Nunez bị loại)
  └────────────────────────┘
```

### 1.1. Cú pháp và các toán tử logic
- **Toán tử so sánh**: `=`, `<>`, `>`, `<`, `>=`, `<=`.
- **Toán tử logic**: `AND`, `OR`, `NOT`.
- **Hàm kiểm tra chuỗi / thuộc tính**: `InStr()`, `VBA!UCase()`, `CurrentMember.Name = '...'`.

### 1.2. Cảnh báo hiệu năng (Performance Optimization)
Hàm `FILTER()` hoạt động bằng cách duyệt qua từng phần tử trong Set tại tầng Formula Engine (FE). Nếu đưa vào một tập hợp gồm 100.000 cầu thủ, câu truy vấn sẽ bị chậm.
- **Giải pháp tối ưu**: Luôn bọc hàm `NonEmpty()` bên trong để loại bỏ các phần tử rỗng ở tầng Storage Engine (SE) trước khi đưa vào hàm `FILTER()`:
  ```mdx
  FILTER(NonEmpty([DIM Player].[Player Name].Members, [Measures].[Goals]), [Measures].[Goals] >= 15)
  ```

---

## 2. CHUYÊN SÂU HÀM `ORDER()`: SẮP XẾP BẢO TỒN PHÂN CẤP VS PHÁ VỠ PHÂN CẤP

Cú pháp: `ORDER(Set, Numeric_or_String_Expression, [ASC | DESC | BASC | BDESC])`.

```
                    SỰ KHÁC NHAU GIỮA DESC VÀ BDESC
     Sắp xếp có thứ bậc (DESC)                 Sắp xếp phá vỡ thứ bậc (BDESC)
  ┌─────────────────────────────────┐        ┌─────────────────────────────────┐
  │ [England] (Tổng: 250 bàn)       │        │ Haaland (Man City - 27 bàn)     │
  │   ├── Haaland    (27 bàn)       │        │ Kane    (Bayern   - 36 bàn)     │
  │   └── Saka       (16 bàn)       │        │ Mbappe  (PSG      - 27 bàn)     │
  │ [Germany] (Tổng: 210 bàn)       │        │ Palmer  (Chelsea  - 22 bàn)     │
  │   ├── Kane       (36 bàn)       │        │ Foden   (Man City - 19 bàn)     │
  │   └── Sane       (8 bàn)        │        │ Saka    (Arsenal  - 16 bàn)     │
  └─────────────────────────────────┘        └─────────────────────────────────┘
  (Kane có 36 bàn vẫn phải đứng sau         (Bỏ qua quốc gia/CLB cha, sắp xếp
   Haaland vì thuộc nhóm [Germany])           phẳng toàn cầu từ cao xuống thấp)
```

### Bảng phân định 4 cờ sắp xếp

| Cờ sắp xếp | Tên tiếng Anh | Cơ chế hoạt động | Ứng dụng thực tế |
| :---: | :--- | :--- | :--- |
| **`ASC`** | Ascending (Hierarchical) | Sắp xếp tăng dần nhưng **giữ nguyên phân cấp cha-con**. | Báo cáo Drill-down thời gian hoặc cơ cấu tổ chức. |
| **`DESC`** | Descending (Hierarchical) | Sắp xếp giảm dần nhưng **giữ nguyên phân cấp cha-con**. | Xếp hạng các chi nhánh trong cùng một vùng miền. |
| **`BASC`** | Break Ascending | **Phá vỡ phân cấp**, sắp xếp phẳng tăng dần trên toàn tập hợp. | Tìm các cầu thủ ít thẻ phạt nhất toàn giải. |
| **`BDESC`** | Break Descending | **Phá vỡ phân cấp**, sắp xếp phẳng giảm dần trên toàn tập hợp. | Xếp hạng Vua phá lưới (Top Scorers), Vua kiến tạo. |

---

## 3. VÍ DỤ PHỨC TẠP: LỌC ĐA TIÊU CHÍ HIỆU SUẤT & ĐỐI CHIẾU TRỰC TIẾP `DESC` VS `BDESC`

> **Đề bài nghiệp vụ**: Ban trinh sát cần tìm kiếm các **"Cầu thủ tấn công hiệu quả cao & kỷ luật tốt"** thỏa mãn đồng thời 3 điều kiện:
> 1. Số bàn thắng (`Goals`) $\ge 12$.
> 2. Đóng góp kiến tạo (`Assists`) $\ge 6$.
> 3. Tỷ lệ thẻ phạt kiểm soát tốt: Không nhận thẻ đỏ nào (`Red Cards = 0`) và Thẻ vàng $\le 5$.
> 4. Hiển thị đối chiếu theo hai cơ cấu: Phân cấp theo Câu lạc bộ (`DESC`) và Xếp hạng phẳng toàn diện (`BDESC`).

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Tính tổng đóng góp bàn thắng (G+A)
MEMBER [Measures].[Total Contributions] AS
    [Measures].[Goals] + [Measures].[Assists],
    FORMAT_STRING = '#,##0'

-- 2. Tập hợp các cầu thủ thỏa mãn bộ lọc đa tiêu chí khắt khe
SET [Filtered_Elite_Attackers] AS
    FILTER(
        NonEmpty(
            [DIM Club].[Club Name].Children * [DIM Player].[Player Name].Children,
            [Measures].[Goals]
        ),
        [Measures].[Goals] >= 12 
        AND [Measures].[Assists] >= 6
        AND [Measures].[Red Cards] = 0
        AND [Measures].[Yellow Cards] <= 5
    )

-- 3. Sắp xếp phá vỡ phân cấp (BDESC) theo Tổng đóng góp G+A
SET [Ranked_Flat_Players] AS
    ORDER(
        [Filtered_Elite_Attackers],
        [Measures].[Total Contributions],
        BDESC
    )

SELECT 
    -- TRỤC CỘT: 5 Thước đo đánh giá chuyên sâu
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Total Contributions],
        [Measures].[Yellow Cards],
        [Measures].[Minutes Played]
    } ON AXIS(0),

    -- TRỤC DÒNG: Danh sách đã lọc và sắp xếp toàn cục
    [Ranked_Flat_Players] ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định tại Mùa giải 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 4. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh chính xác tác dụng của hàm `FILTER` đa điều kiện kết hợp `ORDER(..., BDESC)`:

| Câu lạc bộ (`DIM Club`) | Cầu thủ (`DIM Player`) | Bàn thắng | Kiến tạo | Tổng đóng góp (G+A) | Thẻ vàng | Phút thi đấu |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | **Erling Haaland** | 27 | 7 | **34** | 2 | 2,558 |
| **FC Bayern Munich** | **Harry Kane** | 26 | 8 | **34** | 3 | 2,780 |
| **Manchester City** | **Phil Foden** | 19 | 8 | **27** | 2 | 2,860 |
| **Liverpool FC** | **Mohamed Salah** | 18 | 9 | **27** | 2 | 2,536 |
| **Arsenal FC** | **Bukayo Saka** | 16 | 9 | **25** | 4 | 2,938 |
| **Aston Villa** | **Ollie Watkins** | 17 | 8 | **25** | 4 | 2,980 |
| **Tottenham Hotspur** | **Son Heung-min** | 17 | 7 | **24** | 1 | 2,945 |

### Bóc tách các trường hợp bị loại trừ bởi hàm `FILTER` (Edge Cases Audit):
1. **Trường hợp vi phạm thẻ phạt**:
   - `Nicolas Jackson` (Chelsea): Ghi 14 bàn, 5 kiến tạo $\to$ Bị loại vì nhận **10 thẻ vàng** (vượt ngưỡng $\le 5$).
   - `Darwin Núñez` (Liverpool): Ghi 11 bàn, 8 kiến tạo $\to$ Bị loại vì số bàn thắng chỉ đạt 11 (ngưỡng yêu cầu $\ge 12$).
2. **Trường hợp vi phạm kiến tạo**:
   - `Alexander Isak` (Newcastle): Ghi 21 bàn nhưng chỉ có 2 kiến tạo $\to$ Bị loại vì kiến tạo $< 6$.
3. **Phân tích hiệu quả của cờ `BDESC`**:
   - Các cầu thủ được xếp thẳng theo cột `Total Contributions` từ cao nhất (34) xuống thấp nhất (24), bất kể họ đến từ CLB nào. Nếu dùng `DESC`, Harry Kane sẽ bị đẩy xuống phân nhóm CLB Bayern Munich thay vì xếp ngang hàng trên đỉnh bảng cùng Erling Haaland.
