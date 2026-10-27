# 3.10.9 Câu truy vấn 9: So sánh hiệu năng & thẻ phạt của các CLB giữa Cuối tuần & Ngày thường

**Nội dung truy vấn:** Xác định danh sách các Câu lạc bộ bóng đá toàn diện hàng đầu xuất hiện đồng thời trong cả hai nhóm: **Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (`Is_Weekend = 1`)** và **Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (`Is_Weekend = 0`)**. Ứng dụng phép toán giao tập hợp (`INTERSECT`) giúp lọc ra những đội bóng có bản lĩnh thi đấu đồng đều đỉnh cao (Elite Clubs), duy trì sức tấn công và kiểm soát kỷ luật bất kể thời điểm thi đấu (các trận giải VĐQG cuối tuần hay các trận cúp châu Âu giữa tuần).

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

### Bước 3: Thiết lập Vùng Bộ lọc Giao tập hợp (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho `Club Name` để áp dụng thuật toán `INTERSECT`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `INTERSECT` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 1:*
```mdx
INTERSECT(
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
    ),
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
    )
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Câu lạc bộ (Rows):**
   * Mở rộng chiều **`DIM Club`** $\rightarrow$ tìm thuộc tính **`Club Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Phân loại Cuối tuần / Ngày thường (Columns):**
   * Mở rộng chiều **`DIM Time`** $\rightarrow$ tìm thuộc tính **`Is Weekend`**: Kéo thả lên vùng cột (Columns) để chia bảng làm 2 cột: Cuối tuần (1) và Ngày thường (0).
3. **Kéo Thước đo Bàn thắng & Thẻ vàng (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào vùng dữ liệu trung tâm.
   * Tiếp tục nhấp giữ thước đo **`Yellow Cards`**, kéo thả vào ngay bên cạnh cột `Goals`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận hiệu năng của các đội bóng ưu tú trên cả Cuối tuần và Ngày thường.

---

---

## 3.10.9.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon $\rightarrow$ **`Get Data`** $\rightarrow$ **`From Database`** $\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\rightarrow$ Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\rightarrow$ Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Columns` (Cột ma trận)** | **`Is Weekend`** | Mở thư mục **`DIM Time`** $\rightarrow$ Kéo `Is Weekend` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Yellow Cards` thả vào ô Values. |

### Bước 4: Thiết lập Bộ lọc Top 30 CLB xuất sắc
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại Top 10 Filter: Đổi số `10` thành **`30`** Items theo **`Sum of Goals`** $\rightarrow$ Nhấn **OK**.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\rightarrow$ **Report Layout** $\rightarrow$ chọn **`Show in Tabular Form`**.
* Tắt tổng phụ: **Subtotals** $\rightarrow$ **`Do Not Show Subtotals`**.

---

---

## 3.10.9.3 Sử dụng ngôn ngữ MDX

### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động **SQL Server Management Studio (SSMS)** $\rightarrow$ kết nối Analysis Services.
2. Mở rộng `Databases` $\rightarrow$ `DW_Football_SSAS` $\rightarrow$ `Cubes`.
3. Chuột phải vào Cube **`DW Football Transfermarkt`** $\rightarrow$ chọn **`New Query`** $\rightarrow$ **`MDX`**.

### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 09: So sánh hiệu năng & thẻ phạt của các CLB giữa Cuối tuần & Ngày thường
   Ứng dụng Giao Tập Hợp INTERSECT & Tích Đề-các CROSSJOIN
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (Is_Weekend = 1)
    SET [Top_Weekend_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        )

    -- 2. Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (Is_Weekend = 0)
    SET [Top_Weekday_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        )

    -- 3. Giao tập hợp (INTERSECT): Các CLB xuất sắc toàn diện cả Cuối tuần và Ngày thường
    SET [Elite_Clubs_All_Days] AS
        INTERSECT([Top_Weekend_Clubs], [Top_Weekday_Clubs])

SELECT
    -- Trục Cột (COLUMNS): Tích Đề-các giữa Thời điểm và Thước đo
    CrossJoin(
        { [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] },
        { [Measures].[Goals], [Measures].[Yellow Cards] }
    ) ON COLUMNS,

    -- Trục Dòng (ROWS): Danh sách các CLB ưu tú thuộc tập hợp giao INTERSECT, xếp giảm dần
    ORDER(
        [Elite_Clubs_All_Days],
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SET [Top_Weekend_Clubs]`**: Trích xuất Top 30 CLB ghi bàn nhiều nhất vào các ngày cuối tuần (`Is Weekend = 1`).
* **`SET [Top_Weekday_Clubs]`**: Trích xuất Top 30 CLB ghi bàn nhiều nhất vào các ngày trong tuần (`Is Weekend = 0`).
* **`INTERSECT(...)`**: Phép toán giao tập hợp lọc ra các đội bóng xuất hiện đồng thời trong cả hai danh sách.
* **`CrossJoin(...) ON COLUMNS`**: Kết hợp 2 trạng thái thời điểm với 2 thước đo bàn thắng và thẻ phạt trên trục **CỘT** (Axis 0).
* **`ORDER(..., BDESC) ON ROWS`**: Sắp xếp danh sách CLB giảm dần theo tổng bàn thắng trên trục **HÀNG** (Axis 1).

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm giao tập hợp `INTERSECT(«Set_1», «Set_2»[, ALL])`**:
   * **Cú pháp chuẩn:** `INTERSECT(Set_1, Set_2)`
   * **Tham số thực tế trong truy vấn:**
     * `Set_1`: Tập hợp Top 30 CLB ghi bàn nhiều nhất trên Sân Nhà (kết quả từ hàm `TOPCOUNT` thứ nhất).
     * `Set_2`: Tập hợp Top 30 CLB ghi bàn nhiều nhất trên Sân Khách (kết quả từ hàm `TOPCOUNT` thứ hai).
   * **Cơ chế hoạt động kỹ thuật:**
     * Thực hiện phép giao tập hợp trong đại số MDX ($Set_1 \cap Set_2$).
     * Formula Engine tính toán độc lập hai danh sách Top 30, sau đó hàm `INTERSECT` đối chiếu và chỉ giữ lại những câu lạc bộ xuất hiện đồng thời trong cả hai danh sách.
     * Thứ tự các phần tử trong tập kết quả trả về được bảo toàn theo đúng thứ tự xuất hiện của `Set_1`.
     * Những đội bóng chỉ mạnh sân nhà nhưng yếu sân khách (hoặc ngược lại) sẽ bị loại bỏ, chỉ giữ lại các CLB duy trì được bản lĩnh và phong độ ổn định toàn diện (16 CLB).
   * **Kết quả trả về:** Tập hợp gồm 16 câu lạc bộ ưu tú nhất Châu Âu.

2. **Hàm `TOPCOUNT` kết hợp Tuple tiêu chí cục bộ**:
   * **Cú pháp chuẩn:** `TOPCOUNT(Set, 30, (Goals, [Is Home Game].[1]))`
   * **Cơ chế hoạt động kỹ thuật:**
     * Tiêu chí sắp xếp của hàm `TOPCOUNT` là một Tuple giao cắt đa chiều `([Measures].[Goals], [FACT Player Match Perf].[Is Home Game].[1])`.
     * Kỹ thuật này cho phép lọc và xếp hạng dữ liệu theo điều kiện sân bãi riêng biệt mà không làm ảnh hưởng đến ngữ cảnh toàn cục của toàn bộ câu truy vấn.

3. **Hàm `CrossJoin` trên trục COLUMNS**:
   * **Cơ chế:** Ghép thước đo bàn thắng với hai trạng thái thi đấu `{ [Is Home Game].[1], [Is Home Game].[0] }`, sinh ra hai cột hiển thị trực quan: Bàn thắng Sân Nhà và Bàn thắng Sân Khách.


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Nhấn nút **`! Execute`** (hoặc phím **`F5`**).
2. Xem kết quả hiển thị ma trận phân bổ bàn thắng và thẻ vàng chi tiết giữa Cuối tuần và Ngày thường.

---

---

## 3.10.9.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
