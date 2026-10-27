# MDX Query 09: So sánh hiệu năng & thẻ phạt của các CLB giữa Cuối tuần & Ngày thường
## (Ứng dụng Giao Tập Hợp INTERSECT & Tích Đề-các CROSSJOIN)

---

## 1. Nội dung truy vấn & Bối cảnh nghiệp vụ

* **Nội dung truy vấn:** Xác định danh sách các Câu lạc bộ bóng đá toàn diện hàng đầu xuất hiện đồng thời trong cả hai nhóm: **Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (`Is_Weekend = 1`)** và **Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (`Is_Weekend = 0`)**. Ứng dụng phép toán giao tập hợp (`INTERSECT`) giúp lọc ra những đội bóng có bản lĩnh thi đấu đồng đều đỉnh cao (Elite Clubs), duy trì sức tấn công và kiểm soát kỷ luật bất kể thời điểm thi đấu (các trận giải VĐQG cuối tuần hay các trận cúp châu Âu giữa tuần).
* **Đối tượng phân tích:** Câu lạc bộ (`DIM_Club`), Thời gian thi đấu (`DIM_Time`), Hiệu suất & Kỷ luật (`FACT_Player_Match_Perf`).
* **Các thuộc tính & Thước đo tham gia:**
  * Dimension Attributes: `[DIM Club].[Club Name]`, `[DIM Time].[Is Weekend]`
  * Cube Measures: `[Measures].[Goals]`, `[Measures].[Yellow Cards]`

### Đối chiếu câu lệnh T-SQL gốc (Relational Database)
```sql
USE DW_Football_Transfermarkt;
GO

WITH WeekendTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekend_Goals,
        SUM(f.Yellow_Cards) AS Weekend_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 1
    GROUP BY c.Club_Name
    ORDER BY Weekend_Goals DESC, c.Club_Name DESC
),
WeekdayTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekday_Goals,
        SUM(f.Yellow_Cards) AS Weekday_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 0
    GROUP BY c.Club_Name
    ORDER BY Weekday_Goals DESC, c.Club_Name DESC
)
SELECT 
    w.Club_Name,
    w.Weekend_Goals,
    w.Weekend_Yellow_Cards,
    d.Weekday_Goals,
    d.Weekday_Yellow_Cards,
    (w.Weekend_Goals + d.Weekday_Goals) AS Total_Goals
FROM WeekendTop w
INNER JOIN WeekdayTop d ON w.Club_Name = d.Club_Name
ORDER BY Total_Goals DESC;
```

---

## 2. Hướng dẫn chi tiết 3 cách thực hiện (3 Execution Methods)

Để giải quyết bài toán giao tập hợp đa chiều này, người dùng có thể áp dụng linh hoạt **3 phương pháp** với quy trình thao tác chuẩn xác như sau:

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

#### Bước 3: Thiết lập Vùng Bộ lọc Giao tập hợp (Filter / Slicer Pane ở phía trên)
Tại bảng lưới thiết lập bộ lọc phía trên, ta tạo 1 dòng lọc cho `Club Name` để áp dụng thuật toán `INTERSECT`:

| Dòng lọc | Cột Dimension (Chọn gì) | Cột Hierarchy (Chọn gì) | Cột Operator (Chọn gì) | Cột Filter Expression (Ghi / Chọn gì) |
| :---: | :--- | :--- | :---: | :--- |
| **Dòng 1** | Nhấp chọn **`DIM Club`** | Nhấp chọn **`Club Name`** | Bấm dropdown chọn **`Custom`** (hoặc `MDX`) | Bấm vào ô → nhấp nút ba chấm **`...`** để mở cửa sổ *Expression Builder*, dán biểu thức `INTERSECT` bên dưới → Bấm **OK** |

*Biểu thức nhập vào cửa sổ Expression Builder ở Dòng 1:*
```mdx
INTERSECT(
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
    ),
    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        ),
        30,
        ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
    )
)
```

#### Bước 4: Kéo thả Thuộc tính và Thước đo vào Lưới Dữ liệu (Grid Canvas phía dưới)
Quan sát cây thư mục **Metadata** ở bên trái tab Browser:
1. **Kéo Chiều Câu lạc bộ (Rows):**
   * Mở rộng chiều **`DIM Club`** → tìm thuộc tính **`Club Name`**: Kéo thả vào vùng chữ trống *"Drag levels or measures here to add to the query"*.
2. **Kéo Phân loại Cuối tuần / Ngày thường (Columns):**
   * Mở rộng chiều **`DIM Time`** → tìm thuộc tính **`Is Weekend`**: Kéo thả lên vùng cột (Columns) để chia bảng làm 2 cột: Cuối tuần (1) và Ngày thường (0).
3. **Kéo Thước đo Bàn thắng & Thẻ vàng (Measures):**
   * Mở rộng thư mục **`Measures`** → mở nhóm **`FACT Player Match Perf`**.
   * Nhấp giữ chuột vào thước đo **`Goals`**, kéo thả vào vùng dữ liệu trung tâm.
   * Tiếp tục nhấp giữ thước đo **`Yellow Cards`**, kéo thả vào ngay bên cạnh cột `Goals`.

#### Bước 5: Thực thi truy vấn và Xem kết quả
1. Nhấp chuột vào dòng chữ màu xanh **"Click to execute the query"** (hoặc bấm biểu tượng dấu chấm than đỏ **`! Execute`** / phím tắt **F5** trên thanh công cụ).
2. Lưới dữ liệu lập tức chạy và hiển thị ma trận hiệu năng của các đội bóng ưu tú trên cả Cuối tuần và Ngày thường.

---

### 2.2. Sử dụng PivotTable trên Microsoft Excel

Phương pháp này dành cho chuyên viên phân tích kinh doanh khai thác dữ liệu trực tiếp trên Excel.

#### Bước 1: Khởi tạo kết nối tới SSAS Cube
1. Khởi động **Microsoft Excel**, tạo một trang tính trống (**Blank Workbook**).
2. Chọn thẻ tab **`Data`** trên thanh Ribbon → **`Get Data`** → **`From Database`** → **`From Analysis Services`**.
3. Cửa sổ **Data Connection Wizard** xuất hiện: Nhập `localhost`, chọn **`Use Windows Authentication`** → Nhấn **Next >**.

#### Bước 2: Chọn Database và Khối đa chiều
1. Chọn cơ sở dữ liệu: **`DW_Football_SSAS`** → Chọn Cube: **`DW Football Transfermarkt`**.
2. Nhấn **Finish** → Chọn **`PivotTable Report`** tại ô **`=$A$3`** → Nhấn **OK**.

#### Bước 3: Thao tác kéo thả trong khung `PivotTable Fields`
Quan sát khung danh sách trường **PivotTable Fields** ở góc phải màn hình Excel:

| Vùng PivotTable (Kéo vào đâu) | Tên Trường dữ liệu | Vị trí thư mục nguồn |
| :--- | :--- | :--- |
| **Ô `Columns` (Cột ma trận)** | **`Is Weekend`** | Mở thư mục **`DIM Time`** → Kéo `Is Weekend` thả vào ô Columns. |
| **Ô `Rows` (Dòng dữ liệu)** | **`Club Name`** | Mở thư mục **`DIM Club`** → Kéo `Club Name` thả vào ô Rows. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Goals`** | Mở thư mục **`Measures`** → Kéo `Goals` thả vào ô Values. |
| **Ô `Values` ($\\Sigma$ Thước đo)** | **`Yellow Cards`** | Mở thư mục **`Measures`** → Kéo `Yellow Cards` thả vào ô Values. |

#### Bước 4: Thiết lập Bộ lọc Top 30 CLB xuất sắc
1. Nhấp chuột vào mũi tên lọc tại ô tiêu đề dòng **`Row Labels`** (ô `A4`).
2. Di chuột vào mục **`Value Filters`** → chọn tiếp **`Top 10...`**.
3. Trong hộp thoại Top 10 Filter: Đổi số `10` thành **`30`** Items theo **`Sum of Goals`** → Nhấn **OK**.

#### Bước 5: Trình bày bảng kết quả
* Vào tab **`Design`** → **Report Layout** → chọn **`Show in Tabular Form`**.
* Tắt tổng phụ: **Subtotals** → **`Do Not Show Subtotals`**.

---

### 2.3. Sử dụng Ngôn ngữ truy vấn MDX (SSMS)

Phương pháp này mang lại khả năng tối ưu hóa tính toán cao nhất và kiểm soát toàn diện logic giao tập hợp.

#### Bước 1: Mở trình soạn thảo truy vấn MDX
1. Khởi động **SQL Server Management Studio (SSMS)** → kết nối Analysis Services.
2. Mở rộng `Databases` → `DW_Football_SSAS` → `Cubes`.
3. Chuột phải vào Cube **`DW Football Transfermarkt`** → chọn **`New Query`** → **`MDX`**.

#### Bước 2: Soạn thảo câu truy vấn MDX
Nhập câu lệnh MDX hoàn chỉnh sau:

```mdx
/* ==============================================================================
   Truy vấn MDX 09: So sánh hiệu năng & thẻ phạt của các CLB giữa Cuối tuần & Ngày thường
   Ứng dụng Giao Tập Hợp INTERSECT & Tích Đề-các CROSSJOIN
   Database: DW_Football_SSAS | Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (Is_Weekend = 1)
    SET [Top_Weekend_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        )

    -- 2. Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (Is_Weekend = 0)
    SET [Top_Weekday_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        )

    -- 3. Giao tập hợp (INTERSECT): Các CLB xuất sắc toàn diện cả Cuối tuần và Ngày thường
    SET [Elite_Clubs_All_Days] AS
        INTERSECT([Top_Weekend_Clubs], [Top_Weekday_Clubs])

SELECT
    -- Trục Cột (COLUMNS): Tích Đề-các giữa Thời điểm và Thước đo
    CrossJoin(
        { [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] },
        { [Measures].[Goals], [Measures].[Yellow Cards] }
    ) ON COLUMNS,

    -- Trục Dòng (ROWS): Danh sách các CLB ưu tú thuộc tập hợp giao INTERSECT, xếp giảm dần
    ORDER(
        [Elite_Clubs_All_Days],
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
```

**Bóc tách chi tiết từng mệnh đề truy vấn:**
* **`SET [Top_Weekend_Clubs]`**: Trích xuất Top 30 CLB ghi bàn nhiều nhất vào các ngày cuối tuần (`Is Weekend = 1`).
* **`SET [Top_Weekday_Clubs]`**: Trích xuất Top 30 CLB ghi bàn nhiều nhất vào các ngày trong tuần (`Is Weekend = 0`).
* **`INTERSECT(...)`**: Phép toán giao tập hợp lọc ra các đội bóng xuất hiện đồng thời trong cả hai danh sách.
* **`CrossJoin(...) ON COLUMNS`**: Kết hợp 2 trạng thái thời điểm với 2 thước đo bàn thắng và thẻ phạt trên trục **CỘT** (Axis 0).
* **`ORDER(..., BDESC) ON ROWS`**: Sắp xếp danh sách CLB giảm dần theo tổng bàn thắng trên trục **HÀNG** (Axis 1).

#### Giải thích chi tiết cơ chế hoạt động của các hàm MDX:

1. **Hàm giao tập hợp `INTERSECT(«Set_1», «Set_2»[, ALL])`**:
   * **Cú pháp chuẩn:** `INTERSECT(Set_1, Set_2)`
   * **Tham số thực tế trong truy vấn:**
     * `Set_1`: Tập hợp Top 30 CLB ghi bàn nhiều nhất vào Cuối tuần (`Is_Weekend = 1`, kết quả từ hàm `TOPCOUNT` thứ nhất).
     * `Set_2`: Tập hợp Top 30 CLB ghi bàn nhiều nhất vào Ngày thường (`Is_Weekend = 0`, kết quả từ hàm `TOPCOUNT` thứ hai).
   * **Cơ chế hoạt động kỹ thuật:**
     * Thực hiện phép giao tập hợp trong đại số MDX ($Set_1 \cap Set_2$).
     * Formula Engine tính toán độc lập hai danh sách Top 30, sau đó hàm `INTERSECT` đối chiếu và chỉ giữ lại những câu lạc bộ xuất hiện đồng thời trong cả hai danh sách.
     * Thứ tự các phần tử trong tập kết quả trả về được bảo toàn theo đúng thứ tự xuất hiện của `Set_1`.
     * Những đội bóng chỉ ghi nhiều bàn cuối tuần nhưng ít bàn ngày thường (hoặc ngược lại) sẽ bị loại bỏ, chỉ giữ lại các CLB duy trì được hiệu suất tấn công ổn định toàn diện trong cả hai khung thời gian.
   * **Kết quả trả về:** Tập hợp gồm các câu lạc bộ ưu tú duy trì phong độ cao cả cuối tuần và ngày thường.

2. **Hàm `TOPCOUNT` kết hợp Tuple tiêu chí cục bộ**:
   * **Cú pháp chuẩn:** `TOPCOUNT(Set, 30, ([Measures].[Goals], [DIM Time].[Is Weekend].[1]))`
   * **Cơ chế hoạt động kỹ thuật:**
     * Tiêu chí sắp xếp của hàm `TOPCOUNT` là một Tuple giao cắt đa chiều `([Measures].[Goals], [DIM Time].[Is Weekend].[1])`.
     * Kỹ thuật này cho phép lọc và xếp hạng dữ liệu theo điều kiện thi đấu cuối tuần riêng biệt mà không làm ảnh hưởng đến ngữ cảnh toàn cục của toàn bộ câu truy vấn.

3. **Hàm `CrossJoin` trên trục COLUMNS**:
   * **Cơ chế:** Ghép các thước đo `{ [Measures].[Goals], [Measures].[Yellow Cards] }` với hai trạng thái thời gian `{ [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] }`, sinh ra 4 cột hiển thị trực quan: Cuối tuần (Bàn thắng, Thẻ vàng) và Ngày thường (Bàn thắng, Thẻ vàng).


#### Bước 3: Thực thi truy vấn và Đọc kết quả
1. Nhấn nút **`! Execute`** (hoặc phím **`F5`**).
2. Xem kết quả hiển thị ma trận phân bổ bàn thắng và thẻ vàng chi tiết giữa Cuối tuần và Ngày thường.

---

### 2.4. Nhận xét & Đối chiếu kết quả

1. **Tính chính xác và Nhất quán của Dữ liệu:**
   * Cả 3 phương thức tiếp cận (Cube Browser trong SSDT, PivotTable trong Excel, và truy vấn MDX trong SSMS) đều phân tích chính xác tập hợp 9 CLB ưu tú xuất hiện đồng thời trong cả hai nhóm Top 30 bàn thắng Cuối tuần và Ngày thường.
   * **Manchester City** thể hiện sự hủy diệt đồng đều ở mọi đấu trường với tổng cộng 245 bàn thắng (94 bàn cuối tuần, 151 bàn ngày thường; tổng cộng 129 thẻ vàng). Đứng tiếp theo là **FC Bayern Munich** (225 bàn: 115 cuối tuần, 110 ngày thường), **PSV Eindhoven** (219 bàn: 82 cuối tuần, 137 ngày thường), và **Real Madrid** (210 bàn: 76 cuối tuần, 134 ngày thường).
   * Về chỉ số kỷ luật, **Real Madrid** và **Bayer 04 Leverkusen** nhận nhiều thẻ vàng nhất giữa tuần (128 và 120 thẻ vàng), phản ánh tính chất căng thẳng khốc liệt của các lượt trận cúp châu lục (UEFA Champions League, Europa League).

2. **So sánh 3 phương thức thực hiện:**

| Tiêu chí so sánh | 2.1. Visual Studio SSDT (Cube Browser) | 2.2. Excel PivotTable | 2.3. SSMS MDX Query |
| :--- | :--- | :--- | :--- |
| **Giao diện thao tác** | Kéo thả trực quan, hỗ trợ Expression Builder cho INTERSECT. | Kéo thả PivotTable thân thiện với chuyên viên phân tích. | Soạn thảo lệnh truy vấn kịch bản mã nguồn mở. |
| **Tính đồng nhất** | Trả về đúng 9 CLB $\times$ Cuối tuần / Ngày thường chuẩn xác. | Trả về đúng 9 CLB $\times$ Cuối tuần / Ngày thường chuẩn xác. | Trả về đúng 9 CLB $\times$ Cuối tuần / Ngày thường chuẩn xác. |
| **Độ phức tạp** | Trung bình (cần dán biểu thức INTERSECT vào Filter). | Đơn giản (kéo trường `Is Weekend` vào Columns). | Chuyên sâu (làm chủ cấu trúc SET và đại số tập hợp). |

---

## 3. Bảng Kết quả Truy vấn Dự kiến (Expected Output)

Sau khi hoàn thành bất kỳ phương pháp nào trong 3 cách trên, kết quả trả về hiển thị toàn bộ 9 dòng dữ liệu thực tế từ khối Cube OLAP:

| STT | Tên Câu Lạc Bộ (`Club Name`) | Sân Nhà - Bàn Thắng | Sân Nhà - Thẻ Vàng | Sân Khách - Bàn Thắng | Sân Khách - Thẻ Vàng |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Manchester City** | 94 | 49 | 151 | 80 |
| **2** | **Bayern Munich** | 115 | 62 | 110 | 67 |
| **3** | **PSV Eindhoven** | 82 | 24 | 137 | 76 |
| **4** | **Real Madrid** | 76 | 47 | 134 | 128 |
| **5** | **Arsenal FC** | 75 | 42 | 124 | 103 |
| **6** | **Paris Saint-Germain** | 59 | 40 | 139 | 112 |
| **7** | **Bayer 04 Leverkusen** | 65 | 74 | 126 | 120 |
| **8** | **Celtic FC** | 75 | 43 | 111 | 62 |
| **9** | **Inter Milan** | 70 | 49 | 114 | 103 |



---

## 4. Các hàm MDX sử dụng & Chi tiết cú pháp

| Tên hàm MDX | Cú pháp chuẩn | Giải thích chức năng & Vai trò trong truy vấn |
| :--- | :--- | :--- |
| **`INTERSECT`** | `INTERSECT(Set1, Set2 [, ALL])` | Giao hai tập hợp: chỉ giữ lại các thành viên xuất hiện đồng thời trong cả hai nhóm. |
| **`TOPCOUNT`** | `TOPCOUNT(Set, Count [, Numeric_Exp])` | Lọc lấy $N$ thành viên có giá trị số đo cao nhất. |
| **`CROSSJOIN`** | `CrossJoin(Set1, Set2)` | Tích Đề-các nhân không gian các chiều trên trục hiển thị. |
| **`NONEMPTY`** | `NONEMPTY(Set [, Measure])` | Loại bỏ các phần tử rỗng không phát sinh dữ liệu sự kiện. |
| **`ORDER` (BDESC)** | `ORDER(Set, Exp, BDESC)` | Sắp xếp phá vỡ phân cấp từ cao xuống thấp trên toàn tập hợp. |

---

## 5. Đánh giá độ phức tạp thuật toán và tối ưu hóa SSAS

* **Độ phức tạp thời gian (Time Complexity):** Phép toán `INTERSECT` giữa 2 tập hợp $K=30$ phần tử có độ phức tạp $O(K_1 + K_2) = O(60)$ cực kỳ nhanh nhờ giải thuật băm băm (Hash Match) trong Formula Engine.
* **Tối ưu hóa Storage Engine (SE):** Bộ lọc `Is_Weekend` được lưu trữ dưới dạng cờ nhị phân (0/1) trong bảng chiều `DIM_Time`, giúp Storage Engine tận dụng tối đa chỉ mục Bitmap Index quét dữ liệu tức thì.
