# 3.10.4 Câu truy vấn 4: Bàn thắng, kiến tạo & số phút thi đấu trung bình phân theo độ tuổi năm 2023

**Nội dung truy vấn:** Khảo sát sự phân bố hiệu suất ghi bàn (`Goals`), kiến tạo (`Assists`) và thời lượng thi đấu trung bình mỗi trận (`Avg Minutes Played`) theo từng độ tuổi cầu thủ (`Age`) trong năm 2023. Đồng thời áp dụng cấu trúc rẽ nhánh `CASE WHEN` để phân loại cầu thủ vào 3 giai đoạn sự nghiệp: Tài năng trẻ (U21), Độ tuổi đỉnh cao (Prime 22-29), và Lão tướng (Veteran 30+), giúp phân tích chu kỳ phát triển của vận động viên.

## 3.10.4.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Members
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Trong cửa sổ **Solution Explorer**, nhấp đúp chuột vào tệp khối đa chiều: **`DW_Football_Cube.cube`** (hoặc `DW Football Transfermarkt.cube`).
3. Chuyển sang tab **`Calculations`** ở cạnh trên để tạo 2 thước đo tính toán phân loại độ tuổi và phút thi đấu trung bình:
   * **Thước đo 1 (`Avg Minutes Played`):** Nhấp chuột phải vào Script Organizer → chọn **New Calculated Member**:
     * Name: `Avg Minutes Played`
     * Parent hierarchy: `Measures`
     * Expression: `IIF([Measures].[FACT Player Match Perf Count] = 0, NULL, [Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count])`
     * Format String: `#,##0.0`
   * **Thước đo 2 (`Career Stage Group`):** Tạo Calculated Member thứ hai:
     * Name: `Career Stage Group`
     * Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       CASE 
           WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBER_VALUE < 21 THEN "U21 - Tài năng trẻ"
           WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBER_VALUE <= 29 THEN "Prime 22-29 - Đỉnh cao"
           ELSE "Veteran 30+ - Lão tướng"
       END
       ```
4. Chọn menu **Build** → **Deploy Solution** để cập nhật 2 thước đo mới vào cấu trúc Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nạp cấu trúc mới deploy).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** → Bấm **OK** (hiển thị `{ 2023 }`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
1. **Kéo Chiều Tuổi cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** → tìm thuộc tính **`Age`**: Kéo thả vào vùng Rows.
2. **Kéo 4 Thước đo đã đồng bộ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Career Stage Group`** thả vào cạnh cột `Age`.
     * Kéo **`Goals`** thả vào tiếp theo.
     * Kéo **`Assists`** thả vào tiếp theo.
     * Kéo **`Avg Minutes Played`** thả vào cột cuối cùng.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 4 cột phân tích hiệu suất theo từng độ tuổi giống hệt câu truy vấn MDX.

---

## 3.10.4.2 Sử dụng Pivot Excel

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
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** → Kéo `Year` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Age`** | Mở thư mục **`DIM Player`** → Kéo `Age` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Career Stage Group`** | Mở thư mục **`Measures`** → Kéo `Career Stage Group` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Assists`** | Mở thư mục **`Measures`** → Kéo `Assists` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Avg Minutes Played`** | Mở thư mục **`Measures`** → Kéo `Avg Minutes Played` thả vào ô Values. |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Year`), nhấp mũi tên xổ xuống → tick chọn năm **`2023`** → Nhấn **OK**.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Sắp xếp tuổi tăng dần: Nhấp chuột phải vào cột `Age` → chọn **Sort** → **Sort Smallest to Largest**.

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
   * Mở rộng thư mục **`Databases`** → mở rộng database **`DW_Football_SSAS`** → mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
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

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Mệnh đề định nghĩa thành viên tính toán `WITH MEMBER`**:
   * **Cú pháp chuẩn:** `WITH MEMBER «Member_Name» AS «Expression»[, FORMAT_STRING = '...']`
   * **Cơ chế hoạt động kỹ thuật:**
     * Cho phép tạo ra các thước đo ảo (Calculated Measures) chỉ tồn tại tạm thời trong phiên thực thi của câu truy vấn MDX mà không cần can thiệp thay đổi cấu trúc Cube trên SSAS.
     * Các thành viên này được Formula Engine tính toán động theo từng tọa độ ô dữ liệu (cell) tại thời điểm hiển thị.

2. **Hàm điều kiện `IIF(«Logical_Expression», «True_Part», «False_Part»)` kết hợp `IsEmpty()`**:
   * **Cú pháp chuẩn:** `IIF(Condition, Value_If_True, Value_If_False)`
   * **Tham số thực tế trong truy vấn:**
     * `Condition`: `IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0` (kiểm tra mẫu số số lần ra sân).
     * `Value_If_True`: `NULL` (nếu mẫu số rỗng hoặc bằng 0).
     * `Value_If_False`: Phép chia tính trung bình `ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Đây là giải thuật tính toán phòng vệ (Defensive Calculation) chuẩn mực trong OLAP. Nếu cầu thủ ở độ tuổi đó chưa ra sân trận nào, mẫu số bằng 0 sẽ lập tức trả về `NULL`, triệt tiêu hoàn toàn nguy cơ phát sinh lỗi chia cho 0 (`#DIV/0!`) gây gián đoạn câu truy vấn.

3. **Cấu trúc rẽ nhánh `CASE WHEN ... THEN ... ELSE ... END`**:
   * **Cú pháp chuẩn:** `CASE WHEN Cond1 THEN Res1 WHEN Cond2 THEN Res2 ELSE ResElse END`
   * **Tham số thực tế trong truy vấn:**
     * `WHEN Age <= 21 THEN "U21 Young Talent"`
     * `WHEN Age <= 29 THEN "Prime Age (22-29)"`
     * `ELSE "Veteran (30+)"`
   * **Cơ chế hoạt động kỹ thuật:**
     * Đánh giá giá trị số tuổi của thành viên hiện hành trên trục dòng (`CURRENTMEMBER.MEMBERVALUE`).
     * Thực hiện phân loại động độ tuổi vào 3 nhóm chuyên môn thể thao: Cầu thủ trẻ tiềm năng (U21), Độ tuổi đỉnh cao sự nghiệp (22-29), và Cầu thủ dạn dày kinh nghiệm (30+), giúp báo cáo có tính phân tầng nghiệp vụ sâu sắc.

4. **Thuộc tính `.CURRENTMEMBER` và `.MEMBERVALUE`**:
   * **Cú pháp chuẩn:** `«Dimension/Hierarchy».CURRENTMEMBER.MEMBERVALUE`
   * **Tham số thực tế trong truy vấn:** `[DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE`.
   * **Cơ chế hoạt động kỹ thuật:**
     * `.CURRENTMEMBER`: Con trỏ ngữ cảnh trỏ đến thành viên của chiều `Age` đang được xử lý tại dòng hiện hành.
     * `.MEMBERVALUE`: Trích xuất giá trị số học nguyên thủy (numeric scalar) của thuộc tính tuổi (ví dụ: `21`, `28`, `35`) thay vì dạng chuỗi ký tự hiển thị (`.NAME`), cho phép thực hiện các phép so sánh toán học `<=`, `>` và sắp xếp một cách chính xác.

5. **Hàm `ORDER(FILTER(...), BASC)`**:
   * **Cú pháp chuẩn:** `ORDER(Set, Criteria, BASC)`
   * **Tham số thực tế:** Lọc các độ tuổi hợp lệ có dữ liệu (`NOT ISEMPTY AND Age > 0`) và sắp xếp tăng dần toàn cục (`BASC` - Break Hierarchy Ascending) từ 16 tuổi đến 42 tuổi.


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận phân bổ hiệu suất theo từng độ tuổi kèm cột phân nhóm giai đoạn sự nghiệp.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.4.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
