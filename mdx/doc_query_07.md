# 3.10.7 Câu truy vấn 7: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu thuộc Nước Anh

**Nội dung truy vấn:** Xác định nhóm các quốc gia có cầu thủ đóng góp vào **80% tổng số bàn thắng** được ghi tại tất cả các giải đấu bóng đá diễn ra trên lãnh thổ Nước Anh (`Country_Name = 'England'`). Ứng dụng nguyên lý Pareto $80/20$ giúp liên đoàn bóng đá và các câu lạc bộ đánh giá thị trường xuất khẩu cầu thủ chủ lực, phục vụ chiến lược cấp giấy phép lao động (Work Permit) và chính sách ngoại binh.

## 3.10.7.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Member Tỷ Lệ Pareto
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $
ightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để tính tổng bàn thắng của giải đấu tại Anh và tỷ lệ phần trăm đóng góp:
   * **Thước đo 1 (`England Total Goals`):**
     * Name: `England Total Goals` | Parent hierarchy: `Measures`
     * Expression: `([DIM Player].[Country Of Citizenship].[All], [Measures].[Goals], [DIM Competition].[Country Name].[England])`
   * **Thước đo 2 (`Pct Of England Goals`):**
     * Name: `Pct Of England Goals` | Parent hierarchy: `Measures`
     * Expression: `IIF([Measures].[England Total Goals] = 0, NULL, [Measures].[Goals] / [Measures].[England Total Goals])`
     * Format String: `0.00%`
4. Chọn menu **Build** $
ightarrow$ **Deploy Solution** để đồng bộ vào Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định Nước Anh và áp dụng thuật toán `TOPPERCENT 80%`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Competition`** | Nhấp chọn **`Country Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`England`** $
ightarrow$ Bấm **OK** (hiển thị `{ England }`) |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Country Of Citizenship`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $
ightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `TOPPERCENT` bên dưới $
ightarrow$ Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 2:*
```mdx
TOPPERCENT(
    NONEMPTY(
        [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
        ([Measures].[Goals], [DIM Competition].[Country Name].[England])
    ),
    80,
    [Measures].[Goals]
)
```

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Quốc tịch (Rows):**
   * Mở rộng chiều **`DIM Player`** $
ightarrow$ tìm thuộc tính **`Country Of Citizenship`**: Kéo thả vào vùng Rows.
2. **Kéo Thước đo Bàn thắng & Tỷ lệ % (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào cạnh cột `Country Of Citizenship`.
     * Kéo **`Pct Of England Goals`** thả vào cột tiếp theo.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 2 cột `Goals` và `Pct Of England Goals` theo danh sách các quốc gia chiếm 80% bàn thắng.

---

## 3.10.7.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $
ightarrow$ **`Get Data`** $
ightarrow$ **`From Database`** $
ightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $
ightarrow$ Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $
ightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $
ightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $
ightarrow$ Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Country Name`** | Mở thư mục **`DIM Competition`** $
ightarrow$ Kéo `Country Name` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Country Of Citizenship`** | Mở thư mục **`DIM Player`** $
ightarrow$ Kéo `Country Of Citizenship` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Pct Of England Goals`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Pct Of England Goals` thả vào ô Values. |

### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. Tại ô **`B1`** (bên cạnh nhãn `Country Name`), nhấp mũi tên xổ xuống $
ightarrow$ tick chọn **`England`** $
ightarrow$ Nhấn **OK**.
2. **Cấu hình Bộ lọc Pareto 80%:**
   * Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
   * Di chuột vào mục **`Value Filters`** $
ightarrow$ chọn tiếp **`Top 10...`**.
   * Trong hộp thoại Top 10 Filter: Đổi sang **`Top`** $
ightarrow$ Nhập **`80`** $
ightarrow$ Chọn **`Percent`** theo **`Sum of Goals`** $
ightarrow$ Nhấn **OK**.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $
ightarrow$ **Report Layout** $
ightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp giảm dần theo số bàn thắng.

---

## 3.10.7.3 Sử dụng ngôn ngữ MDX

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
   Truy vấn MDX 07: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu ở Anh
   Khai thác: TOPPERCENT, NONEMPTY, EXCEPT, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tổng số bàn thắng của toàn bộ giải đấu tại Anh
    MEMBER [Measures].[England Total Goals] AS
        (
            [Measures].[Goals],
            [DIM Player].[Country Of Citizenship].[All],
            [DIM Competition].[Country Name].[England]
        )

    -- 2. Tỷ lệ phần trăm đóng góp bàn thắng của từng quốc gia
    MEMBER [Measures].[Pct Of England Goals] AS
        IIF(
            ISEMPTY([Measures].[England Total Goals]) OR [Measures].[England Total Goals] = 0,
            NULL,
            ROUND(([Measures].[Goals] / [Measures].[England Total Goals]) * 100, 2)
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột: Tổng số bàn thắng và Tỷ lệ phần trăm đóng góp
    {
        [Measures].[Goals],
        [Measures].[Pct Of England Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các quốc gia chiếm 80% tổng số bàn thắng, xếp giảm dần
    ORDER(
        TOPPERCENT(
            NONEMPTY(
                EXCEPT(
                    [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                    { [DIM Player].[Country Of Citizenship].[All] }
                ),
                (
                    [Measures].[Goals],
                    [DIM Competition].[Country Name].[England]
                )
            ),
            80,
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Các giải đấu diễn ra tại Nước Anh
WHERE (
    [DIM Competition].[Country Name].[England]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`WITH MEMBER [Measures].[England Total Goals]`**: Tính tổng số bàn thắng toàn thể tại Nước Anh bằng cách kết hợp tọa độ giao cắt `(Goals, [All] Country, [England])`.
* **`WITH MEMBER [Measures].[Pct Of England Goals]`**: Tính tỷ trọng đóng góp của từng quốc gia so với tổng bàn thắng toàn giải, định dạng phần trăm `0.00%`.
* **`TOPPERCENT(Set, 80, [Measures].[Goals])`**: Thuật toán Pareto tự động tính toán tổng tích lũy từ quốc gia có nhiều bàn thắng nhất đi xuống và dừng lại khi chạm ngưỡng $80\%$.
* **`NONEMPTY(EXCEPT(...), Tuple)`**: Loại bỏ nút tổng hợp `[All]` và lọc sạch các quốc gia không có bàn thắng nào tại Anh trước khi tính tổng tích lũy phần trăm, đảm bảo mẫu số chính xác tuyệt đối.
* **`ORDER(..., BDESC) ON ROWS`**: Sắp xếp danh sách các quốc gia thuộc Top 80% theo thứ tự giảm dần số bàn thắng trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.
* **`WHERE ([DIM Competition].[Country Name].[England])`**: Trục lát cắt dữ liệu (Slicer Axis), định vị ngữ cảnh phân tích tại Nước Anh.

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm xếp hạng tích lũy Pareto `TOPPERCENT(«Set», «Percentage», «Numeric_Expression»)`**:
   * **Cú pháp chuẩn:** `TOPPERCENT(Set, Percentage, Numeric_Expression)`
   * **Tham số thực tế trong truy vấn:**
     * `Set`: Tập hợp các quốc tịch cầu thủ sau khi đã loại bỏ nút `[All]` và lọc sạch ô thưa.
     * `Percentage`: `80` (ngưỡng tỷ lệ phần trăm tích lũy cần đạt tới).
     * `Numeric_Expression`: `[Measures].[Goals]` (thước đo số bàn thắng dùng để tính tỷ trọng).
   * **Cơ chế hoạt động kỹ thuật:**
     * **Bước 1:** Tính tổng số bàn thắng của toàn bộ tập hợp quốc gia tham gia các giải đấu tại Anh ($Total$).
     * **Bước 2:** Sắp xếp toàn bộ các quốc gia theo thứ tự số bàn thắng giảm dần.
     * **Bước 3:** Tiến hành cộng dồn tích lũy (Cumulative Sum) số bàn thắng từ quốc gia đứng đầu (Anh, Pháp, Na Uy...) trở xuống.
     * **Bước 4:** Tại mỗi quốc gia nạp vào, tính tỷ lệ phần trăm tích lũy: $CumPct = rac{\sum_{i=1}^k Goals_i}{Total} 	imes 100\%$.
     * **Bước 5:** Tiếp tục nạp thêm quốc gia cho đến khi tỷ lệ tích lũy đạt hoặc vừa vượt qua ngưỡng `80%`, sau đó dừng lại và trả về đúng danh sách $k$ quốc gia đó.
   * **Ý nghĩa nghiệp vụ:** Tự động hóa hoàn toàn thuật toán nguyên lý Pareto kinh điển (80/20) mà không cần viết vòng lặp thủ công như trong SQL.
   * **Kết quả trả về:** Tập hợp 13 quốc gia dẫn đầu chiếm $81.66\%$ tổng số bàn thắng của bóng đá Anh.

2. **Tọa độ Tuple cố định mẫu số `[Measures].[England Total Goals]`**:
   * **Cú pháp chuẩn:** `( [Measures].[Goals], [DIM Player].[Country Of Citizenship].[All], [DIM Competition].[Country Name].[England] )`
   * **Cơ chế hoạt động kỹ thuật:**
     * Kỹ thuật gán tọa độ cấp cao nhất `[Country Of Citizenship].[All]` giúp bỏ qua sự phân rã theo từng dòng của trục ROWS, luôn giữ cố định tổng số bàn thắng toàn thể của giải đấu tại Anh làm mẫu số cho phép tính tỷ trọng phần trăm `[Pct Of England Goals]`.

3. **Hàm `ORDER(TOPPERCENT(...), [Measures].[Goals], BDESC)`**:
   * **Cơ chế:** Sắp xếp danh sách các quốc gia thuộc nhóm Top 80% theo thứ tự giảm dần số bàn thắng trên quy mô toàn cục (`BDESC`), đảm bảo hiển thị trực quan từ quốc gia ghi nhiều bàn nhất trở xuống.


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị danh sách 13 quốc gia dẫn đầu chiếm $81.66\%$ tổng bàn thắng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.7.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
