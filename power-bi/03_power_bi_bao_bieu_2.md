# 4.2.2 Báo biểu 2: Vận hành Trận đấu, Lợi thế Sân nhà và Tương quan Sân vận động (Club Match Operations & Home Advantage Analytics)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 2 (Executive Dashboard 2)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

Báo biểu được thiết kế theo đúng [**`rule.md`**](../rule.md): Tối ưu hóa không gian hiển thị trên độ phân giải **Full HD 1920 x 1080 px (16:9)**, bố cục **2 tầng** (Tầng trên: Title 20pt + 4 KPI Cards Callout 35pt + 3 Slicers mở rộng $H = 75 - 80\text{ px}$; Tầng dưới: **4 biểu đồ nâng cao** với Title 18pt, Dữ liệu/Trục 12pt), **chuẩn hóa toàn bộ tên hiển thị tiếng Việt (Rename for this visual)** và triệt tiêu hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ
1. **Lợi thế sân nhà (Home Advantage) có thật không và lớn tới mức nào?** So sánh hỏa lực tấn công khi thi đấu tại sân nhà so với khi phải làm khách.
2. **Quy mô sân vận động có liên quan tới hiệu quả ghi bàn của CLB không?** Phân tích tương quan giữa sức chứa sân (`Stadium Seats`) và tổng bàn thắng (`Goals`) ghi được.
3. **Thứ hạng giải đấu nào đang dịch chuyển qua các mùa giải?** Theo dõi sự biến thiên vị thế sức mạnh tấn công giữa các giải đấu hàng đầu châu Âu qua từng mùa (`Season`).

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Tỷ lệ bàn sân nhà (%)** | Chuẩn hóa về tỷ trọng (Normalized Ratio) thay vì số tuyệt đối, giúp so sánh công bằng giữa các CLB thi đấu nhiều trận và ít trận. Ngưỡng tham chiếu trung tính là **50%**: tỷ lệ càng vượt xa 50% thì yếu tố "chảo lửa sân nhà" càng rõ nét. |
| **Scatter Sức chứa vs Bàn thắng** | Phân tích tương quan 2 biến định lượng (Bivariate Correlation); kết hợp **Đường xu hướng (Trend line)** và **2 đường Trung vị (Median lines)** kháng nhiễu đối với các sân vận động siêu lớn (outliers). |
| **Ribbon Chart theo Mùa giải** | Biểu diễn đồng thời cả **quy mô bàn thắng** lẫn **sự hoán đổi thứ bậc (Rank tracking)** của từng giải đấu qua chuỗi thời gian, khắc phục nhược điểm che khuất thông tin của biểu đồ cột truyền thống. |

### 1.3. Bài toán thực tế giải quyết
* **Ban huấn luyện CLB:** Nhận diện những đội bóng "khôn nhà dại chợ" (tỷ lệ bàn sân nhà > 65%) để xây dựng giáo án chiến thuật tâm lý và phòng ngự phản công riêng biệt khi đá sân khách.
* **Ban quản trị CLB & Giám đốc tài chính:** Đánh giá quyết định đầu tư mở rộng sức chứa khán đài: liệu quy mô sân có thực sự thúc đẩy thành tích ghi bàn hay chỉ mang giá trị thương mại và bán vé.
* **Nhà đài & Đối tác bản quyền:** Nắm bắt giải đấu nào đang có đà bùng nổ bàn thắng qua từng mùa để định giá gói bản quyền truyền hình tối ưu nhất.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 2 - VẬN HÀNH TRẬN ĐẤU & TƯƠNG QUAN SÂN VẬN ĐỘNG (Font: 20pt Bold, Center)      |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Trận Đấu]   | [Card 2: Bàn Sân Nhà]     | [Card 3: Bàn Sân Khách]     | [Card 4: Tỷ lệ Bàn Sân Nhà %]     |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold                |
| Nền: Pastel Blue #EFF6FF  | Nền: Pastel Green #F0FDF4 | Nền: Pastel Amber #FFFBEB   | Nền: Pastel Purple #FAF5FF        |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu]                                  | [Slicer 2: Mùa giải]        | [Slicer 3: Loại giải đấu (Tile)]  |
| (W: 650, H: 75, X: 20, Y: 210)                        | (W: 600, H: 75, X: 690)     | (W: 590, H: 75, X: 1310)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT SO SÁNH (Title: 18pt)]  | [Ô 2: TRÊN - PHẢI | MA TRẬN PHÂN TÁN SCATTER (Title: 18pt)]    |
| So sánh Bàn thắng Sân nhà vs Sân khách Top 10 CLB       | Tương quan Sức chứa Sân vận động vs Tổng Bàn thắng CLB        |
| X-axis: Tên CLB (12pt Navy), Y-axis: Bàn thắng (12pt)   | X: Sức chứa (12pt), Y: Bàn thắng (12pt), Trend & Median Lines |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BIỂU ĐỒ DẢI LỤA RIBBON (18pt)]      | [Ô 4: DƯỚI - PHẢI | BẢNG MA TRẬN ĐA CẤP (Title: 18pt)]        |
| Dịch chuyển Thứ hạng Bàn thắng giữa các Giải theo Mùa   | Bảng xếp hạng Chi tiết CLB: Sức chứa sân & Hỏa lực Sân nhà    |
| X: Mùa giải (12pt), Y: Bàn thắng, Legend: Giải đấu     | Tích hợp Mini Data Bars, Heatmap, Tắt Subtotals phẳng rõ nét  |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi tạo Trang Báo cáo và Cấu hình Canvas
1. Tại thanh quản lý trang ở mép dưới Power BI Desktop, nhấp vào biểu tượng dấu cộng `+` để thêm một trang mới.
2. Nhấp đúp chuột vào tên trang vừa tạo và **đặt tên trang chính thức**:
   * **Tên trang:** `Vận hành CLB & Sân đấu` (hoặc `Báo biểu 2`).
3. Nhấp chuột vào khoảng trống Canvas để mở bảng **Format report page**:
   * **Canvas settings** $\rightarrow$ **Type:** Chọn `Custom`, thiết lập `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói hiện đại **`#F8FAFC`**, thiết lập **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng trên)
1. Trên thanh tác vụ **Insert**, nhấp chọn **Text box**.
2. Nhập nội dung tiêu đề chuẩn mực:
   `BÁO BIỂU 2: VẬN HÀNH TRẬN ĐẤU, LỢI THẾ SÂN NHÀ & TƯƠNG QUAN SÂN VẬN ĐỘNG`
3. Bôi đen toàn bộ văn bản và định dạng:
   * Font chữ: `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Căn giữa (**Center**), Màu chữ: Xanh than đậm `#0F172A` (hoặc Trắng `#FFFFFF`).
4. Tab **General** $\rightarrow$ **Effects**:
   * **Background:** Nền trắng `#FFFFFF` (hoặc màu thương hiệu đậm).
   * **Visual border:** Bật **On**, màu viền `#CBD5E1`, Bo góc (**Rounded corners**): **`10 px`**.
5. Tab **General** $\rightarrow$ **Properties**:
   * Size: `Width = 1880 px`, `Height = 55 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 15 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tinh hoa (Callout 35pt Bold)

Cả 4 thẻ Card đều đặt thẳng hàng tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px`:

#### 1. Card 1: Tổng số Trận đấu (Total Matches Played)
* Kéo thước đo `[Measures].[Distinct Matches Played]` vào ô **Fields** (hoặc `DIM Game [Game ID]` chọn *Count Distinct*).
* **Phần đặt tên (Rename for this visual):**
  * Nhấp đúp hoặc chuột phải vào trường $\rightarrow$ đổi tên hiển thị thành: `Tổng trận đấu`.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG TRẬN ĐẤU (MATCHES)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa (**Center**), màu chữ `#1E3A8A`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Blue **`#EFF6FF`**, Viền `#93C5FD`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 20 px`, `Y = 95 px`.

#### 2. Card 2: Bàn thắng Ghi được trên Sân nhà (Home Goals)
* Kéo thước đo `[Measures].[Goals]` vào ô **Fields**.
* Tại khung **Filters on this visual**: Kéo `Is Home Game` vào và lọc giá trị `-1` (hoặc `1` đại diện cho trận sân nhà).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: `Bàn sân nhà`.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `BÀN THẮNG SÂN NHÀ`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#065F46`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Green **`#F0FDF4`**, Viền `#86EFAC`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 495 px`, `Y = 95 px`.

#### 3. Card 3: Bàn thắng Ghi được trên Sân khách (Away Goals)
* Kéo thước đo `[Measures].[Goals]` vào ô **Fields**.
* Tại khung **Filters on this visual**: Lọc `Is Home Game = 0` (đại diện cho trận sân khách).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: `Bàn sân khách`.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `BÀN THẮNG SÂN KHÁCH`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Tỷ lệ Bàn thắng Sân nhà (Home Goals Ratio %)
* Kéo thước đo tính toán `[Measures].[Home Goals Ratio]` vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: `Tỷ lệ sân nhà (%)`.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỶ LỆ BÀN SÂN NHÀ (%)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#5B21B6`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Purple **`#FAF5FF`**, Viền `#D8B4FE`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 1445 px`, `Y = 95 px`.

---

### Bước 4: Thiết lập Hệ thống 3 Slicers Mở rộng (Không bị cụt thanh Dropdown)

Cả 3 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`** (khắc phục hoàn toàn lỗi cụt khung xổ Dropdown):

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 20 px | 210 px | 650 px | 75 px |
| **Slicer 2** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown | 690 px | 210 px | 600 px | 75 px |
| **Slicer 3** | `DIM Competition [Competition Type]` | **`Loại giải đấu`** | Tile (Thẻ ngang) | 1310 px | 210 px | 590 px | 75 px |

* **Định dạng chung cho Slicers:**
  * Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt` Bold**, màu chữ `#0F172A`.
  * Values (dữ liệu mục chọn): Font `Segoe UI`, Cỡ chữ **`12 pt`**.
  * Effects: Nền trắng `#FFFFFF`, Viền mỏng `#CBD5E1`, Bo góc `8 px`.

---

### Bước 5 – Ô 1 (Trên - Trái): Clustered Column Chart – So sánh Hỏa lực Sân nhà vs Sân khách Top 10 CLB

1. Tại khung **Visualizations**, chọn visual **Clustered column chart** (Biểu đồ cột cụm).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Club [Club Name]`.
   * **Y-axis:** Kéo `[Measures].[Goals]`.
   * **Legend:** Kéo trường hoặc thước đo phân loại sân nhà/sân khách (hoặc kéo đồng thời 2 thước đo `Home Goals` và `Away Goals` vào ô Y-axis).
4. **Phần đặt tên (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Số bàn thắng`**
   * Nhãn Legend: Đổi thành **`Sân nhà`** (Màu xanh `#2563EB`) và **`Sân khách`** (Màu cam hổ phách `#F59E0B`).
5. **Bộ lọc Top 10:** Tại khung Filters $\rightarrow$ `Club Name` $\rightarrow$ chọn **Top N** $\rightarrow$ nhập `10` $\rightarrow$ By value kéo `Goals` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `So sánh Bàn thắng Sân nhà vs Sân khách – Top 10 CLB`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Trục danh mục):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, Xoay nhãn nghiêng 45° để hiện trọn vẹn tên CLB.
   * **Y-axis (Trục giá trị):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục Forest Green `#1B5E20`**.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Tương quan Sức chứa Sân vận động vs Bàn thắng (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Scatter chart** (Biểu đồ phân tán).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Values:** Kéo `DIM Club [Club Name]`.
   * **X-axis:** Kéo thước đo chuẩn hóa `[Measures].[Stadium Capacity Cleaned]` (hoặc `[Stadium Capacity]`).
   * **Y-axis:** Kéo thước đo `[Measures].[Goals]`.
   * **Size:** Kéo `[Measures].[Distinct Matches Played]` (hoặc `DIM Game [Game ID]` đếm số trận).
   * **Legend:** Kéo `DIM Competition [Competition Name]` (phân màu theo giải đấu).
4. **Phần đặt tên (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân vận động`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Tổng bàn thắng`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận thi đấu`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Kẻ đường Xu hướng & Trung vị (Analytics Pane):**
   * **Trend line:** Bật **On**, màu Xám than `#64748B`, nét đứt (Dashed) để quan sát tương quan thuận chiều giữa sức chứa sân và số bàn thắng.
   * **X-Axis Constant / Median line:** Nhãn `Median Sức chứa`, nét đứt.
   * **Y-Axis Constant / Median line:** Nhãn `Median Bàn thắng`, nét đứt.
6. **Định dạng:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Tương quan Sức chứa Sân vận động và Bàn thắng`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Sức chứa sân (chỗ ngồi)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Tổng số bàn thắng`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#1565C0`.
   * **Legend:** Vị trí `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7 – Ô 3 (Dưới - Trái): Ribbon Chart – Dịch chuyển Thứ hạng Giải đấu qua các Mùa (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Ribbon chart** (Biểu đồ dải lụa theo dõi thứ bậc).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Time [Season]`.
   * **Y-axis:** Kéo `[Measures].[Goals]`.
   * **Legend:** Kéo `DIM Competition [Competition Name]`.
4. **Phần đặt tên (Rename for this visual):**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Tổng số bàn thắng`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Bộ lọc giải đấu Top N:** Tại Filters $\rightarrow$ `Competition Name` $\rightarrow$ chọn **Top N** = `6`, By value kéo `Goals` $\rightarrow$ nhấp **Apply filter** (tập trung 6 giải đấu lớn nhất để dải lụa không bị rối mắt).
6. **Định dạng:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Dịch chuyển Thứ hạng Bàn thắng giữa các Giải đấu qua các Mùa`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Mùa giải):** Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Cỡ chữ **`12 pt`**, màu `#1565C0`.
   * **Ribbons:** Độ trong suốt (Transparency) đặt `30%` để nhìn thấu các đường dải lụa vắt chéo khi hoán đổi vị trí thứ hạng.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8 – Ô 4 (Dưới - Phải): Bảng Xếp hạng CLB theo Sức chứa Sân và Lợi thế Sân nhà (NÂNG CAO)

Bạn có thể sử dụng visual **Table** (phẳng $100\%$ không bị lồng cấp) hoặc visual **Matrix** (đa cấp chuẩn OLAP):

#### Cấu hình dữ liệu:
1. Kích thước & Vị trí:
   * Size: `Width = 925 px` (hoặc linh hoạt), `Height = 385 px`.
   * Position: `Horizontal = 975 px`, `Vertical = 695 px`.
2. Kéo thả các trường dữ liệu:
   * `DIM Competition [Competition Name]`
   * `DIM Club [Club Name]`
   * `[Measures].[Stadium Capacity Cleaned]` (hoặc `[Stadium Capacity]`)
   * `[Measures].[Goals]`
   * `[Measures].[Home Goals Ratio]`
3. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Tổng bàn thắng`**
   * `Home Goals Ratio` $\rightarrow$ Đổi tên thành: **`Tỷ lệ bàn sân nhà`**

#### Bật Mini Data Bars & Heatmap (Tab Format visual $\rightarrow$ Cell elements):
* Vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * **Data bars cho Bàn thắng:** Tại `Select series` chọn `Tổng bàn thắng` $\rightarrow$ Bật **Data bars = ON** $\rightarrow$ nhấp `fx` chọn màu xanh `#3B82F6`.
  * **Heatmap cho Tỷ lệ sân nhà:** Tại `Select series` chọn `Tỷ lệ bàn sân nhà` $\rightarrow$ Bật **Background color = ON** $\rightarrow$ nhấp `fx` chọn gradient từ trắng `#FFFFFF` (50%) sang vàng cam `#FEF3C7` ($\ge 65\%$).

#### Định dạng hiển thị:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Bảng Xếp hạng Chi tiết CLB theo Sức chứa Sân và Tỷ lệ Bàn Sân nhà`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, Text wrap **On**, Auto-size width **On**, màu nền xám sáng thanh lịch `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap **On**.
* **Subtotals:** Tắt **Off** (triệt tiêu phân mảnh).
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Đối soát và Nhận xét Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering & Drill-down)
* Khi nhấp chọn giải đấu `Premier League` trên Slicer:
  * Toàn bộ 4 thẻ KPI cập nhật tức thời số liệu riêng cho giải Ngoại Hạng Anh.
  * Biểu đồ Cột Top 10 hiển thị riêng các CLB Anh (`Manchester City`, `Arsenal`, `Liverpool`, `Aston Villa`...).
  * Biểu đồ Phân tán (Scatter) làm nổi bật tương quan giữa sân Etihad, Emirates, Anfield với tổng bàn thắng.
  * Bảng xếp hạng bên dưới lọc tự động danh sách các CLB Premier League với thanh Data Bar trực quan, không bao giờ bị lỗi tràn dòng hay dấu `...`.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Lợi thế sân nhà có thật về mặt thống kê (Empirical Home Advantage):**
   * Tỷ lệ ghi bàn trên sân nhà trung bình của các giải đấu lớn dao động quanh mức **`56% - 62%`**, lệch rõ rệt khỏi mốc cân bằng lý thuyết $50\%$. Điều này chứng minh áp lực khán giả và quen thuộc mặt cỏ mang lại lợi thế hỏa lực thực tế.
2. **Quy mô sân vận động phản ánh thương mại hơn là nguyên nhân hỏa lực (Correlation vs Causation):**
   * Đường xu hướng (Trend line) trên biểu đồ phân tán có độ dốc dương nhẹ, nhưng xuất hiện nhiều ngoại lệ: nhiều CLB có sức chứa sân dưới mức trung vị (Median) vẫn đạt sản lượng bàn thắng vượt trội nhờ chất lượng đội hình. Điều này chứng minh quy mô sân vận động gắn liền với doanh thu bán vé hơn là đóng vai trò quyết định tới số bàn thắng.
3. **Sự dịch chuyển quyền lực giữa các giải đấu (League Dominance Evolution):**
   * Thông qua Ribbon Chart, người xem nhận thấy rõ sự bám đuổi quyết liệt giữa Premier League và Bundesliga về tổng số bàn thắng qua các mùa, cung cấp cơ sở dữ liệu quan trọng cho các nhà tài trợ đánh giá mức độ hấp dẫn của giải đấu.
