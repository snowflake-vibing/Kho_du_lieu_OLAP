# 3.10 Thực hiện các câu truy vấn sử dụng SSAS, Pivot table, ngôn ngữ MDX

## 3.10.1 Câu truy vấn 1

**Nội dung truy vấn:** Xác định danh sách 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh (Premier League - GB1) trong mùa giải 2023/2024 (Season = '2023'). Phân tích này giúp ban chuyên môn và nhà quản lý nhận diện các tiền đạo có hiệu suất làm bàn xuất sắc nhất, phục vụ công tác chuyển nhượng và đánh giá phong độ.

### 3.10.1.1 Sử dụng Cube Browser

**Bước 1:** Mở tab **Browser** trong trình thiết kế cube `DW Football Transfermarkt.cube`. Màn hình đang ở trạng thái trống, sẵn sàng để kéo thả các dimension, measure hoặc thiết lập bộ lọc.

**Bước 2:** Kéo các Hierarchy `Competition ID`, `Season` và `Player Name` vào khu vực bộ lọc (filter) ở phía trên.

**Bước 3:** Thiết lập bộ lọc cho `DIM Competition` (Hierarchy `Competition ID`). Đặt Operator là **Equal** và chọn Filter Expression là **{ GB1 }**.

**Bước 4:** Thiết lập bộ lọc cho `DIM Time` (Hierarchy `Season`). Đặt Operator là **Equal** và chọn Filter Expression là **{ 2023 }** (hoặc `2023/2024`).

**Bước 5:** Thiết lập bộ lọc cho `DIM Player` (Hierarchy `Player Name`). Đặt Operator là **Custom** và nhấp vào nút `...` để mở cửa sổ *Expression Builder*.

**Bước 6:** Trong cửa sổ "Expression Builder", nhập một biểu thức MDX tùy chỉnh dùng hàm TOPCOUNT để tìm 10 cầu thủ hàng đầu dựa trên measure `[Measures].[Goals]`:
```mdx
TOPCOUNT([DIM Player].[Player Name].[Player Name].MEMBERS, 10, [Measures].[Goals])
```

**Bước 7:** Kéo thuộc tính `Player Name` (từ `DIM Player`) vào khu vực hàng (Rows) và kéo measure `Goals` (từ `Measures`) vào khu vực dữ liệu (Data area).

**Bước 8:** Nhấp "Click to execute the query" (hoặc nút Execute) để xem kết quả. Bảng kết quả hiển thị 10 cầu thủ ghi nhiều bàn thắng nhất giải Ngoại Hạng Anh mùa giải 2023/2024.

---

### 3.10.1.2 Sử dụng Pivot Excel

**Bước 1:** Từ cửa sổ "PivotTable Fields", kéo các trường `Competition ID` và `Season` vào khu vực **Filters**.

**Bước 2:** Kéo trường `Player Name` vào khu vực **Rows** và kéo measure `Goals` vào khu vực **Values** (hiển thị `Sum of Goals`).

**Bước 3:** Nhấp vào bộ lọc `Competition ID` và chọn **{ GB1 }**.

**Bước 4:** Nhấp vào bộ lọc `Season` và chọn **{ 2023 }** (mùa bóng 2023/2024).

**Bước 5:** PivotTable hiển thị danh sách các cầu thủ thuộc giải Ngoại Hạng Anh mùa giải 2023/2024.

**Bước 6:** Nhấp vào mũi tên lọc trên Row Labels (cột `Player Name`), chọn **Value Filters**, và sau đó chọn **Top 10...**.

**Bước 7:** Trong hộp thoại "Top 10 Filter", thiết lập Show **Top 10 Items by Sum of Goals** và nhấp **OK**.

**Bước 8:** PivotTable hiển thị kết quả cuối cùng: danh sách 10 cầu thủ ghi bàn nhiều nhất giải Ngoại Hạng Anh mùa 2023/2024 được sắp xếp theo số bàn thắng (`Sum of Goals`) giảm dần.

---

### 3.10.1.3 Sử dụng ngôn ngữ MDX

**Bước 1:** Mở trình soạn thảo truy vấn MDX và viết một truy vấn với mục đích "Xác định top 10 cầu thủ ghi nhiều bàn thắng nhất tại giải Ngoại Hạng Anh mùa giải 2023/2024". Truy vấn này chỉ định:
* ● SELECT measure `[Measures].[Goals]` trên **COLUMNS** (Cột).
* ● Sử dụng hàm `TOPCOUNT` để SELECT 10 bản ghi hàng đầu trên **ROWS** (Hàng), dựa trên tập hợp `NONEMPTY` của `[DIM Player].[Player Name]` theo `[Measures].[Goals]`.
* ● Lấy dữ liệu từ khối Cube `[DW Football Transfermarkt]`.
* ● Sử dụng mệnh đề `WHERE` để làm lát cắt ngữ cảnh giới hạn trong giải Ngoại Hạng Anh (`[DIM Competition].[Competition ID].[GB1]`) và mùa giải 2023 (`[DIM Time].[Season].[2023]`).

```mdx
/* ==============================================================================
   Truy vấn MDX 01: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024 (Season = '2023')
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

SELECT
    -- Trục Cột (COLUMNS): Trích xuất thước đo Tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng (ROWS): Xếp hạng và lấy đúng 10 cầu thủ ghi nhiều bàn nhất
    TOPCOUNT(
        NONEMPTY(
            [DIM Player].[Player Name].[Player Name].MEMBERS,
            (
                [Measures].[Goals],
                [DIM Competition].[Competition ID].[GB1],
                [DIM Time].[Season].[2023]
            )
        ),
        10,
        [Measures].[Goals]
    ) ON ROWS

-- Khối Cube nguồn
FROM [DW Football Transfermarkt]

-- Trục lát cắt ngữ cảnh (Slicer Axis): Giới hạn trong giải GB1 và mùa 2023/2024
WHERE (
    [DIM Competition].[Competition ID].[GB1],
    [DIM Time].[Season].[2023]
);
```

**Bước 2:** Thực thi (Execute) truy vấn MDX. Xem kết quả trong tab Results. Kết quả là một bảng gồm 10 cầu thủ hàng đầu và số bàn thắng Goals tương ứng, khớp với các tiêu chí đã lọc (Erling Haaland với 27 bàn, Cole Palmer với 22 bàn, Alexander Isak với 21 bàn...).

---

### 3.10.1.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.

| Xếp hạng | Tên Cầu Thủ (`Player Name`) | Tổng Số Bàn Thắng (`Goals`) |
| :---: | :--- | :---: |
| **1** | **Erling Haaland** | **27** |
| **2** | **Cole Palmer** | **22** |
| **3** | **Alexander Isak** | **21** |
| **4** | **Dominic Solanke** | **19** |
| **5** | **Ollie Watkins** | **19** |
| **6** | **Phil Foden** | **19** |
| **7** | **Mohamed Salah** | **18** |
| **8** | **Heung-min Son** | **17** |
| **9** | **Bukayo Saka** | **16** |
| **10** | **Jarrod Bowen** | **16** |
