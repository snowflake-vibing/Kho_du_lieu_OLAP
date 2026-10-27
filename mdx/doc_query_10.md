# 3.10.10 Câu truy vấn 10: Tăng trưởng bàn thắng theo Quý (QoQ) của Top 10 CLB hàng đầu Châu Âu năm 2023

**Nội dung truy vấn:** Phân tích sự biến động số bàn thắng và tốc độ tăng trưởng Quý-trên-Quý (**Quarter-over-Quarter - QoQ Growth**) của **Top 10 Câu lạc bộ bóng đá hàng đầu Châu Âu** có tổng số bàn thắng cao nhất trong năm 2023. Truy vấn ứng dụng hàm phân cấp thời gian `PREVMEMBER` kết hợp hàm logic `IIF` để tính tỷ lệ tăng trưởng bàn thắng giữa các quý liên tiếp ($Q2 \text{ vs } Q1$, $Q3 \text{ vs } Q2$, $Q4 \text{ vs } Q3$).

Đặc biệt, nhằm loại bỏ hoàn toàn các giá trị rỗng/null, tại Quý 1 ($Q1$) truy vấn chỉ lấy số bàn thắng (do là quý đầu tiên của năm phân tích nên chưa có quý liền kề trước đó làm mốc so sánh), và hiển thị song song cả Bàn thắng lẫn Tỷ lệ Tăng trưởng QoQ ở các Quý 2, 3, 4. Nhờ đó, kết quả đạt đúng 7 cột dữ liệu dày đặc, không có bất kỳ ô `null` nào.

---

## 3.10.10.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Tăng Trưởng QoQ
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSAS_Football_Transfermarkt`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** → chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để tính bàn thắng quý trước và tỷ lệ tăng trưởng QoQ:
   * **Thước đo 1 (`Prev Quarter Goals`):**
     * Name: `Prev Quarter Goals` | Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       IIF(
           [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT,
           ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER),
           NULL
       )
       ```
   * **Thước đo 2 (`QoQ Goals Growth`):**
     * Name: `QoQ Goals Growth` | Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       IIF(
           ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
           NULL,
           ROUND((([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]), 4)
       )
       ```
     * Format String: `0.00%`
4. Chọn menu **Build** → **Deploy Solution** để cập nhật Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa kéo thả.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, tạo dòng lọc cố định năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** → Bấm **OK** (hiển thị `{ 2023 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Câu lạc bộ (Rows):**
   * Mở rộng chiều **`DIM Club`** → tìm thuộc tính **`Club Name`**: Kéo thả vào vùng Rows.
2. **Kéo Phân cấp Quý (Columns):**
   * Mở rộng thư mục **`DIM Time`** → mở rộng phân cấp **`Hierarchy`** → tìm cấp độ **`Quarter`**: Kéo thả lên vùng cột (Columns) để chia bảng theo các Quý (1, 2, 3, 4).
3. **Kéo Thước đo Bàn thắng & Tăng trưởng QoQ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào vùng dữ liệu.
     * Kéo **`QoQ Goals Growth`** thả vào ngay bên cạnh `Goals`.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức hiển thị bảng ma trận phân bổ bàn thắng và tăng trưởng QoQ qua các Quý năm 2023.

---

## 3.10.10.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`SSAS_Football_Transfermarkt`** → Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** → Chọn **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** → Kéo `Year` thả vào ô Filters (chọn năm `2023`). |
| **Ô `Columns` (Cột ma trận)** | **`Quarter`** | Mở thư mục **`DIM Time`** → mở `Hierarchy` → Kéo `Quarter` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** → Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`QoQ Goals Growth`** | Mở thư mục **`Measures`** → Kéo `QoQ Goals Growth` thả vào ô Values. |

### Bước 4: Thiết lập Bộ lọc Top 10 CLB
1. Nhấp chuột vào mũi tên lọc tại tiêu đề hàng **Row Labels (Club Name)** trên PivotTable.
2. Chọn **Value Filters** → chọn **Top 10...**.
3. Thiết lập: **Top 10** theo trường **`Sum of Goals`** → Bấm **OK**.
4. (Tùy chọn) Ẩn cột rỗng `Q1 QoQ Goals Growth` để bảng dữ liệu gọn gàng và thẩm mỹ nhất.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Sắp xếp danh sách giảm dần theo tổng bàn thắng.

---

## 3.10.10.3 Sử dụng ngôn ngữ MDX

### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động phần mềm **SQL Server Management Studio (SSMS)**.
2. Tại hộp thoại kết nối máy chủ:
   * **Server type:** Nhấp chọn **`Analysis Services`**.
   * **Server name:** Nhập `localhost` (hoặc instance SSAS).
   * **Authentication:** Chọn **`Windows Authentication`**.
   * Nhấn nút **Connect**.
3. Trong cửa sổ **Object Explorer** (bên trái):
   * Mở rộng thư mục **`Databases`** → mở rộng database **`SSAS_Football_Transfermarkt`** → mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 10: Tăng trưởng bàn thắng theo Quý (QoQ) của Top 10 CLB Châu Âu
   Khai thác: PREVMEMBER, IIF, TOPCOUNT, NONEMPTY, FORMAT_STRING
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Bàn thắng của Quý liền trước (chỉ xét trong cùng năm phân cấp 2023)
    MEMBER [Measures].[Prev Quarter Goals] AS
        IIF(
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT,
            (
                [Measures].[Goals],
                [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER
            ),
            NULL
        ),
        FORMAT_STRING = "#,##0"

    -- 2. Tỷ lệ tăng trưởng so với Quý liền trước (QoQ Goals Growth %)
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                ([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals],
                4
            )
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột: Liệt kê rõ ràng 7 cột đo lường, loại bỏ cột Q1 QoQ rỗng
    {
        ([DIM Time].[Hierarchy].[Year].[2023].[1], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[QoQ Goals Growth])
    } ON COLUMNS,

    -- Trục Dòng: Top 10 CLB có tổng số bàn thắng cao nhất trong năm 2023
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
        ),
        10,
        ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`[DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER`**: Trả về thành viên thời gian liền kề trước đó trong cùng cấp bậc phân cấp. Kết hợp điều kiện so sánh `.PARENT` giúp giới hạn tính toán chặt chẽ trong phạm vi năm phân tích 2023, đảm bảo Quý 1 đầu năm trả về `NULL` an toàn.
* **`IIF(ISEMPTY(...) OR ... = 0, NULL, ...)`**: Hàm điều kiện ngăn ngừa lỗi chia cho 0 (`#VALUE!`) khi Quý trước không có bàn thắng hoặc khi ở Quý 1 đầu năm.
* **Tập hợp 7 Tuples trên `COLUMNS`**: Bằng cách chỉ định chính xác các tuple `(Quý, Measure)`, ta chỉ đưa vào cột `Goals` cho Q1, và đưa cả `Goals` lẫn `QoQ Goals Growth` cho các Q2, Q3, Q4. Kỹ thuật này loại bỏ triệt để cột `Q1 QoQ` rỗng vô ích, tạo bảng dữ liệu 7 cột đặc 100% không chứa bất kỳ ô null nào.
* **`TOPCOUNT(NONEMPTY(...), 10, ...)`**: Lọc tự động Top 10 Câu lạc bộ có thành tích ghi bàn tổng lực xuất sắc nhất trong năm 2023 theo thứ tự giảm dần.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ SSMS xem ô chọn database đã trỏ chính xác về `SSAS_Football_Transfermarkt`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận 10 dòng $\times$ 7 cột số liệu sạch sẽ, không có bất kỳ ô trống nào.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

## 3.10.10.4 Kết quả và Nhận xét

Bảng kết quả trả về thực tế đối chiếu từ khối Cube OLAP:

| STT | Câu Lạc Bộ (`Club Name`) | Q1 Bàn Thắng | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Manchester City** | 30 | 37 | +23.33% | 20 | -45.95% | 42 | +110.00% |
| **2** | **PSV Eindhoven** | 27 | 22 | -18.52% | 23 | +4.55% | 39 | +69.57% |
| **3** | **Bayer 04 Leverkusen** | 29 | 17 | -41.38% | 23 | +35.29% | 39 | +69.57% |
| **4** | **Feyenoord Rotterdam** | 30 | 22 | -26.67% | 28 | +27.27% | 28 | +0.00% |
| **5** | **Bayern Munich** | 26 | 20 | -23.08% | 23 | +15.00% | 37 | +60.87% |
| **6** | **Real Madrid** | 21 | 28 | +33.33% | 17 | -39.29% | 37 | +117.65% |
| **7** | **Arsenal FC** | 26 | 21 | -19.23% | 18 | -14.29% | 34 | +88.89% |
| **8** | **Atlético de Madrid** | 19 | 27 | +42.11% | 16 | -40.74% | 35 | +118.75% |
| **9** | **Liverpool FC** | 16 | 28 | +75.00% | 17 | -39.29% | 35 | +105.88% |
| **10** | **Borussia Dortmund** | 30 | 28 | -6.67% | 12 | -57.14% | 25 | +108.33% |

**Nhận xét nghiệp vụ:**
* Cả 3 cách tiếp cận (duyệt Cube trong SSDT, PivotTable trong Excel, và truy vấn MDX trong SSMS) đều đồng nhất 100% kết quả.
* Manchester City chứng tỏ sức mạnh hủy diệt khi dẫn đầu cả năm với 139 bàn thắng, đỉnh điểm là Quý 4 với 42 bàn thắng (tăng trưởng QoQ đạt $+110.00\%$).
* Hầu hết các CLB lớn đều có chu kỳ phong độ tương đồng: hạ nhiệt vào Quý 3 do quãng nghỉ hè và tăng tốc mạnh mẽ ở Quý 4 khi bước vào giai đoạn tăng tốc của vòng bảng UEFA Champions League và các giải vô địch quốc gia hàng đầu Châu Âu.
