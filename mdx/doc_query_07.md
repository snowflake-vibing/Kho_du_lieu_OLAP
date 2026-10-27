# 3.10.7 Câu truy vấn 7: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu thuộc Nước Anh

**Nội dung truy vấn:** Xác định nhóm các quốc gia có cầu thủ đóng góp vào **80% tổng số bàn thắng** được ghi tại tất cả các giải đấu bóng đá diễn ra trên lãnh thổ Nước Anh (`Country_Name = 'England'`). Ứng dụng nguyên lý Pareto $80/20$ giúp liên đoàn bóng đá và các câu lạc bộ đánh giá thị trường xuất khẩu cầu thủ chủ lực, phục vụ chiến lược cấp giấy phép lao động (Work Permit) và chính sách ngoại binh.

## 3.10.7.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định các giải đấu tại Nước Anh và áp dụng hàm `TOPPERCENT`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Competition`** | Nhấp chọn **`Country Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`England`** $\rightarrow$ Bấm **OK** (hiển thị `{ England }`) |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Country Of Citizenship`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** mở *Expression Builder*, dán biểu thức `TOPPERCENT` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào Expression Builder ở Dòng 2:*
```mdx
TOPPERCENT(
    NONEMPTY(
        EXCEPT([DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS, { [DIM Player].[Country Of Citizenship].[All] }),
        ([Measures].[Goals], [DIM Competition].[Country Name].[England])
    ),
    80,
    [Measures].[Goals]
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Quốc tịch (Rows):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Country Of Citizenship`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Thước đo Bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào ngay bên cạnh cột `Country Of Citizenship`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị nhóm các quốc gia dẫn đầu chiếm 80% số bàn thắng tại Nước Anh.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.7.2 Sử dụng Pivot Excel

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
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Country Name`** | Mở thư mục **`DIM Competition`** $\rightarrow$ Kéo `Country Name` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Country Of Citizenship`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Country Of Citizenship` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Country Name`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn **`England`** $\rightarrow$ Nhấn **OK**.

### Bước 5: Cấu hình Bộ lọc Top 80 Percent (Pareto Filter)
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại **Top 10 Filter (Country Of Citizenship)**:
   * Ô thứ nhất: Chọn **`Top`**.
   * Ô thứ hai: Nhập số **`80`**.
   * Ô thứ ba: Bấm dropdown đổi từ `Items` sang **`Percent`**.
   * Ô thứ tư (By): Chọn thước đo **`Sum of Goals`**.
4. Nhấn **OK**. Excel sẽ áp dụng chính xác thuật toán Pareto $80\%$ và chỉ giữ lại nhóm quốc gia tích lũy đủ $80\%$ bàn thắng.
5. **Sắp xếp:** Chuột phải vào cột `Sum of Goals` $\rightarrow$ chọn **Sort Largest to Smallest**.

---

## 3.10.7.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 07: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu ở Anh
   Khai thác: TOPPERCENT, NONEMPTY, EXCEPT, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tổng số bàn thắng của toàn bộ giải đấu tại Anh
    MEMBER [Measures].[England Total Goals] AS
        (
            [Measures].[Goals],
            [DIM Player].[Country Of Citizenship].[All],
            [DIM Competition].[Country Name].[England]
        )

    -- 2. Tỷ lệ phần trăm đóng góp bàn thắng của từng quốc gia
    MEMBER [Measures].[Pct Of England Goals] AS
        IIF(
            ISEMPTY([Measures].[England Total Goals]) OR [Measures].[England Total Goals] = 0,
            NULL,
            ROUND(([Measures].[Goals] / [Measures].[England Total Goals]) * 100, 2)
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột: Tổng số bàn thắng và Tỷ lệ phần trăm đóng góp
    {
        [Measures].[Goals],
        [Measures].[Pct Of England Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các quốc gia chiếm 80% tổng số bàn thắng, xếp giảm dần
    ORDER(
        TOPPERCENT(
            NONEMPTY(
                EXCEPT(
                    [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                    { [DIM Player].[Country Of Citizenship].[All] }
                ),
                (
                    [Measures].[Goals],
                    [DIM Competition].[Country Name].[England]
                )
            ),
            80,
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Các giải đấu diễn ra tại Nước Anh
WHERE (
    [DIM Competition].[Country Name].[England]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`WITH MEMBER [Measures].[England Total Goals]`**: Tính tổng số bàn thắng toàn thể tại Nước Anh bằng cách kết hợp tọa độ giao cắt `(Goals, [All] Country, [England])`.
* **`WITH MEMBER [Measures].[Pct Of England Goals]`**: Tính tỷ trọng đóng góp của từng quốc gia so với tổng bàn thắng toàn giải, định dạng phần trăm `0.00%`.
* **`TOPPERCENT(Set, 80, [Measures].[Goals])`**: Thuật toán Pareto tự động tính toán tổng tích lũy từ quốc gia có nhiều bàn thắng nhất đi xuống và dừng lại khi chạm ngưỡng $80\%$.
* **`NONEMPTY(EXCEPT(...), Tuple)`**: Loại bỏ nút tổng hợp `[All]` và lọc sạch các quốc gia không có bàn thắng nào tại Anh trước khi tính tổng tích lũy phần trăm, đảm bảo mẫu số chính xác tuyệt đối.
* **`ORDER(..., BDESC) ON ROWS`**: Sắp xếp danh sách các quốc gia thuộc Top 80% theo thứ tự giảm dần số bàn thắng trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.
* **`WHERE ([DIM Competition].[Country Name].[England])`**: Trục lát cắt dữ liệu (Slicer Axis), định vị ngữ cảnh phân tích tại Nước Anh.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị danh sách 13 quốc gia dẫn đầu chiếm $81.66\%$ tổng bàn thắng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.7.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
