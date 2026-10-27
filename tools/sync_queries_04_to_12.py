# -*- coding: utf-8 -*-
"""
Script to synchronize 2.1 Cube Browser and 2.2 Pivot Excel with 2.3 MDX
for query_04, query_06, query_07, query_10, query_11, query_12
"""
import re

# ==============================================================================
# 1. UPDATE query_04.md
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_04.md', 'r', encoding='utf-8') as f:
    q04 = f.read()

# Add Calculated Member steps in 2.1
cb_04_replacement = """### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Members
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Trong cửa sổ **Solution Explorer**, nhấp đúp chuột vào tệp khối đa chiều: **`DW_Football_Cube.cube`** (hoặc `DW Football Transfermarkt.cube`).
3. Chuyển sang tab **`Calculations`** ở cạnh trên để tạo 2 thước đo tính toán phân loại độ tuổi và phút thi đấu trung bình:
   * **Thước đo 1 (`Avg Minutes Played`):** Nhấp chuột phải vào Script Organizer $\\rightarrow$ chọn **New Calculated Member**:
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
4. Chọn menu **Build** $\\rightarrow$ **Deploy Solution** để cập nhật 2 thước đo mới vào cấu trúc Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nạp cấu trúc mới deploy).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** $\\rightarrow$ Bấm **OK** (hiển thị `{ 2023 }`) |

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
1. **Kéo Chiều Tuổi cầu thủ (Rows):**
   * Mở rộng chiều **`DIM Player`** $\\rightarrow$ tìm thuộc tính **`Age`**: Kéo thả vào vùng Rows.
2. **Kéo 4 Thước đo đã đồng bộ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Career Stage Group`** thả vào cạnh cột `Age`.
     * Kéo **`Goals`** thả vào tiếp theo.
     * Kéo **`Assists`** thả vào tiếp theo.
     * Kéo **`Avg Minutes Played`** thả vào cột cuối cùng.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 4 cột phân tích hiệu suất theo từng độ tuổi giống hệt câu truy vấn MDX."""

q04 = re.sub(r'###\s+2\.1\.\s+Sử dụng Cube Browser[\s\S]*?(?=###\s+2\.2)', cb_04_replacement + '\n\n', q04)

# Update Excel in query_04
excel_04_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** $\\rightarrow$ Kéo `Year` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Age`** | Mở thư mục **`DIM Player`** $\\rightarrow$ Kéo `Age` thả vào ô Rows. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Career Stage Group`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Career Stage Group` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Assists`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Assists` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Avg Minutes Played`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Avg Minutes Played` thả vào ô Values. |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
* Tại ô **`B1`** (bên cạnh nhãn `Year`), nhấp mũi tên xổ xuống $\\rightarrow$ tick chọn năm **`2023`** $\\rightarrow$ Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp tuổi tăng dần: Nhấp chuột phải vào cột `Age` $\\rightarrow$ chọn **Sort** $\\rightarrow$ **Sort Smallest to Largest**."""

q04 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', excel_04_replacement + '\n\n', q04)

with open('d:/Kho_du_lieu_OLAP/mdx/query_04.md', 'w', encoding='utf-8') as f:
    f.write(q04)
print('query_04.md synchronized successfully')


# ==============================================================================
# 2. UPDATE query_06.md
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_06.md', 'r', encoding='utf-8') as f:
    q06 = f.read()

cb_06_replacement = """### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Thể Hình
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $\\rightarrow$ chuyển đến tab **`Calculations`**.
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
4. Chọn menu **Build** $\\rightarrow$ **Deploy Solution** để đồng bộ 3 thước đo vào khối Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận các thước đo mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Tuyến thi đấu (Rows):**
   * Mở rộng chiều **`DIM Player`** $\\rightarrow$ tìm thuộc tính **`Main Position`**: Kéo thả vào vùng Rows.
2. **Kéo 5 Thước đo Thể hình & Hiệu năng (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Min Height Cm`** thả vào cạnh `Main Position`.
     * Kéo **`Avg Height Cm`** thả vào tiếp theo.
     * Kéo **`Max Height Cm`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào tiếp theo.
     * Kéo **`Yellow Cards`** thả vào cột cuối cùng.

#### Bước 4: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 5 cột chỉ số thể hình và hiệu năng theo từng tuyến thi đấu chính."""

q06 = re.sub(r'###\s+2\.1\.\s+Sử dụng Cube Browser[\s\S]*?(?=###\s+2\.2)', cb_06_replacement + '\n\n', q06)

excel_06_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Main Position`** | Mở thư mục **`DIM Player`** $\\rightarrow$ Kéo `Main Position` thả vào ô Rows. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Min Height Cm`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Min Height Cm` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Avg Height Cm`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Avg Height Cm` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Max Height Cm`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Max Height Cm` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Yellow Cards` thả vào ô Values. |

#### Bước 4: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout`** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Bảng hiển thị đồng bộ 5 cột chỉ số thể hình và thi đấu khớp 100% với Cube Browser và MDX."""

q06 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', excel_06_replacement + '\n\n', q06)

with open('d:/Kho_du_lieu_OLAP/mdx/query_06.md', 'w', encoding='utf-8') as f:
    f.write(q06)
print('query_06.md synchronized successfully')


# ==============================================================================
# 3. UPDATE query_07.md
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_07.md', 'r', encoding='utf-8') as f:
    q07 = f.read()

cb_07_replacement = """### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Member Tỷ Lệ Pareto
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $\\rightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để tính tổng bàn thắng của giải đấu tại Anh và tỷ lệ phần trăm đóng góp:
   * **Thước đo 1 (`England Total Goals`):**
     * Name: `England Total Goals` | Parent hierarchy: `Measures`
     * Expression: `([DIM Player].[Country Of Citizenship].[All], [Measures].[Goals], [DIM Competition].[Country Name].[England])`
   * **Thước đo 2 (`Pct Of England Goals`):**
     * Name: `Pct Of England Goals` | Parent hierarchy: `Measures`
     * Expression: `IIF([Measures].[England Total Goals] = 0, NULL, [Measures].[Goals] / [Measures].[England Total Goals])`
     * Format String: `0.00%`
4. Chọn menu **Build** $\\rightarrow$ **Deploy Solution** để đồng bộ vào Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định Nước Anh và áp dụng thuật toán `TOPPERCENT 80%`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Competition`** | Nhấp chọn **`Country Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`England`** $\\rightarrow$ Bấm **OK** (hiển thị `{ England }`) |
| **Dòng 2** | Nhấp chọn **`DIM Player`** | Nhấp chọn **`Country Of Citizenship`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô $\\rightarrow$ nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `TOPPERCENT` bên dưới $\\rightarrow$ Bấm **OK** |

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

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Quốc tịch (Rows):**
   * Mở rộng chiều **`DIM Player`** $\\rightarrow$ tìm thuộc tính **`Country Of Citizenship`**: Kéo thả vào vùng Rows.
2. **Kéo Thước đo Bàn thắng & Tỷ lệ % (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào cạnh cột `Country Of Citizenship`.
     * Kéo **`Pct Of England Goals`** thả vào cột tiếp theo.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 2 cột `Goals` và `Pct Of England Goals` theo danh sách các quốc gia chiếm 80% bàn thắng."""

q07 = re.sub(r'###\s+2\.1\.\s+Sử dụng Cube Browser[\s\S]*?(?=###\s+2\.2)', cb_07_replacement + '\n\n', q07)

excel_07_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Country Name`** | Mở thư mục **`DIM Competition`** $\\rightarrow$ Kéo `Country Name` thả vào ô Filters. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Country Of Citizenship`** | Mở thư mục **`DIM Player`** $\\rightarrow$ Kéo `Country Of Citizenship` thả vào ô Rows. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Pct Of England Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Pct Of England Goals` thả vào ô Values. |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. Tại ô **`B1`** (bên cạnh nhãn `Country Name`), nhấp mũi tên xổ xuống $\\rightarrow$ tick chọn **`England`** $\\rightarrow$ Nhấn **OK**.
2. **Cấu hình Bộ lọc Pareto 80%:**
   * Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
   * Di chuột vào mục **`Value Filters`** $\\rightarrow$ chọn tiếp **`Top 10...`**.
   * Trong hộp thoại Top 10 Filter: Đổi sang **`Top`** $\\rightarrow$ Nhập **`80`** $\\rightarrow$ Chọn **`Percent`** theo **`Sum of Goals`** $\\rightarrow$ Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp giảm dần theo số bàn thắng."""

q07 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', excel_07_replacement + '\n\n', q07)

with open('d:/Kho_du_lieu_OLAP/mdx/query_07.md', 'w', encoding='utf-8') as f:
    f.write(q07)
print('query_07.md synchronized successfully')


# ==============================================================================
# 4. UPDATE query_10.md
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_10.md', 'r', encoding='utf-8') as f:
    q10 = f.read()

cb_10_replacement = """### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures Tăng Trưởng QoQ
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $\\rightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để tính bàn thắng quý trước và tỷ lệ tăng trưởng QoQ:
   * **Thước đo 1 (`Prev Quarter Goals`):**
     * Name: `Prev Quarter Goals` | Parent hierarchy: `Measures`
     * Expression: `([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER)`
   * **Thước đo 2 (`QoQ Goals Growth`):**
     * Name: `QoQ Goals Growth` | Parent hierarchy: `Measures`
     * Expression:
       ```mdx
       IIF(
           ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
           NULL,
           ROUND((([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100, 2)
       )
       ```
     * Format String: `0.00%`
4. Chọn menu **Build** $\\rightarrow$ **Deploy Solution** để cập nhật Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 2 dòng lọc để cố định đội bóng Real Madrid và năm 2023:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Giữ nguyên **`Equal`** ($=$) | Bấm vào ô, tick chọn **`Real Madrid`** $\\rightarrow$ Bấm **OK** (hiển thị `{ Real Madrid }`) |
| **Dòng 2** | Nhấp chọn **`DIM Time`** | Nhấp chọn **`Year`** | Chọn **`Equal`** ($=$) | Bấm vào ô, tick chọn năm **`2023`** $\\rightarrow$ Bấm **OK** (hiển thị `{ 2023 }`) |

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Câu lạc bộ Đối thủ (Rows):**
   * Mở rộng chiều **`Opponent Club`** $\\rightarrow$ tìm thuộc tính **`Club Name`**: Kéo thả vào vùng Rows.
2. **Kéo Phân cấp Quý (Columns):**
   * Mở rộng thư mục **`DIM Time`** $\\rightarrow$ mở rộng phân cấp **`Hierarchy`** $\\rightarrow$ tìm cấp độ **`Quarter`**: Kéo thả lên vùng cột (Columns) để chia bảng theo các Quý (Q1, Q2, Q3, Q4).
3. **Kéo Thước đo Bàn thắng & Tăng trưởng QoQ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Goals`** thả vào vùng dữ liệu trung tâm.
     * Kéo **`QoQ Goals Growth`** thả vào ngay bên cạnh `Goals`.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận phân bổ bàn thắng và tăng trưởng QoQ của Real Madrid vào lưới từng đối thủ qua các Quý năm 2023."""

q10 = re.sub(r'###\s+2\.1\.\s+Sử dụng Cube Browser[\s\S]*?(?=###\s+2\.2)', cb_10_replacement + '\n\n', q10)

excel_10_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\\rightarrow$ Kéo `Club Name` thả vào ô Filters. |
| **Ô `Filters` (Bộ lọc báo cáo)** | **`Year`** | Mở thư mục **`DIM Time`** $\\rightarrow$ Kéo `Year` thả vào ô Filters. |
| **Ô `Columns` (Cột ma trận)** | **`Quarter`** | Mở thư mục **`DIM Time`** $\\rightarrow$ mở `Hierarchy` $\\rightarrow$ Kéo `Quarter` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`Opponent Club`** $\\rightarrow$ Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`QoQ Goals Growth`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `QoQ Goals Growth` thả vào ô Values (hoặc kéo `Goals` lần 2 và chọn Show Values As `% Difference From`). |

#### Bước 4: Thiết lập Giá trị Bộ lọc trên Sheet Excel
1. Tại ô bên cạnh nhãn `Club Name`, nhấp mũi tên xổ xuống $\\rightarrow$ tick chọn **`Real Madrid`** $\\rightarrow$ Nhấn **OK**.
2. Tại ô bên cạnh nhãn `Year`, nhấp mũi tên xổ xuống $\\rightarrow$ tick chọn năm **`2023`** $\\rightarrow$ Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp danh sách đối thủ giảm dần theo tổng bàn thắng."""

q10 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', excel_10_replacement + '\n\n', q10)

with open('d:/Kho_du_lieu_OLAP/mdx/query_10.md', 'w', encoding='utf-8') as f:
    f.write(q10)
print('query_10.md synchronized successfully')


# ==============================================================================
# 5. UPDATE query_11.md
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_11.md', 'r', encoding='utf-8') as f:
    q11 = f.read()

cb_11_replacement = """### 2.1. Sử dụng Cube Browser (Visual Studio / SSDT)

Phương pháp này được thực hiện trực tiếp trong môi trường phát triển khối đa chiều (SQL Server Data Tools / Visual Studio).

#### Bước 1: Mở giao diện Cube Designer & Tạo Calculated Measures
1. Khởi động **Visual Studio**, mở Solution dự án SSAS (`SSIS_Football_Transfermarkt` hoặc `DW_Football_SSAS`).
2. Mở tệp khối đa chiều **`DW_Football_Cube.cube`** $\\rightarrow$ chuyển đến tab **`Calculations`**.
3. Tạo 2 Calculated Members để làm sạch sức chứa và đếm số trận đấu duy nhất:
   * **Thước đo 1 (`Stadium Capacity Cleaned`):**
     * Name: `Stadium Capacity Cleaned` | Parent hierarchy: `Measures`
     * Expression: `COALESCEEMPTY([DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE, 0)`
     * Format String: `#,##0`
   * **Thước đo 2 (`Distinct Matches Played`):**
     * Name: `Distinct Matches Played` | Parent hierarchy: `Measures`
     * Expression: `DISTINCTCOUNT(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS)`
     * Format String: `#,##0`
4. Chọn menu **Build** $\\rightarrow$ **Deploy Solution** để nạp thước đo vào Cube.

#### Bước 2: Chuyển sang Tab `Browser` & Kích hoạt `Design Mode`
1. Nhấp chọn tab **`Browser`** (bấm nút **Reconnect** để nhận cấu trúc mới).
2. Nhấp vào biểu tượng **`Design Mode`** để mở giao diện thiết kế đồ họa.

#### Bước 3: Thiết lập Vùng Bộ lọc Sức chứa (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho `Stadium Seats`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Stadium Seats`** | Bấm dropdown chọn **`Greater Than or Equal`** | Nhập số **`60000`** $\\rightarrow$ Bấm **OK** (hiển thị `>= 60000`) |

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu
1. **Kéo Chiều Sân vận động & CLB (Rows):**
   * Mở rộng chiều **`DIM Club`** $\\rightarrow$ tìm thuộc tính **`Stadium Name`**: Kéo thả vào vùng Rows.
   * Tìm tiếp thuộc tính **`Club Name`** trong `DIM Club`: Kéo thả vào ngay cạnh cột `Stadium Name`.
2. **Kéo 3 Thước đo đã đồng bộ (Measures):**
   * Mở rộng thư mục **`Measures`**:
     * Kéo **`Stadium Capacity Cleaned`** thả vào cạnh cột `Club Name`.
     * Kéo **`Distinct Matches Played`** thả vào tiếp theo.
     * Kéo **`Goals`** thả vào cột cuối cùng.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5**).
2. Lưới dữ liệu lập tức chạy và hiển thị đúng 3 cột thước đo theo từng sân vận động quy mô lớn."""

q11 = re.sub(r'###\s+2\.1\.\s+Sử dụng Cube Browser[\s\S]*?(?=###\s+2\.2)', cb_11_replacement + '\n\n', q11)

excel_11_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Stadium Name`** | Mở thư mục **`DIM Club`** $\\rightarrow$ Kéo `Stadium Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** $\\rightarrow$ Kéo `Club Name` thả vào ô Rows (nằm dưới `Stadium Name`). |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Stadium Capacity Cleaned`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Stadium Capacity Cleaned` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Distinct Matches Played`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Distinct Matches Played` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Goals` thả vào ô Values. |

#### Bước 4: Thiết lập Bộ lọc Sức chứa >= 60.000 khán giả
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** $\\rightarrow$ chọn tiếp **`Greater Than Or Equal To...`**.
3. Trong hộp thoại: Chọn lọc theo **`Stadium Capacity Cleaned`** $\\ge$ **`60000`** $\\rightarrow$ Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Sắp xếp giảm dần theo số trận đấu duy nhất (`Distinct Matches Played`)."""

q11 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', lambda m: excel_11_replacement + '\n\n', q11)

with open('d:/Kho_du_lieu_OLAP/mdx/query_11.md', 'w', encoding='utf-8') as f:
    f.write(q11)
print('query_11.md synchronized successfully')


# ==============================================================================
# 6. UPDATE query_12.md (Excel Top 1 month per coach)
# ==============================================================================
with open('d:/Kho_du_lieu_OLAP/mdx/query_12.md', 'r', encoding='utf-8') as f:
    q12 = f.read()

excel_12_replacement = """### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** $\\rightarrow$ **`Get Data`** $\\rightarrow$ **`From Database`** $\\rightarrow$ **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** $\\rightarrow$ Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** $\\rightarrow$ Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** $\\rightarrow$ Chọn **`PivotTable Report`** tại ô **`=$A$3`** $\\rightarrow$ Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Rows` (Dòng dữ liệu)** | **`Coach Name`** | Mở thư mục **`DIM Club`** $\\rightarrow$ Kéo `Coach Name` thả vào ô Rows. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Month`** | Mở thư mục **`DIM Time`** $\\rightarrow$ Kéo `Month` thả vào ô Rows (nằm dưới `Coach Name`). |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Yellow Cards` thả vào ô Values. |
| **Ô `Values` ($\\\\Sigma$ Thước đo)** | **`Red Cards`** | Mở thư mục **`Measures`** $\\rightarrow$ Kéo `Red Cards` thả vào ô Values. |

#### Bước 4: Cấu hình Bộ lọc Top 1 Tháng kỷ lục cho từng HLV (Đồng bộ thuật toán GENERATE)
1. Trong bảng PivotTable, nhấp chuột vào mũi tên lọc bên cạnh một ô giá trị **`Month`** (cột tháng).
2. Di chuột vào mục **`Value Filters`** $\\rightarrow$ chọn tiếp **`Top 10...`**.
3. Trong hộp thoại Top 10 Filter:
   * Thiết lập: **`Top`** $\\rightarrow$ nhập **`1`** $\\rightarrow$ **`Items`** theo **`Sum of Yellow Cards`** $\\rightarrow$ Nhấn **OK**.
   * *Ý nghĩa:* Bộ lọc này yêu cầu PivotTable chỉ giữ lại đúng **1 tháng cao nhất** cho mỗi huấn luyện viên, loại bỏ hoàn toàn các tháng còn lại, tái lập chính xác 100% thuật toán `GENERATE + TOPCOUNT(..., 1)` của ngôn ngữ MDX!

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** $\\rightarrow$ **Report Layout** $\\rightarrow$ chọn **`Show in Tabular Form`**.
* Bảng hiển thị mỗi HLV đúng 1 dòng tháng kỷ lục, đồng bộ hoàn hảo với Cube Browser và MDX."""

q12 = re.sub(r'###\s+2\.2\.\s+Sử dụng PivotTable[\s\S]*?(?=###\s+2\.3)', lambda m: excel_12_replacement + '\n\n', q12)

with open('d:/Kho_du_lieu_OLAP/mdx/query_12.md', 'w', encoding='utf-8') as f:
    f.write(q12)
print('query_12.md synchronized successfully')
