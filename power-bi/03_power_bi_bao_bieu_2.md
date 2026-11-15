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
2. **Áp lực từ "Chảo lửa Sân khách" ảnh hưởng ra sao đến hiệu suất ghi bàn?** Sử dụng Combo Chart 2 trục Y để đối chiếu giữa Sức chứa khán đài của đối thủ (`Opponent Club [Stadium Seats]`) và Bàn thắng ghi được (`Goals`) trên các sân vận động khách (`Stadium Name`), kiểm chứng hiệu ứng áp lực khán giả.
3. **Biến thiên bàn thắng đối đầu theo chu kỳ các tháng trong mùa giải?** Biểu đồ vùng (Area Chart) theo dõi phân bố bàn thắng theo từng tháng (`Month`) qua các mùa giải (`Season`), nhận diện thời điểm bùng nổ bàn thắng đối đầu đỉnh cao trong năm.
4. **Bảng danh mục cặp đấu đối đầu kinh điển (Head-to-Head Matchup Table):** Liệt kê chi tiết các cặp đấu có nhiều bàn thắng nhất giữa CLB chủ quản và CLB đối thủ, tích hợp thanh dữ liệu trực quan (Data Bars) và số thẻ phạt, triệt tiêu 100% ô trống NULL.

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Biểu đồ Cột ngang Top 10 Đối thủ** | Xếp hạng các đối thủ bị ghi nhiều bàn nhất (`Opponent Club` by `Goals`), nhận diện đối thủ kỵ rơ và đối thủ dễ chịu của CLB. |
| **Combo Chart 2 Trục Y Chảo lửa Sân khách** | Đối soát tương quan trực quan giữa Sức chứa Sân vận động đối thủ (Cột - Trục Y trái) và Bàn thắng ghi được (Đường - Trục Y phải) trên từng sân vận động khách (`Stadium Name`). Giải quyết câu hỏi về hiệu ứng áp lực chảo lửa sân khách. |
| **Area Chart (Biểu đồ Vùng xếp chồng)** | Theo dõi biến thiên bàn thắng theo chu kỳ các Tháng trong năm phân lớp theo Mùa giải (`Season`). Phản ánh rõ phong độ đối đầu bùng nổ vào giai đoạn nước rút hay đầu mùa. |
| **Bảng Danh mục Cặp đấu Đối đầu (Table + Data Bars)** | Bảng phẳng liệt kê các cặp đấu chạm trán thực tế giữa `DIM Club` và `Opponent Club`, hiển thị Bàn thắng (`Goals`) kèm thanh dữ liệu **Data Bars** và Thẻ phạt (`Yellow Cards`). Tự động lọc sạch 100% các ô NULL, không bị loãng dữ liệu. |

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
| [Slicer 1: Giải đấu]          | [Slicer 2: CLB Chủ quản]   | [Slicer 3: Mùa giải]       | [Slicer 4: Tháng thi đấu]         |
| (W: 455, H: 75, X: 20, Y: 210)| (W: 455, H: 75, X: 495)    | (W: 455, H: 75, X: 970)    | (W: 455, H: 75, X: 1445)          |
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT THANH NGANG (18pt)]     | [Ô 2: TRÊN - PHẢI | COMBO CHART 2 TRỤC Y (Title: 18pt)]        |
| Top 10 Đối thủ bị Chọc thủng Lưới Nhiều Nhất            | Chảo lửa Sân khách: Sức chứa [Cột Y1] vs Bàn thắng [Đường Y2] |
| Y: CLB Đối thủ (12pt Navy), X: Bàn thắng (12pt Green)   | X: Sân khách (12pt), Cột: Chỗ ngồi (12pt), Đường: Bàn thắng   |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BIỂU ĐỒ VÙNG DIỆN TÍCH AREA (18pt)] | [Ô 4: DƯỚI - PHẢI | BẢNG CẶP ĐẤU ĐỐI ĐẦU TABLE (18pt)]     |
| Biến thiên Bàn thắng theo Tháng qua các Mùa giải         | Bảng Danh mục Cặp đấu Kinh điển: Bàn thắng & Thẻ phạt          |
| X: Tháng (12pt), Y: Bàn thắng, Legend: Mùa giải         | Cột: CLB Chủ quản, CLB Đối thủ, Bàn thắng (Data Bars), Thẻ phạt|
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

### Bước 4: Thiết lập Hệ thống 4 Slicers Đối Xứng Chuẩn Nghiệp Vụ (Mùa giải & Tháng)

Cả 4 bộ lọc đều được đặt tại `Vertical = 210 px`, chiều cao mở rộng **`Height = 75 px`**, chiều rộng đều đặn **`Width = 455 px`** (thẳng hàng và khớp $100\%$ với 4 thẻ KPI bên trên):

| Slicer | Trường dữ liệu | **Phần đặt tên (Rename for this visual)** | Kiểu hiển thị | X | Y | W | H |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Slicer 1** | `DIM Competition [Competition Name]` | **`Giải đấu`** | Dropdown | 20 px | 210 px | 455 px | 75 px |
| **Slicer 2** | `DIM Club [Club Name]` | **`CLB Chủ quản (Đội phân tích)`** | Dropdown | 495 px | 210 px | 455 px | 75 px |
| **Slicer 3** | `DIM Time [Season]` | **`Mùa giải`** | Dropdown / Tile | 970 px | 210 px | 455 px | 75 px |
| **Slicer 4** | `DIM Time [Month]` | **`Tháng thi đấu`** | Dropdown / Tile | 1445 px | 210 px | 455 px | 75 px |

* **Định dạng chung cho Slicers:**
  * Slicer header: Font `Segoe UI`, Cỡ chữ **`15 pt` Bold**, màu chữ `#0F172A`.
  * Values (dữ liệu mục chọn): Font `Segoe UI`, Cỡ chữ **`12 pt`**.
  * Effects: Nền trắng `#FFFFFF`, Viền mỏng `#CBD5E1`, Bo góc `8 px`.

> **Ưu điểm nghiệp vụ thể thao tuyệt đối:**
> 1. **Chuẩn mực Mùa giải bóng đá:** Không dùng năm dương lịch (1/1 – 31/12) gây xé lẻ mùa giải. Sử dụng **`Season`** (ví dụ `2023/2024`) kết hợp **`Month`** (Tháng) giúp người xem đánh giá chính xác phong độ đối đầu của CLB ở từng giai đoạn: đầu mùa (tháng 8–9), kỳ nghỉ đông (tháng 12–1) hoặc giai đoạn nước rút tranh cúp vô địch (tháng 4–5).
> 2. **Bố cục đối xứng 1:1 hoàn hảo:** 4 thẻ KPI rộng 455px đặt ngay trên 4 bộ lọc Slicers rộng 455px, tạo cấu trúc phân vùng cân đối tuyệt đối.

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

### Bước 6 – Ô 2 (Trên - Phải): Combo Chart 2 Trục Y – Áp lực Chảo lửa Sân khách: Sức chứa Khán đài vs Bàn thắng Ghi được (Line and Clustered Column Chart)

1. Tại khung **Visualizations**, chọn visual **Line and clustered column chart** (Biểu đồ kết hợp Cột cụm và Đường với 2 trục Y độc lập).
2. Kích thước & Vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`.
   * **Position:** `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Stadium Name]`** (Tên sân vận động của đối thủ).
   * **Column y-axis (Trục Y trái - Cột):** Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Stadium Seats]`** (Sức chứa chỗ ngồi của sân khách).
   * **Line y-axis (Trục Y phải - Đường):** Kéo thước đo **`[Measures].[Goals]`** (Số bàn thắng ghi được trên sân này).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Opponent Club [Stadium Name]` $\rightarrow$ Đổi tên thành: **`Sân vận động Đối thủ`**
   * `Stadium Seats` $\rightarrow$ Đổi tên thành: **`Sức chứa khán đài (Chỗ ngồi)`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
5. **Cấu hình Bộ lọc Top 10 Sân vận động hỏa lực lớn nhất (Filters on this visual):**
   * Tại khung **Filters on this visual**, mở mục `Sân vận động Đối thủ` (hoặc `Stadium Name`).
   * Chọn Filter type: **Top N**, nhập **`10`**.
   * Ô **By value**: Kéo thước đo **`[Measures].[Goals]`** vào.
   * Nhấp nút **Apply filter** (Tập trung hiển thị 10 chảo lửa sân khách có nhiều bàn thắng nhất, e.g. Giuseppe Meazza, Olimpico di Roma, Jan Breydelstadion...).
6. **Định dạng hiển thị chi tiết (Tab Format visual):**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Áp lực Chảo lửa Sân khách: Sức chứa Khán đài vs Bàn thắng Ghi được`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **Columns (Màu cột sức chứa):** Đặt màu Cột xanh dương đậm hiện đại `#2563EB`.
   * **Lines (Màu đường bàn thắng):** Đặt màu Đường đỏ cam rực lửa `#EF4444`, Stroke width: `3 px`.
   * **Markers (Điểm đánh dấu trên đường):** Bật **On**, Shape: Tròn (Circle), Size: `6`, Màu nền `#DC2626`.
   * **Data labels:** Bật **On**, Cỡ chữ **`11 pt` Bold**.
   * **X-axis (Tên sân khách):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis (Cột - Trục Y trái):** Title bật **On**, nhập `Sức chứa sân khách (chỗ ngồi)`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#2563EB`.
   * **Secondary y-axis (Đường - Trục Y phải):** Title bật **On**, nhập `Bàn thắng ghi được`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#DC2626`.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ CỦA COMBO CHART CHẢO LỬA SÂN KHÁCH:**
> * **Giải quyết bài toán tâm lý thi đấu sân khách:** Phân tích xem quy mô khán đài khổng lồ của đối thủ (như San Siro 75k chỗ, Olimpico 70k chỗ) có tạo ra áp lực đè nặng khiến hiệu suất ghi bàn của đội khách sụt giảm hay không.
> * **Khác biệt 100% về chiều phân tích:** Trục X khai thác trực tiếp thuộc tính `Stadium Name` và `Stadium Seats` của chiều đa vai trò `Opponent Club`, hoàn toàn không trùng lặp với bất kỳ biểu đồ nào trong toàn bộ hệ thống báo cáo!

---

### Bước 7 – Ô 3 (Dưới - Trái): Area Chart – Biến thiên Bàn thắng Đối đầu theo Tháng qua các Mùa giải (Biểu đồ Vùng xếp chồng)

1. Tại khung **Visualizations**, chọn visual **Area chart** (Biểu đồ Vùng diện tích).
2. Kích thước & Vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`.
   * **Position:** `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu:
   * **X-axis:** Mở bảng **`DIM Time`**, kéo thuộc tính **`[Month]`** (Tháng 1 đến Tháng 12).
   * **Y-axis:** Kéo thước đo **`[Measures].[Goals]`** (Bàn thắng ghi được).
   * **Legend:** Mở bảng **`DIM Time`**, kéo thuộc tính **`[Season]`** (Mùa giải).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Month` $\rightarrow$ Đổi tên thành: **`Tháng`**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
5. **Định dạng hiển thị chi tiết (Tab Format visual):**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Biến thiên Bàn thắng Đối đầu theo Tháng qua các Mùa giải`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **X-axis (Tháng):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Tổng số bàn thắng`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#1E3A8A`.
   * **Lines & Colors:** Các dải màu mùa giải trong suốt tinh tế (Transparency `40% - 60%`), tạo hiệu ứng vùng màu xếp lớp uốn lượn đẹp mắt.
   * **Legend:** Vị trí `TopCenter`, Font `Segoe UI`, Cỡ chữ **`12 pt`**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ CỦA BIỂU ĐỒ VÙNG (AREA CHART):**
> * Khắc họa rõ nét nhịp điệu phong độ và tính chu kỳ của các giải đấu bóng đá châu Âu theo các tháng trong năm (khởi động vào tháng 8-9, duy trì ổn định qua mùa đông tháng 11-12, và bùng nổ bàn thắng ở giai đoạn nước rút quyết định tháng 3-4-5).
> * Việc xếp chồng các diện tích mùa giải giúp so sánh trực tiếp sản lượng bàn thắng giữa các mùa giải xem mùa nào có hỏa lực bùng nổ hơn vào cùng một thời điểm trong năm.

---

### Bước 8 – Ô 4 (Dưới - Phải): Table – Bảng Danh mục Cặp đấu Đối đầu Kinh điển (Head-to-Head Matchup Table + Data Bars)

Sử dụng visual **Table (Bảng phẳng danh mục)** thay thế cho bảng ma trận 2 chiều, giúp loại bỏ hoàn toàn các ô trống NULL và hiển thị trực diện các cặp đấu có hỏa lực mạnh nhất:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Tại khung **Visualizations**, chọn visual **Table** (biểu tượng bảng danh sách phẳng).
* Kéo các trường vào ô **Columns**:
  1. Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`**.
  2. Mở bảng **`Opponent Club`**, kéo thuộc tính **`[Club Name]`**.
  3. Kéo thước đo **`[Measures].[Goals]`**.
  4. Kéo thước đo **`[Measures].[Yellow Cards]`**.

#### 2. Phần đặt tên chuẩn tiếng Việt (Rename for this visual):
* Nhấp chuột phải vào từng trường trong ô Columns $\rightarrow$ chọn **Rename for this visual**:
  * `DIM Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Chủ quản`**
  * `Opponent Club [Club Name]` $\rightarrow$ Đổi tên thành: **`CLB Đối thủ`**
  * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng`**
  * `Yellow Cards` $\rightarrow$ Đổi tên thành: **`Thẻ vàng`**

#### 3. Bật thanh dữ liệu Data Bars trực quan cho cột Bàn thắng (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng Table $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn trường **`Bàn thắng`** (hoặc `Goals`).
  * Gạt công tắc **Data bars** sang **ON**!
  * Nhấp vào nút **`fx`** bên cạnh Data bars:
    * **Positive bar:** Chọn màu Xanh dương hiện đại **`#2563EB`** (hoặc `#3B82F6`).
    * **Bar direction:** Chọn `Left to right` (Trái sang phải).
    * Mục **Show bar only:** Để **Off** (hiển thị cả con số bàn thắng bên cạnh thanh màu).
    * Nhấp **OK**. Cột Bàn thắng lập tức hiển thị các thanh dữ liệu trực quan sinh động như biểu đồ thanh thu nhỏ!

#### 4. Sắp xếp thứ tự (Sort Order):
* Nhấp chuột trực tiếp vào tiêu đề cột **`Bàn thắng`** trên bảng để sắp xếp giảm dần (**Descending** $\downarrow$).
* Bảng sẽ tự động hiển thị những cặp đấu có nhiều bàn thắng nhất lên đầu (ví dụ: *Celtic vs Hibernian: 19 bàn*, *Fenerbahce vs Istanbulspor: 19 bàn*, *Bayern Munich vs Mainz: 18 bàn*...).

#### 5. Định dạng hiển thị chuẩn mực:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Bảng Danh mục Cặp đấu Đối đầu Kinh điển`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#0F172A`, màu nền tiêu đề `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#1E293B`, xen kẽ màu dòng (Alternate rows) nhạt `#F8FAFC`.
* **Totals:** Tắt **Totals: Off** (do đây là bảng xếp hạng các cặp đấu đối đầu, không cần dòng tổng cộng ở đáy).
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ CỦA TABLE CẶP ĐẤU ĐỐI ĐẦU:**
> * **Sạch sẽ 100% dữ liệu:** Triệt tiêu hoàn toàn nhược điểm của ma trận 2 chiều (vốn sinh ra hàng nghìn ô NULL do các đội khác giải không đá với nhau). Bảng Table chỉ hiển thị những cặp đấu đã thực sự diễn ra trong lịch sử kho dữ liệu (`NON EMPTY`).
> * **Linh hoạt đa tầng:** Khi không bấm bộ lọc, bảng đóng vai trò là bảng xếp hạng Top các trận cầu mưa bàn thắng toàn châu Âu. Khi người dùng bấm Slicer chọn 1 CLB (như *Real Madrid*), bảng tự động thu gọn lại thành danh sách toàn bộ các đối thủ của riêng Real Madrid kèm thanh Data Bars so sánh hỏa lực.

---

## 4. Kết quả Đối soát và Lập luận Chuyên môn

### 4.1. Khả năng tương tác chéo (Cross-filtering)
* **Khai thác theo CLB Chủ quản:**
  * Khi nhấp chọn `Real Madrid` trên Slicer: Toàn bộ bảng Ô 1 lập tức hiển thị Top 10 đối thủ bị Real Madrid chọc thủng lưới nhiều nhất: `UD Almería` (12 bàn), `CA Osasuna` (11 bàn), `Cádiz CF` (10 bàn), `Villarreal` (10 bàn), `FC Barcelona` (8 bàn).
  * Khi chuyển sang chọn `Manchester City`: Ô 1 chuyển ngay sang danh sách đối thủ của Man City: `RB Leipzig` (14 bàn), `Bournemouth` (13 bàn), `Fulham` (13 bàn), `Manchester United` (13 bàn).
  * Bảng danh mục cặp đấu ở Ô 4 cho phép người xem nhìn bao quát danh sách các cặp đấu nhiều bàn thắng nhất, hoặc lọc riêng theo từng CLB để xem trọn vẹn thành tích đối đầu mà không bị gián đoạn bởi các ô trống.

### 4.2. Lập luận phân tích nghiệp vụ thể thao (Sport Intelligence Insights)
1. **Giá trị của Chiều đa vai trò (Role-Playing Dimension) trong OLAP:**
   * Việc một bảng sự kiện (`FACT_Player_Match_Perf`) liên kết đồng thời tới 2 khóa ngoại của cùng một chiều CLB (`Club_SK` và `Opponent_Club_SK`) cho phép thực hiện các phép chiếu ma trận chéo (Cross-tabulation). Đây là điểm sáng kiến trúc OLAP nâng cao, giải quyết trọn vẹn bài toán quan hệ song phương giữa hai thực thể cùng loại mà mô hình quan hệ thông thường xử lý rất phức tạp.
2. **Quy luật "Kỵ rơ" trong Thể thao đỉnh cao:**
   * Thông qua ma trận khắc chế ở Ô 2, người xem nhận thấy rõ có những đối thủ tuy đứng thứ hạng thấp hơn trên bảng tổng sắp nhưng lại nằm ở Góc II (Ít bàn thắng - Nhiều thẻ vàng) của CLB lớn. Điều này phản ánh tính chất chiến thuật "khắc tinh" đặc thù trong bóng đá, nơi các đội bóng chơi rắn và chủ động phá lối chơi của đối thủ mạnh.
3. **Cường độ Cạnh tranh của các Trận Derby (Derby Match Intensity):**
   * Các cuộc đối đầu truyền kiếp (như El Clásico hay Derby Manchester) luôn nằm ở Góc I (Góc có cả số bàn thắng lẫn số thẻ phạt cao nhất). Cường độ thi đấu và sự căng thẳng tâm lý đẩy tỷ lệ thẻ phạt trong các trận đấu này cao hơn **`45%`** so với các vòng đấu thông thường.
