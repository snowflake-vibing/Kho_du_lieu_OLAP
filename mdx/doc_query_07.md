# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.7 Câu truy vấn 7

**Nội dung truy vấn:** Xác định nhóm các quốc gia có cầu thủ đóng góp vào 80% tổng số bàn thắng được ghi tại tất cả các giải đấu bóng đá diễn ra trên lãnh thổ Nước Anh Country Name là England. Ứng dụng nguyên lý Pareto 80/20 giúp liên đoàn bóng đá và các câu lạc bộ đánh giá thị trường xuất khẩu cầu thủ chủ lực, phục vụ chiến lược cấp giấy phép lao động và chính sách ngoại binh.

### 3.10.7.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên để khởi tạo 2 thước đo tính toán tổng bàn thắng tại Anh và tỷ lệ phần trăm Pareto:
* ● Thước đo thứ nhất: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `England Total Goals`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All], [DIM Competition].[Country Name].[England])
```
* ● Thước đo thứ hai: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Pct Of England Goals`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
IIF([Measures].[England Total Goals] = 0, NULL, [Measures].[Goals] / [Measures].[England Total Goals])
```
Đặt Format String là `0.00%`.

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để đồng bộ cấu trúc mới vào máy chủ SSAS.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để nhận cấu trúc mới, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc quốc gia giải đấu tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Competition.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Country Name.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn England rồi nhấp nút OK để xác nhận.

**Bước 5:** Thiết lập điều kiện lọc Top 80% Pareto quốc tịch cầu thủ tại dòng thứ hai trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Country Of Citizenship.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.
* ● Trong cửa sổ Expression Builder, dán biểu thức TOPPERCENT để lọc các quốc gia chiếm 80% bàn thắng:
```mdx
TOPPERCENT(
    NONEMPTY(
        [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
        ([Measures].[Goals], [DIM Competition].[Country Name].[England])
    ),
    80,
    [Measures].[Goals]
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 6:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Country Of Citizenship, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong khung Metadata, mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo các thước đo thả vào khu vực dữ liệu bên cạnh cột Country Of Citizenship theo thứ tự gồm Goals và Pct Of England Goals.

**Bước 7:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả danh sách 18 quốc gia đóng góp 80% tổng số bàn thắng tại Nước Anh.

---

### 3.10.7.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Competition, nhấp giữ chuột trái vào trường Country Name, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Country Of Citizenship, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Goals và Pct Of England Goals.

**Bước 2:** Thiết lập giá trị cho bộ lọc quốc gia giải đấu: Tại ô B1 nằm cạnh nhãn Country Name trên trang tính, nhấp chuột vào nút mũi tên xổ xuống, tích chọn England rồi nhấp nút OK.

**Bước 3:** Cấu hình bộ lọc Pareto 80%:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Country Of Citizenship.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Trong hộp thoại Top 10 Filter xuất hiện, đổi ô thứ nhất sang Top, nhập số 80 vào ô thứ hai, tại ô thứ ba chọn Percent theo thước đo Sum of Goals rồi nhấp nút OK để áp dụng.

**Bước 4:** Sắp xếp giảm dần theo số bàn thắng: Nhấp chuột phải vào một ô số bất kỳ trong cột Goals, di chuột chọn mục Sort rồi nhấp chọn Sort Largest to Smallest.

**Bước 5:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh danh sách 18 quốc gia dẫn đầu chiếm 80% tổng số bàn thắng tại giải đấu ở Anh.

---

### 3.10.7.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu ở Anh. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH MEMBER` định nghĩa `[Measures].[England Total Goals]` cố định cấp All làm mẫu số và `[Measures].[Pct Of England Goals]` tính tỷ lệ phần trăm đóng góp.
* ● Lựa chọn 2 thước đo hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `TOPPERCENT` lấy các quốc gia đạt ngưỡng 80% số bàn thắng trên trục hàng ROWS, kết hợp hàm `ORDER` với cờ `BDESC` để sắp xếp giảm dần.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn trong giải đấu ở Nước Anh `[DIM Competition].[Country Name].[England]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 07: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu ở Anh
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tổng số bàn thắng của toàn bộ giải đấu tại Anh cố định cấp All làm mẫu số
    MEMBER [Measures].[England Total Goals] AS
        (
            [Measures].[Goals],
            [DIM Player].[Country Of Citizenship].[All],
            [DIM Competition].[Country Name].[England]
        )

    -- 2. Tỷ lệ phần trăm đóng góp bàn thắng của từng quốc gia
    MEMBER [Measures].[Pct Of England Goals] AS
        IIF(
            ISEMPTY([Measures].[England Total Goals]) OR [Measures].[England Total Goals] = 0,
            NULL,
            [Measures].[Goals] / [Measures].[England Total Goals]
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột COLUMNS: Tổng số bàn thắng và Tỷ lệ phần trăm đóng góp
    {
        [Measures].[Goals],
        [Measures].[Pct Of England Goals]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các quốc gia chiếm 80% tổng số bàn thắng, xếp giảm dần
    ORDER(
        TOPPERCENT(
            NONEMPTY(
                EXCEPT(
                    [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                    { [DIM Player].[Country Of Citizenship].[All] }
                ),
                (
                    [Measures].[Goals],
                    [DIM Competition].[Country Name].[England]
                )
            ),
            80,
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt Slicer Axis: Các giải đấu diễn ra tại Nước Anh
WHERE (
    [DIM Competition].[Country Name].[England]
);
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về danh sách 18 quốc gia dẫn đầu chiếm 80.32% tổng số bàn thắng.

---

### 3.10.7.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Quốc Tịch `Country Of Citizenship` | Tổng Bàn Thắng `Goals` | Tỷ Lệ Đóng Góp `Pct Of England Goals` |
| :---: | :--- | :---: | :---: |
| **1** | **England** | **714** | 31.93% |
| **2** | **Brazil** | **194** | 8.68% |
| **3** | **Norway** | **91** | 4.07% |
| **4** | **France** | **89** | 3.98% |
| **5** | **Portugal** | **86** | 3.85% |
| **6** | **Argentina** | **79** | 3.53% |
| **7** | **Germany** | **54** | 2.42% |
| **8** | **Belgium** | **53** | 2.37% |
| **9** | **Netherlands** | **52** | 2.33% |
| **10** | **Denmark** | **51** | 2.28% |
| **11** | **Spain** | **51** | 2.28% |
| **12** | **Sweden** | **48** | 2.15% |
| **13** | **Jamaica** | **44** | 1.97% |
| **14** | **Korea, South** | **42** | 1.88% |
| **15** | **Scotland** | **39** | 1.74% |
| **16** | **Egypt** | **37** | 1.65% |
| **17** | **Nigeria** | **37** | 1.65% |
| **18** | **Ghana** | **35** | 1.57% |
