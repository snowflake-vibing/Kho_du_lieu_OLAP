# BỘ QUY TẮC THIẾT KẾ BÁO BIỂU POWER BI & PHÂN TÍCH OLAP
> **File:** `rule.md`  
> **Áp dụng cho:** Hệ thống Báo cáo & Trực quan hóa dữ liệu Kho dữ liệu Bóng đá Châu Âu (`DW Football Transfermarkt`).  
> **Mục tiêu:** Đảm bảo tính nhất quán tuyệt đối về thẩm mỹ cao cấp, chuẩn mực thống kê, giải quyết bài toán nghiệp vụ thực tế và đáp ứng yêu cầu khắt khe của giảng viên hướng dẫn.

---

## 1. QUY CHUẨN TYPOGRAPHY & CỠ CHỮ BẮT BUỘC (VISUAL HIERARCHY)

Mọi visual trên Dashboard bắt buộc phải tuân thủ nghiêm ngặt thang phân cấp cỡ chữ sau:

| Thành phần giao diện | Cỡ chữ quy định | Kiểu chữ (Style) | Vị trí / Căn lề | Ghi chú & Ý nghĩa |
| :--- | :---: | :---: | :---: | :--- |
| **Tiêu đề Banner trên cùng (Header)** | **`20 pt`** | In đậm (**Bold**) | Căn giữa (**Center**) | Tiêu đề chính của báo biểu, màu chữ đen tuyền (`#0F172A`) hoặc trắng tương phản trên nền banner. |
| **Tiêu đề từng Visual / Bảng (Title)** | **`18 pt`** | In đậm (**Bold**) | Căn giữa (**Center**) | Tăng lên 18 pt để làm nổi bật rõ ràng chủ đề của từng biểu đồ, thẻ KPI, bộ lọc Slicer và bảng số liệu. |
| **Giá trị Callout trên KPI Cards** | **`35 pt`** | In đậm (**Bold**) | Căn giữa (**Center**) | Cỡ chữ 35 pt lớn nổi bật, thu hút thị giác ngay lập tức vào các con số chỉ số cốt lõi. |
| **Dữ liệu ô bảng số liệu (Cell Values)** | **`12 pt`** | Thường (Regular) | Canh lề theo kiểu dữ liệu | Đảm bảo tính dễ đọc trong Bảng Ma trận (Matrix Visual), không bị tràn ô. |
| **Tiêu đề Cột & Dòng bảng số liệu** | **`12 pt`** | In đậm (**Bold**) | Khớp với cột dữ liệu | Tiêu đề cột chuẩn tiếng Việt, không viết tắt gây khó hiểu. |
| **Nhãn trục tọa độ (Axes Labels & Values)** | **`12 pt`** | Thường (Regular) | Trục X & Trục Y | Trục số đo và trục danh mục đều đặt cỡ chữ 12 pt. |
| **Nhãn dữ liệu (Data Labels)** | **`12 pt`** | In đậm nhẹ | Trên thanh / điểm dữ liệu | Bật On để người xem đọc ngay số liệu mà không cần rà chuột. |

---

## 2. QUY CHUẨN NỀN MÀU & BẢN ĐỒ MÀU NGỮ NGHĨA (COLOR PALETTE & CONTRAST)

### 2.1. Nền thẻ KPI Cards (Luminance > 90% - Chữ đen tương phản cao WCAG AAA)
* Toàn bộ 4 thẻ KPI bắt buộc sử dụng **màu nền sáng Pastel**, chữ số và tiêu đề dùng màu đen tuyền (`#0F172A`):
  * **Card 1 (Tổng Bàn Thắng):** Nền xanh dương nhạt (`#EFF6FF` / `#E3F2FD`), viền xanh `#93C5FD`.
  * **Card 2 (Tổng Kiến Tạo):** Nền xanh mint nhạt (`#F0FDF4` / `#E8F5E9`), viền xanh `#86EFAC`.
  * **Card 3 (Tổng Đóng Góp G+A):** Nền vàng hổ phách nhạt (`#FFFBEB` / `#FFF8E1`), viền vàng `#FCD34D`.
  * **Card 4 (Hiệu Suất Mins/Bàn):** Nền tím oải hương nhạt (`#FAF5FF` / `#F3E5F5`), viền tím `#D8B4FE`.

### 2.2. Phân biệt màu sắc các trục trên biểu đồ (Axes Color Differentiation)
* Trục tọa độ phải mang màu sắc phân biệt để người xem nhận biết ngay bản chất thông tin:
  * **Trục danh mục (Category Axis - Tên cầu thủ, Mùa giải, Quý):** Dùng màu trung tính đậm như **Xanh Navy đậm (`#0D47A1`)** hoặc **Xám than Slate (`#334155`)**.
  * **Trục số đo định lượng (Value Axis - Thang đo Bàn thắng, Kiến tạo):** Dùng màu chỉ số tương ứng như **Xanh lục Forest Green (`#1B5E20`)** hoặc **Xanh đại dương (`#1565C0`)**.
  * **Phân biệt vị trí thi đấu (Donut / Scatter Legend):** Tiền đạo màu Đỏ cam (`#EF4444`), Tiền vệ màu Xanh dương (`#3B82F6`), Hậu vệ màu Xanh lục (`#10B981`).

### 2.3. Nền Canvas & Cấu trúc Thẻ nổi (Card Elevation UI)
* Nền Canvas sử dụng màu xám khói hiện đại **`#F8FAFC`** (Slate 50), Transparency `0%`.
* Mỗi Visual Container được đóng khung như một thẻ Card độc lập: Nền trắng tinh khiết **`#FFFFFF`**, viền mỏng mảnh **`#E2E8F0`** và **bo tròn góc `8px - 10px`** tạo chiều sâu chuyên nghiệp như sản phẩm SaaS thương mại.

---

## 3. QUY TẮC BỐ CỤC PHÂN VÙNG TRANG BÁO BIỂU (PAGE ARCHITECTURE & 4-QUADRANT GRID)

Bố cục không gian tổng thể của trang báo biểu được quy định chặt chẽ thành **2 tầng chức năng rõ rệt**:

```
+-------------------------------------------------------------------------------------------------------------------------+
| [TẦNG TRÊN CÙNG: HEADER, KPI CARDS & FILTERS]                                                                           |
| 1. Title Banner trên cùng (Font 20pt Bold)                                                                              |
| 2. Khối các thẻ KPI Cards (Title 15-18pt, Value 35pt Bold cực kỳ nổi bật trên thẻ nổi)                                 |
| 3. Hệ thống Bộ lọc tương tác (Slicers): Chiều cao thoáng đãng (H = 75 - 80px), không bị cụt thanh Dropdown/Tile       |
+-------------------------------------------------------------+-----------------------------------------------------------+
| [TẦNG DƯỚI: LƯỚI PHÂN TÍCH 4 BIỂU ĐỒ NÂNG CAO (LINH HOẠT TỶ LỆ TRỰC QUAN)]                                               |
+-------------------------------------------------------------+-----------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI]                                          | [Ô 2: TRÊN - PHẢI (NÂNG CAO)]                             |
| Biểu đồ 1: Thanh Phân cấp (Clustered Bar Chart, Title 18pt) | Biểu đồ 2: Ma trận 4 Góc phần tư (Scatter Quadrant, 18pt) |
| Top 10 Chân sút (Trục Y Navy, Trục X Forest Green, 12pt)    | Goals vs Assists vs Mins theo Vị trí, 2 đường Median      |
+-------------------------------------------------------------+-----------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI (NÂNG CAO)]                               | [Ô 4: DƯỚI - PHẢI (NÂNG CAO)]                             |
| Biểu đồ 3: Bản đồ Phân tầng Đa cấp (Treemap, Title 18pt)    | Biểu đồ 4: Bảng Ma trận Đa cấp (Executive Matrix, 18pt)   |
| Phân tích cơ cấu tỷ trọng bàn thắng (Giải -> Vị trí -> CLB) | Tích hợp Mini Data Bars & Heatmap, Dữ liệu 12pt phẳng     |
+-------------------------------------------------------------+-----------------------------------------------------------+
```

### Chi tiết phân vùng:
1. **Phần trên cùng (Top Section - Control & Summary Zone):**
   * **Title Banner:** Đặt ở vị trí cao nhất (X: 20px, Y: 15px), font 20pt Bold, nhận diện rõ tên báo cáo và khối dữ liệu OLAP.
   * **Khối KPI Cards:** Dàn đều ngay bên dưới (Y: 95px, H: 95px - 105px), hiển thị các chỉ số tổng quan sống còn (Title 15pt - 18pt, **Value 35pt Bold** nổi bật thu hút ánh nhìn tức thì).
   * **Khối Bộ lọc Slicers/Filters:** Đặt ngay dưới khối KPI (Y: 210px), **bắt buộc chiều cao H = 75px - 80px**, chiều rộng thoáng đãng (ví dụ: Season $W = 455\text{ px}$, Competition $W = 455\text{ px}$, Vị trí dạng ngang/Tile $W = 900\text{ px}$). Tuyệt đối không dùng chiều cao nhỏ hẹp ($50\text{ px}$) làm che khuất hoặc cụt thanh Dropdown và nhãn nút chọn.
2. **Phần dưới (Bottom Section - 4-Quadrant Visual Analytics Grid):**
   * Bố trí **đúng 4 loại biểu đồ nâng cao**, tiêu đề từng visual đặt **`18 pt` Bold** để làm nổi bật tên phân tích:
     * **Ô 1 (Trên - Trái):** Biểu đồ thanh ngang phân cấp (Top 10 Chân sút Châu Âu).
     * **Ô 2 (Trên - Phải):** Biểu đồ phân tán 4 góc phần tư (Scatter / Quadrant Bubble Plot) phân loại cầu thủ.
     * **Ô 3 (Dưới - Trái):** Bản đồ phân tầng đa cấp (Hierarchical Treemap Drill-down) phân tích cơ cấu tỷ trọng Part-to-Whole. Có thể mở rộng chiều rộng ($W \approx 1230\text{ px}$) để các khối chữ nhật tỷ trọng hiển thị trọn vẹn và hoành tráng.
     * **Ô 4 (Dưới - Phải):** Bảng ma trận đa cấp tích hợp thanh đo trực quan (Executive Matrix with Embedded Data Bars). Chiều rộng $W \approx 625\text{ px} - 925\text{ px}$ tùy theo mức phân bổ với Treemap.

---

## 4. QUY TẮC KHÔNG GIAN & TRIỆT TIÊU DẤU BA CHẤM (ZERO ELLIPSIS GUARANTEE)

1. **Tuyệt đối không có dấu ba chấm (`...`):** Không một ô dữ liệu, tiêu đề visual, tiêu đề cột hay nhãn trục nào được phép co rút hiển thị `...`.
2. **Kích hoạt tự động xuống dòng và tự co giãn cột:**
   * Trong Bảng Ma trận (Matrix): Bắt buộc bật `wordWrap = true` cho cả Column Headers, Row Headers và Values.
   * Bật `autoSizeColumnWidth = true` để bảng tự tính toán khoảng thở tối ưu.
3. **Chuẩn hóa nhãn hiển thị tiếng Việt ngắn gọn:**
   * Thay vì để nguyên tên trường gốc dài dòng của Fact/Dim, bắt buộc đổi tên hiển thị trong visual:
     * `DIM Player [Player Name]` $\rightarrow$ `Cầu thủ`
     * `DIM Club [Club Name]` $\rightarrow$ `Câu lạc bộ`
     * `FACT Player Match Perf [Minutes Played]` $\rightarrow$ `Số phút thi đấu`
     * `FACT Player Match Perf [Goals]` $\rightarrow$ `Bàn thắng`
     * `FACT Player Match Perf [Assists]` $\rightarrow$ `Kiến tạo`
     * `FACT Player Match Perf [Goal Contributions]` $\rightarrow$ `Tổng G+A`
     * `FACT Player Match Perf [Yellow Cards]` $\rightarrow$ `Thẻ vàng`
4. **Mở rộng không gian hiển thị:** Ưu tiên thiết kế trên canvas độ phân giải cao **Full HD 1920 x 1080 px (16:9)** để bảng ma trận và biểu đồ thanh ngang có đủ diện tích trình bày trọn vẹn họ tên cầu thủ và số liệu.

---

## 5. QUY CHUẨN BIỂU ĐỒ NÂNG CAO & Ý NGHĨA THỐNG KÊ (SPORTS ANALYTICS)

Để đáp ứng gu thẩm mỹ và yêu cầu chuyên môn khắt khe của giảng viên, dashboard phải vượt lên trên các biểu đồ sơ cấp bằng hệ thống phân tích nâng cao:

### 5.1. Ma trận 4 Góc phần tư Hiệu quả Tấn công (Scatter Quadrant Plot)
* **Ý nghĩa thống kê:** Chuyển từ thống kê mô tả đơn biến sang **phân tích tương quan đa biến (Multivariate Analysis)** giữa 3 biến định lượng: $X = \text{Assists}$, $Y = \text{Goals}$, $\text{Size} = \text{Minutes Played}$ và 1 biến phân loại $\text{Color} = \text{Main Position}$.
* **Kháng ngoại lai (Robust Statistics):** Sử dụng **2 đường tham chiếu Trung vị (Median Reference Lines)** thay vì Trung bình (Mean) để loại trừ ảnh hưởng bóp méo của các Outlier ghi 30-40 bàn (Haaland, Mbappé).
* **Phân loại chiến thuật 4 góc phần tư:**
  * *Góc I (Top-Right):* **Siêu sao Toàn diện** (High Goals, High Assists - Kane, Salah).
  * *Góc II (Top-Left):* **Sát thủ Vòng cấm** (High Goals, Low Assists - Haaland).
  * *Góc III (Bottom-Right):* **Nhạc trưởng Kiến thiết** (Low Goals, High Assists - De Bruyne).
  * *Góc IV (Bottom-Left):* **Cầu thủ Hỗ trợ / Dự bị xoay tua**.

### 5.2. Thước đo tỷ suất chuẩn hóa `Mins Per Goal`
* Thước đo $R = \frac{\text{Minutes Played}}{\text{Goals}}$ khử hoàn toàn **sai số về thời lượng ra sân (Exposure Time Bias)**, đánh giá công bằng hiệu quả của cầu thủ đá chính lẫn cầu thủ dự bị bùng nổ.

### 5.3. Bản đồ Phân tầng Đa cấp (Hierarchical Treemap Drill-down) thay thế Decomposition Tree
* **Khắc phục giới hạn kỹ thuật:** Trên kết nối **Live Connection tới SSAS Multidimensional (MDX)**, visual AI *Decomposition Tree* thường phát sinh lỗi hệ thống (*"Something's wrong with the visual"*) do tầng phiên dịch DAX-MDX không hỗ trợ thuật toán chia nhánh tự động.
* **Giải pháp chuẩn hóa:** Sử dụng **Treemap Drill-down** phân tích cơ cấu tỷ trọng đa tầng Part-to-Whole: Cho phép người dùng đào sâu phân tích từ `Giải đấu` $\rightarrow$ `Vị trí thi đấu` $\rightarrow$ `Câu lạc bộ` $\rightarrow$ `Cầu thủ cụ thể` một cách mượt mà, ổn định tuyệt đối $100\%$.

### 5.4. Bảng Ma trận Tích hợp Mini Data Bars & Heatmap
* Tích hợp thanh tiến độ trực quan **Data Bars** trong cột `Bàn thắng` và dải màu **Heatmap** trong cột `Tổng G+A`. Tắt `Stepped layout` để bảng hiển thị dạng phẳng chuyên nghiệp như báo cáo điều hành tài chính.

---

## 6. GIẢI QUYẾT BÀI TOÁN NGHIỆP VỤ THỰC TẾ (REAL-WORLD VALUE)

Mọi biểu đồ trên Báo biểu 1 phải trả lời trực tiếp cho 3 bài toán quyết định của ban lãnh đạo CLB bóng đá:
1. **Bài toán Tuyển trạch Moneyball:** Tìm kiếm các cầu thủ có hiệu suất số phút/bàn thắng cực thấp (dưới 110 phút/bàn) nhưng thời lượng ra sân chưa nhiều $\rightarrow$ Đây là những món hời chuyển nhượng bị định giá thấp.
2. **Bài toán Định hình Chiến thuật Tuyển dụng:** Giúp HLV xác định chính xác đội bóng đang thiếu mẫu trung phong độc lập (Góc II) hay tiền vệ liên kết lối chơi (Góc I & III) để mua đúng người.
3. **Bài toán Quản trị Rủi ro Phụ thuộc (Concentration Risk):** Phát hiện CLB có đang phụ thuộc quá 60% bàn thắng vào một ngôi sao duy nhất hay không để chủ động phương án dự phòng khi chấn thương.

---

## 7. QUY TẮC KỸ THUẬT & KIỂM TRA THỰC TẾ (CLEAN TESTING PROTOCOL)

1. **Đồng bộ 3 chiều tuyệt đối:** Mã MDX trong SSMS, thao tác kéo thả trên Power BI và tài liệu hướng dẫn Markdown (`power-bi/02_power_bi_bao_bieu_1.md`) phải ăn khớp 100% về số lượng dòng, cột, tọa độ và con số thực tế.
2. **Quy tắc dọn dẹp Workspace:** Mọi script kiểm tra tạm thời trong terminal phải được xóa hoàn toàn sau khi chạy, giữ workspace luôn sạch sẽ.
3. **Đồng bộ GitHub:** Mọi cập nhật trong file PBIX và tài liệu MD phải được commit và push lên nhánh `main` với commit message chuẩn Conventional Commits (`feat:`, `docs:`, `fix:`).

---

## 8. QUY TẮC KIẾN TRÚC KẾT NỐI: LIVE CONNECTION VS IMPORT MODE TRONG ĐỒ ÁN OLAP & RÀNG BUỘC KỸ THUẬT

### 8.1. Tại sao đồ án OLAP bắt buộc dùng Live Connection?
* **Mục tiêu học thuật:** Khẳng định sự thông suốt của toàn bộ quy trình từ ETL (SSIS) $\rightarrow$ Kho dữ liệu (DW SQL Server) $\rightarrow$ Khối đa chiều (SSAS Multidimensional Cube) $\rightarrow$ Lớp trực quan hóa (Power BI).
* **Single Source of Truth (Điểm tin cậy duy nhất):** Mọi logic tính toán (Aggregations, Hierarchies, Measures) được quản trị tập trung tại SSAS Server. File `.pbix` đóng vai trò là tầng Presentation mỏng (Thin Client), dung lượng cực nhẹ và không sao chép trùng lặp dữ liệu vào bộ nhớ máy cục bộ.
* **So sánh với Import Mode thực tế:** Trong doanh nghiệp hiện nay, 90% dự án dùng *Import Mode* hoặc *Direct Lake (Fabric Semantic Model)* vì cho phép viết DAX tự do, tạo Calculated Columns/Tables và hỗ trợ 100% visual AI. Tuy nhiên, trong đồ án môn học Kho dữ liệu & OLAP, chuyển sang Import Mode sẽ làm mất đi ý nghĩa thực nghiệm của việc xây dựng Cube SSAS.

### 8.2. Các ràng buộc kỹ thuật bất khả xâm phạm khi dùng Live Connection (SSAS Multidimensional):
1. **$100\%$ sử dụng Measures và Dimensions ĐÃ CÓ SẴN trong Cube:** Không thể viết thêm Calculated Columns trong Power BI, không tự ý thêm các measure mà Cube chưa hỗ trợ. Mọi thước đo phải lấy trực tiếp từ khối Cube `[DW Football Transfermarkt]`.
2. **Tuyệt đối không lọc thẻ Card bằng Measure:** Trong Live Connection, kéo một Measure (như `Is Home Game`) vào bộ lọc visual của thẻ Card sẽ kích hoạt phép tính trên Grand Total (toàn giải) dẫn đến giá trị bị `(Blank)`. Muốn lọc, chỉ được lọc bằng **Dimension Attribute Hierarchy** (như `Season`, `Competition Name`, `Main Position`).
3. **Không dùng các Visual AI không tương thích MDX:** *Decomposition Tree*, *Key Influencers*, *Q&A* sinh ra các truy vấn DAX nâng cao không thể dịch chuẩn sang ngôn ngữ MDX của SSAS Multidimensional. Bắt buộc thay bằng **Hierarchical Treemap Drill-down** hoặc **Matrix**.
4. **Chuẩn hóa đặt tên hiển thị (Rename for this visual):** Mọi trường kéo thả từ Cube vào visual bắt buộc phải nhấp chuột phải chọn `Rename for this visual` để đổi tên tiếng Việt chuẩn hóa, loại bỏ hoàn toàn các tiền tố kỹ thuật `DIM...`, `FACT...` và triệt tiêu dấu ba chấm (`...`).
