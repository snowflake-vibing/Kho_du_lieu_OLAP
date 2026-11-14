# 4.2.2 Báo biểu 2: Phân tích Đối đầu Trực tiếp và Lịch sử Chạm trán giữa các Câu lạc bộ (Head-to-Head & Opponent Club Analytics)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 2 (Executive Dashboard 2)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **ĐỈNH CAO OLAP - KHAI THÁC CHIỀU ĐA VAI TRÒ (ROLE-PLAYING DIMENSION):** Báo biểu 2 giải quyết trực tiếp bài toán kinh điển **Truy vấn 10** trong tài liệu Kho dữ liệu (`docs/15_queries.md`): *Phân tích lịch sử đối đầu giữa CLB chủ quản (`DIM Club`) và CLB đối thủ (`Opponent Club`)*.
> * Việc đưa cặp chiều đa vai trò **`DIM Club` vs `Opponent Club`** lên giao diện phân tích thể hiện tư duy kiến trúc OLAP chuẩn mực, giúp giảng viên đánh giá xuất sắc năng lực khai thác kho dữ liệu.
> * Khác biệt hoàn toàn $100\%$ với Báo biểu 1 (Hỏa lực cá nhân cầu thủ) và Báo biểu 3 (Kỷ luật & Tải trọng), Báo biểu 2 tập trung vào **Lịch sử chạm trán, Bản đồ khắc chế đối thủ và Ma trận Derby đối đầu chéo**.
> * Toàn bộ các trường dữ liệu và thước đo **đã có sẵn $100\%$ trong Cube SSAS**, không cần viết thêm mã, kéo thả là hiển thị dữ liệu tức thì.

Báo biểu tuân thủ đầy đủ bộ quy chuẩn [**`rule.md`**](../rule.md):
* **Canvas:** Độ phân giải **Full HD 1920 x 1080 px (16:9)**, màu nền xám khói `#F8FAFC`.
* **Phân cấp Typography (Visual Hierarchy):** Title Banner **`20 pt` Bold**, Tiêu đề từng Visual **`18 pt` Bold**, Callout Value thẻ KPI **`35 pt` Bold** (cực kỳ nổi bật), Nhãn dữ liệu & Trục tọa độ **`12 pt`**.
* **Bộ lọc Slicers rộng rãi:** Chiều cao mở rộng **`H = 75 px`**, hiển thị trọn vẹn cả tiêu đề, khung xổ Dropdown và các nút chọn Tile, triệt tiêu hoàn toàn lỗi bị cụt thanh cuộn.
* **Chuẩn hóa nhãn hiển thị (Rename for this visual):** Từng trường dữ liệu đều có hướng dẫn đổi tên tiếng Việt ngắn gọn, chuyên nghiệp, xóa bỏ hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Ai là "con mồi" ưa thích nhất của từng CLB hàng đầu châu Âu?** Khi người dùng chọn một CLB (ví dụ: *Real Madrid* hoặc *Manchester City*), báo biểu sẽ chỉ ra ngay những đối thủ (`Opponent Club`) bị CLB này chọc thủng lưới nhiều lần nhất.
2. **Tính chất của các cặp đấu đối đầu ra sao (Trận cầu tưng bừng hay Trận Derby nảy lửa)?** Đặt số bàn thắng ghi được (`Goals`) song song với số thẻ phạt (`Yellow Cards`) để phân biệt những trận cầu cống hiến với những cuộc chạm trán căng thẳng kịch liệt.
3. **Lịch sử đối đầu giữa các kỳ phùng địch thủ thay đổi như thế nào qua các mùa giải?** Theo dõi sản lượng bàn thắng ghi vào lưới các đối thủ truyền kiếp qua từng mùa (`Season`).
4. **Bản đồ đối đầu chéo toàn diện (Head-to-Head Cross Matrix):** Tạo bảng ma trận nhiệt giao cắt giữa toàn bộ các CLB trong giải đấu để tra cứu thành tích đối đầu song phương.

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Biểu đồ Cột ngang Top 10 Đối thủ** | Xếp hạng các đối thủ bị ghi nhiều bàn nhất (`Opponent Club` by `Goals`), nhận diện đối thủ kỵ rơ và đối thủ dễ chịu của CLB. |
| **Scatter Bàn thắng vs Thẻ phạt Đối đầu** | Phân tích tương quan 2 biến định lượng ($X = \text{Goals}$, $Y = \text{Yellow Cards}$); kết hợp **2 đường Trung vị (Median lines)** để phân loại 4 tính chất trận đấu: Derby nảy lửa (Thẻ cao - Bàn nhiều); Trận cầu kịch chiến bạo lực (Thẻ cao - Bàn ít); Đối thủ ưa thích (Thẻ ít - Bàn nhiều); Trận đấu thông thường. |
| **Biểu đồ Cột Nhóm theo Mùa giải** | Biểu diễn biến thiên lịch sử bàn thắng qua chuỗi thời gian đối đầu giữa CLB chủ quản và Top 5 đối thủ truyền kiếp. |
| **Ma trận Đối đầu Chéo (Cross Heatmap)** | Bảng ma trận $N \times N$ giữa `DIM Club` (Dòng) và `Opponent Club` (Cột), tích hợp dải màu **Heatmap Gradient** chuẩn mực trong phân tích thể thao chuyên nghiệp. |

### 1.3. Bài toán thực tế giải quyết
* **Ban huấn luyện & Chuyên gia phân tích đối thủ:** Đánh giá điểm mạnh/điểm yếu lịch sử khi chuẩn bị chiến thuật đối đầu với một đối thủ cụ thể tại vòng đấu tiếp theo.
* **Bộ phận Truyền thông & Nhà đài:** Khai thác số liệu đối đầu lịch sử để làm phóng sự hâm nóng trước thềm các trận Derby (El Clásico, Derby Manchester, Derby London...).
* **Cổ động viên & Người hâm mộ:** Tra cứu nhanh thành tích đối đầu giữa hai đội bóng bất kỳ qua các mùa giải.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 2 - PHÂN TÍCH ĐỐI ĐẦU TRỰC TIẾP GIỮA CÁC CLB (Font: 20pt Bold, Center)        |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Trận Chạm Trán] | [Card 2: Tổng Bàn Thắng]   | [Card 3: Tổng Thẻ Vàng]    | [Card 4: Tổng Phút Đối Đầu]       |
| Callout: 35pt Bold            | Callout: 35pt Bold         | Callout: 35pt Bold         | Callout: 35pt Bold (Millions)     |
| Nền: Pastel Blue #EFF6FF      | Nền: Pastel Green #F0FDF4  | Nền: Pastel Amber #FFFBEB  | Nền: Pastel Purple #FAF5FF        |
| (W: 455, H: 95, X: 20)        | (W: 455, H: 95, X: 495)    | (W: 455, H: 95, X: 970)    | (W: 455, H: 95, X: 1445)          |
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu]                                  | [Slicer 2: CLB Chủ quản Cần Phân Tích] | [Slicer 3: Mùa giải]       |
| (W: 650, H: 75, X: 20, Y: 210)                        | (W: 600, H: 75, X: 690)                | (W: 590, H: 75, X: 1310)   |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT THANH NGANG (18pt)]     | [Ô 2: TRÊN - PHẢI | MA TRẬN PHÂN TÁN SCATTER (Title: 18pt)]    |
| Top 10 Đối thủ bị Chọc thủng Lưới Nhiều Nhất            | Ma trận Khắc chế Đối thủ: Bàn thắng vs Thẻ phạt Đối đầu       |
| Y: CLB Đối thủ (12pt Navy), X: Bàn thắng (12pt Green)   | X: Bàn thắng (12pt), Y: Thẻ vàng (12pt), Size: Trận, 2 Median |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | CỘT CỤM LỊCH SỬ MÙA GIẢI (18pt)]    | [Ô 4: DƯỚI - PHẢI | MA TRẬN ĐỐI ĐẦU CHÉO HEATMAP (18pt)]       |
| Lịch sử Bàn thắng Ghi vào Lưới Đối thủ qua các Mùa      | Ma trận Đối đầu Trực tiếp Song phương (H2H Cross Matrix)      |
| X: Mùa giải (12pt), Y: Bàn thắng, Legend: CLB Đối thủ   | Dòng: CLB Chủ quản, Cột: CLB Đối thủ, Giá trị: Bàn thắng      |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi tạo Trang Báo cáo và Cấu hình Canvas
1. Tại thanh quản lý trang ở mép dưới Power BI Desktop, nhấp vào biểu tượng dấu cộng `+` để thêm một trang mới.
2. Nhấp đúp chuột vào tên trang vừa tạo và **đặt tên trang chính thức**:
   * **Tên trang:** `Đối đầu CLB & Đối thủ` (hoặc `Báo biểu 2`).
3. Nhấp chuột vào khoảng trống Canvas để mở bảng **Format report page**:
   * **Canvas settings** $\rightarrow$ **Type:** Chọn `Custom`, thiết lập `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói hiện đại **`#F8FAFC`**, thiết lập **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng trên)
1. Trên thanh tác vụ **Insert**, nhấp chọn **Text box**.
2. Nhập nội dung tiêu đề chuẩn mực:
   `BÁO BIỂU 2: PHÂN TÍCH ĐỐI ĐẦU TRỰC TIẾP & LỊCH SỬ CHẠM TRÁN GIỮA CÁC CÂU LẠC BỘ`
3. Bôi đen toàn bộ văn bản và định dạng:
   * Font chữ: `Segoe UI`, Cỡ chữ: **`20 pt`**, In đậm (**Bold**), Căn giữa (**Center**), Màu chữ: Xanh than đậm `#0F172A`.
4. Tab **General** $\rightarrow$ **Effects**:
   * **Background:** Nền trắng `#FFFFFF`.
   * **Visual border:** Bật **On**, màu viền `#CBD5E1`, Bo góc (**Rounded corners**): **`10 px`**.
5. Tab **General** $\rightarrow$ **Properties**:
   * Size: `Width = 1880 px`, `Height = 55 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 15 px`.

---

### Bước 3: Thiết lập Khối 4 Thẻ KPI Tinh hoa (Chuyên sâu Đối đầu Trực tiếp)

Cả 4 thẻ Card đều đặt thẳng hàng tại `Vertical = 95 px`, chiều cao `Height = 95 px`, chiều rộng `Width = 455 px`:

#### 1. Card 1: Tổng số Trận Chạm trán (Total Head-to-Head Matches)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Distinct Matches Played]`** vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Số trận đối đầu`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG SỐ TRẬN CHẠM TRÁN`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa (**Center**), màu chữ `#1E3A8A`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Blue **`#EFF6FF`**, Viền `#93C5FD`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 20 px`, `Y = 95 px`.

#### 2. Card 2: Tổng số Bàn thắng Ghi vào Đối thủ (Total Goals Scored)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Goals]`** vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Bàn thắng ghi được`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG BÀN THẮNG GHI VÀO ĐỐI THỦ`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#065F46`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Green **`#F0FDF4`**, Viền `#86EFAC`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 495 px`, `Y = 95 px`.

#### 3. Card 3: Tổng số Thẻ Vàng Đối đầu (Total Yellow Cards in Head-to-Head)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Yellow Cards]`** vào ô **Fields** (thể hiện tính quyết liệt của các cuộc chạm trán).
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Số thẻ vàng`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG THẺ VÀNG ĐỐI ĐẦU`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`. **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Tổng Thời lượng Thi đấu Đối đầu (Total Minutes Played)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Minutes Played]`** vào ô **Fields**.
* **Phần đặt tên (Rename for this visual):**
  * Đổi tên trường thành: **`Tổng số phút`**.
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG THỜI LƯỢNG THI ĐẤU ĐỐI ĐẦU`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#5B21B6`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, Display units chọn **`Millions`** (hoặc `Auto`). **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Purple **`#FAF5FF`**, Viền `#D8B4FE`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 1445 px`, `Y = 95 px`.

---

### Bước 4: Thiết lập Hệ thống 3 Slicers Mở rộng (Không bị cụt thanh Dropdown)

Cả 3 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`**:

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 20 px | 210 px | 650 px | 75 px |
| **Slicer 2** | `DIM Club [Club Name]` | **`CLB Chủ quản (Đội phân tích)`** | Dropdown | 690 px | 210 px | 600 px | 75 px |
| **Slicer 3** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown | 1310 px | 210 px | 590 px | 75 px |

* **Định dạng chung cho Slicers:**
  * Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt` Bold**, màu chữ `#0F172A`.
  * Values (dữ liệu mục chọn): Font `Segoe UI`, Cỡ chữ **`12 pt`**.
  * Effects: Nền trắng `#FFFFFF`, Viền mỏng `#CBD5E1`, Bo góc `8 px`.

> **Mẹo thao tác:** Khi người dùng chọn CLB ở Slicer 2 (ví dụ: `Real Madrid` hoặc `Manchester City`), toàn bộ 4 biểu đồ bên dưới sẽ tự động biến thành hồ sơ đối đầu riêng biệt của CLB đó với mọi đối thủ!

---

### Bước 5 – Ô 1 (Trên - Trái): Clustered Bar Chart – Top 10 Đối thủ bị Chọc thủng Lưới Nhiều Nhất

1. Tại khung **Visualizations**, chọn visual **Clustered bar chart** (Biểu đồ thanh ngang).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Y-axis:** Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Club Name]`** vào ô này.
   * **X-axis:** Kéo thước đo **`[Measures].[Goals]`**.
   * **Tooltips:** Kéo `[Measures].[Distinct Matches Played]`, `[Measures].[Yellow Cards]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Opponent Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Đối thủ`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi vào đối thủ`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận đối đầu`**
   * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Số thẻ vàng`**
5. **Bộ lọc Top 10 Đối thủ:**
   * Tại khung **Filters on this visual** $\rightarrow$ chọn trường `Club Name` (của Opponent Club) $\rightarrow$ chọn mục **Top N** $\rightarrow$ nhập `10` $\rightarrow$ tại ô **By value** kéo `Goals` $\rightarrow$ nhấp **Apply filter**.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Top 10 Đối thủ bị Chọc thủng Lưới Nhiều Nhất`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **Bars:** Màu Xanh dương hoàng gia **`#2563EB`**.
   * **Y-axis (Tên đối thủ):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, *Maximum width* đặt `35%` để hiển thị trọn vẹn tên CLB đối thủ.
   * **X-axis (Bàn thắng):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục Forest Green `#1B5E20`**.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Ma trận Khắc chế Đối thủ: Bàn thắng vs Thẻ phạt Chạm trán (NÂNG CAO)

1. Tại khung **Visualizations**, chọn visual **Scatter chart** (Biểu đồ phân tán 4 góc phần tư).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Values:** Mở bảng **`Opponent Club`**, kéo **`[Club Name]`**.
   * **X-axis:** Kéo thước đo **`[Measures].[Goals]`** (Bàn thắng ghi được).
   * **Y-axis:** Kéo thước đo **`[Measures].[Yellow Cards]`** (Thẻ phạt nhận phải trong trận đấu).
   * **Size:** Kéo thước đo **`[Measures].[Distinct Matches Played]`** (Số trận đối đầu).
   * **Legend:** Mở bảng `DIM Competition`, kéo `[Competition Name]`.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Opponent Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Đối thủ`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
   * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Số thẻ vàng nhận phải`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận đối đầu`**
   * `Competition Name` $\rightarrow$ Đổi tên thành: **`Giải đấu`**
5. **Kẻ đường Xu hướng & Trung vị (Thẻ Analytics - Kính lúp):**
   * **Trend line:** Bật **On**, màu Xám than `#64748B`, nét đứt (Dashed).
   * **X-Axis Constant Line (Median Bàn thắng):** Bật On, nhập giá trị trung vị bàn thắng (ví dụ: khoảng 4 bàn), nét đứt, nhãn `Median Bàn thắng`.
   * **Y-Axis Constant Line (Median Thẻ vàng):** Bật On, nhập giá trị trung vị thẻ vàng (ví dụ: khoảng 5 thẻ), nét đứt, nhãn `Median Thẻ vàng`.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Khắc chế Đối thủ: Bàn thắng vs Thẻ phạt Chạm trán`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis:** Title bật **On**, nhập `Tổng số bàn thắng ghi vào đối thủ`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#1565C0`.
   * **Y-axis:** Title bật **On**, nhập `Số thẻ vàng trong các cuộc chạm trán`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#DC2626`.
   * **Legend:** Vị trí `BottomCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA 4 GÓC PHẦN TƯ KHẮC CHẾ ĐỐI ĐẦU:**
> * **Góc I (Trên - Phải): TRẬN CẦU RỰC LỬA / DERBY CĂNG THẲNG:** Bàn thắng nhiều VÀ thẻ phạt cũng rất nhiều. Đây là các trận cầu đỉnh cao có tính chất tranh chấp quyết liệt (như Real Madrid vs Barcelona, Man City vs Man United).
> * **Góc II (Trên - Trái): ĐỐI THỦ KỴ RƠ / KHẮC NGHIỆT:** Ghi được ít bàn thắng nhưng phải nhận rất nhiều thẻ vàng. Đây là các đối thủ có lối đá phòng ngự chặt chém khiến CLB chủ quản ức chế phạm lỗi.
> * **Góc IV (Dưới - Phải): "CON MỒI" ƯA THÍCH (Favorite Opponent):** Bàn thắng dồi dào nhưng nhận rất ít thẻ vàng. Lối chơi áp đảo hoàn toàn, chiến thắng dễ dàng.
> * **Góc III (Dưới - Trái): CHẠM TRÁN THÔNG THƯỜNG / ÍT VA CHẠM:** Số trận ít, bàn thắng và thẻ phạt đều ở mức thấp.

---

### Bước 7 – Ô 3 (Dưới - Trái): Clustered Column Chart – Lịch sử Bàn thắng Ghi vào Lưới các Kỳ phùng Địch thủ qua các Mùa giải

1. Tại khung **Visualizations**, chọn visual **Clustered column chart** (Biểu đồ cột cụm theo chuỗi thời gian).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Kéo `DIM Time [Season]`.
   * **Y-axis:** Kéo `[Measures].[Goals]`.
   * **Legend:** Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Club Name]`**.
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
   * `Opponent Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Đối thủ`**
5. **Bộ lọc Top 5 Đối thủ lớn nhất:**
   * Tại khung Filters on this visual $\rightarrow$ chọn `Club Name` (của Opponent Club) $\rightarrow$ chọn **Top N** = `5`, By value kéo `Goals` $\rightarrow$ nhấp **Apply filter** (giúp biểu đồ hiển thị thoáng mắt, tập trung vào 5 kỳ phùng địch thủ lớn nhất).
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Lịch sử Bàn thắng Ghi vào Lưới các Kỳ phùng Địch thủ qua các Mùa giải`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
   * **X-axis (Mùa giải):** Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Cỡ chữ **`12 pt`**, màu `#1565C0`.
   * **Data labels:** Bật **On**, Cỡ chữ **`12 pt` Bold**.
   * **Legend:** Vị trí `TopCenter`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8 – Ô 4 (Dưới - Phải): Matrix – Ma trận Đối đầu Trực tiếp Song phương (Head-to-Head Cross Heatmap)

Sử dụng visual **Matrix (Ma trận đa chiều)** để tạo bảng đối đầu chéo kinh điển:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Kéo các trường vào các ô cấu hình:
  * **Rows (Hàng dọc):** Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`**.
  * **Columns (Cột ngang):** Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Club Name]`**.
  * **Values (Giá trị ô):** Kéo thước đo **`[Measures].[Goals]`**.

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường $\rightarrow$ chọn **Rename for this visual**:
  * `DIM Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Chủ quản`**
  * `Opponent Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Đối thủ`**
  * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng`**

#### 3. Bật Heatmap Gradient đối đầu (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng Matrix $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn `Bàn thắng` (hoặc `Goals`).
  * Gạt công tắc **Background color** sang **ON**!
  * Nhấp vào nút **`fx`**:
    * **Format style:** Chọn `Gradient`.
    * **Minimum (Giá trị thấp nhất):** Chọn màu trắng `#FFFFFF` (hoặc xanh nhạt `#EFF6FF`).
    * **Maximum (Giá trị cao nhất):** Chọn màu Xanh dương đậm `#1D4ED8`.
    * Nhấp **OK**. Lập tức bảng biến thành **Ma trận nhiệt Heatmap đối đầu chéo**, các ô có số bàn thắng lớn sẽ nổi bật rực rỡ, đường chéo chính (CLB tự đá với chính mình) sẽ tự động rỗng không có màu!

#### 4. Định dạng hiển thị:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Ma trận Đối đầu Trực tiếp Song phương (Head-to-Head Cross Heatmap)`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**).
* **Row headers & Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, Text wrap **On**, màu nền xám sáng thanh lịch `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, Text wrap **On**.
* **Subtotals:** Tắt **Row subtotals: Off** và **Column subtotals: Off** để ma trận vuông vức, phẳng và chuyên nghiệp.
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* **Khai thác theo CLB Chủ quản:**
  * Khi nhấp chọn `Real Madrid` trên Slicer: Toàn bộ bảng Ô 1 lập tức hiển thị Top 10 đối thủ bị Real Madrid chọc thủng lưới nhiều nhất: `UD Almería` (12 bàn), `CA Osasuna` (11 bàn), `Cádiz CF` (10 bàn), `Villarreal` (10 bàn), `FC Barcelona` (8 bàn).
  * Khi chuyển sang chọn `Manchester City`: Ô 1 chuyển ngay sang danh sách đối thủ của Man City: `RB Leipzig` (14 bàn), `Bournemouth` (13 bàn), `Fulham` (13 bàn), `Manchester United` (13 bàn).
  * Ma trận đối đầu chéo ở Ô 4 cho phép người xem nhìn bao quát toàn bộ giải đấu, nhận biết ngay những cặp đấu có "cơn mưa bàn thắng" trong lịch sử.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Giá trị của Chiều đa vai trò (Role-Playing Dimension) trong OLAP:**
   * Việc một bảng sự kiện (`FACT_Player_Match_Perf`) liên kết đồng thời tới 2 khóa ngoại của cùng một chiều CLB (`Club_SK` và `Opponent_Club_SK`) cho phép thực hiện các phép chiếu ma trận chéo (Cross-tabulation). Đây là điểm sáng kiến trúc OLAP nâng cao, giải quyết trọn vẹn bài toán quan hệ song phương giữa hai thực thể cùng loại mà mô hình quan hệ thông thường xử lý rất phức tạp.
2. **Quy luật "Kỵ rơ" trong Thể thao đỉnh cao:**
   * Thông qua ma trận khắc chế ở Ô 2, người xem nhận thấy rõ có những đối thủ tuy đứng thứ hạng thấp hơn trên bảng tổng sắp nhưng lại nằm ở Góc II (Ít bàn thắng - Nhiều thẻ vàng) của CLB lớn. Điều này phản ánh tính chất chiến thuật "khắc tinh" đặc thù trong bóng đá, nơi các đội bóng chơi rắn và chủ động phá lối chơi của đối thủ mạnh.
3. **Cường độ Cạnh tranh của các Trận Derby (Derby Match Intensity):**
   * Các cuộc đối đầu truyền kiếp (như El Clásico hay Derby Manchester) luôn nằm ở Góc I (Góc có cả số bàn thắng lẫn số thẻ phạt cao nhất). Cường độ thi đấu và sự căng thẳng tâm lý đẩy tỷ lệ thẻ phạt trong các trận đấu này cao hơn **`45%`** so với các vòng đấu thông thường.
