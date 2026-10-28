# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.9 Câu truy vấn 9

**Nội dung truy vấn:** Xác định các câu lạc bộ bóng đá toàn diện xuất hiện đồng thời trong cả hai nhóm gồm 30 đội ghi bàn nhiều nhất vào ngày cuối tuần và 30 đội ghi bàn nhiều nhất vào ngày thường, đồng thời so sánh số bàn thắng và số thẻ phạt giữa hai thời điểm thi đấu nhằm đánh giá tính ổn định về phong độ của các đội bóng.

### 3.10.9.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc giao tập hợp INTERSECT tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Club.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Club Name.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.
* ● Trong cửa sổ Expression Builder, dán biểu thức giao tập hợp INTERSECT giữa Top 30 cuối tuần và Top 30 ngày thường:
```mdx
INTERSECT(
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
    ),
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
    )
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 4:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Club, nhấp giữ chuột trái vào thuộc tính Club Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Mở rộng thư mục chiều DIM Time, tìm thuộc tính Is Weekend, nhấp giữ chuột trái kéo thả lên vùng Columns để chia bảng theo thời điểm cuối tuần hoặc ngày thường.
* ● Mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, lần lượt nhấp giữ chuột trái và kéo các thước đo Goals và Yellow Cards thả vào vùng dữ liệu trung tâm.

**Bước 5:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng ma trận hiệu năng của các đội bóng ưu tú trên cả hai thời điểm cuối tuần và ngày thường.

---

### 3.10.9.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Is Weekend, kéo chuột xuống phía dưới và thả vào ô Columns.
* ● Mở rộng thư mục DIM Club, nhấp giữ chuột trái vào trường Club Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Goals và Yellow Cards.

**Bước 2:** Thiết lập bộ lọc Top 30 câu lạc bộ xuất sắc:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Club Name.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Trong hộp thoại Top 10 Filter xuất hiện, đổi số 10 thành 30 theo trường Sum of Goals rồi nhấp nút OK để áp dụng.

**Bước 3:** Tắt dòng tổng phụ để bảng gọn gàng: Trên thanh Ribbon, chọn thẻ Design, nhấp vào mục Subtotals rồi chọn Do Not Show Subtotals.

**Bước 4:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh ma trận 4 cột gồm bàn thắng và thẻ vàng cho cả hai thời điểm ngày thường và cuối tuần của các câu lạc bộ ưu tú.

---

### 3.10.9.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích so sánh hiệu năng và thẻ phạt của các câu lạc bộ giữa cuối tuần và ngày thường. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH SET` định nghĩa tập hợp `[Top_Weekend_Clubs]` lọc Top 30 CLB cuối tuần, tập hợp `[Top_Weekday_Clubs]` lọc Top 30 CLB ngày thường, và tập hợp `[Elite_Clubs_All_Days]` sử dụng hàm `INTERSECT` để lấy các CLB xuất hiện đồng thời trong cả hai nhóm.
* ● Sử dụng hàm `CrossJoin` kết hợp hai trạng thái thời điểm và hai thước đo hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `ORDER` với cờ `BDESC` sắp xếp danh sách các CLB ưu tú giảm dần theo tổng bàn thắng trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 09: So sánh hiệu năng và thẻ phạt của các CLB giữa Cuối tuần và Ngày thường
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần Is_Weekend = 1
    SET [Top_Weekend_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        )

    -- 2. Top 30 CLB ghi bàn nhiều nhất vào Ngày thường Is_Weekend = 0
    SET [Top_Weekday_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        )

    -- 3. Giao tập hợp INTERSECT: Các CLB xuất sắc toàn diện cả Cuối tuần và Ngày thường
    SET [Elite_Clubs_All_Days] AS
        INTERSECT([Top_Weekend_Clubs], [Top_Weekday_Clubs])

SELECT
    -- Trục Cột COLUMNS: Tích Đề-các giữa Thời điểm và Thước đo
    CrossJoin(
        { [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] },
        { [Measures].[Goals], [Measures].[Yellow Cards] }
    ) ON COLUMNS,

    -- Trục Dòng ROWS: Danh sách các CLB ưu tú thuộc tập hợp giao INTERSECT, xếp giảm dần
    ORDER(
        [Elite_Clubs_All_Days],
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận đối chiếu phong độ toàn diện của các câu lạc bộ xuất sắc nhất bóng đá Châu Âu.

---

### 3.10.9.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Tên Câu Lạc Bộ `Club Name` | Cuối Tuần Bàn Thắng | Cuối Tuần Thẻ Vàng | Ngày Thường Bàn Thắng | Ngày Thường Thẻ Vàng |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Manchester City** | 94 | 49 | 151 | 80 |
| **2** | **Bayern Munich** | 115 | 62 | 110 | 67 |
| **3** | **PSV Eindhoven** | 82 | 24 | 137 | 76 |
| **4** | **Real Madrid** | 76 | 47 | 134 | 128 |
| **5** | **Arsenal FC** | 75 | 42 | 124 | 103 |
| **6** | **Paris Saint-Germain** | 59 | 40 | 139 | 112 |
| **7** | **Bayer 04 Leverkusen** | 65 | 74 | 126 | 120 |
| **8** | **Celtic FC** | 75 | 43 | 111 | 62 |
| **9** | **Inter Milan** | 70 | 49 | 114 | 103 |
