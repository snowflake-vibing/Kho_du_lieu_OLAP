# 3.10.5 Câu truy vấn 5: So sánh tổng bàn thắng giữa chân Trái, chân Phải & 2 Chân theo vị trí chi tiết

**Nội dung truy vấn:** Khảo sát xem đặc điểm chân thuận (`Foot`: Left, Right, Both) tương quan như thế nào với số lượng bàn thắng ghi được ở từng vai trò vị trí cụ thể trên sân cỏ (`Sub_Position` như Centre-Forward, Left Winger, Right Winger, Attacking Midfield, Second Striker). Sử dụng phép toán hợp tập hợp (`UNION`) để gom nhóm các vị trí tiền đạo và tiền vệ tấn công chủ lực, phục vụ công tác phân tích chiến thuật và bố trí cầu thủ chạy cánh nghịch chân (Inverted Wingers).

## 3.10.5.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo các dòng lọc để chọn nhóm vị trí tấn công và loại trừ giá trị rỗng/nút All của chân thuận:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Sub Position`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `UNION` bên dưới $\rightarrow$ Bấm **OK** |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Foot`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `EXCEPT` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào Expression Builder ở Dòng 1 (Hợp tập hợp các vị trí tấn công & tiền vệ):*
```mdx
UNION(
    { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
    { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
)
```

*Biểu thức nhập vào Expression Builder ở Dòng 2 (Loại trừ phần tử All của chân thuận):*
```mdx
EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Vị trí & Chân thuận (Rows/Columns):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Sub Position`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
   * Tìm tiếp thuộc tính **`Foot`** trong `DIM Player`: Kéo thả vào ngay bên cạnh cột `Sub Position` (hoặc kéo lên vùng Columns để tạo ma trận chéo 2 chiều).
2. **Kéo Thước đo Bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo và thả vào ngay bên cạnh cột `Foot` trên lưới.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận phân bổ bàn thắng theo từng vị trí chi tiết và chân thuận.
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

## 3.10.5.2 Sử dụng Pivot Excel

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
| **Ô `Columns` (Cột ma trận)** | **`Foot`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Foot` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Sub Position`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Sub Position` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values (hiển thị `Sum of Goals`). |

### Bước 4: Lọc các Vị trí Trọng điểm
* Tại mũi tên lọc ở ô tiêu đề `Row Labels` (cột `Sub Position`), bỏ chọn `(Select All)`, chỉ tick chọn 5 vị trí:
  * `Centre-Forward`
  * `Second Striker`
  * `Left Winger`
  * `Right Winger`
  * `Attacking Midfield`
* Nhấn **OK**.

### Bước 5: Tạo Heatmap Trực quan (Color Scales)
1. Dùng chuột bôi đen toàn bộ vùng số liệu bàn thắng bên trong bảng ma trận.
2. Vô thẻ tab **`Home`** trên thanh Ribbon $\rightarrow$ chọn **`Conditional Formatting`** $\rightarrow$ chọn **`Color Scales`** $\rightarrow$ chọn dải màu xanh lá - vàng - đỏ (Green - Yellow - Red Color Scale).
3. Bảng ma trận sẽ hiển thị các gam màu trực quan: ô màu xanh lá đậm là nơi có số lượng bàn thắng cao nhất (như Tiền đạo cắm chân Phải, Tiền đạo cánh Phải thuận chân Trái).

---

## 3.10.5.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 05: Bàn thắng theo vị trí chi tiết và chân thuận
   Khai thác: UNION, CROSSJOIN, EXCEPT, NONEMPTY, ORDER (DESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột: Thước đo Bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Các cặp (Sub Position, Foot) sắp xếp phân cấp theo từng vị trí
    ORDER(
        NONEMPTY(
            CrossJoin(
                -- Hợp tập hợp (UNION): Kết hợp các vị trí tấn công và tiền vệ
                UNION(
                    { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
                    { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
                ),
                -- Tập hợp các loại chân thuận (loại bỏ nút All)
                EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })
            ),
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        DESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT { [Measures].[Goals] } ON COLUMNS`**: Chọn thước đo tổng số bàn thắng đặt trên trục **CỘT** (Axis 0).
* **`ORDER(..., [Measures].[Goals], DESC) ON ROWS`**: Sắp xếp kết quả theo thứ tự giảm dần số bàn thắng, sử dụng từ khóa `DESC` (duy trì phân cấp - Hierarchy-preserving) giúp gom các dòng của cùng một nhóm vị trí lại với nhau.
* **`UNION(...)`**: Hợp nhất hai tập hợp con của các vai trò tấn công (Tiền đạo cắm, Hộ công) và vai trò sáng tạo (Tiền đạo cánh, Tiền vệ tấn công) thành một tập hợp duy nhất.
* **`CrossJoin(...)`**: Tạo tích Đề-các giữa tập hợp các vị trí thi đấu đã hợp nhất với các loại chân thuận (`Foot`).
* **`EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All] })`**: Loại trừ phần tử tổng hợp `[All]` để chỉ giữ lại các giá trị lá cụ thể (`Left`, `Right`, `Both`).
* **`NONEMPTY(...)`**: Loại bỏ trước các tổ hợp không có bàn thắng phát sinh ở mức lưu trữ trước khi chuyển sang Formula Engine.
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy vấn dữ liệu.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị danh sách ma trận các cặp vị trí và chân thuận xếp theo thứ tự bàn thắng giảm dần.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.5.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
