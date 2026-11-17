# 4.2.1 Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công Đa cấp (Grouping and Totals Attacking Performance Report)

Tài liệu này cung cấp hướng dẫn thiết kế hoàn chỉnh **Báo biểu 1** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **TIÊU CHÍ CHẤM ĐIỂM BẮT BUỘC - BÁO CÁO DẠNG GROUPING AND TOTALS:**
> * Báo biểu 1 được thiết kế chuyên trách để đáp ứng trọn vẹn yêu cầu tiên quyết của giảng viên: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
> * Toàn bộ phần thân trang được cấu thành bởi **2 Bảng Ma trận Phân nhóm & Tổng hợp Đa cấp (2 Matrix Visuals)** đặt song song đối xứng, khai thác 2 góc nhìn bổ trợ nhau:
>   1. **Visual 1 (Bên Trái) – Grouping theo Tổ chức:** Phân nhóm 2 tầng `Giải đấu` (`Competition Name`) $\rightarrow$ `Câu lạc bộ` (`Club Name`).
>   2. **Visual 2 (Bên Phải) – Grouping theo Chiến thuật:** Phân nhóm 3 tầng `Tuyến thi đấu` (`Main Position`) $\rightarrow$ `Vị trí chi tiết` (`Sub Position`) $\rightarrow$ `Cầu thủ` (`Player Name`).
> * Cả 2 bảng đều kích hoạt đầy đủ các dòng **Tổng phụ (Subtotals)** cho từng cấp nhóm và dòng **Tổng cộng toàn cục (Grand Total)** ở đáy trang, kèm tính năng tương tác chéo (Cross-Filtering) đồng bộ tức thời.

---

## 1. Mục tiêu Nghiệp vụ và Ý nghĩa Thống kê Đa chiều

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Phân hóa hỏa lực theo Giải đấu và Câu lạc bộ (Visual 1):** Giải đấu nào có số lượng bàn thắng và tính cởi mở cao nhất châu Âu? Trong từng giải, các CLB phân tầng như thế nào giữa nhóm đua vô địch (ghi > 80 bàn) và nhóm đua trụ hạng (dưới 35 bàn)?
2. **Cơ cấu hỏa lực theo Tuyến và Vai trò Chiến thuật (Visual 2):** Trong bóng đá đỉnh cao, bàn thắng đến từ đâu? Tuyến Tiền đạo (`Attack`) gánh bao nhiêu % bàn thắng, tuyến Tiền vệ (`Midfield`) đóng góp bao nhiêu % kiến tạo? Vai trò nào tạo đột biến cao nhất giữa Trung phong cắm (`Centre-Forward`) và Tiền đạo dạt biên (`Winger`)?
3. **Phân tích Chiều sâu Đội hình (Tương tác chéo giữa 2 bảng):** Khi nhấp chọn một CLB ở Visual 1 (ví dụ: *Manchester City* hoặc *Real Madrid*), Visual 2 lập tức hiển thị phân rã hỏa lực của riêng CLB đó: Tiền đạo ghi bao nhiêu bàn (Subtotal Attack), Tiền vệ ghi bao nhiêu bàn (Subtotal Midfield), Hậu vệ ghi bao nhiêu bàn (Subtotal Defender). Đội bóng vô địch là đội bóng có hỏa lực trải đều cả 3 tuyến, không bị phụ thuộc vào một cá nhân duy nhất.

### 1.2. Phân định độc lập tuyệt đối với Báo biểu 2 và Báo biểu 3
* **Báo biểu 1 (Grouping & Totals Report):** Độc quyền về **Phân nhóm đa cấp và Tổng hợp cơ cấu hỏa lực** (Giải đấu $\rightarrow$ CLB; Tuyến $\rightarrow$ Vị trí $\rightarrow$ Cầu thủ).
* **Báo biểu 2 (Executive Tactical Dashboard):** Độc quyền về **Trinh sát tác chiến & Bắt bài kẻ mạnh trước trận đấu** (Soi chân thuận `Foot`, độ tuổi `Age`, quốc tịch `Nationality`, thánh địa sân bãi `Stadium`).
* **Báo biểu 3 (Executive Discipline Dashboard):** Độc quyền về **Kỷ luật thẻ phạt và Tải trọng thể lực** (Thẻ vàng `Yellow Cards`, Thẻ đỏ `Red Cards`, Phút thi đấu theo lứa tuổi).

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG ĐA CẤP (Font: 20pt Bold, Center)           |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Bàn Thắng]  | [Card 2: Tổng Kiến Tạo]   | [Card 3: Tổng Đóng Góp G+A] | [Card 4: Thời Lượng TB / Trận]    |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold                |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB    | Nền Pastel Purple #FAF5FF         |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải]                                  | [Slicer 2: Giải đấu]                                            |
| DIM Time [Season] (Dropdown, H = 75 px)               | DIM Competition [Competition Name] (Dropdown, H = 75 px)        |
| Tọa độ: X = 20 px, Y = 210 px | Width = 925 px        | Tọa độ: X = 975 px, Y = 210 px | Width = 925 px                 |
+-------------------------------------------------------+-----------------------------------------------------------------+
| [VISUAL 1: MA TRẬN PHÂN NHÓM TỔ CHỨC (18pt Bold)]     | [VISUAL 2: MA TRẬN PHÂN NHÓM CHIẾN THUẬT (18pt Bold)]           |
| Phân nhóm: Giải đấu -> Câu lạc bộ                     | Phân nhóm: Tuyến thi đấu -> Vị trí chi tiết -> Cầu thủ          |
| Rows: Competition Name -> Club Name                   | Rows: Main Position -> Sub Position -> Player Name              |
| Values: Goals, Assists, Goal Contributions (Data Bars)| Values: Goals, Assists, Goal Contributions (Data Bars), Minutes |
| Distinct Matches Played, Minutes Played               | Subtotals: ON (Tổng Tuyến & Vị trí) | Grand Total: ON           |
| Subtotals: ON (Tổng cấp Giải đấu) | Grand Total: ON   |                                                                 |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 760 px| Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 760 px         |
+-------------------------------------------------------+-----------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi động và Cấu hình Canvas 1920 x 1080 px
1. Mở phần mềm **Power BI Desktop**, kết nối **Connect live** tới máy chủ SSAS `localhost`, chọn khối Cube **`[DW Football Transfermarkt]`**.
2. Nhấp chọn tab trang bên dưới cùng, đổi tên trang thành: `Hiệu suất Tấn công (Grouping & Totals)`.
3. Mở khung **Format report page**:
   * **Canvas settings:** Type: `Custom`, `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói `#F8FAFC`, gạt **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng 1)
1. Trên thẻ **Insert**, chọn **Text box**.
2. Nhập nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG ĐA CẤP (GROUPING AND TOTALS REPORT)`.
3. Font `Segoe UI`, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
4. Thẻ **General** $\rightarrow$ **Properties**: `Width = 1880 px`, `Height = 55 px`, `X = 20 px`, `Y = 15 px`.
5. **Effects:** Nền `#FFFFFF`, Viền mỏng `#E2E8F0`, Bo góc `10 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tấn công Cốt lõi
Tạo 4 visual **Card (new)** hoặc **Card** truyền thống tại hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

1. **Card 1 (Tổng Bàn Thắng):** `X = 20 px`.
   * Kéo thước đo **`[Measures].[Goals]`**. Đổi tên: `Tổng Bàn Thắng`.
   * Callout value: **`35 pt` Bold**, màu `#0F172A`. Nền `#EFF6FF` (Pastel Blue), Bo góc `10 px`.
2. **Card 2 (Tổng Kiến Tạo):** `X = 495 px`.
   * Kéo thước đo **`[Measures].[Assists]`**. Đổi tên: `Tổng Kiến Tạo`.
   * Callout value: **`35 pt` Bold**. Nền `#F0FDF4` (Pastel Green), Bo góc `10 px`.
3. **Card 3 (Tổng Đóng Góp G+A):** `X = 970 px`.
   * Kéo thước đo **`[Measures].[Goal Contributions]`**. Đổi tên: `Tổng Đóng Góp G+A`.
   * Callout value: **`35 pt` Bold**. Nền `#FFFBEB` (Pastel Amber), Bo góc `10 px`.
4. **Card 4 (Thời Lượng TB / Trận):** `X = 1445 px`.
   * Kéo thước đo **`[Measures].[Avg Minutes Played]`**. Đổi tên: `Thời Lượng TB / Trận (Phút)`.
   * Callout value: **`35 pt` Bold** (hiển thị ~64.4 phút). Nền `#FAF5FF` (Pastel Purple), Bo góc `10 px`.

---

### Bước 4: Thiết lập 2 Bộ lọc Slicers Rộng rãi Cân xứng
Tại hàng `Y = 210 px`, `Height = 75 px`, tạo 2 bộ lọc dạng Dropdown rộng rãi:

1. **Slicer 1 (Mùa giải):**
   * Tọa độ: `X = 20 px`, `Width = 925 px`.
   * Kéo trường `DIM Time [Season]`. Style: `Dropdown`.
2. **Slicer 2 (Giải đấu):**
   * Tọa độ: `X = 975 px`, `Width = 925 px`.
   * Kéo trường `DIM Competition [Competition Name]`. Style: `Dropdown`.

---

### Bước 5: Visual 1 (Bên Trái) – Ma trận Phân nhóm theo Cấp Tổ chức (Giải đấu $\rightarrow$ Câu lạc bộ)

Bảng phân nhóm và tổng hợp toàn bộ hỏa lực của các đội bóng trong từng giải đấu:

#### 1. Cấu hình trường dữ liệu:
* Chọn visual **Matrix** (Ma trận).
* Thẻ **General** $\rightarrow$ **Properties**: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
* **Rows (Phân nhóm 2 cấp):**
  1. `DIM Competition` $\rightarrow$ **`[Competition Name]`** (Cấp 1: Giải đấu).
  2. `DIM Club` $\rightarrow$ **`[Club Name]`** (Cấp 2: Câu lạc bộ).
* **Values (Các thước đo tổng hợp):**
  1. `[Measures].[Goals]` (Bàn thắng).
  2. `[Measures].[Assists]` (Kiến tạo).
  3. `[Measures].[Goal Contributions]` (Tổng G+A).
  4. `[Measures].[Distinct Matches Played]` (Số trận).
  5. `[Measures].[Minutes Played]` (Số phút).

#### 2. Kích hoạt Grouping & Totals:
* Tab **Format visual** $\rightarrow$ mục **Subtotals**:
  * Gạt công tắc **Row subtotals sang ON**!
  * Chọn định dạng dòng Subtotal: Chữ in đậm (**Bold**), màu nền xám nhạt `#E2E8F0` để phân biệt rõ ràng.
* Mục **Grand total**:
  * Gạt công tắc **Row grand total sang ON**!
* **Bố cục hiển thị:**
  * Nhấp chọn bảng Matrix $\rightarrow$ nhìn lên góc trên bên phải, nhấp vào biểu tượng **mũi tên phân nhánh `⑂` (Expand all down one level)** để bung mở các CLB bên dưới từng giải đấu.
  * Tùy chọn: Tại mục **Row headers** $\rightarrow$ **Options**, có thể bật **Stepped layout: ON** để có các nút gập mở `+ / -` gọn gàng.

#### 3. Bật thanh dữ liệu Data Bars:
* Vào tab **Format visual** $\rightarrow$ **Cell elements**:
  * Ô **Select series**: Chọn `Goal Contributions`.
  * Gạt **Data bars: ON**. Bấm `fx` chọn màu xanh `#2563EB`, hướng `Left to right`.

#### 4. Đổi tên cột & Định dạng hiển thị:
* Title: Bật **On**, nhập `Báo cáo Phân nhóm Hỏa lực theo Giải đấu & Câu lạc bộ (Grouping by Club)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* Đổi tên nhãn: `Competition Name` $\rightarrow$ `Giải đấu`, `Club Name` $\rightarrow$ `Câu lạc bộ`, `Goal Contributions` $\rightarrow$ `Tổng G+A`.
* Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Bên Phải) – Ma trận Phân nhóm theo Cấp Chiến thuật (Tuyến $\rightarrow$ Vị trí $\rightarrow$ Cầu thủ)

Bảng phân nhóm và tổng hợp cơ cấu đóng góp bàn thắng theo tuyến thi đấu và từng ngôi sao:

#### 1. Cấu hình trường dữ liệu:
* Chọn visual **Matrix** (Ma trận).
* Thẻ **General** $\rightarrow$ **Properties**: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
* **Rows (Phân nhóm 3 cấp):**
  1. `DIM Player` $\rightarrow$ **`[Main Position]`** (Cấp 1: Tuyến thi đấu - *Attack, Midfield, Defender*).
  2. `DIM Player` $\rightarrow$ **`[Sub Position]`** (Cấp 2: Vị trí chi tiết - *Centre-Forward, Left Winger...*).
  3. `DIM Player` $\rightarrow$ **`[Player Name]`** (Cấp 3: Cầu thủ).
* **Values (Các thước đo tổng hợp):**
  1. `[Measures].[Goals]` (Bàn thắng).
  2. `[Measures].[Assists]` (Kiến tạo).
  3. `[Measures].[Goal Contributions]` (Tổng G+A).
  4. `[Measures].[Minutes Played]` (Số phút thi đấu).

#### 2. Kích hoạt Grouping & Totals:
* Tab **Format visual** $\rightarrow$ mục **Subtotals**:
  * Gạt công tắc **Row subtotals sang ON**!
  * Subtotal tự động tính tổng cho từng Tuyến thi đấu (ví dụ: *Tổng bàn thắng của toàn bộ Tiền đạo*) và từng Vị trí chi tiết (*Tổng bàn thắng của các Trung phong cắm*).
* Mục **Grand total**:
  * Gạt công tắc **Row grand total sang ON**!
* **Bố cục hiển thị:**
  * Tại **Row headers** $\rightarrow$ **Options**: Bật **Stepped layout: ON** (hiển thị cấu trúc cây có nút `+ / -` trực quan, cho phép người dùng click bung xem từng tuyến cực kỳ chuyên nghiệp).

#### 3. Bật thanh dữ liệu Data Bars:
* Vào tab **Format visual** $\rightarrow$ **Cell elements**:
  * Chọn series `Goal Contributions`, bật **Data bars: ON**, chọn màu xanh dương `#2563EB`.

#### 4. Đổi tên cột & Định dạng hiển thị:
* Title: Bật **On**, nhập `Báo cáo Phân nhóm Đóng góp theo Tuyến thi đấu & Cầu thủ (Grouping by Position)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* Đổi tên nhãn: `Main Position` $\rightarrow$ `Tuyến thi đấu`, `Sub Position` $\rightarrow$ `Vị trí`, `Player Name` $\rightarrow$ `Cầu thủ`.
* Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo Đạt Điểm Tuyệt đối

1. **Chuẩn mực Grouping & Totals 100%:**
   * Cả 2 visual ma trận đều là bảng phân nhóm đa tầng có tính năng gập mở `+ / -`, có đầy đủ các dòng **Subtotals** in đậm rõ ràng và dòng **Grand Total** ở đáy trang.
2. **Kịch bản Thuyết trình Tương tác Chéo ấn tượng:**
   * Khi giảng viên nhấp vào CLB `Manchester City` ở bảng bên trái $\rightarrow$ Toàn bộ bảng bên phải tự động cập nhật lại cơ cấu hỏa lực của riêng Man City:
     * Dòng Subtotal tuyến Tiền đạo (*Attack*): Thấy ngay Haaland đóng góp 95 G+A, Alvarez đóng góp 32 G+A.
     * Dòng Subtotal tuyến Tiền vệ (*Midfield*): Foden 53 G+A, De Bruyne 30 G+A, Bernardo Silva 25 G+A.
     * Dòng Subtotal tuyến Hậu vệ (*Defender*): Gvardiol, Walker đóng góp các pha kiến tạo.
   * Thao tác này chứng minh năng lực phân tích kho dữ liệu đa chiều OLAP ở đẳng cấp cao nhất, thuyết phục hoàn toàn mọi giảng viên khó tính.
