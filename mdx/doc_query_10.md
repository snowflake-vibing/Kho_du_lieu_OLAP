# 3.10.10 Câu truy vấn 10: Thống kê bàn thắng của Real Madrid vào lưới các đối thủ theo từng Quý trong năm

**Nội dung truy vấn:** Phân tích sự biến động số bàn thắng ghi được của Câu lạc bộ **Real Madrid** vào lưới các đối thủ cạnh tranh qua từng Quý trong năm 2023 (từ Quý 1 đến Quý 4). Đồng thời ứng dụng hàm phân cấp thời gian `PREVMEMBER` để tính tỷ lệ tăng trưởng bàn thắng so với Quý liền trước (**Quarter-over-Quarter - QoQ Growth**), hỗ trợ ban huấn luyện nhận diện đối thủ kỵ dơ và đánh giá điểm rơi phong độ của đội bóng.

## 3.10.10.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Tăng Trưởng QoQ
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** → chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để tính bàn thắng quý trước và tỷ lệ tăng trưởng QoQ:
   * **Thước đo 1 (`Prev Quarter Goals`):**
     * Name: `Prev Quarter Goals` | Parent hierarchy: `Measures`
     * Expression: `([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER)`
   * **Thước đo 2 (`QoQ Goals Growth`):**
     * Name: `QoQ Goals Growth` | Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       IIF(
           ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
           NULL,
           ROUND((([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100, 2)
       )
       ```
     * Format String: `0.00%`
4. Chọn menu **Build** → **Deploy Solution** để cập nhật Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định đội bóng Real Madrid và năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`Real Madrid`** → Bấm **OK** (hiển thị `{ Real Madrid }`) |
| **Dòng 2** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** → Bấm **OK** (hiển thị `{ 2023 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Câu lạc bộ Đối thủ (Rows):**
   * Mở rộng chiều **`Opponent Club`** → tìm thuộc tính **`Club Name`**: Kéo thả vào vùng Rows.
2. **Kéo Phân cấp Quý (Columns):**
   * Mở rộng thư mục **`DIM Time`** → mở rộng phân cấp **`Hierarchy`** → tìm cấp độ **`Quarter`**: Kéo thả lên vùng cột (Columns) để chia bảng theo các Quý (Q1, Q2, Q3, Q4).
3. **Kéo Thước đo Bàn thắng & Tăng trưởng QoQ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào vùng dữ liệu trung tâm.
     * Kéo **`QoQ Goals Growth`** thả vào ngay bên cạnh `Goals`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận phân bổ bàn thắng và tăng trưởng QoQ của Real Madrid vào lưới từng đối thủ qua các Quý năm 2023.

---

## 3.10.10.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** → Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** → Chọn **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Club Name`** | Mở thư mục **`DIM Club`** → Kéo `Club Name` thả vào ô Filters. |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** → Kéo `Year` thả vào ô Filters. |
| **Ô `Columns` (Cột ma trận)** | **`Quarter`** | Mở thư mục **`DIM Time`** → mở `Hierarchy` → Kéo `Quarter` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`Opponent Club`** → Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`QoQ Goals Growth`** | Mở thư mục **`Measures`** → Kéo `QoQ Goals Growth` thả vào ô Values (hoặc kéo `Goals` lần 2 và chọn Show Values As `% Difference From`). |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. Tại ô bên cạnh nhãn `Club Name`, nhấp mũi tên xổ xuống → tick chọn **`Real Madrid`** → Nhấn **OK**.
2. Tại ô bên cạnh nhãn `Year`, nhấp mũi tên xổ xuống → tick chọn năm **`2023`** → Nhấn **OK**.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Sắp xếp danh sách đối thủ giảm dần theo tổng bàn thắng.

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
   * Mở rộng thư mục **`Databases`** → mở rộng database **`DW_Football_SSAS`** → mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
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
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER
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
            [DIM Time].[Hierarchy].[Year].[2023],
            [DIM Time].[Hierarchy].[Quarter]
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
* **`[DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER`**: Trả về thành viên thời gian liền kề trước đó trong cùng cấp bậc phân cấp. Ví dụ: khi đang ở `Quarter 2`, hàm sẽ tự động lấy giá trị của `Quarter 1`.
* **`IIF(ISEMPTY(...) OR ... = 0, NULL, ...)`**: Hàm điều kiện ngăn ngừa chia cho 0 khi Quý trước không có bàn thắng hoặc khi ở Quý 1 đầu năm (chưa có kỳ trước đó).
* **`DESCENDANTS([Hierarchy].[Year].[2023], [Quarter])`**: Trích xuất toàn bộ các nút con ở cấp độ `Quarter` trực thuộc năm 2023 mà không cần liệt kê thủ công từng Quý.
* **`CrossJoin(...) ON COLUMNS`**: Kết hợp 4 Quý với 2 thước đo (Bàn thắng và Tăng trưởng QoQ) trên trục **CỘT** (Axis 0).
* **`ORDER(NONEMPTY(...), Goals, BDESC) ON ROWS`**: Sắp xếp danh sách các CLB đối thủ giảm dần theo tổng số bàn thua phải nhận từ Real Madrid trên trục **HÀNG** (Axis 1).
* **`WHERE ([DIM Club].[Club Name].[Real Madrid])`**: Trục lát cắt dữ liệu (Slicer Axis), cố định đội bóng thực hiện ghi bàn là Real Madrid.

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm điều hướng chuỗi thời gian `.PREVMEMBER`**:
   * **Cú pháp chuẩn:** `«Member».PREVMEMBER`
   * **Tham số thực tế trong truy vấn:** `[DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Dựa trên cây phân cấp thời gian tự nhiên (`Year -> Quarter -> Month -> Date`).
     * Với mỗi Quý hiện hành đang được duyệt trên trục cột (ví dụ `Q2-2023`), hàm `.PREVMEMBER` điều hướng lùi lại đúng 1 bước trên cùng cấp độ phân cấp để trỏ về Quý liền kề trước đó (`Q1-2023`).
     * Khi kết hợp trong Tuple `([Measures].[Goals], CURRENTMEMBER.PREVMEMBER)`, nó truy xuất số bàn thắng của Quý liền trước làm mốc so sánh.
     * Tại Quý đầu tiên (`Q1-2023`), do không có quý nào đứng trước trong phạm vi phân cấp của năm, hàm trả về giá trị rỗng (`NULL`).
   * **Kết quả trả về:** Thành viên thời gian liền kề trước đó trong cùng phân cấp.

2. **Hàm duyệt cây phân cấp `DESCENDANTS(«Member»[, «Level»[, «Desc_Flag»]])`**:
   * **Cú pháp chuẩn:** `DESCENDANTS(Member, Level)`
   * **Tham số thực tế trong truy vấn:**
     * `Member`: Nút gốc `[DIM Time].[Hierarchy].[Year].[2023]`.
     * `Level`: Cấp độ con `[DIM Time].[Hierarchy].[Quarter]`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Thuật toán duyệt cây đa chiều sẽ đi từ nút cha `Year 2023` xuống và tự động trích xuất toàn bộ các nút con ở cấp độ `Quarter` (`Q1`, `Q2`, `Q3`, `Q4`).
     * Cơ chế này giúp truy vấn hoàn toàn tự động và linh hoạt, không cần phải gõ cứng tên từng Quý trong mã nguồn.
   * **Kết quả trả về:** Tập hợp 4 Quý của năm 2023.

3. **Hàm điều kiện `IIF` tính tỷ lệ tăng trưởng Quý-trên-Quý (QoQ Growth %)**:
   * **Cơ chế:** Áp dụng công thức $rac{Goals_{Current} - Goals_{Prev}}{Goals_{Prev}} 	imes 100\%$. Hàm `IIF` kiểm tra nếu `Prev Quarter Goals` bị rỗng (tại Q1) hoặc bằng 0 thì gán `NULL`, triệt tiêu hoàn toàn lỗi chia cho 0.


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận phân bổ bàn thắng theo Quý và tăng trưởng QoQ của các đối thủ cạnh tranh với Real Madrid.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.10.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
