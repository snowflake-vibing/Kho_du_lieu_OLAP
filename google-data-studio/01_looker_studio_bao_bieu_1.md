# Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu và Huấn luyện viên Trưởng (Grouping and Totals Tournament Hierarchy & Head Coach Performance Report)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md)

---

## 1. Mục tiêu Nghiệp vụ và Điểm nhấn Học thuật

* **Đạt chuẩn 100% Tiêu chí Đồ án (Grouping and Totals Report):** Báo biểu 1 được thiết kế chuyên biệt để đáp ứng yêu cầu: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
* **Khai thác toàn bộ các trường dữ liệu MỚI 100%**: Sử dụng **`Coach_Name`** (Huấn luyện viên trưởng: Pep Guardiola, Xabi Alonso, Arteta...), **`Competition_Type`** (Cúp Châu Âu `international_cup` vs Giải Quốc nội `domestic_league`), **`Competition_Country`** (Quốc gia giải đấu), **`Quarter`** (Quý thi đấu) và thẻ chỉ số **`Total Coaches`** (`175` HLV), loại bỏ hoàn toàn cảm giác lặp lại các cột cũ ở Báo biểu 2 và 3.
* **Cấu trúc 2 Bảng Tổng hợp Đa cấp (Dual Pivot Tables with Subtotals & Totals):** Toàn bộ phần thân trang được cấu thành bởi **2 Bảng tổng hợp phân cấp (Pivot Tables)** đặt song song đối xứng:
  1. **Visual 1 (Bên Trái) – Grouping Cấu trúc Giải đấu:** Phân nhóm 3 tầng `Loại giải` (`Competition_Type`) $\rightarrow$ `Quốc gia` (`Competition_Country`) $\rightarrow$ `Tên giải đấu` (`Competition_Name`).
  2. **Visual 2 (Bên Phải) – Grouping theo Huấn luyện viên trưởng:** Phân nhóm 3 tầng `Huấn luyện viên trưởng` (`Coach_Name`) $\rightarrow$ `Câu lạc bộ` (`Club_Name`) $\rightarrow$ `Cầu thủ ghi bàn` (`Player_Name`).
* **Tính năng Tổng hợp:** Cả 2 bảng đều kích hoạt đầy đủ dòng **Tổng phụ (Subtotals)** cho từng cấp nhóm và dòng **Tổng cộng (Grand Total)** ở đáy bảng, kèm tính năng tương tác chéo (Cross-filtering) mượt mà.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU & HUẤN LUYỆN VIÊN    |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Số Trận]    | [Card 2: Tổng Số HLV Trưởng]| [Card 3: Tổng Bàn Thắng]  | [Card 4: Tổng Đóng Góp G+A]       |
| 6,965 Trận Quản Trị       | 175 Huấn Luyện Viên       | 19.17K Bàn Thắng Ghi Được | 33.91K Điểm Sát Thương Tấn Công   |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Purple #FAF5FF | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB          |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)   | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+---------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Loại Cúp/Giải] | [Bộ lọc 3: Quốc gia giải] | [Bộ lọc 4: Quý thi đấu]           |
| Season (Dropdown)         | Competition_Type (Drop)   | Competition_Country (Drop)| Quarter (Dropdown)                |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 455, H: 75, X: 970)   | (W: 455, H: 75, X: 1445)          |
+-------------------------------------------------------+-----------------------------------------------------------------+
| [VISUAL 1: PIVOT TABLE CẤU TRÚC GIẢI ĐẤU (18pt Bold)] | [VISUAL 2: PIVOT TABLE HUẤN LUYỆN VIÊN TRƯỞNG (18pt Bold)]      |
| Phân nhóm: Loại giải -> Quốc gia -> Tên giải đấu      | Phân nhóm: Huấn luyện viên trưởng -> Câu lạc bộ -> Cầu thủ      |
| Rows: Competition_Type -> Country -> Competition_Name | Rows: Coach_Name -> Club_Name -> Player_Name                    |
| Metrics: Số trận, Bàn thắng, Kiến tạo, Tổng G+A (Bar) | Metrics: Bàn thắng, Kiến tạo, Tổng G+A (Bar), Số trận           |
| Subtotals: Bật ON | Grand Total: Bật ON               | Subtotals: Bật ON (Dòng Tổng HLV) | Grand Total: Bật ON         |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 760 px| Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 760 px         |
+-------------------------------------------------------+-----------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo
1. Trong báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Cấu trúc Giải đấu & HLV (Grouping & Totals)`.
3. Menu **Trang** $\rightarrow$ **Cài đặt trang hiện tại** $\rightarrow$ tab **Kiểu**:
   * **Nền trang:** Màu xám khói `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Thêm **Hộp văn bản (Text box)** tại: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
2. Nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU VÀ HUẤN LUYỆN VIÊN TRƯỞNG`.
3. Font: **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu `#0F172A`, Nền `#FFFFFF`, Bo viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI Quản trị & Hỏa lực (Scorecards)
Menu **Thêm biểu đồ** $\rightarrow$ **Thẻ chỉ số (Scorecard)**, hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

1. **Thẻ 1 (Tổng Số Trận Quản Trị):** `X = 20 px`, Metric `Appearance_ID` (COUNT_DISTINCT). Đổi tên: `Tổng Số Trận Quản Trị`. Cỡ chữ **`35 pt` Bold** (hiển thị `6,965`), Nền `#EFF6FF`, Bo góc `10 px`.
2. **Thẻ 2 (Tổng Số Huấn Luyện Viên Trưởng):** `X = 495 px`, tạo Calculated Field: `COUNT_DISTINCT(Coach_Name)`. Đổi tên: `Tổng Số HLV Trưởng`. Cỡ chữ **`35 pt` Bold** (hiển thị **`175`** HLV), Nền `#FAF5FF`, Bo góc `10 px`.
3. **Thẻ 3 (Tổng Bàn Thắng Toàn Giải):** `X = 970 px`, Metric `Goals` (SUM). Đổi tên: `Tổng Bàn Thắng Toàn Giải`. Cỡ chữ **`35 pt` Bold** (hiển thị `19.17K`), Nền `#F0FDF4`, Bo góc `10 px`.
4. **Thẻ 4 (Tổng Đóng Góp G+A):** `X = 1445 px`, Metric `Goal_Contributions` (SUM). Đổi tên: `Tổng Đóng Góp G+A`. Cỡ chữ **`35 pt` Bold** (hiển thị `33.91K`), Nền `#FFFBEB`, Bo góc `10 px`.

---

### Bước 4: Thiết lập 4 Bộ lọc Điều khiển (Controls)
Menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ hàng `Y = 210 px`, `Height = 75 px`, `Width = 455 px`:

1. **Bộ lọc 1 (Mùa giải):** `X = 20 px`, Loại `Drop-down list`, Control field: `Season`.
2. **Bộ lọc 2 (Phân loại Cúp / Giải - MỚI):** `X = 495 px`, Loại `Drop-down list`, Control field: `Competition_Type` (Lọc xem Cúp Châu lục `international_cup` hay Giải Quốc nội `domestic_league`).
3. **Bộ lọc 3 (Quốc gia giải đấu - MỚI):** `X = 970 px`, Loại `Drop-down list`, Control field: `Competition_Country` (Lọc theo England, Spain, Germany, Italy, France...).
4. **Bộ lọc 4 (Quý thi đấu - MỚI):** `X = 1445 px`, Loại `Drop-down list`, Control field: `Quarter` (Lọc theo Q1, Q2, Q3, Q4).

---

### Bước 5: Visual 1 (Bên Trái) – Pivot Table Phân nhóm Cấu trúc Giải đấu (Loại giải $\rightarrow$ Quốc gia $\rightarrow$ Tên giải)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)**.
2. Tọa độ & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimensions - Grouping):** Kéo lần lượt 3 trường:
     1. `Competition_Type` (Cấp 1: Phân loại giải - *domestic_league vs international_cup*).
     2. `Competition_Country` (Cấp 2: Quốc gia giải đấu).
     3. `Competition_Name` (Cấp 3: Tên giải đấu cụ thể).
   * **Phương diện cột:** Để trống.
   * **Chỉ số (Metrics - Totals):** Kéo các thước đo:
     1. `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận`).
     2. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     3. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     4. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng số bàn thắng, kiến tạo cho từng Loại giải và từng Quốc gia).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total / Summary row):** Gạt sang **ON**! (Hiển thị dòng Tổng cộng toàn bộ châu Âu ở đáy bảng).
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng hiển thị là **Thanh (Bar)** màu xanh dương `#2563EB`.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề bảng: `Báo cáo Phân nhóm Cấu trúc Giải đấu & Hỏa lực (Tournament Hierarchy)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Bên Phải) – Pivot Table Phân nhóm theo Huấn Luyện Viên Trưởng (HLV $\rightarrow$ CLB $\rightarrow$ Cầu thủ)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)**.
2. Tọa độ & Kích thước: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimensions - Grouping):** Kéo lần lượt 3 trường:
     1. `Coach_Name` (Cấp 1: Huấn luyện viên trưởng - *Pep Guardiola, Xabi Alonso, Mikel Arteta, Carlo Ancelotti, Luis Enrique, Arne Slot...*).
     2. `Club_Name` (Cấp 2: Câu lạc bộ dẫn dắt).
     3. `Player_Name` (Cấp 3: Cầu thủ / Học trò ghi bàn).
   * **Phương diện cột:** Để trống.
   * **Chỉ số (Metrics - Totals):** Kéo các thước đo:
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
     4. `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận cầm quân`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng cho từng Huấn luyện viên trưởng).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total):** Gạt sang **ON**!
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng **Thanh (Bar)** màu xanh dương `#2563EB`.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Báo cáo Phân nhóm Hiệu suất Tấn công theo Huấn Luyện Viên Trưởng (Head Coach Analytics)`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo

1. **Khẳng định tính chất Grouping & Totals:** Cả 2 visual đều là bảng phân nhóm đa tầng có tính năng gập mở, có đầy đủ các dòng Subtotals in đậm rõ ràng và dòng Grand Total ở đáy trang.
2. **Khả năng tương tác chéo (Cross-filtering):** Khi người xem nhấp vào giải đấu `Premier League` ở bảng bên trái, bảng bên phải lập tức tự động lọc và hiển thị ngay các Huấn luyện viên đang cầm quân tại Ngoại Hạng Anh (*Pep Guardiola, Mikel Arteta, Jürgen Klopp...*) cùng thành tích và dàn học trò của họ.
3. **Tuyệt đối không trùng lặp:** Khai thác toàn diện các góc nhìn mới về cấu trúc giải đấu (`Competition_Type`, `Competition_Country`) và nhà cầm quân (`Coach_Name`, `Total Coaches = 175`).
