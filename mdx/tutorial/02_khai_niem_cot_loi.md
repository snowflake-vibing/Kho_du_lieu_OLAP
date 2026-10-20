# CHƯƠNG 02: 8 KHÁI NIỆM CỐT LÕI TRONG MÔ HÌNH ĐA CHIỀU (CORE CONCEPTS)

---

## 1. HỆ THỐNG CÁC THỰC THỂ CỐT LÕI CỦA KHỐI ĐA CHIỀU

Trong phân tích OLAP, mọi câu truy vấn MDX đều được xây dựng dựa trên 8 thực thể hình học và toán học cơ bản. Việc nắm vững mối quan hệ giữa các thực thể này là điều kiện tiên quyết để viết đúng và tối ưu mã MDX.

```
                  ┌──────────────────────────────────────────────────┐
                  │                 CUBE (Khối)                      │
                  │        [DW Football Transfermarkt]               │
                  └────────────────────────┬─────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         │                                                                   │
         ▼                                                                   ▼
┌─────────────────────────────────┐                         ┌─────────────────────────────────┐
│     DIMENSIONS (Chiều dữ liệu)   │                         │       MEASURES (Thước đo)       │
│  [DIM Player], [DIM Club],...   │                         │  [Goals], [Assists], [Cards]    │
└────────────────┬────────────────┘                         └────────────────┬────────────────┘
                 │                                                           │
                 ▼                                                           │
┌─────────────────────────────────┐                                          │
│     HIERARCHIES (Cây phân cấp)  │                                          │
│   Year -> Quarter -> Month      │                                          │
└────────────────┬────────────────┘                                          │
                 │                                                           │
                 ▼                                                           │
┌─────────────────────────────────┐                                          │
│         LEVELS (Cấp độ)         │                                          │
│     [Year], [Quarter], [Month]  │                                          │
└────────────────┬────────────────┘                                          │
                 │                                                           │
                 ▼                                                           │
┌─────────────────────────────────┐                                          │
│        MEMBERS (Phần tử)        │                                          │
│   [2023], [Erling Haaland]      │                                          │
└────────────────┬────────────────┘                                          │
                 │                                                           │
                 └─────────────────────────┬─────────────────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │    TUPLE (Bộ tọa độ)│
                                │ (Haaland, 2023, G)  │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │   SET (Tập hợp bộ)  │
                                │  { Tuple1, Tuple2 } │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │  CELL (Ô dữ liệu)   │
                                │    Giá trị: "36"    │
                                └─────────────────────┘
```

---

## 2. ĐỊNH NGHĨA CHI TIẾT TỪNG THỰC THỂ

### 2.1. Cube (Khối dữ liệu)
Là không gian lưu trữ và xử lý đa chiều tập trung, đóng gói toàn bộ bảng sự kiện (`FACT`) và các bảng chiều (`DIM`).
- **Tên trong dự án**: `[DW Football Transfermarkt]`.
- **Đặc trưng**: Chứa toàn bộ các quan hệ phân cấp, tiền tính toán (aggregations) và các phân vùng dữ liệu vật lý (partitions).

### 2.2. Dimension (Chiều dữ liệu)
Đại diện cho danh mục các thực thể nghiệp vụ dùng để lọc, cắt lát hoặc nhóm dữ liệu.
- Trong dự án bóng đá gồm 5 Dimension chính:
  1. `[DIM Player]`: Chiều Cầu thủ (Cá nhân, Quốc tịch, Vị trí, Chân thuận, Độ tuổi, Chiều cao).
  2. `[DIM Club]`: Chiều Câu lạc bộ (Tên đội bóng, Huấn luyện viên, Sân vận động, Quy mô đội hình).
  3. `[DIM Competition]`: Chiều Giải đấu (Tên giải, Quốc gia tổ chức, Loại giải đấu).
  4. `[DIM Game]`: Chiều Trận đấu (Vòng đấu, Mùa giải, Đội nhà, Đội khách, Bàn thắng mỗi đội).
  5. `[DIM Time]`: Chiều Thời gian (Ngày, Tháng, Quý, Năm, Ngày trong tuần).

### 2.3. Hierarchy (Cây phân cấp) & Level (Cấp độ)
Một chiều có thể có một hoặc nhiều Hierarchy. Mỗi Hierarchy gồm nhiều Level sắp xếp theo trật tự bao hàm từ tổng quan đến chi tiết:
- **Cây phân cấp thời gian chuẩn**:
  `[DIM Time].[Hierarchy].[All]` $\to$ `[Year]` $\to$ `[Quarter]` $\to$ `[Month]` $\to$ `[Full Date]`.
- **Cây phân cấp vị trí thi đấu**:
  `[DIM Player].[Position Hierarchy].[All]` $\to$ `[Main Position]` $\to$ `[Sub Position]`.

### 2.4. Member (Phần tử) & All Member
Member là một giá trị dữ liệu cụ thể tại một Level.
- **Member lá (Leaf Member)**: Là phần tử ở cấp thấp nhất, không có con. *Ví dụ*: `[DIM Time].[Full Date].[2023-05-21]`.
- **Member trung gian (Non-leaf Member)**: Chứa các phần tử con. *Ví dụ*: `[DIM Time].[Quarter].[Q2 2023]`.
- **Member gốc (`[All]`)**: Phần tử mặc định đại diện cho tổng cộng của toàn bộ chiều (Ví dụ: `[DIM Player].[All Players]`).

### 2.5. Measure (Độ đo) & Measure Group
Là các đại lượng số học được tổng hợp từ các cột trong bảng FACT. Mọi Measure đều thuộc về chiều đặc biệt `[Measures]`.
- *Ví dụ*: `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Minutes Played]`, `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`.

### 2.6. Tuple (Bộ tọa độ điểm)
Một **Tuple** là một vector tọa độ xác định chính xác một điểm trong không gian đa chiều.
- **Quy tắc toán học**: Một Tuple được bao trong dấu ngoặc tròn `(...)`. Mỗi chiều chỉ được xuất hiện **tối đa một lần** trong một Tuple.
- *Hợp lệ*: `([DIM Player].[Player Name].[Erling Haaland], [DIM Time].[Year].[2023], [Measures].[Goals])`
- *Không hợp lệ*: `([DIM Player].[Player Name].[Erling Haaland], [DIM Player].[Player Name].[Bukayo Saka])` $\to$ **LỖI!** Vì chứa 2 Member cùng thuộc chiều Player.

### 2.7. Set (Tập hợp các bộ tọa độ)
Một **Set** là một tập hợp các Tuple có **cùng chiều không gian và cùng thứ tự cấu trúc** (Dimensionality).
- **Quy tắc toán học**: Một Set được bao trong dấu ngoặc nhọn `{...}`.
- *Hợp lệ*:
  ```mdx
  {
      ([DIM Player].[Main Position].[Attack], [Measures].[Goals]),
      ([DIM Player].[Main Position].[Midfield], [Measures].[Goals])
  }
  ```
- *Không hợp lệ*: `{ ([DIM Player].[Main Position].[Attack]), ([DIM Club].[Club Name].[Arsenal FC]) }` $\to$ **LỖI!** Hai Tuple không cùng chiều không gian.

### 2.8. Cell (Ô dữ liệu)
Là giá trị số học cụ thể nằm tại giao điểm của một Tuple đầy đủ chứa một Measure. Nếu một chiều không được chỉ định rõ trong Tuple, SSAS sẽ tự động lấy Member mặc định (thường là Member `[All]`).

---

## 3. VÍ DỤ PHỨC TẠP: MINH HỌA ĐẦY ĐỦ 8 KHÁI NIỆM TRONG MỘT TRUY VẤN

Để kiểm chứng toàn bộ 8 khái niệm trên, xét một truy vấn phức tạp kết hợp Tuple, Set, Level, Hierarchy, Member `[All]`, Calculated Measure và xử lý ô rỗng:

> **Đề bài nghiệp vụ**: Thống kê so sánh hiệu năng của hai siêu tiền đạo **Erling Haaland** và **Kylian Mbappé** trong năm 2023 trên 3 phương diện:
> 1. Số bàn thắng thực tế (`Goals`).
> 2. Tỷ trọng bàn thắng của cầu thủ đó đóng góp vào **Tổng số bàn thắng của toàn bộ cầu thủ trên toàn thế giới (`[All Players]`)**.
> 3. Tỷ trọng bàn thắng của cầu thủ so với **Tổng bàn thắng của riêng CLB chủ quản của họ**.

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Tính tổng bàn thắng toàn cầu (Sử dụng Member [All])
MEMBER [Measures].[Global Total Goals] AS
    ([DIM Player].[Player Name].[All], [Measures].[Goals]),
    FORMAT_STRING = '#,##0'

-- 2. Tỷ trọng đóng góp toàn cầu
MEMBER [Measures].[Global Goal Share] AS
    IIF(
        [Measures].[Global Total Goals] = 0, 
        NULL,
        [Measures].[Goals] / [Measures].[Global Total Goals]
    ),
    FORMAT_STRING = '0.000%'

-- 3. Bàn thắng tổng cộng của CLB chủ quản tương ứng
MEMBER [Measures].[Club Total Goals] AS
    ([DIM Player].[Player Name].[All], [Measures].[Goals]),
    FORMAT_STRING = '#,##0'

-- 4. Tỷ trọng đóng góp cho riêng CLB
MEMBER [Measures].[Club Goal Share] AS
    IIF(
        ([DIM Player].[Player Name].[All], [Measures].[Goals]) = 0, 
        NULL,
        [Measures].[Goals] / ([DIM Player].[Player Name].[All], [Measures].[Goals])
    ),
    FORMAT_STRING = '0.00%'

-- 5. Định nghĩa Set gồm 2 Tuple phức tạp đa chiều
SET [Selected_Strikers_Tuples] AS
    {
        ([DIM Club].[Club Name].[Manchester City], [DIM Player].[Player Name].[Erling Haaland]),
        ([DIM Club].[Club Name].[Paris Saint-Germain], [DIM Player].[Player Name].[Kylian Mbappé]),
        ([DIM Club].[Club Name].[Arsenal FC], [DIM Player].[Player Name].[Bukayo Saka]),
        ([DIM Club].[Club Name].[Real Madrid], [DIM Player].[Player Name].[Vinicius Junior])
    }

SELECT 
    -- Trục Cột: Tập hợp các Measure gốc và Measure tính toán
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Club Total Goals],
        [Measures].[Club Goal Share],
        [Measures].[Global Goal Share]
    } ON COLUMNS,

    -- Trục Dòng: Tập hợp các Tuple 2 chiều (CLB x Cầu thủ)
    NON EMPTY [Selected_Strikers_Tuples] ON ROWS

FROM [DW Football Transfermarkt]
-- Trục cắt lát (Slicer Tuple): Cố định tại Năm 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```

---

## 4. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là bảng kết quả hiển thị ma trận ô dữ liệu (Cellset) phản ánh đầy đủ các trường hợp:

| Câu lạc bộ (`DIM Club`) | Cầu thủ (`DIM Player`) | Bàn thắng (`Goals`) | Kiến tạo (`Assists`) | Tổng bàn CLB (`Club Goals`) | Tỷ trọng CLB (`Club Share`) | Tỷ trọng Toàn cầu (`Global Share`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | **Erling Haaland** | 44 | 11 | 148 | 29.73% | 0.462% |
| **Paris Saint-Germain** | **Kylian Mbappé** | 42 | 9 | 125 | 33.60% | 0.441% |
| **Arsenal FC** | **Bukayo Saka** | 18 | 14 | 102 | 17.65% | 0.189% |
| **Real Madrid** | **Vinicius Junior** | 23 | 19 | 119 | 19.33% | 0.241% |
| **Manchester City** | **[All Players] (Tổng)** | 148 | 98 | 148 | 100.00% | 1.554% |
| **Paris Saint-Germain** | **[All Players] (Tổng)** | 125 | 82 | 125 | 100.00% | 1.312% |

### Giải thích chi tiết các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp Tuple đa chiều kết hợp**: Mỗi dòng là một Tuple kết hợp giữa một Member của `[DIM Club]` và một Member của `[DIM Player]`.
2. **Trường hợp Member `[All]` chuyển ngữ cảnh**: Tại thước đo `[Club Total Goals]`, tọa độ cầu thủ được giải phóng về `[DIM Player].[Player Name].[All]`, trong khi tọa độ CLB vẫn giữ nguyên (Manchester City = 148 bàn), cho phép tính toán tỷ lệ đóng góp của riêng Haaland đạt xấp xỉ **29.73%**.
3. **Trường hợp Member `[All]` cấp toàn cục**: Tại thước đo `[Global Goal Share]`, mẫu số là tổng số bàn thắng của toàn bộ các cầu thủ trong năm 2023 trên toàn thế giới (~9.520 bàn), chỉ ra rằng một mình Haaland đã chiếm tới **0.462%** tổng số bàn thắng toàn cầu.
4. **Trường hợp ô rỗng và an toàn toán học**: Sử dụng hàm `IIF` kiểm tra mẫu số khác 0 tránh lỗi chia cho 0 (`#DIV/0!`), bảo đảm toàn vẹn dữ liệu cho mọi Cell trong ma trận.
