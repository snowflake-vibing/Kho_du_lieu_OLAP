# Báo biểu 1: Phân tích Hiệu suất Ghi bàn và Đóng góp Kiến tạo (Bao gồm Báo cáo Phân nhóm & Tổng hợp Grouping and Totals)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md)

---

## 1. Mục tiêu Nghiệp vụ và Điểm nhấn Học thuật

* **Đánh giá hiệu suất tấn công:** Phân tích toàn diện hỏa lực của các chân sút hàng đầu châu Âu thông qua 2 biến số then chốt: **Bàn thắng (`Goals`)** và **Kiến tạo (`Assists`)**, đặt trong mối tương quan với thời lượng thi đấu (`Minutes_Played`) và vị trí thi đấu (`Main_Position`).
* **Đạt chuẩn 100% Tiêu chí Đồ án (Grouping and Totals Report):** Báo biểu 1 tích hợp visual **Bảng tổng hợp phân cấp (Pivot Table with Subtotals & Grand Total)** gom nhóm 3 tầng: **`Giải đấu` $\rightarrow$ `Câu lạc bộ` $\rightarrow$ `Cầu thủ`**, tự động tính dòng tổng phụ (**Subtotal**) cho từng CLB, từng giải đấu và dòng tổng cộng (**Grand Total**) ở đáy bảng.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] HIỆU SUẤT GHI BÀN & KIẾN TẠO CỦA CẦU THỦ BÓNG ĐÁ CHÂU ÂU (Font: 20pt Bold, Center)                     |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Bàn Thắng]  | [Card 2: Tổng Kiến Tạo]   | [Card 3: Tổng Đóng Góp G+A] | [Card 4: Thời Lượng TB/Trận]      |
| SUM(Goals)                | SUM(Assists)              | SUM(Goal_Contributions)     | Calculated: Mins/Appearances      |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Giải đấu]      | [Bộ lọc 3: Vị trí thi đấu]                                      |
| Season (Dropdown)         | Competition_Name (Drop)   | Main_Position (Dropdown hoặc Cố định)                           |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 900, H: 75, X: 1000)                                        |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH NGANG (BAR CHART)]    | [Ô 2: TRÊN - PHẢI | MA TRẬN 4 GÓC PHẦN TƯ (SCATTER CHART)]    |
| Top 10 Chân sút ghi bàn nhiều nhất Châu Âu              | Tương quan Assists (Trục X) vs Goals (Trục Y) theo Vị trí     |
| Dimension: Player_Name, Metric: SUM(Goals)              | Kích thước: Minutes_Played, 2 đường tham chiếu trung bình     |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BẢN ĐỒ TỶ TRỌNG (TREEMAP CHART)]    | [Ô 4: DƯỚI - PHẢI | BÁO CÁO PHÂN NHÓM & TỔNG HỢP (PIVOT TABLE)]|
| Bản đồ phân tầng tỷ trọng đóng góp bàn thắng            | Bảng Tổng hợp Đa cấp (Grouping & Totals Report)               |
| Drill-down: Giải đấu -> Vị trí -> CLB                   | Rows: Giải đấu -> CLB -> Cầu thủ                              |
| Metric: SUM(Goal_Contributions)                         | Subtotals: Bật ON | Grand Total: Bật ON                       |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo và Màu nền
1. Mở báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Hiệu suất Ghi bàn & Kiến tạo`.
3. Nhấp menu **Trang (Page)** $\rightarrow$ **Cài đặt trang hiện tại (Current page settings)** $\rightarrow$ tab **Kiểu (Style)**:
   * **Màu nền trang (Page Background):** Chọn `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Trên thanh công cụ, chọn biểu tượng **Hộp văn bản (Text box)**.
2. Vẽ hộp tại tọa độ: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
3. Nhập văn bản: `BÁO BIỂU 1: PHÂN TÍCH HIỆU SUẤT GHI BÀN & KIẾN TẠO CỦA CẦU THỦ BÓNG ĐÁ CHÂU ÂU`.
4. Cấu hình kiểu chữ: Font **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu chữ đen `#0F172A`, Nền `#FFFFFF`, Bo góc viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI (Scorecards)
Chọn menu **Thêm biểu đồ (Add a chart)** $\rightarrow$ chọn **Thẻ chỉ số (Scorecard)**. Tạo 4 thẻ dàn đều ở hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

#### 1. Thẻ 1: Tổng Bàn Thắng (Total Goals)
* **Vị trí:** `X = 20 px`.
* **Chỉ số (Metric):** Kéo trường `Goals`, phép tổng hợp chọn `SUM`. Đổi tên hiển thị: `Tổng Bàn Thắng`.
* **Kiểu (Style):** Cỡ chữ chỉ số **`35 pt` Bold**, Màu chữ `#0F172A`, Màu nền `#EFF6FF` (Pastel Blue), Bo góc viền `10 px`.

#### 2. Thẻ 2: Tổng Kiến Tạo (Total Assists)
* **Vị trí:** `X = 495 px`.
* **Chỉ số (Metric):** Kéo trường `Assists`, phép tổng hợp `SUM`. Đổi tên: `Tổng Kiến Tạo`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#F0FDF4` (Pastel Green), Bo góc `10 px`.

#### 3. Thẻ 3: Tổng Đóng Góp Bàn Thắng (Goal Contributions)
* **Vị trí:** `X = 970 px`.
* **Chỉ số (Metric):** Kéo trường `Goal_Contributions`, phép tổng hợp `SUM`. Đổi tên: `Tổng Đóng Góp G+A`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#FFFBEB` (Pastel Amber), Bo góc `10 px`.

#### 4. Thẻ 4: Thời Lượng Thi Đấu Trung Bình (Avg Minutes Played)
* **Vị trí:** `X = 1445 px`.
* **Tạo trường tính toán (Calculated Field):**
  * Tại khung dữ liệu bên phải, bấm **Thêm trường (Add field)** $\rightarrow$ Đặt tên: `Avg_Minutes_Played`.
  * Công thức: `SUM(Minutes_Played) / COUNT(Appearance_ID)`. Bấm **Lưu (Save)**.
* **Chỉ số (Metric):** Kéo trường `Avg_Minutes_Played` vào thẻ. Đổi tên: `Thời Lượng TB / Trận (Phút)`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#FAF5FF` (Pastel Purple), Bo góc `10 px`.

---

### Bước 4: Thiết lập Hệ thống Bộ lọc Tương tác (Controls)
Chọn menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ Đặt ở hàng `Y = 210 px`, `Height = 75 px`:

1. **Bộ lọc 1: Mùa giải (Season):**
   * Vị trí: `X = 20 px`, `Width = 455 px`.
   * Loại: **Danh sách thả xuống (Drop-down list)**.
   * Trường điều khiển (Control field): `Season`.
2. **Bộ lọc 2: Giải đấu (Competition):**
   * Vị trí: `X = 495 px`, `Width = 455 px`.
   * Loại: **Danh sách thả xuống (Drop-down list)**.
   * Trường điều khiển (Control field): `Competition_Name`.
3. **Bộ lọc 3: Vị trí thi đấu (Position):**
   * Vị trí: `X = 1000 px`, `Width = 900 px`.
   * Loại: **Danh sách thả xuống (Drop-down list)** (hoặc **Danh sách có kích thước cố định**).
   * Trường điều khiển (Control field): `Main_Position`.

---

### Bước 5: Ô 1 (Trên - Trái) – Biểu đồ Thanh Ngang: Top 10 Chân sút ghi bàn nhiều nhất
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ thanh ngang (Bar chart)**.
2. Vị trí & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Player_Name` (Đổi tên: `Cầu thủ`).
   * **Chỉ số (Metric):** `Goals` (SUM, Đổi tên: `Bàn thắng`).
   * **Sắp xếp (Sort):** `Goals` giảm dần (**Descending**).
   * **Số lượng thanh (Number of bars):** Chọn `10` (Top 10).
4. **Kiểu (Style):**
   * Màu thanh: Xanh dương hiện đại `#2563EB`.
   * Bật **Hiển thị nhãn dữ liệu (Show data labels): ON** (Cỡ chữ `11 pt`).
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Ô 2 (Trên - Phải) – Biểu đồ Phân tán (Scatter Chart): Ma trận 4 Góc phần tư Hiệu quả Tấn công
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ phân tán (Scatter chart)**.
2. Vị trí & Kích thước: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Player_Name`.
   * **Chỉ số trục X (X Metric):** `Assists` (SUM, Đổi tên: `Số pha kiến tạo`).
   * **Chỉ số trục Y (Y Metric):** `Goals` (SUM, Đổi tên: `Số bàn thắng`).
   * **Kích thước bong bóng (Size Metric):** `Minutes_Played` (SUM).
   * **Màu sắc theo phương diện (Color by dimension):** `Main_Position`.
4. **Kiểu (Style):**
   * Tiêu đề: `Ma trận 4 Góc phần tư Hiệu quả Tấn công (Goals vs Assists)`.
   * **Đường tham chiếu (Reference Lines):**
     * Thêm Reference Line 1 trên trục X: Kiểu `Giá trị trung bình (Average)` hoặc Hằng số `15`, nét đứt.
     * Thêm Reference Line 2 trên trục Y: Kiểu `Giá trị trung bình (Average)` hoặc Hằng số `20`, nét đứt.
   * *Ý nghĩa chiến thuật:* Phân rã 4 nhóm: Góc I (Siêu sao toàn diện: Salah, Kane), Góc II (Sát thủ vòng cấm: Haaland), Góc III (Nhạc trưởng: De Bruyne), Góc IV (Cầu thủ hỗ trợ).
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Ô 3 (Dưới - Trái) – Biểu đồ Tỷ trọng Treemap: Cơ cấu Đóng góp Bàn thắng Phân cấp Drill-down
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bản đồ cây (Treemap chart)**.
2. Vị trí & Kích thước: `X = 20 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * Bật **Khoan sâu (Drill-down): BẬT (ON)**.
   * **Phương diện phân tầng:** Kéo lần lượt 3 trường:
     1. `Competition_Name` (Cấp 1: Giải đấu).
     2. `Main_Position` (Cấp 2: Vị trí thi đấu).
     3. `Club_Name` (Cấp 3: Câu lạc bộ).
   * **Chỉ số kích thước (Size Metric):** `Goal_Contributions` (SUM).
   * **Chỉ số màu (Color Metric):** `Goals` (SUM).
4. **Kiểu (Style):**
   * Tiêu đề: `Bản đồ Tỷ trọng Đóng góp Bàn thắng Phân cấp (Drill-down)`.
   * Bật nhãn dữ liệu hiển thị rõ tên và giá trị.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8: Ô 4 (Dưới - Phải) – Báo cáo Phân nhóm & Tổng hợp Đa cấp (Grouping and Totals Report)

> [!IMPORTANT]
> **ĐÁP ỨNG TIÊU CHÍ BẮT BUỘC CỦA ĐỒ ÁN:**
> * Đây là thành phần quyết định đáp ứng yêu cầu: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
> * Trong Looker Studio, visual **Bảng tổng hợp (Pivot Table)** được thiết lập gom nhóm 3 cấp: **`Giải đấu` $\rightarrow$ `Câu lạc bộ` $\rightarrow$ `Cầu thủ`**, kích hoạt cả dòng **Tổng phụ (Subtotals)** và dòng **Tổng cộng (Grand Total)**.

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)** (hoặc chọn **Bảng tổng hợp / Pivot Table**).
2. Vị trí & Kích thước: `X = 975 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimension - Grouping):** Kéo lần lượt 3 trường:
     1. `Competition_Name` (Cấp 1: Phân nhóm Giải đấu).
     2. `Club_Name` (Cấp 2: Phân nhóm Câu lạc bộ).
     3. `Player_Name` (Cấp 3: Chi tiết Cầu thủ).
   * **Phương diện cột (Column Dimension):** Để trống.
   * **Chỉ số (Metrics - Totals):** Kéo 4 thước đo:
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
     4. `Minutes_Played` (SUM, Đổi tên: `Số phút`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * Chuyển sang thẻ **Kiểu (Style)** của Pivot Table:
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng số bàn thắng, kiến tạo cho từng CLB và từng Giải đấu).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total / Summary row):** Gạt sang **ON**! (Hiển thị dòng Tổng cộng toàn bộ châu Âu ở đáy bảng).
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng hiển thị là **Thanh (Bar)** hoặc **Bản đồ nhiệt (Heatmap)** màu xanh dương `#2563EB`.
   * **Tiêu đề bảng:** Bật Title: `Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công Đa cấp (Grouping & Totals Report)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Đối soát Dữ liệu

Khi kiểm tra trên Looker Studio, các con số đối soát hoàn toàn khớp $100\%$ với kết quả trên Power BI Desktop và khối Cube SSAS:
* **Tổng Bàn thắng toàn giải:** `19,173` bàn.
* **Tổng Kiến tạo toàn giải:** `14,738` pha kiến tạo.
* **Tổng Đóng góp G+A:** `33,911` lần tạo đột biến.
* **Top 10 chân sút:** Erling Haaland (`81` bàn), Kylian Mbappé (`71` bàn), Robert Lewandowski (`51` bàn), Mohamed Salah (`50` bàn), Mauro Icardi (`50` bàn)...
* Bảng Grouping & Totals Ô 4 hiển thị hoàn hảo cấu trúc cây thư mục, cho phép người dùng nhấp vào từng Giải đấu để xem tổng của giải, mở ra xem tổng từng CLB và chi tiết từng cầu thủ.
