# 3.10.3 Câu truy vấn 3: Tổng phút thi đấu & đóng góp bàn thắng cho cầu thủ > 20 G+A mùa 2023/2024

**Nội dung truy vấn:** Đo lường khối lượng thời gian thi đấu (`Minutes_Played`) và hiệu quả tạo dấu ấn lên bàn thắng (`Goal_Contributions = Goals + Assists`) đối với những ngôi sao tấn công hàng đầu đạt cột mốc trên 20 đóng góp bàn thắng ($> 20\text{ G+A}$) trong mùa giải 2023/2024 nhằm đánh giá mức độ phụ thuộc vào trụ cột và tải trọng thi đấu.

## 3.10.3.1 Sử dụng Cube Browser

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định mùa giải 2023/2024 và thiết lập ngưỡng điều kiện $G+A > 20$:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Season`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn mùa **`2023/2024`** → Bấm **OK** |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Player Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô → nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức bên dưới → Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 2:*
```mdx
FILTER(
    NONEMPTY([DIM Player].[Player Name].[Player Name].MEMBERS, ([Measures].[Goal Contributions], [DIM Time].[Season].[2023/2024])),
    [Measures].[Goal Contributions] > 20
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** → tìm thuộc tính **`Player Name`**.
   * Nhấp giữ chuột vào **`Player Name`**, kéo và thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Thước đo Phút thi đấu & Đóng góp bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** → mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Minutes Played`**, kéo thả vào ngay bên cạnh cột `Player Name`.
   * Tiếp tục nhấp giữ thước đo **`Goal Contributions`**, kéo thả vào ngay bên cạnh cột `Minutes Played`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than màu đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị danh sách các cầu thủ đạt cột mốc trên 20 bàn thắng và kiến tạo (Harry Kane 44 G+A, Kylian Mbappé 38 G+A, Cole Palmer 33 G+A...).
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

---

## 3.10.3.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon.
3. Trong nhóm lệnh *Get & Transform Data* (hoặc *Get External Data*):
   * Nhấp chọn **`Get Data`** → chọn **`From Database`** → chọn **`From Analysis Services`**.
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
   * Vị trí đặt bảng: Chọn ô **`=$A$3`** của Sheet hiện tại → Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Season`** | Mở thư mục **`DIM Time`** → Kéo `Season` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Player Name`** | Mở thư mục **`DIM Player`** → Kéo `Player Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Minutes Played`** | Mở thư mục **`Measures`** → Kéo `Minutes Played` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goal Contributions`** | Mở thư mục **`Measures`** → Kéo `Goal Contributions` thả vào ô Values. |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Season`), nhấp mũi tên xổ xuống → tick chọn mùa bóng **`2023/2024`** → Nhấn **OK**.

### Bước 5: Cấu hình Bộ lọc Cầu thủ có G+A > 20 & Sắp xếp
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** → chọn tiếp **`Greater Than...`**.
3. Trong hộp thoại **Value Filter (Player Name)**:
   * Dropdown chọn thước đo: Chọn **`Sum of Goal Contributions`**.
   * Ô điều kiện: Nhập số **`20`**.
   * Nhấn **OK**.
4. **Sắp xếp giảm dần:** Nhấp chuột phải vào một ô số bất kỳ trong cột `Sum of Goal Contributions` → chọn **Sort** → chọn **Sort Largest to Smallest**.

### Bước 6: Trình bày bảng kết quả
* Vô thẻ ngữ cảnh **`Design`** trên Ribbon → chọn **Report Layout** → chọn **`Show in Tabular Form`**.
* Chọn **Grand Totals** → chọn **`Off for Rows and Columns`** để bảng dữ liệu tập trung hoàn toàn vào danh sách cầu thủ.

---

---

## 3.10.3.3 Sử dụng ngôn ngữ MDX

### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động phần mềm **SQL Server Management Studio (SSMS)**.
2. Tại hộp thoại kết nối máy chủ:
   * **Server type:** Nhấp chọn **`Analysis Services`**.
   * **Server name:** Nhập `localhost` (hoặc tên máy tính / instance SSAS).
   * **Authentication:** Chọn **`Windows Authentication`**.
   * Nhấn nút **Connect**.
3. Trong cửa sổ **Object Explorer** (bên trái):
   * Mở rộng thư mục **`Databases`** → mở rộng database **`DW_Football_SSAS`** → mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 03: Cầu thủ có trên 20 đóng góp bàn thắng (G+A) mùa giải 2023/2024
   Khai thác: FILTER, ORDER (BDESC), NONEMPTY, MEMBERS
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Tổng số phút thi đấu và tổng đóng góp bàn thắng (G+A)
    {
        [Measures].[Minutes Played],
        [Measures].[Goal Contributions]
    } ON COLUMNS,

    -- Trục Dòng (ROWS): Các cầu thủ có G+A > 20, sắp xếp giảm dần toàn cục
    ORDER(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                (
                    [Measures].[Goal Contributions],
                    [DIM Time].[Season].[2023/2024]
                )
            ),
            [Measures].[Goal Contributions] > 20
        ),
        [Measures].[Goal Contributions],
        BDESC
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh (Slicer Axis): Mùa giải 2023/2024
WHERE (
    [DIM Time].[Season].[2023/2024]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT`**: Khởi tạo khai báo các trục hiển thị kết quả.
* **`{ [Measures].[Minutes Played], [Measures].[Goal Contributions] } ON COLUMNS`**: Chọn hai thước đo thời lượng thi đấu và tổng đóng góp bàn thắng đặt trên trục **CỘT** (Axis 0).
* **`ORDER(..., [Measures].[Goal Contributions], BDESC) ON ROWS`**: Sắp xếp tập hợp cầu thủ theo thứ tự giảm dần tuyệt đối (`BDESC` - Break Hierarchy Descending) trên trục **HÀNG** (Axis 1).
* **`FILTER(..., [Measures].[Goal Contributions] > 20)`**: Hàm lọc logic tương đương với mệnh đề `HAVING SUM(Goal_Contributions) > 20` trong SQL.
* **`NONEMPTY(...)`**: Tiền lọc dữ liệu thưa, loại bỏ trước những cầu thủ không thi đấu hoặc không có G+A nào trong mùa giải 2023/2024 trước khi đưa vào hàm `FILTER`.
* **`FROM [DW Football Transfermarkt]`**: Chỉ định khối Cube nguồn cần truy xuất dữ liệu.
* **`WHERE ([DIM Time].[Season].[2023/2024])`**: Trục lát cắt dữ liệu (Slicer Axis), định vị ngữ cảnh trong mùa giải 2023/2024.

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm `ORDER(«Set», «Criteria»[, BASC | BDESC | ASC | DESC])`**:
   * **Cú pháp chuẩn:** `ORDER(Set, Criteria, BDESC)`
   * **Tham số thực tế trong truy vấn:**
     * `Set`: Tập hợp các cầu thủ đã thỏa mãn điều kiện lọc từ hàm `FILTER(...)`.
     * `Criteria`: `[Measures].[Goal Contributions]` (tiêu chí định lượng dùng để sắp xếp).
     * Cờ sắp xếp: `BDESC` (Break Hierarchy Descending).
   * **Cơ chế hoạt động kỹ thuật:**
     * Hàm tính toán giá trị `Goal Contributions` cho từng cầu thủ trong tập hợp kết quả của hàm `FILTER`.
     * Cờ `BDESC` chỉ định thuật toán bẻ gãy hoàn toàn cấu trúc phân cấp (Hierarchy-breaking) để thực hiện sắp xếp giảm dần trên quy mô toàn cục (Global Sort). Nhờ đó, danh sách cầu thủ được xếp hạng chuẩn xác từ người đóng góp nhiều nhất (Harry Kane - 44) xuống thấp dần mà không bị chia cắt theo các phân nhóm phân cấp nội bộ.
   * **Kết quả trả về:** Tập hợp các cầu thủ đã được sắp xếp giảm dần theo tổng đóng góp bàn thắng.

2. **Hàm `FILTER(«Set», «Logical_Expression»)`**:
   * **Cú pháp chuẩn:** `FILTER(Set, Logical_Expression)`
   * **Tham số thực tế trong truy vấn:**
     * `Set`: Tập hợp cầu thủ sau khi đã loại bỏ ô thưa bằng `NONEMPTY(...)`.
     * `Logical_Expression`: `[Measures].[Goal Contributions] > 20`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Formula Engine duyệt tuần tự qua từng phần tử (cầu thủ) trong tập hợp đầu vào.
     * Tại mỗi cầu thủ, biểu thức điều kiện `[Measures].[Goal Contributions] > 20` được tính toán trong ngữ cảnh mùa giải `2023/2024` (từ mệnh đề lát cắt Slicer `WHERE`).
     * Chỉ những cầu thủ có giá trị logic là `TRUE` (tổng số bàn thắng + kiến tạo vượt mốc 20) mới được giữ lại trong tập kết quả; các phần tử có tổng $\le 20$ hoặc rỗng bị loại bỏ hoàn toàn.
     * **Ý nghĩa đối chiếu:** Hàm này tương đương trực tiếp với mệnh đề `HAVING SUM(Goal_Contributions) > 20` trong truy vấn SQL truyền thống.
   * **Kết quả trả về:** Tập hợp con gồm các cầu thủ đạt mốc trên 20 đóng góp bàn thắng.

3. **Hàm `NONEMPTY(«Set_1»[, «Set_2»])`**:
   * **Cú pháp chuẩn:** `NONEMPTY(Set_1, Set_2)`
   * **Tham số thực tế trong truy vấn:**
     * `Set_1`: `[DIM Player].[Player Name].[Player Name].MEMBERS`.
     * `Set_2`: Tuple `([Measures].[Goal Contributions], [DIM Time].[Season].[2023/2024])`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Lọc sạch dữ liệu thưa ở tầng Storage Engine trước khi chuyển sang Formula Engine. Cầu thủ nào không có dữ liệu G+A trong mùa 2023/2024 sẽ bị loại trừ ngay từ đầu, giúp hàm `FILTER` chỉ cần đánh giá trên vài trăm cầu thủ thay vì quét qua toàn bộ cơ sở dữ liệu.
   * **Kết quả trả về:** Tập hợp các cầu thủ có dữ liệu thi đấu thực tế trong mùa giải 2023/2024.

4. **Thuộc tính `.MEMBERS`**:
   * **Cú pháp chuẩn:** `«Hierarchy/Level».MEMBERS`
   * **Tham số thực tế trong truy vấn:** `[DIM Player].[Player Name].[Player Name]`.
   * **Cơ chế hoạt động kỹ thuật:** Trích xuất toàn bộ danh sách các thành viên ở cấp độ `Player Name` để làm đầu vào cho chuỗi hàm xử lý tập hợp `NONEMPTY -> FILTER -> ORDER`.


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận đa chiều với danh sách cầu thủ có G+A > 20, kèm 2 cột số phút thi đấu và tổng G+A.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.3.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
