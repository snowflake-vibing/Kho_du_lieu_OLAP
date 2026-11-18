# Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công theo Giải đấu, Chu kỳ Thời gian và Huấn luyện viên Trưởng (Grouping and Totals Report)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md)

---

## 1. Mục tiêu Nghiệp vụ và Điểm nhấn Học thuật

* **Đạt chuẩn 100% Tiêu chí Đồ án (Grouping and Totals Report):** Báo biểu 1 được thiết kế chuyên biệt để đáp ứng yêu cầu: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
* **Khai thác toàn bộ các trường dữ liệu MỚI 100%**: Sử dụng **`Coach_Name`** (Huấn luyện viên trưởng), **`Competition_Type`** (Cúp Châu Âu vs Giải Quốc nội), **`Competition_Country`** (Quốc gia giải đấu), **`Match_Round`** (Vòng đấu từ `DIM_Game`), **`Quarter`** (Quý thi đấu) và thẻ chỉ số **`Total Coaches`** (`175` HLV), loại bỏ hoàn toàn cảm giác lặp lại các cột cũ ở Báo biểu 2 và 3.
* **Bộ ba Visual kết hợp hoàn chỉnh (Stacked Bar + Stacked Column + Pivot Table):**
  1. **Visual 1 (Trên Trái) – Biểu đồ Thanh Ngang Xếp chồng Phân cấp (Stacked Bar Chart with 4-Level Drill-down):** Phân tầng cấu trúc giải đấu và vòng đấu 4 cấp (`Competition_Type` $\rightarrow$ `Competition_Country` $\rightarrow$ `Competition_Name` $\rightarrow$ `Match_Round`), bật **Khoan sâu (Drill-down)** và **Nhãn dữ liệu (Data labels)**.
  2. **Visual 2 (Dưới Trái) – Biểu đồ Cột Dọc Xếp chồng Theo Mùa giải & Quý (Stacked Column Chart with Drill-down):** Phân nhóm hỏa lực theo `Season` $\rightarrow$ `Quarter`, xếp chồng `Goals` + `Assists`, bật **Nhãn dữ liệu (Data labels)**.
  3. **Visual 3 (Bên Phải) – Bảng Ma trận Phân nhóm & Tổng hợp theo HLV Trưởng (Pivot Table with Subtotals & Grand Total):** Phân nhóm 3 tầng `Coach_Name` $\rightarrow$ `Club_Name` $\rightarrow$ `Player_Name`, kích hoạt dòng **Tổng phụ (Subtotals)** cho từng HLV và dòng **Tổng cộng (Grand Total)** ở đáy bảng.
* **Tính năng Tương tác Chéo (Cross-filtering):** Nhấp chọn một giải đấu/vòng đấu (Visual 1) hoặc một Mùa giải/Quý (Visual 2) $\rightarrow$ Toàn bộ trang và Bảng Ma trận HLV (Visual 3) tự động lọc đồng bộ tức thời.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG      |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Số Trận]    | [Card 2: Tổng Số HLV Trưởng]| [Card 3: Tổng Bàn Thắng]  | [Card 4: Tổng Đóng Góp G+A]       |
| 6,965 Trận Quản Trị       | 175 Huấn Luyện Viên       | 19.17K Bàn Thắng Ghi Được | 33.91K Điểm Sát Thương Tấn Công   |
| Nền Pastel Blue #EFF6FF   | Nền Pastel Purple #FAF5FF | Nền Pastel Green #F0FDF4  | Nền Pastel Amber #FFFBEB          |
| (W: 455, H: 90, X: 20)    | (W: 455, H: 90, X: 495)   | (W: 455, H: 90, X: 970)   | (W: 455, H: 90, X: 1445)          |
+---------------------------+---------------------------+---------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Loại Cúp/Giải] | [Bộ lọc 3: Quốc gia giải] | [Bộ lọc 4: Quý thi đấu]           |
| Season (Dropdown)         | Competition_Type (Drop)   | Competition_Country (Drop)| Quarter (Dropdown)                |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 455, H: 75, X: 970)   | (W: 455, H: 75, X: 1445)          |
+--------------------------------------------------+----------------------------------------------------------------------+
| [VISUAL 1: STACKED BAR CẤU TRÚC GIẢI ĐẤU]        | [VISUAL 3: PIVOT TABLE HUẤN LUYỆN VIÊN TRƯỞNG (SUBTOTALS & TOTAL)]   |
| Trục Y: Type -> Country -> Comp -> Match_Round   | Rows: Coach_Name -> Club_Name -> Player_Name                         |
| Trục X: Goals (#2563EB) + Assists (#06B6D4)      | Metrics: Goals, Assists, Goal_Contributions (Bar), Matches           |
| Drill-down: 4 cấp | Data labels: ON              | Subtotals: Bật ON (Dòng Tổng HLV) | Grand Total: Bật ON              |
| X = 20, Y = 280 | W = 860 px, H = 380 px         |                                                                      |
+--------------------------------------------------+                                                                      |
| [VISUAL 2: STACKED COLUMN THEO MÙA GIẢI & QUÝ]   |                                                                      |
| Trục X: Season -> Quarter (Drill-down 2 cấp)     |                                                                      |
| Trục Y: Goals (#2563EB) + Assists (#06B6D4)      |                                                                      |
| Data labels: ON | Cross-filtering: ON            |                                                                      |
| X = 20, Y = 680 | W = 860 px, H = 380 px         | Tọa độ: X = 900 px, Y = 280 px | W = 1000 px, H = 780 px             |
+--------------------------------------------------+----------------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo
1. Trong báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Grouping & Totals (Giải đấu, Quý & HLV)`.
3. Menu **Trang** $\rightarrow$ **Cài đặt trang hiện tại** $\rightarrow$ tab **Kiểu**:
   * **Nền trang:** Màu xám khói `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Thêm **Hộp văn bản (Text box)** tại: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
2. Nội dung: `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG`.
3. Font: **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu `#0F172A`, Nền `#FFFFFF`, Bo viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI Quản trị & Hỏa lực (Scorecards)
Menu **Thêm biểu đồ** $\rightarrow$ **Thẻ chỉ số (Scorecard)**, hàng `Y = 85 px`, `Height = 90 px`, `Width = 455 px`:

1. **Thẻ 1 (Tổng Số Trận Quản Trị):** `X = 20 px`, Metric `Appearance_ID` (COUNT_DISTINCT). Đổi tên: `Tổng Số Trận Quản Trị`. Cỡ chữ **`35 pt` Bold** (hiển thị `6,965`), Nền `#EFF6FF`, Bo góc `10 px`.
2. **Thẻ 2 (Tổng Số Huấn Luyện Viên Trưởng):** `X = 495 px`, tạo Calculated Field: `COUNT_DISTINCT(Coach_Name)`. Đổi tên: `Tổng Số HLV Trưởng`. Cỡ chữ **`35 pt` Bold** (hiển thị **`175`** HLV), Nền `#FAF5FF`, Bo góc `10 px`.
3. **Thẻ 3 (Tổng Bàn Thắng Toàn Giải):** `X = 970 px`, Metric `Goals` (SUM). Đổi tên: `Tổng Bàn Thắng Toàn Giải`. Cỡ chữ **`35 pt` Bold** (hiển thị `19.17K`), Nền `#F0FDF4`, Bo góc `10 px`.
4. **Thẻ 4 (Tổng Đóng Góp G+A):** `X = 1445 px`, Metric `Goal_Contributions` (SUM). Đổi tên: `Tổng Đóng Góp G+A`. Cỡ chữ **`35 pt` Bold** (hiển thị `33.91K`), Nền `#FFFBEB`, Bo góc `10 px`.

---

### Bước 4: Thiết lập 4 Bộ lọc Điều khiển (Controls)
Menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ hàng `Y = 190 px`, `Height = 75 px`, `Width = 455 px`:

1. **Bộ lọc 1 (Mùa giải):** `X = 20 px`, Loại `Drop-down list`, Control field: `Season`.
2. **Bộ lọc 2 (Phân loại Cúp / Giải - MỚI):** `X = 495 px`, Loại `Drop-down list`, Control field: `Competition_Type`.
3. **Bộ lọc 3 (Quốc gia giải đấu - MỚI):** `X = 970 px`, Loại `Drop-down list`, Control field: `Competition_Country`.
4. **Bộ lọc 4 (Quý thi đấu - MỚI):** `X = 1445 px`, Loại `Drop-down list`, Control field: `Quarter`.

---

### Bước 5: Visual 1 (Trên Trái) – Stacked Bar Chart Phân cấp Giải đấu & Vòng đấu

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ thanh xếp chồng (Stacked bar chart)**.
2. Tọa độ & Kích thước: `X = 20 px`, `Y = 280 px`, `Width = 860 px`, `Height = 380 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện (Dimension):** Kéo lần lượt 4 cấp phân loại:
     1. `Competition_Type`
     2. `Competition_Country`
     3. `Competition_Name`
     4. `Match_Round` (Cấp 4 từ `DIM_Game`)
   * **Khoan sâu (Drill-down):** Gạt sang **BẬT (ON)**!
   * **Chỉ số (Metrics):** `Goals` (SUM) và `Assists` (SUM).
   * **Sắp xếp (Sort):** `Goals` Giảm dần (Descending).
4. **Định dạng (Style):**
   * `Goals`: `#2563EB`; `Assists`: `#06B6D4`.
   * **Bật Nhãn dữ liệu (Show data labels):** **ON**.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Phân cấp Hỏa lực theo Giải đấu & Vòng đấu (Stacked Bar Drill-down)`, Cỡ chữ **`16 pt` Bold**, Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Dưới Trái) – Stacked Column Chart Phân nhóm theo Mùa giải & Quý

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ cột xếp chồng (Stacked column chart)**.
2. Tọa độ & Kích thước: `X = 20 px`, `Y = 680 px`, `Width = 860 px`, `Height = 380 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện (Dimension):** Kéo lần lượt 2 cấp phân loại:
     1. `Season` (Cấp 1: `2022/2023`, `2023/2024`).
     2. `Quarter` (Cấp 2: Quý `1`, `2`, `3`, `4`).
   * **Khoan sâu (Drill-down):** Gạt sang **BẬT (ON)**!
   * **Chỉ số (Metrics):** `Goals` (SUM) và `Assists` (SUM).
4. **Định dạng (Style):**
   * `Goals`: `#2563EB`; `Assists`: `#06B6D4` (đồng bộ 100% với Visual 1).
   * **Bật Nhãn dữ liệu (Show data labels):** **ON**.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Tổng hợp Hỏa lực theo Mùa giải & Quý (Stacked Column Grouping & Totals)`, Cỡ chữ **`16 pt` Bold**, Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Visual 3 (Bên Phải) – Pivot Table Phân nhóm theo Huấn Luyện Viên Trưởng (Grouping & Totals)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng tổng hợp có tổng phụ (Pivot table with subtotals)**.
2. Tọa độ & Kích thước: `X = 900 px`, `Y = 280 px`, `Width = 1000 px`, `Height = 780 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện hàng (Row Dimensions - Grouping):**
     1. `Coach_Name` (Cấp 1: Huấn luyện viên trưởng)
     2. `Club_Name` (Cấp 2: Câu lạc bộ)
     3. `Player_Name` (Cấp 3: Cầu thủ ghi bàn)
   * **Chỉ số (Metrics - Totals):**
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Tổng G+A`).
     4. `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận`).
4. **Kích hoạt Grouping & Totals (Style):**
   * **Show subtotals:** **ON**! (Dòng tổng riêng cho từng HLV).
   * **Show grand total:** **ON**! (Dòng tổng cộng ở đáy bảng).
   * **Thanh dữ liệu:** Tại cột `Goal_Contributions`, chọn **Thanh (Bar)** màu `#2563EB`.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Bảng Ma trận Phân nhóm & Tổng hợp theo HLV Trưởng (Matrix Grouping & Totals)`, Cỡ chữ **`18 pt` Bold**, Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo

1. **Hài hòa giữa Trực quan Đồ họa và Chuẩn mực Grouping & Totals:** Bộ ba **Stacked Bar + Stacked Column + Pivot Table** đảm bảo cả tính đa dạng biểu đồ lẫn dòng Subtotals/Grand Total theo đúng tiêu chí chấm điểm.
2. **Tương tác chéo linh hoạt:** Nhấp vào `uefa-champions-league` $\rightarrow$ `Final` ở Visual 1 hoặc Quý `4` ở Visual 2 sẽ tự động lọc đồng bộ toàn bộ trang và bảng HLV bên phải.
