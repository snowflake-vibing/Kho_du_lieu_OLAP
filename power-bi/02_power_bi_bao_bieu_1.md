# 4.2.1 Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu và Huấn luyện viên Trưởng (Grouping and Totals Tournament Hierarchy & Head Coach Performance Report)

Tài liệu này cung cấp hướng dẫn thiết kế hoàn chỉnh **Báo biểu 1** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **TIÊU CHÍ CHẤM ĐIỂM BẮT BUỘC - BÁO CÁO DẠNG GROUPING AND TOTALS:**
> * Báo biểu 1 được thiết kế chuyên trách để đáp ứng trọn vẹn yêu cầu tiên quyết của giảng viên: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
> * **Khai thác toàn bộ các trường dữ liệu và thước đo MỚI 100%**: Sử dụng **`Coach Name`** (Huấn luyện viên trưởng), **`Competition Type`** (Phân loại Cúp Châu Âu vs Giải Quốc nội), **`Country Name`** (Quốc gia tổ chức), **`Quarter`** (Quý thi đấu), **`QoQ Goals Growth`** (Tăng trưởng bàn thắng theo Quý) và thước đo mới **`Total Coaches`** (`175` HLV), loại bỏ hoàn toàn cảm giác lặp lại các cột cũ ở Báo biểu 2 và 3.
> * Toàn bộ phần thân trang được cấu thành bởi **2 Bảng Ma trận Phân nhóm & Tổng hợp Đa cấp (2 Matrix Visuals)** đặt song song đối xứng:
>   1. **Visual 1 (Bên Trái) – Grouping Cấu trúc Giải đấu & Tăng trưởng:** Phân nhóm 3 tầng `Loại giải` (`Competition Type`) $\rightarrow$ `Quốc gia` (`Country Name`) $\rightarrow$ `Tên giải đấu` (`Competition Name`).
>   2. **Visual 2 (Bên Phải) – Grouping Hỏa lực theo Huấn luyện viên trưởng:** Phân nhóm 3 tầng `Huấn luyện viên trưởng` (`Coach Name`) $\rightarrow$ `Câu lạc bộ` (`Club Name`) $\rightarrow$ `Cầu thủ ghi bàn` (`Player Name`).
> * Cả 2 bảng đều kích hoạt đầy đủ các dòng **Tổng phụ (Subtotals)** cho từng cấp nhóm và dòng **Tổng cộng toàn cục (Grand Total)** ở đáy trang, kèm tính năng tương tác chéo (Cross-Filtering) đồng bộ tức thời.

---

## 1. Mục tiêu Nghiệp vụ và Ý nghĩa Thống kê Đa chiều

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Bức tranh Cấu trúc Giải đấu & Tăng trưởng Bàn thắng (Visual 1):** Giải Vô địch Quốc gia (`domestic_league`) và Cúp Châu lục (`international_cup` - Champions League) có sự chênh lệch hỏa lực ra sao? Nhịp độ tăng trưởng bàn thắng theo Quý (`QoQ Goals Growth`) bùng nổ mạnh nhất ở giai đoạn nào trong năm (vòng bảng hay vòng knock-out)? Quốc gia nào sở hữu nền bóng đá cởi mở tấn công nhất châu Âu?
2. **Hiệu suất Tấn công Dưới Triết lý Huấn luyện viên trưởng (Visual 2):** Đánh giá năng lực xây dựng hỏa lực và hiệu quả dùng người của từng Thuyền trưởng đại tài (*Pep Guardiola, Xabi Alonso, Mikel Arteta, Carlo Ancelotti, Luis Enrique, Arne Slot...*). Dưới trướng mỗi HLV, đội bóng ghi được bao nhiêu bàn thắng, kiến tạo, và học trò nào là ngòi nổ chủ lực số 1?
3. **Phân tích Tương tác Chéo Đỉnh cao (Cross-Filtering):** Khi nhấp chọn giải đấu `Premier League` ở Visual 1 $\rightarrow$ Visual 2 tự động lọc ra toàn bộ các Huấn luyện viên đang cầm quân tại Ngoại Hạng Anh cùng dàn học trò của họ. Khi nhấp chọn `international_cup` $\rightarrow$ Visual 2 hiển thị các HLV có hỏa lực mạnh nhất tại đấu trường Champions League.

### 1.2. Phân định độc lập tuyệt đối với Báo biểu 2 và Báo biểu 3
* **Báo biểu 1 (Grouping & Totals Report):** Độc quyền về **Cấu trúc Giải đấu (`Competition Type`, `Country Name`, `QoQ Growth`)** và **Triết lý Huấn luyện viên trưởng (`Coach Name`, `Total Coaches`)**.
* **Báo biểu 2 (Executive Tactical Dashboard):** Độc quyền về **Trinh sát tác chiến & Bắt bài kẻ mạnh trước trận đấu** (Soi chân thuận `Foot`, độ tuổi `Age`, quốc tịch cầu thủ `Player Country`, thánh địa `Stadium`).
* **Báo biểu 3 (Executive Discipline Dashboard):** Độc quyền về **Kỷ luật thẻ phạt và Tải trọng thể lực** (Thẻ vàng `Yellow Cards`, Thẻ đỏ `Red Cards`, Phút thi đấu theo lứa tuổi).

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU & HUẤN LUYỆN VIÊN    |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Số Trận]    | [Card 2: Tổng Số HLV Trưởng]| [Card 3: Tổng Bàn Thắng]  | [Card 4: Tổng Đóng Góp G+A]       |
| 6,965 Trận Quản Trị       | 175 Huấn Luyện Viên       | 19.17K Bàn Thắng Ghi Được | 33.91K Điểm Sát Thương Tấn Công   |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold                |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Purple #FAF5FF | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB          |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)   | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+---------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Loại Cúp/Giải] | [Bộ lọc 3: Quốc gia giải] | [Bộ lọc 4: Quý thi đấu]           |
| DIM Time [Season]         | Comp [Competition Type]   | Comp [Country Name]       | DIM Time [Quarter]                |
| Dropdown (W: 455, H: 75)  | Dropdown (W: 455, H: 75)  | Dropdown (W: 455, H: 75)  | Tile/Drop (W: 455, H: 75)         |
| Tọa độ: X = 20, Y = 210   | Tọa độ: X = 495, Y = 210  | Tọa độ: X = 970, Y = 210  | Tọa độ: X = 1445, Y = 210         |
+-------------------------------------------------------+-----------------------------------------------------------------+
| [VISUAL 1: PHÂN NHÓM CẤU TRÚC GIẢI ĐẤU (18pt Bold)]   | [VISUAL 2: PHÂN NHÓM THEO HUẤN LUYỆN VIÊN (18pt Bold)]          |
| Rows: Loại giải -> Quốc gia -> Tên giải đấu           | Rows: Huấn luyện viên trưởng -> Câu lạc bộ -> Cầu thủ           |
| Values: Số trận, Bàn thắng, Tăng trưởng QoQ (%), G+A  | Values: Bàn thắng, Kiến tạo, Tổng G+A (Data Bars), Số trận      |
| Subtotals: ON (Tổng cấp Loại giải & Quốc gia)         | Subtotals: ON (Dòng Tổng HLV) | Grand Total: ON                 |
| Grand Total: ON (Tổng toàn bộ châu Âu)                | Tương tác chéo: Lọc HLV theo giải đấu được chọn                |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 760 px| Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 760 px         |
+-------------------------------------------------------+-----------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi động và Cấu hình Canvas 1920 x 1080 px
1. Mở phần mềm **Power BI Desktop**, kết nối **Connect live** tới máy chủ SSAS `localhost`, chọn khối Cube **`[DW Football Transfermarkt]`**.
2. Đổi tên trang thành: `Cấu trúc Giải đấu & HLV (Grouping & Totals)`.
3. Mở khung **Format report page**:
   * **Canvas settings:** Type: `Custom`, `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói `#F8FAFC`, gạt **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng 1)
1. Trên thẻ **Insert**, chọn **Text box**.
2. Nhập nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU VÀ HUẤN LUYỆN VIÊN TRƯỞNG`.
3. Font `Segoe UI`, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
4. Thẻ **General** $\rightarrow$ **Properties**: `Width = 1880 px`, `Height = 55 px`, `X = 20 px`, `Y = 15 px`.
5. **Effects:** Nền `#FFFFFF`, Viền mỏng `#E2E8F0`, Bo góc `10 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Quản trị & Hỏa lực Cốt lõi
Tạo 4 visual **Card** tại hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

1. **Card 1 (Tổng Số Trận Quản Trị):** `X = 20 px`.
   * Kéo thước đo **`[Measures].[Distinct Matches Played]`**. Đổi tên: `Tổng Số Trận Quản Trị`.
   * Callout value: **`35 pt` Bold** (hiển thị `6,965`), màu `#0F172A`. Nền `#EFF6FF` (Pastel Blue), Bo góc `10 px`.
2. **Card 2 (Tổng Số Huấn Luyện Viên Trưởng):** `X = 495 px`.
   * Kéo thước đo chuẩn **`[Measures].[Total Coaches]`** (vừa được triển khai trực tiếp trong Cube). Đổi tên: `Tổng Số HLV Trưởng`.
   * Callout value: **`35 pt` Bold** (hiển thị **`175`** HLV đại tài), màu `#0F172A`. Nền `#FAF5FF` (Pastel Purple), Bo góc `10 px`.
3. **Card 3 (Tổng Bàn Thắng Toàn Giải):** `X = 970 px`.
   * Kéo thước đo **`[Measures].[Goals]`**. Đổi tên: `Tổng Bàn Thắng Toàn Giải`.
   * Callout value: **`35 pt` Bold** (hiển thị `19.17K`). Nền `#F0FDF4` (Pastel Green), Bo góc `10 px`.
4. **Card 4 (Tổng Điểm Sát Thương Tấn Công G+A):** `X = 1445 px`.
   * Kéo thước đo **`[Measures].[Goal Contributions]`**. Đổi tên: `Tổng Đóng Góp G+A`.
   * Callout value: **`35 pt` Bold** (hiển thị `33.91K`). Nền `#FFFBEB` (Pastel Amber), Bo góc `10 px`.

---

### Bước 4: Thiết lập Khối 4 Bộ lọc Slicers Mới 100%
Tại hàng `Y = 210 px`, `Height = 75 px`, tạo 4 bộ lọc rộng rãi `Width = 455 px`:

1. **Slicer 1 (Mùa giải):** `X = 20 px`, kéo `DIM Time [Season]`, Style `Dropdown`.
2. **Slicer 2 (Phân loại Cúp / Giải - MỚI):** `X = 495 px`, kéo `DIM Competition [Competition Type]`, Style `Dropdown` (Lọc xem Cúp Châu lục `international_cup` hay Giải Quốc nội `domestic_league`).
3. **Slicer 3 (Quốc gia giải đấu - MỚI):** `X = 970 px`, kéo `DIM Competition [Country Name]`, Style `Dropdown` (Lọc theo England, Spain, Germany, Italy, France...).
4. **Slicer 4 (Quý thi đấu - MỚI):** `X = 1445 px`, kéo `DIM Time [Quarter]`, Style `Tile` hoặc `Dropdown` (Lọc theo Q1, Q2, Q3, Q4).

---

### Bước 5: Visual 1 (Bên Trái) – Ma trận Phân nhóm Cấu trúc Giải đấu & Tăng trưởng

Bảng phân nhóm và tổng hợp toàn bộ hỏa lực theo cơ cấu giải đấu và đo lường nhịp độ tăng trưởng theo Quý:

#### 1. Cấu hình trường dữ liệu:
* Chọn visual **Matrix** (Ma trận).
* Thẻ **General** $\rightarrow$ **Properties**: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
* **Rows (Phân nhóm 3 cấp):**
  1. `DIM Competition` $\rightarrow$ **`[Competition Type]`** (Cấp 1: Loại giải - *domestic_league vs international_cup*).
  2. `DIM Competition` $\rightarrow$ **`[Country Name]`** (Cấp 2: Quốc gia giải đấu).
  3. `DIM Competition` $\rightarrow$ **`[Competition Name]`** (Cấp 3: Tên giải đấu cụ thể).
* **Values (Các thước đo tổng hợp):**
  1. `[Measures].[Distinct Matches Played]` (Số trận tổ chức).
  2. `[Measures].[Goals]` (Số bàn thắng ghi được).
  3. `[Measures].[QoQ Goals Growth]` (Tốc độ tăng trưởng bàn thắng theo Quý QoQ - hiển thị định dạng %).
  4. `[Measures].[Assists]` (Pha kiến tạo).
  5. `[Measures].[Goal Contributions]` (Tổng G+A).

#### 2. Kích hoạt Grouping & Totals:
* Tab **Format visual** $\rightarrow$ mục **Subtotals**:
  * Gạt công tắc **Row subtotals sang ON**!
  * Định dạng dòng Subtotal: Chữ in đậm (**Bold**), màu nền xám nhạt `#E2E8F0`.
  * *Ý nghĩa:* Dòng Subtotal cấp Loại giải cho biết toàn bộ Cúp Châu Âu ghi bao nhiêu bàn; Dòng Subtotal quốc gia cho biết bóng đá Anh/Tây Ban Nha nổ bao nhiêu bàn.
* Mục **Grand total**: Gạt **Row grand total sang ON**!
* **Bố cục hiển thị:**
  * Nhấp chọn Matrix $\rightarrow$ vào **Row headers** $\rightarrow$ **Options** $\rightarrow$ bật **Stepped layout: ON** (dạng cây có nút gập mở `+ / -` cực kỳ gọn gàng).

#### 3. Bật thanh dữ liệu Data Bars:
* Vào tab **Format visual** $\rightarrow$ **Cell elements**:
  * Chọn series `Goal Contributions`, bật **Data bars: ON**, chọn màu xanh `#2563EB`.

#### 4. Đổi tên cột & Định dạng hiển thị:
* Title: Bật **On**, nhập `Báo cáo Phân nhóm Cấu trúc Giải đấu & Tăng trưởng Bàn thắng (Tournament Hierarchy)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* Đổi tên nhãn: `Competition Type` $\rightarrow$ `Loại giải`, `Country Name` $\rightarrow$ `Quốc gia`, `Competition Name` $\rightarrow$ `Giải đấu`, `QoQ Goals Growth` $\rightarrow$ `Tăng trưởng QoQ`.
* Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Bên Phải) – Ma trận Phân nhóm Hiệu suất Tấn công theo Huấn Luyện Viên Trưởng

Bảng phân nhóm và tổng hợp sản lượng tấn công dưới triết lý của từng Thuyền trưởng đại tài:

#### 1. Cấu hình trường dữ liệu:
* Chọn visual **Matrix** (Ma trận).
* Thẻ **General** $\rightarrow$ **Properties**: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
* **Rows (Phân nhóm 3 cấp):**
  1. `DIM Club` $\rightarrow$ **`[Coach Name]`** (Cấp 1: Huấn luyện viên trưởng - *Pep Guardiola, Xabi Alonso, Mikel Arteta, Carlo Ancelotti, Luis Enrique, Arne Slot...*).
  2. `DIM Club` $\rightarrow$ **`[Club Name]`** (Cấp 2: Câu lạc bộ dẫn dắt).
  3. `DIM Player` $\rightarrow$ **`[Player Name]`** (Cấp 3: Cầu thủ / Học trò ghi bàn).
* **Values (Các thước đo tổng hợp):**
  1. `[Measures].[Goals]` (Số bàn thắng).
  2. `[Measures].[Assists]` (Số pha kiến tạo).
  3. `[Measures].[Goal Contributions]` (Tổng G+A).
  4. `[Measures].[Distinct Matches Played]` (Số trận cầm quân).

#### 2. Kích hoạt Grouping & Totals:
* Tab **Format visual** $\rightarrow$ mục **Subtotals**:
  * Gạt công tắc **Row subtotals sang ON**!
  * *Ý nghĩa:* Dòng Subtotal cấp HLV cho biết chính xác tổng số bàn thắng, kiến tạo mà HLV đó đem lại (ví dụ: *Pep Guardiola mang về 245 bàn, 190 kiến tạo $\rightarrow$ 435 G+A sau 99 trận*).
* Mục **Grand total**: Gạt **Row grand total sang ON**!
* **Bố cục hiển thị:** Bật **Stepped layout: ON** (có nút `+ / -` cho phép người dùng bấm bung mở từng HLV để xem danh sách học trò).

#### 3. Bật thanh dữ liệu Data Bars:
* Vào tab **Format visual** $\rightarrow$ **Cell elements**:
  * Chọn series `Goal Contributions`, bật **Data bars: ON**, chọn màu xanh dương `#2563EB`.

#### 4. Đổi tên cột & Định dạng hiển thị:
* Title: Bật **On**, nhập `Báo cáo Phân nhóm Hiệu suất Tấn công theo Huấn Luyện Viên Trưởng (Head Coach Analytics)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* Đổi tên nhãn: `Coach Name` $\rightarrow$ `Huấn luyện viên`, `Club Name` $\rightarrow$ `Câu lạc bộ`, `Player Name` $\rightarrow$ `Cầu thủ / Học trò`.
* Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo Đạt Điểm Tuyệt đối

1. **Chuẩn mực Grouping & Totals 100%:**
   * Cả 2 visual ma trận đều là bảng phân nhóm đa tầng có tính năng gập mở `+ / -`, có đầy đủ các dòng **Subtotals** in đậm rõ ràng và dòng **Grand Total** ở đáy trang.
2. **Kịch bản Thuyết trình Tương tác Chéo ấn tượng:**
   * Khi giảng viên nhấp vào giải đấu `Premier League` ở Bảng 1 $\rightarrow$ Bảng 2 tự động lọc ra toàn bộ các Huấn luyện viên đang cầm quân tại Ngoại Hạng Anh (*Pep Guardiola, Mikel Arteta, Jürgen Klopp, Unai Emery...*) cùng thành tích và dàn học trò của họ.
   * Khi nhấp vào `international_cup` (Cúp Châu Âu) ở Bảng 1 $\rightarrow$ Bảng 2 lọc ra các HLV có hỏa lực mạnh nhất tại đấu trường Champions League.
3. **Tuyệt đối không trùng lặp:** Khai thác toàn diện các góc nhìn mới về cấu trúc giải đấu (`Competition Type`, `Country Name`, `QoQ Growth`) và nhà cầm quân (`Coach Name`, `Total Coaches = 175`).
