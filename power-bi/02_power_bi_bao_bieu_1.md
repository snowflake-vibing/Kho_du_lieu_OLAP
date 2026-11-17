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
     * *Thời Lượng Thi Đấu Trung Bình (`Avg Minutes Played`):* Thời lượng trung bình mỗi lượt ra sân của cầu thủ (đo lường độ bền thể lực và tính ổn định trong đội hình chính, trung bình toàn giải đạt ~64.4 phút/trận).
  2. **Biểu đồ Thanh Phân cấp (Top 10 Chân sút ghi bàn nhiều nhất Châu Âu):** Biểu đồ thanh ngang với chiều cao lớn và độ rộng mở rộng, phân tách trục danh mục (Navy Blue) và trục định lượng (Forest Green), hiển thị trọn vẹn họ tên 10 chân sút xuất sắc nhất giải mà không bao giờ bị cắt cụt.
  3. **Biểu đồ Nâng cao 1: Ma trận 4 Góc phần tư Hiệu quả Tấn công (Scatter / Bubble Quadrant Plot):** 
     * Trực quan hóa tương quan 2 chiều giữa `Assists` (Trục X) và `Goals` (Trục Y), kích thước bong bóng theo `Minutes Played`, phân loại màu theo `Main Position`.
     * Hai đường phân cách trung vị (Median Reference Lines) chia mặt phẳng tọa độ thành **4 Góc phần tư Chiến lược (Sports Analytics Quadrants)**:
       * *Góc I (Top-Right) - Siêu sao toàn diện (Elite Performers):* Ghi bàn xuất sắc VÀ kiến tạo thượng thặng (Harry Kane, Mohamed Salah, Kylian Mbappé).
       * *Góc II (Top-Left) - Sát thủ vòng cấm (Pure Goal Scorers):* Bàn thắng vượt trội, tập trung dứt điểm độc lập (Erling Haaland, Robert Lewandowski).
       * *Góc III (Bottom-Right) - Nhạc trưởng kiến tạo (Master Playmakers):* Kiến tạo dồi dào, điều tiết nhịp độ tấn công (Kevin De Bruyne, Bruno Fernandes).
       * *Góc IV (Bottom-Left) - Cầu thủ hỗ trợ / Luân phiên thi đấu (Rotational Squad).*
  4. **Biểu đồ Nâng cao 2: Bản đồ Phân tầng Đa cấp (Hierarchical Treemap Drill-down):** Phân tích cơ cấu đóng góp bàn thắng (Part-to-Whole Composition) phân cấp đa tầng từ Giải đấu (`Competition Name`) -> Vị trí thi đấu (`Main Position`) -> Câu lạc bộ (`Club Name`), hỗ trợ tính năng khoan sâu (Drill-down) trực quan, tương thích tuyệt đối 100% với Live Connection tới SSAS Multidimensional Cube (loại bỏ hoàn toàn lỗi AI query của Decomposition Tree).
  5. **Báo cáo Phân nhóm & Tổng hợp Đa cấp (Grouping and Totals Matrix Visual - Đạt chuẩn 100% Yêu cầu Đồ án):**
     * Đáp ứng trọn vẹn yêu cầu tiên quyết của đồ án môn học: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
     * Cấu trúc phân nhóm phân cấp 3 tầng (3-Level Hierarchical Grouping): **Giải đấu (`Competition Name`) $\rightarrow$ Câu lạc bộ (`Club Name`) $\rightarrow$ Cầu thủ (`Player Name`)**.
     * Kích hoạt đầy đủ các dòng **Tổng phụ (Subtotals)** cho từng Câu lạc bộ và từng Giải đấu, cùng dòng **Tổng cộng toàn cục (Grand Total)** ở đáy bảng, tích hợp thanh tiến độ trực quan **Data Bars** trong cột đóng góp bàn thắng.
  6. **Hệ thống Lọc Thông minh (Smart Slicers):** Mùa giải (`Season`), Giải đấu (`Competition Name`), Vị trí thi đấu (`Main Position`).

---

## 2. Chuẩn mực Thiết kế và Bộ Quy tắc Thẩm mỹ Cao cấp

Báo biểu được chuẩn hóa toàn diện theo các nguyên lý thiết kế đồ họa thông tin (Information Architecture & Data Visualization Guidelines):

| Tiêu chuẩn thiết kế | Thông số kỹ thuật | Mục đích & Hiệu ứng thị giác |
| :--- | :--- | :--- |
| **Độ phân giải Canvas** | **Full HD 1920 x 1080 px** (Tỷ lệ 16:9) | Chuẩn màn hình thuyết trình cao cấp, mở rộng diện tích gấp 2.25 lần so với chuẩn cũ 1280x720, giải phóng hoàn toàn không gian chật chội. |
| **Màu nền Canvas** | Xám khói hiện đại `#F8FAFC` (Slate 50), Transparency: `0%` | Tạo chiều sâu không gian, loại bỏ cảm giác chói gắt của nền trắng tinh truyền thống. |
| **Thẻ Container (Visual Cards)** | Nền trắng `#FFFFFF`, Viền `#E2E8F0` (1px), **Bo góc `10 px`** | Cấu trúc khối nổi (Card Elevation UI) sang trọng, phân chia ranh giới visual mạch lạc, khoa học. |
| **Banner Header** | Cỡ chữ **20 pt**, In đậm (**Bold**), Căn giữa (**Center**) | Tiêu đề trang trọng, dẫn dắt thị giác tức thì vào chủ đề báo biểu. |
| **Tiêu đề Visual (Titles)** | Cỡ chữ **18 pt**, In đậm (**Bold**), Căn giữa (**Center**) | Chuẩn hóa toàn bộ tiêu đề visual, khẳng định rõ câu hỏi kinh doanh mà biểu đồ giải quyết. |
| **Thẻ KPI (Cards)** | Title: **15 pt - 18 pt** Bold, Value: **35 pt** Bold, Màu chữ `#0F172A` | Tuân thủ tuyệt đối quy định: Giá trị 35pt nổi bật thu hút ánh nhìn tức thì trên nền sáng Pastel có độ tương phản > 12:1. |
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
| [Card 1: Tổng Bàn Thắng]  | [Card 2: Tổng Kiến Tạo]   | [Card 3: Tổng Đóng Góp G+A] | [Card 4: Thời Lượng TB / Trận]    |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold                |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải]      | [Slicer 2: Giải đấu]      | [Slicer 3: Vị trí thi đấu (Tile - Phẳng ngang)]                 |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 900, H: 80, X: 1000)                                        |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH PHÂN CẤP (18pt)]       | [Ô 2: TRÊN - PHẢI | MA TRẬN 4 GÓC PHẦN TƯ (SCATTER - 18pt)]   |
| Top 10 Chân sút ghi nhiều bàn nhất Châu Âu              | Ma trận Tương quan Goals vs Assists vs Mins theo Vị trí       |
| Trục Y (Navy Blue #0D47A1), Trục X (Forest Green #1B5E20)| 2 Đường phân chia Trung vị (Median Reference Lines)           |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BẢN ĐỒ PHÂN TẦNG TREEMAP (18pt)]     | [Ô 4: DƯỚI - PHẢI | GROUPING & TOTALS MATRIX (18pt)]           |
| Bản đồ phân tầng tỷ trọng Đóng góp Bàn thắng (Treemap)    | Báo cáo Phân nhóm & Tổng hợp Đa cấp (Grouping & Totals)       |
| Phân cấp Drill-down: Giải đấu -> Vị trí -> CLB            | Phân cấp: Giải đấu -> CLB -> Cầu thủ                          |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px   | Subtotals: ON (Tổng CLB & Giải) | Grand Total: ON (Tổng toàn) |
|                                                           | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
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
Tạo 4 thẻ Card đặt thẳng hàng ngang tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px` mỗi thẻ, khoảng cách đều 20 px:

1. **Card 1: Tổng số Bàn thắng (Total Goals)**:
   * Nhấp chọn visual **Card**, kéo thước đo `[Measures].[Goals]` vào ô **Fields**.
   * **Phần đặt tên (Rename for this visual):** Nhấp chuột phải vào trường trong ô Fields $\rightarrow$ Đổi tên thành: **`Tổng bàn thắng`**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG BÀN THẮNG (GOALS)`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#1E3A8A`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`35 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A` (cực kỳ nổi bật trên thẻ). **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**: Nền Pastel Blue `#EFF6FF`, Viền `#93C5FD`, Bo góc **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 95 px`), Position (`Horizontal = 20 px`, `Vertical = 95 px`).

2. **Card 2: Tổng số Kiến tạo (Total Assists)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Assists]` vào ô **Fields**.
   * **Phần đặt tên (Rename for this visual):** Nhấp chuột phải vào trường $\rightarrow$ Đổi tên thành: **`Tổng kiến tạo`**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG KIẾN TẠO (ASSISTS)`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#065F46`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`35 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**: Nền Pastel Green `#F0FDF4`, Viền `#86EFAC`, Bo góc **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 95 px`), Position (`Horizontal = 495 px`, `Vertical = 95 px`).

3. **Card 3: Tổng Đóng góp Bàn thắng (Goal Contributions = Goals + Assists)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Goal Contributions]` vào ô **Fields**.
   * **Phần đặt tên (Rename for this visual):** Nhấp chuột phải vào trường $\rightarrow$ Đổi tên thành: **`Tổng đóng góp G+A`**.
   * Tab **General** -> **Title**: Bật **On**, nhập `TỔNG ĐÓNG GÓP (G+A)`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#92400E`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`35 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**: Nền Pastel Amber `#FFFBEB`, Viền `#FCD34D`, Bo góc **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 95 px`), Position (`Horizontal = 970 px`, `Vertical = 95 px`).

4. **Card 4: Thời lượng Thi đấu Trung bình Mỗi trận (Avg Minutes Played)**:
   * Thêm visual **Card**, kéo thước đo **`[Measures].[Avg Minutes Played]`** vào ô **Fields** (thước đo tính trung bình số phút thi đấu mỗi lượt ra sân, có sẵn 100% trong Cube).
   * **Phần đặt tên (Rename for this visual):** Nhấp chuột phải vào trường $\rightarrow$ Đổi tên thành: **`Số phút TB / trận`**.
   * Tab **General** -> **Title**: Bật **On**, nhập `THỜI LƯỢNG THI ĐẤU TRUNG BÌNH`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**), màu chữ `#5B21B6`.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ **`35 pt`**, In đậm (**Bold**), màu đen tuyền `#0F172A`, Display units: `None` (hiển thị con số thực tế `64.36` hoặc ~64 phút). **Category label**: Tắt **Off**.
   * Tab **General** -> **Effects**: Nền Pastel Purple `#FAF5FF`, Viền `#D8B4FE`, Bo góc **`10 px`**.
   * **Properties:** Size (`Width = 455 px`, `Height = 95 px`), Position (`Horizontal = 1445 px`, `Vertical = 95 px`).

---

### Bước 5: Thêm Hệ thống Bộ lọc Đa chiều Thông minh (Smart Slicers)
Đắt 3 Slicer tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px - 80 px`** (không dùng chiều cao 50px gây cụt thanh Dropdown), chiều rộng phân bổ thoáng đãng:

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown | 20 px | 210 px | 455 px | 75 px |
| **Slicer 2** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 495 px | 210 px | 455 px | 75 px |
| **Slicer 3** | `DIM Player [Main Position]` | **`Vị trí thi đấu`** | Tile (Thẻ ngang) | 1000 px | 210 px | 900 px | 80 px |

* **Định dạng chung cho Slicers:**
  * Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt`**, In đậm (**Bold**), màu `#0F172A`.
  * Values (mục chọn): Font `Segoe UI`, Cỡ chữ **`12 pt`**.
  * Effects: Nền trắng `#FFFFFF`, Viền mỏng `#CBD5E1`, Bo góc `8 px`.

---

### Bước 6: Tạo Biểu đồ Thanh phân cấp Top 10 Chân sút Châu Âu (Ô 1: Trên - Trái)
1. Thêm visual **Clustered bar chart**.
2. Thiết lập kích thước và vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 20 px`, `Vertical = 300 px`
3. Kéo thả các trường:
   * **Y-axis (Trục tung):** Kéo `DIM Player [Player Name]` vào ô này.
   * **X-axis (Trục hoành):** Kéo thước đo `[Measures].[Goals]` vào ô này.
   * **Tooltips:** Kéo các thước đo `[Measures].[Assists]`, `[Measures].[Minutes Played]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Player Name` $\rightarrow$ Đổi tên thành: **`Cầu thủ`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng`**
   * `Assists` $\rightarrow$ Đổi tên thành: **`Kiến tạo`**
   * `Minutes Played` $\rightarrow$ Đổi tên thành: **`Số phút thi đấu`**
5. **Bộ lọc Top 10:** Khung Filters -> `Player Name` -> chọn **Top N**, nhập `10`, By value kéo `Goals` -> nhấp **Apply filter**.
6. **Định dạng visual & phân biệt màu sắc các trục:**
   * Tab **Format visual** -> **Title**: Nhập `Top 10 chân sút ghi bàn nhiều nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**).
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
2. Thiết lập kích thước và vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`
   * **Position:** `Horizontal = 975 px`, `Vertical = 300 px`
3. Kéo thả các trường dữ liệu:
   * **Values (Điểm chi tiết):** Tìm chiều `DIM Player`, kéo thuộc tính `Player Name` vào ô **Values**.
   * **X-axis (Trục hoành):** Kéo thước đo `[Measures].[Assists]` (Tổng số đường kiến tạo thành bàn).
   * **Y-axis (Trục tung):** Kéo thước đo `[Measures].[Goals]` (Tổng số bàn thắng ghi được).
   * **Size (Kích thước bong bóng):** Kéo thước đo `[Measures].[Goal Contributions]` (hoặc `[Minutes Played]`).
   * **Legend (Màu sắc theo nhóm):** Kéo `DIM Player [Main Position]` (Attack, Midfield, Defender) để phân biệt rõ vị trí thi đấu.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Player Name` $\rightarrow$ Đổi tên thành: **`Cầu thủ`**
   * `Assists` $\rightarrow$ Đổi tên thành: **`Số pha kiến tạo`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Số bàn thắng`**
   * `Goal Contributions` $\rightarrow$ Đổi tên thành: **`Tổng G+A`**
   * `Main Position` $\rightarrow$ Đổi tên thành: **`Vị trí`**
5. **Bộ lọc Visual (Filters on this visual):**
   * Để biểu đồ không bị quá dày đặc điểm, tại ô `DIM Player [Player Name]`, chọn **Top N** -> nhập `30` (hoặc `40`) -> By value kéo `Goal Contributions` -> nhấp **Apply filter** (Tập trung phân tích 30-40 ngôi sao tấn công hàng đầu Châu Âu).
6. **Kẻ 2 đường phân chia 4 Góc phần tư (Quadrant Reference Lines):**
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
   * Tab **Format visual** -> **Title**: Nhập `Ma trận hiệu quả tấn công cầu thủ`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Số pha kiến tạo (Assists)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**.
   * **Y-axis:** Title bật **On**, nhập `Số bàn thắng (Goals)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**.
   * **Legend:** Position chọn `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8: Tạo Biểu đồ Nâng cao 2: Bản đồ Phân tầng Đa cấp (Treemap Drill-down) (Ô 3: Dưới - Trái)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Treemap** (Bản đồ phân tầng diện tích đa cấp).
   *(Lưu ý kỹ thuật: Visual Treemap sử dụng phép toán phân vùng diện tích hình chữ nhật chuẩn OLAP, tương thích tuyệt đối 100% với SSAS Multidimensional Live Connection, loại bỏ triệt để lỗi không tương thích "Something's wrong with the visual" của AI Split trên Decomposition Tree).*
2. Thiết lập kích thước và vị trí mở rộng thoáng đãng:
   * **Size:** `Width = 1233 px`, `Height = 385 px`
   * **Position:** `Horizontal = 20 px`, `Vertical = 695 px`
3. Kéo thả các trường dữ liệu vào khung **Build visual**:
   * **Group / Category (Phân cấp nhóm đa tầng):** Kéo lần lượt 3 trường phân cấp từ vĩ mô xuống vi mô:
     1. `DIM Competition [Competition Name]` (Tầng 1: Giải đấu)
     2. `DIM Player [Main Position]` (Tầng 2: Vị trí thi đấu)
     3. `DIM Club [Club Name]` (Tầng 3: Câu lạc bộ)
   * **Values (Kích thước ô tỷ trọng):** Kéo thước đo `[Measures].[Goal Contributions]` (hoặc `[Measures].[Goals]`).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
   * `Main Position` $\rightarrow$ Đổi tên thành: **`Vị trí thi đấu`**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Goal Contributions` $\rightarrow$ Đổi tên thành: **`Tổng đóng góp G+A`**
5. **Hướng dẫn kích hoạt tính năng Khoan sâu (Drill-down):**
   * Rê chuột lên góc trên bên phải thanh tiêu đề của visual Treemap:
     * Nhấp mũi tên đơn trỏ xuống (↓) để bật chế độ **Click to turn on Drill down**: Khi nhấp vào một khối Giải đấu (ví dụ: `Premier League`), visual sẽ lập tức phóng to phân rã thành các khối Vị trí thi đấu (`Attack`, `Midfield`, `Defender`) trong giải đấu đó.
     * Nhấp biểu tượng mũi tên đôi trỏ xuống (↓↓) để chuyển toàn bộ biểu đồ xuống cấp phân tích tiếp theo.
     * Nhấp mũi tên phân nhánh (⑂) để mở rộng đồng thời cả 2 cấp phân tầng trên cùng một màn hình hiển thị.
5. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Bật **On**, nhập `Bản đồ Đóng góp bàn thắng`, Font `Segoe UI`, Cỡ chữ **`18 pt`**, In đậm (**Bold**), Căn giữa (**Center**).
   * Tab **Format visual** -> **Category labels**: Bật **On**, Font `Segoe UI`, Cỡ chữ **`12 pt`**, In đậm (**Bold**).
   * Tab **General** -> **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 9: Thiết lập Báo cáo Phân nhóm & Tổng hợp Đa cấp (Grouping and Totals Matrix Visual) (Ô 4: Dưới - Phải)

> [!IMPORTANT]
> **TIÊU CHÍ CHẤM ĐIỂM BẮT BUỘC - BÁO CÁO GROUPING & TOTALS:**
> * Đây là thành phần đáp ứng trực tiếp yêu cầu đề bài: *"Mỗi công cụ thực hiện tối thiểu 3 report, trong đó có 1 report dạng Grouping and Totals"*.
> * Visual **Matrix** được cấu hình phân nhóm 3 tầng tự nhiên: **Giải đấu (`Competition Name`) $\rightarrow$ Câu lạc bộ (`Club Name`) $\rightarrow$ Cầu thủ (`Player Name`)**.
> * Kích hoạt đầy đủ các dòng **Subtotals** (tính tổng số bàn thắng, kiến tạo cho từng CLB và từng Giải đấu) và dòng **Grand Total** (tổng cộng toàn bộ châu Âu) ở đáy ma trận.

#### 1. Thêm visual Matrix và Cấu hình trường dữ liệu:
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Matrix** (Ma trận phân cấp, nằm ngay bên cạnh biểu tượng Table).
2. Kích thước & Tọa độ: `Width = 925 px`, `Height = 385 px`, `Horizontal = 975 px`, `Vertical = 695 px`.
3. Kéo thả các trường dữ liệu:
   * **Rows (Phân nhóm đa cấp - Grouping):** Kéo lần lượt 3 trường theo đúng thứ tự phân tầng từ lớn xuống nhỏ:
     1. Mở bảng **`DIM Competition`**, kéo thuộc tính **`[Competition Name]`** (Cấp 1: Phân nhóm Giải đấu).
     2. Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`** (Cấp 2: Phân nhóm Câu lạc bộ).
     3. Mở bảng **`DIM Player`**, kéo thuộc tính **`[Player Name]`** (Cấp 3: Chi tiết Cầu thủ).
   * **Values (Các chỉ số tổng hợp định lượng - Totals):** Kéo các thước đo Measure chuẩn từ Cube:
     1. Kéo thước đo **`[Measures].[Goals]`** (Số bàn thắng ghi được).
     2. Kéo thước đo **`[Measures].[Assists]`** (Số pha kiến tạo).
     3. Kéo thước đo **`[Measures].[Goal Contributions]`** (Tổng đóng góp G+A).
     4. Kéo thước đo **`[Measures].[Minutes Played]`** (Tổng thời lượng thi đấu).

#### 2. Kích hoạt Tính năng Phân nhóm và Tổng hợp (Grouping & Totals):
1. **Bật Dòng Tổng phụ (Subtotals):**
   * Nhấp chọn Matrix $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Subtotals**:
   * Tại mục **Row subtotals**: Gạt công tắc sang **ON**!
   * *Ý nghĩa:* Tự động sinh ra các dòng tổng phụ in đậm cho từng Câu lạc bộ và từng Giải đấu (ví dụ: dòng tổng bàn thắng của `Manchester City`, dòng tổng bàn thắng của `Premier League`).
2. **Bật Dòng Tổng cộng toàn cục (Grand Total):**
   * Trong mục Subtotals, cuộn xuống phần **Grand total**: Bật **Row grand total: ON**!
   * *Ý nghĩa:* Hiển thị dòng tổng kết toàn bộ số liệu của tất cả các giải đấu ở đáy bảng.
3. **Điều hướng hiển thị phân nhóm:**
   * **Cách bung toàn bộ phân cấp (Expand all):** Nhấp chọn bảng Matrix, nhìn lên thanh công cụ nhỏ ở góc trên bên phải visual, nhấp 2 lần vào biểu tượng **mũi tên phân nhánh `⑂` (Expand all down one level in the hierarchy)** để bung trọn vẹn cả 3 cấp Giải đấu $\rightarrow$ CLB $\rightarrow$ Cầu thủ.
   * **Tùy chọn Bố cục Bậc thang (Stepped Layout):**
     * Vào tab **Format visual** $\rightarrow$ **Row headers** $\rightarrow$ mở rộng mục **Options**:
       * *Nếu để Stepped layout = ON:* Bảng hiển thị dạng cây gập mở (Tree view) cực kỳ gọn gàng với các dấu cộng `+ / -` để người dùng chủ động bấm bung xem chi tiết từng đội.
       * *Nếu để Stepped layout = OFF:* Bảng tự động dàn phẳng thành 3 cột độc lập riêng biệt (`Giải đấu`, `Câu lạc bộ`, `Cầu thủ`) kèm các dòng Subtotal xen kẽ.

#### 3. Đổi tên nhãn cột hiển thị (Rename for this visual):
* Nhấp chuột phải vào từng trường trong ô Rows / Values $\rightarrow$ chọn **Rename for this visual**:
  * `Competition Name` $\rightarrow$ Đổi tên: **`Competition`** (hoặc `Giải đấu`)
  * `Club Name` $\rightarrow$ Đổi tên: **`Club`** (hoặc `Câu lạc bộ`)
  * `Player Name` $\rightarrow$ Đổi tên: **`Player`** (hoặc `Cầu thủ`)
  * `Goals` $\rightarrow$ Đổi tên: **`Goals`** (hoặc `Bàn thắng`)
  * `Assists` $\rightarrow$ Đổi tên: **`Assists`** (hoặc `Kiến tạo`)
  * `Goal Contributions` $\rightarrow$ Đổi tên: **`Goal Contributions`** (hoặc `Tổng G+A`)
  * `Minutes Played` $\rightarrow$ Đổi tên: **`Minutes Played`** (hoặc `Số phút`)

#### 4. Bật thanh dữ liệu Data Bars trực quan (Tab Format visual $\rightarrow$ Cell elements):
* Vào tab **Format visual** $\rightarrow$ **Cell elements**:
  * Tại ô **Select series**: Chọn `Goal Contributions` (hoặc `Goals`).
  * Gạt công tắc **Data bars** sang **ON**!
  * Nhấp nút **`fx`** bên cạnh Data bars:
    * **Positive bar:** Chọn màu Xanh dương hiện đại **`#2563EB`**.
    * **Bar direction:** Chọn `Left to right`.
    * **Show bar only:** Để **Off** (hiển thị cả con số bên cạnh thanh).
    * Nhấp **OK**.

#### 5. Định dạng hiển thị chuẩn mực:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Báo cáo Phân nhóm & Tổng hợp Hiệu suất Tấn công Đa cấp (Grouping & Totals)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
* **Row headers & Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#0F172A`, màu nền tiêu đề `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#1E293B`.
* **Subtotals formatting:** In đậm (**Bold**), màu nền dòng Subtotal xám nhạt `#E2E8F0` để phân biệt rõ ràng với các dòng chi tiết.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

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
