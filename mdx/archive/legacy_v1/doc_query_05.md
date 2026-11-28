# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.5 Câu truy vấn 5

**Nội dung truy vấn:** Khảo sát mối tương quan giữa đặc điểm chân thuận gồm chân trái, chân phải, hai chân với số lượng bàn thắng ghi được theo từng vị trí tấn công cụ thể gồm tiền đạo cắm, tiền đạo cánh trái, tiền đạo cánh phải, tiền vệ tấn công và hộ công nhằm phục vụ phân tích chiến thuật và bố trí đội hình.

### 3.10.5.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan. Màn hình lúc này chia làm 3 khu vực gồm khung Metadata ở bên trái, vùng thiết lập bộ lọc Filter Pane ở phía trên bên phải và lưới dữ liệu Data Grid ở phía dưới bên phải.

**Bước 3:** Thiết lập bộ lọc nhóm vị trí tấn công tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Sub Position.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.
* ● Trong cửa sổ Expression Builder, dán biểu thức hợp tập hợp UNION để gom 5 vị trí tấn công và tiền vệ:
```mdx
UNION(
    { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
    { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
)
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 4:** Thiết lập bộ lọc loại bỏ nút All của chân thuận tại dòng thứ hai trong vùng bộ lọc Filter Pane:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Foot.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Custom.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhấp tiếp vào nút dấu ba chấm mở rộng để mở cửa sổ Expression Builder.
* ● Trong cửa sổ Expression Builder, dán biểu thức EXCEPT để loại bỏ nút tổng hợp All:
```mdx
EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })
```
Sau đó nhấp nút OK ở góc dưới cửa sổ Expression Builder để lưu điều kiện lọc.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Sub Position, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong khung Metadata, nhấp giữ chuột trái vào thuộc tính Foot trong chiều DIM Player, kéo sang thả vào vị trí ngay bên cạnh cột Sub Position.
* ● Tiếp tục trong khung Metadata, mở rộng thư mục Measures, mở rộng tiếp nhóm FACT Player Match Perf, nhấp giữ chuột trái vào thước đo Goals, kéo sang và thả vào vị trí ngay bên cạnh cột Foot.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị ma trận phân bổ bàn thắng theo từng vị trí chi tiết và loại chân thuận.

---

### 3.10.5.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Sub Position, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Foot, kéo chuột xuống phía dưới và thả tiếp vào ô Rows ngay bên dưới trường Sub Position.
* ● Mở rộng thư mục Measures, nhấp giữ chuột trái vào thước đo Goals, kéo chuột xuống phía dưới và thả vào ô Values với giá trị hiển thị là Sum of Goals.

**Bước 2:** Thiết lập lọc các vị trí trọng điểm: Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Sub Position, bỏ chọn ô Select All, chỉ tích chọn 5 vị trí gồm Centre-Forward, Second Striker, Left Winger, Right Winger và Attacking Midfield rồi nhấp nút OK.

**Bước 3:** Định dạng bố cục bảng danh sách phẳng: Trên thanh Ribbon, chọn thẻ Design, tại mục Report Layout nhấp chọn Show in Tabular Form, tiếp tục tại mục Subtotals nhấp chọn Do Not Show Subtotals để bảng hiển thị dạng phẳng 3 cột gồm Vị trí chi tiết, Chân thuận và Số bàn thắng.

**Bước 4:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh gồm đúng 18 dòng dữ liệu phân bổ bàn thắng theo từng vị trí chi tiết và chân thuận, hoàn toàn trùng khớp với kết quả từ Cube Browser và MDX.

---

### 3.10.5.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích so sánh tổng số bàn thắng giữa các loại chân thuận theo từng vị trí chi tiết. Truy vấn chỉ định rõ các mệnh đề:
* ● Lựa chọn thước đo `[Measures].[Goals]` hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `UNION` hợp nhất hai nhóm vị trí tấn công và tiền vệ, kết hợp hàm `EXCEPT` loại trừ nút All của chân thuận, sau đó dùng hàm `CrossJoin` và `NONEMPTY` tạo tích Đề-các trên trục hàng ROWS, kết hợp hàm `ORDER` với từ khóa `DESC` để sắp xếp giảm dần số bàn thắng theo từng nhóm vị trí.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 05: Bàn thắng theo vị trí chi tiết và chân thuận
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột COLUMNS: Thước đo Bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng ROWS: Các cặp Sub Position và Foot sắp xếp phân cấp theo từng vị trí
    ORDER(
        NONEMPTY(
            CrossJoin(
                -- Hợp tập hợp UNION: Kết hợp các vị trí tấn công và tiền vệ
                UNION(
                    { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
                    { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
                ),
                -- Tập hợp các loại chân thuận loại bỏ nút All
                EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })
            ),
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        DESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về danh sách ma trận các cặp vị trí và chân thuận kèm số bàn thắng tương ứng được sắp xếp khoa học.

---

### 3.10.5.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Vị Trí Chi Tiết `Sub Position` | Chân Thuận `Foot` | Tổng Bàn Thắng `Goals` |
| :---: | :--- | :---: | :---: |
| **1** | **Attacking Midfield** | right | **1308** |
| **2** | **Attacking Midfield** | left | **667** |
| **3** | **Attacking Midfield** | both | **59** |
| **4** | **Attacking Midfield** | Unknown | **1** |
| **5** | **Centre-Forward** | right | **5457** |
| **6** | **Centre-Forward** | left | **1114** |
| **7** | **Centre-Forward** | both | **273** |
| **8** | **Centre-Forward** | Unknown | **34** |
| **9** | **Left Winger** | right | **2015** |
| **10** | **Left Winger** | left | **186** |
| **11** | **Left Winger** | both | **79** |
| **12** | **Left Winger** | Unknown | **2** |
| **13** | **Right Winger** | left | **1207** |
| **14** | **Right Winger** | right | **783** |
| **15** | **Right Winger** | both | **76** |
| **16** | **Right Winger** | Unknown | **0** |
| **17** | **Second Striker** | right | **242** |
| **18** | **Second Striker** | left | **93** |
