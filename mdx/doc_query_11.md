# 3.10.11 Câu truy vấn 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả

**Nội dung truy vấn:** Thống kê danh sách các Sân vận động quy chuẩn quốc tế có sức chứa trên 60.000 chỗ ngồi (`Stadium_Seats >= 60.000`) cùng Câu lạc bộ chủ quản, tổng số bàn thắng ghi được và **số lượng trận đấu duy nhất** (`Distinct Matches Played`) đã từng tổ chức tại các sân đấu này. Ứng dụng hàm `COALESCEEMPTY` để làm sạch dữ liệu khuyết thiếu sức chứa và hàm `DISTINCTCOUNT` kết hợp `EXISTING` để loại trừ việc đếm trùng 22-30 cầu thủ ra sân trong cùng một trận.

## 3.10.11.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo dòng lọc để giới hạn các sân vận động có sức chứa từ 60.000 chỗ ngồi trở lên:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Stadium Seats`** | Bấm dropdown chọn **`Greater Than Or Equal`** ($\ge$) | Gõ số **`60000`** $\rightarrow$ Bấm **OK** (hiển thị `{ >= 60000 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Sân vận động & Câu lạc bộ (Rows):**
   * Mở rộng chiều **`DIM Club`** $\rightarrow$ tìm thuộc tính **`Stadium Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
   * Tìm tiếp thuộc tính **`Club Name`** trong `DIM Club`: Kéo thả vào ngay bên cạnh cột `Stadium Name`.
2. **Kéo Thước đo Sức chứa và Bàn thắng (Measures):**
   * Mở rộng chiều **`DIM Club`** $\rightarrow$ kéo thuộc tính **`Stadium Seats`** vào cạnh cột `Club Name`.
   * Mở rộng thư mục **`Measures`** $\rightarrow$ kéo thước đo **`Goals`** vào vùng dữ liệu trung tâm.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị danh sách các sân vận động khổng lồ của bóng đá Châu Âu (Camp Nou 99.354 chỗ, Wembley 90.000 chỗ, Signal Iduna Park 81.365 chỗ...).
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.11.2 Sử dụng Pivot Excel

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
| **Ô `Rows` (Dòng dữ liệu)** | **`Stadium Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Stadium Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Rows (nằm dưới `Stadium Name`). |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Stadium Seats`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Stadium Seats` thả vào ô Values (chọn `Max of Stadium Seats`). |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |

### Bước 4: Cấu hình Bộ lọc Sức chứa >= 60.000 chỗ
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn **`Greater Than Or Equal To...`**.
3. Trong hộp thoại: Chọn theo **`Max of Stadium Seats`** và nhập số **`60000`** $\rightarrow$ Nhấn **OK**.
4. **Sắp xếp:** Chuột phải vào cột `Max of Stadium Seats` $\rightarrow$ chọn **Sort Largest to Smallest**.
5. Vô thẻ **`Design`** $\rightarrow$ chọn **Report Layout** $\rightarrow$ **`Show in Tabular Form`** $\rightarrow$ **Subtotals** $\rightarrow$ **`Do Not Show Subtotals`**.

---

## 3.10.11.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả
   Khai thác: COALESCEEMPTY, DISTINCTCOUNT, EXISTING, FILTER, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Sức chứa sân vận động xử lý NULL bằng COALESCEEMPTY
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        COALESCEEMPTY(
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE,
            0
        ),
        FORMAT_STRING = "#,##0 Chỗ"

    -- 2. Đếm số trận đấu duy nhất diễn ra tại sân vận động
    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Sức chứa sân đã làm sạch, số trận duy nhất và tổng bàn thắng
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các sân vận động có sức chứa >= 60.000 chỗ, xếp giảm dần
    ORDER(
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] }),
                    EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] })
                ),
                [Measures].[FACT Player Match Perf Count]
            ),
            [Measures].[Stadium Capacity Cleaned] >= 60000
        ),
        [Measures].[Stadium Capacity Cleaned],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE, 0)`**: Hàm kiểm tra giá trị đầu tiên khác rỗng. Nếu thuộc tính `Stadium Seats` bị NULL hoặc rỗng, hàm tự động gán giá trị mặc định là 0 để chống lỗi tính toán số học.
* **`DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`**: Đếm số lượng phần tử duy nhất (Distinct Game ID). Từ khóa `EXISTING` thực hiện chuyển đổi ngữ cảnh để tập hợp `Game ID` chỉ bao gồm các trận diễn ra tại đúng sân vận động và câu lạc bộ đang hiển thị trên dòng đó, ngăn chặn việc đếm trùng 22-30 cầu thủ mỗi trận.
* **`CrossJoin([Stadium Name].MEMBERS, [Club Name].MEMBERS)`**: Kết hợp cặp thuộc tính Tên sân và Tên CLB chủ quản trên trục dòng.
* **`FILTER(NONEMPTY(...), [Measures].[Stadium Capacity Cleaned] >= 60000)`**: Lọc các sân vận động đạt chuẩn quy mô trên 60.000 chỗ ngồi.
* **`ORDER(..., [Measures].[Stadium Capacity Cleaned], BDESC) ON ROWS`**: Sắp xếp danh sách sân vận động theo sức chứa giảm dần toàn cục trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị 16 siêu sân vận động của bóng đá Châu Âu cùng sức chứa, số trận đã diễn ra và tổng bàn thắng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.11.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
