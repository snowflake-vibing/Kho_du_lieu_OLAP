# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.12 Câu truy vấn 12

**Nội dung truy vấn:** Xác định tháng có số lượng thẻ phạt kỷ lục cao nhất của từng Huấn luyện viên trưởng danh tiếng trong năm thi đấu, đi kèm tổng số thẻ vàng Yellow Cards và thẻ đỏ Red Cards. Ứng dụng hàm lặp tập hợp GENERATE kết hợp TOPCOUNT lấy đúng 1 tháng cao nhất giải quyết triệt để bài toán Group By Top 1 Per Category trong đại số đa chiều, hỗ trợ ban kỷ luật và truyền thông nhận diện thời điểm căng thẳng tâm lý lớn nhất của các huấn luyện viên.

### 3.10.12.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc lặp tập hợp GENERATE tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Club.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Coach Name.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.
* ● Trong cửa sổ Expression Builder, dán biểu thức GENERATE kết hợp TOPCOUNT lấy duy nhất 1 tháng có nhiều thẻ vàng nhất cho mỗi huấn luyện viên:
```mdx
GENERATE(
    FILTER(
        NONEMPTY(
            EXCEPT([DIM Club].[Coach Name].[Coach Name].MEMBERS, { [DIM Club].[Coach Name].[All] }),
            [Measures].[Yellow Cards]
        ),
        [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown" AND [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown Coach"
    ),
    TOPCOUNT(
        NONEMPTY(
            CrossJoin(
                { [DIM Club].[Coach Name].CURRENTMEMBER },
                EXCEPT([DIM Time].[Month].[Month].MEMBERS, { [DIM Time].[Month].[All] })
            ),
            [Measures].[Yellow Cards]
        ),
        1,
        [Measures].[Yellow Cards]
    )
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 4:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Club, nhấp giữ chuột trái vào thuộc tính Coach Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Mở rộng thư mục chiều DIM Time, tìm thuộc tính Month, nhấp giữ chuột trái kéo sang thả vào vị trí ngay bên cạnh cột Coach Name.
* ● Mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, lần lượt nhấp giữ chuột trái và kéo các thước đo Yellow Cards và Red Cards thả vào khu vực dữ liệu.

**Bước 5:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng kết quả mỗi huấn luyện viên đúng duy nhất một tháng có số thẻ phạt cao điểm nhất.

---

### 3.10.12.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Club, nhấp giữ chuột trái vào trường Coach Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục DIM Time, nhấp giữ chuột trái vào trường Month, kéo chuột xuống phía dưới và thả tiếp vào ô Rows ngay phía dưới trường Coach Name.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Yellow Cards và Red Cards.

**Bước 2:** Cấu hình bộ lọc Top 1 tháng kỷ lục cho từng huấn luyện viên:
* ● Trên bảng PivotTable, nhấp chuột vào nút mũi tên lọc bên cạnh một ô giá trị thuộc cột Month.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Top 10...
* ● Trong hộp thoại Top 10 Filter xuất hiện, thiết lập Top 1 Items theo trường Sum of Yellow Cards rồi nhấp nút OK để áp dụng.

**Bước 3:** Sắp xếp giảm dần theo số thẻ vàng kỷ lục: Nhấp chuột phải vào một ô số bất kỳ trong cột Sum of Yellow Cards, di chuột chọn mục Sort rồi nhấp chọn Sort Largest to Smallest.

**Bước 4:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh danh sách các huấn luyện viên cùng tháng cao điểm phải nhận nhiều thẻ phạt nhất.

---

### 3.10.12.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích tìm tháng kỷ lục thẻ phạt của từng huấn luyện viên trưởng. Truy vấn chỉ định rõ các mệnh đề:
* ● Lựa chọn hai thước đo `[Measures].[Yellow Cards]` và `[Measures].[Red Cards]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `GENERATE` kết hợp `TOPCOUNT` với tham số đếm bằng 1 để duyệt tuần tự qua từng huấn luyện viên và trích xuất đúng một tháng có nhiều thẻ vàng nhất trên trục hàng ROWS, kết hợp hàm `ORDER` với cờ `BDESC` để sắp xếp giảm dần toàn cục.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 12: Thẻ phạt phân theo Huấn luyện viên trưởng và Tháng trong năm
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột COLUMNS: Thước đo Thẻ vàng và Thẻ đỏ
    {
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Duyệt qua từng HLV, tìm đúng 1 tháng có nhiều thẻ vàng nhất
    ORDER(
        GENERATE(
            FILTER(
                NONEMPTY(
                    EXCEPT([DIM Club].[Coach Name].[Coach Name].MEMBERS, { [DIM Club].[Coach Name].[All] }),
                    [Measures].[Yellow Cards]
                ),
                [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown" AND [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown Coach"
            ),
            TOPCOUNT(
                NONEMPTY(
                    CrossJoin(
                        { [DIM Club].[Coach Name].CURRENTMEMBER },
                        EXCEPT([DIM Time].[Month].[Month].MEMBERS, { [DIM Time].[Month].[All] })
                    ),
                    [Measures].[Yellow Cards]
                ),
                1,
                [Measures].[Yellow Cards]
            )
        ),
        [Measures].[Yellow Cards],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về danh sách các huấn luyện viên trưởng cùng tháng đỉnh điểm căng thẳng và số lượng thẻ phạt chi tiết.

---

### 3.10.12.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Huấn Luyện Viên `Coach Name` | Tháng Kỷ Lục Thẻ Phạt `Month` | Thẻ Vàng `Yellow Cards` | Thẻ Đỏ `Red Cards` |
| :---: | :--- | :---: | :---: | :---: |
| **1** | **Matías Almeyda** | Tháng 10 | **32** | 1 |
| **2** | **Diego Simeone** | Tháng 10 | **27** | 0 |
| **3** | **João Pereira** | Tháng 10 | **27** | 0 |
| **4** | **Rúben Amorim** | Tháng 12 | **25** | 0 |
| **5** | **Sergio Francisco** | Tháng 10 | **25** | 0 |
| **6** | **Sven Vandenbroeck** | Tháng 10 | **25** | 1 |
| **7** | **Russell Martin** | Tháng 10 | **24** | 0 |
| **8** | **José Mourinho** | Tháng 1 | **24** | 0 |
| **9** | **Stefano Pioli** | Tháng 10 | **23** | 0 |
| **10** | **Erik ten Hag** | Tháng 10 | **22** | 0 |
