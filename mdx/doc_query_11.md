# 3.10.11 Câu truy vấn 11: Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả

**Nội dung truy vấn:** Thống kê danh sách các Sân vận động quy chuẩn quốc tế có sức chứa trên 60.000 chỗ ngồi (`Stadium_Seats >= 60.000`) cùng Câu lạc bộ chủ quản, tổng số bàn thắng ghi được và **số lượng trận đấu duy nhất** (`Distinct Matches Played`) đã từng tổ chức tại các sân đấu này. Ứng dụng hàm `COALESCEEMPTY` để làm sạch dữ liệu khuyết thiếu sức chứa và hàm `DISTINCTCOUNT` kết hợp `EXISTING` để loại trừ việc đếm trùng 22-30 cầu thủ ra sân trong cùng một trận.

## 3.10.11.1 Sử dụng Cube Browser

### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $
ightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để làm sạch sức chứa và đếm số trận đấu duy nhất:
   * **Thước đo 1 (`Stadium Capacity Cleaned`):**
     * Name: `Stadium Capacity Cleaned` | Parent hierarchy: `Measures`
     * Expression: `COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE, 0)`
     * Format String: `#,##0`
   * **Thước đo 2 (`Distinct Matches Played`):**
     * Name: `Distinct Matches Played` | Parent hierarchy: `Measures`
     * Expression: `DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`
     * Format String: `#,##0`
4. Chọn menu **Build** $
ightarrow$ **Deploy Solution** để nạp thước đo vào Cube.

### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

### Bước 3: Thiết lập Vùng Bộ lọc Sức chứa (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho `Stadium Seats`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Stadium Seats`** | Bấm dropdown chọn **`Greater Than or Equal`** | Nhập số **`60000`** $
ightarrow$ Bấm **OK** (hiển thị `>= 60000`) |

### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Sân vận động & CLB (Rows):**
   * Mở rộng chiều **`DIM Club`** $
ightarrow$ tìm thuộc tính **`Stadium Name`**: Kéo thả vào vùng Rows.
   * Tìm tiếp thuộc tính **`Club Name`** trong `DIM Club`: Kéo thả vào ngay cạnh cột `Stadium Name`.
2. **Kéo 3 Thước đo đã đồng bộ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Stadium Capacity Cleaned`** thả vào cạnh cột `Club Name`.
     * Kéo **`Distinct Matches Played`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào cột cuối cùng.

### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 3 cột thước đo theo từng sân vận động quy mô lớn.

---

## 3.10.11.2 Sử dụng Pivot Excel

### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\rightarrow$ **`Get Data`** $\rightarrow$ **`From Database`** $\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\rightarrow$ Nhấn **Next >**.

### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\rightarrow$ Nhấn **OK**.

### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Stadium Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Stadium Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\rightarrow$ Kéo `Club Name` thả vào ô Rows (nằm dưới `Stadium Name`). |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Stadium Capacity Cleaned`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Stadium Capacity Cleaned` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Distinct Matches Played`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Distinct Matches Played` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\rightarrow$ Kéo `Goals` thả vào ô Values. |

### Bước 4: Thiết lập Bộ lọc Sức chứa >= 60.000 khán giả
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\rightarrow$ chọn tiếp **`Greater Than Or Equal To...`**.
3. Trong hộp thoại: Chọn lọc theo **`Stadium Capacity Cleaned`** $\ge$ **`60000`** $\rightarrow$ Nhấn **OK**.

### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\rightarrow$ **Report Layout** $\rightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp giảm dần theo số trận đấu duy nhất (`Distinct Matches Played`).

---

## 3.10.11.3 Sử dụng ngôn ngữ MDX

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

### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

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


### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Kiểm tra trên thanh công cụ xem ô chọn database đã trỏ chính xác về `DW_Football_SSAS`.
2. Nhấn nút **`! Execute`** trên thanh công cụ (hoặc nhấn phím tắt **`F5`**).
3. Đọc dữ liệu tại khung bên dưới:
   * **Tab `Results`:** Hiển thị 16 siêu sân vận động của bóng đá Châu Âu cùng sức chứa, số trận đã diễn ra và tổng bàn thắng.
   * **Tab `Messages`:** Hiển thị thông báo `Execution completed successfully.` kèm thời gian thực thi chi tiết.

---

---

## 3.10.11.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
