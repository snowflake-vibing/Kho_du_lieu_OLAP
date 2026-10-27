# 3.10.6 Câu truy vấn 6: Chiều cao trung bình, chiều cao lớn nhất/nhỏ nhất, bàn thắng và thẻ vàng theo vị trí chính

**Nội dung truy vấn:** Đánh giá tương quan thể hình (chiều cao trung bình `Avg Height Cm`, chiều cao cực đại `Max Height Cm`, chiều cao cực tiểu `Min Height Cm`) và hiệu suất thi đấu (tổng bàn thắng `Goals`, tổng thẻ vàng `Yellow Cards`) phân bổ theo 4 tuyến thi đấu chính trên sân cỏ (`Main_Position`: Attack, Midfield, Defender, Goalkeeper). Phân tích này hỗ trợ ban huấn luyện đánh giá tiêu chí thể hình tối ưu cho từng vai trò trên sân.

## 3.10.6.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Thể Hình
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSAS_Football_Transfermarkt`).
2. Mở tệp khối đa chiều **`DW Football Transfermarkt.cube`** → chuyển đến tab **`Calculations`**.
3. Tại Script Organizer, tạo tập hợp và 3 Calculated Members để tính toán các chỉ số thể hình theo đúng ngữ cảnh cầu thủ:
   * **Tập hợp (`ValidPlayers`):** Nhấp chuột phải → chọn **New Named Set**:
     * Name: `ValidPlayers`
     * Expression:
       ```mdx
       NONEMPTY(
           EXISTING CrossJoin(
               [DIM Player].[Player Name].[Player Name].MEMBERS,
               EXCEPT(
                   [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                   { [DIM Player].[Height In Cm].[0], [DIM Player].[Height In Cm].[All] }
               )
           ),
           [Measures].[FACT Player Match Perf Count]
       )
       ```
   * **Thước đo 1 (`Avg Height Cm`):** Nhấp chuột phải → chọn **New Calculated Member**:
     * Name: `Avg Height Cm` | Parent hierarchy: `Measures`
     * Expression: `ROUND(AVG([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE), 1)`
     * Format String: `#,##0.0`
   * **Thước đo 2 (`Max Height Cm`):** Nhấp chuột phải → chọn **New Calculated Member**:
     * Name: `Max Height Cm` | Parent hierarchy: `Measures`
     * Expression: `MAX([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)`
     * Format String: `#,##0`
   * **Thước đo 3 (`Min Height Cm`):** Nhấp chuột phải → chọn **New Calculated Member**:
     * Name: `Min Height Cm` | Parent hierarchy: `Measures`
     * Expression: `MIN([ValidPlayers], [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)`
     * Format String: `#,##0`
4. Chọn menu **Build** → **Deploy Solution** để đồng bộ tập hợp và các thước đo mới vào Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận các thước đo mới được deploy).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta loại bỏ các bản ghi không hợp lệ (`Missing`):

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Main Position`** | Chọn **`Not Equal`** ($
e$) | Tick chọn giá trị **`Missing`** → Bấm **OK** |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Tuyến thi đấu (Rows):**
   * Mở rộng chiều **`DIM Player`** → tìm thuộc tính **`Main Position`**: Kéo thả vào vùng Rows.
2. **Kéo 5 Thước đo Thể hình & Hiệu năng (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Avg Height Cm`** thả vào cạnh `Main Position`.
     * Kéo **`Max Height Cm`** thả vào tiếp theo.
     * Kéo **`Min Height Cm`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào tiếp theo.
     * Kéo **`Yellow Cards`** thả vào cột cuối cùng.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị chính xác bảng 4 dòng tuyến thi đấu và 5 cột chỉ số thể hình & thi đấu.

---

---

## 3.10.6.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`SSAS_Football_Transfermarkt`** (hoặc `DW_Football_SSAS`).
2. Chọn Cube: **`DW Football Transfermarkt`** → Nhấn **Finish**.
3. Chọn vị trí đặt bảng: **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Main Position`** | Mở thư mục **`DIM Player`** → Kéo `Main Position` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Avg Height Cm`** | Mở thư mục **`Measures`** → Kéo `Avg Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Max Height Cm`** | Mở thư mục **`Measures`** → Kéo `Max Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Min Height Cm`** | Mở thư mục **`Measures`** → Kéo `Min Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** → Kéo `Yellow Cards` thả vào ô Values. |

### Bước 4: Lọc và Sắp xếp bảng kết quả
1. Tại mũi tên lọc ở ô tiêu đề `Row Labels` (cột `Main Position`), bỏ tick chọn giá trị **`Missing`** để giữ lại đúng 4 vị trí chính.
2. Nhấp chuột phải vào một ô trong cột **`Goals`** → chọn **Sort** → **`Sort Largest to Smallest`** để xếp thứ tự theo số bàn thắng giảm dần.
3. Vào tab **`Design`** → **Report Layout`** → chọn **`Show in Tabular Form`**. Bảng hiển thị đồng bộ 5 cột chỉ số khớp 100% với Cube Browser và MDX.

---

---

## 3.10.6.3 Sử dụng ngôn ngữ MDX

### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động phần mềm **SQL Server Management Studio (SSMS)**.
2. Tại hộp thoại kết nối máy chủ:
   * **Server type:** Nhấp chọn **`Analysis Services`**.
   * **Server name:** Nhập `localhost` (hoặc tên máy tính / instance SSAS).
   * **Authentication:** Chọn **`Windows Authentication`** → Nhấn **Connect**.
3. Trong cửa sổ **Object Explorer** (bên trái):
   * Mở rộng thư mục **`Databases`** → mở database **`SSAS_Football_Transfermarkt`** (hoặc `DW_Football_SSAS`) → mở thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 06: Thể hình (AVG, MAX, MIN) và hiệu suất theo vị trí chính
   Khai thác: WITH SET, WITH MEMBER, AVG, MAX, MIN, CrossJoin, NONEMPTY, ORDER
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tập hợp các cặp (Cầu thủ, Chiều cao) hợp lệ theo ngữ cảnh từng tuyến thi đấu
    SET [ValidPlayers] AS
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                EXCEPT(
                    [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                    { [DIM Player].[Height In Cm].[0], [DIM Player].[Height In Cm].[All] }
                )
            ),
            [Measures].[FACT Player Match Perf Count]
        )

    -- 2. Chiều cao trung bình theo vị trí
    MEMBER [Measures].[Avg Height Cm] AS
        ROUND(
            AVG(
                [ValidPlayers],
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
            ),
            1
        ),
        FORMAT_STRING = "#,##0.0"

    -- 3. Chiều cao lớn nhất (Max Height) theo vị trí
    MEMBER [Measures].[Max Height Cm] AS
        MAX(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

    -- 4. Chiều cao nhỏ nhất (Min Height) theo vị trí
    MEMBER [Measures].[Min Height Cm] AS
        MIN(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Các chỉ số thống kê thể hình và kết quả thi đấu
    {
        [Measures].[Avg Height Cm],
        [Measures].[Max Height Cm],
        [Measures].[Min Height Cm],
        [Measures].[Goals],
        [Measures].[Yellow Cards]
    } ON COLUMNS,

    -- Trục Dòng: Các vị trí chính hợp lệ, sắp xếp theo số bàn thắng giảm dần
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].[Missing], [DIM Player].[Main Position].[All] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SET [ValidPlayers]`**: Sử dụng `CrossJoin([Player Name].MEMBERS, [Height In Cm].MEMBERS)` kết hợp `NONEMPTY` để tạo tập hợp các tuple `(Cầu thủ, Chiều cao)`. Kỹ thuật này là mấu chốt để liên kết đúng thành viên `[Player Name]` với giá trị thuộc tính `[Height In Cm]` của cầu thủ đó.
* **`WITH MEMBER [Measures].[Avg Height Cm]`**: Sử dụng hàm `AVG` tính trung bình cộng giá trị `[Height In Cm].CURRENTMEMBER.MEMBER_VALUE` trên tập hợp `[ValidPlayers]`.
* **`WITH MEMBER [Measures].[Max Height Cm]` & `[Min Height Cm]`**: Sử dụng hàm `MAX` và `MIN` để tìm chiều cao cực đại và cực tiểu của các cầu thủ thuộc từng tuyến thi đấu.
* **`SELECT { ... } ON COLUMNS`**: Đặt 3 chỉ số thể hình tính toán cùng 2 thước đo bàn thắng và thẻ phạt lên trục **CỘT** (Axis 0).
* **`ORDER(EXCEPT(...), [Measures].[Goals], BDESC) ON ROWS`**: Loại trừ nút tổng hợp `[All]` và giá trị ngoại lệ `[Missing]`, sau đó sắp xếp 4 tuyến thi đấu giảm dần theo tổng số bàn thắng ghi được (`BDESC`) trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Kỹ thuật `CrossJoin` kết hợp `EXISTING` giải quyết bài toán Context Transition**:
   * **Bản chất vấn đề:** Trong SSAS, `[Player Name]` và `[Height In Cm]` là hai phân cấp thuộc tính độc lập trong chiều `[DIM Player]`. Nếu chỉ duyệt qua `[Player Name].MEMBERS`, thuộc tính `[Height In Cm].CURRENTMEMBER` sẽ không tự động thay đổi mà vẫn nằm ở nút gốc `[All]`, dẫn đến lỗi trả về `None` hoặc `All`.
   * **Giải pháp:** Sử dụng `CrossJoin([Player Name].MEMBERS, [Height In Cm].MEMBERS)`. Mỗi phần tử của tập hợp lúc này là một Tuple chứa cả Cầu thủ và Chiều cao của họ. Khi hàm `AVG/MAX/MIN` duyệt qua tập hợp này, `[Height In Cm].CURRENTMEMBER.MEMBER_VALUE` sẽ trích xuất chính xác số đo chiều cao (cm) thực tế của từng người.
   * **Từ khóa `EXISTING`:** Ép tập hợp tuple phải tuân thủ ngữ cảnh dòng hiện hành (`Main Position` trên trục ROWS).

2. **Các hàm thống kê tập hợp `AVG()`, `MAX()`, `MIN()`**:
   * **Cú pháp chuẩn:**
     * `AVG(Set, Numeric_Expression)`: Tính trung bình cộng của biểu thức số học trên tập hợp.
     * `MAX(Set, Numeric_Expression)`: Tìm giá trị lớn nhất.
     * `MIN(Set, Numeric_Expression)`: Tìm giá trị nhỏ nhất.
   * **Tham số thực tế trong truy vấn:**
     * `Set`: Tập hợp `[ValidPlayers]`.
     * `Numeric_Expression`: Giá trị số học `[DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE`.

3. **Hàm làm tròn `ROUND(«Numeric_Expression», «Decimals»)`**:
   * Làm tròn kết quả chiều cao trung bình đến 1 chữ số thập phân (`1`), kết hợp chuỗi định dạng `FORMAT_STRING = "#,##0.0"`.

4. **Hàm `ORDER(EXCEPT(...), [Measures].[Goals], BDESC)`**:
   * Dùng `EXCEPT` loại bỏ `[Missing]` và nút tổng hợp `[All]` của `Main Position`, sau đó dùng `ORDER` với cờ `BDESC` để sắp xếp 4 tuyến thi đấu giảm dần theo tổng số bàn thắng.

### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `SSAS_Football_Transfermarkt` (hoặc `DW_Football_SSAS`).
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận 4 dòng tương ứng với 4 tuyến thi đấu và 5 cột chỉ số thể hình & hiệu suất chính xác 100%.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.6.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
