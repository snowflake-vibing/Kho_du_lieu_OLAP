# MDX Query 04: Bàn thắng, kiến tạo & số phút thi đấu trung bình phân theo độ tuổi năm 2023
## (Ứng dụng Thành viên Tính toán WITH MEMBER & Hàm Điều Kiện IIF)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Khảo sát sự phân bố hiệu suất ghi bàn (`Goals`), kiến tạo (`Assists`) và thời lượng thi đấu trung bình mỗi trận (`Avg Minutes Played`) theo từng độ tuổi cầu thủ (`Age`) trong năm 2023. Phân tích này hỗ trợ ban huấn luyện và bộ phận tuyển trạch đánh giá điểm rơi phong độ, độ bền thể lực và chu kỳ phát triển của vận động viên theo độ tuổi thực tế.
* **Đối tượng phân tích:** Cầu thủ (`DIM_Player`), Thời gian (`DIM_Time`), Hiệu suất thi đấu (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Player].[Age]`, `[DIM Time].[Year]`
  * Cube Measures gốc: `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Minutes Played]`, `[Measures].[FACT Player Match Perf Count]`
  * Calculated Measure: `[Measures].[Avg Minutes Played]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Transfermarkt;
GO

SELECT 
    p.Age,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Assists) AS Total_Assists,
    ROUND(CAST(SUM(f.Minutes_Played) AS FLOAT) / COUNT(*), 2) AS Avg_Minutes_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Year = 2023 AND p.Age IS NOT NULL AND p.Age > 0
GROUP BY p.Age
ORDER BY p.Age ASC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để phân tích tương quan giữa độ tuổi và hiệu suất thi đấu, người dùng có thể áp dụng linh hoạt **3 phương pháp**:

```mermaid
flowchart TD
    Start["Khởi động Phân tích theo Độ tuổi"] --> Choice{"Lựa chọn Phương pháp"}

    Choice -->|"Cách 1: Trực quan Thiết kế"| CB["2.1. Cube Browser (Visual Studio / SSDT)"]
    Choice -->|"Cách 2: Báo cáo Doanh nghiệp"| Excel["2.2. Excel PivotTable"]
    Choice -->|"Cách 3: Lập trình Đa chiều"| MDX["2.3. Ngôn ngữ MDX (SSMS)"]

    CB --> CB_Step["Mở .cube -> Tab Browser (Design Mode) -> Filter Year = 2023 -> Kéo Age vào Rows, Measures vào Data -> Execute (F5)"]
    Excel --> Excel_Step["Data -> Get Data from SSAS -> PivotTable Fields -> Filter Year = 2023 -> Rows: Age -> Values: Goals, Assists, Avg Minutes"]
    MDX --> MDX_Step["SSMS Connect AS -> New MDX Query -> Soạn WITH MEMBER/IIF, ORDER (BASC) -> Execute (F5)"]

    CB_Step --> Finish["2.4. Nhận xét & Đối chiếu Kết quả Đồng nhất"]
    Excel_Step --> Finish
    MDX_Step --> Finish
```

---

### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Member Số Phút TB
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSAS_Football_Transfermarkt`).
2. Trong cửa sổ **Solution Explorer**, nhấp đúp chuột vào tệp khối đa chiều: **`DW Football Transfermarkt.cube`**.
3. Chuyển sang tab **`Calculations`** ở cạnh trên để tạo thước đo tính toán số phút thi đấu trung bình:
   * Nhấp chuột phải vào Script Organizer → chọn **New Calculated Member**:
     * Name: `[Avg Minutes Played]`
     * Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       IIF(
           IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
           NULL,
           ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
       )
       ```
     * Format String: `#,##0.00`
4. Chọn menu **Build** → **Deploy Solution** để cập nhật thước đo mới vào cấu trúc Cube trên Analysis Services server.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nạp cấu trúc mới deploy).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** → Bấm **OK** (hiển thị `{ 2023 }`) |

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Tuổi cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** → tìm thuộc tính **`Age`**: Kéo thả vào vùng Rows.
2. **Kéo 3 Thước đo (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào vùng dữ liệu.
     * Kéo **`Assists`** thả vào ngay bên cạnh `Goals`.
     * Kéo **`Avg Minutes Played`** thả vào cột tiếp theo.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 3 cột phân tích hiệu suất theo từng độ tuổi, khớp 100% với câu truy vấn MDX.

---

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`SSAS_Football_Transfermarkt`** → Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** → Chọn **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** → Kéo `Year` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Age`** | Mở thư mục **`DIM Player`** → Kéo `Age` thả vào ô Rows. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Assists`** | Mở thư mục **`Measures`** → Kéo `Assists` thả vào ô Values. |
| **Ô `Values` ($\Sigma$ Thước đo)** | **`Avg Minutes Played`** | Mở thư mục **`Measures`** → Kéo `Avg Minutes Played` thả vào ô Values. |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Year`), nhấp mũi tên xổ xuống → tick chọn năm **`2023`** → Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Sắp xếp tuổi tăng dần: Nhấp chuột phải vào cột `Age` → chọn **Sort** → **Sort Smallest to Largest**.

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
   * Mở rộng thư mục **`Databases`** → mở rộng database **`SSAS_Football_Transfermarkt`** → mở rộng thư mục **`Cubes`**.
   * Nhấp chuột phải vào khối Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → chọn **`MDX`**.
4. Cửa sổ soạn thảo truy vấn MDX xuất hiện.

#### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 04: Hiệu suất bàn thắng, kiến tạo & phút thi đấu theo độ tuổi
   Khai thác: WITH MEMBER, IIF, ROUND, FILTER, ORDER (BASC)
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

SELECT
    -- Trục Cột: Các chỉ số hiệu suất thi đấu (Bàn thắng, Kiến tạo, Phút trung bình)
    {
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    -- Trục Dòng: Các độ tuổi hợp lệ, sắp xếp tăng dần từ 17 đến 45
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
* **`SELECT { ... } ON COLUMNS`**: Đưa 3 chỉ số đo lường hiệu suất (`Goals`, `Assists`, `Avg Minutes Played`) lên trục **CỘT** (Axis 0).
* **`ORDER(FILTER(...), BASC) ON ROWS`**: Lọc bỏ các dòng có độ tuổi bằng 0 hoặc bị khuyết thiếu (`ISEMPTY`), sau đó sắp xếp độ tuổi tăng dần (`BASC` - Break Hierarchy Ascending) trên trục **HÀNG** (Axis 1).
* **`FROM [DW Football Transfermarkt]`**: Nguồn khối Cube đa chiều phân tích.
* **`WHERE ([DIM Time].[Year].[2023])`**: Trục lát cắt dữ liệu (Slicer Axis), giới hạn phạm vi tính toán trong năm dương lịch 2023.

#### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Mệnh đề định nghĩa thành viên tính toán `WITH MEMBER`**:
   * **Cú pháp chuẩn:** `WITH MEMBER «Member_Name» AS «Expression»[, FORMAT_STRING = '...']`
   * **Cơ chế:** Cho phép tạo ra các thước đo ảo chỉ tồn tại tạm thời trong phiên thực thi của câu truy vấn MDX mà không làm thay đổi cấu trúc Cube vật lý.

2. **Hàm điều kiện `IIF(«Logical_Expression», «True_Part», «False_Part»)` kết hợp `IsEmpty()`**:
   * **Cú pháp chuẩn:** `IIF(Condition, Value_If_True, Value_If_False)`
   * **Tham số thực tế trong truy vấn:**
     * `Condition`: `IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0`
     * `Value_If_True`: `NULL` (nếu mẫu số rỗng hoặc bằng 0).
     * `Value_If_False`: Phép chia tính trung bình `ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)`.
   * **Cơ chế:** Ngăn ngừa hoàn toàn lỗi chia cho 0 (`#DIV/0!`), bảo đảm an toàn dữ liệu tính toán.

3. **Thuộc tính `.CURRENTMEMBER` và `.MEMBERVALUE`**:
   * **Cú pháp chuẩn:** `«Dimension/Hierarchy».CURRENTMEMBER.MEMBERVALUE`
   * **Cơ chế:** Trích xuất giá trị số học nguyên bản của thuộc tính tuổi (ví dụ: `18`, `25`, `35`) phục vụ phép so sánh điều kiện lọc `> 0` và sắp xếp thứ tự số học.

4. **Hàm `ORDER(FILTER(...), BASC)`**:
   * **Cú pháp chuẩn:** `ORDER(Set, Criteria, BASC)`
   * **Cơ chế:** Lọc các độ tuổi hợp lệ có dữ liệu (`NOT ISEMPTY AND Age > 0`) và sắp xếp tăng dần toàn cục (`BASC`) từ 17 tuổi đến 45 tuổi.

#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `SSAS_Football_Transfermarkt`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị ma trận phân bổ hiệu suất 3 chỉ số theo từng độ tuổi.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

### 2.4. Nhận xét & Đối chiếu kết quả (Comparison & Validation)

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 cách tiếp cận (**Cube Browser trong SSDT**, **PivotTable trong Excel**, và **Ngôn ngữ MDX trong SSMS**) đều trả về cùng một kết quả duy nhất và chuẩn xác tuyệt đối trên 29 nhóm tuổi:
     * Độ tuổi từ 25 đến 29 tuổi đóng góp nhiều bàn thắng và kiến tạo nhất (đỉnh cao là 29 tuổi với 1.008 bàn thắng và 776 kiến tạo).
     * Thời lượng thi đấu trung bình mỗi trận tăng dần từ 40.31 phút (ở tuổi 19), đạt đỉnh 67-70 phút ở giai đoạn 28-33 tuổi, và duy trì mức ổn định ở các cầu thủ kỳ cựu.
   * Số liệu phản ánh chính xác chu kỳ thể lực và phong độ thực tế của cầu thủ bóng đá chuyên nghiệp.

2. **So sánh Ưu - Nhược điểm của từng phương thức:**

| Phương thức | Ưu điểm nổi bật | Hạn chế | Đối tượng người dùng phù hợp |
| :--- | :--- | :--- | :--- |
| **Cube Browser (SSDT)** | Kiểm tra nhanh các thước đo cơ bản theo từng độ tuổi; dễ dàng kéo thả xác minh tính liên tục của dữ liệu. | Giao diện cơ bản chỉ hiển thị danh sách phẳng, không tùy biến biểu đồ trực quan. | Kỹ sư BI, Nhà phát triển khối Cube SSAS. |
| **Excel PivotTable** | Hỗ trợ vẽ biểu đồ đường (Line Chart) thể hiện đường cong phát triển phong độ theo tuổi cực kỳ trực quan. | Cần làm mới (Refresh) thủ công khi dữ liệu Cube thay đổi. | Chuyên viên phân tích thể thao, Bộ phận tuyển trạch và chuyển nhượng. |
| **Ngôn ngữ MDX (SSMS)** | Khả năng tính toán mạnh mẽ nhất với `WITH MEMBER`, `IIF`, `ROUND`; kiểm soát trọn vẹn thứ tự sắp xếp `ORDER BASC`. | Cú pháp MDX đòi hỏi người viết nắm vững cách dùng `MEMBERVALUE` cho các thuộc tính số học. | Kỹ sư Dữ liệu (Data Engineer), Quản trị viên CSDL (DBA). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị đầy đủ 29 dòng dữ liệu thực tế từ khối Cube OLAP:

| STT | Độ Tuổi (`Age`) | Tổng Bàn Thắng (`Goals`) | Tổng Kiến Tạo (`Assists`) | Số Phút TB/Trận (`Avg Minutes`) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | **17** | - | - | - |
| **2** | **18** | 0 | 0 | 6.00 |
| **3** | **19** | 1 | 3 | 40.31 |
| **4** | **20** | 24 | 16 | 47.78 |
| **5** | **21** | 46 | 54 | 42.69 |
| **6** | **22** | 127 | 115 | 44.89 |
| **7** | **23** | 298 | 266 | 51.30 |
| **8** | **24** | 447 | 391 | 57.07 |
| **9** | **25** | 672 | 536 | 59.74 |
| **10** | **26** | 865 | 694 | 62.56 |
| **11** | **27** | 838 | 641 | 63.33 |
| **12** | **28** | 948 | 718 | 66.09 |
| **13** | **29** | 1,008 | 776 | 67.72 |
| **14** | **30** | 816 | 582 | 65.17 |
| **15** | **31** | 632 | 471 | 65.28 |
| **16** | **32** | 720 | 561 | 69.87 |
| **17** | **33** | 660 | 484 | 69.45 |
| **18** | **34** | 543 | 403 | 68.92 |
| **19** | **35** | 507 | 316 | 66.56 |
| **20** | **36** | 222 | 198 | 68.58 |
| **21** | **37** | 199 | 139 | 66.51 |
| **22** | **38** | 165 | 126 | 70.28 |
| **23** | **39** | 130 | 80 | 68.85 |
| **24** | **40** | 72 | 41 | 65.41 |
| **25** | **41** | 15 | 13 | 71.21 |
| **26** | **42** | 3 | 2 | 73.11 |
| **27** | **43** | 6 | 5 | 80.28 |
| **28** | **44** | 0 | 0 | 90.00 |
| **29** | **45** | 1 | 1 | 56.80 |

---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm | Cú pháp chuẩn | Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`WITH MEMBER`** | `WITH MEMBER [DW Football Transfermarkt] AS 'Exp' [, FORMAT_STRING = '...']` | Định nghĩa thước đo tính toán số phút trung bình trong phạm vi phiên truy vấn. |
| **`IIF`** | `IIF(Logical_Exp, True_Part, False_Part)` | Xử lý an toàn mẫu số của phép tính trung bình, trả về `NULL` khi số lần ra sân bằng 0 hoặc rỗng để chống lỗi chia cho 0. |
| **`ROUND`** | `ROUND(Numeric_Exp, Decimals)` | Làm tròn số phút thi đấu trung bình mỗi trận đến 2 chữ số thập phân. |
| **`MEMBERVALUE`** | `Member.MEMBERVALUE` | Trích xuất giá trị số học nguyên bản của thuộc tính `Age` thay vì giá trị chuỗi văn bản (`NAME`), phục vụ phép so sánh số học `> 0` và sắp xếp `ORDER`. |
| **`ORDER` (BASC)** | `ORDER(Set, Criteria, BASC)` | Sắp xếp tập hợp các độ tuổi theo thứ tự tăng dần toàn cục từ 17 đến 45 tuổi. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

### 1. Phân tích Độ phức tạp Không gian (Space Complexity)
* **Số lượng độ tuổi thực tế:** Cầu thủ chuyên nghiệp trong năm 2023 có đúng 29 nhóm tuổi (từ 17 đến 45 tuổi).
* **Kích thước ma trận kết quả:** $29 \text{ dòng tuổi} \times 3 \text{ cột chỉ số} = 87 \text{ cells}$.
* **Bộ nhớ RAM sử dụng:** Cực kỳ nhỏ (dưới $2\text{ KB}$ RAM).

### 2. Phân tích Độ phức tạp Thời gian (Time Complexity)
* **Quét dữ liệu theo lát cắt năm 2023:** Storage Engine (SE) quét qua phân vùng năm 2023, gom nhóm dữ liệu theo từng tuổi với chi phí $O(N_{2023})$ với $N_{2023} \approx 65.000$ bản ghi ra sân.
* **Tính toán Calculated Members:** Formula Engine (FE) thực thi phép tính `Avg Minutes` trực tiếp trên bộ nhớ đệm cho 29 nhóm tuổi trong vòng chưa đầy $0.1\text{ ms}$.
* **Tổng thời gian phản hồi:** Khoảng **$5\text{ ms} - 15\text{ ms}$**.

### 3. Cơ chế hoạt động của Động cơ SSAS (Storage Engine vs Formula Engine)
* **Storage Engine (SE):** Truy xuất các phân vùng khối dữ liệu của năm 2023, thực hiện tổng hợp các giá trị `Goals`, `Assists`, `Minutes Played` và đếm số dòng `FACT Count` cho từng giá trị `Age`.
* **Formula Engine (FE):** Nhận kết quả tổng hợp, áp dụng phép chia `Avg Minutes` với hàm phòng vệ `IIF`, sau đó đóng gói cellset ma trận gửi về client.
