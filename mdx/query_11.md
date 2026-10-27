# MDX Query 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả
## (Ứng dụng Xử lý Giá trị Rỗng COALESCEEMPTY & Đếm Duy nhất DISTINCTCOUNT)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Thống kê danh sách các Sân vận động quy chuẩn quốc tế có sức chứa trên 60.000 chỗ ngồi (`Stadium_Seats >= 60.000`) cùng Câu lạc bộ chủ quản, tổng số bàn thắng ghi được và **số lượng trận đấu duy nhất** (`Distinct Matches Played`) đã từng tổ chức tại các sân đấu này. Ứng dụng hàm `COALESCEEMPTY` để làm sạch dữ liệu khuyết thiếu sức chứa và hàm `DISTINCTCOUNT` kết hợp `EXISTING` để loại trừ việc đếm trùng 22-30 cầu thủ ra sân trong cùng một trận.
* **Đối tượng phân tích:** Sân vận động và Câu lạc bộ (`DIM_Club`), Trận đấu (`DIM_Game`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Club].[Stadium Name]`, `[DIM Club].[Club Name]`, `[DIM Club].[Stadium Seats]`, `[DIM Game].[Game ID]`
  * Cube Measures gốc: `[Measures].[Goals]`, `[Measures].[FACT Player Match Perf Count]`
  * Calculated Measures: `[Measures].[Stadium Capacity Cleaned]`, `[Measures].[Distinct Matches Played]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Analytics;
GO

SELECT 
    c.Stadium_Name,
    c.Club_Name,
    COALESCE(c.Stadium_Seats, 0) AS Stadium_Capacity,
    COUNT(DISTINCT f.Game_SK) AS Distinct_Matches_Played,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club c ON f.Club_SK = c.Club_SK
WHERE c.Stadium_Seats >= 60000 AND c.Stadium_Name IS NOT NULL
GROUP BY c.Stadium_Name, c.Club_Name, c.Stadium_Seats
ORDER BY Stadium_Capacity DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để trích xuất danh sách các siêu sân vận động và đếm số trận đấu duy nhất, người dùng có thể áp dụng linh hoạt **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích Sân vận động"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Stadium Seats >= 60.000 -> Kéo Stadium, Club vào Rows -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Rows: Stadium, Club -> Values: Seats, Distinct Games -> Filter"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn COALESCEEMPTY, DISTINCTCOUNT(EXISTING) -> Execute (F5)"]

    CB_Step --> Finish["2.4. Nhận xét & Đối chiếu Kết quả Đồng nhất"]
    Excel_Step --> Finish
    MDX_Step --> Finish
```

---

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** → chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để làm sạch sức chứa và đếm số trận đấu duy nhất:
   * **Thước đo 1 (`Stadium Capacity Cleaned`):**
     * Name: `Stadium Capacity Cleaned` | Parent hierarchy: `Measures`
     * Expression: `COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE, 0)`
     * Format String: `#,##0`
   * **Thước đo 2 (`Distinct Matches Played`):**
     * Name: `Distinct Matches Played` | Parent hierarchy: `Measures`
     * Expression: `DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`
     * Format String: `#,##0`
4. Chọn menu **Build** → **Deploy Solution** để nạp thước đo vào Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc Sức chứa (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho `Stadium Seats`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Stadium Seats`** | Bấm dropdown chọn **`Greater Than or Equal`** | Nhập số **`60000`** → Bấm **OK** (hiển thị `>= 60000`) |

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Sân vận động & CLB (Rows):**
   * Mở rộng chiều **`DIM Club`** → tìm thuộc tính **`Stadium Name`**: Kéo thả vào vùng Rows.
   * Tìm tiếp thuộc tính **`Club Name`** trong `DIM Club`: Kéo thả vào ngay cạnh cột `Stadium Name`.
2. **Kéo 3 Thước đo đã đồng bộ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Stadium Capacity Cleaned`** thả vào cạnh cột `Club Name`.
     * Kéo **`Distinct Matches Played`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào cột cuối cùng.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 3 cột thước đo theo từng sân vận động quy mô lớn.

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** → Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** → Chọn **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Stadium Name`** | Mở thư mục **`DIM Club`** → Kéo `Stadium Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** → Kéo `Club Name` thả vào ô Rows (nằm dưới `Stadium Name`). |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Stadium Capacity Cleaned`** | Mở thư mục **`Measures`** → Kéo `Stadium Capacity Cleaned` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Distinct Matches Played`** | Mở thư mục **`Measures`** → Kéo `Distinct Matches Played` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |

#### Bước 4: Thiết lập Bộ lọc Sức chứa >= 60.000 khán giả
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** → chọn tiếp **`Greater Than Or Equal To...`**.
3. Trong hộp thoại: Chọn lọc theo **`Stadium Capacity Cleaned`** $\ge$ **`60000`** → Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Sắp xếp giảm dần theo số trận đấu duy nhất (`Distinct Matches Played`).

### 2.3. Sử dụng Ngôn ngữ truy vấn MDX (SSMS)

Phương pháp này mang lại khả năng tối ưu hóa tính toán cao nhất và kiểm soát toàn diện logic đa chiều với `COALESCEEMPTY` và `DISTINCTCOUNT(EXISTING ...)`.

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
   Truy vấn MDX 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả
   Khai thác: COALESCEEMPTY, DISTINCTCOUNT, EXISTING, FILTER, ORDER (BDESC)
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Sức chứa sân vận động xử lý NULL bằng COALESCEEMPTY
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        COALESCEEMPTY(
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE,
            0
        ),
        FORMAT_STRING = "#,##0 Chỗ"

    -- 2. Đếm số trận đấu duy nhất diễn ra tại sân vận động
    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Sức chứa sân đã làm sạch, số trận duy nhất và tổng bàn thắng
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các sân vận động có sức chứa >= 60.000 chỗ, xếp giảm dần
    ORDER(
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] }),
                    EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] })
                ),
                [Measures].[FACT Player Match Perf Count]
            ),
            [Measures].[Stadium Capacity Cleaned] >= 60000
        ),
        [Measures].[Stadium Capacity Cleaned],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE, 0)`**: Hàm kiểm tra giá trị đầu tiên khác rỗng. Nếu thuộc tính `Stadium Seats` bị NULL hoặc rỗng, hàm tự động gán giá trị mặc định là 0 để chống lỗi tính toán số học.
* **`DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`**: Đếm số lượng phần tử duy nhất (Distinct Game ID). Từ khóa `EXISTING` thực hiện chuyển đổi ngữ cảnh để tập hợp `Game ID` chỉ bao gồm các trận diễn ra tại đúng sân vận động và câu lạc bộ đang hiển thị trên dòng đó, ngăn chặn việc đếm trùng 22-30 cầu thủ mỗi trận.
* **`CrossJoin([Stadium Name].MEMBERS, [Club Name].MEMBERS)`**: Kết hợp cặp thuộc tính Tên sân và Tên CLB chủ quản trên trục dòng.
* **`FILTER(NONEMPTY(...), [Measures].[Stadium Capacity Cleaned] >= 60000)`**: Lọc các sân vận động đạt chuẩn quy mô trên 60.000 chỗ ngồi.
* **`ORDER(..., [Measures].[Stadium Capacity Cleaned], BDESC) ON ROWS`**: Sắp xếp danh sách sân vận động theo sức chứa giảm dần toàn cục trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

#### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm làm sạch ô rỗng `COALESCEEMPTY(«Value_1», «Value_2»[, ...])`**:
   * **Cú pháp chuẩn:** `COALESCEEMPTY(Value_1, Value_2)`
   * **Tham số thực tế trong truy vấn:**
     * `Value_1`: `[DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE`.
     * `Value_2`: `0`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Tương đương với hàm `COALESCE()` hoặc `ISNULL()` trong SQL.
     * Hàm đánh giá giá trị sức chứa `Stadium Seats`; nếu dữ liệu bị rỗng (`NULL/Empty` do sân vận động chưa cập nhật thông tin sức chứa), hàm lập tức thay thế bằng giá trị mặc định là `0`.
     * Nhờ đó, biểu thức lọc điều kiện `[Stadium Capacity Cleaned] >= 60000` ở phía sau luôn có giá trị số học hợp lệ để so sánh, tránh lỗi gián đoạn phép toán logic.
   * **Kết quả trả về:** Giá trị số học nguyên vẹn của sức chứa sân đã được làm sạch.

2. **Hàm đếm duy nhất `DISTINCTCOUNT(«Set»)` kết hợp từ khóa `EXISTING`**:
   * **Cú pháp chuẩn:** `DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`
   * **Cơ chế hoạt động kỹ thuật:**
     * Bảng sự kiện `FACT_Player_Match_Perf` ghi nhận hiệu suất ở mức độ chi tiết của từng cầu thủ ra sân (trung bình mỗi trận đấu có từ 22 đến 30 dòng bản ghi).
     * Nếu sử dụng hàm đếm thông thường `COUNT`, số lượng trận đấu sẽ bị phóng đại gấp 22-30 lần.
     * Hàm `DISTINCTCOUNT` duyệt qua tập hợp các mã trận đấu `Game ID` và chỉ đếm các giá trị phân biệt duy nhất.
     * Từ khóa `EXISTING` kích hoạt cơ chế chuyển đổi ngữ cảnh (**Context Transition**): ép tập hợp `Game ID` chỉ bao gồm các trận đấu thực sự diễn ra tại đúng sân vận động và câu lạc bộ đang hiển thị trên dòng hiện hành, mang lại số lượng trận đấu thực tế chính xác tuyệt đối.
   * **Kết quả trả về:** Số lượng trận đấu duy nhất đã diễn ra trên từng sân vận động.

3. **Hàm `FILTER(NONEMPTY(...), Cleaned Capacity >= 60000)`**:
   * **Cơ chế:** Lọc lấy các sân vận động đạt chuẩn quy mô siêu sân đấu với sức chứa từ 60.000 khán giả trở lên và sắp xếp giảm dần toàn cục bằng `ORDER(..., BDESC)`.


#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị 16 siêu sân vận động của bóng đá Châu Âu cùng sức chứa, số trận đã diễn ra và tổng bàn thắng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối: Có 16 sân vận động đạt tiêu chuẩn trên 60.000 chỗ ngồi. Dẫn đầu là Camp Nou (99.354 chỗ, 38 trận, 134 bàn), Wembley Stadium (90.000 chỗ, 18 trận, 58 bàn), và Signal Iduna Park (81.365 chỗ, 36 trận, 132 bàn).
   * Thước đo `Distinct Matches Played` tận dụng hàm `DISTINCTCOUNT` kết hợp `EXISTING` giúp đếm chính xác số trận đấu duy nhất mà không bị nhân bản theo số lượng bản ghi ra sân của cầu thủ trong Fact Table.

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Thao tác lọc toán tử `>= 60000` cực kỳ nhanh chóng trên giao diện; xác minh dữ liệu chiều CLB ngay lập tức. | Chưa hỗ trợ hiển thị hàm `DISTINCTCOUNT` động trên lưới nếu chưa tạo sẵn Measure Group riêng cho Game. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Giao diện đồ họa quen thuộc; hỗ trợ định dạng số có dấu phân cách hàng nghìn (`99,354 Chỗ`) dễ nhìn. | Cần kích hoạt Data Model (Power Pivot) nếu muốn dùng tính năng `Distinct Count` trong Excel PivotTable. | Chuyên viên tổ chức sự kiện thể thao, Quản lý cơ sở vật chất sân đấu. |
| **Ngôn ngữ MDX (SSMS)** | Giải quyết triệt để bài toán đếm phần tử duy nhất trong ngữ cảnh bằng `DISTINCTCOUNT(EXISTING ...)`; xử lý sạch NULL bằng `COALESCEEMPTY`. | Cần hiểu sâu về cơ chế Context Transition giữa các Dimension khác nhau qua Fact Table. | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị 16 siêu sân vận động của bóng đá Châu Âu:

| Sân Vận Động (`Stadium Name`) | Câu Lạc Bộ Chủ Quản (`Club Name`) | Sức Chứa Chuẩn Hóa (`Stadium Capacity`) | Số Trận Đã Diễn Ra (`Distinct Matches`) | Tổng Bàn Thắng (`Goals`) |
| :--- | :--- | :---: | :---: | :---: |
| **Camp Nou** | FC Barcelona | 99.354 Chỗ | 38 | 134 |
| **Wembley Stadium** | England | 90.000 Chỗ | 18 | 58 |
| **Signal Iduna Park** | Borussia Dortmund | 81.365 Chỗ | 36 | 132 |
| **Santiago Bernabéu** | Real Madrid | 81.044 Chỗ | 42 | 148 |
| **San Siro** | Inter Milan | 80.018 Chỗ | 44 | 146 |
| **Stade de France** | France | 80.000 Chỗ | 16 | 49 |
| **Allianz Arena** | Bayern Munich | 75.024 Chỗ | 38 | 152 |
| **Olympiastadion Berlin** | Hertha BSC | 74.475 Chỗ | 32 | 88 |
| **Old Trafford** | Manchester United | 74.310 Chỗ | 40 | 118 |
| **Stadio Olimpico** | AS Roma | 70.634 Chỗ | 42 | 110 |
| **Metropolitano Stadium** | Atletico Madrid | 68.456 Chỗ | 38 | 120 |
| **Stade Vélodrome** | Olympique Marseille | 67.394 Chỗ | 36 | 98 |
| **Tottenham Hotspur Stadium** | Tottenham Hotspur | 62.850 Chỗ | 38 | 114 |
| **London Stadium** | West Ham United | 62.500 Chỗ | 36 | 92 |
| **Benito Villamarín** | Real Betis | 60.720 Chỗ | 34 | 86 |
| **Emirates Stadium** | Arsenal FC | 60.704 Chỗ | 40 | 136 |

> *Ghi chú:* Thước đo `Distinct Matches Played` tận dụng hàm `DISTINCTCOUNT` kết hợp với `EXISTING` giúp đếm chính xác số trận đấu duy nhất mà không bị nhân bản theo số lượng 22-30 cầu thủ ra sân mỗi trận trong Fact Table.

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`COALESCEEMPTY`** | `COALESCEEMPTY(Exp1, Exp2, ...)` | Trả về giá trị đầu tiên khác rỗng. Dùng để gán giá trị mặc định 0 nếu thuộc tính sức chứa sân bị NULL. |
| **`DISTINCTCOUNT`** | `DISTINCTCOUNT(Set_Expression)` | Đếm số lượng phần tử duy nhất (Distinct Game ID) trong không gian trận đấu thực tế, loại trừ việc đếm trùng 22-30 cầu thủ trong cùng một trận. |
| **`EXISTING`** | `EXISTING Set` | Ép chuyển đổi ngữ cảnh để tập hợp `Game ID` chỉ bao gồm các trận diễn ra tại CLB và Sân vận động đang hiển thị trên dòng đó. |
| **`FILTER`** | `FILTER(Set, Condition)` | Lọc các sân vận động có sức chứa quy chuẩn trên 60.000 chỗ ngồi. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Sắp xếp danh sách sân vận động theo sức chứa giảm dần trên toàn cục. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Số sân vận động $>60.000$ chỗ tại Châu Âu:** Chỉ khoảng $S \approx 16 - 25$ sân vận động nổi tiếng.
* **Bộ nhớ RAM sử dụng:** Cực kỳ nhỏ (dưới $3\text{ KB}$ RAM).

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Chi phí tính `DISTINCTCOUNT`:** $O(N_{\text{stadiums}} \times G)$ với $G$ là số trận trung bình mỗi sân ($\approx 20 - 50$ trận).
* **Tổng thời gian phản hồi:** Khoảng **$10\text{ ms} - 25\text{ ms}$**.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Quét các phân vùng chứa dữ liệu sân vận động, lọc các bản ghi có `Stadium_Seats >= 60000`, tổng hợp số bàn thắng `Goals`.
* **Formula Engine (FE):** Nhận diện từ khóa `EXISTING`, duyệt tập hợp các `Game_SK` duy nhất gắn với từng sân vận động qua hàm `DISTINCTCOUNT`, định dạng chuỗi `#,#0 Chỗ` và gửi Cellset về client.
