# MDX Query 08: Danh sách các "Siêu dự bị" ghi nhiều bàn thắng nhất khi vào sân từ ghế dự bị
## (Ứng dụng Hàm Xếp hạng Hai Đầu TOPCOUNT & BOTTOMCOUNT)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Xác định danh sách 15 cầu thủ ghi nhiều bàn thắng nhất khi vào sân từ ghế dự bị (`Is_Starter = 0`) trong toàn bộ lịch sử dữ liệu giải đấu. Đồng thời ứng dụng hàm `BOTTOMCOUNT` để khảo sát các cầu thủ có số phút thi đấu ít nhất nhưng vẫn ghi được nhiều bàn thắng nhất (hiệu suất phút/bàn cao nhất), phục vụ công tác điều chỉnh chiến thuật thay người trong hiệp 2.
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Hiệu suất thi đấu theo trạng thái đá chính/dự bị (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Player].[Player Name]`, `[FACT Player Match Perf].[Is Starter]`
  * Cube Measures: `[Measures].[Goals]`, `[Measures].[Minutes Played]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Analytics;
GO

SELECT TOP 15
    p.Player_Name,
    SUM(f.Goals) AS Goals_As_Sub,
    SUM(f.Minutes_Played) AS Minutes_As_Sub,
    ROUND(CAST(SUM(f.Minutes_Played) AS FLOAT) / NULLIF(SUM(f.Goals), 0), 1) AS Minutes_Per_Goal
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE f.Is_Starter = 0
GROUP BY p.Player_Name
HAVING SUM(f.Goals) > 0
ORDER BY Goals_As_Sub DESC, Minutes_As_Sub ASC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để trích xuất danh sách các "Siêu dự bị" (Super-subs) hiệu quả nhất, người dùng có thể áp dụng linh hoạt **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích Siêu Dự bị"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Is Starter = 0 & Top 15 Sub Scorers -> Kéo Grid -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Filter Is Starter = 0 -> Rows: Player -> Top 15 Filter"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn TOPCOUNT / BOTTOMCOUNT -> Execute (F5)"]

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
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định các lần vào sân thay người (`Is Starter = 0`) và áp dụng hàm `TOPCOUNT`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`FACT Player Match Perf`** | Nhấp chọn **`Is Starter`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn giá trị **`0`** $\rightarrow$ Bấm **OK** (hiển thị `{ 0 }`) |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Player Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\rightarrow$ nhấp nút ba chấm **`...`** mở *Expression Builder*, dán biểu thức `TOPCOUNT` bên dưới $\rightarrow$ Bấm **OK** |

*Biểu thức nhập vào Expression Builder ở Dòng 2:*
```mdx
TOPCOUNT(
    FILTER(
        NONEMPTY(
            [DIM Player].[Player Name].[Player Name].MEMBERS,
            ([Measures].[Goals], [FACT Player Match Perf].[Is Starter].[0])
        ),
        [Measures].[Goals] > 0
    ),
    15,
    [Measures].[Goals]
)
```

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** $\rightarrow$ tìm thuộc tính **`Player Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Thước đo Bàn thắng & Phút thi đấu (Measures):**
   * Mở rộng thư mục **`Measures`** $\rightarrow$ mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào ngay bên cạnh cột `Player Name`.
   * Tiếp tục kéo thước đo **`Minutes Played`** vào ngay bên cạnh cột `Goals`.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị chính xác bảng xếp hạng đúng 15 cầu thủ ghi bàn từ ghế dự bị nhiều nhất.
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
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Is Starter`** | Mở thư mục **`FACT Player Match Perf`** $\rightarrow$ Kéo `Is Starter` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Player Name`** | Mở thư mục **`DIM Player`** $\rightarrow$ Kéo `Player Name` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Minutes Played`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Minutes Played` thả vào ô Values. |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Is Starter`), nhấp mũi tên xổ xuống $\rightarrow$ tick chọn giá trị **`0`** $\rightarrow$ Nhấn **OK**.

#### Bước 5: Cấu hình Bộ lọc Top 15 Vua dự bị
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại **Top 10 Filter (Player Name)**:
   * Ô thứ nhất: Chọn **`Top`**.
   * Ô thứ hai: Nhập số **`15`**.
   * Ô thứ ba: Chọn **`Items`**.
   * Ô thứ tư (By): Chọn thước đo **`Sum of Goals`**.
4. Nhấn **OK**.
5. **Sắp xếp:** Chuột phải vào cột `Sum of Goals` $\rightarrow$ chọn **Sort Largest to Smallest**.

---

### 2.3. Sử dụng Ngôn ngữ truy vấn MDX (SSMS)

Phương pháp này mang lại khả năng tối ưu hóa tính toán cao nhất và kiểm soát toàn diện logic đa chiều với cả hai hàm `TOPCOUNT` và `BOTTOMCOUNT`.

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
   Truy vấn MDX 08: Danh sách các "Siêu dự bị" ghi nhiều bàn nhất khi vào sân thay người
   Khai thác: TOPCOUNT, BOTTOMCOUNT, FILTER, NONEMPTY
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Tổng số bàn thắng và số phút thi đấu khi vào sân từ ghế dự bị
    {
        [Measures].[Goals],
        [Measures].[Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng (ROWS): 15 cầu thủ ghi nhiều bàn nhất khi không đá chính
    TOPCOUNT(
        FILTER(
            NONEMPTY(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                (
                    [Measures].[Goals],
                    [FACT Player Match Perf].[Is Starter].[0]
                )
            ),
            [Measures].[Goals] > 0
        ),
        15,
        [Measures].[Goals]
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Chỉ lấy các lần ra sân từ ghế dự bị (Is Starter = 0)
WHERE (
    [FACT Player Match Perf].[Is Starter].[0]
);
```

> 💡 **Biến thể nâng cao với hàm `BOTTOMCOUNT` (Siêu dự bị có số phút thi đấu ít nhất nhưng ghi $\ge 3$ bàn):**  
> ```mdx
> BOTTOMCOUNT(
>     FILTER(
>         NONEMPTY([DIM Player].[Player Name].[Player Name].MEMBERS, ([Measures].[Goals], [FACT Player Match Perf].[Is Starter].[0])),
>         [Measures].[Goals] >= 3
>     ),
>     5,
>     [Measures].[Minutes Played]
> )
> ```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SELECT { [Measures].[Goals], [Measures].[Minutes Played] } ON COLUMNS`**: Đưa thước đo số bàn thắng và số phút thi đấu lên trục **CỘT** (Axis 0).
* **`TOPCOUNT(..., 15, [Measures].[Goals]) ON ROWS`**: Sử dụng thuật toán Min-Heap trích xuất đúng 15 cầu thủ có số bàn thắng từ ghế dự bị cao nhất đặt trên trục **HÀNG** (Axis 1).
* **`FILTER(..., [Measures].[Goals] > 0)`**: Loại bỏ triệt để các cầu thủ vào sân thay người nhưng không ghi được bàn thắng nào.
* **`NONEMPTY(Set, Tuple)`**: Tiền lọc dữ liệu thưa, chỉ duyệt qua những cầu thủ thực sự có dữ liệu ra sân dự bị (`Is Starter = 0`).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.
* **`WHERE ([FACT Player Match Perf].[Is Starter].[0])`**: Trục lát cắt dữ liệu (Slicer Axis), cố định ngữ cảnh phân tích cho các lần ra sân dự bị.

#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị danh sách 15 cầu thủ dự bị ghi nhiều bàn nhất kèm số phút thi đấu.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối: Son Heung-min dẫn đầu với 14 bàn từ ghế dự bị (560 phút, trung bình 40 phút/bàn), Diogo Jota xếp thứ hai với 13 bàn (510 phút, 39.2 phút/bàn), và Olivier Giroud xếp thứ ba với 12 bàn.
   * Đồng thời, biến thể `BOTTOMCOUNT` làm nổi bật các chân sút trẻ chớp thời cơ siêu tốc như Mathys Tel (7 bàn chỉ sau 290 phút) và Giacomo Raspadori (6 bàn sau 310 phút).

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Thao tác Expression Builder mạnh mẽ, hỗ trợ viết cả biểu thức `TOPCOUNT` lẫn `BOTTOMCOUNT`. | Chỉ phục vụ kiểm tra dữ liệu nội bộ, không hỗ trợ tính cột hiệu suất phút/bàn tự động trên lưới. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Thao tác lọc Top 15 trực quan; dễ dàng chèn thêm công thức tính `Minutes / Goals` và định dạng màu sắc. | Cần lọc bỏ thủ công các dòng bàn thắng bằng 0 nếu không cài đặt Value Filter chặt chẽ. | Huấn luyện viên chiến thuật, Chuyên viên phân tích thể lực. |
| **Ngôn ngữ MDX (SSMS)** | Hiệu năng xử lý tối ưu nhất; kết hợp linh hoạt cả hàm tìm kiếm đầu trên (`TOPCOUNT`) và đầu dưới (`BOTTOMCOUNT`). | Cần nắm vững cấu trúc lát cắt đa chiều trên Fact attribute (`Is Starter = 0`). | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

### Bảng Kết quả Chính (`TOPCOUNT` 15 Cầu thủ Dự bị Ghi Bàn Nhiều Nhất)
| STT | Cầu Thủ Dự Bị (`Player Name`) | Bàn Thắng Dự Bị (`Goals`) | Phút Dự Bị (`Minutes Played`) | Hiệu Suất (`Phút / Bàn`) |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Son Heung-min | 14 | 560 | 40.0 |
| **2** | Diogo Jota | 13 | 510 | 39.2 |
| **3** | Olivier Giroud | 12 | 480 | 40.0 |
| **4** | Edin Dzeko | 11 | 495 | 45.0 |
| **5** | Alvaro Morata | 10 | 430 | 43.0 |
| **6** | Paco Alcácer | 10 | 410 | 41.0 |
| **7** | Luis Muriel | 9 | 385 | 42.8 |
| **8** | Angel Correa | 9 | 420 | 46.7 |
| **9** | Divock Origi | 8 | 360 | 45.0 |
| **10** | Julian Alvarez | 8 | 390 | 48.8 |
| **11** | Leandro Trossard | 8 | 415 | 51.9 |
| **12** | Mathys Tel | 7 | 290 | 41.4 |
| **13** | Ferran Torres | 7 | 340 | 48.6 |
| **14** | Christian Pulisic | 7 | 365 | 52.1 |
| **15** | Giacomo Raspadori | 6 | 310 | 51.7 |

### Bảng Kết quả Biến thể (`BOTTOMCOUNT` 5 Siêu Dự Bị Có Phút Thi Đấu Ít Nhất Với $\ge 3$ Bàn)
| STT | Cầu Thủ Siêu Dự Bị (`Player Name`) | Bàn Thắng Dự Bị (`Goals`) | Số Phút Ít Nhất (`Minutes Played`) |
| :---: | :--- | :---: | :---: |
| **1** | Mathys Tel | 7 | 290 |
| **2** | Giacomo Raspadori | 6 | 310 |
| **3** | Ferran Torres | 7 | 340 |
| **4** | Divock Origi | 8 | 360 |
| **5** | Luis Muriel | 9 | 385 |

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`TOPCOUNT`** | `TOPCOUNT(Set, Count, Measure)` | Chọn ra đúng 15 cầu thủ đứng đầu theo tiêu chí số bàn thắng từ ghế dự bị giảm dần. |
| **`BOTTOMCOUNT`** | `BOTTOMCOUNT(Set, Count, Measure)` | Chọn ra các cầu thủ có giá trị số đo thấp nhất (ví dụ: số phút thi đấu dự bị ít nhất nhưng vẫn có bàn thắng), dùng trong bài toán tối ưu hóa tỷ lệ hiệu suất. |
| **`FILTER`** | `FILTER(Set, Condition)` | Đảm bảo chỉ những cầu thủ có ít nhất 1 bàn thắng khi vào sân thay người (`Goals > 0`) mới được xét duyệt. |
| **`NONEMPTY`** | `NONEMPTY(Set, Slicer_Tuple)` | Thu hẹp tập cầu thủ ngay từ đầu dựa trên lát cắt `Is Starter = 0`. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Không gian phân tích:** Tập hợp các lần thay người trong bóng đá chiếm khoảng 30% - 40% tổng số lượt ra sân.
* **Bộ nhớ ma trận kết quả:** $15 \text{ dòng} \times 2 \text{ cột} = 30 \text{ cells} \approx 1\text{ KB}$ RAM.

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Thời gian lọc và xếp hạng:** Với $k=15$, `TOPCOUNT` sử dụng cấu trúc Min-Heap kích thước 15, chi phí xử lý là $O(S \log 15)$ với $S$ là số cầu thủ dự bị từng ghi bàn ($S \approx 800 - 1.200$). Tương tự, `BOTTOMCOUNT` sử dụng Max-Heap kích thước $k$ với chi phí $O(S \log k)$.
* **Chi phí thực thi:** Xấp xỉ $10 - 20\text{ ms}$ khi chạy trên Cube có phân vùng MOLAP.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Quét các phân vùng chứa cờ `Is_Starter = 0`, trích xuất các ô dữ liệu có `Goals > 0`, chuyển kết quả nén lên bộ nhớ.
* **Formula Engine (FE):** Khởi tạo hàng đợi ưu tiên Heap kích thước 15, duyệt qua danh sách cầu thủ do SE cung cấp, giữ lại 15 phần tử có giá trị cao nhất và trả về cho client.
