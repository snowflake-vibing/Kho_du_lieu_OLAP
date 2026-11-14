# 4.2.2 Báo biểu 2: Vận hành CLB, Hạ tầng Thánh địa Sân đấu & Dấu ấn Huấn luyện viên (Club Operations, Stadium Infrastructure & Squad Analytics)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 2 (Executive Dashboard 2)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **ĐỘC LẬP NGHIỆP VỤ & 100% DỮ LIỆU CÓ SẴN:** Báo biểu 2 giải quyết trọn vẹn các bài toán **Truy vấn 11, 12, 13** trong hồ sơ Kho dữ liệu (`docs/15_queries.md`). Khác biệt hoàn toàn với Báo biểu 1 (chuyên sâu Hỏa lực Bàn thắng/Kiến tạo) và Báo biểu 3 (chuyên sâu Kỷ luật Thẻ phạt), Báo biểu 2 tập trung độc lập vào **Hạ tầng Sân vận động (`Stadium Name`, `Stadium Seats`), Tần suất Trận đấu (`Distinct Matches Played`), Dấu ấn Huấn luyện viên (`Coach Name`) và Quy mô Đội hình (`Squad Size`)**. Toàn bộ trường đều đã có sẵn trong Cube SSAS hiện tại, kéo thả là ra số liệu ngay lập tức.

Báo biểu tuân thủ đầy đủ bộ quy chuẩn [**`rule.md`**](../rule.md):
* **Canvas:** Độ phân giải **Full HD 1920 x 1080 px (16:9)**, màu nền xám khói `#F8FAFC`.
* **Phân cấp Typography (Visual Hierarchy):** Title Banner **`20 pt` Bold**, Tiêu đề từng Visual **`18 pt` Bold**, Callout Value thẻ KPI **`35 pt` Bold** (cực kỳ nổi bật), Nhãn dữ liệu & Trục tọa độ **`12 pt`**.
* **Bộ lọc Slicers rộng rãi:** Chiều cao mở rộng **`H = 75 px`**, hiển thị trọn vẹn cả tiêu đề, khung xổ Dropdown và các nút chọn Tile, triệt tiêu hoàn toàn lỗi bị cụt thanh cuộn.
* **Chuẩn hóa nhãn hiển thị (Rename for this visual):** Từng trường dữ liệu đều có hướng dẫn đổi tên tiếng Việt ngắn gọn, chuyên nghiệp, xóa bỏ hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Những "thánh địa" sân vận động nào có quy mô lớn nhất Châu Âu và tần suất đón các trận cầu đỉnh cao ra sao?** Khảo sát các sân bóng trên 60.000 chỗ ngồi (Camp Nou, Wembley, Signal Iduna Park, Santiago Bernabéu...).
2. **Quy mô khán đài sân vận động có tương quan với mật độ thi đấu thực tế của các CLB không?** Phân tích xem các CLB sở hữu sân vận động lớn có tần suất thi đấu dày đặc hơn (đá nhiều cúp châu lục) hay không.
3. **Cơ cấu tổ chức trận đấu và quy mô lực lượng (`Squad Size`) giữa các giải VĐQG hàng đầu biến thiên ra sao qua các mùa giải?** Theo dõi sự biến đổi số lượng trận đấu của Premier League, La Liga, Serie A, Bundesliga, Ligue 1 qua chuỗi thời gian.
4. **Hồ sơ vận hành của từng CLB:** Kết hợp thông tin sân nhà, HLV trưởng đương nhiệm và độ dày lực lượng cầu thủ để đánh giá bộ máy vận hành của đội bóng.

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Biểu đồ Cột ngang Top 10 Sân vận động** | Xếp hạng và so sánh biến định lượng quy mô sức chứa khán đài (`Stadium Capacity Cleaned`) theo từng thánh địa bóng đá. |
| **Scatter Sức chứa vs Số trận đấu + 2 Median** | Phân tích tương quan 2 biến định lượng (Bivariate Correlation); kết hợp **Đường xu hướng (Trend line)** và **2 đường Trung vị (Median lines)** để phân loại 4 nhóm vận hành: Sân lớn - Thi đấu nhiều (CLB siêu sao toàn diện); Sân vừa - Thi đấu nhiều (Tối ưu công suất); Sân nhỏ - Thi đấu ít; Sân lớn - Thi đấu ít. |
| **Biểu đồ Cột Xếp chồng theo Mùa giải** | Biểu diễn quy mô số lượng trận đấu tổ chức qua chuỗi thời gian phân tách theo từng giải đấu (Time-series Decomposition). |
| **Bảng Tra cứu Vận hành Đa chỉ số** | Tích hợp dữ liệu danh mục định danh (`Club Name`, `Stadium Name`, `Coach Name`) với số đo định lượng (`Stadium Seats`, `Squad Size`, `Matches Played`), kết hợp **Mini Data Bars** trực quan. |

### 1.3. Bài toán thực tế giải quyết
* **Ban điều hành Giải đấu & Ban tổ chức sân:** Đánh giá công suất phục vụ khán giả và năng lực vận hành tổ chức sự kiện thi đấu xuyên suốt mùa giải.
* **Giám đốc điều hành CLB (CEO):** Phân tích tương quan giữa quy mô đội hình (`Squad Size`) và số trận thực tế mà HLV trưởng (`Coach Name`) phải xoay tua nhân sự.
* **Nhà tài trợ & Đối tác thương mại:** Nhận diện những sân bóng có quy mô khán giả khổng lồ để đàm phán hợp đồng quảng cáo bảng LED và quyền đặt tên sân (Naming rights).

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 2 - VẬN HÀNH CLB, SÂN ĐẤU & QUY MÔ ĐỘI HÌNH (Font: 20pt Bold, Center)         |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Trận Đấu]   | [Card 2: Tổng Lượt Ra Sân]| [Card 3: Lượt Xuất Phát Chính]| [Card 4: Thời Lượng Thi Đấu TB]   |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold                |
| Nền: Pastel Blue #EFF6FF  | Nền: Pastel Green #F0FDF4 | Nền: Pastel Amber #FFFBEB   | Nền: Pastel Purple #FAF5FF        |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu]                                  | [Slicer 2: Mùa giải]        | [Slicer 3: Loại giải đấu (Tile)]  |
| (W: 650, H: 75, X: 20, Y: 210)                        | (W: 600, H: 75, X: 690)     | (W: 590, H: 75, X: 1310)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT THANH NGANG (18pt)]     | [Ô 2: TRÊN - PHẢI | MA TRẬN PHÂN TÁN SCATTER (Title: 18pt)]    |
| Top 10 Thánh địa Sân Vận Động Lớn nhất Châu Âu          | Tương quan Sức chứa Sân vận động vs Tần suất Trận đấu CLB     |
| Y: Sân đấu (12pt Navy), X: Sức chứa (12pt Green)        | X: Sức chứa (12pt), Y: Số trận (12pt), Size: Lượt ra sân      |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | CỘT XẾP CHỒNG THEO MÙA (18pt)]      | [Ô 4: DƯỚI - PHẢI | BẢNG ĐIỀU HÀNH & TRA CỨU CLB (18pt)]      |
| Tần suất Trận đấu Tổ chức giữa các Giải qua từng Mùa    | Danh bạ Sân vận động, Huấn luyện viên & Quy mô Đội hình       |
| X: Mùa giải (12pt), Y: Số trận (12pt), Legend: Giải đấu | Cột: CLB, Sân, HLV, Sức chứa, Đội hình, Số trận (Data Bars)   |
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
   `BÁO BIỂU 2: VẬN HÀNH CLB, HẠ TẦNG SÂN ĐẤU & QUY MÔ ĐỘI HÌNH BÓNG ĐÁ CHÂU ÂU`
3. Bôi đen toàn bộ văn bản và định dạng:
   * Font chữ: `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Căn giữa (**Center**), Màu chữ: Xanh than đậm `#0F172A`.
4. Tab **General** $\rightarrow$ **Effects**:
   * **Background:** Nền trắng `#FFFFFF`.
   * **Visual border:** Bật **On**, màu viền `#CBD5E1`, Bo góc (**Rounded corners**): **`10 px`**.
5. Tab **General** $\rightarrow$ **Properties**:
   * Size: `Width = 1880 px`, `Height = 55 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 15 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tinh hoa (Chuyên sâu Vận hành & Lực lượng)

Cả 4 thẻ Card đều đặt thẳng hàng tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px`:

#### 1. Card 1: Tổng số Trận đấu Tổ chức (Total Matches Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Distinct Matches Played]`** vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng trận đấu`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG SỐ TRẬN ĐẤU TỔ CHỨC`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa (**Center**), màu chữ `#1E3A8A`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Blue **`#EFF6FF`**, Viền `#93C5FD`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 20 px`, `Y = 95 px`.

#### 2. Card 2: Tổng Lượt Cầu thủ Ra sân (Total Appearances)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[FACT Player Match Perf Count]`** vào ô **Fields** (thước đo đếm tổng số lượt đăng ký thi đấu của các cầu thủ).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng lượt ra sân`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG LƯỢT CẦU THỦ RA SÂN`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#065F46`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Green **`#F0FDF4`**, Viền `#86EFAC`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 495 px`, `Y = 95 px`.

#### 3. Card 3: Tổng Lượt Xuất phát Đá chính (Total Starters)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Is Starter]`** vào ô **Fields** (tính tổng số lượt ra sân trong đội hình xuất phát 11 người).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Lượt đá chính`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG LƯỢT XUẤT PHÁT ĐÁ CHÍNH`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Thời lượng Thi đấu Trung bình Mỗi trận (Avg Minutes Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Avg Minutes Played]`** vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Số phút TB / trận`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `THỜI LƯỢNG THI ĐẤU TRUNG BÌNH`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#5B21B6`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, Display units chọn `None`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Purple **`#FAF5FF`**, Viền `#D8B4FE`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 1445 px`, `Y = 95 px`.

---

### Bước 4: Thiết lập Hệ thống 3 Slicers Mở rộng (Không bị cụt thanh Dropdown)

Cả 3 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`**:

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

### Bước 5 – Ô 1 (Trên - Trái): Clustered Bar Chart – Top 10 Thánh địa Sân Vận Động Lớn nhất Châu Âu

1. Tại khung **Visualizations**, chọn visual **Clustered bar chart** (Biểu đồ thanh ngang).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Y-axis:** Kéo `DIM Club [Stadium Name]` (hoặc `Club Name`).
   * **X-axis:** Kéo thước đo **`[Measures].[Stadium Capacity Cleaned]`**.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Stadium Name` $\rightarrow$ Đổi tên thành: **`Sân vận động`**
   * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân (chỗ ngồi)`**
5. **Bộ lọc Top 10 Sân bóng:**
   * Khung Filters on this visual $\rightarrow$ chọn trường `Stadium Name` $\rightarrow$ chọn **Top N** $\rightarrow$ nhập `10` $\rightarrow$ tại ô **By value** kéo `Stadium Capacity Cleaned` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Top 10 Thánh địa Sân Vận Động có Sức chứa Lớn nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **Bars:** Màu Xanh dương hoàng gia **`#2563EB`**.
   * **Y-axis (Tên sân vận động):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, *Maximum width* đặt `35%` để hiển thị trọn vẹn tên sân.
   * **X-axis (Sức chứa):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục Forest Green `#1B5E20`**.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Tương quan Sức chứa Sân vận động vs Tần suất Trận đấu (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Scatter chart** (Biểu đồ phân tán).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Values:** Kéo `DIM Club [Club Name]`.
   * **X-axis:** Kéo thước đo **`[Measures].[Stadium Capacity Cleaned]`** (Sức chứa sân).
   * **Y-axis:** Kéo thước đo **`[Measures].[Distinct Matches Played]`** (Số trận đấu đã tổ chức).
   * **Size:** Kéo thước đo **`[Measures].[FACT Player Match Perf Count]`** (Tổng lượt cầu thủ ra sân).
   * **Legend:** Kéo `DIM Competition [Competition Name]` (phân màu bong bóng theo giải đấu).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân vận động`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận thi đấu`**
   * `FACT Player Match Perf Count` $\rightarrow$ Đổi tên thành: **`Tổng lượt ra sân`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Kẻ đường Xu hướng & Trung vị (Thẻ Analytics - Kính lúp):**
   * **Trend line:** Bật **On**, màu Xám than `#64748B`, nét đứt (Dashed) để thể hiện tương quan giữa quy mô sân và mật độ thi đấu.
   * **X-Axis Constant Line (Median Sức chứa):** Bật On, nhập giá trị trung vị sân (khoảng 40,000 chỗ), nét đứt, nhãn `Median Sức chứa`.
   * **Y-Axis Constant Line (Median Số trận):** Bật On, nhập giá trị trung vị số trận (khoảng 38 trận/mùa), nét đứt, nhãn `Median Số trận`.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Tương quan Quy mô Sân vận động vs Tần suất Trận đấu CLB`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Sức chứa sân vận động (chỗ ngồi)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Số lượng trận đấu tổ chức`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#1565C0`.
   * **Legend:** Vị trí `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA 4 GÓC PHẦN TƯ MA TRẬN VẬN HÀNH SÂN ĐẤU:**
> * **Góc I (Trên - Phải): THÁNH ĐỊA TOÀN NĂNG (Elite Arenas):** Sân lớn (> 50.000 chỗ) VÀ tần suất thi đấu dày đặc (> 45 trận/mùa). Đây là các siêu CLB (Real Madrid, Bayern, Man City) vừa đá giải VĐQG vừa tiến sâu tại Champions League.
> * **Góc II (Trên - Trái): KHAI THÁC HIỆU QUẢ CAO (Optimized Operations):** Sân quy mô vừa nhưng tổ chức số trận rất lớn nhờ thành tích tốt tại các cúp quốc nội.
> * **Góc IV (Dưới - Phải): QUY MÔ DƯ THỪA / CHƯA KHAI THÁC HẾT:** Sân vận động rất lớn nhưng CLB sớm bị loại ở các đấu trường cúp nên số trận thực tế ít.
> * **Góc III (Dưới - Trái): SÂN NHỎ - THI ĐẤU CƠ BẢN:** Các đội bóng tầm trung với lịch thi đấu tiêu chuẩn 34–38 trận.

---

### Bước 7 – Ô 3 (Dưới - Trái): Stacked Column Chart – Tần suất Trận đấu Tổ chức giữa các Giải qua từng Mùa giải

1. Tại khung **Visualizations**, chọn visual **Stacked column chart** (Biểu đồ cột xếp chồng theo thời gian).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Time [Season]`.
   * **Y-axis:** Kéo `[Measures].[Distinct Matches Played]`.
   * **Legend:** Kéo `DIM Competition [Competition Name]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số lượng trận đấu tổ chức`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Bộ lọc Top 6 Giải đấu lớn nhất:**
   * Tại khung Filters $\rightarrow$ `Competition Name` $\rightarrow$ chọn **Top N** = `6`, By value kéo `Distinct Matches Played` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Tần suất Tổ chức Trận đấu giữa các Giải đấu qua từng Mùa giải`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Mùa giải):** Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Cỡ chữ **`12 pt`**, màu `#1565C0`.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8 – Ô 4 (Dưới - Phải): Table / Matrix – Danh bạ Sân vận động, Huấn luyện viên & Quy mô Đội hình (NÂNG CAO)

Sử dụng visual **Table (Bảng phẳng)** để tra cứu đa chỉ số điều hành:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Kéo lần lượt các trường sau vào ô **Columns**:
  1. `DIM Club [Club Name]`
  2. `DIM Club [Stadium Name]`
  3. `DIM Club [Coach Name]`
  4. `[Measures].[Stadium Capacity Cleaned]`
  5. `DIM Club [Squad Size]`
  6. `[Measures].[Distinct Matches Played]`

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường $\rightarrow$ chọn **Rename for this visual**:
  * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
  * `Stadium Name` $\rightarrow$ Đổi tên thành: **`Sân vận động`**
  * `Coach Name` $\rightarrow$ Đổi tên thành: **`Huấn luyện viên trưởng`**
  * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân`**
  * `Squad Size` $\rightarrow$ Đổi tên thành: **`Quy mô đội hình`**
  * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận thi đấu`**

#### 3. Bật Mini Data Bars trực quan (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn cột **`Sức chứa sân`**.
  * Gạt công tắc **Data bars** sang **ON**! Nhấp nút `fx` chọn màu xanh `#3B82F6` $\rightarrow$ OK. Cột Sức chứa sân lập tức xuất hiện thanh đo mini so sánh quy mô trực quan.
  * Tại ô xổ xuống **Select series**: Chọn tiếp cột **`Số trận thi đấu`**.
  * Gạt công tắc **Background color** sang **ON**! Nhấp `fx` chọn dải màu Gradient từ trắng `#FFFFFF` sang xanh ngọc nhạt `#E0F2FE` để nhận diện các CLB có mật độ thi đấu cao nhất.

#### 4. Định dạng hiển thị:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Danh bạ Vận hành CLB: Sân vận động, Huấn luyện viên & Quy mô Đội hình`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, Text wrap **On**, Auto-size width **On**, màu nền xám sáng thanh lịch `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap **On**.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* Khi nhấp chọn giải đấu `Premier League` trên Slicer:
  * Toàn bộ 4 thẻ KPI cập nhật tức thời số liệu riêng cho giải Ngoại Hạng Anh (380 trận đấu/mùa, hơn 10.000 lượt ra sân).
  * Biểu đồ Cột Top 10 Sân vận động lọc riêng các thánh địa nước Anh (`Old Trafford` ~74k chỗ, `Tottenham Hotspur Stadium` ~62k, `Emirates Stadium` ~60k, `London Stadium` ~60k...).
  * Biểu đồ Phân tán (Scatter) làm nổi bật các CLB Anh có mật độ thi đấu lớn nhất do tham chiến ở 4 đấu trường song song (Premier League, FA Cup, Carabao Cup, Cúp Châu Âu).
  * Bảng xếp hạng bên dưới lọc tự động danh sách các CLB Premier League cùng tên HLV trưởng (Pep Guardiola, Mikel Arteta, Jürgen Klopp...) và quy mô đội hình thực tế.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Năng lực Thương mại & Tối ưu Hạ tầng (Venue Commercialization):**
   * Các SVĐ quy mô trên 60.000 khán giả tập trung chủ yếu tại Ngoại Hạng Anh, La Liga và Bundesliga. Tuy nhiên, doanh thu ngày thi đấu (Matchday Revenue) phụ thuộc vào cả sức chứa lẫn tần suất tổ chức trận đấu. Góc phần tư I chứng minh việc thi đấu nhiều trận tại cúp châu lục tạo ra lợi thế kép khổng lồ về dòng tiền bán vé cho các CLB tinh hoa.
2. **Quy mô Đội hình vs Khối lượng Trận đấu (Squad Depth vs Fixture Congestion):**
   * Thông qua bảng danh bạ vận hành, các đội bóng thi đấu trên 50 trận/mùa luôn duy trì `Squad Size` từ **`28 – 32 cầu thủ`** để HLV trưởng thực hiện xoay tua, tránh quá tải cơ bắp. Ngược lại, các đội bóng chỉ thi đấu khoảng 34–38 trận thường có quy mô đội hình gọn nhẹ hơn (**`23 – 25 cầu thủ`**) nhằm tối ưu quỹ lương.
3. **Tính Ổn định của Giải đấu qua Chuỗi Thời gian (League Schedule Stability):**
   * Biểu đồ cột xếp chồng theo mùa phản ánh tính ổn định tuyệt đối về quy mô tổ chức của các giải đấu lớn qua các năm, tạo điều kiện thuận lợi cho các liên đoàn bóng đá bán bản quyền truyền hình dài hạn.
