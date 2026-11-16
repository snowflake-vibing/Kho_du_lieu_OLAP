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
1. **Những CLB nào có rủi ro kỷ luật cao nhất châu Âu?** Xếp hạng tổng lượng thẻ phạt cảnh cáo (`Yellow Cards`) và thẻ phạt đuổi khỏi sân (`Red Cards`) theo từng CLB.
2. **Biến động thứ hạng về đóng góp bàn thắng của các CLB hàng đầu châu Âu qua các mùa giải?** Sử dụng biểu đồ dải ruy băng xếp hạng (Ribbon Chart) để theo dõi sự dịch chuyển thứ hạng về tổng đóng góp bàn thắng (`Goal Contributions = Goals + Assists`) của các CLB (`Club Name`) qua các mùa giải (`Season`), nhận diện những đội bóng bứt phá ngoạn mục hoặc sa sút phong độ tấn công qua từng mùa.
3. **Độ tuổi nào trong bóng đá chuyên nghiệp đang phải gánh tải trọng thi đấu lớn nhất và có xu hướng phạm lỗi nhiều nhất?** Đặt số phút thi đấu (`Minutes Played`) và số thẻ phạt (`Yellow Cards`) trên cùng trục độ tuổi (`Age`).
4. **Vị trí thi đấu chuyên môn nào trên sân là "điểm nóng" gánh chịu nhiều thẻ đỏ nhất?** Phân tích cơ cấu và tỷ trọng thẻ đỏ theo vị trí cụ thể (`Sub Position`: *Trung vệ, Tiền vệ phòng ngự, Tiền đạo cắm...*).

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Stacked Bar Chart (Vàng + Đỏ)** | So sánh tổng lượng thẻ phạt và cơ cấu mức độ nghiêm trọng (thẻ vàng cảnh cáo vs thẻ đỏ trực tiếp/gián tiếp) giữa các CLB hàng đầu. |
| **Ribbon Chart (Dải Ruy Băng Xếp Hạng)** | Theo dõi trực quan sự thay đổi thứ hạng (Rank Change) về tổng đóng góp bàn thắng (`Goal Contributions`) của các CLB hàng đầu châu Âu (`Club Name`) qua các mùa giải (`Season`). Khắc họa rõ nét sự trỗi dậy hay sa sút hỏa lực tấn công của từng đội bóng và tương tác mượt mà khi lọc theo từng Giải đấu. |
| **Combo Chart 2 Trục Y (Dual Axis)** | Đặt tải trọng thời lượng (Cột - Trục Y trái) và số thẻ phạt (Đường - Trục Y phải) trên cùng một trục danh mục độ tuổi (`Age`), giải quyết bài toán so sánh 2 đại lượng khác thang đo (Khử Exposure Bias). |
| **Donut Chart (Tỷ trọng Thẻ đỏ theo Vị trí)** | Trực quan hóa tỷ trọng thẻ đỏ theo từng vị trí chuyên môn trên sân (`Sub Position`), nhận diện mắt xích rủi ro kỷ luật chiến thuật cao nhất toàn đội hình. |

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
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải]          | [Slicer 2: Giải đấu]       | [Slicer 3: Quốc gia]       | [Slicer 4: Vị trí thi đấu]        |
| (W: 455, H: 75, X: 20, Y: 210)| (W: 455, H: 75, X: 495)    | (W: 455, H: 75, X: 970)    | (W: 455, H: 75, X: 1445)          |
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH XẾP CHỒNG (18pt)]     | [Ô 2: TRÊN - PHẢI | BIỂU ĐỒ DẢI RUY BĂNG RIBBON (18pt)]  |
| Top 10 CLB nhận Nhiều Thẻ Phạt Nhất (Thẻ Vàng & Thẻ Đỏ) | Xếp hạng Đóng góp Bàn thắng (G+A) theo CLB qua các Mùa|
| Y: CLB (12pt Navy), X: Thẻ (12pt), Màu Vàng/Đỏ ngữ nghĩa| X: Mùa giải (12pt), Y: Đóng góp G+A, Legend: CLB       |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | COMBO CHART 2 TRỤC Y (18pt)]        | [Ô 4: DƯỚI - PHẢI | BIỂU ĐỒ VÀNH KHĂN DONUT (Title: 18pt)]     |
| Tải trọng Thi đấu (Cột) & Thẻ phạt (Đường) theo Độ tuổi | Phân bổ Thẻ Đỏ theo Vị trí Chi tiết (Sub Position)            |
| X: Tuổi (12pt), Y-trái: Phút (Xanh), Y-phải: Thẻ (Đỏ)   | Legend: Vị trí (Trung vệ, Tiền đạo...), Values: Thẻ đỏ (12pt) |
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

### Bước 4: Thiết lập Hệ thống 4 Slicers Đối xứng Cân bằng (Không bị cụt thanh Dropdown)

Cả 4 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`**, chiều rộng cân xứng $W = 455\text{ px}$ thẳng hàng với 4 thẻ KPI:

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown | 20 px | 210 px | 455 px | 75 px |
| **Slicer 2** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 495 px | 210 px | 455 px | 75 px |
| **Slicer 3** | `DIM Competition [Country Name]` | **`Quốc gia`** | Dropdown | 970 px | 210 px | 455 px | 75 px |
| **Slicer 4** | `DIM Player [Main Position]` | **`Vị trí thi đấu`** | Dropdown | 1445 px | 210 px | 455 px | 75 px |

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

### Bước 6 – Ô 2 (Trên - Phải): Ribbon Chart – Xếp hạng Đóng góp Bàn thắng (Goal Contributions) của các CLB qua các Mùa giải

1. Tại khung **Visualizations**, chọn visual **Ribbon chart** (Biểu đồ Dải ruy băng xếp hạng theo thời gian).
2. Kích thước & Vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`.
   * **Position:** `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis (Trục hoành):** Mở bảng **`DIM Time`**, kéo thuộc tính **`[Season]`** (Mùa giải: *2022/2023* và *2023/2024*).
   * **Y-axis (Trục tung):** Mở thư mục **`Measures`**, kéo thước đo **`[Measures].[Goal Contributions]`** (Tổng đóng góp bàn thắng = Bàn thắng + Kiến tạo).
   * **Legend (Nhóm dải ruy băng):** Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`** (Tên Câu lạc bộ).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Club Name` $\rightarrow$ Đổi tên thành: **`Câu lạc bộ`**
   * `Goal Contributions` $\rightarrow$ Đổi tên thành: **`Đóng góp G+A`**
5. **Cấu hình Bộ lọc Top 8 CLB hàng đầu (Filters on this visual):**
   * Tại khung **Filters on this visual**, mở mục `Câu lạc bộ` (hoặc `Club Name`).
   * Chọn Filter type: **Top N**, nhập **`8`** (hoặc `6`).
   * Ô **By value**: Kéo thước đo **`[Measures].[Goal Contributions]`** vào.
   * Nhấp nút **Apply filter** (Tập trung hiển thị 8 CLB có tổng đóng góp bàn thắng cao nhất: *Manchester City, Bayern Munich, PSV Eindhoven, Real Madrid, Bayer 04 Leverkusen, Feyenoord Rotterdam, SL Benfica, Paris Saint-Germain* để các dải ruy băng to bản, uốn lượn sắc sảo, không bị rối mắt).
6. **Định dạng hiển thị chi tiết (Tab Format visual):**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Xếp hạng Đóng góp Bàn thắng (G+A) theo CLB qua các Mùa giải`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **Ribbons:** Bật **Ribbons: On**, Spacing: `0`, Match series color: **On**, Transparency: **`25% - 30%`** để tạo hiệu ứng chuyển động mượt mà.
   * **Data labels:** Bật **On**, Display units: **`None`** (hiển thị chính xác số nguyên đóng góp bàn thắng của từng CLB), Cỡ chữ **`10 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Font `Segoe UI`, Cỡ chữ **`11 pt`**.
   * **X-axis (Mùa giải):** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#0F172A`.
   * **Y-axis (Đóng góp G+A):** Title bật **On**, nhập `Tổng đóng góp bàn thắng (G+A)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#1E3A8A`.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ & SỰ ĐỘC ĐÁO CỦA RIBBON CHART:**
> * **Độc nhất vô nhị trong toàn bộ dự án:** Ribbon Chart trực quan hóa **sự hoán đổi thứ hạng (Rank Changes)** của các CLB qua từng mùa giải, làm nổi bật ngay những màn bứt phá hoặc tụt hạng ngoạn mục về hỏa lực tấn công.
> * **Phát hiện điểm nhấn thực tế từ Cube:** Nhìn vào 8 CLB dẫn đầu châu Âu, người xem thấy ngay cú lội ngược dòng ngoạn mục của **Bayer 04 Leverkusen** (vọt từ hạng 8 với **`137` G+A** mùa `2022/2023` lên chiếm ngôi đầu **`224` G+A** mùa `2023/2024`), sự thăng tiến của **PSV Eindhoven** (`180` $\rightarrow$ `216`) và **Real Madrid** (`179` $\rightarrow$ `206`), đối lập với đà giảm của **SL Benfica** (`194` $\rightarrow$ `164`).
> * **Tương tác đa chiều thông minh với Slicer Giải đấu:** Khi người dùng chọn một giải đấu cụ thể trên Slicer 2 (như `laliga`), biểu đồ không bị co thành 1 dải đơn lẻ mà lập tức chuyển thành bảng xếp hạng cuộc đua G+A giữa các CLB thuộc chính giải đấu đó.
> * **Bổ sung góc nhìn cho Ô 1:** Ô 1 xếp hạng rủi ro thẻ phạt CLB (Kỷ luật), còn Ô 2 theo dõi biến động thứ hạng đóng góp bàn thắng CLB qua thời gian, tạo sự đối chiếu toàn diện giữa **Hiệu suất tấn công** và **Giá phải trả về Kỷ luật**.

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

### Bước 8 – Ô 4 (Dưới - Phải): Donut Chart – Phân bổ Thẻ Đỏ theo Vị trí Chi tiết trên Sân (Sub Position)

Sử dụng visual **Donut chart (Biểu đồ Vành khăn)** để phân rã tỷ trọng thẻ đỏ theo vị trí thi đấu cụ thể, xóa bỏ hoàn toàn bảng Table lặp lại giữa các trang báo cáo:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Tại khung **Visualizations**, chọn visual **Donut chart** (biểu tượng hình vành khăn tròn).
* Kéo các trường vào ô cấu hình:
  * **Legend:** Mở bảng **`DIM Player`**, kéo thuộc tính **`[Sub Position]`** (Vị trí thi đấu cụ thể: *Centre-Back, Centre-Forward, Defensive Midfield, Central Midfield, Right-Back, Left-Back...*).
  * **Values:** Kéo thước đo **`[Measures].[Red Cards]`** (Tổng số thẻ đỏ).

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường trong ô Legend / Values $\rightarrow$ chọn **Rename for this visual**:
  * `Sub Position` $\rightarrow$ Đổi tên thành: **`Vị trí chi tiết`**
  * `Red Cards` $\rightarrow$ Đổi tên thành: **`Số thẻ đỏ`**

#### 3. Cấu hình Bộ lọc Top 8 Vị trí nhận nhiều thẻ đỏ nhất (Filters on this visual):
* Tại khung **Filters on this visual**, mở mục `Vị trí chi tiết` (hoặc `Sub Position`).
* Chọn Filter type: **Top N**, nhập **`8`**.
* Ô **By value**: Kéo thước đo **`[Measures].[Red Cards]`** vào.
* Nhấp nút **Apply filter** (Tập trung hiển thị 8 vị trí có nguy cơ thẻ đỏ cao nhất, loại bỏ các vị trí không có thẻ).

#### 4. Định dạng hiển thị chi tiết (Tab Format visual):
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Phân bổ Thẻ Đỏ theo Vị trí Chi tiết trên Sân`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
* **Slices (Màu sắc các lát cắt):**
  * `Centre-Back` (Trung vệ): Đặt màu Đỏ sẫm chủ đạo **`#DC2626`** (vị trí nhận nhiều thẻ đỏ nhất).
  * `Centre-Forward` (Tiền đạo cắm): Màu Cam đậm **`#EA580C`**.
  * `Defensive Midfield` (Tiền vệ phòng ngự): Màu Xanh dương đậm **`#1D4ED8`**.
  * `Right-Back / Left-Back`: Màu Xanh lục / Tím.
* **Detail labels (Nhãn số liệu chi tiết):**
  * Position: `Outside`.
  * Label contents: Chọn **`Category, percent of total`** (hiển thị Tên vị trí và Tỷ lệ phần trăm) hoặc `All detail labels`.
  * Font `Segoe UI`, Cỡ chữ **`11 pt` Bold**.
* **Legend:** Vị trí `RightCenter`, Font `Segoe UI`, Cỡ chữ **`12 pt`**.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ CỦA DONUT CHART VỊ TRÍ CHI TIẾT:**
> * **Giải phóng sự trùng lặp:** Cả Báo biểu 1 và 2 đều đã có Table tra cứu, việc dùng Donut Chart tại Ô 4 của Báo biểu 3 giúp toàn bộ bộ 3 báo cáo có cấu trúc visual phong phú, đa dạng và bắt mắt $100\%$.
> * **Phát hiện chiến thuật cốt lõi:** Trung vệ (`Centre-Back`) gánh tới **`253 thẻ đỏ`** (chiếm hơn $35\%$ tổng số thẻ đỏ toàn giải đấu). Đặc biệt, Tiền đạo cắm (`Centre-Forward`) nhận tới **`89 thẻ đỏ`**, cao hơn cả Tiền vệ phòng ngự (`84 thẻ đỏ`) do các tình huống trả đũa va chạm hoặc tiểu xảo khi tranh chấp bóng bổng!

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* Khi nhấp chọn giải đấu `laliga` trên Slicer 2:
  * Thẻ KPI cập nhật tức thời: La Liga ghi nhận tới **`135 thẻ đỏ`** và **`3,686 thẻ vàng`**.
  * Biểu đồ Ribbon Chart ở Ô 2 lập tức thu hẹp về các CLB tại La Liga, làm nổi bật vị thế dẫn đầu của `Real Madrid` (`133` $\rightarrow$ `155` G+A) và cú bứt phá của `Girona FC` (vọt từ `101` lên `150` G+A để vượt qua `FC Barcelona` `134` và `Atlético de Madrid` `118`).
  * Donut Chart ở Ô 4 phân rã ngay tỷ trọng thẻ đỏ tại La Liga theo từng vị trí phòng ngự và tấn công.
  * Biểu đồ Combo ở Ô 3 phản ánh chính xác nhóm tuổi nào tại giải đấu này chịu tải trọng và thẻ phạt cao nhất.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Sự khác biệt về Văn hóa Kỷ luật và Triết lý Trọng tài giữa các Giải đấu:**
   * So sánh giữa La Liga (135 thẻ đỏ) và Premier League (chỉ 46 thẻ đỏ) minh chứng rõ nét sự khác biệt giữa hai trường phái: bóng đá Tây Ban Nha đề cao sự nghiêm ngặt và xử phạt triệt để các hành vi phạm lỗi, trong khi bóng đá Anh ưu tiên tính liên tục của trận đấu và độ va chạm thể lực cao mà không rút thẻ đỏ tràn lan.
2. **Quy luật Tải trọng theo Chu kỳ Độ tuổi (Age Load Curve):**
   * Biểu đồ Combo 2 trục thể hiện rõ đỉnh parabol của tải trọng thi đấu rơi vào nhóm tuổi **24 – 29 tuổi** (giai đoạn sung sức nhất của sự nghiệp cầu thủ). Đường thẻ vàng bám sát theo độ dốc của số phút thi đấu chứng minh thẻ phạt trong bóng đá hiện đại là hệ quả tự nhiên của cường độ tranh chấp thể lực, thay vì yếu tố tâm lý bộc phát của cầu thủ trẻ.
3. **Phân bổ Rủi ro Thẻ phạt theo Cấu trúc Đội hình (Tactical Disciplinary Hotspots):**
   * Donut Chart chỉ ra trung vệ và các hậu vệ biên là "lá chắn lửa" chịu áp lực lớn nhất từ các đợt phản công của đối phương, dẫn đến các pha phạm lỗi chiến thuật (Tactical Foul) để ngăn chặn bàn thắng mười mươi. Ban huấn luyện cần đặc biệt chú trọng xây dựng phương án bọc lót khu vực trung lộ để giảm tải số lần trung vệ phải đối đầu trực tiếp 1-1.
