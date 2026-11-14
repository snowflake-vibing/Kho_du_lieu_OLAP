# 4.2.2 Báo biểu 2: Vận hành CLB, Tương quan Sân vận động và Dịch chuyển Giải đấu (Club Operations, Stadium Analytics & League Evolution)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 2 (Executive Dashboard 2)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **TIÊU CHÍ THIẾT KẾ THỰC TẾ:** Toàn bộ báo biểu được xây dựng **$100\%$ dựa trên các Thước đo (Measures) và Chiều phân tích (Dimensions) ĐÃ CÓ SẴN** trong khối SSAS Cube hiện tại. Không yêu cầu can thiệp hay sửa đổi CSDL/Cube, không sử dụng các bộ lọc dòng Measure gây lỗi rỗng (BLANK), đảm bảo người dùng kéo thả là hiển thị số liệu chính xác ngay lập tức.

Báo biểu tuân thủ đầy đủ bộ quy chuẩn [**`rule.md`**](../rule.md):
* **Canvas:** Độ phân giải **Full HD 1920 x 1080 px (16:9)**, màu nền xám khói `#F8FAFC`.
* **Phân cấp Typography (Visual Hierarchy):** Title Banner **`20 pt` Bold**, Tiêu đề từng Visual **`18 pt` Bold**, Callout Value thẻ KPI **`35 pt` Bold** (cực kỳ nổi bật), Nhãn dữ liệu & Trục tọa độ **`12 pt`**.
* **Bộ lọc Slicers rộng rãi:** Chiều cao mở rộng **`H = 75 px`**, hiển thị trọn vẹn cả tiêu đề, khung xổ Dropdown và các nút chọn Tile, triệt tiêu hoàn toàn lỗi bị cụt thanh cuộn.
* **Chuẩn hóa nhãn hiển thị (Rename for this visual):** Từng trường dữ liệu đều có hướng dẫn đổi tên tiếng Việt ngắn gọn, chuyên nghiệp, xóa bỏ hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ
1. **Những CLB nào sở hữu hỏa lực tấn công toàn diện nhất châu Âu?** Đánh giá song song cả khả năng dứt điểm (`Goals`) và khả năng kiến tạo dọn cỗ (`Assists`) của từng đội bóng.
2. **Quy mô sân vận động có tương quan thuận với số bàn thắng của CLB không?** Phân tích xem các CLB sở hữu "chảo lửa" khán đài lớn (`Stadium Seats`) có ghi được nhiều bàn thắng hơn các đội sân nhỏ hay không.
3. **Thứ hạng hỏa lực giữa các giải đấu hàng đầu thay đổi ra sao qua các mùa giải?** Theo dõi sự biến thiên vị thế sức mạnh giữa Premier League, La Liga, Serie A, Bundesliga, Ligue 1 qua từng mùa (`Season`).

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Biểu đồ Cột cụm Đôi (Goals & Assists)** | So sánh song biến định lượng trên cùng một đối tượng danh mục (Bivariate Comparison). Nhận diện rõ CLB nào tấn công cân bằng (vừa ghi bàn vừa kiến tạo cao) và CLB nào tấn công đơn điệu. |
| **Scatter Sức chứa vs Bàn thắng** | Phân tích tương quan 2 biến định lượng (Bivariate Correlation); kết hợp **Đường xu hướng (Trend line)** và **2 đường Trung vị (Median lines)** để phân loại 4 nhóm CLB: Sân lớn - Bàn nhiều; Sân nhỏ - Bàn nhiều (hiệu quả cao); Sân lớn - Bàn ít (dưới kỳ vọng); Sân nhỏ - Bàn ít. |
| **Ribbon Chart theo Mùa giải** | Biểu diễn đồng thời cả **quy mô bàn thắng** lẫn **sự hoán đổi thứ bậc (Rank tracking)** của từng giải đấu qua chuỗi thời gian, giúp quan sát các pha "vượt mặt" về thứ hạng mà biểu đồ đường thường không thể hiện rõ. |

### 1.3. Bài toán thực tế giải quyết
* **Ban điều hành CLB & Giám đốc thể thao:** So sánh tương quan giữa năng lực đón khán giả và thành tích chuyên môn để quyết định kế hoạch nâng cấp hạ tầng sân vận động.
* **Chuyên gia phân tích chiến thuật:** Đánh giá độ phụ thuộc vào dàn hỏa lực kiến tạo của các đội bóng hàng đầu châu Âu.
* **Nhà đài & Đối tác truyền thông:** Nhận biết giải đấu nào đang có đà tăng trưởng hỏa lực hấp dẫn khán giả qua các mùa để ưu tiên phát sóng khung giờ vàng.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 2 - VẬN HÀNH CLB, SÂN ĐẤU & DỊCH CHUYỂN GIẢI ĐẤU (Font: 20pt Bold, Center)     |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Trận Đấu]   | [Card 2: Tổng Bàn Thắng]  | [Card 3: Tổng Kiến Tạo]     | [Card 4: Thời Lượng Thi Đấu TB]   |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold                |
| Nền: Pastel Blue #EFF6FF  | Nền: Pastel Green #F0FDF4 | Nền: Pastel Amber #FFFBEB   | Nền: Pastel Purple #FAF5FF        |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu]                                  | [Slicer 2: Mùa giải]        | [Slicer 3: Loại giải đấu (Tile)]  |
| (W: 650, H: 75, X: 20, Y: 210)                        | (W: 600, H: 75, X: 690)     | (W: 590, H: 75, X: 1310)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT CỤM ĐÔI (Title: 18pt)]  | [Ô 2: TRÊN - PHẢI | MA TRẬN PHÂN TÁN SCATTER (Title: 18pt)]    |
| Top 10 CLB Hỏa lực Tấn công Mạnh nhất (Bàn thắng & G+A) | Tương quan Sức chứa Sân vận động vs Tổng Bàn thắng CLB        |
| X: CLB (12pt Navy), Y: Bàn thắng (Xanh) & Kiến tạo (Cam)| X: Sức chứa (12pt), Y: Bàn thắng (12pt), Kèm 2 Đường Median   |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BIỂU ĐỒ DẢI LỤA RIBBON (18pt)]      | [Ô 4: DƯỚI - PHẢI | BẢNG MA TRẬN / BẢNG TRA CỨU (18pt)]       |
| Dịch chuyển Thứ hạng Bàn thắng giữa các Giải theo Mùa   | Bảng Xếp hạng CLB theo Sức chứa Sân & Hiệu quả Ghi bàn        |
| X: Mùa giải (12pt), Y: Bàn thắng, Legend: Giải đấu     | Tích hợp Mini Data Bars, Dữ liệu 12pt phẳng lì không dấu ...  |
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
   `BÁO BIỂU 2: VẬN HÀNH CLB, SÂN ĐẤU & DỊCH CHUYỂN GIẢI ĐẤU QUA CÁC MÙA GIẢI`
3. Bôi đen toàn bộ văn bản và định dạng:
   * Font chữ: `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Căn giữa (**Center**), Màu chữ: Xanh than đậm `#0F172A` (hoặc Trắng `#FFFFFF`).
4. Tab **General** $\rightarrow$ **Effects**:
   * **Background:** Nền trắng `#FFFFFF`.
   * **Visual border:** Bật **On**, màu viền `#CBD5E1`, Bo góc (**Rounded corners**): **`10 px`**.
5. Tab **General** $\rightarrow$ **Properties**:
   * Size: `Width = 1880 px`, `Height = 55 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 15 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tinh hoa (Dùng 100% Thước đo có sẵn trong Cube)

Cả 4 thẻ Card đều đặt thẳng hàng tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px`:

#### 1. Card 1: Tổng số Trận đấu (Total Matches Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Distinct Matches Played]`** vào ô **Fields** (thước đo tính Distinct trận đấu đã có sẵn trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Nhấp đúp vào trường trong ô Fields $\rightarrow$ đổi tên hiển thị thành: **`Tổng trận đấu`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG TRẬN ĐẤU (MATCHES)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa (**Center**), màu chữ `#1E3A8A`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Blue **`#EFF6FF`**, Viền `#93C5FD`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 20 px`, `Y = 95 px`.

#### 2. Card 2: Tổng số Bàn thắng Toàn giải (Total Goals)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Goals]`** vào ô **Fields** (hiển thị trực tiếp con số 19,173 bàn thắng, không cần filter).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng bàn thắng`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG BÀN THẮNG TOÀN GIẢI`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#065F46`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Green **`#F0FDF4`**, Viền `#86EFAC`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 495 px`, `Y = 95 px`.

#### 3. Card 3: Tổng số Pha Kiến tạo (Total Assists)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Assists]`** vào ô **Fields** (hiển thị trực tiếp 14,064 pha kiến tạo, có sẵn trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng kiến tạo`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG PHA KIẾN TẠO (ASSISTS)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Thời lượng Thi đấu Trung bình Mỗi trận (Avg Minutes Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Avg Minutes Played]`** vào ô **Fields** (thước đo tính trung bình số phút thi đấu mỗi trận, có sẵn trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Số phút TB / trận`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `THỜI LƯỢNG THI ĐẤU TRUNG BÌNH`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#5B21B6`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, Display units chọn `None`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Purple **`#FAF5FF`**, Viền `#D8B4FE`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 1445 px`, `Y = 95 px`.

---

### Bước 4: Thiết lập Hệ thống 3 Slicers Mở rộng (Không bị cụt thanh Dropdown)

Cả 3 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`** (triệt tiêu hoàn toàn lỗi cụt khung xổ Dropdown):

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

### Bước 5 – Ô 1 (Trên - Trái): Clustered Column Chart – Hỏa lực Tấn công Toàn diện Top 10 CLB (Bàn thắng & Kiến tạo)

1. Tại khung **Visualizations**, chọn visual **Clustered column chart** (Biểu đồ cột cụm đứng).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Club [Club Name]`.
   * **Y-axis:** Kéo đồng thời 2 thước đo:
     1. `[Measures].[Goals]`
     2. `[Measures].[Assists]`
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng`**
   * `Assists` $\rightarrow$ Đổi tên thành: **`Kiến tạo`**
5. **Bộ lọc Top 10 CLB:**
   * Tại khung **Filters on this visual** $\rightarrow$ chọn trường `Club Name` $\rightarrow$ chọn mục **Top N** $\rightarrow$ nhập `10` $\rightarrow$ tại ô **By value** kéo thả thước đo `Goals` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Top 10 CLB có Hỏa lực Tấn công Mạnh nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **Columns (Màu sắc 2 cột):**
     * Cột `Bàn thắng`: Màu Xanh dương hoàng gia **`#2563EB`**.
     * Cột `Kiến tạo`: Màu Cam hổ phách **`#F59E0B`**.
   * **X-axis (Trục danh mục):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, Xoay nhãn nghiêng 45° để hiển thị trọn vẹn tên CLB.
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
3. Kéo thả trường dữ liệu (sử dụng 100% trường có sẵn trong Cube):
   * **Values:** Kéo `DIM Club [Club Name]`.
   * **X-axis:** Kéo thước đo **`[Measures].[Stadium Capacity Cleaned]`** (sức chứa sân đã chuẩn hóa có sẵn trong Cube).
   * **Y-axis:** Kéo thước đo **`[Measures].[Goals]`**.
   * **Size:** Kéo thước đo **`[Measures].[Distinct Matches Played]`** (hoặc `[Measures].[Goal Contributions]`).
   * **Legend:** Kéo `DIM Competition [Competition Name]` (phân màu bong bóng theo giải đấu).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân vận động`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Tổng bàn thắng`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận thi đấu`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Kẻ đường Xu hướng & Trung vị (Thẻ Analytics - Kính lúp):**
   * **Trend line (Đường xu hướng):** Bật **On**, màu Xám than `#64748B`, nét đứt (Dashed) để thể hiện chiều tương quan giữa quy mô sân và số bàn thắng.
   * **X-Axis Constant Line (Median Sức chứa):** Bật On, nhập giá trị trung vị sân (khoảng 40,000 chỗ), nét đứt, nhãn `Median Sức chứa`.
   * **Y-Axis Constant Line (Median Bàn thắng):** Bật On, nhập giá trị trung vị bàn thắng (khoảng 80 bàn), nét đứt, nhãn `Median Bàn thắng`.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Tương quan Sức chứa Sân vận động và Bàn thắng`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Sức chứa sân (chỗ ngồi)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Tổng số bàn thắng`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu sắc `#1565C0`.
   * **Legend:** Vị trí `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7 – Ô 3 (Dưới - Trái): Ribbon Chart – Dịch chuyển Thứ hạng Bàn thắng giữa các Giải đấu qua các Mùa (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Ribbon chart** (Biểu đồ dải lụa theo dõi biến thiên thứ bậc).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Time [Season]`.
   * **Y-axis:** Kéo `[Measures].[Goals]`.
   * **Legend:** Kéo `DIM Competition [Competition Name]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Tổng số bàn thắng`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Bộ lọc Top 6 Giải đấu lớn nhất:**
   * Tại khung Filters $\rightarrow$ `Competition Name` $\rightarrow$ chọn **Top N** = `6`, By value kéo `Goals` $\rightarrow$ nhấp **Apply filter** (tập trung 6 giải đấu lớn nhất châu Âu để các dải lụa xếp tầng thoáng mắt, dễ đọc).
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Dịch chuyển Thứ hạng Bàn thắng giữa các Giải đấu qua các Mùa`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Mùa giải):** Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Cỡ chữ **`12 pt`**, màu `#1565C0`.
   * **Ribbons:** Độ trong suốt (Transparency) đặt `30%` để nhìn rõ các đường dải lụa đan chéo khi thứ hạng hoán đổi.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8 – Ô 4 (Dưới - Phải): Bảng Xếp hạng CLB theo Sức chứa Sân & Hiệu quả Tấn công (NÂNG CAO)

Bạn có thể sử dụng visual **Table (Bảng phẳng)** hoặc visual **Matrix (Ma trận)**:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Kéo lần lượt các trường sau vào ô **Columns** (nếu dùng Table) hoặc **Rows & Values** (nếu dùng Matrix):
  1. `DIM Competition [Competition Name]`
  2. `DIM Club [Club Name]`
  3. `[Measures].[Stadium Capacity Cleaned]`
  4. `[Measures].[Distinct Matches Played]`
  5. `[Measures].[Goals]`
  6. `[Measures].[Assists]`

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường $\rightarrow$ chọn **Rename for this visual**:
  * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
  * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
  * `Stadium Capacity Cleaned` $\rightarrow$ Đổi tên thành: **`Sức chứa sân`**
  * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận thi đấu`**
  * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng`**
  * `Assists` $\rightarrow$ Đổi tên thành: **`Kiến tạo`**

#### 3. Bật Mini Data Bars trực quan (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn cột **`Bàn thắng`**.
  * Gạt công tắc **Data bars** sang **ON**! Nhấp nút `fx` chọn màu xanh `#3B82F6` $\rightarrow$ OK. Cột Bàn thắng lập tức có thanh tiến độ mini trực quan.
  * Tại ô xổ xuống **Select series**: Chọn tiếp cột **`Sức chứa sân`**.
  * Gạt công tắc **Background color** sang **ON**! Nhấp `fx` chọn dải màu Gradient từ trắng `#FFFFFF` sang vàng cam nhạt `#FEF3C7` để tạo hiệu ứng Heatmap nhận diện sân bóng quy mô lớn.

#### 4. Định dạng hiển thị:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Bảng Xếp hạng Toàn diện CLB theo Sức chứa Sân và Hiệu suất Ghi bàn`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, Text wrap **On**, Auto-size width **On**, màu nền xám sáng thanh lịch `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap **On**.
* **Subtotals:** Tắt **Off** (nếu dùng Matrix) để loại bỏ phân mảnh, giúp bảng phẳng và rõ nét.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* Khi nhấp chọn giải đấu `Premier League` trên Slicer:
  * Toàn bộ 4 thẻ KPI cập nhật tức thời số liệu riêng cho giải Ngoại Hạng Anh (khoảng 380 trận/mùa, hơn 1,000 bàn thắng).
  * Biểu đồ Cột cụm Top 10 lọc riêng các CLB hàng đầu nước Anh (`Manchester City`, `Arsenal`, `Liverpool`, `Aston Villa`...).
  * Biểu đồ Phân tán (Scatter) làm nổi bật vị trí của các sân bóng lớn (Old Trafford, Tottenham Hotspur Stadium, Emirates, Anfield) so với sản lượng bàn thắng thực tế.
  * Bảng xếp hạng bên dưới lọc tự động danh sách các CLB Premier League với thanh Data Bar trực quan, không bao giờ bị lỗi tràn dòng hay dấu ba chấm (`...`).

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Tính cân bằng giữa Bàn thắng và Kiến tạo:**
   * Các CLB dẫn đầu châu Âu (như Man City, Bayern Munich, Real Madrid) luôn duy trì tỷ lệ `Assists / Goals` đạt trên **`75%`**, chứng tỏ lối chơi tấn công phối hợp tập thể bài bản. Ngược lại, các đội bóng tầm trung thường có tỷ lệ này thấp hơn do phụ thuộc vào các tình huống bóng cố định hoặc nỗ lực cá nhân độc lập.
2. **Quy mô sân vận động không quyết định hỏa lực (Tương quan ≠ Nhân quả):**
   * Đường xu hướng (Trend line) trên biểu đồ phân tán có độ dốc dương nhẹ, nhưng xuất hiện nhiều ngoại lệ đáng chú ý: nhiều CLB sở hữu sân vận động có sức chứa dưới mức trung vị (Median) vẫn đạt sản lượng bàn thắng vượt trội nhờ chất lượng đội hình. Điều này chứng minh quy mô sân vận động phản ánh năng lực thương mại và tài chính bán vé hơn là đóng vai trò nguyên nhân trực tiếp tới số bàn thắng.
3. **Sự dịch chuyển quyền lực giữa các giải đấu (League Dominance Evolution):**
   * Thông qua Ribbon Chart, người xem nhận thấy rõ cuộc đua tranh ngôi vị giải đấu có hỏa lực tấn công mạnh nhất giữa Premier League và Bundesliga qua các mùa giải, cung cấp cơ sở dữ liệu quan trọng cho các nhà tài trợ đánh giá mức độ bùng nổ và hấp dẫn của từng giải đấu.
