# Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công Đa cấp (Grouping and Totals Attacking Performance Report)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md)

---

## 1. Mục tiêu Nghiệp vụ và Điểm nhấn Học thuật

* **Đạt chuẩn 100% Tiêu chí Đồ án (Grouping and Totals Report):** Báo biểu 1 được thiết kế chuyên biệt để đáp ứng yêu cầu: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
* **Cấu trúc 2 Bảng Tổng hợp Đa cấp (Dual Pivot Tables with Subtotals & Totals):** Toàn bộ phần thân trang được cấu thành bởi **2 Bảng tổng hợp phân cấp (Pivot Tables)** đặt song song đối xứng:
  1. **Visual 1 (Bên Trái) – Grouping theo Tổ chức:** Phân nhóm 2 tầng `Giải đấu` (`Competition_Name`) $\rightarrow$ `Câu lạc bộ` (`Club_Name`).
  2. **Visual 2 (Bên Phải) – Grouping theo Chiến thuật:** Phân nhóm 3 tầng `Tuyến thi đấu` (`Main_Position`) $\rightarrow$ `Vị trí chi tiết` (`Sub_Position`) $\rightarrow$ `Cầu thủ` (`Player_Name`).
* **Tính năng Tổng hợp:** Cả 2 bảng đều kích hoạt đầy đủ dòng **Tổng phụ (Subtotals)** cho từng cấp nhóm và dòng **Tổng cộng (Grand Total)** ở đáy bảng, kèm tính năng tương tác chéo (Cross-filtering) mượt mà.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG ĐA CẤP (Font: 20pt Bold, Center)           |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Bàn Thắng]  | [Card 2: Tổng Kiến Tạo]   | [Card 3: Tổng Đóng Góp G+A] | [Card 4: Thời Lượng TB / Trận]    |
| SUM(Goals)                | SUM(Assists)              | SUM(Goal_Contributions)     | Calculated: Mins / Appearances    |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB    | Nền Pastel Purple #FAF5FF         |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]                                  | [Bộ lọc 2: Giải đấu]                                            |
| Season (Drop-down list, H = 75 px)                    | Competition_Name (Drop-down list, H = 75 px)                    |
| Tọa độ: X = 20 px, Y = 210 px | Width = 925 px        | Tọa độ: X = 975 px, Y = 210 px | Width = 925 px                 |
+-------------------------------------------------------+-----------------------------------------------------------------+
| [VISUAL 1: PIVOT TABLE TỔ CHỨC (18pt Bold)]           | [VISUAL 2: PIVOT TABLE CHIẾN THUẬT (18pt Bold)]                 |
| Phân nhóm: Giải đấu -> Câu lạc bộ                     | Phân nhóm: Tuyến thi đấu -> Vị trí chi tiết -> Cầu thủ          |
| Rows: Competition_Name -> Club_Name                   | Rows: Main_Position -> Sub_Position -> Player_Name              |
| Metrics: Goals, Assists, Goal_Contributions (Bar)     | Metrics: Goals, Assists, Goal_Contributions (Bar), Minutes      |
| Appearances (COUNT_DISTINCT), Minutes_Played          | Subtotals: Bật ON | Grand Total: Bật ON                         |
| Subtotals: Bật ON | Grand Total: Bật ON               |                                                                 |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 760 px| Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 760 px         |
+-------------------------------------------------------+-----------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo
1. Trong báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Hiệu suất Tấn công (Grouping & Totals)`.
3. Menu **Trang** $\rightarrow$ **Cài đặt trang hiện tại** $\rightarrow$ tab **Kiểu**:
   * **Nền trang:** Màu xám khói `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Thêm **Hộp văn bản (Text box)** tại: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
2. Nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG ĐA CẤP (GROUPING AND TOTALS REPORT)`.
3. Font: **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu `#0F172A`, Nền `#FFFFFF`, Bo viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI Tấn công (Scorecards)
Menu **Thêm biểu đồ** $\rightarrow$ **Thẻ chỉ số (Scorecard)**, hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

1. **Thẻ 1 (Tổng Bàn Thắng):** `X = 20 px`, Metric `Goals` (SUM). Đổi tên: `Tổng Bàn Thắng`. Cỡ chữ **`35 pt` Bold**, Nền `#EFF6FF`, Bo góc `10 px`.
2. **Thẻ 2 (Tổng Kiến Tạo):** `X = 495 px`, Metric `Assists` (SUM). Đổi tên: `Tổng Kiến Tạo`. Cỡ chữ **`35 pt` Bold**, Nền `#F0FDF4`, Bo góc `10 px`.
3. **Thẻ 3 (Tổng Đóng Góp G+A):** `X = 970 px`, Metric `Goal_Contributions` (SUM). Đổi tên: `Tổng Đóng Góp G+A`. Cỡ chữ **`35 pt` Bold**, Nền `#FFFBEB`, Bo góc `10 px`.
4. **Thẻ 4 (Thời Lượng TB / Trận):** `X = 1445 px`, tạo Calculated Field `SUM(Minutes_Played) / COUNT(Appearance_ID)`. Đổi tên: `Thời Lượng TB / Trận (Phút)`. Cỡ chữ **`35 pt` Bold**, Nền `#FAF5FF`, Bo góc `10 px`.

---

### Bước 4: Thiết lập 2 Bộ lọc Điều khiển (Controls)
Menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ hàng `Y = 210 px`, `Height = 75 px`:

1. **Bộ lọc 1 (Mùa giải):** `X = 20 px`, `Width = 925 px`, Loại `Drop-down list`, Control field: `Season`.
2. **Bộ lọc 2 (Giải đấu):** `X = 975 px`, `Width = 925 px`, Loại `Drop-down list`, Control field: `Competition_Name`.

---

### Bước 5: Visual 1 (Bên Trái) – Pivot Table Phân nhóm theo Tổ chức (Giải đấu $\rightarrow$ Câu lạc bộ)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)** (hoặc **Bảng tổng hợp / Pivot Table**).
2. Tọa độ & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimensions - Grouping):** Kéo lần lượt 2 trường:
     1. `Competition_Name` (Cấp 1: Phân nhóm Giải đấu).
     2. `Club_Name` (Cấp 2: Câu lạc bộ).
   * **Phương diện cột (Column Dimensions):** Để trống.
   * **Chỉ số (Metrics - Totals):** Kéo các thước đo:
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
     4. `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận`).
     5. `Minutes_Played` (SUM, Đổi tên: `Số phút`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng số bàn thắng, kiến tạo cho từng Giải đấu).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total / Summary row):** Gạt sang **ON**! (Hiển thị dòng Tổng cộng toàn bộ châu Âu ở đáy bảng).
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng hiển thị là **Thanh (Bar)** màu xanh dương `#2563EB`.
   * **Tương tác chéo:** Cuộn xuống mục **Tương tác trên biểu đồ (Chart interactions)** $\rightarrow$ tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề bảng: `Báo cáo Phân nhóm Hỏa lực theo Giải đấu & Câu lạc bộ (Grouping by Club)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Bên Phải) – Pivot Table Phân nhóm theo Chiến thuật (Tuyến $\rightarrow$ Vị trí $\rightarrow$ Cầu thủ)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)**.
2. Tọa độ & Kích thước: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimensions - Grouping):** Kéo lần lượt 3 trường:
     1. `Main_Position` (Cấp 1: Tuyến thi đấu - *Attack, Midfield, Defender*).
     2. `Sub_Position` (Cấp 2: Vị trí chi tiết - *Centre-Forward, Left Winger...*).
     3. `Player_Name` (Cấp 3: Cầu thủ).
   * **Phương diện cột:** Để trống.
   * **Chỉ số (Metrics - Totals):** Kéo 4 thước đo:
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
     4. `Minutes_Played` (SUM, Đổi tên: `Số phút`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng cho từng Tuyến thi đấu và từng Vị trí).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total):** Gạt sang **ON**!
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng **Thanh (Bar)** màu xanh dương `#2563EB`.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Báo cáo Phân nhóm Đóng góp theo Tuyến thi đấu & Cầu thủ (Grouping by Position)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo

1. **Khẳng định tính chất Grouping & Totals:** Cả 2 visual đều là bảng phân nhóm đa tầng có tính năng gập mở, có đầy đủ các dòng Subtotals in đậm rõ ràng và dòng Grand Total ở đáy trang.
2. **Khả năng tương tác chéo (Cross-filtering):** Khi người xem nhấp vào một CLB ở bảng bên trái (ví dụ: `Manchester City`), bảng bên phải lập tức tự động lọc và hiển thị ngay cơ cấu phân nhóm các tuyến và cầu thủ của riêng Man City kèm Subtotals từng tuyến.
