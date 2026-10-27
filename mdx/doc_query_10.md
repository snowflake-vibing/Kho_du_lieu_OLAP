# 3.10.10 Câu truy vấn 10: Thống kê bàn thắng của Real Madrid vào lưới các đối thủ theo từng Quý trong năm

**Nội dung truy vấn:** Phân tích sự biến động số bàn thắng ghi được của Câu lạc bộ **Real Madrid** vào lưới các đối thủ cạnh tranh qua từng Quý trong năm 2023 (từ Quý 1 đến Quý 4). Đồng thời ứng dụng hàm phân cấp thời gian `PREVMEMBER` để tính tỷ lệ tăng trưởng bàn thắng so với Quý liền trước (**Quarter-over-Quarter - QoQ Growth**), hỗ trợ ban huấn luyện nhận diện đối thủ kỵ dơ và đánh giá điểm rơi phong độ của đội bóng.

## 3.10.10.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Trong cửa sổ **Solution Explorer** (khung bên phải):
   * Mở rộng thư mục **`Cubes`**.
   * Nhấp đúp chuột vào tệp khối đa chiều: **`DW_Football_Cube.cube`** (hoặc `DW Football Transfermarkt.cube`).
3. Màn hình Cube Designer xuất hiện với các tab chức năng ở cạnh trên (*Cube Structure*, *Dimension Usage*, *Calculations*, *Partitions*, *Browser*...).

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (tab ngoài cùng bên phải của trình thiết kế Cube).
2. **Kiểm tra trạng thái kết nối & giao diện:**
   * Nếu nút **Reconnect** (biểu tượng 2 phích cắm ở góc trên bên trái) sáng lên: Nhấp vào để kết nối tới SSAS Database.
   * Nếu màn hình đang ở chế độ soạn thảo văn bản thuần (Text Mode): Nhấp vào biểu tượng **`Design Mode`** (hình chiếc Lưới màu xanh có cây thước kẻ/bút chì màu vàng, nằm cạnh nút Stop xám) để chuyển sang giao diện thiết kế đồ họa trực quan (Graphical Query Designer). Khi đó, màn hình sẽ chia làm 2 phần: **Bảng lọc (Filter Pane)** ở trên và **Lưới dữ liệu (Data Grid)** ở dưới.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định đội bóng Real Madrid và năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`Real Madrid`** $\rightarrow$ Bấm **OK** (hiển thị `{ Real Madrid }`) |
| **Dòng 2** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** $\rightarrow$ Bấm **OK** (hiển thị `{ 2023 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Câu lạc bộ Đối thủ (Rows):**
   * Mở rộng chiều **`Opponent Club`** $\rightarrow$ tìm thuộc tính **`Club Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Phân cấp Quý (Columns):**
   * Mở rộng thư mục **`DIM Time`** $\rightarrow$ mở rộng phân cấp **`Hierarchy Time`** $\rightarrow$ tìm cấp độ **`Quarter`**: Kéo thả lên vùng cột (Columns) để chia bảng theo các Quý (Q1, Q2, Q3, Q4).
3. **Kéo Thước đo Bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào vùng dữ liệu trung tâm (Totals).

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận phân bổ bàn thắng của Real Madrid vào lưới từng đối thủ qua các Quý năm 2023.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.10.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon.
3. Trong nhóm lệnh *Get & Transform Data* (hoặc *Get External Data*):
   * Nhấp chọn **`Get Data`** $\rightarrow$ chọn **`From Database`** $\rightarrow$ chọn **`From Analysis Services`**.
4. Cửa sổ **Data Connection Wizard** xuất hiện:
   * **Server name:** Nhập `localhost` (hoặc tên máy tính / instance SSAS).
   * **Log on credentials:** Chọn **`Use Windows Authentication`**.
   * Nhấn nút **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Tại màn hình *Select Database and Table*:
   * Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** (hoặc tên database SSAS tương ứng).
   * Chọn Cube: **`DW Football Transfermarkt`** (hoặc `DW_Football_Cube`).
2. Nhấn nút **Finish**.
3. Hộp thoại **Import Data** hiện lên:
   * Chọn dạng hiển thị: Tích chọn **`PivotTable Report`**.
   * Vị trí đặt bảng: Chọn ô **`=$A$3`** của Sheet hiện tại $\rightarrow$ Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Filters (chọn `Real Madrid`). |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Year` thả vào ô Filters (chọn `2023`). |
| **Ô `Columns` (Cột ma trận)** | **`Quarter`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Quarter` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`Opponent Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals` (lần 2)** | Kéo tiếp `Goals` vào ô Values để tính tăng trưởng Quý liền trước. |

### Bước 4: Thiết lập Tính toán Tăng trưởng Quý (% Difference From)
1. Tại ô `Sum of Goals 2` trên bảng tính, nhấp chuột phải $\rightarrow$ chọn **`Show Values As`** $\rightarrow$ chọn **`% Difference From...`**.
2. Trong hộp thoại:
   * **Base field:** Chọn **`Quarter`**.
   * **Base item:** Chọn **`(previous)`**.
3. Nhấn **OK**. Excel sẽ tự động tính toán cột tăng trưởng QoQ Growth so sánh giữa Quý này với Quý liền trước.

---

## 3.10.10.3 Sử dụng ngôn ngữ MDX

### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động phần mềm **SQL Server Management Studio (SSMS)**.
2. Tại hộp thoại kết nối máy chủ:
   * **Server type:** Nhấp chọn **`Analysis Services`**.
   * **Server name:** Nhập `localhost` (hoặc tên máy tính / instance SSAS).
   * **Authentication:** Chọn **`Windows Authentication`**.
   * Nhấn nút **Connect**.
3. Trong cửa sổ **Object Explorer** (bên trái):
   * Mở rộng thư mục **`Databases`** $\rightarrow$ mở rộng database **`DW_Football_SSAS`** $\rightarrow$ mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** $\rightarrow$ chọn **`New Query`** $\rightarrow$ chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 10: Tăng trưởng bàn thắng Real Madrid vào lưới đối thủ qua các Quý
   Khai thác: PREVMEMBER, DESCENDANTS, CHILDREN, IIF, NONEMPTY, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Bàn thắng của Quý liền trước (Quarter-over-Quarter Prior)
    MEMBER [Measures].[Prev Quarter Goals] AS
        (
            [Measures].[Goals],
            [DIM Time].[Hierarchy Time].CURRENTMEMBER.PREVMEMBER
        ),
        FORMAT_STRING = "#,##0"

    -- 2. Tỷ lệ tăng trưởng so với Quý liền trước (QoQ Goals Growth %)
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                (([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100,
                2
            )
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột: Các Quý của năm 2023 kết hợp với Bàn thắng và Tăng trưởng QoQ
    CrossJoin(
        DESCENDANTS(
            [DIM Time].[Hierarchy Time].[Year].[2023],
            [DIM Time].[Hierarchy Time].[Quarter]
        ),
        {
            [Measures].[Goals],
            [Measures].[QoQ Goals Growth]
        }
    ) ON COLUMNS,

    -- Trục Dòng: Các đối thủ từng bị Real Madrid chọc thủng lưới, xếp giảm dần
    ORDER(
        NONEMPTY(
            EXCEPT([Opponent Club].[Club Name].[Club Name].MEMBERS, { [Opponent Club].[Club Name].[All] }),
            (
                [Measures].[Goals],
                [DIM Club].[Club Name].[Real Madrid]
            )
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Đội ghi bàn là Real Madrid
WHERE (
    [DIM Club].[Club Name].[Real Madrid]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`[DIM Time].[Hierarchy Time].CURRENTMEMBER.PREVMEMBER`**: Trả về thành viên thời gian liền kề trước đó trong cùng cấp bậc phân cấp. Ví dụ: khi đang ở `Quarter 2`, hàm sẽ tự động lấy giá trị của `Quarter 1`.
* **`IIF(ISEMPTY(...) OR ... = 0, NULL, ...)`**: Hàm điều kiện ngăn ngừa chia cho 0 khi Quý trước không có bàn thắng hoặc khi ở Quý 1 đầu năm (chưa có kỳ trước đó).
* **`DESCENDANTS([Hierarchy Time].[Year].[2023], [Quarter])`**: Trích xuất toàn bộ các nút con ở cấp độ `Quarter` trực thuộc năm 2023 mà không cần liệt kê thủ công từng Quý.
* **`CrossJoin(...) ON COLUMNS`**: Kết hợp 4 Quý với 2 thước đo (Bàn thắng và Tăng trưởng QoQ) trên trục **CỘT** (Axis 0).
* **`ORDER(NONEMPTY(...), Goals, BDESC) ON ROWS`**: Sắp xếp danh sách các CLB đối thủ giảm dần theo tổng số bàn thua phải nhận từ Real Madrid trên trục **HÀNG** (Axis 1).
* **`WHERE ([DIM Club].[Club Name].[Real Madrid])`**: Trục lát cắt dữ liệu (Slicer Axis), cố định đội bóng thực hiện ghi bàn là Real Madrid.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận phân bổ bàn thắng theo Quý và tăng trưởng QoQ của các đối thủ cạnh tranh với Real Madrid.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.10.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
