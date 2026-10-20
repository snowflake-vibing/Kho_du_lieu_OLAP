# CHƯƠNG 08: ĐẠI SỐ TẬP HỢP & XỬ LÝ KHÔNG GIAN ĐA CHIỀU (SET ALGEBRA)

---

## 1. NỀN TẢNG TOÁN HỌC VỀ ĐẠI SỐ TẬP HỢP TRONG MDX

Trong không gian siêu khối, mọi thao tác gộp, lọc hay kết hợp các chiều phân tích đều được quy về các phép toán đại số tập hợp giữa các **Set** (tập hợp các Tuple). 

```
                               CÁC PHÉP TOÁN ĐẠI SỐ TẬP HỢP CHÍNH
  ┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────────────────┐
  │ 1. CROSSJOIN (*)        │ 2. UNION (+)            │ 3. INTERSECT (∩)        │ 4. EXCEPT (-)           │
  │ Tích Đề-các hai tập hợp │ Hợp nhất hai tập hợp    │ Giao điểm: lấy các phần │ Loại trừ: lấy phần tử   │
  │ {A, B} * {1, 2}         │ {A, B} + {B, C}         │ tử có mặt ở cả hai bên  │ thuộc A nhưng không có  │
  │ = {(A,1),(A,2),(B,1)...}│ = {A, B, C} (DISTINCT)  │ {A, B} ∩ {B, C} = {B}   │ trong B: A \ B          │
  └─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### Quy tắc bất biến về Chiều không gian (Dimensionality Rule)
- Trong phép **`CROSSJOIN`**: Hai tập hợp có thể có chiều không gian khác nhau. Không gian kết quả sẽ là tổng số chiều của cả hai: $\text{Dim}(A \times B) = \text{Dim}(A) + \text{Dim}(B)$.
- Trong phép **`UNION`**, **`INTERSECT`**, **`EXCEPT`**: Hai tập hợp bắt buộc phải có **cùng chiều không gian và cùng trật tự các chiều** (Identical Dimensionality). Nếu vi phạm, trình biên dịch SSAS sẽ báo lỗi nghiêm trọng: *"The sets have different dimensionalities"*.

---

## 2. BẢNG TRA CỨU CÁC HÀM VÀ TOÁN TỬ TẬP HỢP

| Tên hàm | Toán tử rút gọn | Cú pháp đầy đủ | Ý nghĩa nghiệp vụ |
| :--- | :---: | :--- | :--- |
| **`CROSSJOIN`** | `*` | `CROSSJOIN(Set1, Set2)` hoặc `Set1 * Set2` | Nhân không gian: tạo tổ hợp mọi cặp Tuple giữa hai tập hợp. |
| **`UNION`** | `+` | `UNION(Set1, Set2, [ALL / DISTINCT])` | Gộp hai danh sách (mặc định loại bỏ trùng lặp nếu dùng `DISTINCT`). |
| **`INTERSECT`** | - | `INTERSECT(Set1, Set2, [ALL])` | Lọc ra các thực thể thỏa mãn đồng thời hai tiêu chí xếp hạng. |
| **`EXCEPT`** | `-` | `EXCEPT(Set1, Set2, [ALL])` hoặc `Set1 - Set2` | Lấy các phần tử thuộc Set1 và gạt bỏ các phần tử thuộc Set2. |
| **`EXTRACT`** | - | `EXTRACT(Set, Dim1, Dim2, ...)` | Chiếu trích xuất lại một số chiều từ một Set đa chiều phức tạp. |

---

## 3. VÍ DỤ PHỨC TẠP: NHẬN DIỆN CÁC "ĐỘI BÓNG ĐẲNG CẤP TOÀN DIỆN VÀ KỶ LUẬT"

> **Đề bài nghiệp vụ**: Ban tổ chức giải đấu cần xác định danh sách các **Đội bóng ưu tú toàn diện (Elite & Disciplined Clubs)** thỏa mãn đồng thời 3 tiêu chí tập hợp khắt khe:
> 1. Phải nằm trong **Top 8 CLB ghi bàn nhiều nhất trên Sân Nhà** (`Home Goals`).
> 2. Phải nằm đồng thời trong **Top 8 CLB ghi bàn nhiều nhất trên Sân Khách** (`Away Goals`) $\to$ **Ứng dụng phép `INTERSECT`**.
> 3. Nhưng **loại trừ** những CLB có hành vi thi đấu bạo lực (bị phạt từ 4 thẻ đỏ trở lên) $\to$ **Ứng dụng phép `EXCEPT`**.
> 4. Sau đó kết hợp nhân không gian với các thước đo hiệu năng $\to$ **Ứng dụng phép `CROSSJOIN`**.

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Tập hợp Top 8 CLB ghi bàn sân nhà tốt nhất
SET [Top_Home_Scoring_Clubs] AS
    TOPCOUNT(
        [DIM Club].[Club Name].Members,
        8,
        ([DIM Game].[Is Home Game].[1], [Measures].[Goals])
    )

-- 2. Tập hợp Top 8 CLB ghi bàn sân khách tốt nhất
SET [Top_Away_Scoring_Clubs] AS
    TOPCOUNT(
        [DIM Club].[Club Name].Members,
        8,
        ([DIM Game].[Is Home Game].[0], [Measures].[Goals])
    )

-- 3. Phép GIAO TẬP HỢP (INTERSECT): Các CLB công thủ toàn diện cả sân nhà lẫn sân khách
SET [Elite_Balanced_Clubs] AS
    INTERSECT(
        [Top_Home_Scoring_Clubs],
        [Top_Away_Scoring_Clubs]
    )

-- 4. Tập hợp các CLB có lối chơi bạo lực (>= 4 thẻ đỏ trong mùa)
SET [Violent_Clubs] AS
    FILTER(
        [DIM Club].[Club Name].Members,
        [Measures].[Red Cards] >= 4
    )

-- 5. Phép LOẠI TRỪ TẬP HỢP (EXCEPT): Đội bóng ưu tú nhưng phải sạch bóng thẻ đỏ
SET [Elite_Disciplined_Clubs] AS
    EXCEPT(
        [Elite_Balanced_Clubs],
        [Violent_Clubs]
    )

-- 6. Thành viên tính toán: Tỷ lệ bàn thắng Sân khách / Sân nhà
MEMBER [Measures].[Away To Home Ratio] AS
    IIF(
        ([DIM Game].[Is Home Game].[1], [Measures].[Goals]) = 0,
        NULL,
        ([DIM Game].[Is Home Game].[0], [Measures].[Goals]) / ([DIM Game].[Is Home Game].[1], [Measures].[Goals])
    ),
    FORMAT_STRING = '0.00%'

SELECT 
    -- TRỤC CỘT: Các thước đo chi tiết bóc tách sân nhà, sân khách và thẻ phạt
    {
        ([DIM Game].[Is Home Game].[1], [Measures].[Goals]),
        ([DIM Game].[Is Home Game].[0], [Measures].[Goals]),
        [Measures].[Goals],
        [Measures].[Away To Home Ratio],
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON AXIS(0),

    -- TRỤC DÒNG: Danh sách các CLB đã trải qua đầy đủ các phép toán đại số tập hợp
    NON EMPTY [Elite_Disciplined_Clubs] ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định tại Mùa giải 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 4. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh chính xác từng bước lọc của đại số tập hợp:

| Tên câu lạc bộ (`DIM Club Name`) | Bàn thắng Sân nhà | Bàn thắng Sân khách | Tổng bàn thắng | Tỷ lệ Khách / Nhà | Thẻ vàng | Thẻ đỏ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | 51 | 45 | 96 | 88.24% | 52 | 2 |
| **Arsenal FC** | 48 | 43 | 91 | 89.58% | 61 | 2 |
| **Liverpool FC** | 49 | 37 | 86 | 75.51% | 64 | 3 |
| **Real Madrid** | 46 | 41 | 87 | 89.13% | 68 | 2 |
| **FC Bayern Munich** | 53 | 41 | 94 | 77.36% | 49 | 2 |
| **Inter Milan** | 44 | 45 | 89 | 102.27% | 58 | 1 |

### Bóc tách các trường hợp bị loại trừ (Audit Log):
1. **Trường hợp bị loại ở bước `INTERSECT`**:
   - `Aston Villa`: Đứng thứ 5 về ghi bàn sân nhà (48 bàn), nhưng chỉ đứng thứ 14 về ghi bàn sân khách (28 bàn) $\to$ Bị phép toán `INTERSECT` loại bỏ vì chỉ mạnh trên sân nhà.
   - `Paris Saint-Germain`: Đứng thứ 3 về sân khách (44 bàn), nhưng sân nhà chỉ đứng thứ 11 $\to$ Bị `INTERSECT` loại bỏ.
2. **Trường hợp bị loại ở bước `EXCEPT`**:
   - `Chelsea FC`: Thỏa mãn cả 2 tiêu chí Top ghi bàn sân nhà và sân khách, tuy nhiên trong mùa giải nhận tới **5 thẻ đỏ** $\to$ Bị phép `EXCEPT` loại thẳng tay khỏi danh sách vì vi phạm tiêu chuẩn kỷ luật.
3. **Phân tích kết quả tập hợp cuối cùng**:
   - Chỉ có **6 câu lạc bộ trên toàn châu Âu** vượt qua được toàn bộ các phễu lọc đại số tập hợp. Trong đó, `Inter Milan` là đội bóng đặc biệt có số bàn thắng sân khách nhiều hơn sân nhà (Tỷ lệ đạt **102.27%**).
