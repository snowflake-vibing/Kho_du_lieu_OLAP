# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.3 Câu truy vấn 3

**Nội dung truy vấn:** Thống kê tổng số phút thi đấu cùng tổng số bàn thắng và kiến tạo của các cầu thủ đạt mốc từ 20 lần đóng góp vào bàn thắng trở lên trong mùa giải 2023/2024 nhằm đánh giá mức độ phụ thuộc vào các trụ cột tấn công.

### 3.10.3.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc mùa giải tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Time.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Season.
* ● Tại cột Operator, giữ nguyên giá trị là Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn mùa bóng 2023/2024 rồi nhấp nút OK để xác nhận.

**Bước 4:** Thiết lập điều kiện lọc cầu thủ có đóng góp bàn thắng trên 20 tại dòng thứ hai trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Player Name.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.

**Bước 5:** Trong cửa sổ Expression Builder, nhấp chuột vào khung soạn thảo và dán biểu thức MDX tùy chỉnh dùng hàm FILTER kết hợp NONEMPTY để lọc danh sách cầu thủ có tổng đóng góp bàn thắng lớn hơn 20:
```mdx
FILTER(
    NONEMPTY([DIM Player].[Player Name].[Player Name].MEMBERS, ([Measures].[Goal Contributions], [DIM Time].[Season].[2023/2024])),
    [Measures].[Goal Contributions] > 20
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 6:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, nhấp chuột mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Player Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng trống.
* ● Tiếp tục trong khung Metadata, nhấp chuột mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, nhấp giữ chuột trái vào thước đo Minutes Played, kéo con trỏ chuột sang khu vực lưới dữ liệu và thả chuột vào vị trí ngay bên cạnh cột Player Name.
* ● Tiếp tục nhấp giữ chuột trái vào thước đo Goal Contributions trong nhóm FACT Player Match Perf, kéo con trỏ chuột sang và thả chuột vào vị trí ngay bên cạnh cột Minutes Played.

**Bước 7:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị danh sách các cầu thủ đạt mốc trên 20 đóng góp bàn thắng trong mùa giải 2023/2024 kèm theo tổng số phút thi đấu.

---

### 3.10.3.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Season, kéo chuột xuống phía dưới và thả vào ô Filters.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Player Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, nhấp giữ chuột trái vào thước đo Minutes Played, kéo chuột xuống phía dưới và thả vào ô Values với giá trị hiển thị là Sum of Minutes Played.
* ● Tiếp tục mở rộng thư mục Measures, nhấp giữ chuột trái vào thước đo Goal Contributions, kéo chuột xuống phía dưới và thả tiếp vào ô Values với giá trị hiển thị là Sum of Goal Contributions.

**Bước 2:** Thiết lập giá trị cho bộ lọc mùa giải trên trang tính Excel: Tại ô B1 nằm cạnh nhãn Season, nhấp chuột vào nút mũi tên xổ xuống, tích chọn mùa bóng 2023/2024 rồi nhấp nút OK.

**Bước 3:** Thiết lập bộ lọc cầu thủ có đóng góp bàn thắng lớn hơn 20:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 có nhãn Row Labels.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Greater Than...
* ● Hộp thoại Value Filter xuất hiện, tại danh sách thả xuống chọn thước đo Sum of Goal Contributions, tại ô điều kiện bên cạnh nhập số 20, sau đó nhấp nút OK để áp dụng bộ lọc.

**Bước 4:** Sắp xếp danh sách giảm dần theo đóng góp bàn thắng: Nhấp chuột phải vào một ô số bất kỳ trong cột Sum of Goal Contributions trên bảng tính, di chuột chọn mục Sort rồi nhấp chọn Sort Largest to Smallest.

**Bước 5:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh danh sách các ngôi sao tấn công đạt trên 20 bàn thắng và kiến tạo trong mùa giải 2023/2024, được sắp xếp từ cao xuống thấp theo thứ tự đóng góp bàn thắng giảm dần.

---

### 3.10.3.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích xác định danh sách cầu thủ có trên 20 đóng góp bàn thắng trong mùa giải 2023/2024. Truy vấn chỉ định rõ các mệnh đề:
* ● Lựa chọn hai thước đo `[Measures].[Minutes Played]` và `[Measures].[Goal Contributions]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `FILTER` kết hợp hàm `NONEMPTY` để lọc các cầu thủ có `Goal Contributions` lớn hơn 20 trên trục hàng ROWS, đồng thời bọc ngoài bằng hàm `ORDER` với cờ `BDESC` để sắp xếp giảm dần toàn cục.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn phạm vi tính toán trong mùa giải 2023/2024 `[DIM Time].[Season].[2023/2024]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 03: Cầu thủ có trên 20 đóng góp bàn thắng G+A mùa giải 2023/2024
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột COLUMNS: Tổng số phút thi đấu và tổng đóng góp bàn thắng
    {
        [Measures].[Minutes Played],
        [Measures].[Goal Contributions]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các cầu thủ có G+A > 20, sắp xếp giảm dần toàn cục
    ORDER(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                (
                    [Measures].[Goal Contributions],
                    [DIM Time].[Season].[2023/2024]
                )
            ),
            [Measures].[Goal Contributions] > 20
        ),
        [Measures].[Goal Contributions],
        BDESC
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt Slicer Axis: Mùa giải 2023/2024
WHERE (
    [DIM Time].[Season].[2023/2024]
);
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu hiển thị danh sách các cầu thủ đạt trên 20 bàn thắng và kiến tạo kèm 2 cột số phút thi đấu và tổng đóng góp bàn thắng, khớp hoàn toàn với các tiêu chí lọc, trong đó Harry Kane dẫn đầu với 56 đóng góp bàn thắng và 3908 phút thi đấu.

---

### 3.10.3.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| Xếp hạng | Tên Cầu Thủ `Player Name` | Số Phút Thi Đấu `Minutes Played` | Đóng Góp Bàn Thắng `Goal Contributions` |
| :---: | :--- | :---: | :---: |
| **1** | **Harry Kane** | 3908 | **56** |
| **2** | **Luuk de Jong** | 3406 | **47** |
| **3** | **Viktor Gyökeres** | 3537 | **45** |
| **4** | **Kylian Mbappé** | 3239 | **42** |
| **5** | **Mauro Icardi** | 3555 | **39** |
| **6** | **Erling Haaland** | 3337 | **38** |
| **7** | **Pierre-Emerick Aubameyang** | 3659 | **38** |
| **8** | **Mohamed Salah** | 2935 | **37** |
| **9** | **Loïs Openda** | 3274 | **35** |
| **10** | **Phil Foden** | 3555 | **35** |
| **11** | **Jude Bellingham** | 3318 | **34** |
| **12** | **Bukayo Saka** | 3661 | **33** |
| **13** | **Cole Palmer** | 2628 | **33** |
| **14** | **Santiago Gimenez** | 2838 | **33** |
| **15** | **Vangelis Pavlidis** | 3000 | **33** |
