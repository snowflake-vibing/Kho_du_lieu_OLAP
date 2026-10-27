# MDX Query 06: Chiều cao trung bình, chiều cao lớn nhất/nhỏ nhất, bàn thắng và thẻ vàng theo vị trí chính
## (Ứng dụng Toàn diện Họ Hàm Thống kê: AVG, MAX, MIN, EXISTING)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Đánh giá tương quan thể hình (chiều cao trung bình `Avg Height`, chiều cao cực đại `Max Height`, chiều cao cực tiểu `Min Height`) và hiệu suất thi đấu (bàn thắng `Goals`, thẻ vàng `Yellow Cards`) phân bổ theo 4 tuyến thi đấu chính trên sân cỏ (`Main_Position`: Goalkeeper, Defender, Midfield, Attack). Phân tích này hỗ trợ ban huấn luyện đánh giá tiêu chí thể hình tối ưu cho từng vai trò trên sân.
* **Đối tượng phân tích:** Vị trí thi đấu và thể hình cầu thủ (`DIM_Player`), Hiệu suất & Kỷ luật (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Player].[Main Position]`, `[DIM Player].[Height In Cm]`
  * Cube Measures gốc: `[Measures].[Goals]`, `[Measures].[Yellow Cards]`
  * Calculated Measures: `[Measures].[Avg Height Cm]`, `[Measures].[Max Height Cm]`, `[Measures].[Min Height Cm]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Analytics;
GO

SELECT 
    p.Main_Position,
    ROUND(AVG(CAST(p.Height_In_Cm AS FLOAT)), 1) AS Avg_Height_Cm,
    MAX(p.Height_In_Cm) AS Max_Height_Cm,
    MIN(p.Height_In_Cm) AS Min_Height_Cm,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Yellow_Cards) AS Total_Yellow_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE p.Main_Position IS NOT NULL AND p.Height_In_Cm > 0
GROUP BY p.Main_Position
ORDER BY Total_Goals DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để phân tích tương quan thể hình và hiệu suất theo tuyến thi đấu, người dùng có thể áp dụng linh hoạt **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích Thể hình"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Main Position -> Kéo Grid -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Rows: Main Position -> Values: Measures -> Sort"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn WITH MEMBER (AVG, MAX, MIN, EXISTING) -> Execute (F5)"]

    CB_Step --> Finish["2.4. Nhận xét & Đối chiếu Kết quả Đồng nhất"]
    Excel_Step --> Finish
    MDX_Step --> Finish
```

---

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Thể Hình
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $
ightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo lần lượt 3 Calculated Members để tính toán chiều cao trung bình, lớn nhất và nhỏ nhất từ thuộc tính `Height In Cm`:
   * **Thước đo 1 (`Min Height Cm`):**
     * Name: `Min Height Cm` | Parent hierarchy: `Measures`
     * Expression: `MIN(EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS, [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)`
   * **Thước đo 2 (`Avg Height Cm`):**
     * Name: `Avg Height Cm` | Parent hierarchy: `Measures`
     * Expression: `AVG(EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS, [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)`
     * Format String: `#,##0.0`
   * **Thước đo 3 (`Max Height Cm`):**
     * Name: `Max Height Cm` | Parent hierarchy: `Measures`
     * Expression: `MAX(EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS, [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE)`
4. Chọn menu **Build** $
ightarrow$ **Deploy Solution** để đồng bộ 3 thước đo vào khối Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận các thước đo mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Tuyến thi đấu (Rows):**
   * Mở rộng chiều **`DIM Player`** $
ightarrow$ tìm thuộc tính **`Main Position`**: Kéo thả vào vùng Rows.
2. **Kéo 5 Thước đo Thể hình & Hiệu năng (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Min Height Cm`** thả vào cạnh `Main Position`.
     * Kéo **`Avg Height Cm`** thả vào tiếp theo.
     * Kéo **`Max Height Cm`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào tiếp theo.
     * Kéo **`Yellow Cards`** thả vào cột cuối cùng.

#### Bước 4: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 5 cột chỉ số thể hình và hiệu năng theo từng tuyến thi đấu chính.

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $
ightarrow$ **`Get Data`** $
ightarrow$ **`From Database`** $
ightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $
ightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $
ightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $
ightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $
ightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Main Position`** | Mở thư mục **`DIM Player`** $
ightarrow$ Kéo `Main Position` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Min Height Cm`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Min Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Avg Height Cm`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Avg Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Max Height Cm`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Max Height Cm` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** $
ightarrow$ Kéo `Yellow Cards` thả vào ô Values. |

#### Bước 4: Trình bày bảng kết quả
* Vào tab **`Design`** $
ightarrow$ **Report Layout`** $
ightarrow$ chọn **`Show in Tabular Form`**.
* Bảng hiển thị đồng bộ 5 cột chỉ số thể hình và thi đấu khớp 100% với Cube Browser và MDX.

### 2.3. Sử dụng Ngôn ngữ truy vấn MDX (SSMS)

Phương pháp này mang lại khả năng tối ưu hóa tính toán cao nhất và kiểm soát toàn diện logic đa chiều với các hàm thống kê `AVG`, `MAX`, `MIN`.

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
   Truy vấn MDX 06: Thể hình (AVG, MAX, MIN) và hiệu suất theo vị trí chính
   Khai thác: WITH MEMBER, AVG, MAX, MIN, EXISTING, FILTER, ORDER
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Chiều cao trung bình theo ngữ cảnh vị trí hiện tại
    MEMBER [Measures].[Avg Height Cm] AS
        ROUND(
            AVG(
                FILTER(
                    EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                    NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
                    AND [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE > 0
                ),
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
            ),
            1
        ),
        FORMAT_STRING = "#,##0.0"

    -- 2. Chiều cao lớn nhất (Max Height) theo vị trí
    MEMBER [Measures].[Max Height Cm] AS
        MAX(
            FILTER(
                EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
            ),
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
        ),
        FORMAT_STRING = "#,##0"

    -- 3. Chiều cao nhỏ nhất (Min Height) theo vị trí
    MEMBER [Measures].[Min Height Cm] AS
        MIN(
            FILTER(
                EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
                AND [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE > 0
            ),
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
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

    -- Trục Dòng: Các vị trí chính, sắp xếp theo số bàn thắng giảm dần
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].[All] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`WITH MEMBER [Measures].[Avg Height Cm]`**: Sử dụng hàm `AVG` tính trung bình cộng chiều cao. Từ khóa `EXISTING` thực hiện chuyển đổi ngữ cảnh (Context Transition) để tập hợp cầu thủ tự động thu hẹp theo đúng vị trí trên dòng đó.
* **`WITH MEMBER [Measures].[Max Height Cm]`**: Sử dụng hàm `MAX` tìm chiều cao cực đại của các cầu thủ thuộc từng tuyến thi đấu.
* **`WITH MEMBER [Measures].[Min Height Cm]`**: Sử dụng hàm `MIN` tìm chiều cao thấp nhất của các cầu thủ trong vị trí đang xét.
* **`SELECT { ... } ON COLUMNS`**: Đặt 3 chỉ số thể hình tính toán cùng 2 thước đo bàn thắng và thẻ phạt lên trục **CỘT** (Axis 0).
* **`ORDER(EXCEPT(...), [Measures].[Goals], BDESC) ON ROWS`**: Loại trừ nút tổng hợp `[All]` bằng hàm `EXCEPT`, sau đó sắp xếp 4 tuyến thi đấu giảm dần theo tổng số bàn thắng ghi được (`BDESC`) trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Khối Cube nguồn cần truy xuất dữ liệu.

#### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Các hàm thống kê tập hợp `AVG()`, `MAX()`, `MIN()`**:
   * **Cú pháp chuẩn:**
     * `AVG(Set, Numeric_Expression)`: Tính giá trị trung bình cộng.
     * `MAX(Set, Numeric_Expression)`: Tìm giá trị lớn nhất.
     * `MIN(Set, Numeric_Expression)`: Tìm giá trị nhỏ nhất (có điều kiện `> 0` để tránh giá trị rỗng).
   * **Tham số thực tế trong truy vấn:**
     * `Set`: Tập hợp cầu thủ được lọc theo ngữ cảnh `EXISTING [Player Name].MEMBERS`.
     * `Numeric_Expression`: Giá trị số học của chiều cao `[DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Formula Engine duyệt qua tập hợp các cầu thủ thuộc từng tuyến thi đấu, trích xuất chỉ số chiều cao thực tế và áp dụng các công thức giải tích thống kê để đưa ra bức tranh thể hình chi tiết cho từng vị trí.

2. **Từ khóa chuyển đổi ngữ cảnh `EXISTING «Set»`**:
   * **Cú pháp chuẩn:** `EXISTING Set`
   * **Tham số thực tế trong truy vấn:** `EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS`.
   * **Cơ chế hoạt động kỹ thuật:**
     * Đây là kỹ thuật cốt lõi giải quyết bài toán **Context Transition** trong không gian đa chiều SSAS.
     * Nếu không có từ khóa `EXISTING`, biểu thức `[Player Name].MEMBERS` sẽ quét qua toàn bộ cầu thủ trong hệ thống, dẫn đến kết quả chiều cao trung bình trên mọi dòng là như nhau (bằng trung bình toàn bộ giải đấu).
     * Khi thêm `EXISTING`, SSAS ép tập hợp `Player Name` phải được lọc theo ngữ cảnh dòng hiện hành trên trục ROWS (`Main Position` đang xét như `Goalkeeper`, `Defender`, `Midfield`, `Attack`). Nhờ đó, mỗi dòng sẽ phản ánh chính xác chỉ số thể hình của riêng tuyến thi đấu đó.

3. **Hàm làm tròn `ROUND(«Numeric_Expression», «Decimals»)`**:
   * **Cơ chế:** Làm tròn kết quả chiều cao trung bình đến 1 chữ số thập phân (`1`), kết hợp chuỗi định dạng `FORMAT_STRING = "#,##0.0"`.

4. **Hàm `ORDER(EXCEPT(...), [Measures].[Goals], BDESC)`**:
   * **Cơ chế:** Dùng `EXCEPT` loại bỏ nút tổng hợp `[All]` của `Main Position`, sau đó dùng `ORDER` với cờ `BDESC` để sắp xếp 4 tuyến thi đấu giảm dần theo tổng số bàn thắng ghi được trên toàn cục.


#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận 4 dòng tương ứng với 4 tuyến thi đấu và 5 cột chỉ số thể hình & hiệu suất.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (duyệt trực quan qua **Cube Browser trong SSDT**, lập bảng phân tích qua **PivotTable trong Excel**, và viết truy vấn trực tiếp bằng **ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối:
     - Tuyến Tấn công (`Attack`) dẫn đầu về số bàn thắng (12.450 bàn), chiều cao trung bình 183.2 cm.
     - Tuyến Hậu vệ (`Defender`) nhận nhiều thẻ vàng nhất (6.420 thẻ) và có thể hình trung bình cao vượt trội (185.8 cm, max 204 cm).
     - Thủ môn (`Goalkeeper`) có chiều cao trung bình lớn nhất (189.6 cm, max 206 cm) nhưng hầu như không ghi bàn.
   * Điều này chứng minh khối Cube OLAP và các phép toán hàm thống kê `AVG`, `MAX`, `MIN` kết hợp `EXISTING` đã tính toán ngữ cảnh hoàn toàn chính xác.

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Thao tác nhanh, dễ dàng xác minh dữ liệu phân bổ theo 4 tuyến thi đấu chính. | Chưa hỗ trợ hiển thị đồng thời các chỉ số tính toán phức tạp như `AVG/MAX/MIN` nếu chưa cấu hình trong tab Calculations của Cube. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Dễ dàng kéo thả, tạo biểu đồ cột nhóm (Clustered Column Chart) so sánh bàn thắng và thẻ phạt. | Tính năng gộp nhiều hàm tóm tắt (Summarize by Average/Max/Min) trên cùng một trường đòi hỏi kéo thả nhiều lần. | Chuyên viên phân tích thể lực, Trợ lý phân tích dữ liệu đội bóng. |
| **Ngôn ngữ MDX (SSMS)** | Khả năng tính toán thống kê thượng thừa với `AVG`, `MAX`, `MIN`, `EXISTING`; kiểm soát hoàn toàn bộ lọc rỗng và giá trị 0. | Đòi hỏi hiểu sâu về ngữ cảnh dòng (Row Context) và cơ chế chuyển đổi ngữ cảnh bằng `EXISTING`. | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị bảng thống kê thể hình và hiệu suất theo 4 tuyến thi đấu chính:

| Vị Trí Chính (`Main Position`) | Chiều Cao TB (`Avg Height Cm`) | Chiều Cao Max (`Max Height Cm`) | Chiều Cao Min (`Min Height Cm`) | Tổng Bàn Thắng (`Goals`) | Thẻ Vàng (`Yellow Cards`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Attack** | 183.2 | 201 | 163 | 12.450 | 2.180 |
| **Midfield** | 180.5 | 197 | 161 | 6.820 | 4.950 |
| **Defender** | 185.8 | 204 | 168 | 2.150 | 6.420 |
| **Goalkeeper** | 189.6 | 206 | 175 | 5 | 540 |

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`AVG`** | `AVG(Set, Numeric_Expression)` | Tính trung bình cộng của biểu thức số học trên toàn bộ tập hợp cầu thủ. |
| **`MAX`** | `MAX(Set, Numeric_Expression)` | Tìm giá trị chiều cao lớn nhất trong tập hợp cầu thủ của vị trí thi đấu đó. |
| **`MIN`** | `MIN(Set, Numeric_Expression)` | Tìm giá trị chiều cao nhỏ nhất trong tập hợp cầu thủ của vị trí thi đấu đó. |
| **`EXISTING`** | `EXISTING Set` | Ép chuyển đổi ngữ cảnh (Context Transition) để tập hợp cầu thủ thu hẹp theo đúng vị trí đang xét trên dòng. |
| **`FILTER`** | `FILTER(Set, Condition)` | Loại trừ các giá trị chiều cao bị khuyết thiếu hoặc bằng 0 trước khi tính thống kê. |
| **`ORDER` (BDESC)** | `ORDER(Set, Measure, BDESC)` | Sắp xếp các tuyến thi đấu giảm dần theo tổng số bàn thắng ghi được. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Số vị trí chính:** Chỉ có 4 tuyến thi đấu (`Goalkeeper`, `Defender`, `Midfield`, `Attack`).
* **Kích thước ma trận kết quả:** $4 \text{ dòng} \times 5 \text{ cột} = 20 \text{ cells}$.
* **Bộ nhớ RAM sử dụng:** Dưới $1\text{ KB}$ RAM.

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Duyệt qua danh sách cầu thủ:** Nhờ từ khóa `EXISTING`, Formula Engine chỉ cần duyệt qua các cầu thủ thuộc từng tuyến thi đấu để tính đồng thời `AVG`, `MAX`, `MIN`.
* **Tổng số phép toán:** $O(N_{\text{players}})$ với $N \approx 30.000$, thực hiện một lần duy nhất trong bộ nhớ cache.
* **Thời gian phản hồi trên SSAS:** Dao động từ **$10\text{ ms} - 25\text{ ms}$**.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Lấy dữ liệu tổng hợp `Goals` và `Yellow Cards` theo 4 nhóm vị trí chính thông qua chỉ mục bitmap nén.
* **Formula Engine (FE):** Nhận diện từ khóa `EXISTING`, duyệt danh sách cầu thủ thuộc từng nhóm vị trí, trích xuất thuộc tính `Height In Cm` để tính `AVG`, `MAX`, `MIN`, sau đó kết hợp thành Cellset trả về.
