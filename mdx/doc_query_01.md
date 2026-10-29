# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.1 Câu truy vấn 1

**Nội dung truy vấn:** Liệt kê danh sách 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh mùa giải 2023 nhằm nhận diện các chân sút hàng đầu phục vụ công tác chuyển nhượng và đánh giá phong độ thi đấu.

### 3.10.1.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc giải đấu tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Competition.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Competition ID.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, giao diện hiển thị danh sách các mã giải đấu, tích chọn mã GB1 rồi nhấp nút OK để xác nhận.

**Bước 4:** Thiết lập bộ lọc mùa giải tại dòng thứ hai trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Season.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn mùa bóng 2023 rồi nhấp nút OK để xác nhận.

**Bước 5:** Thiết lập điều kiện lọc và sắp xếp Top 10 cầu thủ tại dòng thứ ba trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Player Name.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.

**Bước 6:** Do lưới kéo thả của Cube Browser không có tính năng nhấp chuột phải để Sort như Excel, trong cửa sổ Expression Builder, dán biểu thức kết hợp TOPCOUNT và ORDER để vừa lọc 10 cầu thủ xuất sắc nhất vừa sắp xếp giảm dần theo số bàn thắng:
```mdx
ORDER(
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player Name].[Player Name].MEMBERS,
            (
                [Measures].[Goals],
                [DIM Competition].[Competition ID].[GB1],
                [DIM Time].[Season].[2023]
            )
        ),
        10,
        [Measures].[Goals]
    ),
    [Measures].[Goals],
    BDESC
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 7:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, nhấp chuột mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Player Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng trống.
* ● Tiếp tục trong khung Metadata, nhấp chuột mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, nhấp giữ chuột trái vào thước đo Goals, kéo con trỏ chuột sang khu vực lưới dữ liệu và thả chuột vào vị trí ngay bên cạnh cột Player Name.

**Bước 8:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả gồm 10 dòng đại diện cho 10 cầu thủ ghi nhiều bàn thắng nhất giải Ngoại Hạng Anh mùa giải 2023.

---

### 3.10.1.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Competition, nhấp giữ chuột trái vào trường Competition ID, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Season, kéo chuột xuống phía dưới và thả tiếp vào ô Filters ngay phía dưới trường Competition ID.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Player Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, nhấp giữ chuột trái vào thước đo Goals, kéo chuột xuống phía dưới và thả vào ô Values với giá trị hiển thị là Sum of Goals.

**Bước 2:** Thiết lập giá trị cho các bộ lọc trên trang tính Excel:
* ● Tại ô B1 nằm cạnh nhãn Competition ID, nhấp chuột vào nút mũi tên xổ xuống, tích chọn mã giải đấu GB1 rồi nhấp nút OK.
* ● Tại ô B2 nằm cạnh nhãn Season, nhấp chuột vào nút mũi tên xổ xuống, tích chọn mùa bóng 2023 rồi nhấp nút OK.

**Bước 3:** Thiết lập bộ lọc Top 10 cầu thủ ghi bàn:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 có nhãn Row Labels.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Hộp thoại Top 10 Filter xuất hiện, giữ nguyên ô thứ nhất là Top, nhập số 10 vào ô thứ hai, giữ nguyên ô thứ ba là Items, tại ô thứ tư By nhấp mở danh sách thả xuống và chọn thước đo Sum of Goals. Nhấp nút OK để áp dụng bộ lọc.

**Bước 4:** Sắp xếp giảm dần theo số bàn thắng: Nhấp chuột phải vào một ô số bất kỳ trong cột Sum of Goals, ví dụ ô B5, di chuyển con trỏ chuột vào mục Sort rồi nhấp chọn Sort Largest to Smallest để đưa cầu thủ ghi nhiều bàn nhất lên vị trí dẫn đầu bảng.

**Bước 5:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh gồm 10 cầu thủ có số bàn thắng cao nhất giải Ngoại Hạng Anh mùa giải 2023 được sắp xếp giảm dần chính xác tuyệt đối từ Erling Haaland 27 bàn xuống Jean-Philippe Mateta 16 bàn.

---

### 3.10.1.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích xác định top 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh mùa giải 2023. Truy vấn chỉ định rõ các mệnh đề:
* ● Lựa chọn measure `[Measures].[Goals]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `ORDER` kết hợp `TOPCOUNT` để lựa chọn 10 bản ghi hàng đầu và sắp xếp giảm dần theo số bàn thắng trên trục hàng ROWS, kết hợp hàm `NONEMPTY` lọc trước các cầu thủ có phát sinh bàn thắng trong chiều `[DIM Player].[Player Name]` theo `[Measures].[Goals]`.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn phạm vi tính toán trong giải Ngoại Hạng Anh `[DIM Competition].[Competition ID].[GB1]` và mùa giải 2023 `[DIM Time].[Season].[2023]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột COLUMNS: Trích xuất thước đo Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng ROWS: Xếp hạng và lấy đúng 10 cầu thủ ghi nhiều bàn nhất, sắp xếp giảm dần
    ORDER(
        TOPCOUNT(
            NONEMPTY(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                (
                    [Measures].[Goals],
                    [DIM Competition].[Competition ID].[GB1],
                    [DIM Time].[Season].[2023]
                )
            ),
            10,
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt Slicer Axis: Giới hạn trong giải GB1 và mùa 2023
WHERE (
    [DIM Competition].[Competition ID].[GB1],
    [DIM Time].[Season].[2023]
);
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu hiển thị đúng 10 dòng tên cầu thủ và 1 cột số bàn thắng tương ứng, khớp hoàn toàn với các tiêu chí lọc, trong đó Erling Haaland dẫn đầu với 27 bàn thắng, Cole Palmer với 22 bàn thắng và Alexander Isak với 21 bàn thắng.

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
