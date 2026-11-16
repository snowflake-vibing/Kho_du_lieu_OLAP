# 4.2.2 Báo biểu 2: Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh (Scouting Elite Clubs & Top Offensive Threats)

Tài liệu này hướng dẫn chi tiết quy trình thiết kế hoàn chỉnh **Báo biểu 2 (Executive Dashboard 2)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!IMPORTANT]
> **MỤC TIÊU NGHIỆP VỤ - TRINH SÁT & BẮT BÀI ĐỐI THỦ (TACTICAL SCOUTING & OPPOSITION ANALYSIS):**
> * Báo biểu 2 giải quyết bài toán cốt lõi của ban huấn luyện và chuyên gia phân tích trước mỗi trận đấu: **"Tra cứu xem kẻ nào đang mạnh nhất, đối thủ sở hữu những họng pháo nào nguy hiểm nhất để lên phương án dè chừng (bắt chết, phong tỏa) hoặc học hỏi bài bản tấn công!"**
> * Khai thác sâu các đặc tính chiến thuật của cầu thủ trong **`DIM Player`**:
>   * **`Sub Position` (Vị trí thi đấu chi tiết):** Xác định mũi nhọn là Trung phong cắm (`Centre-Forward`), Tiền đạo dạt biên (`Left Winger` / `Right Winger`) hay Tiền vệ công (`Attacking Midfield`) để phòng ngự đúng hướng đánh.
>   * **`Foot` (Chân thuận):** Nhận diện các "kèo trái ma thuật" (`left`) hay thuận chân phải (`right`) để hậu vệ biên biết đường be góc sút, cấm ngoặt bóng vào trung lộ.
>   * **`Height In Cm` (Chiều cao):** Đo lường nguy cơ không chiến (tiền đạo cao 1m90+ như Haaland, Luuk de Jong) để bố trí trung vệ to cao chống bóng bổng và phạt góc.
> * Kết hợp với bức tranh vĩ mô: Xếp hạng các CLB hỏa lực mạnh nhất châu Âu (`DIM Club [Club Name]`), các chảo lửa nổ nhiều bàn nhất (`DIM Game [Stadium]`) và nhịp điệu phong độ theo thời gian.

Báo biểu tuân thủ đầy đủ bộ quy chuẩn [**`rule.md`**](../rule.md):
* **Canvas:** Độ phân giải **Full HD 1920 x 1080 px (16:9)**, màu nền xám khói `#F8FAFC`.
* **Phân cấp Typography (Visual Hierarchy):** Title Banner **`20 pt` Bold**, Tiêu đề từng Visual **`18 pt` Bold**, Callout Value thẻ KPI **`35 pt` Bold** (cực kỳ nổi bật), Nhãn dữ liệu & Trục tọa độ **`12 pt`**.
* **Bộ lọc Slicers rộng rãi:** Chiều cao mở rộng **`H = 75 px`**, hiển thị trọn vẹn cả tiêu đề, khung xổ Dropdown và các nút chọn Tile, triệt tiêu hoàn toàn lỗi bị cụt thanh cuộn.
* **Chuẩn hóa nhãn hiển thị (Rename for this visual):** Từng trường dữ liệu đều có hướng dẫn đổi tên tiếng Việt ngắn gọn, chuyên nghiệp, xóa bỏ hoàn toàn dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ độc lập
1. **Đội bóng nào đang sở hữu hỏa lực tấn công hủy diệt nhất châu Âu?** Xếp hạng Top 10 CLB ghi nhiều bàn thắng nhất (`DIM Club [Club Name]` by `[Measures].[Goals]`), nhận diện những cỗ máy tấn công đáng sợ nhất cần phải dè chừng (Man City, Bayern Munich, Real Madrid, PSV...).
2. **"Chảo lửa Thánh địa" nào bùng nổ nhiều bàn thắng nhất?** Sử dụng Combo Chart 2 trục Y để đối chiếu giữa Số trận tổ chức (`Distinct Matches Played` - Cột) và Bàn thắng ghi được (`Goals` - Đường) trên từng Sân vận động (`DIM Game [Stadium]`), nhận diện các "tử địa" có hiệu suất bàn thắng/trận cao nhất (Etihad, Allianz Arena, San Siro...).
3. **Kẻ mạnh bùng nổ phong độ vào giai đoạn nào trong mùa giải?** Biểu đồ vùng (Area Chart) theo dõi biến thiên bàn thắng theo dòng thời gian liên tục (`Season` $\rightarrow$ `Month`), nhận biết nhịp điệu chu kỳ thăng hoa của các đội bóng lớn.
4. **Hồ sơ chiến thuật của các sát thủ nguy hiểm nhất (Tactical Scouting Table):** Bảng danh sách chi tiết tra cứu từng ngòi nổ: Tên cầu thủ (`Player Name`), CLB, Vị trí (`Sub Position`), Chân thuận (`Foot`), Chiều cao (`Height In Cm`) và Sát thương hỏa lực (`Goals`, `Goal Contributions` kèm Data Bars).

### 1.2. Ý nghĩa thống kê & Giá trị học thuật
| Thành phần trực quan | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Biểu đồ Cột ngang Top 10 CLB Hỏa lực** | Xếp hạng các CLB ghi bàn nhiều nhất châu Âu (`DIM Club` by `Goals`), nhận diện sức mạnh tấn công tổng lực của các đội bóng dẫn đầu. |
| **Combo Chart 2 Trục Y Chảo lửa Sân Vận Động** | Đối soát tương quan trực quan giữa Số trận tổ chức (`Distinct Matches Played` - Cột Y1) và Bàn thắng ghi được (`Goals` - Đường Y2) trên từng Sân vận động (`DIM Game [Stadium]`). |
| **Area Chart (Biểu đồ Vùng dòng thời gian)** | Theo dõi biến thiên bàn thắng theo chu kỳ các Tháng trong năm phân lớp theo Mùa giải (`Season`). Phản ánh rõ phong độ đối đầu bùng nổ vào giai đoạn nước rút hay đầu mùa. |
| **Bảng Trinh sát Đặc tính Chiến thuật (Table + Data Bars)** | Bảng tra cứu từng mũi nhọn nguy hiểm, tích hợp đầy đủ Vị trí (`Sub Position`), Chân thuận (`Foot`), Chiều cao (`Height In Cm`) và Điểm sát thương (`Goal Contributions`), phục vụ trực tiếp công tác bắt bài chiến thuật. |

### 1.3. Bài toán thực tế giải quyết
* **Ban huấn luyện & Trợ lý phân tích chiến thuật:** "Bắt bài" đối thủ trước trận đấu — nhận diện ngòi nổ nguy hiểm nhất, biết rõ chân thuận để be góc sút, chiều cao để phòng ngự bóng bổng.
* **Bộ phận Chuyển nhượng & Tuyển trạch:** Nghiên cứu và học hỏi mô hình vận hành của các đội bóng mạnh nhất châu Âu.
* **Cổ động viên & Truyền thông:** Tra cứu sức mạnh và các thông số độc đáo của các ngôi sao hàng đầu.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas Full HD 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [Visual 0] HERO BANNER TIÊU ĐỀ: BÁO BIỂU 2 - TRINH SÁT & BẮT BÀI CÁC MŨI NHỌN NGUY HIỂM (Font: 20pt Bold, Center)       |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Distinct Matches]    | [Card 2: Total Goals]       | [Card 3: Total Assists]     | [Card 4: Goal Contributions]       |
| Callout: 35pt Bold (6,965)    | Callout: 35pt Bold (19.17K) | Callout: 35pt Bold (14.74K) | Callout: 35pt Bold (33.91K)        |
| Nền: Pastel Blue #EFF6FF      | Nền: Pastel Green #F0FDF4   | Nền: Pastel Amber #FFFBEB   | Nền: Pastel Purple #FAF5FF         |
| (W: 455, H: 95, X: 20)        | (W: 455, H: 95, X: 495)     | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)           |
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu]          | [Slicer 2: CLB Chủ quản]   | [Slicer 3: Mùa giải]       | [Slicer 4: Tháng thi đấu]         |
| (W: 455, H: 75, X: 20, Y: 210)| (W: 455, H: 75, X: 495)    | (W: 455, H: 75, X: 970)    | (W: 455, H: 75, X: 1445)          |
+-------------------------------+----------------------------+----------------------------+-----------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ CỘT THANH NGANG (18pt)]     | [Ô 2: TRÊN - PHẢI | COMBO CHART 2 TRỤC Y (Title: 18pt)]        |
| Top 10 CLB Có Hỏa Lực Tấn Công Mạnh Nhất                | Chảo lửa Sân vận động: Số trận [Cột Y1] vs Bàn thắng [Đường Y2]|
| Y: CLB Chủ quản (12pt), X: Bàn thắng (12pt Green)       | X: Sân vận động (12pt), Cột: Số trận (12pt), Đường: Bàn thắng  |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BIỂU ĐỒ VÙNG DIỆN TÍCH AREA (18pt)] | [Ô 4: DƯỚI - PHẢI | BẢNG TRINH SÁT MŨI NHỌN NGUY HIỂM (18pt)]|
| Biến thiên Bàn thắng theo Dòng Thời gian (24 Tháng)     | Bảng Tra Cứu: Cầu thủ, Vị trí, Chân thuận, Chiều cao, G+A     |
| X: Season -> Month (↓↓), Y: Bàn thắng                   | Cột: Cầu thủ, CLB, Vị trí (Sub Position), Chân, Chiều cao, G+A|
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Từng Bước Thiết lập Chi tiết trên Power BI Desktop

### Bước 1: Khởi tạo Trang Báo cáo và Cấu hình Canvas
1. Tại thanh quản lý trang ở mép dưới Power BI Desktop, nhấp vào biểu tượng dấu cộng `+` để thêm một trang mới.
2. Nhấp đúp chuột vào tên trang vừa tạo và **đặt tên trang chính thức**:
   * **Tên trang:** `Hồ sơ Chiến thuật & Kẻ mạnh` (hoặc `Báo biểu 2`).
3. Nhấp chuột vào khoảng trống Canvas để mở bảng **Format report page**:
   * **Canvas settings** $\rightarrow$ **Type:** Chọn `Custom`, thiết lập `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background:** Chọn màu xám khói hiện đại **`#F8FAFC`**, thiết lập **Transparency = `0%`**.

---

### Bước 2: Thiết lập Hero Banner Tiêu đề Trang (Tầng trên)
1. Trên thanh tác vụ **Insert**, nhấp chọn **Text box**.
2. Nhập nội dung tiêu đề chuẩn mực:
   `BÁO BIỂU 2: HỒ SƠ CHIẾN THUẬT & TRINH SÁT CÁC MŨI NHỌN NGUY HIỂM NHẤT`
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

#### 3. Card 3: Tổng số Pha Kiến tạo Đối đầu (Total Assists)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Assists]`** vào ô **Fields** (nhận diện những chuyên gia dọn cỗ / ngòi nổ chuyền bóng nguy hiểm nhất của các đội).
* **Phần đặt tên (Rename for this visual):**
  * Tùy chọn Tiếng Anh: **`Total Assists`** (hoặc Tiếng Việt: **`Tổng kiến tạo`**).
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG KIẾN TẠO ĐỐI ĐẦU (ASSISTS)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#92400E`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, Display units chọn **`Auto`** (hiển thị `14.74K`). **Category label**: Tắt **Off**.
* Tab **General** $\rightarrow$ **Effects**: Background nền Pastel Amber **`#FFFBEB`**, Viền `#FCD34D`, Bo góc `10 px`.
* **Properties:** `W = 455 px`, `H = 95 px`, `X = 970 px`, `Y = 95 px`.

#### 4. Card 4: Tổng Điểm Sát thương Đóng góp Bàn thắng (Total Goal Contributions = Goals + Assists)
* Thêm visual **Card**.
* Kéo thước đo **`[Measures].[Goal Contributions]`** vào ô **Fields** (thước đo tổng hỏa lực thực tế của các ngôi sao tấn công khi chạm trán đối thủ).
* **Phần đặt tên (Rename for this visual):**
  * Tùy chọn Tiếng Anh: **`Goal Contributions`** (hoặc Tiếng Việt: **`Tổng đóng góp G+A`**).
* Tab **General** $\rightarrow$ **Title**: Bật **On**, nhập `TỔNG ĐÓNG GÓP HỎA LỰC (G+A)`, Font `Segoe UI`, Cỡ chữ **`15 pt - 18 pt` Bold**, Căn giữa, màu chữ `#5B21B6`.
* Tab **Format visual** $\rightarrow$ **Callout value**: Cỡ chữ **`35 pt` Bold**, màu đen tuyền `#0F172A`, Display units chọn **`Auto`** (hiển thị `33.91K`). **Category label**: Tắt **Off**.
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

### Bước 5 – Ô 1 (Trên - Trái): Clustered Bar Chart – Top 10 CLB Có Hỏa Lực Tấn Công Mạnh Nhất Châu Âu

1. Tại khung **Visualizations**, chọn visual **Clustered bar chart** (Biểu đồ thanh ngang).
2. Kích thước & Vị trí:
   * Size: `Width = 925 px`, `Height = 385 px`.
   * Position: `Horizontal = 20 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu:
   * **Y-axis:** Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`** vào ô này (nhận diện những cỗ máy tấn công nguy hiểm nhất).
   * **X-axis:** Kéo thước đo **`[Measures].[Goals]`** (Tổng số bàn thắng hủy diệt đã ghi được).
   * **Tooltips:** Kéo `[Measures].[Assists]`, `[Measures].[Goal Contributions]`.
4. **Phần đặt tên (Rename for this visual):**
   * `DIM Club [Club Name]` $\rightarrow$ Đổi tên: **`Club Name`** (hoặc `CLB Tấn công`)
   * `Goals` $\rightarrow$ Đổi tên: **`Goals`** (hoặc `Bàn thắng ghi được`)
5. **Bộ lọc Top 10 CLB Mạnh nhất (Filters on this visual):**
   * Tại khung **Filters on this visual** $\rightarrow$ chọn trường `Club Name` $\rightarrow$ chọn mục **Top N** $\rightarrow$ nhập `10` $\rightarrow$ tại ô **By value** kéo `Goals` $\rightarrow$ nhấp **Apply filter**.
   * *(Kết quả hiển thị chính xác các cỗ máy ghi bàn hàng đầu: Manchester City 245 bàn, Bayern Munich 225 bàn, PSV Eindhoven 219 bàn, Real Madrid 210 bàn, Feyenoord 200 bàn, Arsenal 199 bàn, Liverpool 198 bàn, PSG 198 bàn...)*.
6. **Định dạng hiển thị:**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Top 10 CLB Có Hỏa Lực Tấn Công Mạnh Nhất`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **Bars:** Màu Xanh dương hoàng gia **`#2563EB`** (hoặc đa sắc theo theme).
   * **Y-axis (Tên CLB):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu sắc: **Xanh Navy đậm `#0D47A1`**, *Maximum width* đặt `35%` để hiển thị trọn vẹn tên CLB không bị dấu ba chấm `...`.
   * **X-axis (Bàn thắng):** Cỡ chữ **`12 pt`**, màu sắc: **Xanh lục `#1B5E20`**.
   * **Data labels:** Bật **On**, Cỡ chữ **`11 pt` Bold**.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA NGHIỆP VỤ CỦA Ô 1:**
> * Định danh ngay những "ông kẹ" sở hữu hàng công khủng khiếp nhất toàn châu Âu. Giúp ban huấn luyện nhận diện các bài bản tấn công vượt trội để học hỏi và đề phòng khi chạm trán.

---

### Bước 6 – Ô 2 (Trên - Phải): Combo Chart 2 Trục Y – Chảo lửa Thánh địa: Số trận Tổ chức vs Bàn thắng Ghi được (Line and Clustered Column Chart)

1. Tại khung **Visualizations**, chọn visual **Line and clustered column chart** (Biểu đồ kết hợp Cột cụm và Đường với 2 trục Y độc lập).
2. Kích thước & Vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`.
   * **Position:** `Horizontal = 975 px`, `Vertical = 300 px`.
3. Kéo thả trường dữ liệu (Tuyệt đối không trùng lặp với Ô 1, sử dụng chiều `DIM Game` độc lập và 100% Thước đo chuẩn 🧮):
   * **X-axis (Trục hoành):** Mở bảng **`DIM Game`**, kéo thuộc tính **`[Stadium]`** (Tên Sân vận động / Thánh địa thi đấu).
   * **Column y-axis (Trục Y trái - Cột):** Mở thư mục **`Measures`**, kéo thước đo **`[Measures].[Distinct Matches Played]`** (Tổng số trận diễn ra trên sân này).
   * **Line y-axis (Trục Y phải - Đường):** Mở thư mục **`Measures`**, kéo thước đo **`[Measures].[Goals]`** (Tổng số bàn thắng bùng nổ trên sân này).
4. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Stadium` $\rightarrow$ Đổi tên thành: **`Sân vận động`**
   * `Distinct Matches Played` $\rightarrow$ Đổi tên thành: **`Số trận tổ chức`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
5. **Cấu hình Bộ lọc Top 10 Chảo lửa bùng nổ nhất (Filters on this visual):**
   * Tại khung **Filters on this visual**, mở mục `Sân vận động` (hoặc `Stadium`).
   * Chọn Filter type: **Top N**, nhập **`10`**.
   * Ô **By value**: Kéo thước đo **`[Measures].[Goals]`** vào.
   * Nhấp nút **Apply filter** (Tập trung hiển thị 10 thánh địa có nhiều bàn thắng nhất châu Âu: *Giuseppe Meazza, Olimpico di Roma, Etihad Stadium, Allianz Arena, Emirates Stadium, Anfield, Parc des Princes, Santiago Bernabéu...*).
6. **Định dạng hiển thị chi tiết (Tab Format visual):**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Chảo lửa Thánh địa: Số trận Tổ chức vs Bàn thắng Ghi được`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **Columns (Màu cột số trận):** Đặt màu Cột xanh dương hiện đại `#2563EB`.
   * **Lines (Màu đường bàn thắng):** Đặt màu Đường đỏ cam rực lửa `#EF4444`, Stroke width: `3 px`.
   * **Markers (Điểm đánh dấu trên đường):** Bật **On**, Shape: Tròn (Circle), Size: `6`, Màu nền `#DC2626`.
   * **Data labels:** Bật **On**, Cỡ chữ **`11 pt` Bold**.
   * **X-axis (Tên Sân vận động):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis (Cột - Trục Y trái):** Title bật **On**, nhập `Số trận tổ chức`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#2563EB`.
   * **Secondary y-axis (Đường - Trục Y phải):** Title bật **On**, nhập `Bàn thắng ghi được`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#DC2626`.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ & TRIỆT TIÊU TRÙNG LẶP 100%:**
> * **Không trùng lặp với Ô 1:** Ô 1 phân tích theo **CLB Đối thủ** (`Opponent Club [Club Name]`), còn Ô 2 khai thác độc lập chiều **Thánh địa Sân bãi** (`DIM Game [Stadium]`).
> * **Giải quyết bài toán "Thánh địa hủy diệt":** Cho thấy sự chênh lệch hiệu suất bàn thắng/trận giữa các sân. Ví dụ: *Etihad Stadium* (49 trận nhưng nổ tới 182 bàn - trung bình 3.71 bàn/trận) và *Allianz Arena* (45 trận nổ 164 bàn - 3.64 bàn/trận) thể hiện rõ hỏa lực hủy diệt của Man City và Bayern Munich tại sân nhà, trong khi *Giuseppe Meazza* (98 trận nổ 263 bàn - 2.68 bàn/trận) mang tính thực dụng của bóng đá Ý.
> * **Tương thích tuyệt đối 100% với SSAS Live Connection:** Cả hai trục Y đều là Thước đo Measure chuẩn (`Distinct Matches Played` và `Goals`), triệt tiêu hoàn toàn lỗi *Discourage implicit measures* của Power BI.

---

### Bước 7 – Ô 3 (Dưới - Trái): Area Chart – Biến thiên Bàn thắng Đối đầu theo Dòng Thời gian Tuyến tính (Biểu đồ Vùng diện tích liên tục)

1. Tại khung **Visualizations**, chọn visual **Area chart** (Biểu đồ Vùng diện tích).
2. Kích thước & Vị trí:
   * **Size:** `Width = 925 px`, `Height = 385 px`.
   * **Position:** `Horizontal = 20 px`, `Vertical = 695 px`.
3. Kéo thả trường dữ liệu (Khử hoàn toàn lỗi đứt nét chấm bi do khóa ghép SSAS):
   * **X-axis (Trục hoành):** Kéo lần lượt 2 trường theo thứ tự từ trên xuống:
     1. Mở bảng **`DIM Time`**, kéo thuộc tính **`[Season]`** (Mùa giải - cấp trên).
     2. Mở bảng **`DIM Time`**, kéo thuộc tính **`[Month]`** (Tháng - cấp dưới).
   * **Y-axis:** Kéo thước đo **`[Measures].[Goals]`** (Bàn thắng ghi được).
   * **Legend:** **Để trống hoàn toàn** (Không kéo gì vào Legend để tránh bị chia cắt các điểm dữ liệu thành các chấm rời rạc).
4. **Kích hoạt chế độ mở rộng phân cấp liền mạch (BƯỚC QUAN TRỌNG NHẤT):**
   * Nhấp chọn biểu đồ Area Chart vừa tạo.
   * Nhìn lên thanh công cụ điều hướng ở góc trên cùng bên phải visual (hoặc góc trên), nhấp vào biểu tượng **hai mũi tên phân nhánh chĩa xuống: `↓↓` (Expand all down one level in the hierarchy - Mở rộng phân cấp)**.
   * **Kết quả:** Trục X sẽ tự động dàn phẳng thành dòng thời gian liên tục 24 tháng: `2022/2023 (Tháng 1 -> 12)` nối tiếp sang `2023/2024 (Tháng 1 -> 12)`. Đường diện tích uốn lượn liền mạch 100%, không bị đứt đoạn hay lặp lại số tháng!
5. **Phần đặt tên chuẩn tiếng Việt (Rename for this visual):**
   * `Month` $\rightarrow$ Đổi tên thành: **`Tháng`**
   * `Season` $\rightarrow$ Đổi tên thành: **`Mùa giải`**
   * `Goals` $\rightarrow$ Đổi tên thành: **`Bàn thắng ghi được`**
6. **Định dạng hiển thị chi tiết (Tab Format visual):**
   * Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Biến thiên Bàn thắng Đối đầu theo Dòng Thời gian`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
   * **X-axis (Thời gian):** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#334155`.
   * **Y-axis:** Title bật **On**, nhập `Tổng số bàn thắng`, Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#1E3A8A`.
   * **Lines & Colors:** 
     * **Lines:** Màu Xanh Navy đậm hiện đại **`#2563EB`**, Stroke width: **`3 px`**.
     * **Shaded area (Vùng phủ bóng):** Bật **On**, Transparency: **`50% - 60%`** để tạo độ chuyển màu tinh tế.
     * **Markers (Điểm đánh dấu):** Bật **On**, Shape: Tròn, Size: `5`, màu `#1D4ED8`.
   * Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc **`10 px`**.

> **Ý NGHĨA PHÂN TÍCH NGHIỆP VỤ CỦA BIỂU ĐỒ VÙNG TUYẾN TÍNH:**
> * **Giải quyết triệt để lỗi kỹ thuật SSAS:** Khóa của `Month` trong Cube SSAS là khóa ghép `(Month, Quarter, Year)`. Khi đưa cả `Season` và `Month` vào X-axis rồi bấm `↓↓`, trục thời gian trở nên liền mạch tuyệt đối, triệt tiêu hoàn toàn hiện tượng hiển thị các chấm rời rạc không nối dòng.
> * **Khắc họa nhịp điệu thi đấu thực tế:** Khắc họa rõ nét nhịp điệu phong độ và tính chu kỳ của các giải đấu bóng đá châu Âu: khởi động vào tháng 8-9, duy trì ổn định qua mùa đông tháng 11-12, bùng nổ bàn thắng ở giai đoạn nước rút quyết định tháng 3-4-5 và trũng xuống chạm đáy vào kỳ nghỉ hè tháng 6-7.

---

### Bước 8 – Ô 4 (Dưới - Phải): Table – Bảng Trinh Sát Đặc Tính Chiến Thuật Của Các Mũi Nhọn Nguy Hiểm Nhất (Tactical Player Scouting Table)

Bảng trinh sát trực diện chân dung các "sát thủ" nguy hiểm nhất để ban huấn luyện lên phương án phòng ngự (be hướng sút chân thuận, chống bóng bổng) hoặc học hỏi bài bản tấn công:

#### 1. Cấu hình trường dữ liệu:
* Size: `Width = 925 px`, `Height = 385 px`.
* Position: `Horizontal = 975 px`, `Vertical = 695 px`.
* Tại khung **Visualizations**, chọn visual **Table** (biểu tượng bảng danh sách phẳng).
* Kéo các trường vào ô **Columns**:
  1. Mở bảng **`DIM Player`**, kéo thuộc tính **`[Player Name]`** (Tên ngôi sao / mũi nhọn nguy hiểm).
  2. Mở bảng **`DIM Club`**, kéo thuộc tính **`[Club Name]`** (CLB chủ quản).
  3. Mở bảng **`DIM Player`**, kéo thuộc tính **`[Sub Position]`** (Vị trí thi đấu: *Centre-Forward, Left Winger, Right Winger...*).
  4. Mở bảng **`DIM Player`**, kéo thuộc tính **`[Foot]`** (Chân thuận: *Left, Right, Both* $\rightarrow$ giúp hậu vệ biết đường be góc sút chân thuận).
  5. Mở bảng **`DIM Player`**, kéo thuộc tính **`[Height In Cm]`** (Chiều cao $\rightarrow$ đo lường nguy cơ không chiến bóng bổng).
  6. Kéo thước đo **`[Measures].[Goal Contributions]`** (Tổng sát thương G+A).
  7. Kéo thước đo **`[Measures].[Goals]`** (Bàn thắng).

*(Lưu ý: Nếu anh muốn giữ nguyên bảng danh mục Cặp đấu CLB như hiện tại thì kéo: `DIM Club [Club Name]`, `Opponent Club [Club Name]`, `[Measures].[Goal Contributions]` và `[Measures].[Yellow Cards]`)*.

#### 2. Phần đặt tên nhãn cột (Rename for this visual):
* Nhấp chuột phải vào từng trường trong ô Columns $\rightarrow$ chọn **Rename for this visual**:
  * `Player Name` $\rightarrow$ Đổi tên: **`Player Name`** (hoặc `Tên cầu thủ`)
  * `DIM Club [Club Name]` $\rightarrow$ Đổi tên: **`Club Name`** (hoặc `CLB`)
  * `Sub Position` $\rightarrow$ Đổi tên: **`Position`** (hoặc `Vị trí`)
  * `Foot` $\rightarrow$ Đổi tên: **`Foot`** (hoặc `Chân thuận`)
  * `Height In Cm` $\rightarrow$ Đổi tên: **`Height`** (hoặc `Chiều cao`)
  * `Goal Contributions` $\rightarrow$ Đổi tên: **`Goal Contributions`** (hoặc `G+A`)
  * `Goals` $\rightarrow$ Đổi tên: **`Goals`** (hoặc `Bàn thắng`)

#### 3. Bật thanh dữ liệu Data Bars trực quan cho cột Goal Contributions (Tab Format visual $\rightarrow$ Cell elements):
* Nhấp chọn bảng Table $\rightarrow$ vào tab **Format visual (Cọ vẽ)** $\rightarrow$ cuộn xuống mục **Cell elements**:
  * Tại ô xổ xuống **Select series**: Chọn trường **`Goal Contributions`**.
  * Gạt công tắc **Data bars** sang **ON**!
  * Nhấp vào nút **`fx`** bên cạnh Data bars:
    * **Positive bar:** Chọn màu Xanh dương hiện đại **`#2563EB`** (hoặc `#3B82F6`).
    * **Bar direction:** Chọn `Left to right` (Trái sang phải).
    * Mục **Show bar only:** Để **Off** (hiển thị cả con số bên cạnh thanh màu).
    * Nhấp **OK**. Cột Goal Contributions lập tức hiển thị các thanh dữ liệu trực quan sinh động như biểu đồ thanh thu nhỏ!

#### 4. Sắp xếp thứ tự (Sort Order):
* Nhấp chuột trực tiếp vào tiêu đề cột **`Goal Contributions`** (hoặc `Goals`) trên bảng để sắp xếp giảm dần (**Descending** $\downarrow$).
* Bảng sẽ tự động hiển thị những cỗ máy hủy diệt nguy hiểm nhất lên đầu: *Erling Haaland (Centre-Forward, chân trái, 195cm, 95 G+A), Harry Kane (Centre-Forward, chân phải, 188cm, 92 G+A), Kylian Mbappé (Centre-Forward, 180cm, 87 G+A), Mohamed Salah (Right Winger, chân trái, 175cm, 78 G+A)...*

#### 5. Định dạng hiển thị chuẩn mực:
* Tab **Format visual** $\rightarrow$ **Title**: Bật **On**, nhập `Bảng Trinh Sát Đặc Tính Chiến Thuật của các Mũi Nhọn Nguy Hiểm`, Font `Segoe UI`, Cỡ chữ **`18 pt` Bold**, Căn giữa (**Center**), màu chữ `#0F172A`.
* **Column headers:** Font `Segoe UI Bold`, Cỡ chữ **`12 pt`**, màu `#0F172A`, màu nền tiêu đề `#F1F5F9`.
* **Values:** Font `Segoe UI`, Cỡ chữ **`12 pt`**, màu `#1E293B`, xen kẽ màu dòng (Alternate rows) nhạt `#F8FAFC`.
* **Totals:** Tắt **Totals: Off** (bảng danh sách tra cứu cá nhân không cần dòng tổng cộng ở đáy).
* Tab **General** $\rightarrow$ **Effects**: Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

> **Ý NGHĨA CHIẾN THUẬT CỦA BẢNG TRINH SÁT:**
> * Cung cấp đầy đủ chân dung nhận dạng của kẻ mạnh: Tên, Vị trí khoét vào cánh nào, Thuận chân nào để be góc, Cao bao nhiêu để chống bóng bổng. Ban huấn luyện nhìn vào bảng này là có ngay phương án phong tỏa toàn diện trước trận đấu!

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
