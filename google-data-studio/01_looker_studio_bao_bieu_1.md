# Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu và Huấn luyện viên Trưởng (Grouping and Totals Tournament Hierarchy & Head Coach Performance Report)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md)

---

## 1. Mục tiêu Nghiệp vụ và Điểm nhấn Học thuật

* **Đạt chuẩn 100% Tiêu chí Đồ án (Grouping and Totals Report):** Báo biểu 1 được thiết kế chuyên biệt để đáp ứng yêu cầu: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
* **Khai thác toàn bộ các trường dữ liệu MỚI 100%**: Sử dụng **`Coach_Name`** (Huấn luyện viên trưởng: Pep Guardiola, Xabi Alonso, Arteta...), **`Competition_Type`** (Cúp Châu Âu `international_cup` vs Giải Quốc nội `domestic_league`), **`Competition_Country`** (Quốc gia giải đấu), **`Match_Round`** (Vòng đấu / Giai đoạn thi đấu từ `DIM_Game`), **`Quarter`** (Quý thi đấu) và thẻ chỉ số **`Total Coaches`** (`175` HLV), loại bỏ hoàn toàn cảm giác lặp lại các cột cũ ở Báo biểu 2 và 3.
* **Cặp đôi tương tác hoàn hảo giữa Đồ họa Phân cấp (Chart) và Bảng Ma trận (Pivot Table):**
  1. **Visual 1 (Bên Trái) – Biểu đồ Thanh Xếp chồng Phân cấp có Drill-down 4 Tầng (Hierarchical Stacked Bar Chart):** Phân tầng cấu trúc giải đấu và vòng đấu 4 cấp (`Competition_Type` $\rightarrow$ `Competition_Country` $\rightarrow$ `Competition_Name` $\rightarrow$ `Match_Round`), kích hoạt tính năng **Khoan sâu (Drill-down)** và tự động hiển thị **Nhãn dữ liệu (Data labels)** trên từng phân đoạn.
  2. **Visual 2 (Bên Phải) – Bảng Ma trận Phân nhóm & Tổng hợp theo HLV Trưởng (Grouping & Totals Pivot Table):** Phân nhóm 3 tầng `Huấn luyện viên trưởng` (`Coach_Name`) $\rightarrow$ `Câu lạc bộ` (`Club_Name`) $\rightarrow$ `Cầu thủ ghi bàn` (`Player_Name`), kích hoạt dòng **Tổng phụ (Subtotals)** cho từng HLV và dòng **Tổng cộng (Grand Total)** ở đáy bảng.
* **Tính năng Tương tác Chéo (Cross-filtering):** Khi người xem nhấp chọn một giải đấu hoặc vòng đấu trên biểu đồ thanh bên trái (ví dụ `uefa-champions-league` $\rightarrow$ `Final`), bảng Ma trận bên phải lập tức tự động lọc và bung ra các HLV cầm quân tại trận chung kết kèm dàn học trò của họ.

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
| [VISUAL 1: THANH XẾP CHỒNG PHÂN CẤP CÓ DRILL-DOWN]    | [VISUAL 2: PIVOT TABLE HUẤN LUYỆN VIÊN TRƯỞNG (18pt Bold)]      |
| Biểu đồ Thanh ngang Phân cấp (Stacked Bar with Drill)  | Phân nhóm: Huấn luyện viên trưởng -> Câu lạc bộ -> Cầu thủ      |
| Trục Y: Competition_Type -> Country -> Competition -> Round | Rows: Coach_Name -> Club_Name -> Player_Name               |
| Trục X: Goals (Xanh dương) + Assists (Xanh Cyan)      | Metrics: Goals, Assists, Goal_Contributions (Bar), Matches      |
| Drill-down 4 cấp: Cúp -> Quốc gia -> Giải -> Vòng đấu | Subtotals: Bật ON (Dòng Tổng HLV) | Grand Total: Bật ON         |
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

### Bước 5: Visual 1 (Bên Trái) – Biểu đồ Thanh Xếp chồng Phân cấp Cấu trúc Giải đấu & Vòng đấu (Stacked Bar Chart with 4-Level Drill-down)

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ thanh xếp chồng (Stacked bar chart)** (hoặc Biểu đồ cột xếp chồng).
2. Tọa độ & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 760 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện (Dimension):** Kéo lần lượt 4 cấp phân loại:
     1. `Competition_Type` (Cấp 1: Phân loại giải - *domestic_league vs international_cup*).
     2. `Competition_Country` (Cấp 2: Quốc gia giải đấu).
     3. `Competition_Name` (Cấp 3: Tên giải đấu cụ thể).
     4. `Match_Round` (Cấp 4: Vòng đấu / Chặng thi đấu từ `DIM_Game` - *Group Stage, last 16, Quarter-Finals, Semi-Finals, Final hoặc Matchday 1..38*).
   * **Khoan sâu (Drill-down):** Gạt công tắc sang **BẬT (ON)**! (Cho phép người dùng bấm vào thanh giải để khoan sâu từ Cúp $\rightarrow$ Quốc gia $\rightarrow$ Giải đấu $\rightarrow$ Vòng đấu).
   * **Chỉ số (Metrics):** Kéo 2 thước đo:
     1. `Goals` (SUM, Đổi tên: `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Kiến tạo`).
   * **Sắp xếp (Sort):** Sắp xếp theo `Goals` Giảm dần (Descending).
4. **Định dạng hiển thị trong thẻ Kiểu (Style):**
   * **Chuỗi màu:**
     * Chuỗi 1 (`Goals`): Xanh dương đậm `#2563EB`.
     * Chuỗi 2 (`Assists`): Xanh Cyan ngọc `#06B6D4`.
   * **Bật Nhãn dữ liệu (Show data labels):** Gạt sang **ON** để hiển thị rõ ràng giá trị số trên từng thanh.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)** (Nhấp vào một thanh/vòng đấu sẽ lọc toàn bộ trang và bảng HLV bên phải).
   * Tiêu đề biểu đồ: `Phân bổ Hỏa lực Tấn công theo Cấu trúc Giải đấu & Vòng đấu (Tournament Hierarchy & Match Round Drill-down)`.
   * Cỡ chữ tiêu đề: **`18 pt` Bold**, Màu `#0F172A`, Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Visual 2 (Bên Phải) – Bảng Ma trận Phân nhóm theo Huấn Luyện Viên Trưởng (HLV $\rightarrow$ CLB $\rightarrow$ Cầu thủ)

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
     4. `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận`).
4. **Kích hoạt Grouping & Totals trong thẻ Kiểu (Style):**
   * **Bật Dòng Tổng phụ (Show subtotals):** Gạt sang **ON**! (Tự động hiển thị dòng tổng cho từng Huấn luyện viên trưởng).
   * **Bật Dòng Tổng cộng toàn bộ (Show grand total):** Gạt sang **ON**! (Dòng tổng cộng toàn diện ở đáy bảng).
   * **Thanh dữ liệu trực quan:** Tại cột `Goal_Contributions`, chọn định dạng **Thanh (Bar)** màu xanh dương `#2563EB`.
   * **Tương tác chéo:** Tích chọn **Áp dụng bộ lọc (Cross-filtering)**.
   * Tiêu đề: `Báo cáo Phân nhóm Hiệu suất Tấn công theo Huấn Luyện Viên Trưởng (Head Coach Analytics)`.
   * Cỡ chữ tiêu đề: **`18 pt` Bold**, Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Tương tác Chéo

1. **Đáp ứng hoàn hảo chuẩn mực Grouping & Totals:** Bảng Ma trận HLV Visual 2 sở hữu tính năng phân nhóm đa cấp độ sâu 3 tầng, hiển thị đầy đủ dòng Subtotals cho từng nhà cầm quân và Grand Total ở đáy trang.
2. **Trải nghiệm trực quan cân đối, không trùng lặp dạng hiển thị:** Bên trái là đồ họa trực quan (Stacked Bar Chart with Drill-down) giúp quan sát tỷ trọng và khoan sâu cấu trúc giải; bên phải là bảng dữ liệu chi tiết đa cấp (Grouping & Totals Matrix), tạo nên cặp đôi thị giác cân bằng, sinh động.
3. **Khả năng tương tác chéo (Cross-filtering):** Khi người xem nhấp vào giải đấu `Premier League` ở biểu đồ bên trái, bảng bên phải lập tức tự động lọc và hiển thị ngay các Huấn luyện viên đang cầm quân tại Ngoại Hạng Anh (*Pep Guardiola, Mikel Arteta, Arne Slot...*) cùng thành tích và dàn học trò của họ.
4. **Bộ trường dữ liệu hoàn toàn mới lạ:** Khai thác triệt để `Coach_Name`, `Total Coaches = 175`, `Competition_Type`, `Competition_Country`, `Quarter`, hoàn toàn độc lập và không tái sử dụng cụm thông tin của Báo biểu 2 và Báo biểu 3.
