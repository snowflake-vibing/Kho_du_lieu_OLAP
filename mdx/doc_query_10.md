# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.10 Câu truy vấn 10

**Nội dung truy vấn:** Phân tích biến động số bàn thắng và tốc độ tăng trưởng qua từng quý của 10 câu lạc bộ có tổng số bàn thắng cao nhất châu Âu trong năm 2023 nhằm đánh giá tính ổn định về phong độ của các đội bóng lớn qua các giai đoạn trong năm.

### 3.10.10.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên. Nếu trước đó đã tạo `Prev_Quarter_Goals` và `QoQ_Goals_Growth` theo hướng dẫn cũ thì nhấp chuột phải vào từng thước đo trong Script Organizer, chọn Delete để xóa cả hai (bản cũ gọi `[Prev Quarter Goals]` có dấu cách, không khớp tên thật có gạch dưới nên Excel báo `#VALUE!`, Browser báo `(null)`). Sau đó khởi tạo **duy nhất một** thước đo tự chủ:
* ● Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `[QoQ Goals Growth]`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập nguyên văn biểu thức:
```mdx
IIF(
    [DIM Time].[Hierarchy].CURRENTMEMBER.LEVEL IS [DIM Time].[Hierarchy].[Quarter]
    AND [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT
    AND NOT ISEMPTY(([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
    AND ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER) <> 0,
    ([Measures].[Goals] - ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
        / ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER),
    NULL
)
```
Đặt Format String là `"0.00%"`.

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để đồng bộ cấu trúc mới vào máy chủ SSAS.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để nhận cấu trúc mới, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc năm tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Year.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn năm 2023 rồi nhấp nút OK để xác nhận.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Club, nhấp giữ chuột trái vào thuộc tính Club Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Mở rộng thư mục chiều DIM Time, mở rộng phân cấp Hierarchy, tìm cấp độ Quarter, nhấp giữ chuột trái kéo thả vào lưới ngay bên phải cột Club Name (Cube Browser chỉ hiển thị dạng danh sách phẳng, không xoay được lên cột).
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo các thước đo Goals và QoQ Goals Growth thả vào vùng dữ liệu.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới hiển thị các dòng `Club Name | Quarter | Goals | QoQ Goals Growth`. Dòng Quarter 1 có QoQ trống là đúng bản chất vì không có quý liền trước trong năm 2023; các dòng Quarter 2, 3, 4 của 10 câu lạc bộ trong bảng nhận xét phải khớp từng con số (ví dụ Manchester City: 30, 37 và 23.33%, 20 và -45.95%, 42 và 110.00%).

---

### 3.10.10.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Year, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Time, mở rộng phân cấp Hierarchy, nhấp giữ chuột trái vào trường Quarter, kéo chuột xuống phía dưới và thả vào ô Columns.
* ● Mở rộng thư mục DIM Club, nhấp giữ chuột trái vào trường Club Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Goals và QoQ Goals Growth.

**Bước 2:** Thiết lập giá trị cho bộ lọc năm: Tại ô B1 nằm cạnh nhãn Year trên trang tính, nhấp chuột vào nút mũi tên xổ xuống, tích chọn năm 2023 rồi nhấp nút OK.

**Bước 3:** Thiết lập bộ lọc Top 10 câu lạc bộ:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Club Name.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Trong hộp thoại Top 10 Filter xuất hiện, thiết lập Top 10 theo trường Sum of Goals rồi nhấp nút OK để áp dụng.

**Bước 4:** Loại bỏ cột Quý 1 QoQ Goals Growth bị rỗng:
* ● Do Quý 1 là quý khởi đầu năm 2023 nên không có quý liền trước để tính tăng trưởng, dẫn đến toàn bộ cột QoQ Goals Growth của Quý 1 mang giá trị rỗng NULL.
* ● Trên trang tính Excel, người dùng nhấp chuột phải vào ô tiêu đề cột QoQ Goals Growth bên dưới Quý 1 rồi chọn lệnh Hide để ẩn cột rỗng này đi.
* ● Bảng PivotTable lúc này hiển thị hoàn chỉnh đúng 7 cột số liệu thực tế sạch đẹp, gồm số bàn thắng Quý 1 cùng số bàn thắng và tỷ lệ tăng trưởng QoQ của 3 Quý tiếp theo gồm Quý 2, Quý 3 và Quý 4.

---

### 3.10.10.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích phân tích tăng trưởng bàn thắng theo Quý QoQ của Top 10 CLB Châu Âu năm 2023. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH MEMBER` định nghĩa duy nhất `[Measures].[QoQ Goals Growth]` với công thức giống hệt tab Calculations: tự lấy bàn thắng quý liền trước bằng `PREVMEMBER` (chỉ trong cùng năm nhờ so sánh `PARENT`) và tính tỷ lệ tăng trưởng, không phụ thuộc thước đo trung gian.
* ● Lựa chọn 7 cột đo lường chính xác trên trục cột COLUMNS gồm bàn thắng Quý 1, bàn thắng và tăng trưởng Quý 2, Quý 3, Quý 4.
* ● Sử dụng hàm `TOPCOUNT` để lấy 10 CLB ghi nhiều bàn nhất trong năm 2023 trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 10: Tăng trưởng bàn thắng theo Quý QoQ của Top 10 CLB Châu Âu
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- Tỷ lệ tăng trưởng so với Quý liền trước - công thức tự chủ, giống hệt tab Calculations
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            [DIM Time].[Hierarchy].CURRENTMEMBER.LEVEL IS [DIM Time].[Hierarchy].[Quarter]
            AND [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT
            AND NOT ISEMPTY(([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
            AND ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER) <> 0,
            ([Measures].[Goals] - ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
                / ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER),
            NULL
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột COLUMNS: Liệt kê rõ ràng 7 cột đo lường loại bỏ cột Quý 1 rỗng
    {
        ([DIM Time].[Hierarchy].[Year].[2023].[1], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[QoQ Goals Growth])
    } ON COLUMNS,

    -- Trục Dòng ROWS: Top 10 CLB có tổng số bàn thắng cao nhất trong năm 2023
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
        ),
        10,
        ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu hiển thị đúng 10 dòng đại diện cho 10 câu lạc bộ hàng đầu và 7 cột chỉ số bàn thắng cùng tỷ lệ tăng trưởng QoQ.

---

### 3.10.10.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Câu Lạc Bộ `Club Name` | Q1 Bàn Thắng | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Manchester City** | 30 | 37 | +23.33% | 20 | -45.95% | 42 | +110.00% |
| **2** | **PSV Eindhoven** | 27 | 22 | -18.52% | 23 | +4.55% | 39 | +69.57% |
| **3** | **Bayer 04 Leverkusen** | 29 | 17 | -41.38% | 23 | +35.29% | 39 | +69.57% |
| **4** | **Feyenoord Rotterdam** | 30 | 22 | -26.67% | 28 | +27.27% | 28 | +0.00% |
| **5** | **Bayern Munich** | 26 | 20 | -23.08% | 23 | +15.00% | 37 | +60.87% |
| **6** | **Real Madrid** | 21 | 28 | +33.33% | 17 | -39.29% | 37 | +117.65% |
| **7** | **Arsenal FC** | 26 | 21 | -19.23% | 18 | -14.29% | 34 | +88.89% |
| **8** | **Atlético de Madrid** | 19 | 27 | +42.11% | 16 | -40.74% | 35 | +118.75% |
| **9** | **Liverpool FC** | 16 | 28 | +75.00% | 17 | -39.29% | 35 | +105.88% |
| **10** | **Borussia Dortmund** | 30 | 28 | -6.67% | 12 | -57.14% | 25 | +108.33% |
