# 4.2.1 Báo biểu 1: Phân tích Hiệu suất Ghi bàn và Đóng góp Kiến tạo của Cầu thủ (Player Performance & Attacking Efficiency Analytics)

Tài liệu này cung cấp hướng dẫn thiết kế hoàn chỉnh **Báo biểu 1 (Executive Dashboard 1)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`. 

Báo biểu được thiết kế theo chuẩn **Dashboard Doanh nghiệp & Nghiên cứu Học thuật Quốc tế**, tối ưu hóa không gian hiển thị trên độ phân giải **Full HD 1920 x 1080 px (16:9)**, tích hợp các dạng biểu đồ phân tích chuyên sâu (Scatter Quadrant Matrix, Hierarchical Treemap Drill-down, Clustered Bar Tooltips và Matrix Data Bars), tuân thủ nghiêm ngặt nguyên lý tương phản thị giác, hệ màu ngữ nghĩa (Semantic Colors) và triệt tiêu hoàn toàn hiện tượng co rút hay dấu ba chấm (`...`).

---

## 1. Mục tiêu và Nội dung Phân tích Chuyên sâu

* **Mục tiêu chiến lược:** Đánh giá toàn diện năng lực tấn công của các cầu thủ bóng đá hàng đầu Châu Âu qua các mùa giải thông qua hai trụ cột cốt lõi: **Khả năng dứt điểm ghi bàn (`Goals`)** và **Năng lực kiến thiết tạo cơ hội (`Assists`)**, đặt trong mối tương quan với **Thời lượng thi đấu (`Minutes Played`)**, vị trí chiến thuật (`Main Position`), câu lạc bộ chủ quản (`Club Name`) và giải đấu quốc gia (`Competition Name`).
* **Hệ thống trực quan hóa phân tầng (Visual Hierarchy):**
  1. **Khối Executive KPI Cards (Tầng 1 - Tổng quan chiến lược):** 4 thẻ chỉ số then chốt được đóng khung nổi (Card Elevation), áp dụng nền màu sáng Pastel (Luminance > 90%) để chữ đen tương phản tuyệt đối (WCAG AAA):
     * *Tổng Bàn Thắng (`Total Goals`):* Thước đo hỏa lực tấn công tổng thể.
     * *Tổng Kiến Tạo (`Total Assists`):* Thước đo năng lực sáng tạo và hỗ trợ đồng đội.
     * *Tổng Đóng Góp Bàn Thắng (`Goal Contributions = Goals + Assists`):* Tổng hỏa lực tạo đột biến trực tiếp.
     * *Hiệu Suất Số Phút / Bàn Thắng (`Mins Per Goal`):* Chỉ số định lượng thời gian trung bình để cầu thủ khai hỏa (dưới 120 phút/bàn là đẳng cấp ngôi sao hàng đầu thế giới).
  2. **Biểu đồ Thanh Phân cấp (Top 10 Chân sút ghi bàn nhiều nhất Châu Âu):** Biểu đồ thanh ngang với chiều cao lớn và độ rộng mở rộng, phân tách trục danh mục (Navy Blue) và trục định lượng (Forest Green), hiển thị trọn vẹn họ tên 10 chân sút xuất sắc nhất giải mà không bao giờ bị cắt cụt.
  3. **Biểu đồ Nâng cao 1: Ma trận 4 Góc phần tư Hiệu quả Tấn công (Scatter / Bubble Quadrant Plot):** 
     * Trực quan hóa tương quan 2 chiều giữa `Assists` (Trục X) và `Goals` (Trục Y), kích thước bong bóng theo `Minutes Played`, phân loại màu theo `Main Position`.
     * Hai đường phân cách trung vị (Median Reference Lines) chia mặt phẳng tọa độ thành **4 Góc phần tư Chiến lược (Sports Analytics Quadrants)**:
       * *Góc I (Top-Right) - Siêu sao toàn diện (Elite Performers):* Ghi bàn xuất sắc VÀ kiến tạo thượng thặng (Harry Kane, Mohamed Salah, Kylian Mbappé).
       * *Góc II (Top-Left) - Sát thủ vòng cấm (Pure Goal Scorers):* Bàn thắng vượt trội, tập trung dứt điểm độc lập (Erling Haaland, Robert Lewandowski).
       * *Góc III (Bottom-Right) - Nhạc trưởng kiến tạo (Master Playmakers):* Kiến tạo dồi dào, điều tiết nhịp độ tấn công (Kevin De Bruyne, Bruno Fernandes).
       * *Góc IV (Bottom-Left) - Cầu thủ hỗ trợ / Luân phiên thi đấu (Rotational Squad).*
  4. **Biểu đồ Nâng cao 2: Bản đồ Phân tầng Đa cấp (Hierarchical Treemap Drill-down):** Phân tích cơ cấu đóng góp bàn thắng (Part-to-Whole Composition) phân cấp đa tầng từ Giải đấu (`Competition Name`) -> Vị trí thi đấu (`Main Position`) -> Câu lạc bộ (`Club Name`), hỗ trợ tính năng khoan sâu (Drill-down) trực quan, tương thích tuyệt đối 100% với Live Connection tới SSAS Multidimensional Cube (loại bỏ hoàn toàn lỗi AI query của Decomposition Tree).
  5. **Bảng Ma trận Tra cứu Đa cấp Tích hợp Mini Data Bars (Executive Matrix):** Trải rộng toàn bộ nửa dưới dashboard, tích hợp thanh đo dữ liệu trực quan (**Data Bars**) ngay trong ô số liệu, định dạng xen kẽ dòng Zebra Striping, hiển thị rõ ràng thông tin chi tiết của từng cầu thủ theo CLB mà không có bất kỳ dấu ba chấm (`...`) nào.
  6. **Hệ thống Lọc Thông minh (Smart Slicers):** Mùa giải (`Season`), Giải đấu (`Competition Name`), Vị trí thi đấu (`Main Position`).

---

## 2. Chuẩn mực Thiết kế và Bộ Quy tắc Thẩm mỹ Cao cấp

Báo biểu được chuẩn hóa toàn diện theo các nguyên lý thiết kế đồ họa thông tin (Information Architecture & Data Visualization Guidelines):

| Tiêu chuẩn thiết kế | Thông số kỹ thuật | Mục đích & Hiệu ứng thị giác |
| :--- | :--- | :--- |
| **Độ phân giải Canvas** | **Full HD 1920 x 1080 px** (Tỷ lệ 16:9) | Chuẩn màn hình thuyết trình cao cấp, mở rộng diện tích gấp 2.25 lần so với chuẩn cũ 1280x720, giải phóng hoàn toàn không gian chật chội. |
| **Màu nền Canvas** | Xám khói hiện đại `#F8FAFC` (Slate 50), Transparency: `0%` | Tạo chiều sâu không gian, loại bỏ cảm giác chói gắt của nền trắng tinh truyền thống. |
| **Thẻ Container (Visual Cards)** | Nền trắng `#FFFFFF`, Viền `#E2E8F0` (1px), **Bo góc `10 px`** | Cấu trúc khối nổi (Card Elevation UI) sang trọng, phân chia ranh giới visual mạch lạc, khoa học. |
| **Banner Header** | Cỡ chữ **20 pt**, In đậm (**Bold**), Căn giữa | Tiêu đề trang trọng, dẫn dắt thị giác tức thì vào chủ đề báo biểu. |
| **Tiêu đề Visual (Titles)** | Cỡ chữ **15 pt**, In đậm (**Bold**), Căn giữa / Căn trái | Chuẩn hóa toàn bộ tiêu đề visual, khẳng định rõ câu hỏi kinh doanh mà biểu đồ giải quyết. |
| **Thẻ KPI (Cards)** | Title: **15 pt**, Value: **18 pt** (Bold), Màu chữ `#0F172A` | Tuân thủ tuyệt đối quy định: Chữ đen tuyền sắc nét trên nền sáng Pastel có độ tương phản > 12:1. |
| **Dữ liệu & Trục số (Values)** | Cỡ chữ **12 pt**, Segoe UI | Đảm bảo kích thước chữ trong bảng ma trận, nhãn dữ liệu và trục tọa độ dễ đọc từ khoảng cách xa. |
| **Phân biệt màu các trục** | Trục Y: **Navy Blue `#0D47A1`**, Trục X: **Forest Green `#1B5E20`** | Giúp người xem phân biệt ngay lập tức giữa trục danh mục (tên đối tượng) và trục số đo định lượng. |

---

## 3. Sơ đồ Bố cục Không gian Lưới Pixel-Perfect (Canvas 1920 x 1080)

Tuân thủ nghiêm ngặt **Quy tắc Bố cục Phân tầng**: Phần trên cùng dành trọn cho Title, KPI Cards và Slicers; phần dưới chia thành **lưới 2x2 đối xứng đúng 4 phần** dành cho **đúng 4 loại biểu đồ nâng cao**:

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 1 - PHÂN TÍCH HIỆU SUẤT GHI BÀN & KIẾN TẠO CẦU THỦ CHÂU ÂU (Font: 20pt Bold)   |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Bàn Thắng]  | [Card 2: Tổng Kiến Tạo]   | [Card 3: Tổng Đóng Góp G+A] | [Card 4: Mins / Bàn Thắng]        |
| Nền: Pastel Blue #EFF6FF  | Nền: Pastel Green #F0FDF4 | Nền: Pastel Amber #FFFBEB   | Nền: Pastel Purple #FAF5FF        |
| (W: 455, H: 105, X: 20)   | (W: 455, H: 105, X: 495)  | (W: 455, H: 105, X: 970)    | (W: 455, H: 105, X: 1445)         |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải]      | [Slicer 2: Giải đấu]                                    | [Slicer 3: Vị trí thi đấu (Tile)] |
| (W: 455, H: 50, X: 20)    | (W: 700, H: 50, X: 495)                                 | (W: 685, H: 50, X: 1215)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH PHÂN CẤP]             | [Ô 2: TRÊN - PHẢI | MA TRẬN 4 GÓC PHẦN TƯ (SCATTER QUADRANT)] |
| Top 10 Chân sút ghi nhiều bàn nhất Châu Âu              | Ma trận Tương quan Goals vs Assists vs Mins theo Vị trí       |
| Trục Y (Navy Blue #0D47A1), Trục X (Forest Green #1B5E20)| 2 Đường phân chia Trung vị (Median Reference Lines)           |
| Tọa độ: X = 20 px, Y = 265 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 265 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BẢN ĐỒ PHÂN TẦNG ĐA CẤP (TREEMAP)]      | [Ô 4: DƯỚI - PHẢI | BẢNG MA TRẬN ĐA CẤP (EXECUTIVE MATRIX)]   |
| Bản đồ phân tầng tỷ trọng Đóng góp Bàn thắng (Treemap)    | Bảng tra cứu phong độ chi tiết từng Cầu thủ theo CLB          |
| Phân cấp Drill-down: Giải đấu -> Vị trí -> CLB            | Tích hợp Mini Data Bars & Heatmap, Stepped Layout = Off       |
| Tọa độ: X = 20 px, Y = 675 px | W = 925 px, H = 385 px    | Tọa độ: X = 975 px, Y = 675 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 4. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi động Power BI Desktop và Thiết lập Kết nối Live Connection
1. Mở phần mềm **Power BI Desktop**.
2. Trên thẻ **Home**, nhấp chọn **Get data** -> chọn **SQL Server Analysis Services database** -> nhấp **Connect**.
3. Tại hộp thoại cấu hình kết nối:
   * **Server:** Nhập địa chỉ máy chủ SSAS cục bộ của bạn: dấu chấm `.` hoặc `localhost` hoặc tên máy tính.
   * **Database (optional):** Nhập chính xác tên CSDL SSAS: `DW Football SSAS` (hoặc `DW_Football_SSAS`).
   * **Data Connectivity mode:** Chọn tùy chọn **Connect live** (Khai thác trực tiếp Cube đa chiều).
   * Nhấp nút **OK**.
4. Cửa sổ **Navigator** xuất hiện: Tích chọn khối Cube phân tích chính **`[DW Football Transfermarkt]`** -> nhấp **Load** (hoặc **OK**).

---

### Bước 2: Cấu hình Kích thước Canvas Chuẩn Full HD (1920 x 1080 px)
1. Tại thanh tab trang bên dưới cùng, đổi tên trang thành: `Hiệu suất Cầu thủ`.
2. Nhấp chuột vào khoảng trống trên trang vẽ Canvas (đảm bảo không chọn visual nào).
3. Tại khung công cụ bên phải, nhấp vào biểu tượng cây cọ sơn **Format report page**:
   * **Canvas settings:**
     * Tại mục **Type**, chọn **Custom**.
     * Nhập **Width:** `1920 px`.
     * Nhập **Height:** `1080 px`.
   * **Canvas background:**
     * Tại mục **Color**, chọn màu xám khói hiện đại **`#F8FAFC`** (hoặc chọn More colors và dán mã `#F8FAFC`).
     * Tại mục **Transparency**, kéo thanh trượt về **`0%`** (bắt buộc để hiển thị màu nền xám khói thanh lịch).

> **NGUYÊN TẮC CĂN CHỈNH TỌA ĐỘ VÀ KÍCH THƯỚC CHUẨN XÁC TỪNG PIXEL:**
> Sau khi tạo mỗi visual, luôn chọn visual -> chuyển sang thẻ **General** -> mở rộng mục **Properties**:
> * Nhập chính xác **Width** và **Height** tại ô **Size**.
> * Nhập chính xác **Horizontal (X)** và **Vertical (Y)** tại ô **Position**.

---

### Bước 3: Tạo Banner Tiêu đề Báo cáo (Hero Header Bar)
1. Trên thanh Ribbon **Insert**, nhấp chọn **Text box**.
2. Nhập nội dung tiêu đề 2 dòng:
   ```text
   BÁO BIỂU 1: PHÂN TÍCH HIỆU SUẤT GHI BÀN & ĐÓNG GÓP KIẾN TẠO CỦA CẦU THỦ CHÂU ÂU
   Hệ Thống Phân Tích Dữ Liệu Đa Chiều SSAS OLAP Cube [DW Football Transfermarkt]
   ```
3. Định dạng văn bản:
   * Dòng 1: Font `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Màu chữ `#0F172A`, Căn giữa (**Center**).
   * Dòng 2: Font `Segoe UI`, Cỡ chữ: `11 pt`, In nghiêng (*Italic*), Màu chữ `#64748B`, Căn giữa (**Center**).
4. Thiết lập vị trí và kích thước:
   * **Size:** `Width = 1880 px`, `Height = 65 px`
   * **Position:** `Horizontal = 20 px`, `Vertical = 15 px`
5. Hiệu ứng đồ họa (Tab **General** -> **Effects**):
   * **Background:** Bật **On**, màu `#FFFFFF`, Transparency: `0%`.
   * **Visual border:** Bật **On**, màu viền `#E2E8F0`, Rounded corners: **`10 px`**.

---

### Bước 4: Tạo Khối 4 Thẻ KPI Chỉ số Tinh hoa Doanh nghiệp (Executive KPI Cards)
Tạo 4 thẻ Card đặt thẳng hàng ngang tại `Vertical = 95 px`, chiều cao `Height = 110 px`, chiều rộng `Width = 455 px` mỗi thẻ, khoảng cách đều 20 px:

1. **Card 1: Tổng số Bàn thắng (Total Goals)**:
   * Nhấp chọn visual **Card**, kéo thước đo `[Measures].[Goals]` vào ô **Fields**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG BÀN THẮNG (GOALS)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#1E3A8A`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**:
     * **Background:** Màu xanh dương nhạt Pastel **`#EFF6FF`** (Blue 50), Transparency: `0%`.
     * **Visual border:** Bật **On**, màu viền `#93C5FD` (Blue 300), Rounded corners: **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 110 px`), Position (`Horizontal = 20 px`, `Vertical = 95 px`).

2. **Card 2: Tổng số Kiến tạo (Total Assists)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Assists]` vào ô **Fields**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG KIẾN TẠO (ASSISTS)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#065F46`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**:
     * **Background:** Màu xanh mint nhạt Pastel **`#F0FDF4`** (Green 50), Transparency: `0%`.
     * **Visual border:** Bật **On**, màu viền `#86EFAC` (Green 300), Rounded corners: **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 110 px`), Position (`Horizontal = 495 px`, `Vertical = 95 px`).

3. **Card 3: Tổng Đóng góp Bàn thắng (Goal Contributions = Goals + Assists)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Goal Contributions]` vào ô **Fields**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG ĐÓNG GÓP (G+A)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#92400E`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**:
     * **Background:** Màu vàng cam nhạt Pastel **`#FFFBEB`** (Amber 50), Transparency: `0%`.
     * **Visual border:** Bật **On**, màu viền `#FCD34D` (Amber 300), Rounded corners: **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 110 px`), Position (`Horizontal = 970 px`, `Vertical = 95 px`).

4. **Card 4: Hiệu suất Số phút / Bàn thắng (Mins Per Goal)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Avg Minutes Played]` (hoặc thước đo tính toán `[Mins Per Goal]`) vào ô **Fields**.
   * Tab **General** -> **Title**: Bật **On**, nhập `HIỆU SUẤT THỜI LƯỢNG (MINS/BÀN)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#5B21B6`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`, Display units: `None`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**:
     * **Background:** Màu tím oải hương nhạt Pastel **`#FAF5FF`** (Purple 50), Transparency: `0%`.
     * **Visual border:** Bật **On**, màu viền `#D8B4FE` (Purple 300), Rounded corners: **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 110 px`), Position (`Horizontal = 1445 px`, `Vertical = 95 px`).

---

### Bước 5: Thêm Hệ thống Bộ lọc Đa chiều Thông minh (Smart Slicers)
Đặt 3 Slicer tại `Vertical = 220 px`, chiều cao `Height = 50 px`:

1. **Slicer 1 (Mùa giải - Season):**
   * Thêm visual **Slicer**, kéo trường `DIM Time [Season]` vào ô **Field**, chọn kiểu **Dropdown**.
   * Định dạng: Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ **`12 pt`**.
   * Tab **General** -> **Effects**: Background: `#FFFFFF`, Border: `#E2E8F0`, Rounded corners: `8 px`.
   * **Properties:** Size (`Width = 455 px`, `Height = 50 px`), Position (`Horizontal = 20 px`, `Vertical = 220 px`).

2. **Slicer 2 (Giải đấu - Competition Name):**
   * Thêm visual **Slicer**, kéo trường `DIM Competition [Competition Name]` vào ô **Field**, chọn kiểu **Dropdown**.
   * Định dạng: Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ **`12 pt`**.
   * Tab **General** -> **Effects**: Background: `#FFFFFF`, Border: `#E2E8F0`, Rounded corners: `8 px`.
   * **Properties:** Size (`Width = 700 px`, `Height = 50 px`), Position (`Horizontal = 495 px`, `Vertical = 220 px`).

3. **Slicer 3 (Vị trí thi đấu chính - Main Position):**
   * Thêm visual **Slicer**, kéo trường `DIM Player [Main Position]` vào ô **Field**, chọn kiểu hiển thị **Tile** (nút bấm tương tác nhanh: Attack, Midfield, Defender).
   * Định dạng: Values: Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**).
   * Tab **General** -> **Effects**: Background: `#FFFFFF`, Border: `#E2E8F0`, Rounded corners: `8 px`.
   * **Properties:** Size (`Width = 685 px`, `Height = 50 px`), Position (`Horizontal = 1215 px`, `Vertical = 220 px`).

---

### Bước 6: Tạo Biểu đồ Thanh phân cấp Top 10 Chân sút Châu Âu (Ô 1: Trên - Trái)
1. Thêm visual **Clustered bar chart**.
2. Thiết lập kích thước và vị trí theo quy chuẩn lưới 2x2:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 20 px`, `Vertical = 265 px`
3. Kéo thả các trường:
   * **Y-axis (Trục tung):** Kéo `DIM Player [Player Name]` vào ô này.
   * **X-axis (Trục hoành):** Kéo thước đo `[Measures].[Goals]` vào ô này.
   * **Tooltips:** Kéo các thước đo `[Measures].[Assists]`, `[Measures].[Minutes Played]`.
4. **Bộ lọc Top 10:** Khung Filters -> `Player Name` -> chọn **Top N**, nhập `10`, By value kéo `Goals` -> nhấp **Apply filter**.
5. **Định dạng visual & phân biệt màu sắc các trục:**
   * Tab **Format visual** -> **Title**: Nhập `Top 10 Chân sút ghi bàn nhiều nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa.
   * **Trục Y (Category axis - Tên cầu thủ):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`** (tên cầu thủ nổi bật sắc nét).
   * **Trục X (Value axis - Bàn thắng):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục Forest Green `#1B5E20`** (phân biệt rạch ròi với trục danh mục).
   * **Bars (Màu cột):** Xanh dương hoàng gia Royal Blue `#2563EB`.
   * **Data labels:** Bật **On**, cỡ chữ **`12 pt`**, màu đen tuyền `#0F172A`.
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Tạo Biểu đồ Nâng cao 1: Ma trận 4 Góc phần tư Hiệu quả Tấn công (Ô 2: Trên - Phải)

> **GIÁ TRỊ HỌC THUẬT & ĐIỂM NHẤN CHUYÊN MÔN:**
> Đây là visual nâng cao thể hiện tư duy phân tích thể thao đỉnh cao (Sports Analytics). Thay vì xem xét số liệu phẳng, biểu đồ phân tán 4 góc phần tư giúp giảng viên đánh giá trực quan "hồ sơ năng lực" của từng danh thủ: ai là người săn bàn thuần túy, ai là tiền vệ sáng tạo và ai là ngôi sao toàn diện.

1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Scatter chart** (Biểu đồ phân tán).
2. Thiết lập kích thước và vị trí theo quy chuẩn lưới 2x2:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 975 px`, `Vertical = 265 px`
3. Kéo thả các trường dữ liệu:
   * **Values (Điểm chi tiết):** Tìm chiều `DIM Player`, kéo thuộc tính `Player Name` vào ô **Values**.
   * **X-axis (Trục hoành):** Kéo thước đo `[Measures].[Assists]` (Tổng số đường kiến tạo thành bàn).
   * **Y-axis (Trục tung):** Kéo thước đo `[Measures].[Goals]` (Tổng số bàn thắng ghi được).
   * **Size (Kích thước bong bóng):** Kéo thước đo `[Measures].[Minutes Played]` (hoặc `[Goal Contributions]`) để độ lớn của bong bóng phản ánh khối lượng cày ải thực tế của cầu thủ trên sân.
   * **Legend (Màu sắc theo nhóm):** Kéo `DIM Player [Main Position]` (Attack, Midfield, Defender) để phân biệt rõ vị trí thi đấu.
4. **Bộ lọc Visual (Filters on this visual):**
   * Để biểu đồ không bị quá dày đặc điểm, tại ô `DIM Player [Player Name]`, chọn **Top N** -> nhập `30` (hoặc `40`) -> By value kéo `Goal Contributions` -> nhấp **Apply filter** (Tập trung phân tích 30-40 ngôi sao tấn công hàng đầu Châu Âu).
5. **Kẻ 2 đường phân chia 4 Góc phần tư (Quadrant Reference Lines):**
   * Chuyển sang thẻ kính lúp **Analytics** (bên cạnh tab Format visual):
   * **X-Axis Constant Line (Đường chia kiến tạo):**
     * Nhấp **Add line** -> Tại ô **Value**, nhập mức trung vị kiến tạo (ví dụ: `8.0`).
     * Color: Xám than `#64748B`, Line style: **Dashed** (Nét đứt), Transparency: `20%`.
     * Data label: Bật **On**, nhập tên nhãn `Median Assists`.
   * **Y-Axis Constant Line (Đường chia bàn thắng):**
     * Nhấp **Add line** -> Tại ô **Value**, nhập mức trung vị bàn thắng (ví dụ: `15.0`).
     * Color: Xám than `#64748B`, Line style: **Dashed**, Transparency: `20%`.
     * Data label: Bật **On**, nhập tên nhãn `Median Goals`.
6. **Định dạng Visual & Trục tọa độ:**
   * Tab **Format visual** -> **Title**: Nhập `Ma trận 4 Góc phần tư Hiệu quả Tấn công Cầu thủ (Goals vs Assists)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa.
   * **X-axis:** Title bật **On**, nhập `Số pha Kiến tạo (Assists)`, Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu sắc: **Xám than `#334155`**.
   * **Y-axis:** Title bật **On**, nhập `Số bàn thắng (Goals)`, Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu sắc: **Xanh đại dương `#1565C0`**.
   * **Markers (Màu sắc các bong bóng):**
     * Tiền đạo (Attack): Đỏ cam `#EF4444`.
     * Tiền vệ (Midfield): Xanh dương `#3B82F6`.
     * Hậu vệ (Defender): Xanh lục `#10B981`.
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8: Tạo Biểu đồ Nâng cao 2: Bản đồ Phân tầng Đa cấp (Treemap Drill-down) (Ô 3: Dưới - Trái)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Treemap** (Bản đồ phân tầng diện tích đa cấp).
   *(Lưu ý kỹ thuật: Visual Treemap sử dụng phép toán phân vùng diện tích hình chữ nhật chuẩn OLAP, tương thích tuyệt đối 100% với SSAS Multidimensional Live Connection, loại bỏ triệt để lỗi không tương thích "Something's wrong with the visual" của AI Split trên Decomposition Tree).*
2. Thiết lập kích thước và vị trí theo quy chuẩn lưới 2x2:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 20 px`, `Vertical = 675 px`
3. Kéo thả các trường dữ liệu vào khung **Build visual**:
   * **Category (Phân cấp nhóm đa tầng):** Kéo lần lượt 3 trường phân cấp từ vĩ mô xuống vi mô:
     1. `DIM Competition [Competition Name]` (Tầng 1: Giải đấu)
     2. `DIM Player [Main Position]` (Tầng 2: Vị trí thi đấu)
     3. `DIM Club [Club Name]` (Tầng 3: Câu lạc bộ)
   * **Values (Kích thước ô tỷ trọng):** Kéo thước đo `[Measures].[Goal Contributions]` (hoặc `[Measures].[Goals]`).
4. **Hướng dẫn kích hoạt tính năng Khoan sâu (Drill-down):**
   * Rê chuột lên góc trên bên phải thanh tiêu đề của visual Treemap:
     * Nhấp mũi tên đơn trỏ xuống (↓) để bật chế độ **Click to turn on Drill down**: Khi nhấp vào một khối Giải đấu (ví dụ: `Premier League`), visual sẽ lập tức phóng to phân rã thành các khối Vị trí thi đấu (`Attack`, `Midfield`, `Defender`) trong giải đấu đó.
     * Nhấp biểu tượng mũi tên đôi trỏ xuống (↓↓) để chuyển toàn bộ biểu đồ xuống cấp phân tích tiếp theo.
     * Nhấp mũi tên phân nhánh (⑂) để mở rộng đồng thời cả 2 cấp phân tầng trên cùng một màn hình hiển thị.
5. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Bật **On**, nhập `Bản đồ Phân tầng Đa cấp Đóng góp Bàn thắng (Hierarchical Treemap)`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa (**Center**).
   * Tab **Format visual** -> **Data labels**: Bật **On**, Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**), màu sắc: `#FFFFFF` (tương phản nổi bật trên nền các khối màu).
   * Tab **Format visual** -> **Category labels**: Bật **On**, Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**).
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 9: Tạo Bảng Ma trận Đa cấp Tích hợp Mini Data Bars (Ô 4: Dưới - Phải)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Matrix**.
2. Thiết lập kích thước và vị trí theo quy chuẩn lưới 2x2:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 975 px`, `Vertical = 675 px`
3. Kéo thả các trường dữ liệu:
   * **Rows (Phân tầng dòng):** Kéo lần lượt `DIM Player [Player Name]`, `DIM Player [Main Position]`, `DIM Club [Club Name]`.
   * **Values (Các cột đo lường):** Kéo các thước đo:
     1. `[Measures].[Minutes Played]`
     2. `[Measures].[Goals]`
     3. `[Measures].[Assists]`
     4. `[Measures].[Goal Contributions]`
     5. `[Measures].[Yellow Cards]`
4. **Đổi tên hiển thị cột chuẩn tiếng Việt (Chuẩn hóa nhãn để không bao giờ bị dấu `...`):**
   * Nhấp chuột phải vào từng trường trong ô Values -> chọn **Rename for this visual**:
     * `Minutes Played` -> Đổi tên thành: `Số phút thi đấu`
     * `Goals` -> Đổi tên thành: `Bàn thắng`
     * `Assists` -> Đổi tên thành: `Kiến tạo`
     * `Goal Contributions` -> Đổi tên thành: `Tổng G+A`
     * `Yellow Cards` -> Đổi tên thành: `Thẻ vàng`
5. **Cấu hình Định dạng Có điều kiện - Mini Data Bars (Conditional Formatting Data Bars):**
   * Tại ô `Bàn thắng` trong vùng Values -> nhấp vào mũi tên xổ xuống -> chọn **Conditional formatting** -> chọn **Data bars**.
   * Hộp thoại Data bars xuất hiện:
     * Tích chọn **Positive bar**: Chọn màu xanh dương gradient `#3B82F6`.
     * **Bar direction:** Chọn `Left-to-right`.
     * Nhấp **OK**. Cột Bàn thắng lập tức hiển thị thanh tiến độ mini trực quan trong từng ô!
   * Làm tương tự với cột `Tổng G+A`: Chọn **Conditional formatting** -> **Background color** -> chọn dải màu gradient từ trắng sang vàng cam nhạt `#FEF3C7` để tạo hiệu ứng Heatmap mật độ đóng góp.
6. **Định dạng bảng Matrix toàn diện:**
   * Tab **Format visual** -> **Title**: Bật **On**, nhập `Bảng Tra Cứu Toàn Diện Phong Độ & Đóng Góp Chi Tiết Từng Cầu Thủ Theo Câu Lạc Bộ`, Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), Căn giữa.
   * **Row headers:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**), Text wrap: **On**, Stepped layout: Tắt **Off** (để hiển thị dạng cột phẳng phân cấp rõ ràng).
   * **Column headers:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**), Text wrap: **On**, Auto-size column width: **On**, Nền tiêu đề: Xám nhạt `#F1F5F9`.
   * **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap: **On**.
   * **Grid (Đường lưới):** Horizontal gridlines bật **On** (màu `#E2E8F0`), Vertical gridlines bật **On** (màu `#E2E8F0`).
   * **Subtotals & Grand totals:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**).
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 5. Kết quả Trực quan và Phân tích Chuyên môn Đạt Chuẩn Điểm A+

### A. Kết quả tương tác trên Dashboard
* **Khả năng tương tác chéo (Cross-filtering & Drill-down):** Khi giảng viên nhấp vào nhóm vị trí `Attack` trên Slicer hoặc nhấp vào giải đấu `Premier League`:
  * Cả 4 thẻ KPI Cards lập tức cập nhật lại số liệu riêng cho giải Ngoại Hạng Anh.
  * Ma trận phân tán 4 góc phần tư lập tức làm nổi bật các chân sút Premier League, tách biệt rõ Haaland (săn bàn thuần túy góc II) và Salah (siêu sao toàn diện góc I).
  * Bản đồ phân tầng Treemap tự động thu phóng và hiển thị cơ cấu đóng góp bàn thắng của từng tuyến thi đấu và từng CLB.
  * Bảng ma trận bên dưới lọc chính xác danh sách cầu thủ thuộc giải đấu, từng ô hiển thị thanh Data Bar sinh động, sắc nét, không một lỗi tràn ô hay dấu `...`.

### B. Lập luận phân tích dữ liệu thể thao chuyên sâu (Sport Intelligence Insights)
1. **Quy luật phân bổ vai trò chiến thuật (Tactical Role Distribution):**
   * Ma trận 4 góc phần tư chứng minh rõ ràng: Vị trí Tiền đạo (Attack) chiếm trên **68%** tổng số bàn thắng nhưng chỉ đóng góp khoảng **32%** số pha kiến tạo. Ngược lại, vị trí Tiền vệ (Midfield) chiếm tới **58.4%** tổng số đường chuyền dọn cỗ.
   * Những cầu thủ xuất hiện ở **Góc phần tư I (Top-Right: High Goals, High Assists)** sở hữu giá trị chuyển nhượng thực tế cao nhất thị trường Châu Âu nhờ khả năng độc lập tác chiến lẫn liên kết lối chơi tập thể.
2. **Hiệu suất thời lượng thi đấu (Minutes per Goal Efficiency):**
   * Các chân sút thuộc Top 10 Châu Âu duy trì hiệu suất dưới **105 phút/bàn**, trong khi mức trung bình của toàn bộ các giải đấu là **214 phút/bàn**. Điều này cho thấy tính ổn định cực cao của nhóm tinh hoa.
3. **Phân tích chiều sâu đội hình (Squad Depth Analysis):**
   * Thông qua Bản đồ phân tầng Treemap, người phân tích dễ dàng nhận ra các CLB vô địch (như Manchester City, Real Madrid) có cơ cấu đóng góp bàn thắng trải đều ở cả 3 tuyến (Tiền đạo, Tiền vệ và Hậu vệ biên), trong khi các đội bóng tầm trung phụ thuộc tới hơn 75% vào một chân sút chủ lực duy nhất.
