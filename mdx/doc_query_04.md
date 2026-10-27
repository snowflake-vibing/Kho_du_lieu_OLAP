# 3.10.4 Câu truy vấn 4: Bàn thắng, kiến tạo & số phút thi đấu trung bình phân theo độ tuổi năm 2023

**Nội dung truy vấn:** Khảo sát sự phân bố hiệu suất ghi bàn (`Goals`), kiến tạo (`Assists`) và thời lượng thi đấu trung bình mỗi trận (`Avg Minutes Played`) theo từng độ tuổi cầu thủ (`Age`) trong năm 2023. Đồng thời áp dụng cấu trúc rẽ nhánh `CASE WHEN` để phân loại cầu thủ vào 3 giai đoạn sự nghiệp: Tài năng trẻ (U21), Độ tuổi đỉnh cao (Prime 22-29), và Lão tướng (Veteran 30+), giúp phân tích chu kỳ phát triển của vận động viên.

## 3.10.4.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc để cố định năm dương lịch 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** $\rightarrow$ Bấm **OK** (hiển thị `{ 2023 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Độ tuổi (Rows):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Age`**.
   * Nhấp giữ chuột vào **`Age`**, kéo và thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo các Thước đo Hiệu suất (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào ngay bên cạnh cột `Age`.
   * Tiếp tục kéo thước đo **`Assists`** vào ngay bên cạnh cột `Goals`.
   * Tiếp tục kéo thước đo **`Minutes Played`** vào ngay bên cạnh cột `Assists`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị bảng phân bổ tổng số bàn thắng, kiến tạo và số phút thi đấu theo từng độ tuổi từ 16 đến 42 tuổi.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.4.2 Sử dụng Pivot Excel

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
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Year` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Age`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Age` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Assists`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Assists` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Minutes Played`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Minutes Played` thả vào ô Values. |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Year`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn năm **`2023`** $\rightarrow$ Nhấn **OK**.

### Bước 5: Tạo Calculated Field tính Số phút trung bình trong Excel
1. Chọn một ô bất kỳ bên trong bảng PivotTable.
2. Vô thẻ ngữ cảnh **`PivotTable Analyze`** trên thanh Ribbon $\rightarrow$ nhóm *Calculations* $\rightarrow$ chọn **`Fields, Items & Sets`** $\rightarrow$ chọn **`Calculated Field...`**.
3. Thiết lập thông số:
   * **Name:** Ghi `Avg Minutes Per Match`
   * **Formula:** Nhập `='Minutes Played' / 'FACT Player Match Perf Count'`
4. Nhấn **OK**. Cột số phút trung bình sẽ được tự động tính và hiển thị lên bảng.

### Bước 6: Sắp xếp và Định dạng hiển thị
* Chuột phải vào cột `Age` $\rightarrow$ chọn **Sort** $\rightarrow$ chọn **`Sort Smallest to Largest`** để xem biểu đồ phát triển từ trẻ đến kỳ cựu.
* Vô thẻ **`Design`** $\rightarrow$ chọn **Report Layout** $\rightarrow$ **`Show in Tabular Form`**.

---

## 3.10.4.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 04: Hiệu suất bàn thắng, kiến tạo & phút thi đấu theo độ tuổi
   Khai thác: WITH MEMBER, CASE WHEN, IIF, ROUND, FILTER, ORDER
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tính số phút trung bình mỗi lần ra sân
    MEMBER [Measures].[Avg Minutes Played] AS
        IIF(
            IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
            NULL,
            ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
        ),
        FORMAT_STRING = "#,##0.00"

    -- 2. Phân loại giai đoạn sự nghiệp bằng CASE WHEN
    MEMBER [Measures].[Career Stage Group] AS
        CASE 
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 21 THEN "U21 Young Talent"
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 29 THEN "Prime Age (22-29)"
            ELSE "Veteran (30+)"
        END

SELECT
    -- Trục Cột: Các chỉ số hiệu suất và phân loại nhóm tuổi
    {
        [Measures].[Career Stage Group],
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng: Các độ tuổi hợp lệ, sắp xếp tăng dần từ 16 đến 42
    ORDER(
        FILTER(
            [DIM Player].[Age].[Age].MEMBERS,
            NOT ISEMPTY([DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE) 
            AND [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE > 0
        ),
        [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE,
        BASC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Năm dương lịch 2023
WHERE (
    [DIM Time].[Year].[2023]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`WITH MEMBER [Measures].[Avg Minutes Played]`**: Khai báo thành viên tính toán nội bộ trong phiên truy vấn. Sử dụng hàm `IIF` xử lý mẫu số bằng 0/NULL để tránh chia cho 0 và hàm `ROUND(..., 2)` để định dạng số thập phân.
* **`WITH MEMBER [Measures].[Career Stage Group]`**: Sử dụng cấu trúc rẽ nhánh `CASE WHEN` dựa trên giá trị số học `MEMBERVALUE` của chiều tuổi để tự động phân nhóm sự nghiệp cho cầu thủ.
* **`SELECT { ... } ON COLUMNS`**: Đưa nhóm tuổi sự nghiệp và các chỉ số đo lường hiệu suất lên trục **CỘT** (Axis 0).
* **`ORDER(FILTER(...), BASC) ON ROWS`**: Lọc bỏ các dòng có độ tuổi bằng 0 hoặc bị khuyết thiếu (`ISEMPTY`), sau đó sắp xếp độ tuổi tăng dần (`BASC` - Break Hierarchy Ascending) trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Nguồn khối Cube đa chiều phân tích.
* **`WHERE ([DIM Time].[Year].[2023])`**: Trục lát cắt dữ liệu (Slicer Axis), giới hạn phạm vi tính toán trong năm dương lịch 2023.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận phân bổ hiệu suất theo từng độ tuổi kèm cột phân nhóm giai đoạn sự nghiệp.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.4.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
