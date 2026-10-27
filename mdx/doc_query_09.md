# 3.10.9 Câu truy vấn 9: So sánh hiệu năng & thẻ phạt Sân nhà vs Sân khách giữa Cuối tuần & Ngày thường

**Nội dung truy vấn:** Xác định danh sách các Câu lạc bộ bóng đá toàn diện hàng đầu xuất hiện đồng thời trong cả hai nhóm: **Top 30 CLB ghi bàn nhiều nhất trên Sân Nhà** và **Top 30 CLB ghi bàn nhiều nhất trên Sân Khách** (`Is_Home_Game` = 1 và 0). Ứng dụng phép toán giao tập hợp (`INTERSECT`) giúp lọc ra những đội bóng có bản lĩnh thi đấu đồng đều đỉnh cao (Elite Clubs), duy trì sức tấn công hủy diệt bất kể yếu tố địa lợi.

## 3.10.9.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta áp dụng hàm giao tập hợp `INTERSECT`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** mở *Expression Builder*, dán biểu thức `INTERSECT` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào Expression Builder ở Dòng 1:*
```mdx
INTERSECT(
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[1])
        ),
        30,
        ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[1])
    ),
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[0])
        ),
        30,
        ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[0])
    )
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Câu lạc bộ (Rows):**
   * Mở rộng chiều **`DIM Club`** $\rightarrow$ tìm thuộc tính **`Club Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Trạng thái Sân nhà / Sân khách (Columns):**
   * Mở rộng thư mục **`FACT Player Match Perf`** $\rightarrow$ tìm thuộc tính **`Is Home Game`**: Kéo thả lên vùng cột (Columns) để chia bảng làm 2 cột: Sân nhà (1) và Sân khách (0).
3. **Kéo Thước đo Bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào vùng dữ liệu (Totals).

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị chính xác bảng so sánh bàn thắng Sân nhà vs Sân khách của nhóm các CLB toàn diện nhất Châu Âu.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.9.2 Sử dụng Pivot Excel

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
| **Ô `Columns` (Cột ma trận)** | **`Is Home Game`** | Mở thư mục **`FACT Player Match Perf`** $\rightarrow$ Kéo `Is Home Game` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |

### Bước 4: Sắp xếp và Đổi tên Tiêu đề
1. Đổi tên giá trị cột: Ô số `1` đặt tên thành `Home Goals`, ô số `0` đặt tên thành `Away Goals`.
2. Chuột phải vào cột tổng cộng `Grand Total` $\rightarrow$ chọn **Sort** $\rightarrow$ **Sort Largest to Smallest** để đưa các CLB có tổng bàn thắng cao nhất lên trên đầu.
3. Vô thẻ ngữ cảnh **`Design`** $\rightarrow$ chọn **Report Layout** $\rightarrow$ chọn **`Show in Tabular Form`**.

---

## 3.10.9.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 09: Giao điểm các CLB thuộc Top 30 Sân Nhà & Top 30 Sân Khách
   Khai thác: INTERSECT, TOPCOUNT, CROSSJOIN, NONEMPTY, EXCEPT
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Bàn thắng Sân Nhà và Sân Khách
    CrossJoin(
        { [Measures].[Goals] },
        { 
            [FACT Player Match Perf].[Is Home Game].[1], 
            [FACT Player Match Perf].[Is Home Game].[0] 
        }
    ) ON COLUMNS,

    -- Trục Dòng: Giao điểm giữa Top 30 Sân Nhà và Top 30 Sân Khách
    INTERSECT(
        -- Tập 1: Top 30 CLB ghi nhiều bàn nhất khi đá Sân Nhà
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[1])
            ),
            30,
            ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[1])
        ),
        -- Tập 2: Top 30 CLB ghi nhiều bàn nhất khi đá Sân Khách
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[0])
            ),
            30,
            ([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[0])
        )
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`CrossJoin({ [Measures].[Goals] }, { [Is Home Game].[1], [Is Home Game].[0] }) ON COLUMNS`**: Kết hợp thước đo bàn thắng với 2 trạng thái sân nhà và sân khách trên trục **CỘT** (Axis 0).
* **`INTERSECT(Tập 1, Tập 2) ON ROWS`**: Trả về các phần tử chung xuất hiện đồng thời trong cả hai tập hợp trên trục **HÀNG** (Axis 1).
* **`TOPCOUNT(NONEMPTY(...), 30, (Goals, [Is Home Game].[1]))`**: Trích xuất Top 30 câu lạc bộ ghi bàn nhiều nhất ở các trận sân nhà.
* **`TOPCOUNT(NONEMPTY(...), 30, (Goals, [Is Home Game].[0]))`**: Trích xuất Top 30 câu lạc bộ ghi bàn nhiều nhất ở các trận sân khách.
* **`EXCEPT([Club Name].MEMBERS, { [Club Name].[All] })`**: Loại trừ nút tổng hợp `[All]` để giữ lại các câu lạc bộ thực tế.
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị 16 câu lạc bộ ưu tú thỏa mãn đồng thời cả 2 tiêu chí cùng 2 cột bàn thắng sân nhà và sân khách.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.9.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
