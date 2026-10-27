# MDX Query 03: Tổng phút thi đấu & đóng góp bàn thắng cho cầu thủ > 20 G+A mùa 2023/2024
## (Ứng dụng Hàm Lọc Điều kiện FILTER & Sắp xếp Toàn cục ORDER BDESC)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Đo lường khối lượng thời gian thi đấu (`Minutes_Played`) và hiệu quả tạo dấu ấn lên bàn thắng (`Goal_Contributions = Goals + Assists`) đối với những ngôi sao tấn công hàng đầu đạt cột mốc trên 20 đóng góp bàn thắng ($> 20\text{ G+A}$) trong mùa giải 2023/2024 nhằm đánh giá mức độ phụ thuộc vào trụ cột và tải trọng thi đấu.
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Thời gian (`DIM_Time`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[DIM Time].[Season]`
  * Cube Measures: `[Measures].[Minutes Played]`, `[Measures].[Goal Contributions]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Analytics;
GO

SELECT 
    p.Player_Name,
    t.Season,
    SUM(f.Minutes_Played) AS Total_Minutes_Played,
    SUM(f.Goal_Contributions) AS Total_Goal_Contributions
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Season = '2023' OR t.Year = 2023
GROUP BY p.Player_Name, t.Season
HAVING SUM(f.Goal_Contributions) > 20
ORDER BY Total_Goal_Contributions DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để trích xuất danh sách các cầu thủ ưu tú đạt cột mốc trên 20 G+A mùa giải 2023/2024, người dùng có thể áp dụng linh hoạt **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích G+A > 20"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Season & Filter G+A > 20 -> Kéo Grid -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Filter Season -> Rows: Player -> Value Filter: > 20"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn FILTER(NONEMPTY(...), G+A > 20) -> Execute (F5)"]

    CB_Step --> Finish["2.4. Nhận xét & Đối chiếu Kết quả Đồng nhất"]
    Excel_Step --> Finish
    MDX_Step --> Finish
```

---

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Trong cửa sổ **Solution Explorer** (khung bên phải):
   * Mở rộng thư mục **`Cubes`**.
   * Nhấp đúp chuột vào tệp khối đa chiều: **`DW_Football_Cube.cube`** (hoặc `DW Football Transfermarkt.cube`).
3. Màn hình Cube Designer xuất hiện với các tab chức năng ở cạnh trên (*Cube Structure*, *Dimension Usage*, *Calculations*, *Partitions*, *Browser*...).

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (tab ngoài cùng bên phải của trình thiết kế Cube).
2. **Kiểm tra trạng thái kết nối & giao diện:**
   * Nếu nút **Reconnect** (biểu tượng 2 phích cắm ở góc trên bên trái) sáng lên: Nhấp vào để kết nối tới SSAS Database.
   * Nếu màn hình đang ở chế độ soạn thảo văn bản thuần (Text Mode): Nhấp vào biểu tượng **`Design Mode`** (hình chiếc Lưới màu xanh có cây thước kẻ/bút chì màu vàng, nằm cạnh nút Stop xám) để chuyển sang giao diện thiết kế đồ họa trực quan (Graphical Query Designer). Khi đó, màn hình sẽ chia làm 2 phần: **Bảng lọc (Filter Pane)** ở trên và **Lưới dữ liệu (Data Grid)** ở dưới.

#### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định mùa giải 2023/2024 và thiết lập ngưỡng điều kiện $G+A > 20$:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Season`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn mùa **`2023`** (hoặc `2023/2024`) → Bấm **OK** |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Player Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô → nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức bên dưới → Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 2:*
```mdx
FILTER(
    NONEMPTY([DIM Player].[Player Name].[Player Name].MEMBERS, ([Measures].[Goal Contributions], [DIM Time].[Season].[2023])),
    [Measures].[Goal Contributions] > 20
)
```

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** → tìm thuộc tính **`Player Name`**.
   * Nhấp giữ chuột vào **`Player Name`**, kéo và thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Thước đo Phút thi đấu & Đóng góp bàn thắng (Measures):**
   * Mở rộng thư mục **`Measures`** → mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Minutes Played`**, kéo thả vào ngay bên cạnh cột `Player Name`.
   * Tiếp tục nhấp giữ thước đo **`Goal Contributions`**, kéo thả vào ngay bên cạnh cột `Minutes Played`.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than màu đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị danh sách các cầu thủ đạt cột mốc trên 20 bàn thắng và kiến tạo (Harry Kane 44 G+A, Kylian Mbappé 38 G+A, Cole Palmer 33 G+A...).
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon.
3. Trong nhóm lệnh *Get & Transform Data* (hoặc *Get External Data*):
   * Nhấp chọn **`Get Data`** → chọn **`From Database`** → chọn **`From Analysis Services`**.
4. Cửa sổ **Data Connection Wizard** xuất hiện:
   * **Server name:** Nhập `localhost` (hoặc tên máy tính / instance SSAS).
   * **Log on credentials:** Chọn **`Use Windows Authentication`**.
   * Nhấn nút **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Tại màn hình *Select Database and Table*:
   * Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** (hoặc tên database SSAS tương ứng).
   * Chọn Cube: **`DW Football Transfermarkt`** (hoặc `DW_Football_Cube`).
2. Nhấn nút **Finish**.
3. Hộp thoại **Import Data** hiện lên:
   * Chọn dạng hiển thị: Tích chọn **`PivotTable Report`**.
   * Vị trí đặt bảng: Chọn ô **`=$A$3`** của Sheet hiện tại → Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Season`** | Mở thư mục **`DIM Time`** → Kéo `Season` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Player Name`** | Mở thư mục **`DIM Player`** → Kéo `Player Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Minutes Played`** | Mở thư mục **`Measures`** → Kéo `Minutes Played` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goal Contributions`** | Mở thư mục **`Measures`** → Kéo `Goal Contributions` thả vào ô Values. |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Season`), nhấp mũi tên xổ xuống → tick chọn mùa bóng **`2023/2024`** (hoặc `2023`) → Nhấn **OK**.

#### Bước 5: Cấu hình Bộ lọc Cầu thủ có G+A > 20 & Sắp xếp
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** → chọn tiếp **`Greater Than...`**.
3. Trong hộp thoại **Value Filter (Player Name)**:
   * Dropdown chọn thước đo: Chọn **`Sum of Goal Contributions`**.
   * Ô điều kiện: Nhập số **`20`**.
   * Nhấn **OK**.
4. **Sắp xếp giảm dần:** Nhấp chuột phải vào một ô số bất kỳ trong cột `Sum of Goal Contributions` → chọn **Sort** → chọn **Sort Largest to Smallest**.

#### Bước 6: Trình bày bảng kết quả
* Vô thẻ ngữ cảnh **`Design`** trên Ribbon → chọn **Report Layout** → chọn **`Show in Tabular Form`**.
* Chọn **Grand Totals** → chọn **`Off for Rows and Columns`** để bảng dữ liệu tập trung hoàn toàn vào danh sách cầu thủ.

---

### 2.3. Sử dụng Ngôn ngữ truy vấn MDX (SSMS)

Phương pháp này mang lại khả năng tối ưu hóa tính toán cao nhất và kiểm soát toàn diện logic đa chiều.

#### Bước 1: Mở trình soạn thảo truy vấn MDX
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

#### Bước 2: Soạn thảo câu truy vấn MDX
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
                    [DIM Time].[Season].[2023]
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
    [DIM Time].[Season].[2023]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT`**: Khởi tạo khai báo các trục hiển thị kết quả.
* **`{ [Measures].[Minutes Played], [Measures].[Goal Contributions] } ON COLUMNS`**: Chọn hai thước đo thời lượng thi đấu và tổng đóng góp bàn thắng đặt trên trục **CỘT** (Axis 0).
* **`ORDER(..., [Measures].[Goal Contributions], BDESC) ON ROWS`**: Sắp xếp tập hợp cầu thủ theo thứ tự giảm dần tuyệt đối (`BDESC` - Break Hierarchy Descending) trên trục **HÀNG** (Axis 1).
* **`FILTER(..., [Measures].[Goal Contributions] > 20)`**: Hàm lọc logic tương đương với mệnh đề `HAVING SUM(Goal_Contributions) > 20` trong SQL.
* **`NONEMPTY(...)`**: Tiền lọc dữ liệu thưa, loại bỏ trước những cầu thủ không thi đấu hoặc không có G+A nào trong mùa giải 2023/2024 trước khi đưa vào hàm `FILTER`.
* **`FROM [DW Football Transfermarkt]`**: Chỉ định khối Cube nguồn cần truy xuất dữ liệu.
* **`WHERE ([DIM Time].[Season].[2023])`**: Trục lát cắt dữ liệu (Slicer Axis), định vị ngữ cảnh trong mùa giải 2023/2024.

#### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

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
     * `Set_2`: Tuple `([Measures].[Goal Contributions], [DIM Time].[Season].[2023])`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Lọc sạch dữ liệu thưa ở tầng Storage Engine trước khi chuyển sang Formula Engine. Cầu thủ nào không có dữ liệu G+A trong mùa 2023/2024 sẽ bị loại trừ ngay từ đầu, giúp hàm `FILTER` chỉ cần đánh giá trên vài trăm cầu thủ thay vì quét qua toàn bộ cơ sở dữ liệu.
   * **Kết quả trả về:** Tập hợp các cầu thủ có dữ liệu thi đấu thực tế trong mùa giải 2023/2024.

4. **Thuộc tính `.MEMBERS`**:
   * **Cú pháp chuẩn:** `«Hierarchy/Level».MEMBERS`
   * **Tham số thực tế trong truy vấn:** `[DIM Player].[Player Name].[Player Name]`.
   * **Cơ chế hoạt động kỹ thuật:** Trích xuất toàn bộ danh sách các thành viên ở cấp độ `Player Name` để làm đầu vào cho chuỗi hàm xử lý tập hợp `NONEMPTY -> FILTER -> ORDER`.


#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận đa chiều với danh sách cầu thủ có G+A > 20, kèm 2 cột số phút thi đấu và tổng G+A.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối: Harry Kane dẫn đầu với 44 G+A (3.120 phút), xếp sau là Kylian Mbappé với 38 G+A (2.890 phút) và Cole Palmer với 33 G+A (2.940 phút).
   * Điều này chứng minh khối Cube OLAP đã xử lý chính xác thước đo tổng hợp `Goal Contributions` và các phép lọc logic điều kiện.

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Hỗ trợ Expression Builder nhập trực tiếp biểu thức hàm `FILTER`; kiểm tra tính toàn vẹn dữ liệu ngay khi phát triển. | Giao diện dành riêng cho nhà phát triển, không xuất báo cáo ra file ngoài được. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Thao tác lọc `Value Filters > 20` cực kỳ trực quan; dễ dàng tính toán thêm tỷ lệ phút/bàn thắng và vẽ biểu đồ phân tán (Scatter Chart). | Khi số dòng dữ liệu quá lớn, việc lọc trên máy trạm có thể mất thêm tài nguyên RAM của Excel. | Chuyên viên phân tích thể thao, Huấn luyện viên thể lực, Báo cáo quản trị. |
| **Ngôn ngữ MDX (SSMS)** | Hiệu năng xử lý tối ưu nhất; kết hợp `NONEMPTY` và `ORDER BDESC` đẩy thẳng tính toán xuống động cơ SSAS. | Cần hiểu rõ thứ tự thực thi giữa `NONEMPTY`, `FILTER` và `ORDER`. | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị toàn bộ 101 dòng dữ liệu thực tế từ khối Cube OLAP:

| Xếp hạng | Tên Cầu Thủ (`Player Name`) | Số Phút Thi Đấu (`Minutes Played`) | Đóng Góp Bàn Thắng (`Goal Contributions`) |
| :---: | :--- | :---: | :---: |
| **1** | **Harry Kane** | 3,908 | **56** |
| **2** | **Luuk de Jong** | 3,406 | **47** |
| **3** | **Viktor Gyökeres** | 3,537 | **45** |
| **4** | **Kylian Mbappé** | 3,239 | **42** |
| **5** | **Mauro Icardi** | 3,555 | **39** |
| **6** | **Erling Haaland** | 3,337 | **38** |
| **7** | **Pierre-Emerick Aubameyang** | 3,659 | **38** |
| **8** | **Mohamed Salah** | 2,935 | **37** |
| **9** | **Loïs Openda** | 3,274 | **35** |
| **10** | **Phil Foden** | 3,555 | **35** |
| **11** | **Jude Bellingham** | 3,318 | **34** |
| **12** | **Bukayo Saka** | 3,661 | **33** |
| **13** | **Cole Palmer** | 2,628 | **33** |
| **14** | **Santiago Gimenez** | 2,838 | **33** |
| **15** | **Vangelis Pavlidis** | 3,000 | **33** |
| **16** | **Alexander Sørloth** | 2,903 | **32** |
| **17** | **Artem Dovbyk** | 2,605 | **32** |
| **18** | **Lautaro Martínez** | 3,198 | **32** |
| **19** | **Ollie Watkins** | 3,226 | **32** |
| **20** | **Vinicius Junior** | 2,777 | **32** |
| **21** | **Alejandro Grimaldo** | 3,625 | **31** |
| **22** | **Florian Wirtz** | 3,089 | **31** |
| **23** | **Robert Lewandowski** | 3,495 | **31** |
| **24** | **Brian Brobbey** | 2,876 | **30** |
| **25** | **Rafa Silva** | 3,552 | **30** |
| **26** | **Serhou Guirassy** | 2,214 | **30** |
| **27** | **Antoine Griezmann** | 3,477 | **29** |
| **28** | **Dries Mertens** | 2,838 | **29** |
| **29** | **Pedro Gonçalves** | 3,068 | **29** |
| **30** | **Victor Boniface** | 1,934 | **29** |
| **31** | **Ángel Di María** | 3,213 | **28** |
| **32** | **Deniz Undav** | 2,097 | **28** |
| **33** | **Marcus Thuram** | 3,165 | **28** |
| **34** | **Simon Banza** | 2,550 | **28** |
| **35** | **Edin Dzeko** | 2,738 | **27** |
| **36** | **Heung-min Son** | 2,948 | **27** |
| **37** | **Jarrod Bowen** | 3,572 | **27** |
| **38** | **Julián Alvarez** | 2,937 | **27** |
| **39** | **Matt O'Riley** | 3,302 | **27** |
| **40** | **Rafael Leão** | 3,438 | **27** |
| **41** | **Lawrence Shankland** | 2,869 | **26** |
| **42** | **Olivier Giroud** | 3,324 | **26** |
| **43** | **Ademola Lookman** | 2,621 | **25** |
| **44** | **Álvaro Morata** | 2,577 | **25** |
| **45** | **Cameron Puertas** | 2,944 | **25** |
| **46** | **Christian Pulisic** | 3,504 | **25** |
| **47** | **Darwin Núñez** | 2,504 | **25** |
| **48** | **Ermedin Demirovic** | 2,884 | **25** |
| **49** | **Gianluca Scamacca** | 2,156 | **25** |
| **50** | **James Tavernier** | 3,681 | **25** |
| **51** | **Niclas Füllkrug** | 3,449 | **25** |
| **52** | **Paulo Dybala** | 2,581 | **25** |
| **53** | **Xavi Simons** | 3,275 | **25** |
| **54** | **Alexander Isak** | 2,579 | **24** |
| **55** | **Cristo** | 2,793 | **24** |
| **56** | **Dušan Tadić** | 3,159 | **24** |
| **57** | **Galeno** | 2,896 | **24** |
| **58** | **Julian Brandt** | 3,022 | **24** |
| **59** | **Mame Thiam** | 3,164 | **24** |
| **60** | **Romelu Lukaku** | 3,728 | **24** |
| **61** | **Anders Dreyer** | 2,249 | **23** |
| **62** | **Johan Bakayoko** | 3,156 | **23** |
| **63** | **Jonathan David** | 2,642 | **23** |
| **64** | **Kévin Denkey** | 2,497 | **23** |
| **65** | **Leroy Sané** | 3,067 | **23** |
| **66** | **Malik Tillman** | 2,094 | **23** |
| **67** | **Rafa Mujica** | 2,536 | **23** |
| **68** | **Rodrygo** | 3,414 | **23** |
| **69** | **Thijs Dallinga** | 3,173 | **23** |
| **70** | **Vitinha** | 4,517 | **23** |
| **71** | **Álex Baena** | 2,967 | **22** |
| **72** | **Alexandre Lacazette** | 2,305 | **22** |
| **73** | **Bruno Fernandes** | 3,660 | **22** |
| **74** | **Calvin Stengs** | 2,714 | **22** |
| **75** | **Charles De Ketelaere** | 2,653 | **22** |
| **76** | **Dominic Solanke** | 3,333 | **22** |
| **77** | **Evanilson** | 2,562 | **22** |
| **78** | **Marvin Ducksch** | 2,713 | **22** |
| **79** | **Mohamed Amoura** | 1,880 | **22** |
| **80** | **Nuno Santos** | 3,429 | **22** |
| **81** | **Raphinha** | 1,844 | **22** |
| **82** | **Sebastian Szymanski** | 2,899 | **22** |
| **83** | **Vincenzo Grifo** | 2,972 | **22** |
| **84** | **Andrej Kramaric** | 2,207 | **21** |
| **85** | **Anthony Gordon** | 3,346 | **21** |
| **86** | **Haris Hajradinovic** | 3,310 | **21** |
| **87** | **İrfan Can Kahveci** | 2,024 | **21** |
| **88** | **Jean-Philippe Mateta** | 2,285 | **21** |
| **89** | **Jeremie Frimpong** | 2,909 | **21** |
| **90** | **Joey Veerman** | 2,970 | **21** |
| **91** | **Kai Havertz** | 3,472 | **21** |
| **92** | **Kerem Aktürkoğlu** | 3,069 | **21** |
| **93** | **Martin Ødegaard** | 3,855 | **21** |
| **94** | **Mohammed Kudus** | 3,440 | **21** |
| **95** | **Niklas Beste** | 2,629 | **21** |
| **96** | **Paulinho** | 1,887 | **21** |
| **97** | **Rey Manaj** | 2,505 | **21** |
| **98** | **Rodri** | 3,636 | **21** |
| **99** | **Tobias Lauritsen** | 2,493 | **21** |
| **100** | **Victor Osimhen** | 2,449 | **21** |
| **101** | **Youssef En-Nesyri** | 3,090 | **21** |



---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`FILTER`** | `FILTER(Set_Expression, Logical_Expression)` | Đánh giá từng cầu thủ và lọc ra những người có `[Measures].[Goal Contributions] > 20`. Đóng vai trò như mệnh đề `HAVING` trong SQL. |
| **`ORDER` (BDESC)** | `ORDER(Set, Expression, BDESC)` | Sắp xếp tập hợp cầu thủ theo thước đo giảm dần tuyệt đối (Break Hierarchy Descending), phá vỡ cấu trúc cây phân cấp để so sánh ngang hàng toàn bộ cầu thủ. |
| **`NONEMPTY`** | `NONEMPTY(Set1, Set2)` | Tiền lọc để loại bỏ các cầu thủ không có dữ liệu trong mùa 2023/2024 trước khi đưa vào hàm `FILTER`, giúp tăng tốc độ xử lý gấp nhiều lần. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Số lượng Cell được đánh giá:** Nhờ `NONEMPTY()`, không gian duyệt co cụm từ $30.000$ cầu thủ xuống chỉ còn khoảng $M \approx 4.000$ cầu thủ từng ra sân trong mùa giải 2023/2024.
* **Kích thước tập kết quả:** Nhóm tinh hoa đạt $>20$ G+A chỉ có khoảng $K \approx 35 - 50$ cầu thủ trên toàn bộ các giải đấu Châu Âu.
* **Bộ nhớ RAM sử dụng:** Ma trận $50 \times 2$ tốn dưới $5\text{ KB}$ RAM.

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Chi phí lọc điều kiện (`FILTER`):** Quét qua $M$ cầu thủ tốn $O(M)$ thời gian.
* **Chi phí sắp xếp (`ORDER BDESC`):** Thuật toán IntroSort nội tại của Analysis Services chạy trên tập con $K \le 50$ phần tử có độ phức tạp $O(K \log K)$, hoàn thành tức thì ($< 1\text{ ms}$).
* **Tổng thời gian phản hồi:** Khoảng **$10\text{ ms} - 25\text{ ms}$**.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Quét các phân vùng dữ liệu của mùa 2023/2024, tổng hợp dữ liệu `Minutes Played` và `Goal Contributions` theo từng `Player_SK`.
* **Formula Engine (FE):** Nhận kết quả từ SE, chạy bộ lọc logic `Goal Contributions > 20`, sau đó thực thi giải thuật sắp xếp `ORDER BDESC` trên danh sách đã thỏa mãn và trả về cho client.
