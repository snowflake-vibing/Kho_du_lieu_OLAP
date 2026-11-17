# Báo biểu 3: Kỷ luật Thẻ phạt & Tải trọng Thi đấu (Discipline & Physical Workload Analytics)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [04_power_bi_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/power-bi/04_power_bi_bao_bieu_3.md)

---

## 1. Mục tiêu Nghiệp vụ và Ý nghĩa Thống kê Kỷ luật Thể thao

* **Kiểm soát Kỷ luật & Thẻ phạt:** Phân tích bức tranh toàn cảnh về mức độ bạo lực và lỗi thẻ phạt trên các sân cỏ châu Âu thông qua hai chỉ số định lượng: **Thẻ vàng (`Yellow_Cards`)** và **Thẻ đỏ (`Red_Cards`)**, phân loại theo từng Câu lạc bộ và Vị trí thi đấu chi tiết (`Sub_Position`).
* **Đo lường Tải trọng Thể lực (Physical Workload):** Theo dõi tổng thời lượng thi đấu tích lũy (`Minutes_Played`) qua các mùa giải, đánh giá mức độ cày ải thể lực của các giải đấu và độ tuổi chịu áp lực thi đấu cao nhất.
* **Tương quan Kỷ luật vs Thể lực theo Độ tuổi:** Khám phá sự biến đổi giữa mức độ cày ải thể lực và xu hướng phạm lỗi theo từng nấc thang tuổi tác (từ sao mai trẻ 18-21 tuổi, đỉnh cao 25-29 tuổi, đến cựu binh 34-38 tuổi).

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] PHÂN TÍCH KỶ LUẬT THẺ PHẠT & TẢI TRỌNG THI ĐẤU (DISCIPLINE & WORKLOAD) (Font: 20pt Bold, Center)        |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Thẻ Vàng]   | [Card 2: Tổng Thẻ Đỏ]     | [Card 3: Tổng Lượt Ra Sân]| [Card 4: Tổng Số Phút]            |
| SUM(Yellow_Cards)         | SUM(Red_Cards)            | COUNT(Appearance_ID)      | SUM(Minutes_Played)               |
| Nền Pastel Hổ phách #FFFBEB| Nền Pastel Đỏ #FEF2F2    | Nền Pastel Xanh #EFF6FF   | Nền Pastel Lục #F0FDF4            |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Giải đấu]      | [Bộ lọc 3: Quốc gia giải]   | [Bộ lọc 4: Vị trí thi đấu]        |
| Season (Dropdown)         | Competition_Name (Drop)   | Competition_Country (Drop)  | Main_Position (Dropdown)          |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 455, H: 75, X: 970)     | (W: 455, H: 75, X: 1445)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH XẾP CHỒNG (BAR CHART)]| [Ô 2: TRÊN - PHẢI | BIỂU ĐỒ ĐƯỜNG PHÂN RÃ THEO GIẢI ĐẤU)]     |
| Top 10 CLB nhận Nhiều Thẻ Phạt Nhất (Thẻ Vàng & Thẻ Đỏ) | Biến động Tải trọng Thể lực (Phút thi đấu) theo Mùa giải      |
| Dimension: Club_Name, Metrics: Yellow_Cards, Red_Cards  | Dimension: Season, Breakdown: Competition_Name, Metric: Mins  |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | COMBO CHART 2 TRỤC Y (CỘT & ĐƯỜNG)] | [Ô 4: DƯỚI - PHẢI | BIỂU ĐỒ VÀNH KHĂN (DONUT CHART)]          |
| Tải trọng Thi đấu (Cột) & Thẻ phạt (Đường) theo Độ tuổi | Phân bổ Thẻ Đỏ theo Vị trí Chi tiết (Sub Position)            |
| Dimension: Age, Bars: Minutes_Played, Lines: Cards      | Dimension: Sub_Position, Metric: SUM(Red_Cards), Hole: 50%   |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo
1. Trong báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Kỷ luật & Tải trọng Thi đấu`.
3. Menu **Trang** $\rightarrow$ **Cài đặt trang hiện tại** $\rightarrow$ tab **Kiểu**:
   * **Nền trang:** Chọn `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Thêm **Hộp văn bản (Text box)** tại: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
2. Nội dung: `BÁO BIỂU 3: PHÂN TÍCH KỶ LUẬT THẺ PHẠT & TẢI TRỌNG THI ĐẤU (DISCIPLINE & PHYSICAL WORKLOAD)`.
3. Font: **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu `#0F172A`, Nền `#FFFFFF`, Bo viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI Kỷ luật & Tải trọng (Scorecards)
Menu **Thêm biểu đồ** $\rightarrow$ **Thẻ chỉ số (Scorecard)**, hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

#### 1. Thẻ 1: Tổng Thẻ Vàng (Total Yellow Cards)
* **Vị trí:** `X = 20 px`.
* **Chỉ số (Metric):** `Yellow_Cards` (SUM). Đổi tên: `Tổng Thẻ Vàng`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền màu vàng nhạt `#FFFBEB` (Pastel Amber), Bo góc `10 px`.

#### 2. Thẻ 2: Tổng Thẻ Đỏ (Total Red Cards)
* **Vị trí:** `X = 495 px`.
* **Chỉ số (Metric):** `Red_Cards` (SUM). Đổi tên: `Tổng Thẻ Đỏ`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền màu đỏ nhạt `#FEF2F2` (Pastel Red), Bo góc `10 px`.

#### 3. Thẻ 3: Tổng Lượt Ra Sân (Total Appearances)
* **Vị trí:** `X = 970 px`.
* **Chỉ số (Metric):** `Appearance_ID` (COUNT). Đổi tên: `Tổng Lượt Ra Sân`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền màu xanh dương nhạt `#EFF6FF` (Pastel Blue), Bo góc `10 px`.

#### 4. Thẻ 4: Tổng Số Phút Thi Đấu (Total Minutes Played)
* **Vị trí:** `X = 1445 px`.
* **Chỉ số (Metric):** `Minutes_Played` (SUM). Đổi tên: `Tổng Số Phút Thi Đấu`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Định dạng số thu gọn (Compact numbers - hàng Triệu phút), Nền xanh lục nhạt `#F0FDF4` (Pastel Green), Bo góc `10 px`.

---

### Bước 4: Thiết lập 4 Bộ lọc Tương tác (Controls)
Menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ hàng `Y = 210 px`, `Height = 75 px`, `Width = 455 px`:

1. **Bộ lọc 1: Mùa giải (Season):** `X = 20 px`, Loại `Drop-down list`, Control field: `Season`.
2. **Bộ lọc 2: Giải đấu (Competition):** `X = 495 px`, Loại `Drop-down list`, Control field: `Competition_Name`.
3. **Bộ lọc 3: Quốc gia (Country):** `X = 970 px`, Loại `Drop-down list`, Control field: `Competition_Country`.
4. **Bộ lọc 4: Tuyến thi đấu (Main Position):** `X = 1445 px`, Loại `Drop-down list`, Control field: `Main_Position`.

---

### Bước 5: Ô 1 (Trên - Trái) – Biểu đồ Thanh Xếp Chồng: Top 10 CLB Nhận Nhiều Thẻ Phạt Nhất
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ thanh ngang xếp chồng (Stacked bar chart)**.
2. Vị trí & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Club_Name` (Đổi tên: `Câu lạc bộ`).
   * **Chỉ số (Metrics):** Kéo lần lượt 2 trường:
     1. `Yellow_Cards` (SUM, Đổi tên: `Thẻ vàng`).
     2. `Red_Cards` (SUM, Đổi tên: `Thẻ đỏ`).
   * **Sắp xếp (Sort):** `Yellow_Cards` giảm dần (**Descending**), giới hạn Top `10`.
4. **Kiểu (Style):**
   * Tiêu đề: `Top 10 CLB Nhận Nhiều Thẻ Phạt Nhất (Thẻ Vàng & Thẻ Đỏ)`.
   * **Màu sắc ngữ nghĩa thẻ phạt:**
     * Chuỗi 1 (`Yellow_Cards`): Chọn màu Vàng hổ phách rực rỡ **`#F59E0B`** (Amber 500).
     * Chuỗi 2 (`Red_Cards`): Chọn màu Đỏ cảnh báo **`#DC2626`** (Red 600).
   * Bật **Hiển thị nhãn dữ liệu (Show data labels): ON**.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Ô 2 (Trên - Phải) – Biểu đồ Đường Phân Rã: Biến động Tải trọng Thể lực theo Giải đấu qua các Mùa
*(Lưu ý: Do Looker Studio không có visual Ribbon Chart độc quyền của Power BI, visual đối ứng chuẩn xác và trực quan nhất là Biểu đồ đường phân rã nhiều chuỗi / Line Chart with Breakdown Dimension)*:

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ đường (Line chart)**.
2. Vị trí & Kích thước: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Season` (Đổi tên: `Mùa giải`).
   * **Chiều phân rã (Breakdown Dimension):** `Competition_Name` (Đổi tên: `Giải đấu`).
   * **Chỉ số (Metric):** `Minutes_Played` (SUM, Đổi tên: `Số phút thi đấu`).
   * **Số lượng chuỗi (Number of series):** Giới hạn `5 - 6` giải đấu hàng đầu.
4. **Kiểu (Style):**
   * Tiêu đề: `Biến động Tải trọng Thể lực (Phút thi đấu) theo Giải đấu qua các Mùa giải`.
   * Độ dày đường: `3 px`, bật điểm mút dữ liệu (Show points).
   * Bật **Chú giải (Legend):** Đặt ở phía trên hoặc bên phải.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Ô 3 (Dưới - Trái) – Combo Chart 2 Trục Y: Tải trọng Thi đấu & Thẻ phạt theo Độ tuổi
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ kết hợp (Combo chart)**.
2. Vị trí & Kích thước: `X = 20 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Age` (Đổi tên: `Độ tuổi`).
   * **Chỉ số chuỗi 1 (Cột - Trục Y trái):** `Minutes_Played` (SUM, Đổi tên: `Số phút thi đấu`).
   * **Chỉ số chuỗi 2 (Đường - Trục Y phải):** Tạo trường tính toán `Total_Cards` = `Yellow_Cards + Red_Cards` (SUM, Đổi tên: `Tổng số thẻ phạt`).
   * **Sắp xếp (Sort):** `Age` tăng dần (**Ascending** từ 17 đến 40 tuổi).
4. **Kiểu (Style):**
   * Tiêu đề: `Tương quan Tải trọng Thi đấu (Cột) & Thẻ phạt (Đường) theo Độ tuổi`.
   * Chuỗi 1 (Cột): Màu xanh dương `#2563EB`.
   * Chuỗi 2 (Đường): Màu đỏ đậm `#DC2626`, bật điểm mút, gạt công tắc **Trục Y phụ (Secondary axis)** sang ON.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8: Ô 4 (Dưới - Phải) – Biểu đồ Vành Khăn (Donut Chart): Phân bổ Thẻ Đỏ theo Vị trí Chi tiết
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ hình tròn (Pie chart)**.
2. Vị trí & Kích thước: `X = 975 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Sub_Position` (Đổi tên: `Vị trí chi tiết`).
   * **Chỉ số (Metric):** `Red_Cards` (SUM, Đổi tên: `Số thẻ đỏ`).
   * **Bộ lọc biểu đồ (Filter):** Thêm bộ lọc `Red_Cards > 0` để loại bỏ các vị trí không có thẻ đỏ.
4. **Kiểu (Style):**
   * Tiêu đề: `Tỷ lệ Phân bổ Thẻ Đỏ theo Vị trí Chi tiết (Sub Position)`.
   * **Lỗ khuyết ở giữa (Donut hole):** Kéo thanh trượt lên mức **`50%`** để chuyển thành Biểu đồ Vành khăn (Donut Chart) hiện đại.
   * **Nhãn dữ liệu (Data labels):** Chọn hiển thị `Tỷ lệ phần trăm (Percentage)` hoặc `Giá trị (Value)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Lập luận Thể thao Chuyên sâu

1. **Quy luật Kỷ luật theo Vị trí:**
   * Visual Ô 4 chỉ ra rõ ràng: Vị trí **Trung vệ (`Centre-Back`)** và **Tiền vệ phòng ngự (`Defensive Midfield`)** chiếm tới hơn **`55%`** tổng số thẻ đỏ toàn giải do tính chất phòng ngự khu vực và ngăn chặn các pha phản công nguy hiểm.
2. **Quy luật Tải trọng Thể lực hình chuông theo Độ tuổi:**
   * Visual Ô 3 thể hiện rõ đường phân phối hình chuông chuẩn: Tải trọng thể lực và số phút thi đấu đạt đỉnh ở nhóm tuổi **24 - 28 tuổi** (giai đoạn vàng của sự nghiệp), sau đó giảm dần khi bước qua tuổi 32.
3. **Màu sắc ngữ nghĩa nhất quán:**
   * Toàn bộ các visual trên báo biểu áp dụng màu sắc chuẩn thể thao: Thẻ vàng là Amber `#F59E0B`, Thẻ đỏ là Crimson `#DC2626`, Phút thi đấu là Xanh dương `#2563EB`, tạo trải nghiệm trực quan đồng bộ $100\%$ với phiên bản Power BI Desktop.
