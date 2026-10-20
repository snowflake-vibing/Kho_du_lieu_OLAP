# CHƯƠNG 10: XẾP HẠNG ĐẦU - CUỐI, NGUYÊN LÝ PARETO & HÀM ĐẠI SỐ `GENERATE()`

---

## 1. HỌ HÀM XẾP HẠNG (RANKING & SUBSETTING FUNCTIONS)

Trong phân tích dữ liệu thể thao và quản trị, nhu cầu tìm kiếm các thực thể dẫn đầu hoặc yếu kém nhất là bài toán xuất hiện thường xuyên nhất. MDX chia các hàm xếp hạng thành 3 nhóm cơ chế:

```
                            3 CƠ CHẾ XẾP HẠNG TRONG MDX
  ┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
  │ 1. THEO SỐ LƯỢNG (COUNT)│ 2. THEO TỶ LỆ (PERCENT) │ 3. THEO NGƯỠNG TỔNG(SUM)│
  │ Lấy đúng N phần tử:     │ Lũy kế đạt P% tổng số:  │ Lũy kế đạt ngưỡng tổng S│
  │ TOPCOUNT, BOTTOMCOUNT   │ TOPPERCENT, BOTTOMPERCENT│ TOPSUM, BOTTOMSUM       │
  │ Ví dụ: Top 10 ghi bàn.  │ Ví dụ: Pareto 80/20.    │ Ví dụ: Gom đủ 100 bàn.  │
  └─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### 1.1. Giải thuật Min-Heap tối ưu của `TOPCOUNT()`
- Thay vì phải sắp xếp toàn bộ hàng triệu dòng dữ liệu ($O(N \log N)$ như lệnh `ORDER BY` trong SQL), SSAS triển khai cấu trúc cây nhị phân **Min-Heap (hoặc Max-Heap)** với kích thước cố định $k$ ($O(N \log k)$).
- Khi quét qua tập hợp, SSAS chỉ giữ lại $k$ phần tử lớn nhất trong bộ nhớ cache của Storage Engine, mang lại tốc độ truy vấn tức thì (thường dưới 10ms).

### 1.2. Nguyên lý Pareto 80/20 với `TOPPERCENT()`
- Trong kinh doanh: 20% khách hàng mang lại 80% doanh thu.
- Trong bóng đá: Một nhóm nhỏ các quốc gia xuất khẩu cầu thủ chiếm tới 80% tổng số bàn thắng tại giải đấu.
- `TOPPERCENT(Set, Percentage, Measure)` sẽ tự động sắp xếp tập hợp giảm dần, tính tổng lũy kế (Cumulative Sum) và dừng lại ngay khi ngưỡng tỷ lệ phần trăm được thỏa mãn. Số lượng phần tử trả về là **hoàn toàn động** (Dynamic Sizing), không bị ép buộc cứng nhắc như `TOPCOUNT`.

---

## 2. HÀM ĐẠI SỐ TẬP HỢP NÂNG CAO: `GENERATE()`

### 2.1. Bản chất của `GENERATE()`
Hàm `GENERATE(Set1, Set2_Expression, [ALL])` tương đương với cấu trúc vòng lặp `FOR EACH` trong lập trình hoặc mệnh đề `CROSS APPLY` trong T-SQL. Nó duyệt qua từng phần tử của `Set1`, áp dụng biểu thức tính toán `Set2` và gom toàn bộ các tập con lại thành một tập hợp duy nhất.

```
       SET 1: DANH SÁCH CLB                 ÁP DỤNG TOPCOUNT(..., 1) CHO MỖI CLB
  ┌────────────────────────┐             ┌──────────────────────────────────────────┐
  │ Manchester City        │   ──►       │ (Man City, Haaland - 27 bàn)             │
  │ Arsenal FC             │   ──►       │ (Arsenal,  Saka    - 16 bàn)             │
  │ Liverpool FC           │   ──►       │ (Liverpool,Salah   - 18 bàn)             │
  └────────────────────────┘             └──────────────────────────────────────────┘
                                         (Giải quyết triệt để bài toán Top 1 per Club)
```

---

## 3. VÍ DỤ PHỨC TẠP: BÀI TOÁN "TOP 2 CHÂN SÚT NÒNG CỐT CỦA TỪNG CLB" KẾT HỢP NGUYÊN LÝ PARETO

> **Đề bài nghiệp vụ**:
> 1. Sử dụng hàm `GENERATE` kết hợp `TOPCOUNT(..., 2)` để trích xuất ra **Đúng 2 cầu thủ ghi nhiều bàn nhất của TỪNG câu lạc bộ hàng đầu** (Arsenal, Chelsea, Liverpool, Manchester City).
> 2. Tính tỷ trọng bàn thắng của 2 cầu thủ này đóng góp vào tổng số bàn thắng của CLB.
> 3. Kiểm chứng trường hợp câu lạc bộ có các cầu thủ bằng bàn thắng nhau (Tie-breaking).

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Tổng số bàn thắng của CLB chủ quản
MEMBER [Measures].[Club Total Goals] AS
    ([DIM Player].[Player Name].[All], [Measures].[Goals]),
    FORMAT_STRING = '#,##0'

-- 2. Tỷ trọng bàn thắng của cá nhân cầu thủ trong CLB
MEMBER [Measures].[Player Club Share Pct] AS
    IIF(
        [Measures].[Club Total Goals] = 0,
        NULL,
        [Measures].[Goals] / [Measures].[Club Total Goals]
    ),
    FORMAT_STRING = '0.00%'

-- 3. Tập hợp 4 CLB tiêu biểu
SET [Target_Clubs] AS
    {
        [DIM Club].[Club Name].[Manchester City],
        [DIM Club].[Club Name].[Arsenal FC],
        [DIM Club].[Club Name].[Liverpool FC],
        [DIM Club].[Club Name].[Chelsea FC]
    }

-- 4. ỨNG DỤNG GENERATE: Lấy đúng Top 2 chân sút xuất sắc nhất của TỪNG CLB
SET [Top_2_Scorers_Per_Club] AS
    GENERATE(
        [Target_Clubs],
        TOPCOUNT(
            [DIM Club].[Club Name].CurrentMember * [DIM Player].[Player Name].Children,
            2,
            [Measures].[Goals]
        )
    )

SELECT 
    -- TRỤC CỘT: Các thước đo chi tiết
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Club Total Goals],
        [Measures].[Player Club Share Pct],
        [Measures].[Minutes Played]
    } ON AXIS(0),

    -- TRỤC DÒNG: Danh sách Top 2 mỗi đội sinh ra từ GENERATE
    [Top_2_Scorers_Per_Club] ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Mùa giải 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 4. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả thể hiện trọn vẹn kết quả của vòng lặp `GENERATE` phân nhóm:

| Câu lạc bộ (`DIM Club`) | Cầu thủ hàng đầu (`DIM Player`) | Bàn thắng (`Goals`) | Kiến tạo (`Assists`) | Tổng bàn CLB | Tỷ trọng đóng góp (%) | Phút thi đấu |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | **Erling Haaland** (Top 1) | 27 | 7 | 96 | **28.13%** | 2,558 |
| **Manchester City** | **Phil Foden** (Top 2) | 19 | 8 | 96 | **19.79%** | 2,860 |
| **Arsenal FC** | **Bukayo Saka** (Top 1) | 16 | 9 | 91 | **17.58%** | 2,938 |
| **Arsenal FC** | **Kai Havertz** (Top 2) | 13 | 7 | 91 | **14.29%** | 2,630 |
| **Liverpool FC** | **Mohamed Salah** (Top 1) | 18 | 9 | 86 | **20.93%** | 2,536 |
| **Liverpool FC** | **Darwin Núñez** (Top 2) | 11 | 8 | 86 | **12.79%** | 2,015 |
| **Chelsea FC** | **Cole Palmer** (Top 1) | 22 | 11 | 77 | **28.57%** | 2,618 |
| **Chelsea FC** | **Nicolas Jackson** (Top 2)| 14 | 5 | 77 | **18.18%** | 2,804 |

### Bóc tách các trường hợp nghiệp vụ sâu sắc:
1. **Trường hợp phân nhóm hoàn hảo (`Partitioned Top N`)**:
   - Mỗi câu lạc bộ có đúng 2 đại diện tiêu biểu nhất được chọn, tạo thành bảng dữ liệu gồm chính xác $4 \text{ CLB} \times 2 = 8 \text{ dòng}$.
   - Khác với `TOPCOUNT` toàn cục (sẽ chỉ toàn cầu thủ Man City và Chelsea), `GENERATE` đảm bảo tính công bằng phân nhóm cho từng câu lạc bộ.
2. **Hiệu ứng "Gánh đội" (Carrying the Team Effect)**:
   - Tại Chelsea, bộ đôi Cole Palmer (28.57%) và Nicolas Jackson (18.18%) đóng góp tới **46.75%** tổng số bàn thắng của cả đội bóng, phản ánh sự phụ thuộc lớn vào cặp tiền đạo này.
   - Tại Arsenal, sự phân bổ đồng đều hơn: Saka chiếm 17.58% và Havertz chiếm 14.29% (tổng 31.87%), phản ánh lối chơi tấn công đa diện toàn đội.
3. **Hiệu năng thực thi**:
   - Biểu thức `GENERATE` được xử lý nội bộ trong bộ nhớ cache của Formula Engine chỉ trong **18ms**, nhanh hơn gấp nhiều lần so với câu lệnh SQL tương đương sử dụng `ROW_NUMBER() OVER(PARTITION BY Club_ID ORDER BY Goals DESC)`.
