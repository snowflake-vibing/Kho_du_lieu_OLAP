# 3.10.1 Câu truy vấn 1: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024

**Nội dung truy vấn:** Xác định danh sách 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh (Premier League - Mã giải đấu: `GB1`) trong mùa giải 2023/2024. Phân tích này giúp ban chuyên môn và nhà quản lý nhận diện các tiền đạo có hiệu suất làm bàn xuất sắc nhất, phục vụ công tác chuyển nhượng và đánh giá phong độ.

## 3.10.1.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer
1. Khởi động **Visual Studio**, mở Solution chứa dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Trong cửa sổ **Solution Explorer** (khung bên phải):
   * Mở rộng thư mục **`Cubes`**.
   * Nhấp đúp chuột vào tệp khối đa chiều: **`DW_Football_Cube.cube`** (hoặc `DW Football Transfermarkt.cube`).
3. Màn hình Cube Designer xuất hiện với các tab chức năng ở cạnh trên (*Cube Structure*, *Dimension Usage*, *Calculations*, *Partitions*, *Browser*...).

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt Chế độ Thiết kế (Design Mode)
1. Nhấp chọn tab **`Browser`** (tab ngoài cùng bên phải của trình thiết kế Cube).
2. **Kiểm tra trạng thái kết nối & giao diện:**
   * Nếu nút **Reconnect** (biểu tượng 2 phích cắm ở góc trên bên trái) sáng lên: Nhấp vào để kết nối tới SSAS Database.
   * Nếu màn hình đang ở chế độ soạn thảo văn bản thuần (Text Mode): Nhấp vào biểu tượng **`Design Mode`** (hình chiếc Lưới màu xanh có cây thước kẻ/bút chì màu vàng, nằm cạnh nút Stop xám) để chuyển sang giao diện thiết kế đồ họa trực quan (Graphical Query Designer). Khi đó, màn hình sẽ chia làm 2 phần: **Bảng lọc (Filter Pane)** ở trên và **Lưới dữ liệu (Data Grid)** ở dưới.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo lần lượt 3 dòng lọc để cố định giải đấu, mùa giải và áp dụng thuật toán Top 10:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Competition`** | Nhấp chọn **`Competition ID`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn mã **`GB1`** $\rightarrow$ Bấm **OK** (hiển thị `{ GB1 }`) |
| **Dòng 2** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Season`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn mùa **`2023`** (hoặc `2023/2024`) $\rightarrow$ Bấm **OK** |
| **Dòng 3** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Player Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 3:*
```mdx
TOPCOUNT([DIM Player].[Player Name].[Player Name].MEMBERS, 10, [Measures].[Goals])
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Player Name`**.
   * Nhấp giữ chuột vào **`Player Name`**, kéo và thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*. Lúc này trên lưới xuất hiện cột `Player Name`.
2. **Kéo Thước đo Bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo và thả vào **ngay bên cạnh cột `Player Name`** trên lưới.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than màu đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị chính xác bảng xếp hạng đúng **10 cầu thủ ghi bàn nhiều nhất** (Erling Haaland dẫn đầu với 27 bàn, Cole Palmer 22 bàn...).
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.1.2 Sử dụng Pivot Excel

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
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Competition ID`** | Mở thư mục **`DIM Competition`** $\rightarrow$ Kéo `Competition ID` thả vào ô Filters. |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Season`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Season` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Player Name`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Player Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values (hiển thị `Sum of Goals`). |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. **Lọc Giải đấu:** Tại ô **`B1`** (bên cạnh nhãn `Competition ID`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn mã giải **`GB1`** $\rightarrow$ Nhấn **OK**.
2. **Lọc Mùa giải:** Tại ô **`B2`** (bên cạnh nhãn `Season`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn mùa bóng **`2023/2024`** $\rightarrow$ Nhấn **OK**.

### Bước 5: Cấu hình Bộ lọc Top 10 Vua phá lưới
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại **Top 10 Filter (Player Name)**:
   * Ô thứ nhất: Chọn **`Top`**.
   * Ô thứ hai: Nhập số **`10`**.
   * Ô thứ ba: Chọn **`Items`**.
   * Ô thứ tư (By): Chọn thước đo **`Sum of Goals`**.
4. Nhấn **OK**.

### Bước 6: Trình bày bảng kết quả
* Vô thẻ ngữ cảnh **`Design`** trên Ribbon $\rightarrow$ chọn **Report Layout** $\rightarrow$ chọn **`Show in Tabular Form`** (để tiêu đề cột đổi thành `Player Name`).
* Chọn **Grand Totals** $\rightarrow$ chọn **`Off for Rows and Columns`** để ẩn dòng tổng cộng, giữ lại đúng bảng xếp hạng 10 cầu thủ.

---

## 3.10.1.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Trích xuất thước đo Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng (ROWS): Xếp hạng và lấy đúng 10 cầu thủ ghi nhiều bàn nhất
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

-- Trục lát cắt ngữ cảnh (Slicer Axis): Giới hạn trong giải GB1 và mùa 2023/2024
WHERE (
    [DIM Competition].[Competition ID].[GB1],
    [DIM Time].[Season].[2023/2024]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT`**: Khởi tạo khai báo các trục tọa độ trả về của ma trận kết quả.
* **`{ [Measures].[Goals] } ON COLUMNS`**: Chọn thước đo bàn thắng (`Goals`) và định vị hiển thị trên trục **CỘT** (Axis 0).
* **`TOPCOUNT(...) ON ROWS`**: Sử dụng hàm `TOPCOUNT` để lọc lấy đúng 10 thành viên có giá trị số bàn thắng cao nhất và hiển thị trên trục **HÀNG** (Axis 1).
* **`NONEMPTY(...)`**: Loại bỏ trước các cầu thủ không ghi bàn nào trong phạm vi giải đấu và mùa giải đã chọn, giúp thu hẹp tập dữ liệu duyệt.
* **`FROM [DW Football Transfermarkt]`**: Chỉ định nguồn dữ liệu được truy xuất từ khối Cube đa chiều `[DW Football Transfermarkt]`.
* **`WHERE (...)`**: Trục lát cắt ngữ cảnh (Slicer Axis), cố định phạm vi tính toán tại giải đấu Ngoại Hạng Anh (`GB1`) và mùa giải `2023/2024`.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị lưới kết quả ma trận đa chiều với 10 dòng tên cầu thủ và 1 cột số bàn thắng `Goals`.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.1.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
