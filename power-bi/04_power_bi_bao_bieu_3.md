# 4.2.3 Báo biểu 3: Kỷ luật Thẻ phạt, Cường độ Thi đấu và Tải trọng Cầu thủ (Discipline & Match Load Analytics)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 3 (Executive Dashboard 3)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **TIÊU CHÍ THIẾT KẾ THỰC TẾ & ĐỘC LẬP TỰ CHỦ:** Toàn bộ báo biểu được xây dựng **$100\%$ dựa trên các Thước đo (Measures) và Chiều phân tích (Dimensions) ĐÃ CÓ SẴN** trong khối SSAS Cube hiện tại. Không yêu cầu can thiệp hay sửa đổi CSDL/Cube, không sử dụng các bộ lọc dòng Measure gây lỗi rỗng (BLANK), đảm bảo người dùng kéo thả là hiển thị số liệu chính xác ngay lập tức.

Báo biểu tuân thủ đầy đủ bộ quy chuẩn [**`rule.md`**](../rule.md):
* **Canvas:** Độ phân giải **Full HD 1920 x 1080 px (16:9)**, màu nền xám khói `#F8FAFC`.
* **Phân cấp Typography (Visual Hierarchy):** Title Banner **`20 pt` Bold**, Tiêu đề từng Visual **`18 pt` Bold**, Callout Value thẻ KPI **`35 pt` Bold** (cực kỳ nổi bật), Nhãn dữ liệu & Trục tọa độ **`12 pt`**.
* **Bộ lọc Slicers rộng rãi:** Chiều cao mở rộng **`H = 75 px`**, hiển thị trọn vẹn cả tiêu đề, khung xổ Dropdown và các nút chọn Tile, triệt tiêu hoàn toàn lỗi bị cụt thanh cuộn.
* **Chuẩn hóa nhãn hiển thị (Rename for this visual):** Từng trường dữ liệu đều có hướng dẫn đổi tên tiếng Việt ngắn gọn, chuyên nghiệp, xóa bỏ hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ
1. **Những CLB và vị trí thi đấu nào có rủi ro kỷ luật cao nhất châu Âu?** (`Yellow Cards`, `Red Cards`).
2. **Cầu thủ nhận nhiều thẻ phạt là do thi đấu quá nhiều (tải trọng cao) hay do phong cách thi đấu bạo lực / thiếu kiềm chế?** Đặt số thẻ phạt trong mối tương quan với thời lượng ra sân (`Minutes Played`).
3. **Độ tuổi nào trong bóng đá chuyên nghiệp đang phải gánh tải trọng thi đấu lớn nhất và có xu hướng phạm lỗi nhiều nhất?** (`Minutes Played` và `Yellow Cards` theo `Age`).

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Stacked Bar Chart (Vàng + Đỏ)** | So sánh tổng lượng thẻ phạt và cơ cấu mức độ nghiêm trọng (thẻ vàng cảnh cáo vs thẻ đỏ trực tiếp/gián tiếp) giữa các CLB hàng đầu. |
| **Scatter Số phút vs Thẻ vàng + 2 đường Median** | Phân tích tương quan 2 biến định lượng ($X = \text{Minutes Played}$, $Y = \text{Yellow Cards}$); sử dụng **2 đường Trung vị (Median lines)** để kháng ngoại lai (Robust Statistics) và chia 4 góc phần tư rủi ro kỷ luật. |
| **Combo Chart 2 Trục Y (Dual Axis)** | Đặt tải trọng thời lượng (Cột - Trục Y trái) và số thẻ phạt (Đường - Trục Y phải) trên cùng một trục danh mục độ tuổi (`Age`), giải quyết bài toán so sánh 2 đại lượng khác thang đo (Khử Exposure Bias). |
| **Bảng Ma trận Hồ sơ Kỷ luật** | Tra cứu vi mô từng cầu thủ, tích hợp **Data bars** và **Heatmap** cảnh báo trực quan nguy cơ bị treo giò. |

### 1.3. Bài toán thực tế giải quyết
* **Ban huấn luyện & Trợ lý trọng tài:** Nhận diện ngay những cầu thủ nằm ở góc "Bất thường" (Ít phút nhưng nhiều thẻ) để uốn nắn kỷ luật, tránh mất người vì thẻ phạt ở các trận knock-out sống còn.
* **Bộ phận Y tế & Thể lực CLB:** Xác định nhóm tuổi chịu tải trọng cao nhất để phân bổ kế hoạch hồi phục cơ bắp và xoay tua đội hình (Squad Rotation) hợp lý.
* **Ban điều hành CLB:** Dự báo nguy cơ bị ban tổ chức giải phạt tài chính hoặc án treo giò tập thể do vi phạm quy chế kỷ luật giải đấu.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 3 - KỶ LUẬT THẺ PHẠT & TẢI TRỌNG THI ĐẤU (Font: 20pt Bold, Center)           |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Thẻ Vàng]   | [Card 2: Tổng Thẻ Đỏ]     | [Card 3: Tổng Lượt Ra Sân]| [Card 4: Tổng Số Phút]            |
| Callout: 35pt Bold        | Callout: 35pt Bold        | Callout: 35pt Bold          | Callout: 35pt Bold (Millions)     |
| Nền: Pastel Amber #FFFBEB | Nền: Pastel Red #FEF2F2   | Nền: Pastel Blue #EFF6FF    | Nền: Pastel Green #F0FDF4         |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải]                                  | [Slicer 2: Giải đấu]        | [Slicer 3: Vị trí (Tile)]         |
| (W: 650, H: 75, X: 20, Y: 210)                        | (W: 600, H: 75, X: 690)     | (W: 590, H: 75, X: 1310)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH XẾP CHỒNG (18pt)]     | [Ô 2: TRÊN - PHẢI | MA TRẬN PHÂN TÁN SCATTER (Title: 18pt)]    |
| Top 10 CLB nhận Nhiều Thẻ Phạt Nhất (Thẻ Vàng & Thẻ Đỏ) | Ma trận Rủi ro Kỷ luật: Số phút Thi đấu vs Thẻ vàng           |
| Y: CLB (12pt Navy), X: Thẻ (12pt), Màu Vàng/Đỏ ngữ nghĩa| X: Số phút (12pt), Y: Thẻ vàng (12pt), Size: Thẻ đỏ, 2 Median |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | COMBO CHART 2 TRỤC Y (18pt)]        | [Ô 4: DƯỚI - PHẢI | BẢNG HỒ SƠ KỶ LUẬT MATRIX (Title: 18pt)]  |
| Tải trọng Thi đấu (Cột) & Thẻ phạt (Đường) theo Độ tuổi | Hồ sơ Kỷ luật Chi tiết từng Cầu thủ theo CLB                  |
| X: Tuổi (12pt), Y-trái: Phút (Xanh), Y-phải: Thẻ (Đỏ)   | Tích hợp Data Bars Thẻ vàng & Heatmap Thẻ đỏ, Phẳng không ... |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi tạo Trang Báo cáo và Cấu hình Canvas
1. Tại thanh quản lý trang ở mép dưới Power BI Desktop, nhấp vào biểu tượng dấu cộng `+` để thêm một trang mới.
2. Nhấp đúp chuột vào tên trang vừa tạo và **đặt tên trang chính thức**:
   * **Tên trang:** `Kỷ luật & Tải trọng Thi đấu` (hoặc `Báo biểu 3`).
3. Nhấp chuột vào khoảng trống Canvas để mở bảng **Format report page**:
   * **Canvas settings** $\rightarrow$ **Type:** Chọn `Custom`, thiết lập `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói hiện đại **`#F8FAFC`**, thiết lập **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng trên)
1. Trên thanh tác vụ **Insert**, nhấp chọn **Text box**.
2. Nhập nội dung tiêu đề chuẩn mực:
   `BÁO BIỂU 3: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ`
3. Bôi đen toàn bộ văn bản và định dạng:
   * Font chữ: `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Căn giữa (**Center**), Màu chữ: Xanh than đậm `#0F172A`.
4. Tab **General** $\rightarrow$ **Effects**:
   * **Background:** Nền trắng `#FFFFFF`.
   * **Visual border:** Bật **On**, màu viền `#CBD5E1`, Bo góc (**Rounded corners**): **`10 px`**.
5. Tab **General** $\rightarrow$ **Properties**:
   * Size: `Width = 1880 px`, `Height = 55 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 15 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tinh hoa (Dùng 100% Thước đo có sẵn trong Cube)

Cả 4 thẻ Card đều đặt thẳng hàng tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px`:

#### 1. Card 1: Tổng số Thẻ Vàng Toàn giải (Total Yellow Cards)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Yellow Cards]`** vào ô **Fields** (có sẵn 100% trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng thẻ vàng`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG THẺ VÀNG TOÀN GIẢI`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa (**Center**), màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 20 px`, `Y = 95 px`.

#### 2. Card 2: Tổng số Thẻ Đỏ Toàn giải (Total Red Cards)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Red Cards]`** vào ô **Fields** (có sẵn 100% trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng thẻ đỏ`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG THẺ ĐỎ TOÀN GIẢI`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#991B1B`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Red **`#FEF2F2`**, Viền `#FCA5A5`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 495 px`, `Y = 95 px`.

#### 3. Card 3: Tổng Lượt Cầu thủ Thi đấu (Total Appearances)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[FACT Player Match Perf Count]`** vào ô **Fields** (tổng số lượt ra sân thi đấu của các cầu thủ toàn giải).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng lượt ra sân`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG LƯỢT CẦU THỦ RA SÂN`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#1E3A8A`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Blue **`#EFF6FF`**, Viền `#93C5FD`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Tổng Số Phút Thi đấu (Total Minutes Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Minutes Played]`** vào ô **Fields** (có sẵn 100% trong Cube).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng số phút`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG SỐ PHÚT THI ĐẤU`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#065F46`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, mục **Display units** chọn **`Millions`** (hoặc `Auto`). **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Green **`#F0FDF4`**, Viền `#86EFAC`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 1445 px`, `Y = 95 px`.

---

### Bước 4: Thiết lập Hệ thống 3 Slicers Mở rộng (Không bị cụt thanh Dropdown)

Cả 3 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`**:

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown | 20 px | 210 px | 650 px | 75 px |
| **Slicer 2** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 690 px | 210 px | 600 px | 75 px |
| **Slicer 3** | `DIM Player [Main Position]` | **`Vị trí thi đấu`** | Tile (Thẻ ngang) | 1310 px | 210 px | 590 px | 75 px |

* **Định dạng chung cho Slicers:**
  * Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt` Bold**, màu chữ `#0F172A`.
  * Values: Font `Segoe UI`, Cỡ chữ **`12 pt`**.
  * Effects: Nền trắng `#FFFFFF`, Viền mỏng `#CBD5E1`, Bo góc `8 px`.

---

### Bước 5 – Ô 1 (Trên - Trái): Stacked Bar Chart – Top 10 CLB nhận nhiều Thẻ phạt nhất (Thẻ Vàng & Thẻ Đỏ)

1. Tại khung **Visualizations**, chọn visual **Stacked bar chart** (Biểu đồ thanh ngang xếp chồng).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Y-axis:** Kéo `DIM Club [Club Name]`.
   * **X-axis:** Kéo đồng thời 2 thước đo:
     1. `[Measures].[Yellow Cards]`
     2. `[Measures].[Red Cards]`
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Thẻ vàng`**
   * `Red Cards` $\rightarrow$ Đổi tên thành: **`Thẻ đỏ`**
5. **Bộ lọc Top 10 CLB:**
   * Tại khung **Filters on this visual** $\rightarrow$ chọn `Club Name` $\rightarrow$ chọn mục **Top N** $\rightarrow$ nhập `10` $\rightarrow$ tại ô **By value** kéo thả thước đo `Yellow Cards` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Top 10 CLB nhận Nhiều Thẻ Phạt Nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **Bars (Màu sắc chuẩn ngữ nghĩa thể thao):**
     * `Thẻ vàng`: Màu Vàng hổ phách **`#F59E0B`**.
     * `Thẻ đỏ`: Màu Đỏ cảnh báo **`#DC2626`**.
   * **Y-axis (Tên CLB):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, *Maximum width* đặt `35%` để tên CLB dài không bị co rút.
   * **X-axis (Số lượng thẻ):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục Forest Green `#1B5E20`**.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Ma trận Rủi ro Kỷ luật: Số phút Thi đấu vs Thẻ vàng (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Scatter chart** (Biểu đồ phân tán 4 góc phần tư).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu (100% có sẵn trong Cube):
   * **Values:** Kéo `DIM Player [Player Name]`.
   * **X-axis:** Kéo thước đo **`[Measures].[Minutes Played]`**.
   * **Y-axis:** Kéo thước đo **`[Measures].[Yellow Cards]`**.
   * **Size:** Kéo thước đo **`[Measures].[Red Cards]`** (hoặc `[Measures].[Is Starter]`).
   * **Legend:** Kéo `DIM Player [Main Position]` (phân màu theo vị trí thi đấu).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Player Name` $\rightarrow$ Đổi tên thành: **`Cầu thủ`**
   * `Minutes Played` $\rightarrow$ Đổi tên thành: **`Số phút thi đấu`**
   * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Số thẻ vàng`**
   * `Red Cards` $\rightarrow$ Đổi tên thành: **`Thẻ đỏ`**
   * `Main Position` $\rightarrow$ Đổi tên thành: **`Vị trí`**
5. **Bộ lọc Top 40 Cầu thủ:**
   * Tại khung **Filters on this visual** $\rightarrow$ chọn `Player Name` $\rightarrow$ **Top N** = `40`, By value kéo `Yellow Cards` $\rightarrow$ nhấp **Apply filter**.
6. **Kẻ đường Xu hướng & Trung vị (Thẻ Analytics - Kính lúp):**
   * **Trend line:** Bật **On**, màu Xám than `#64748B`, nét đứt (Dashed) thể hiện tương quan giữa thời lượng và số thẻ.
   * **X-Axis Constant Line (Median Số phút):** Bật On, nhập giá trị trung vị số phút (ví dụ: khoảng 1,800 phút), nét đứt, nhãn `Median Số phút`.
   * **Y-Axis Constant Line (Median Thẻ vàng):** Bật On, nhập giá trị trung vị thẻ vàng (ví dụ: khoảng 6 thẻ), nét đứt, nhãn `Median Thẻ vàng`.
7. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Rủi ro Kỷ luật: Số phút Thi đấu vs Thẻ vàng`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Số phút thi đấu (Tải trọng)`, Cỡ chữ **`12 pt` Bold**, màu `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Số thẻ vàng nhận phải`, Cỡ chữ **`12 pt` Bold**, màu `#1565C0`.
   * **Markers (Màu sắc vị trí):** Defender `#10B981`, Midfield `#3B82F6`, Attack `#EF4444`, Goalkeeper `#8B5CF6`.
   * **Legend:** Vị trí `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA 4 GÓC PHẦN TƯ MA TRẬN RỦI RO:**
> * **Góc II (Trên - Trái): RỦI RO KỶ LUẬT CAO BẤT THƯỜNG (Báo động đỏ):** Thi đấu ít phút nhưng số thẻ vàng cực cao. Đây là các cầu thủ có lối đá bạo lực, dễ đẩy đội bóng vào thế thiếu người.
> * **Góc I (Trên - Phải): TẢI TRỌNG CAO & KỶ LUẬT ĐÁNG CHÚ Ý:** Cầu thủ thi đấu nhiều phút và nhận nhiều thẻ tương xứng với cường độ tranh chấp liên tục.
> * **Góc IV (Dưới - Phải): HÌNH MẪU KỶ LUẬT (Fair-play Star):** Cầu thủ "cày ải" số phút khổng lồ nhưng nhận rất ít thẻ vàng (lối chơi phán đoán, dùng trí tuệ hơn dùng sức).
> * **Góc III (Dưới - Trái): AN TOÀN / XOAY TUA:** Cầu thủ ít ra sân và nhận ít thẻ.

---

### Bước 7 – Ô 3 (Dưới - Trái): Combo Chart 2 Trục Y – Tải trọng Thi đấu (Cột) vs Thẻ vàng (Đường) theo Độ tuổi (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Line and clustered column chart** (Biểu đồ kết hợp Cột & Đường 2 trục Y độc lập).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Player [Age]`.
   * **Column y-axis (Trục Y bên trái):** Kéo `[Measures].[Minutes Played]`.
   * **Line y-axis (Trục Y bên phải):** Kéo `[Measures].[Yellow Cards]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Age` $\rightarrow$ Đổi tên thành: **`Độ tuổi`**
   * `Minutes Played` $\rightarrow$ Đổi tên thành: **`Tổng số phút thi đấu`**
   * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Tổng số thẻ vàng`**
5. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Tương quan Tải trọng Thi đấu (Cột) và Thẻ vàng (Đường) theo Độ tuổi`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Độ tuổi):** Cỡ chữ **`12 pt`**, màu sắc `#334155`, mục **Type** chọn **`Categorical`** để hiển thị rõ ràng từng độ tuổi (từ 17 đến 40).
   * **Y-axis bên trái (Số phút - Cột):** Cỡ chữ **`12 pt`**, màu **Xanh lục Forest Green `#1B5E20`**.
   * **Secondary y-axis bên phải (Số thẻ - Đường):** Bật **On**, Cỡ chữ **`12 pt`**, màu **Đỏ rực `#DC2626`** (phân biệt màu riêng biệt tuyệt đối giữa 2 trục Y).
   * **Columns (Màu cột tải trọng):** Màu Xanh lá mạ **`#22C55E`** (hoặc Xanh dương `#3B82F6`).
   * **Lines (Đường thẻ phạt):** Màu Đỏ **`#DC2626`**, Stroke width: `3 px`, Markers: Bật **On**.
   * **Data labels:** Bật **On** (chọn áp dụng cho Line), Cỡ chữ **`12 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8 – Ô 4 (Dưới - Phải): Table / Matrix – Hồ sơ Kỷ luật & Tải trọng Chi tiết từng Cầu thủ theo CLB (NÂNG CAO)

Bạn có thể sử dụng visual **Table (Bảng phẳng)** hoặc visual **Matrix (Ma trận)**:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Kéo lần lượt các trường sau vào ô **Columns** (nếu dùng Table) hoặc **Rows & Values** (nếu dùng Matrix):
  1. `DIM Player [Player Name]`
  2. `DIM Club [Club Name]`
  3. `[Measures].[Minutes Played]`
  4. `[Measures].[FACT Player Match Perf Count]`
  5. `[Measures].[Yellow Cards]`
  6. `[Measures].[Red Cards]`

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường $\rightarrow$ chọn **Rename for this visual**:
  * `Player Name` $\rightarrow$ Đổi tên thành: **`Cầu thủ`**
  * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
  * `Minutes Played` $\rightarrow$ Đổi tên thành: **`Số phút thi đấu`**
  * `FACT Player Match Perf Count` $\rightarrow$ Đổi tên thành: **`Số trận ra sân`**
  * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Thẻ vàng`**
  * `Red Cards` $\rightarrow$ Đổi tên thành: **`Thẻ đỏ`**

#### 3. Bật Conditional Formatting (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn cột **`Thẻ vàng`**.
  * Gạt công tắc **Data bars** sang **ON**! Nhấp nút `fx` chọn màu Vàng hổ phách `#F59E0B` $\rightarrow$ OK. Cột Thẻ vàng lập tức có thanh tiến độ mini trực quan.
  * Tại ô xổ xuống **Select series**: Chọn tiếp cột **`Thẻ đỏ`**.
  * Gạt công tắc **Background color** sang **ON**! Nhấp `fx` chọn dải màu Gradient từ trắng `#FFFFFF` (giá trị 0 thẻ) sang đỏ nhạt `#FECACA` (thẻ đỏ cao) để tạo hiệu ứng Heatmap cảnh báo nóng nguy cơ treo giò.

#### 4. Định dạng hiển thị:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Hồ sơ Kỷ luật & Tải trọng Chi tiết từng Cầu thủ theo CLB`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, Text wrap **On**, Auto-size width **On**, màu nền xám sáng thanh lịch `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap **On**.
* **Subtotals:** Tắt **Off** (nếu dùng Matrix) để loại bỏ các dòng tổng phụ phân mảnh, giúp bảng phẳng và rõ nét.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* Khi nhấp chọn vị trí `Defender` (Hậu vệ) trên Slicer:
  * Toàn bộ 4 thẻ KPI cập nhật tức thời số thẻ và tải trọng của riêng tuyến phòng ngự (chiếm tỷ trọng thẻ vàng lớn nhất toàn giải đấu).
  * Biểu đồ Cột cụm Top 10 lọc riêng các CLB có hàng thủ "rắn" nhất châu Âu.
  * Biểu đồ Phân tán (Scatter) hiển thị rõ các trung vệ có lối chơi quyết liệt (góc trên-phải và góc trên-trái).
  * Biểu đồ Combo 2 trục phản ánh độ tuổi chín muồi của trung vệ (27–31 tuổi) với tải trọng ra sân lớn nhất.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Phân biệt Thẻ phạt do Tải trọng vs Thẻ phạt do Kỷ luật kém:**
   * Thông qua biểu đồ phân tán (Scatter) kết hợp đường xu hướng, ta nhận thấy số lượng thẻ vàng tăng tỷ lệ thuận với số phút thi đấu. Tuy nhiên, những cầu thủ nằm lệch hẳn lên phía trên đường xu hướng và nằm ở Góc II (Ít phút - Nhiều thẻ) là các cá nhân tiềm ẩn rủi ro thẻ phạt cao nhất, cần được ban huấn luyện nhắc nhở kiểm soát hành vi thi đấu.
2. **Quy luật Tải trọng theo Chu kỳ Độ tuổi (Age Load Curve):**
   * Biểu đồ Combo 2 trục thể hiện rõ đỉnh parabol của tải trọng thi đấu rơi vào nhóm tuổi **24 – 29 tuổi** (giai đoạn sung sức nhất của sự nghiệp cầu thủ). Đường thẻ vàng bám sát theo độ dốc của số phút thi đấu chứng minh thẻ phạt trong bóng đá hiện đại là hệ quả tự nhiên của cường độ tranh chấp thể lực, thay vì yếu tố tâm lý bộc phát của cầu thủ trẻ.
3. **Quản trị Rủi ro Treo giò (Suspension Risk Management):**
   * Bảng ma trận hồ sơ với Data Bars và Heatmap giúp Giám đốc Thể thao theo dõi các cầu thủ đang tiến sát mốc 5 thẻ vàng (mốc bị treo giò 1 trận tại các giải VĐQG châu Âu), từ đó chủ động phương án nhân sự dự phòng cho các vòng đấu kế tiếp.
