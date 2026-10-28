# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.11 Câu truy vấn 11

**Nội dung truy vấn:** Thống kê danh sách các sân vận động có sức chứa từ 60.000 chỗ ngồi trở lên cùng câu lạc bộ chủ quản, tổng số trận đấu đã diễn ra và tổng số bàn thắng ghi được tại các sân đấu này nhằm đánh giá quy mô cơ sở vật chất và mức độ sôi động của các cầu trường lớn.

### 3.10.11.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên để khởi tạo 2 thước đo tính toán làm sạch sức chứa và đếm số trận đấu duy nhất:
* ● Thước đo thứ nhất: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Stadium Capacity Cleaned`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE, 0)
```
Đặt Format String là `#,##0 Chỗ`.
* ● Thước đo thứ hai: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Distinct Matches Played`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)
```
Đặt Format String là `#,##0`.

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để đồng bộ cấu trúc mới vào máy chủ SSAS.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để nhận cấu trúc mới, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc sức chứa sân tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Club.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Stadium Seats.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Greater Than or Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, nhập số 60000 rồi nhấp nút OK để xác nhận.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Club, nhấp giữ chuột trái vào thuộc tính Stadium Name, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong chiều DIM Club, nhấp giữ chuột trái vào thuộc tính Club Name, kéo sang thả vào vị trí ngay bên cạnh cột Stadium Name.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo các thước đo Stadium Capacity Cleaned, Distinct Matches Played và Goals thả vào vùng dữ liệu.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng danh sách các sân vận động quy mô lớn kèm sức chứa, số trận duy nhất và tổng bàn thắng.

---

### 3.10.11.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Club, nhấp giữ chuột trái vào trường Stadium Name, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục DIM Club, nhấp giữ chuột trái vào trường Club Name, kéo chuột xuống phía dưới và thả tiếp vào ô Rows ngay dưới trường Stadium Name.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Stadium Capacity Cleaned, Distinct Matches Played và Goals.

**Bước 2:** Thiết lập bộ lọc sức chứa trên 60.000 khán giả:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Stadium Name.
* ● Di chuột vào mục Value Filters, nhấp chuột chọn dòng lệnh Greater Than Or Equal To...
* ● Trong hộp thoại xuất hiện, chọn lọc theo trường Stadium Capacity Cleaned với giá trị lớn hơn hoặc bằng 60000 rồi nhấp nút OK để áp dụng.

**Bước 3:** Sắp xếp giảm dần theo số trận đấu: Nhấp chuột phải vào một ô số bất kỳ trong cột Distinct Matches Played, di chuột chọn mục Sort rồi nhấp chọn Sort Largest to Smallest.

**Bước 4:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh danh sách các siêu sân vận động bóng đá Châu Âu.

---

### 3.10.11.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích thống kê số trận đấu diễn ra tại sân vận động có sức chứa từ 60.000 khán giả trở lên. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH SET` định nghĩa tập hợp `[ValidStadiums]` lọc các sân có sức chứa lớn hơn hoặc bằng 60000 chỗ.
* ● Mệnh đề `WITH MEMBER` định nghĩa `[Measures].[Stadium Capacity Cleaned]` hiển thị sức chứa và `[Measures].[Distinct Matches Played]` sử dụng hàm `DISTINCTCOUNT` kết hợp từ khóa `EXISTING` đếm số lượng trận đấu duy nhất không bị trùng lặp.
* ● Lựa chọn 3 thước đo hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `ORDER` với cờ `BDESC` sắp xếp danh sách sân theo sức chứa giảm dần trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 11: Số trận đấu diễn ra tại sân vận động có sức chứa trên 60.000 khán giả
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tập hợp các sân vận động quy mô lớn có sức chứa từ 60.000 chỗ trở lên
    SET [ValidStadiums] AS
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] }),
                    EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                    EXCEPT([DIM Club].[Stadium Seats].[Stadium Seats].MEMBERS, { [DIM Club].[Stadium Seats].[0], [DIM Club].[Stadium Seats].[All] })
                ),
                [Measures].[FACT Player Match Perf Count]
            ),
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE >= 60000
        )

    -- 2. Sức chứa sân vận động định dạng chuẩn
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
        FORMAT_STRING = "#,##0 Chỗ"

    -- 3. Đếm số trận đấu duy nhất diễn ra tại sân vận động
    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột COLUMNS: Sức chứa sân đã làm sạch, số trận duy nhất và tổng bàn thắng
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các sân vận động có sức chứa từ 60.000 chỗ trở lên, xếp giảm dần
    ORDER(
        [ValidStadiums],
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về danh sách các siêu sân vận động kèm số trận thực tế và tổng bàn thắng.

---

### 3.10.11.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| STT | Sân Vận Động `Stadium Name` | Câu Lạc Bộ Chủ Quản `Club Name` | Sức Chứa `Stadium Capacity` | Số Trận Đã Diễn Ra `Distinct Matches` | Tổng Bàn Thắng `Goals` |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | **Santiago Bernabéu** | Real Madrid | 83186 Chỗ | 101 | 210 |
| **2** | **SIGNAL IDUNA PARK** | Borussia Dortmund | 81365 Chỗ | 89 | 177 |
| **3** | **Atatürk Olimpiyat** | Fatih Karagümrük | 77563 Chỗ | 72 | 118 |
| **4** | **Giuseppe Meazza** | AC Milan | 75923 Chỗ | 100 | 169 |
| **5** | **Giuseppe Meazza** | Inter Milan | 75923 Chỗ | 97 | 184 |
| **6** | **Allianz Arena** | Bayern Munich | 75000 Chỗ | 90 | 225 |
| **7** | **Old Trafford** | Manchester United | 74879 Chỗ | 94 | 145 |
| **8** | **Olympiastadion Berlin** | Hertha BSC | 74667 Chỗ | 34 | 40 |
| **9** | **La Cartuja** | Real Betis Balompié | 71374 Chỗ | 90 | 111 |
| **10** | **Olimpico di Roma** | Associazione Sportiva Roma | 70634 Chỗ | 105 | 156 |
| **11** | **Olimpico di Roma** | Società Sportiva Lazio | 70634 Chỗ | 97 | 146 |
