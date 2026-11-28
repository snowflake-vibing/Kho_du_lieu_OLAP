# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.4 Câu truy vấn 4

**Nội dung truy vấn:** Khảo sát sự phân bố bàn thắng, kiến tạo và thời lượng thi đấu trung bình mỗi trận theo từng độ tuổi của cầu thủ trong năm 2023 nhằm phân tích chu kỳ phát triển phong độ và thể lực của vận động viên theo độ tuổi thực tế.

---

### 3.10.4.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên để khởi tạo thước đo tính toán số phút thi đấu trung bình:
* ● Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `[Avg Minutes Played]`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
IIF(
    IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
    NULL,
    ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
)
```
Đặt Format String là `#,##0.00`.

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để triển khai cấu trúc thước đo mới lên máy chủ SSAS.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để làm mới cấu trúc, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc năm tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Year.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn năm 2023 rồi nhấp nút OK để xác nhận.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Age, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong khung Metadata, mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo 3 thước đo thả vào khu vực dữ liệu bên cạnh cột Age theo thứ tự gồm: Goals, Assists và Avg Minutes Played.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả phân bố hiệu suất gồm bàn thắng, kiến tạo và số phút trung bình theo từng độ tuổi trong năm 2023.

---

### 3.10.4.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Year, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Age, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm: Goals, Assists và Avg Minutes Played.

**Bước 2:** Thiết lập giá trị cho bộ lọc năm trên trang tính Excel: Tại ô B1 nằm cạnh nhãn Year, nhấp chuột vào nút mũi tên xổ xuống, tích chọn năm 2023 rồi nhấp nút OK.

**Bước 3:** Sắp xếp độ tuổi theo thứ tự tăng dần: Trên trang tính Excel, nhấp chuột phải vào một ô số bất kỳ trong cột Age, di chuột chọn mục Sort rồi nhấp chọn Sort Smallest to Largest.

**Bước 4:** Định dạng hiển thị bảng dạng danh sách phẳng: Trên thanh Ribbon, chọn thẻ Design, tại mục Report Layout nhấp chọn Show in Tabular Form. Bảng PivotTable lúc này hiển thị hoàn chỉnh đúng 3 cột số liệu hiệu suất theo từng độ tuổi từ 17 đến 45 trong năm 2023.

---

### 3.10.4.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu SSAS_Football_Transfermarkt (hoặc DW Football SSAS), mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích khảo sát hiệu suất ghi bàn, kiến tạo và số phút thi đấu trung bình phân theo độ tuổi trong năm 2023. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH MEMBER` định nghĩa động thước đo tính toán `[Measures].[Avg Minutes Played]` tính số phút trung bình mỗi lần ra sân kèm hàm xử lý tránh chia cho 0 `IIF`.
* ● Lựa chọn 3 thước đo `[Measures].[Goals]`, `[Measures].[Assists]` và `[Measures].[Avg Minutes Played]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `FILTER` loại bỏ các độ tuổi rỗng hoặc không hợp lệ trên chiều `[DIM Player].[Age]`, kết hợp hàm `ORDER` với cờ `BASC` để sắp xếp tuổi tăng dần trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn phạm vi tính toán trong năm 2023 `[DIM Time].[Year].[2023]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 04: Hiệu suất bàn thắng, kiến tạo & phút thi đấu theo độ tuổi
   Database: SSAS_Football_Transfermarkt | Cube: [DW Football Transfermarkt]
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

SELECT
    -- Trục Cột COLUMNS: Các chỉ số hiệu suất thi đấu
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các độ tuổi hợp lệ, sắp xếp tăng dần từ 17 đến 45
    ORDER(
        FILTER(
            [DIM Player].[Age].[Age].MEMBERS,
            NOT ISEMPTY([DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE) 
            AND [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE > 0
        ),
        [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE,
        BASC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Năm dương lịch 2023
WHERE (
    [DIM Time].[Year].[2023]
);
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào SSAS_Football_Transfermarkt. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu hiển thị đúng 29 dòng đại diện cho 29 độ tuổi và 3 cột chỉ số hiệu suất.

---

### 3.10.4.4 Kết quả và Nhận xét

Bảng kết quả trả về thực tế đối chiếu từ khối Cube OLAP:

| STT | Độ Tuổi (`Age`) | Tổng Bàn Thắng (`Goals`) | Tổng Kiến Tạo (`Assists`) | Số Phút TB/Trận (`Avg Minutes`) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | **17** | - | - | - |
| **2** | **18** | 0 | 0 | 6.00 |
| **3** | **19** | 1 | 3 | 40.31 |
| **4** | **20** | 24 | 16 | 47.78 |
| **5** | **21** | 46 | 54 | 42.69 |
| **6** | **22** | 127 | 115 | 44.89 |
| **7** | **23** | 298 | 266 | 51.30 |
| **8** | **24** | 447 | 391 | 57.07 |
| **9** | **25** | 672 | 536 | 59.74 |
| **10** | **26** | 865 | 694 | 62.56 |
| **11** | **27** | 838 | 641 | 63.33 |
| **12** | **28** | 948 | 718 | 66.09 |
| **13** | **29** | 1,008 | 776 | 67.72 |
| **14** | **30** | 816 | 582 | 65.17 |
| **15** | **31** | 632 | 471 | 65.28 |
| **16** | **32** | 720 | 561 | 69.87 |
| **17** | **33** | 660 | 484 | 69.45 |
| **18** | **34** | 543 | 403 | 68.92 |
| **19** | **35** | 507 | 316 | 66.56 |
| **20** | **36** | 222 | 198 | 68.58 |
| **21** | **37** | 199 | 139 | 66.51 |
| **22** | **38** | 165 | 126 | 70.28 |
| **23** | **39** | 130 | 80 | 68.85 |
| **24** | **40** | 72 | 41 | 65.41 |
| **25** | **41** | 15 | 13 | 71.21 |
| **26** | **42** | 3 | 2 | 73.11 |
| **27** | **43** | 6 | 5 | 80.28 |
| **28** | **44** | 0 | 0 | 90.00 |
| **29** | **45** | 1 | 1 | 56.80 |

**Nhận xét nghiệp vụ:**
* Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.
* Giai đoạn từ 25 đến 29 tuổi là đỉnh cao năng suất ghi bàn và kiến tạo trong bóng đá chuyên nghiệp.
* Thời lượng thi đấu trung bình mỗi trận tăng dần từ các lứa trẻ (dưới 20 tuổi) và đạt độ chín ổn định trên 65 phút/trận ở các độ tuổi từ 28 đến 35 tuổi.
