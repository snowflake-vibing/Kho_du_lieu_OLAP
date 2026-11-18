# 4.2.1 Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu, Chu kỳ Thời gian và Huấn luyện viên Trưởng (Grouping and Totals Report)

Tài liệu này cung cấp hướng dẫn thiết kế hoàn chỉnh **Báo biểu 1** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **TIÊU CHÍ CHẤM ĐIỂM BẮT BUỘC - BÁO CÁO DẠNG GROUPING AND TOTALS:**
> * Báo biểu 1 được thiết kế chuyên trách để đáp ứng trọn vẹn yêu cầu tiên quyết của giảng viên: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
> * **Khai thác toàn bộ các trường dữ liệu và thước đo MỚI 100%**: Sử dụng **`Coach Name`** (Huấn luyện viên trưởng), **`Competition Type`** (Phân loại Cúp Châu Âu vs Giải Quốc nội), **`Country Name`** (Quốc gia tổ chức), **`Round`** (Vòng đấu / Chặng thi đấu từ `DIM Game`), **`Quarter`** (Quý thi đấu) và thước đo mới **`Total Coaches`** (`175` HLV), loại bỏ hoàn toàn cảm giác lặp lại các cột cũ ở Báo biểu 2 và 3.
> * **Bộ ba Visual kết hợp hoàn chỉnh (Stacked Bar + Stacked Column + Matrix Grouping & Totals):**
>   1. **Visual 1 (Trên Trái) – Biểu đồ Thanh Ngang Xếp chồng Phân cấp (Stacked Bar Chart with Total Labels & 4-Level Drill-down):** Phân tầng cấu trúc giải đấu và vòng đấu 4 cấp (`Competition Type` $\rightarrow$ `Country Name` $\rightarrow$ `Competition Name` $\rightarrow$ `Round` từ `DIM Game`), bật **Total Labels: ON** hiển thị Tổng G+A trên đầu mỗi thanh.
>   2. **Visual 2 (Dưới Trái) – Biểu đồ Cột Dọc Xếp chồng Theo Chu kỳ Thời gian (Stacked Column Chart with Total Labels & Drill-down):** Phân nhóm hỏa lực theo Mùa giải và Quý (`Season` $\rightarrow$ `Quarter`), xếp chồng `Goals` + `Assists` và bật **Total Labels: ON** hiển thị Tổng G+A trên đỉnh mỗi cột.
>   3. **Visual 3 (Bên Phải) – Bảng Ma trận Phân nhóm & Tổng hợp theo HLV Trưởng (Grouping & Totals Matrix Visual):** Phân nhóm 3 tầng `Huấn luyện viên trưởng` (`Coach Name`) $\rightarrow$ `Câu lạc bộ` (`Club Name`) $\rightarrow$ `Cầu thủ ghi bàn` (`Player Name`), kích hoạt dòng **Tổng phụ (Subtotals)** cho từng HLV và dòng **Tổng cộng (Grand Total)** ở đáy bảng.
> * **Tính năng Tương tác Chéo (Cross-filtering):** Nhấp chọn một giải đấu / vòng đấu (Visual 1) hoặc một Mùa giải / Quý (Visual 2) $\rightarrow$ Toàn bộ thẻ KPI và Bảng Ma trận HLV (Visual 3) lập tức lọc đồng bộ theo lát cắt đó.

---

## 1. Mục tiêu Nghiệp vụ và Ý nghĩa Thống kê Đa chiều

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Bức tranh Cấu trúc Giải đấu & Vòng đấu (Visual 1 - Stacked Bar):** Giải Vô địch Quốc gia (`domestic_league`) và Cúp Châu lục (`international_cup` - Champions League) có sự chênh lệch hỏa lực ra sao? Khoan sâu 4 cấp xuống từng Vòng đấu (`Round` từ `DIM Game`) để xem sản lượng bàn thắng qua Vòng bảng, Vòng 1/8, Tứ kết, Bán kết và Chung kết.
2. **Nhịp điệu Hỏa lực theo Mùa giải & Quý (Visual 2 - Stacked Column):** Hỏa lực bàn thắng và kiến tạo phân bổ ra sao qua từng Mùa giải (`2022/2023` = 16,903 G+A; `2023/2024` = 17,009 G+A) và khi khoan sâu xuống từng Quý (`Q1`, `Q2`, `Q3`, `Q4`)? Nhãn Total Labels trên đỉnh cột cho thấy ngay tổng sản lượng từng giai đoạn.
3. **Hiệu suất Tấn công Dưới Triết lý Huấn luyện viên trưởng (Visual 3 - Matrix Grouping & Totals):** Đánh giá năng lực xây dựng hỏa lực của từng Thuyền trưởng (*Pep Guardiola, Vincent Kompany, Peter Bosz, Xabi Alonso, Mikel Arteta, Luis Enrique...*). Dòng Subtotal của từng HLV cho biết tổng bàn thắng, tổng kiến tạo, tổng G+A và số trận cầm quân; dòng Grand Total ở đáy bảng tổng hợp toàn bộ hệ thống.

### 1.2. Phân định độc lập tuyệt đối với Báo biểu 2 và Báo biểu 3
* **Báo biểu 1 (Grouping & Totals Report):** Độc quyền về **Cấu trúc Giải đấu & Vòng đấu (`Competition Type`, `Country Name`, `Round`)**, **Chu kỳ Quý (`Quarter`)** và **Triết lý Huấn luyện viên trưởng (`Coach Name`, `Total Coaches = 175`)**.
* **Báo biểu 2 (Executive Tactical Dashboard):** Độc quyền về **Trinh sát tác chiến & Bắt bài kẻ mạnh trước trận đấu** (Soi chân thuận `Foot`, độ tuổi `Age`, quốc tịch cầu thủ `Player Country`, thánh địa `Stadium`).
* **Báo biểu 3 (Executive Discipline Dashboard):** Độc quyền về **Kỷ luật thẻ phạt và Tải trọng thể lực** (Thẻ vàng `Yellow Cards`, Thẻ đỏ `Red Cards`, Phút thi đấu theo lứa tuổi).

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG      |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Số Trận]    | [Card 2: Tổng Số HLV Trưởng]| [Card 3: Tổng Bàn Thắng]  | [Card 4: Tổng Đóng Góp G+A]       |
| 6,965 Trận Quản Trị       | 175 Huấn Luyện Viên       | 19.17K Bàn Thắng Ghi Được | 33.91K Điểm Sát Thương Tấn Công   |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold                |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Purple #FAF5FF | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB          |
| (W: 455, H: 90, X: 20)    | (W: 455, H: 90, X: 495)   | (W: 455, H: 90, X: 970)   | (W: 455, H: 90, X: 1445)          |
+---------------------------+---------------------------+---------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Loại Cúp/Giải] | [Bộ lọc 3: Quốc gia giải] | [Bộ lọc 4: Quý thi đấu]           |
| DIM Time [Season]         | Comp [Competition Type]   | Comp [Country Name]       | DIM Time [Quarter]                |
| Dropdown (W: 455, H: 75)  | Dropdown (W: 455, H: 75)  | Dropdown (W: 455, H: 75)  | Tile/Drop (W: 455, H: 75)         |
| Tọa độ: X = 20, Y = 190   | Tọa độ: X = 495, Y = 190  | Tọa độ: X = 970, Y = 190  | Tọa độ: X = 1445, Y = 190         |
+--------------------------------------------------+----------------------------------------------------------------------+
| [VISUAL 1: STACKED BAR CẤU TRÚC GIẢI ĐẤU]        | [VISUAL 3: MATRIX PHÂN NHÓM & TỔNG HỢP THEO HLV TRƯỞNG]              |
| Y: Competition Type -> Country -> Comp -> Round  | Rows: Coach Name -> Club Name -> Player Name                         |
| X: Goals (#2563EB) + Assists (#06B6D4)           | Values: Goals, Assists, Goal Contributions (Data Bars), Matches      |
| Total labels: ON | Drill-down: 4 cấp             | Subtotals: ON (Dòng Tổng từng HLV) | Grand Total: ON                 |
| X = 20, Y = 280 | W = 860 px, H = 380 px         | Stepped layout: ON (Cây thư mục gập mở + / -)                        |
+--------------------------------------------------+                                                                      |
| [VISUAL 2: STACKED COLUMN THEO MÙA GIẢI & QUÝ]   |                                                                      |
| X: Season -> Quarter (Drill-down 2 cấp)          |                                                                      |
| Y: Goals (#2563EB) + Assists (#06B6D4)           |                                                                      |
| Total labels: ON (Tổng G+A trên đỉnh mỗi cột)    |                                                                      |
| X = 20, Y = 680 | W = 860 px, H = 380 px         | Tọa độ: X = 900 px, Y = 280 px | W = 1000 px, H = 780 px             |
+--------------------------------------------------+----------------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi động và Cấu hình Canvas 1920 x 1080 px
1. Mở phần mềm **Power BI Desktop**, kết nối **Connect live** tới máy chủ SSAS `localhost`, chọn khối Cube **`[DW Football Transfermarkt]`**.
2. Đổi tên trang thành: `Grouping & Totals (Giải đấu, Quý & HLV)`.
3. Mở khung **Format report page**:
   * **Canvas settings:** Type: `Custom`, `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói `#F8FAFC`, gạt **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng 1)
1. Trên thẻ **Insert**, chọn **Text box**.
2. Nhập nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG`.
3. Font `Segoe UI`, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), màu `#0F172A`.
4. Thẻ **General** $\rightarrow$ **Properties**: `Width = 1880 px`, `Height = 55 px`, `X = 20 px`, `Y = 15 px`.
5. **Effects:** Nền `#FFFFFF`, Viền mỏng `#E2E8F0`, Bo góc `10 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Quản trị & Hỏa lực Cốt lõi
Tạo 4 visual **Card** tại hàng `Y = 85 px`, `Height = 90 px`, `Width = 455 px`:

1. **Card 1 (Tổng Số Trận Quản Trị):** `X = 20 px`.
   * Kéo thước đo **`[Measures].[Distinct Matches Played]`**. Đổi tên: `Tổng Số Trận Quản Trị`.
   * Callout value: **`35 pt` Bold** (hiển thị `6,965`), màu `#0F172A`. Nền `#EFF6FF` (Pastel Blue), Bo góc `10 px`.
2. **Card 2 (Tổng Số Huấn Luyện Viên Trưởng):** `X = 495 px`.
   * Kéo thước đo chuẩn **`[Measures].[Total Coaches]`**. Đổi tên: `Tổng Số HLV Trưởng`.
   * Callout value: **`35 pt` Bold** (hiển thị **`175`** HLV), màu `#0F172A`. Nền `#FAF5FF` (Pastel Purple), Bo góc `10 px`.
3. **Card 3 (Tổng Bàn Thắng Toàn Giải):** `X = 970 px`.
   * Kéo thước đo **`[Measures].[Goals]`**. Đổi tên: `Tổng Bàn Thắng Toàn Giải`.
   * Callout value: **`35 pt` Bold** (hiển thị `19.17K`). Nền `#F0FDF4` (Pastel Green), Bo góc `10 px`.
4. **Card 4 (Tổng Điểm Sát Thương Tấn Công G+A):** `X = 1445 px`.
   * Kéo thước đo **`[Measures].[Goal Contributions]`**. Đổi tên: `Tổng Đóng Góp G+A`.
   * Callout value: **`35 pt` Bold** (hiển thị `33.91K`). Nền `#FFFBEB` (Pastel Amber), Bo góc `10 px`.

---

### Bước 4: Thiết lập Khối 4 Bộ lọc Slicers Mới 100%
Tại hàng `Y = 190 px`, `Height = 75 px`, tạo 4 bộ lọc rộng rãi `Width = 455 px`:

1. **Slicer 1 (Mùa giải):** `X = 20 px`, kéo `DIM Time [Season]`, Style `Dropdown`.
2. **Slicer 2 (Phân loại Cúp / Giải - MỚI):** `X = 495 px`, kéo `DIM Competition [Competition Type]`, Style `Dropdown` (Lọc xem Cúp Châu lục `international_cup` hay Giải Quốc nội `domestic_league`).
3. **Slicer 3 (Quốc gia giải đấu - MỚI):** `X = 970 px`, kéo `DIM Competition [Country Name]`, Style `Dropdown` (Lọc theo England, Spain, Germany, Italy, France...).
4. **Slicer 4 (Quý thi đấu - MỚI):** `X = 1445 px`, kéo `DIM Time [Quarter]`, Style `Tile` hoặc `Dropdown` (Lọc theo Q1, Q2, Q3, Q4).

---

### Bước 5: Visual 1 (Trên Trái) – Stacked Bar Chart Phân cấp Giải đấu & Vòng đấu

Biểu đồ thanh ngang xếp chồng phân tầng cấu trúc giải đấu 4 cấp kèm nhãn **Total Labels**:

1. **Cấu hình trường dữ liệu:**
   * Chọn visual **Stacked bar chart** (Biểu đồ thanh ngang xếp chồng).
   * Thẻ **General** $\rightarrow$ **Properties**: `X = 20 px`, `Y = 280 px`, `Width = 860 px`, `Height = 380 px`.
   * **Y-axis (Phân cấp 4 tầng - 4-Level Drill-down):** Kéo lần lượt 4 trường:
     1. `DIM Competition` $\rightarrow$ **`[Competition Type]`** (Cấp 1: Loại giải).
     2. `DIM Competition` $\rightarrow$ **`[Country Name]`** (Cấp 2: Quốc gia giải đấu).
     3. `DIM Competition` $\rightarrow$ **`[Competition Name]`** (Cấp 3: Tên giải đấu cụ thể).
     4. `DIM Game` $\rightarrow$ **`[Round]`** (Cấp 4: Vòng đấu / Chặng thi đấu - *Group A-H, last 16, Quarter-Finals, Semi-Finals, Final hoặc Matchday 1..38*).
   * **X-axis:** Kéo 2 thước đo: `[Measures].[Goals]` và `[Measures].[Assists]`.
2. **Định dạng Grouping & Totals (Tab Format visual):**
   * **Total labels:** Gạt **ON**! (Font `Segoe UI Bold`, `11 pt`, màu `#0F172A` hiển thị **Tổng G+A** ở đầu mỗi thanh).
   * **Data labels:** Gạt **ON** (`Inside end`, `10 pt`).
   * **Bars:** `Goals` màu **`#2563EB`** (Xanh dương đậm), `Assists` màu **`#06B6D4`** (Xanh Cyan).
   * **Y-axis Title:** `OFF`; **X-axis:** `OFF`.
3. **Tiêu đề:** Bật **ON**, nhập `Phân cấp Hỏa lực theo Giải đấu & Vòng đấu (Stacked Bar Drill-down)`, Font `Segoe UI`, **`16 pt` Bold**, Căn giữa. Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Dưới Trái) – Stacked Column Chart Phân nhóm theo Mùa giải & Quý

Biểu đồ cột dọc xếp chồng thể hiện tổng sản lượng tấn công theo chu kỳ thời gian kèm nhãn **Total Labels**:

1. **Cấu hình trường dữ liệu:**
   * Chọn visual **Stacked column chart** (Biểu đồ cột dọc xếp chồng).
   * Thẻ **General** $\rightarrow$ **Properties**: `X = 20 px`, `Y = 680 px`, `Width = 860 px`, `Height = 380 px`.
   * **X-axis (Phân cấp 2 tầng - Drill-down):** Kéo lần lượt 2 trường:
     1. `DIM Time` $\rightarrow$ **`[Season]`** (Cấp 1: `2022/2023`, `2023/2024`).
     2. `DIM Time` $\rightarrow$ **`[Quarter]`** (Cấp 2: Quý `1`, `2`, `3`, `4`).
   * **Y-axis:** Kéo 2 thước đo: `[Measures].[Goals]` và `[Measures].[Assists]`.
2. **Định dạng Grouping & Totals (Tab Format visual):**
   * **Total labels:** Gạt **ON**! (Font `Segoe UI Bold`, `12 pt`, màu `#0F172A` hiển thị tổng **16,903** cho mùa `2022/2023` và **17,009** cho mùa `2023/2024`; khi bấm Drill-down xuống Quý sẽ tự động hiển thị tổng của từng Quý).
   * **Data labels:** Gạt **ON** (`Inside center`, `11 pt`).
   * **Columns:** `Goals` màu **`#2563EB`**, `Assists` màu **`#06B6D4`** (đồng bộ màu 100% với Visual 1).
   * **X-axis Title:** `OFF`; **Y-axis:** `OFF`.
3. **Tiêu đề:** Bật **ON**, nhập `Tổng hợp Hỏa lực theo Mùa giải & Quý (Stacked Column Grouping & Totals)`, Font `Segoe UI`, **`16 pt` Bold**, Căn giữa. Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Visual 3 (Bên Phải) – Ma trận Phân nhóm & Tổng hợp theo Huấn Luyện Viên Trưởng (Matrix Grouping & Totals)

Bảng ma trận đa cấp độ sâu 3 tầng hoàn thiện chuẩn mực **Grouping and Totals** với dòng Subtotals và Grand Total:

1. **Cấu hình trường dữ liệu:**
   * Chọn visual **Matrix** (Ma trận phân cấp).
   * Thẻ **General** $\rightarrow$ **Properties**: `X = 900 px`, `Y = 280 px`, `Width = 1000 px`, `Height = 780 px`.
   * **Rows (Phân nhóm 3 cấp):**
     1. `DIM Club` $\rightarrow$ **`[Coach Name]`** (Cấp 1: Huấn luyện viên trưởng - *Pep Guardiola, Vincent Kompany, Peter Bosz, Xabi Alonso, Mikel Arteta...*).
     2. `DIM Club` $\rightarrow$ **`[Club Name]`** (Cấp 2: Câu lạc bộ dẫn dắt).
     3. `DIM Player` $\rightarrow$ **`[Player Name]`** (Cấp 3: Cầu thủ / Học trò ghi bàn).
   * **Values (Các thước đo tổng hợp):**
     1. `[Measures].[Goals]` (Số bàn thắng).
     2. `[Measures].[Assists]` (Số pha kiến tạo).
     3. `[Measures].[Goal Contributions]` (Tổng G+A).
     4. `[Measures].[Distinct Matches Played]` (Số trận cầm quân).
2. **Kích hoạt Grouping & Totals:**
   * Tab **Format visual** $\rightarrow$ mục **Subtotals**:
     * Gạt **Row subtotals: ON**! Định dạng chữ in đậm (**Bold**), màu nền xám nhạt `#E2E8F0`.
     * *Ý nghĩa:* Dòng Subtotal cấp HLV hiển thị tổng chính xác từng vị Thuyền trưởng (ví dụ: *Pep Guardiola: 245 bàn, 190 kiến tạo, 435 G+A sau 99 trận*).
   * Mục **Grand total**: Gạt **Row grand total: ON**! (Dòng tổng cộng toàn bộ ở đáy bảng).
   * **Row headers** $\rightarrow$ **Options**: Bật **Stepped layout: ON** (cây thư mục có nút `+ / -` gập mở mượt mà).
3. **Bật thanh dữ liệu Data Bars:**
   * Tab **Format visual** $\rightarrow$ **Cell elements** $\rightarrow$ chọn `Goal Contributions`, bật **Data bars: ON**, màu **`#2563EB`**.
4. **Tiêu đề & Nhãn:**
   * Title: Bật **ON**, nhập `Bảng Ma trận Phân nhóm & Tổng hợp theo HLV Trưởng (Matrix Grouping & Totals)`, Font `Segoe UI`, **`18 pt` Bold**, Căn giữa.
   * Đổi tên nhãn hàng: `Coach Name` $\rightarrow$ `Huấn luyện viên`, `Club Name` $\rightarrow$ `Câu lạc bộ`, `Player Name` $\rightarrow$ `Cầu thủ`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo

1. **Đáp ứng 100% cả tính trực quan lẫn chuẩn mực Grouping & Totals:**
   * **Stacked Bar (Visual 1)** & **Stacked Column (Visual 2)** mang lại sự đa dạng đồ họa, đều có **Drill-down phân nhóm (Grouping)** và bật **Total Labels (Totals)**.
   * **Matrix (Visual 3)** cung cấp đầy đủ dòng **Subtotals** theo từng HLV và **Grand Total** ở đáy bảng, đảm bảo tuyệt đối tiêu chí chấm điểm của đề bài.
2. **Kịch bản Tương tác Chéo (Cross-filtering):**
   * Nhấp vào `uefa-champions-league` $\rightarrow$ `Final` ở **Stacked Bar (Visual 1)** $\rightarrow$ **Stacked Column (Visual 2)** tự động lọc thời điểm diễn ra trận chung kết và **Matrix (Visual 3)** lập tức bung ra danh sách HLV cùng cầu thủ ghi bàn ở trận Chung kết!
   * Nhấp vào Quý `4` của `2023/2024` ở **Stacked Column (Visual 2)** $\rightarrow$ Xem ngay phong độ bùng nổ của các giải đấu và HLV trong giai đoạn nước rút Q4!
