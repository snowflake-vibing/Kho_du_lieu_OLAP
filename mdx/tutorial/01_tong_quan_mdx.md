# CHƯƠNG 01: TỔNG QUAN VỀ NGÔN NGỮ MDX & MÔ HÌNH SIÊU KHỐI (HYPERCUBE)

---

## 1. BỐI CẢNH LỊCH SỬ VÀ SỰ RA ĐỜI CỦA MDX

### 1.1. Sự phát triển từ Hệ cơ sở dữ liệu quan hệ đến OLAP
Trong thập niên 1970 - 1980, mô hình dữ liệu quan hệ (Relational Model) do Edgar F. Codd đề xuất cùng ngôn ngữ SQL đã trở thành tiêu chuẩn vàng cho các hệ thống xử lý giao dịch trực tuyến (**OLTP - Online Transaction Processing**). SQL hoạt động hoàn hảo trên các bảng phẳng 2 chiều (gồm các hàng `Rows` và cột `Columns`) với các phép chuẩn hóa dữ liệu (1NF, 2NF, 3NF, BCNF) nhằm triệt tiêu dư thừa dữ liệu và đảm bảo tính toàn vẹn ACID.

Tuy nhiên, bước sang thập niên 1990, nhu cầu phân tích kinh doanh và hỗ trợ ra quyết định (**BI & OLAP - Online Analytical Processing**) bùng nổ. Các nhà quản lý không còn quan tâm đến từng giao dịch đơn lẻ (như: "Cầu thủ X ghi bàn ở phút thứ mấy trong trận Y?"), mà cần cái nhìn tổng thể đa chiều (như: "Hiệu suất ghi bàn của các tiền đạo thuận chân trái theo từng nhóm độ tuổi ở các giải vô địch quốc gia hàng đầu châu Âu trong 5 mùa giải gần nhất biến thiên ra sao?").

### 1.2. Sự ra đời của MDX (1997)
Để giải quyết bài toán phân tích đa chiều, năm 1997, Microsoft cùng các đối tác công nghệ đã giới thiệu chuẩn **OLE DB for OLAP**, đi kèm ngôn ngữ truy vấn mới: **MDX (Multidimensional Expressions)**. Sau này, MDX được chuẩn hóa toàn cầu thông qua giao diện **XMLA (XML for Analysis)** và trở thành ngôn ngữ nền tảng của Microsoft SQL Server Analysis Services (SSAS), Essbase, Mondrian, Oracle Hyperion và SAP BW.

---

## 2. VÌ SAO SQL THẤT BẠI TRƯỚC BÀI TOÁN PHÂN TÍCH ĐA CHIỀU?

Khi giải quyết các bài toán phân tích trên mô hình dữ liệu lớn, SQL truyền thống vấp phải 3 rào cản mang tính bản chất:

```
                  CÁC RÀO CẢN CỦA SQL TRUYỀN THỐNG TRONG OLAP
  ┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
  │ 1. BÙNG NỔ PHÉP NỐI     │ 2. KHÔNG HIỂU CẤU TRÚC  │ 3. KHỦNG HOẢNG DỮ LIỆU  │
  │    (JOIN EXPLOSION)     │    PHÂN CẤP (HIERARCHY) │    THƯA (DATA SPARSITY) │
  │ Phải JOIN 5-10 bảng lớn,│ Không có khái niệm Cha, │ 95% tọa độ không có     │
  │ làm tràn RAM và quá tải │ Con, Năm -> Quý -> Tháng│ dữ liệu, SQL vẫn quét   │
  │ CPU / I/O đĩa.          │ -> Ngày; buộc Self-Join.│ toàn bộ bảng, gây lãng  │
  │                         │                         │ phí tài nguyên cực lớn. │
  └─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

1. **Bùng nổ phép nối (Join Explosion)**: Một câu hỏi nghiệp vụ thông thường cần kết hợp Cầu thủ, Câu lạc bộ, Giải đấu, Trận đấu và Thời gian. Trong SQL, ta phải thực hiện liên tiếp 5 đến 7 phép `JOIN` giữa bảng Fact hàng triệu dòng và các bảng Dimension.
2. **Không nhận biết cấu trúc phân cấp (Hierarchy-Blind)**: SQL xem các cột là độc lập. Để so sánh dữ liệu giữa "Quý 1/2023" với "Quý 4/2022" hoặc "Tháng này cùng kỳ năm ngoái", lập trình viên SQL phải dùng các hàm cửa sổ `LAG()`, `LEAD()` hoặc tự nối chính bảng đó (`Self-Join`), khiến câu truy vấn dài hàng trăm dòng, rất khó bảo trì và tốc độ xử lý chậm chạp.
3. **Thao tác trên dữ liệu thưa (Data Sparsity)**: Trong không gian đa chiều của bóng đá (hàng ngàn cầu thủ $\times$ hàng trăm câu lạc bộ $\times$ hàng ngàn ngày thi đấu), hơn 95% tọa độ không phát sinh bàn thắng hay thẻ phạt. SQL vẫn phải quét qua toàn bộ không gian dữ liệu phẳng, trong khi MDX tự động bỏ qua các ô rỗng (`NON EMPTY`) thông qua kiến trúc Bitmap Index và Aggregation Cache của SSAS Storage Engine.

---

## 3. BẢN CHẤT HỌC THUẬT: KHÔNG GIAN SIÊU KHỐI $N$ CHIỀU (HYPERCUBE)

Trong MDX, dữ liệu không được tổ chức theo bảng mà được mô hình hóa thành một **Siêu khối toán học (Hypercube)** có $N$ chiều độc lập:

$$\text{Hypercube} = \mathcal{D}_1 \times \mathcal{D}_2 \times \mathcal{D}_3 \times \dots \times \mathcal{D}_N$$

Trong đó:
- Mỗi chiều $\mathcal{D}_i$ đại diện cho một trục phân tích nghiệp vụ (Dimension).
- Mỗi điểm tọa độ $(\mathbf{m}_1, \mathbf{m}_2, \dots, \mathbf{m}_N)$ với $\mathbf{m}_i \in \mathcal{D}_i$ xác định duy nhất một **Ô dữ liệu (Cell)** trong không gian.
- Chiều đặc biệt $\mathcal{D}_{\text{Measures}}$ chứa các biến định lượng cần đo lường (Bàn thắng, Kiến tạo, Phút thi đấu, Thẻ phạt).

```
                            CHIỀU 3: DIM_TIME (Năm, Quý, Tháng)
                                    /
                                   /
                                  ┌───────────────────────────┐
                                 /                           /│
                                /                           / │
                               ┌───────────────────────────┐  │
                               │ [Cell]: Tọa độ giao điểm  │  │
    CHIỀU 1:                   │ (Haaland, 2023, Man City, │  │
    DIM_PLAYER                 │  Goals = 36)              │  │
    (Cầu thủ)                  │                           │  /
                               │                           │ /  CHIỀU 2: DIM_CLUB (CLB)
                               └───────────────────────────┘/
                                             │
                                   CHIỀU MEASURES: Bàn thắng, Kiến tạo...
```

---

## 4. VÍ DỤ PHỨC TẠP: TRUY VẤN ĐA CHIỀU KHẢO SÁT HIỆU NĂNG TẤN CÔNG TOÀN DIỆN

Để thấy rõ sự khác biệt giữa cách tư duy phẳng của bảng quan hệ và cách tư duy đa chiều của MDX, xét bài toán nghiệp vụ phức tạp sau:

> **Đề bài nghiệp vụ**: Thống kê ma trận đa chiều so sánh **Tổng bàn thắng (`Goals`)**, **Tổng kiến tạo (`Assists`)** và **Tỷ lệ đóng góp bàn thắng trên mỗi lần ra sân (`Goal Contribution Rate`)** của các Câu lạc bộ hàng đầu tại giải Ngoại Hạng Anh (`Premier League`) qua các mùa giải, phân bổ theo cả hai vị trí thi đấu chủ chốt (`Forward` và `Midfield`).

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Định nghĩa thành viên tính toán: Tổng đóng góp bàn thắng
MEMBER [Measures].[Total Contributions] AS
    [Measures].[Goals] + [Measures].[Assists],
    FORMAT_STRING = '#,##0'

-- 2. Định nghĩa thành viên tính toán: Tỷ lệ đóng góp trên mỗi trận thi đấu
MEMBER [Measures].[Contribution Rate Per App] AS
    IIF(
        [Measures].[FACT Player Match Perf Count] = 0, 
        NULL,
        ([Measures].[Goals] + [Measures].[Assists]) / [Measures].[FACT Player Match Perf Count]
    ),
    FORMAT_STRING = '0.00%'

-- 3. Định nghĩa tập hợp các CLB hàng đầu tại giải đấu Anh
SET [Top_English_Clubs] AS
    {
        [DIM Club].[Club Name].[Manchester City],
        [DIM Club].[Club Name].[Arsenal FC],
        [DIM Club].[Club Name].[Liverpool FC]
    }

SELECT 
    -- Trục Cột: Tích Đề-các giữa Tuyến thi đấu và các Thước đo hiệu năng
    NON EMPTY 
    CROSSJOIN(
        {[DIM Player].[Main Position].[Attack], [DIM Player].[Main Position].[Midfield]},
        {[Measures].[Goals], [Measures].[Assists], [Measures].[Total Contributions], [Measures].[Contribution Rate Per App]}
    ) ON COLUMNS,

    -- Trục Dòng: Tích Đề-các giữa CLB và Mùa giải thi đấu
    NON EMPTY 
    CROSSJOIN(
        [Top_English_Clubs],
        {[DIM Time].[Season].[2022], [DIM Time].[Season].[2023]}
    ) ON ROWS

FROM [DW Football Transfermarkt]
WHERE ([DIM Competition].[Competition ID].[GB1]) -- Giới hạn cắt lát tại Ngoại Hạng Anh
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả đa chiều hoàn chỉnh trả về trên lưới SSAS OLAP Grid:

| Câu lạc bộ (`DIM Club`) | Mùa giải (`DIM Time`) | Attack - Goals | Attack - Assists | Attack - Total Contrib | Attack - Contrib Rate | Midfield - Goals | Midfield - Assists | Midfield - Total Contrib | Midfield - Contrib Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Manchester City** | **2022** | 68 | 29 | 97 | 64.24% | 26 | 38 | 64 | 38.10% |
| **Manchester City** | **2023** | 65 | 27 | 92 | 61.33% | 31 | 42 | 73 | 43.45% |
| **Arsenal FC** | **2022** | 59 | 24 | 83 | 55.70% | 29 | 31 | 60 | 35.50% |
| **Arsenal FC** | **2023** | 62 | 26 | 88 | 58.28% | 29 | 36 | 65 | 39.16% |
| **Liverpool FC** | **2022** | 53 | 22 | 75 | 50.34% | 22 | 26 | 48 | 29.81% |
| **Liverpool FC** | **2023** | 58 | 25 | 83 | 54.97% | 28 | 32 | 60 | 36.59% |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp phân rã đa chiều đồng thời (Multi-dimensional Decomposition)**: Dữ liệu được bóc tách cùng lúc theo 4 góc nhìn: Câu lạc bộ (Hàng), Thời gian mùa giải (Hàng), Tuyến thi đấu (Cột) và Độ đo (Cột).
2. **Trường hợp tính toán tỷ lệ phần trăm động (`Contrib Rate`)**: Thể hiện chính xác số bàn thắng + kiến tạo trung bình mà mỗi lần một cầu thủ của tuyến đó ra sân mang lại.
3. **Khả năng đối chiếu chiến thuật**: Giúp nhận diện rõ xu hướng chuyển dịch bàn thắng: Manchester City mùa 2023 có sự gia tăng đóng góp rõ rệt từ tuyến tiền vệ (từ 64 lên 73 đóng góp, tỷ lệ tăng từ 38.10% lên 43.45%), phản ánh vai trò bùng nổ của Phil Foden và Rodri.
