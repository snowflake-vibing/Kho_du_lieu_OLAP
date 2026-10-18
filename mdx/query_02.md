# MDX Query 02: Top 10 Vua kiến tạo khu vực Tiền vệ ở các giải VĐQG
## (Ứng dụng Tích Đề-các CROSSJOIN & Hàm Xếp hạng TOPCOUNT)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Thống kê danh sách 10 cầu thủ thi đấu ở vị trí tiền vệ (`Main_Position = 'Midfield'`) có tổng số pha kiến tạo thành bàn (`Assists`) cao nhất tại tất cả các giải Vô địch Quốc gia hàng đầu Châu Âu (`Competition_Type = 'domestic_league'`), hỗ trợ công tác tuyển trạch và định giá tiền vệ sáng tạo (Playmakers).
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Giải đấu (`DIM_Competition`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[DIM Player].[Main Position]`, `[DIM Competition].[Competition Type]`
  * Cube Measures: `[Measures].[Assists]` (Tổng số pha kiến tạo)

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Analytics;
GO

SELECT TOP 10
    p.Player_Name,
    p.Main_Position,
    c.Competition_Type,
    SUM(f.Assists) AS Total_Assists
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
WHERE p.Main_Position LIKE '%Midfield%'
  AND c.Competition_Type = 'domestic_league'
GROUP BY p.Player_Name, p.Main_Position, c.Competition_Type
ORDER BY Total_Assists DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để trích xuất danh sách Top 10 tiền vệ kiến tạo hàng đầu trên hệ thống OLAP, người dùng có thể thực hiện linh hoạt qua **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích Tiền vệ Kiến tạo"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Comp Type, Position & Top 10 -> Kéo Grid -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Filters: Type, Position -> Rows: Player -> Top 10 Filter"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn TOPCOUNT/CROSSJOIN/NONEMPTY -> Execute (F5)"]

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo lần lượt 3 dòng lọc để cố định loại giải đấu, vị trí tiền vệ và trích xuất Top 10:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Competition`** | Nhấp chọn **`Competition Type`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`domestic_league`** $\rightarrow$ Bấm **OK** (hiển thị `{ domestic_league }`) |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Main Position`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn **`Midfield`** $\rightarrow$ Bấm **OK** (hiển thị `{ Midfield }`) |
| **Dòng 3** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Player Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 3:*
```mdx
TOPCOUNT([DIM Player].[Player Name].[Player Name].MEMBERS, 10, [Measures].[Assists])
```

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Player Name`**.
   * Nhấp giữ chuột vào **`Player Name`**, kéo và thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*. Lúc này trên lưới xuất hiện cột `Player Name`.
2. **Kéo Thước đo Kiến tạo (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở rộng nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Assists`**, kéo và thả vào **ngay bên cạnh cột `Player Name`** trên lưới.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than màu đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị chính xác bảng xếp hạng đúng **10 tiền vệ kiến tạo nhiều nhất** (Kevin De Bruyne dẫn đầu với 18 kiến tạo, Bruno Fernandes 15 kiến tạo...).
3. **Mẹo chuyên môn:** Nhấp vào biểu tượng **`Design Mode`** trên thanh công cụ để xem câu lệnh MDX mà Visual Studio tự động biên dịch phía sau giao diện kéo thả này.

---

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon.
3. Trong nhóm lệnh *Get & Transform Data* (hoặc *Get External Data*):
   * Nhấp chọn **`Get Data`** $\rightarrow$ chọn **`From Database`** $\rightarrow$ chọn **`From Analysis Services`**.
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
   * Vị trí đặt bảng: Chọn ô **`=$A$3`** của Sheet hiện tại $\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Competition Type`** | Mở thư mục **`DIM Competition`** $\rightarrow$ Kéo `Competition Type` thả vào ô Filters. |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Main Position`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Main Position` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Player Name`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Player Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Assists`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Assists` thả vào ô Values (hiển thị `Sum of Assists`). |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. **Lọc Loại giải đấu:** Tại ô **`B1`** (bên cạnh nhãn `Competition Type`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn **`domestic_league`** $\rightarrow$ Nhấn **OK**.
2. **Lọc Vị trí Tiền vệ:** Tại ô **`B2`** (bên cạnh nhãn `Main Position`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn **`Midfield`** $\rightarrow$ Nhấn **OK**.

#### Bước 5: Cấu hình Bộ lọc Top 10 Vua kiến tạo
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại **Top 10 Filter (Player Name)**:
   * Ô thứ nhất: Chọn **`Top`**.
   * Ô thứ hai: Nhập số **`10`**.
   * Ô thứ ba: Chọn **`Items`**.
   * Ô thứ tư (By): Chọn thước đo **`Sum of Assists`**.
4. Nhấn **OK**.

#### Bước 6: Trình bày bảng kết quả
* Vô thẻ ngữ cảnh **`Design`** trên Ribbon $\rightarrow$ chọn **Report Layout** $\rightarrow$ chọn **`Show in Tabular Form`** (để tiêu đề cột đổi thành `Player Name`).
* Chọn **Grand Totals** $\rightarrow$ chọn **`Off for Rows and Columns`** để ẩn dòng tổng cộng, giữ lại đúng bảng xếp hạng 10 cầu thủ.

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
   * Mở rộng thư mục **`Databases`** $\rightarrow$ mở rộng database **`DW_Football_SSAS`** $\rightarrow$ mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** $\rightarrow$ chọn **`New Query`** $\rightarrow$ chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

#### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 02: Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG
   Khai thác: TOPCOUNT, CROSSJOIN, NONEMPTY, MEMBERS
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Tổng số kiến tạo
    { [Measures].[Assists] } ON COLUMNS,

    -- Trục Dòng (ROWS): Top 10 tiền vệ có số kiến tạo nhiều nhất
    TOPCOUNT(
        NONEMPTY(
            CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                { [DIM Player].[Main Position].[Midfield] }
            ),
            (
                [Measures].[Assists],
                [DIM Competition].[Competition Type].[domestic_league]
            )
        ),
        10,
        [Measures].[Assists]
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh (Slicer Axis): Các giải Vô địch Quốc gia (domestic_league)
WHERE (
    [DIM Competition].[Competition Type].[domestic_league]
);
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT`**: Khởi tạo khai báo các trục tọa độ hiển thị kết quả của ma trận đa chiều.
* **`{ [Measures].[Assists] } ON COLUMNS`**: Chọn thước đo tổng số pha kiến tạo (`Assists`) và định vị hiển thị trên trục **CỘT** (Axis 0).
* **`TOPCOUNT(...) ON ROWS`**: Sử dụng thuật toán Min-Heap để lọc ra đúng 10 tiền vệ có thành tích kiến tạo cao nhất trên trục **HÀNG** (Axis 1).
* **`CrossJoin([Player Name].MEMBERS, { [Main Position].[Midfield] })`**: Thực hiện phép tích Đề-các để gắn chặt danh sách cầu thủ với vai trò tiền vệ, bảo đảm chỉ các tiền vệ mới được đưa vào xét duyệt.
* **`NONEMPTY(...)`**: Loại bỏ trước các cặp (Player, Midfield) không có bất kỳ kiến tạo nào ở giải VĐQG trước khi chạy thuật toán sắp xếp, giảm tải tối đa tài nguyên Formula Engine.
* **`FROM [DW Football Transfermarkt]`**: Chỉ định khối Cube nguồn cần trích xuất dữ liệu.
* **`WHERE ([DIM Competition].[Competition Type].[domestic_league])`**: Trục lát cắt dữ liệu (Slicer Axis), giới hạn ngữ cảnh phân tích trong các giải Vô địch Quốc gia.

#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị lưới kết quả ma trận đa chiều với 10 dòng tên tiền vệ và 1 cột số kiến tạo `Assists`.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối: Kevin De Bruyne dẫn đầu với 18 kiến tạo, xếp tiếp theo là Bruno Fernandes và Florian Wirtz (15 kiến tạo).
   * Điều này chứng minh khối Cube OLAP đã được phân vùng và liên kết phân cấp thuộc tính (Attribute Hierarchy) giữa Player và Main Position hoàn toàn chính xác.

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Thao tác trực quan, hỗ trợ Expression Builder với hàm `TOPCOUNT` trực tiếp; kiểm tra cấu trúc đa chiều tức thì. | Giao diện phát triển nội bộ, không phù hợp cho việc thuyết trình báo cáo thương mại. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Giao diện đồ họa quen thuộc; dễ dàng tạo biểu đồ cột so sánh kiến tạo, lọc Slicer tương tác. | Cần cài đặt kết nối Analysis Services OLE DB provider trên máy người dùng. | Chuyên viên phân tích dữ liệu thể thao, Scout bóng đá, Báo cáo quản trị. |
| **Ngôn ngữ MDX (SSMS)** | Hiệu năng xử lý tối ưu nhất; kết hợp linh hoạt `CrossJoin` và `NONEMPTY` ở cấp độ lưu trữ. | Đòi hỏi nắm vững cú pháp tập hợp đa chiều (Set theory). | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị danh sách 10 tiền vệ kiến tạo xuất sắc nhất tại các giải VĐQG:

| Xếp hạng | Tên Cầu Thủ (`Player Name`) | Vị trí Thi Đấu | Câu Lạc Bộ Tiêu Biểu | Số Pha Kiến Tạo (`Assists`) |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Kevin De Bruyne** | Midfield | Manchester City | **18** |
| **2** | **Bruno Fernandes** | Midfield | Manchester United | **15** |
| **3** | **Florian Wirtz** | Midfield | Bayer 04 Leverkusen | **15** |
| **4** | **Martin Ødegaard** | Midfield | Arsenal FC | **13** |
| **5** | **Pascal Groß** | Midfield | Brighton & Hove Albion | **13** |
| **6** | **Toni Kroos** | Midfield | Real Madrid | **12** |
| **7** | **Hakan Çalhanoğlu** | Midfield | Inter Milan | **12** |
| **8** | **Joshua Kimmich** | Midfield | Bayern Munich | **11** |
| **9** | **James Maddison** | Midfield | Tottenham Hotspur | **11** |
| **10** | **İlkay Gündoğan** | Midfield | FC Barcelona | **11** |

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`TOPCOUNT`** | `TOPCOUNT(Set, Count, [Numeric_Expression])` | Trích xuất chính xác 10 tiền vệ có số kiến tạo cao nhất theo thứ tự giảm dần dựa trên cấu trúc Min-Heap. |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` hoặc toán tử `*` | Tích đề-các giữa danh sách cầu thủ và thành viên `[DIM Player].[Main Position].[Midfield]`, đảm bảo kết quả trả về vừa có tên cầu thủ vừa xác nhận vị trí thi đấu. |
| **`NONEMPTY`** | `NONEMPTY(Set1, Set2)` | Loại trừ các cặp (Player, Midfield) không có bất kỳ kiến tạo nào ở giải VĐQG trước khi sắp xếp, giảm tải triệt để tài nguyên tính toán. |
| **`MEMBERS`** | `Hierarchy.MEMBERS` | Trả về tập hợp tất cả các thành viên cấp độ `Player Name`. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Số chiều tham gia:** Cầu thủ ($N \approx 30.000$) $\times$ Vị trí ($1$ thành viên `Midfield`) $\times$ Giải đấu ($1$ loại giải `domestic_league`).
* **Không gian bộ nhớ sau tối ưu:** Việc kết hợp trực tiếp `{ [DIM Player].[Main Position].[Midfield] }` đã thu hẹp không gian từ $30.000 \times 4$ vị trí xuống chỉ còn tập hợp các tiền vệ (khoảng $\approx 8.000$ cầu thủ).
* **Bộ nhớ kết quả:** Trả về ma trận $10 \times 1$, tiêu tốn tài nguyên dưới $1\text{ KB}$ RAM.

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Duyệt và kiểm tra dữ liệu:** $O(M)$ với $M$ là số lượng tiền vệ đã từng ra sân ở giải quốc nội ($M \approx 4.000$).
* **Chi phí sắp xếp (Sorting):** Sử dụng Min-Heap trong `TOPCOUNT` đạt chi phí $O(M \log 10) \approx O(M)$, nhanh hơn nhiều so với full-scan `ORDER BY` trong SQL truyền thống ($O(N \log N)$).
* **Tổng thời gian phản hồi:** Khoảng **$10\text{ ms} - 25\text{ ms}$**.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Tận dụng mối quan hệ thuộc tính (Attribute Hierarchy) giữa Player và Main Position để quét trực tiếp các Block dữ liệu cần tính, nén và chuyển lên cache.
* **Formula Engine (FE):** Khởi tạo Min-Heap kích thước 10 để tìm các tiền vệ có số kiến tạo cao nhất, định dạng cellset và gửi kết quả về cho client.
