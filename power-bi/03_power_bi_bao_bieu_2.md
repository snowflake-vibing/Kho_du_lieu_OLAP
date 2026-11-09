# 4.2.2 Báo biểu 2: Vận hành Trận đấu, Câu lạc bộ và Tương quan Sân vận động (Club Match Operations & Stadium Capacity)

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế hoàn chỉnh **Báo biểu 2 (Dashboard 2)** trên **Power BI Desktop**, tập trung phân tích năng lực thi đấu của các câu lạc bộ bóng đá, ưu thế sân nhà / sân khách và ảnh hưởng của quy mô sức chứa sân vận động.

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Phân tích tương quan giữa hiệu suất thi đấu sân nhà (`Is_Home_Game = 1`) và sân khách (`Is_Home_Game = 0`), tổng số bàn thắng theo các giải đấu hàng đầu châu Âu, đồng thời đánh giá tác động của quy mô sân vận động (`Stadium_Seats`) tới khả năng bùng nổ bàn thắng của các đội bóng.
* **Đối tượng theo dõi:**
  * Khối 4 Thẻ KPI: Tổng số trận đấu (`Total Games`), Bàn thắng sân nhà, Bàn thắng sân khách, Tỷ lệ thắng sân nhà (`Home Win Rate %`).
  * Biểu đồ cột phân cụm (Clustered Column Chart): So sánh số bàn thắng Sân nhà vs Sân khách của Top các Câu lạc bộ ghi nhiều bàn nhất.
  * Biểu đồ sơ đồ cây (Treemap Visual): Phân bổ tổng bàn thắng theo các Giải đấu hàng đầu (Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, UEFA Champions League).
  * Biểu đồ kết hợp cột và đường (Line and Clustered Column Chart): Tương quan giữa Sức chứa sân vận động (`Stadium_Seats`) và Hiệu số bàn thắng.
  * Bảng ma trận xếp hạng câu lạc bộ (Matrix Visual): Bảng thống kê chi tiết Câu lạc bộ, Giải đấu, Số trận, Bàn thắng, Sức chứa sân.
  * Hệ thống bộ lọc cắt lát (Slicers): Giải đấu (`Competition_Name`), Mùa giải (`Season`), Loại vòng đấu (`Round`).

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Khởi tạo trang báo cáo mới và tiêu đề
1. Ở mép dưới cùng của Power BI Desktop, nhấp chuột vào dấu cộng `+` bên cạnh thẻ `Hiệu suất Cầu thủ` để tạo trang mới.
2. Nhấp đúp chuột đổi tên thẻ thành: `Vận hành CLB & Sân đấu`.
3. Kiểm tra Canvas settings đảm bảo tỷ lệ chuẩn `16:9`.
4. Trên thanh Ribbon **Insert**, nhấp nút **Text box**, kéo khung đặt ở đỉnh trang và nhập nội dung:
   `BÁO BIỂU 2: PHÂN TÍCH VẬN HÀNH TRẬN ĐẤU, HIỆU SUẤT CLB VÀ TƯƠNG QUAN SÂN VẬN ĐỘNG`
5. Định dạng văn bản: Font `Segoe UI`, Cỡ chữ `15 pt`, In đậm (**Bold**), Căn lề giữa (**Center**).

---

### Bước 2: Thiết lập 4 Thẻ KPI vận hành trận đấu (Card Visuals)
1. **Card 1: Tổng số Trận đấu (Total Matches)**:
   * Thêm visual **Card**, kéo trường `DIM Game [Game_ID]` (chọn hàm `Distinct Count`) vào ô **Fields**.
   * Đổi tên hiển thị thành `Tổng Trận Đấu`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
2. **Card 2: Bàn thắng Sân nhà (Home Goals)**:
   * Thêm visual **Card**, lọc `Is_Home_Game = 1`, kéo thước đo `Goals` vào ô **Fields**.
   * Đổi tên thành `Bàn Thắng Sân Nhà`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
3. **Card 3: Bàn thắng Sân khách (Away Goals)**:
   * Thêm visual **Card**, lọc `Is_Home_Game = 0`, kéo thước đo `Goals` vào ô **Fields**.
   * Đổi tên thành `Bàn Thắng Sân Khách`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
4. **Card 4: Tỷ lệ Ưu thế Sân nhà (Home Advantage %)**:
   * Thêm visual **Card**, kéo tỷ lệ phần trăm bàn thắng sân nhà trên tổng bàn thắng vào ô **Fields**.
   * Đổi tên thành `Tỷ lệ Bàn Sân Nhà (%)`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**), định dạng phần trăm `0.0%`.

---

### Bước 3: Tạo Biểu đồ cột phân cụm Bàn thắng Sân nhà vs Sân khách (Clustered Column Chart)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Clustered column chart**.
2. Kéo khung đặt ở góc phía trên bên trái trang Canvas.
3. Kéo thả các trường dữ liệu:
   * **Vùng X-axis:** Kéo thuộc tính `DIM Club [Club Name]` vào ô **X-axis**.
   * **Vùng Y-axis:** Lần lượt kéo 2 thước đo:
     1. `Bàn Thắng Sân Nhà` (Home Goals)
     2. `Bàn Thắng Sân Khách` (Away Goals)
4. **Thiết lập bộ lọc Top 10 Câu lạc bộ:**
   * Tại khung **Filters on this visual**, mở mục `Club Name`, chọn **Top N**, nhập `10`, kéo thước đo `Goals` vào ô **By value** và nhấp **Apply filter**.
5. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Bật **On**, nhập: `So sánh Bàn thắng Sân nhà vs Sân khách của Top 10 CLB Châu Âu`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Data labels**: Bật **On** hiển thị số bàn trên mỗi đỉnh cột, cỡ chữ `9 pt`.
   * Trục X và Trục Y: Font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 4: Tạo Biểu đồ Treemap phân bổ Bàn thắng theo Giải đấu (Treemap Visual)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Treemap** (biểu đồ các khối hình chữ nhật phân cấp).
2. Kéo khung đặt ở góc phía trên bên phải trang báo cáo.
3. Kéo thả các trường dữ liệu:
   * **Vùng Category:** Kéo thuộc tính `DIM Competition [Competition Name]` vào ô **Category**.
   * **Vùng Values:** Kéo thước đo `Goals` vào ô **Values**.
4. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Bật **On**, nhập: `Quy mô Bàn thắng phân bổ theo Giải đấu Châu Âu`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Data labels**: Bật **On**, hiển thị tên giải đấu và số lượng bàn thắng tương ứng, cỡ chữ `9 pt`.

---

### Bước 5: Tạo Biểu đồ kết hợp Tương quan Sức chứa Sân và Bàn thắng (Line and Clustered Column Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Line and clustered column chart**.
2. Kéo khung đặt ở góc phía dưới bên trái Canvas.
3. Kéo thả các trường dữ liệu:
   * **Vùng X-axis:** Kéo trường `DIM Club [Club Name]` vào ô **X-axis**.
   * **Vùng Column Y-axis (Cột):** Kéo thước đo `Goals` vào ô này.
   * **Vùng Line Y-axis (Đường):** Kéo thuộc tính `DIM Club [Stadium Seats]` (chọn hàm `Average` hoặc `Max`) vào ô này.
4. **Đổi tên và định dạng visual:**
   * Đổi tên cột thành `Tổng số Bàn thắng`.
   * Đổi tên đường thành `Sức chứa Sân vận động (Chỗ ngồi)`.
   * Tab **Format visual** -> **Title**: Bật **On**, nhập: `Tương quan giữa Tổng số Bàn thắng và Sức chứa Sân vận động của CLB`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Data labels**: Bật **On** cho cả Cột và Đường, cỡ chữ `9 pt`.
   * **Y-axis**: Bật cả 2 trục Y để thang đo Chỗ ngồi và thang đo Bàn thắng hiển thị rõ ràng, font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 6: Tạo Bảng Ma trận Xếp hạng Câu lạc bộ chi tiết (Matrix Visual)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Matrix**.
2. Kéo khung đặt ở góc phía dưới bên phải màn hình.
3. Kéo thả các trường dữ liệu:
   * **Vùng Rows:** Kéo `DIM Competition [Competition Name]` ở cấp 1 và `DIM Club [Club Name]` ở cấp 2.
   * **Vùng Values:** Kéo các trường: `Stadium Name`, `Stadium Seats`, `Total Games`, `Goals`, `QoQ Goals Growth`.
4. **Định dạng bảng:**
   * Vào tab **Format visual**:
   * Mục **Column headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * Mục **Values**: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * Row headers bật `Stepped layout` thụt lề 12px để mở rộng từng giải đấu ra danh sách CLB trực thuộc.

---

### Bước 7: Thêm các bộ lọc tương tác (Slicers)
Thêm 3 Slicer điều khiển (Tiêu đề Slicer header: Font `Segoe UI`, cỡ chữ `10 pt`, in đậm; Values: cỡ chữ `10 pt`):
1. **Slicer 1 (Giải đấu):** `DIM Competition [Competition Name]`, kiểu Dropdown.
2. **Slicer 2 (Mùa giải):** `DIM Time [Season]`, kiểu Dropdown.
3. **Slicer 3 (Loại giải đấu):** `DIM Competition [Competition Type]` (Domestic League, Domestic Cup, International Cup), kiểu Tile.

---

### Bước 8: Kết quả và Nhận xét phân tích
* **Kết quả trực quan:** Dashboard cho phép người xem khoan sâu vào từng giải đấu (ví dụ khi nhấp chọn `Bundesliga` hoặc `Champions League`), toàn bộ ma trận so sánh sân nhà/sân khách và tương quan sân bãi của các CLB lập tức cập nhật chuẩn xác.
* **Nhận xét chuyên môn:**
  * **Yếu tố sân nhà:** Các đội bóng hàng đầu châu Âu có tỷ lệ ghi bàn trên sân nhà chiếm từ **56% đến 62%** tổng số bàn thắng, cho thấy sự cổ vũ của khán giả nhà và sự quen thuộc mặt sân tạo ra lợi thế tâm lý và chiến thuật rất lớn.
  * **Tương quan sức chứa sân vận động:** Các câu lạc bộ sở hữu sân vận động có sức chứa khổng lồ trên 60.000 chỗ (như Santiago Bernabéu của Real Madrid, Allianz Arena của Bayern Munich, Etihad Stadium của Man City) đều nằm trong nhóm có hiệu số bàn thắng vượt trội nhất toàn cầu.
