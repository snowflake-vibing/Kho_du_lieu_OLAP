# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.1 Câu truy vấn 1

**Nội dung truy vấn:** Xác định danh sách 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh Premier League có mã giải đấu GB1 trong mùa giải 2023/2024. Phân tích này giúp ban chuyên môn và nhà quản lý nhận diện các tiền đạo có hiệu suất làm bàn xuất sắc nhất, phục vụ công tác chuyển nhượng và đánh giá phong độ.

### 3.10.1.1 Sử dụng Cube Browser

**Bước 1:** Khởi động phần mềm Visual Studio, trong cửa sổ Solution Explorer ở khung bên phải màn hình, nhấp đúp chuột vào tệp khối đa chiều DW Football Transfermarkt.cube. Trình thiết kế Cube Designer xuất hiện. Trên thanh tab chức năng nằm ở mép trên, nhấp chuột vào tab Browser nằm ở ngoài cùng bên phải.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng Design Mode có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc giải đấu tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Competition.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Competition ID.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, giao diện hiển thị danh sách các mã giải đấu, tích chọn mã GB1 rồi nhấp nút OK để xác nhận.

**Bước 4:** Thiết lập bộ lọc mùa giải tại dòng thứ hai trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Season.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn mùa bóng 2023/2024 rồi nhấp nút OK để xác nhận.

**Bước 5:** Thiết lập điều kiện lọc Top 10 cầu thủ tại dòng thứ ba trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Player Name.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.

**Bước 6:** Trong cửa sổ Expression Builder, nhấp chuột vào khung soạn thảo và dán biểu thức MDX tùy chỉnh dùng hàm TOPCOUNT để xếp hạng lấy đúng 10 cầu thủ ghi bàn nhiều nhất:
```mdx
TOPCOUNT([DIM Player].[Player Name].[Player Name].MEMBERS, 10, [Measures].[Goals])
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 7:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, nhấp chuột mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Player Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng trống.
* ● Tiếp tục trong khung Metadata, nhấp chuột mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, nhấp giữ chuột trái vào thước đo Goals, kéo con trỏ chuột sang khu vực lưới dữ liệu và thả chuột vào vị trí ngay bên cạnh cột Player Name.

**Bước 8:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả gồm 10 dòng đại diện cho 10 cầu thủ ghi nhiều bàn thắng nhất giải Ngoại Hạng Anh mùa giải 2023/2024.

---

### 3.10.1.2 Sử dụng Pivot Excel

**Bước 1:** Khởi động phần mềm Microsoft Excel, nhấp chọn Blank Workbook để tạo một trang tính mới. Trên thanh Ribbon ở phía trên, nhấp chuột vào thẻ Data. Trong nhóm công cụ Get & Transform Data, nhấp chuột vào nút Get Data, di chuột chọn From Database rồi nhấp chuột chọn From Analysis Services.

**Bước 2:** Cửa sổ Data Connection Wizard xuất hiện. Tại ô Server name, nhập địa chỉ localhost hoặc tên máy chủ dịch vụ SSAS. Tại mục Log on credentials, nhấp chọn ô tròn Use Windows Authentication. Nhấp chuột vào nút Next ở góc dưới bên phải.

**Bước 3:** Tại bước chọn Database và Cube, nhấp chuột chọn cơ sở dữ liệu DW Football SSAS trong danh sách phía trên, sau đó nhấp chuột chọn khối Cube DW Football Transfermarkt ở danh sách phía dưới rồi nhấp nút Finish. Hộp thoại Import Data hiện ra, nhấp chọn ô tròn PivotTable Report, kiểm tra vị trí đặt bảng tại ô A3 rồi nhấp nút OK.

**Bước 4:** Thao tác kéo thả các trường trong khung danh sách PivotTable Fields ở cạnh phải màn hình:
* ● Nhấp chuột mở rộng thư mục DIM Competition, nhấp giữ chuột trái vào trường Competition ID, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Nhấp chuột mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Season, kéo chuột xuống phía dưới và thả tiếp vào ô Filters ngay phía dưới trường Competition ID.
* ● Nhấp chuột mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Player Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Nhấp chuột mở rộng thư mục Measures, nhấp giữ chuột trái vào thước đo Goals, kéo chuột xuống phía dưới và thả vào ô Values. Giá trị hiển thị tại ô này là Sum of Goals.

**Bước 5:** Thiết lập giá trị cho các bộ lọc trên trang tính Excel:
* ● Tại ô B1 nằm cạnh nhãn Competition ID, nhấp chuột vào nút mũi tên xổ xuống, tích chọn mã giải đấu GB1 rồi nhấp nút OK.
* ● Tại ô B2 nằm cạnh nhãn Season, nhấp chuột vào nút mũi tên xổ xuống, tích chọn mùa bóng 2023/2024 rồi nhấp nút OK.

**Bước 6:** Thiết lập bộ lọc Top 10 cầu thủ ghi bàn:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 có nhãn Row Labels.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Hộp thoại Top 10 Filter xuất hiện, giữ nguyên ô thứ nhất là Top, nhập số 10 vào ô thứ hai, giữ nguyên ô thứ ba là Items, tại ô thứ tư By nhấp mở danh sách thả xuống và chọn thước đo Sum of Goals. Nhấp nút OK để áp dụng bộ lọc.

**Bước 7:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh gồm 10 cầu thủ có số bàn thắng cao nhất giải Ngoại Hạng Anh mùa 2023/2024 được sắp xếp theo thứ tự số bàn thắng Sum of Goals giảm dần.

---

### 3.10.1.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Khởi động phần mềm SQL Server Management Studio. Tại hộp thoại Connect to Server, mục Server type nhấp chọn Analysis Services, mục Server name nhập localhost hoặc tên instance SSAS, mục Authentication chọn Windows Authentication rồi nhấp nút Connect.

**Bước 2:** Trong cửa sổ Object Explorer ở bên trái màn hình, nhấp chuột mở rộng thư mục Databases, mở rộng tiếp cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes. Nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX. Cửa sổ soạn thảo truy vấn MDX xuất hiện ở khung làm việc chính bên phải.

**Bước 3:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích xác định top 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh mùa giải 2023/2024. Truy vấn chỉ định rõ các mệnh đề:
* ● Lựa chọn measure `[Measures].[Goals]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `TOPCOUNT` để lựa chọn 10 bản ghi hàng đầu hiển thị trên trục hàng ROWS, kết hợp hàm `NONEMPTY` lọc trước các cầu thủ có phát sinh bàn thắng trong chiều `[DIM Player].[Player Name]` theo `[Measures].[Goals]`.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn phạm vi tính toán trong giải Ngoại Hạng Anh `[DIM Competition].[Competition ID].[GB1]` và mùa giải 2023/2024 `[DIM Time].[Season].[2023/2024]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột COLUMNS: Trích xuất thước đo Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng ROWS: Xếp hạng và lấy đúng 10 cầu thủ ghi nhiều bàn nhất
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player Name].[Player Name].MEMBERS,
            (
                [Measures].[Goals],
                [DIM Competition].[Competition ID].[GB1],
                [DIM Time].[Season].[2023/2024]
            )
        ),
        10,
        [Measures].[Goals]
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt Slicer Axis: Giới hạn trong giải GB1 và mùa 2023/2024
WHERE (
    [DIM Competition].[Competition ID].[GB1],
    [DIM Time].[Season].[2023/2024]
);
```

**Bước 4:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 5:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu hiển thị đúng 10 dòng tên cầu thủ và 1 cột số bàn thắng Goals tương ứng, khớp hoàn toàn với các tiêu chí lọc, trong đó Erling Haaland dẫn đầu với 27 bàn thắng, Cole Palmer với 22 bàn thắng và Alexander Isak với 21 bàn thắng.

---

### 3.10.1.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| Xếp hạng | Tên Cầu Thủ `Player Name` | Tổng Số Bàn Thắng `Goals` |
| :---: | :--- | :---: |
| **1** | **Erling Haaland** | **27** |
| **2** | **Cole Palmer** | **22** |
| **3** | **Alexander Isak** | **21** |
| **4** | **Dominic Solanke** | **19** |
| **5** | **Ollie Watkins** | **19** |
| **6** | **Phil Foden** | **19** |
| **7** | **Mohamed Salah** | **18** |
| **8** | **Heung-min Son** | **17** |
| **9** | **Bukayo Saka** | **16** |
| **10** | **Jarrod Bowen** | **16** |
