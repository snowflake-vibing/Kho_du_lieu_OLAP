# 3.10.12 Câu truy vấn 12: Thẻ phạt của các đội bóng phân theo Huấn luyện viên trưởng & Tháng trong năm

**Nội dung truy vấn:** Xác định **tháng có số lượng thẻ phạt kỷ lục cao nhất** (tháng cao điểm căng thẳng) của từng Huấn luyện viên trưởng danh tiếng trong năm thi đấu, đi kèm tổng số thẻ vàng (`Yellow Cards`) và thẻ đỏ (`Red Cards`). Ứng dụng hàm lặp tập hợp `GENERATE` kết hợp `TOPCOUNT(..., 1)` giải quyết triệt để bài toán *"Group By Top 1 Per Category"* trong đại số đa chiều, hỗ trợ ban kỷ luật và truyền thông nhận diện thời điểm căng thẳng tâm lý lớn nhất của các HLV.

## 3.10.12.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta áp dụng hàm lặp tập hợp `GENERATE`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Game`** | Nhấp chọn **`Coach Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** mở *Expression Builder*, dán biểu thức `GENERATE` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào Expression Builder ở Dòng 1:*
```mdx
GENERATE(
    FILTER(
        NONEMPTY(
            EXCEPT([DIM Game].[Coach Name].[Coach Name].MEMBERS, { [DIM Game].[Coach Name].[All] }),
            [Measures].[Yellow Cards]
        ),
        [DIM Game].[Coach Name].CURRENTMEMBER.NAME <> "Unknown"
    ),
    TOPCOUNT(
        NONEMPTY(
            CrossJoin(
                { [DIM Game].[Coach Name].CURRENTMEMBER },
                EXCEPT([DIM Time].[Month].[Month].MEMBERS, { [DIM Time].[Month].[All] })
            ),
            [Measures].[Yellow Cards]
        ),
        1,
        [Measures].[Yellow Cards]
    )
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Huấn luyện viên & Tháng (Rows):**
   * Mở rộng chiều **`DIM Game`** $\rightarrow$ tìm thuộc tính **`Coach Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
   * Mở rộng chiều **`DIM Time`** $\rightarrow$ tìm thuộc tính **`Month`**: Kéo thả vào ngay bên cạnh cột `Coach Name`.
2. **Kéo Thước đo Thẻ phạt (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Yellow Cards`**, kéo thả vào ngay bên cạnh cột `Month`.
   * Tiếp tục kéo thước đo **`Red Cards`** vào ngay bên cạnh cột `Yellow Cards`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị mỗi huấn luyện viên đúng duy nhất 1 tháng có số thẻ vàng cao điểm nhất.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.12.2 Sử dụng Pivot Excel

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
| **Ô `Rows` (Dòng dữ liệu)** | **`Coach Name`** | Mở thư mục **`DIM Game`** $\rightarrow$ Kéo `Coach Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Month`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Month` thả vào ô Rows (nằm dưới `Coach Name`). |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Yellow Cards` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Red Cards`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Red Cards` thả vào ô Values. |

### Bước 4: Thiết lập Bộ lọc Top 1 Tháng theo từng HLV trong Excel
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng cấp con **`Month`**.
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn **`Top 10...`**.
3. Trong hộp thoại:
   * Đổi số 10 thành số **`1`**.
   * Chọn theo thước đo **`Sum of Yellow Cards`**.
   * Nhấn **OK**. Excel sẽ tự động thu gọn mỗi HLV chỉ giữ lại đúng 1 tháng có số thẻ vàng cao nhất!
4. Vô thẻ **`Design`** $\rightarrow$ chọn **Report Layout** $\rightarrow$ **`Show in Tabular Form`** $\rightarrow$ **Subtotals** $\rightarrow$ **`Do Not Show Subtotals`**.

---

## 3.10.12.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 12: Thẻ phạt phân theo Huấn luyện viên trưởng & Tháng trong năm
   Khai thác: GENERATE, TOPCOUNT, CURRENTMEMBER, NONEMPTY, FILTER, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Thước đo Thẻ vàng và Thẻ đỏ
    {
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,

    -- Trục Dòng: Duyệt qua từng HLV, tìm đúng 1 tháng có nhiều thẻ vàng nhất
    ORDER(
        GENERATE(
            FILTER(
                NONEMPTY(
                    EXCEPT([DIM Game].[Coach Name].[Coach Name].MEMBERS, { [DIM Game].[Coach Name].[All] }),
                    [Measures].[Yellow Cards]
                ),
                [DIM Game].[Coach Name].CURRENTMEMBER.NAME <> "Unknown"
            ),
            TOPCOUNT(
                NONEMPTY(
                    CrossJoin(
                        { [DIM Game].[Coach Name].CURRENTMEMBER },
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

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`GENERATE(Set1, Set2_Expression)`**: Vòng lặp tập hợp (Set Iteration). Với mỗi HLV thuộc `Set1`, hệ thống thực thi biểu thức `Set2` để tìm ra tháng cao điểm của HLV đó rồi ghép nối kết quả lại thành một tập hợp duy nhất.
* **`TOPCOUNT(CrossJoin({ Coach.CURRENTMEMBER }, Month.MEMBERS), 1, Yellow Cards)`**: Trích xuất chính xác 1 tháng có số thẻ vàng lớn nhất cho HLV hiện hành đang được duyệt bởi hàm `GENERATE`.
* **`CURRENTMEMBER`**: Biến con trỏ tham chiếu đến đối tượng HLV đang được xét trong vòng lặp.
* **`FILTER(NONEMPTY(...), ... <> 'Unknown')`**: Lọc sạch các giá trị khuyết thiếu thông tin HLV trước khi đưa vào vòng lặp.
* **`ORDER(..., [Measures].[Yellow Cards], BDESC) ON ROWS`**: Sắp xếp danh sách kết quả sau khi duyệt `GENERATE` theo thứ tự giảm dần số thẻ vàng trên toàn cục trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị danh sách các HLV cùng tháng kỷ lục thẻ phạt và số thẻ vàng, thẻ đỏ tương ứng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.12.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
