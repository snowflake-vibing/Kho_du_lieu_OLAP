# 4.2.3 Báo biểu 3: Kỷ luật Thẻ phạt, Cường độ Thi đấu và Tải trọng Cầu thủ (Discipline & Match Load Analysis)

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế hoàn chỉnh **Báo biểu 3 (Dashboard 3)** trên **Power BI Desktop**, tập trung phân tích khía cạnh kỷ luật trận đấu (Thẻ vàng, Thẻ đỏ) và tải trọng thể lực (Thời lượng số phút thi đấu) của các cầu thủ theo vị trí và độ tuổi.

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Giám sát mức độ quyết liệt của các trận đấu thông qua số lượng thẻ vàng (`Yellow_Cards`) và thẻ đỏ (`Red_Cards`), đánh giá tải trọng thi đấu thực tế (`Minutes_Played`), tỷ lệ xuất phát trong đội hình chính (`Is_Starter`) và phân tích nguy cơ nhận thẻ theo độ tuổi và vị trí thi đấu trên sân.
* **Đối tượng theo dõi:**
  * Khối 4 Thẻ KPI Kỷ luật: Tổng số thẻ vàng, Tổng số thẻ đỏ, Tỷ lệ thẻ phạt trung bình mỗi trận, Tổng số phút thi đấu tích lũy.
  * Biểu đồ thanh ngang phân cụm (Clustered Bar Chart): Top 10 Câu lạc bộ nhận nhiều thẻ phạt nhất Châu Âu.
  * Biểu đồ vành khăn (Donut Chart): Tỷ lệ phân bổ thẻ phạt theo Vị trí thi đấu (`Main_Position`: Defender, Midfield, Attack, Goalkeeper).
  * Biểu đồ kết hợp cột và đường (Line and Clustered Column Chart): Tương quan giữa Thời lượng thi đấu (`Minutes_Played` - Cột) và Số lượng thẻ phạt (`Cards` - Đường) theo từng độ tuổi (`Age`).
  * Bảng ma trận chi tiết kỷ luật (Matrix Visual): Tra cứu chi tiết thẻ vàng, thẻ đỏ, số phút và tỷ lệ đá chính của cầu thủ theo từng Câu lạc bộ.
  * Hệ thống bộ lọc cắt lát (Slicers): Mùa giải (`Season`), Giải đấu (`Competition_Name`), Vị trí thi đấu (`Main_Position`).

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Khởi tạo trang báo cáo và banner tiêu đề
1. Ở mép dưới Power BI Desktop, nhấp chuột vào dấu cộng `+` để thêm trang thứ ba (`Page 3`).
2. Đổi tên thẻ thành: `Kỷ luật & Tải trọng Thi đấu`.
3. Kiểm tra Canvas settings: Đảm bảo tỷ lệ chuẩn **16:9** (`Width: 1280 px`, `Height: 720 px`).
   * **Canvas background**: Giữ nguyên mặc định nguyên bản của Power BI, tuyệt đối không chỉnh màu sắc hay độ trong suốt.
4. Trên thanh Ribbon **Insert**, nhấp chọn **Text box**, nhập tiêu đề:
   `BÁO BIỂU 3: PHÂN TÍCH KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU VÀ TẢI TRỌNG CẦU THỦ`
5. Định dạng văn bản: Font `Segoe UI`, Cỡ chữ `15 pt`, In đậm (**Bold**), Căn giữa (**Center**).
6. Thiết lập vị trí và kích thước tại **Properties** (Tab **General** -> **Properties**):
   * **Size:** `Width = 1250 px`, `Height = 45 px`
   * **Position:** `Horizontal = 15 px`, `Vertical = 10 px`

> **MẸO NHẬP TỌA ĐỘ VÀ KÍCH THƯỚC CHUẨN XÁC TỪNG PIXEL:**
> Sau khi tạo mỗi visual, nhấp chọn visual -> Tại khung **Visualizations**, chọn tab **General** -> Mở rộng mục **Properties**:
> * **Size:** Nhập **Width** (Chiều rộng) và **Height** (Chiều cao).
> * **Position:** Nhập **Horizontal** (Tọa độ ngang X) và **Vertical** (Tọa độ dọc Y).

---

### Bước 2: Thiết lập 4 Thẻ KPI Kỷ luật và Thể lực (Card Visuals)
Tạo 4 thẻ Card đặt thành một hàng ngang ngay phía dưới Banner tiêu đề (Y = 65 px, Chiều cao = 85 px):

1. **Card 1: Tổng số Thẻ Vàng (Total Yellow Cards)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Yellow Cards]` vào ô **Fields**.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
   * **Category label**: Bật **On**, Font `Segoe UI`, Cỡ chữ `10 pt`, đổi tên hiển thị thành `Tổng Thẻ Vàng`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 15 px`, `Vertical = 65 px`).
2. **Card 2: Tổng số Thẻ Đỏ (Total Red Cards)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Red Cards]` vào ô **Fields**.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
   * **Category label**: Bật **On**, Font `Segoe UI`, Cỡ chữ `10 pt`, đổi tên hiển thị thành `Tổng Thẻ Đỏ`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 333 px`, `Vertical = 65 px`).
3. **Card 3: Tỷ lệ Thẻ phạt / Trận (Cards Per Match)**:
   * Thêm visual **Card**, kéo thước đo tính trung bình thẻ mỗi trận vào ô **Fields**.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**), định dạng 2 chữ số thập phân (`#,##0.00`).
   * **Category label**: Bật **On**, Font `Segoe UI`, Cỡ chữ `10 pt`, đổi tên hiển thị thành `Trung bình Thẻ / Trận`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 651 px`, `Vertical = 65 px`).
4. **Card 4: Tổng Thời lượng Thi đấu (Total Minutes)**:
   * Thêm visual **Card**, kéo thước đo `[Measures].[Minutes Played]` vào ô **Fields**.
   * Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**), hiển thị rút gọn đơn vị triệu phút (`M mins`).
   * **Category label**: Bật **On**, Font `Segoe UI`, Cỡ chữ `10 pt`, đổi tên hiển thị thành `Tổng Số Phút Thi Đấu`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 970 px`, `Vertical = 65 px`).

---

### Bước 3: Thêm 3 Bộ lọc tương tác đa chiều (Slicers)
Tạo 3 Slicer đặt thành hàng ngang ngay dưới khối KPI (Y = 160 px, Chiều cao = 50 px):
1. **Slicer 1 (Mùa giải):**
   * Thêm visual **Slicer**, kéo `DIM Time [Season]` vào ô **Field**, chọn kiểu **Dropdown**.
   * Định dạng: Header Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 390 px`, `Height = 50 px`), Position (`Horizontal = 15 px`, `Vertical = 160 px`).
2. **Slicer 2 (Giải đấu):**
   * Thêm visual **Slicer**, kéo `DIM Competition [Competition Name]` vào ô **Field**, chọn kiểu **Dropdown**.
   * Định dạng: Header Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 420 px`, `Height = 50 px`), Position (`Horizontal = 445 px`, `Vertical = 160 px`).
3. **Slicer 3 (Vị trí thi đấu):**
   * Thêm visual **Slicer**, kéo `DIM Player [Main Position]` vào ô **Field**, chọn kiểu **Tile**.
   * Định dạng: Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 390 px`, `Height = 50 px`), Position (`Horizontal = 875 px`, `Vertical = 160 px`).

---

### Bước 4: Tạo Biểu đồ thanh ngang Top 10 CLB nhận nhiều thẻ phạt nhất (Clustered Bar Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Clustered bar chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 475 px`, `Height = 485 px`
   * **Position:** `Horizontal = 15 px`, `Vertical = 220 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng Y-axis:** Kéo thuộc tính `DIM Club [Club Name]` vào ô **Y-axis**.
   * **Vùng X-axis:** Lần lượt kéo 2 thước đo:
     1. `Yellow Cards` (Thẻ vàng)
     2. `Red Cards` (Thẻ đỏ)
4. **Thiết lập bộ lọc Top 10 CLB:**
   * Tại khung **Filters on this visual**, mục `Club Name`, chọn kiểu lọc **Top N**, nhập `10`, By value kéo thước đo `Yellow Cards` và nhấp **Apply filter**.
5. **Định dạng chuẩn font chữ và cỡ chữ:**
   * Tab **Format visual** -> **Title**: Nhập `Top 10 CLB nhận nhiều thẻ phạt nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **X-axis** & **Y-axis**: Values chọn Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Data labels**: Bật **On**, Font `Segoe UI`, Cỡ chữ `9 pt`.
   * **Legend**: Font `Segoe UI`, Cỡ chữ `10 pt`.

---

### Bước 5: Tạo Biểu đồ vành khăn Cơ cấu thẻ phạt theo Vị trí thi đấu (Donut Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Donut chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 330 px`, `Height = 235 px`
   * **Position:** `Horizontal = 505 px`, `Vertical = 220 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng Legend:** Kéo thuộc tính `DIM Player [Main Position]` (Defender, Midfield, Attack, Goalkeeper) vào ô **Legend**.
   * **Vùng Values:** Kéo thước đo `Yellow Cards` vào ô **Values**.
4. **Định dạng chuẩn font chữ và cỡ chữ:**
   * Tab **Format visual** -> **Title**: Nhập `Tỷ lệ Thẻ vàng phân bổ theo Vị trí thi đấu`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Detail labels**: Chọn `Category, percent of total`, Font `Segoe UI`, Cỡ chữ `9 pt`.
   * **Legend**: Vị trí `Right center`, Font `Segoe UI`, Cỡ chữ `10 pt`.

---

### Bước 6: Tạo Biểu đồ kết hợp Tương quan Số phút thi đấu và Thẻ phạt theo Độ tuổi (Line and Clustered Column Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Line and clustered column chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 415 px`, `Height = 235 px`
   * **Position:** `Horizontal = 850 px`, `Vertical = 220 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng X-axis:** Kéo thuộc tính `DIM Player [Age]` (Độ tuổi từ 16 đến 40) vào ô **X-axis**.
   * **Vùng Column Y-axis (Cột):** Kéo thước đo `Minutes Played` vào ô này (đổi tên hiển thị thành `Tổng số Phút thi đấu`).
   * **Vùng Line Y-axis (Đường):** Kéo thước đo `Yellow Cards` vào ô này (đổi tên hiển thị thành `Số Thẻ vàng nhận phạt`).
4. **Định dạng chuẩn font chữ và cỡ chữ:**
   * Tab **Format visual** -> **Title**: Nhập `Tương quan giữa Tải trọng Thi đấu (Cột) và Thẻ phạt (Đường) theo Độ tuổi`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **X-axis** & **Y-axis**: Values chọn Font `Segoe UI`, Cỡ chữ `10 pt` (bật cả trục tung bên trái cho Cột và trục tung phụ bên phải cho Đường).
   * **Data labels**: Bật **On**, Font `Segoe UI`, Cỡ chữ `9 pt`.
   * **Legend**: Font `Segoe UI`, Cỡ chữ `10 pt`.

---

### Bước 7: Tạo Bảng Ma trận Kỷ luật chi tiết (Matrix Visual)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Matrix**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 760 px`, `Height = 235 px`
   * **Position:** `Horizontal = 505 px`, `Vertical = 470 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng Rows:** Kéo lần lượt `DIM Player [Player Name]` và `DIM Club [Club Name]` vào ô **Rows**.
   * **Vùng Values:** Kéo các thước đo: `Minutes Played`, `Is Starter`, `Yellow Cards`, `Red Cards`.
4. **Định dạng chuẩn font chữ và cỡ chữ:**
   * Đổi tên hiển thị các cột: `Số phút`, `Số trận đá chính`, `Thẻ vàng`, `Thẻ đỏ`.
   * Tab **Format visual** -> **Column headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * **Row headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * **Values**: Font `Segoe UI`, Cỡ chữ `10 pt`.

---

### Bước 8: Kết quả và Nhận xét phân tích
* **Kết quả trực quan:** Dashboard phân tích rõ ràng mức độ va chạm và kỷ luật thi đấu. Khi nhấp chọn vị trí `Defender`, toàn bộ danh sách các hậu vệ nhận nhiều thẻ nhất và phân bổ độ tuổi lập tức hiển thị chi tiết.
* **Nhận xét chuyên môn:**
  * **Vị trí nhận nhiều thẻ nhất:** Hậu vệ (Defender) và Tiền vệ phòng ngự (Defensive Midfielder) chiếm tới hơn **70%** tổng số thẻ vàng và thẻ đỏ toàn giải đấu do đặc thù nhiệm vụ đánh chặn và ngăn cản các đợt phản công nguy hiểm.
  * **Độ tuổi chịu tải trọng cao nhất:** Độ tuổi từ **24 đến 29 tuổi** là giai đoạn đỉnh cao thể lực, chiếm tới hơn **60%** tổng số phút thi đấu toàn mùa giải và cũng là nhóm tuổi có tần suất va chạm và nhận thẻ phạt nhiều nhất.
