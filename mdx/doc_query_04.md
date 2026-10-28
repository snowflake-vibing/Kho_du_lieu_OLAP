# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.4 Câu truy vấn 4

**Nội dung truy vấn:** Khảo sát sự phân bố bàn thắng, kiến tạo và thời lượng thi đấu trung bình mỗi trận theo từng độ tuổi của cầu thủ trong năm 2023, đồng thời phân loại cầu thủ theo 3 giai đoạn sự nghiệp gồm lứa trẻ dưới 21 tuổi, độ tuổi đỉnh cao từ 22 đến 29 tuổi và lão tướng từ 30 tuổi trở lên nhằm phân tích chu kỳ phát triển phong độ của vận động viên.

### 3.10.4.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên để khởi tạo 2 thước đo tính toán phân loại độ tuổi và số phút thi đấu trung bình:
* ● Thước đo thứ nhất: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Avg Minutes Played`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
IIF([Measures].[FACT Player Match Perf Count] = 0, NULL, [Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count])
```
* ● Thước đo thứ hai: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Career Stage Group`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức phân loại giai đoạn sự nghiệp:
```mdx
CASE 
    WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBER_VALUE <= 21 THEN "U21 Young Talent"
    WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBER_VALUE <= 29 THEN "Prime Age 22-29"
    ELSE "Veteran 30+"
END
```

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để triển khai cấu trúc các thước đo mới lên máy chủ SSAS.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để làm mới cấu trúc, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc năm tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Year.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn năm 2023 rồi nhấp nút OK để xác nhận.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Age, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong khung Metadata, mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo các thước đo thả vào khu vực dữ liệu bên cạnh cột Age theo thứ tự gồm Career Stage Group, Goals, Assists và Avg Minutes Played.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả phân bố hiệu suất và phân nhóm sự nghiệp theo từng độ tuổi trong năm 2023.

---

### 3.10.4.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Year, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Age, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Career Stage Group, Goals, Assists và Avg Minutes Played.

**Bước 2:** Thiết lập giá trị cho bộ lọc năm trên trang tính Excel: Tại ô B1 nằm cạnh nhãn Year, nhấp chuột vào nút mũi tên xổ xuống, tích chọn năm 2023 rồi nhấp nút OK.

**Bước 3:** Sắp xếp độ tuổi theo thứ tự tăng dần: Trên trang tính Excel, nhấp chuột phải vào một ô số bất kỳ trong cột Age, di chuột chọn mục Sort rồi nhấp chọn Sort Smallest to Largest.

**Bước 4:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh thể hiện sự phân bổ các chỉ số bàn thắng, kiến tạo, số phút thi đấu trung bình và nhóm giai đoạn sự nghiệp theo độ tuổi từ trẻ đến lão tướng trong năm 2023.

---

### 3.10.4.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích khảo sát hiệu suất ghi bàn, kiến tạo và số phút thi đấu trung bình phân theo độ tuổi trong năm 2023. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH MEMBER` định nghĩa động hai thước đo tính toán gồm `[Measures].[Avg Minutes Played]` tính số phút trung bình mỗi lần ra sân kèm hàm xử lý tránh chia cho 0, và `[Measures].[Career Stage Group]` sử dụng cấu trúc `CASE WHEN` phân loại 3 nhóm tuổi sự nghiệp.
* ● Lựa chọn 4 thước đo `[Measures].[Career Stage Group]`, `[Measures].[Goals]`, `[Measures].[Assists]` và `[Measures].[Avg Minutes Played]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `FILTER` loại bỏ các độ tuổi rỗng hoặc không hợp lệ trên chiều `[DIM Player].[Age]`, kết hợp hàm `ORDER` với cờ `BASC` để sắp xếp tuổi tăng dần trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn phạm vi tính toán trong năm 2023 `[DIM Time].[Year].[2023]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 04: Hiệu suất bàn thắng, kiến tạo và phút thi đấu theo độ tuổi
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tính số phút trung bình mỗi lần ra sân
    MEMBER [Measures].[Avg Minutes Played] AS
        IIF(
            IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
            NULL,
            ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
        ),
        FORMAT_STRING = "#,##0.00"

    -- 2. Phân loại giai đoạn sự nghiệp bằng CASE WHEN
    MEMBER [Measures].[Career Stage Group] AS
        CASE 
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 21 THEN "U21 Young Talent"
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 29 THEN "Prime Age 22-29"
            ELSE "Veteran 30+"
        END

SELECT
    -- Trục Cột COLUMNS: Các chỉ số hiệu suất và phân loại nhóm tuổi
    {
        [Measures].[Career Stage Group],
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các độ tuổi hợp lệ, sắp xếp tăng dần từ 16 đến 42
    ORDER(
        FILTER(
            [DIM Player].[Age].[Age].MEMBERS,
            NOT ISEMPTY([DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE) 
            AND [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE > 0
        ),
        [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE,
        BASC
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt Slicer Axis: Năm dương lịch 2023
WHERE (
    [DIM Time].[Year].[2023]
);
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu phân tích chi tiết hiệu suất thi đấu theo từng độ tuổi trong năm 2023, từ lứa tuổi 17 đến 38.

---

### 3.10.4.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| Độ Tuổi `Age` | Phân Khúc Sự Nghiệp `Career Stage` | Tổng Bàn Thắng `Goals` | Tổng Kiến Tạo `Assists` | Số Phút Trung Bình Một Trận `Avg Minutes Played` |
| :---: | :--- | :---: | :---: | :---: |
| **17** | U21 Young Talent | 0 | 0 | 0.00 |
| **18** | U21 Young Talent | 0 | 0 | 6.00 |
| **19** | U21 Young Talent | 1 | 3 | 40.31 |
| **20** | U21 Young Talent | 24 | 16 | 47.78 |
| **21** | U21 Young Talent | 46 | 54 | 42.69 |
| **22** | Prime Age 22-29 | 127 | 115 | 44.89 |
| **23** | Prime Age 22-29 | 298 | 266 | 51.30 |
| **24** | Prime Age 22-29 | 447 | 391 | 57.07 |
| **25** | Prime Age 22-29 | 672 | 536 | 59.74 |
| **26** | Prime Age 22-29 | 865 | 694 | 62.56 |
| **27** | Prime Age 22-29 | 838 | 641 | 63.33 |
| **28** | Prime Age 22-29 | 948 | 718 | 66.09 |
| **29** | Prime Age 22-29 | 1008 | 776 | 67.72 |
| **30** | Veteran 30+ | 816 | 582 | 65.17 |
| **35** | Veteran 30+ | 507 | 316 | 66.56 |
| **38** | Veteran 30+ | 165 | 126 | 70.28 |
