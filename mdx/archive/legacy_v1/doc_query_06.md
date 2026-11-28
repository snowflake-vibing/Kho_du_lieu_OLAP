# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.6 Câu truy vấn 6

**Nội dung truy vấn:** Đánh giá mối tương quan giữa các chỉ số thể hình gồm chiều cao trung bình, chiều cao lớn nhất, chiều cao nhỏ nhất với hiệu suất thi đấu gồm tổng số bàn thắng và tổng số thẻ vàng trên 4 tuyến thi đấu chính gồm tiền đạo, tiền vệ, hậu vệ và thủ môn nhằm phân tích tiêu chí thể hình tối ưu cho từng vai trò trên sân.

### 3.10.6.1 Sử dụng Cube Browser

**Bước 1:** Trong trình thiết kế cube `DW Football Transfermarkt.cube`, nhấp chuột vào tab **Calculations** ở mép trên để khởi tạo tập hợp và 3 thước đo tính toán thể hình:
* ● Khởi tạo tập hợp ValidPlayers: Nhấp chuột phải vào khung Script Organizer, chọn New Named Set. Đặt Name là `ValidPlayers`, tại ô Expression nhập biểu thức kết hợp tên cầu thủ và chiều cao đã có dữ liệu thi đấu:
```mdx
NONEMPTY(
    EXISTING CrossJoin(
        [DIM Player].[Player Name].[Player Name].MEMBERS,
        [DIM Player].[Height In Cm].[Height In Cm].MEMBERS
    ),
    [Measures].[FACT Player Match Perf Count]
)
```
* ● Thước đo thứ nhất: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Avg Height Cm`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
ROUND(AVG([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE), 1)
```
* ● Thước đo thứ hai: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Max Height Cm`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
MAX([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)
```
* ● Thước đo thứ ba: Nhấp chuột phải vào khung Script Organizer, chọn New Calculated Member. Đặt Name là `Min Height Cm`, đặt Parent hierarchy là `Measures`, tại ô Expression nhập biểu thức:
```mdx
MIN([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)
```

**Bước 2:** Trên thanh menu công cụ của Visual Studio, chọn menu Build rồi nhấp chọn Deploy Solution để đồng bộ tập hợp và các thước đo mới vào cấu trúc Cube.

**Bước 3:** Chuyển sang tab **Browser** trên thanh tab của trình thiết kế Cube Designer. Quan sát thanh công cụ phía trên tab Browser, nhấp chuột vào nút Reconnect để nhận các thước đo mới, sau đó nhấp chọn biểu tượng **Design Mode** có hình lưới màu xanh và cây thước kẻ màu vàng để chuyển sang giao diện thiết kế đồ họa trực quan.

**Bước 4:** Thiết lập bộ lọc loại bỏ giá trị Missing tại dòng thứ nhất trong vùng bộ lọc Filter Pane ở phía trên:
* ● Nhấp chuột vào ô tại cột Dimension, mở danh sách thả xuống và nhấp chọn chiều DIM Player.
* ● Nhấp chuột sang ô tại cột Hierarchy cùng dòng, mở danh sách thả xuống và nhấp chọn Hierarchy Main Position.
* ● Tại cột Operator, nhấp mở danh sách thả xuống và chọn toán tử Not Equal.
* ● Nhấp chuột vào ô tại cột Filter Expression, tích chọn giá trị Missing rồi nhấp nút OK để loại bỏ.

**Bước 5:** Kéo thả các trường dữ liệu vào lưới Data Grid:
* ● Trong khung Metadata ở bên trái màn hình, mở rộng thư mục chiều DIM Player, nhấp giữ chuột trái vào thuộc tính Main Position, kéo con trỏ chuột sang khu vực lưới dữ liệu Data Grid bên phải và thả chuột vào vùng Rows.
* ● Tiếp tục trong khung Metadata, mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái và kéo các thước đo thả vào khu vực dữ liệu bên cạnh cột Main Position theo thứ tự gồm Avg Height Cm, Max Height Cm, Min Height Cm, Goals và Yellow Cards.

**Bước 6:** Nhấp chuột vào dòng chữ màu xanh Click to execute the query trên lưới dữ liệu hoặc nhấn biểu tượng Execute có hình dấu chấm than màu đỏ trên thanh công cụ phía trên. Lưới dữ liệu lập tức hiển thị bảng 4 dòng tuyến thi đấu và 5 cột chỉ số thể hình cùng hiệu suất thi đấu.

---

### 3.10.6.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ danh sách trường PivotTable Fields ở cạnh phải màn hình Excel, thao tác kéo thả các trường vào từng khu vực:
* ● Mở rộng thư mục DIM Player, nhấp giữ chuột trái vào trường Main Position, kéo chuột xuống phía dưới và thả vào ô Rows.
* ● Mở rộng thư mục Measures, lần lượt nhấp giữ chuột trái vào các thước đo kéo thả vào ô Values gồm Avg Height Cm, Max Height Cm, Min Height Cm, Goals và Yellow Cards.

**Bước 2:** Thiết lập lọc và sắp xếp trên bảng PivotTable:
* ● Trên trang tính Excel, nhấp chuột vào nút mũi tên lọc tại ô tiêu đề A4 nhãn Row Labels của cột Main Position, bỏ chọn giá trị Missing để giữ lại đúng 4 vị trí chính rồi nhấp nút OK.
* ● Nhấp chuột phải vào một ô số bất kỳ trong cột Goals, di chuột chọn mục Sort rồi nhấp chọn Sort Largest to Smallest để sắp xếp theo số bàn thắng giảm dần.

**Bước 3:** Trang tính Excel hiển thị bảng PivotTable hoàn chỉnh gồm 4 tuyến thi đấu chính với đầy đủ 5 cột chỉ số thể hình và thi đấu, đồng bộ tuyệt đối với Cube Browser và MDX.

---

### 3.10.6.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Trong cửa sổ Object Explorer của phần mềm SQL Server Management Studio, mở rộng cơ sở dữ liệu DW Football SSAS, mở rộng thư mục Cubes, nhấp chuột phải vào khối Cube DW Football Transfermarkt, di chuột chọn New Query rồi nhấp chuột chọn MDX để mở trình soạn thảo truy vấn.

**Bước 2:** Nhấp chuột vào khung soạn thảo MDX và viết truy vấn với mục đích khảo sát thể hình và hiệu suất theo vị trí chính. Truy vấn chỉ định rõ các mệnh đề:
* ● Mệnh đề `WITH SET` định nghĩa tập hợp `[ValidPlayers]` tạo các cặp Cầu thủ và Chiều cao có phát sinh dữ liệu thi đấu bằng hàm `CrossJoin` và `NONEMPTY`.
* ● Mệnh đề `WITH MEMBER` tính toán 3 chỉ số thể hình gồm `[Measures].[Avg Height Cm]` dùng hàm `AVG`, `[Measures].[Max Height Cm]` dùng hàm `MAX`, và `[Measures].[Min Height Cm]` dùng hàm `MIN`.
* ● Lựa chọn 5 thước đo hiển thị trên trục cột COLUMNS.
* ● Sử dụng hàm `EXCEPT` loại bỏ giá trị Missing và nút All trên chiều `[DIM Player].[Main Position]`, kết hợp hàm `ORDER` với cờ `BDESC` để sắp xếp giảm dần theo số bàn thắng trên trục hàng ROWS.
* ● Truy vấn dữ liệu từ khối Cube nguồn `[DW Football Transfermarkt]`.

```mdx
/* ==============================================================================
   Truy vấn MDX 06: Thể hình AVG, MAX, MIN và hiệu suất theo vị trí chính
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tập hợp các cặp Cầu thủ và Chiều cao có dữ liệu thi đấu theo ngữ cảnh
    SET [ValidPlayers] AS
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                [DIM Player].[Height In Cm].[Height In Cm].MEMBERS
            ),
            [Measures].[FACT Player Match Perf Count]
        )

    -- 2. Chiều cao trung bình theo vị trí thi đấu
    MEMBER [Measures].[Avg Height Cm] AS
        ROUND(
            AVG(
                [ValidPlayers],
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
            ),
            1
        ),
        FORMAT_STRING = "#,##0.0"

    -- 3. Chiều cao lớn nhất theo vị trí thi đấu
    MEMBER [Measures].[Max Height Cm] AS
        MAX(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

    -- 4. Chiều cao nhỏ nhất theo vị trí thi đấu
    MEMBER [Measures].[Min Height Cm] AS
        MIN(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột COLUMNS: Các chỉ số thống kê thể hình và kết quả thi đấu
    {
        [Measures].[Avg Height Cm],
        [Measures].[Max Height Cm],
        [Measures].[Min Height Cm],
        [Measures].[Goals],
        [Measures].[Yellow Cards]
    } ON COLUMNS,

    -- Trục Dòng ROWS: Các vị trí chính hợp lệ, sắp xếp theo số bàn thắng giảm dần
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].[Missing], [DIM Player].[Main Position].[All] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bước 3:** Kiểm tra thanh công cụ phía trên đảm bảo ô chọn cơ sở dữ liệu đang trỏ đúng vào DW Football SSAS. Nhấp chuột vào nút Execute có biểu tượng hình dấu chấm than màu đỏ trên thanh công cụ hoặc nhấn phím F5 trên bàn phím.

**Bước 4:** Quan sát kết quả trong tab Results ở khung phía dưới màn hình. Hệ thống trả về ma trận dữ liệu phân tích chi tiết thể hình và thành tích thi đấu của 4 tuyến trên sân cỏ.

---

### 3.10.6.4 Nhận xét

Cả 3 cách gồm duyệt cube trong SSAS, dùng PivotTable trong Excel và viết truy vấn MDX đều trả về cùng một kết quả dữ liệu chính xác tuyệt đối.

| Tuyến Thi Đấu `Main Position` | Chiều Cao Trung Bình `Avg Height Cm` | Chiều Cao Lớn Nhất `Max Height Cm` | Chiều Cao Nhỏ Nhất `Min Height Cm` | Tổng Bàn Thắng `Goals` | Thẻ Vàng `Yellow Cards` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Attack** | 180.9 | 201 | 160 | 11561 | 6292 |
| **Midfield** | 180.2 | 202 | 160 | 5000 | 10050 |
| **Defender** | 183.9 | 206 | 163 | 2610 | 11551 |
| **Goalkeeper** | 190.5 | 206 | 179 | 2 | 801 |
