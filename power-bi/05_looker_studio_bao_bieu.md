# 4.3 Quá trình lập báo biểu bằng công cụ Google Data Studio (Looker Studio) cho Dữ liệu Bóng đá Châu Âu

Tài liệu này hướng dẫn chi tiết quy trình xây dựng hệ thống 3 báo biểu trực quan hóa dữ liệu bóng đá trên nền tảng đám mây **Google Data Studio (Looker Studio)** dựa trên tệp dữ liệu phẳng `Football_Report_Data.csv` đã được trích xuất từ kho dữ liệu ở mục 4.1.2.

---

## 4.3.1 Báo biểu 1: Giám sát hiệu suất ghi bàn của các chân sút chủ lực theo giải đấu

### 1. Mục tiêu và nội dung
* **Nội dung:** Giám sát danh sách các chân sút chủ lực có hiệu suất ghi bàn cao trong các giải đấu hàng đầu châu Âu, phân tích phân bổ bàn thắng theo thời gian và giải đấu thông qua bộ 3 biểu đồ: Cột đứng, Hình tròn và Đường xu hướng.

### 2. Các bước thực hiện chi tiết

#### Bước 1: Khởi tạo và thêm các visual lên trang báo cáo
1. Tại giao diện chỉnh sửa của báo cáo Looker Studio, nhấp nút **Thêm biểu đồ** (Add a chart) trên thanh menu.
2. Thêm 3 loại biểu đồ vào trang Canvas:
   * **Biểu đồ cột (Column Chart):** Đặt ở nửa bên trái trang.
   * **Biểu đồ hình tròn (Pie Chart):** Đặt ở góc trên bên phải.
   * **Biểu đồ chuỗi thời gian (Time Series / Line Chart):** Đặt ở góc dưới bên phải.

#### Bước 2: Thiết lập cấu hình dữ liệu cho Biểu đồ Cột
1. Nhấp chọn biểu đồ Cột vừa thêm.
2. Tại bảng điều khiển **Thiết lập** (Setup) ở cạnh phải màn hình:
   * **Phương diện (Dimension):** Kéo trường `Player_Name` vào ô Phương diện.
   * **Chỉ số (Metric):** Kéo trường `Goals` vào ô Chỉ số (hàm `SUM`).
   * **Sắp xếp (Sort):** Chọn `Goals` theo chiều **Giảm dần (Descending)**, giới hạn hiển thị **10 thanh (Top 10)**.

#### Bước 3: Tạo và áp dụng các bộ lọc chuyên sâu (Filters)
1. Tại bảng Thiết lập của biểu đồ cột, cuộn xuống mục **Bộ lọc biểu đồ** -> nhấp **Thêm bộ lọc** -> **Tạo bộ lọc**:
   * **Tên bộ lọc:** Nhập `Scorers_Only`.
   * **Quy tắc:** Chọn `Bao gồm` (Include).
   * **Trường:** Chọn `Goals`.
   * **Điều kiện:** Chọn `Lớn hơn (>)`.
   * **Giá trị:** Nhập `0`.
   * Nhấp nút **Lưu** (Save) để loại bỏ các cầu thủ không ghi bàn.

#### Bước 4: Cấu hình đồng bộ cho Biểu đồ Tròn và Biểu đồ Đường
1. Nhấp chọn Biểu đồ Tròn:
   * **Phương diện:** Chọn `Competition_Name` (Tên giải đấu).
   * **Chỉ số:** Chọn `Goals` (SUM).
   * **Bộ lọc:** Áp dụng bộ lọc `Scorers_Only`.
2. Nhấp chọn Biểu đồ Đường:
   * **Phương diện:** Chọn `Month` hoặc `Quarter`.
   * **Chỉ số:** Chọn `Goals` (SUM).
   * **Sắp xếp:** Chọn thời gian Tăng dần.
   * **Bộ lọc:** Áp dụng bộ lọc `Scorers_Only`.

#### Bước 5: Đổi tên hiển thị và định dạng thẩm mỹ
1. Tại ô Chỉ số, đổi tên hiển thị thành `Tổng Bàn Thắng`.
2. Tại tab **Kiểu** (Style), bật ô **Hiển thị nhãn dữ liệu** (Show data labels) để hiển thị con số trên đỉnh các cột và điểm mút của đường.

---

## 4.3.2 Báo biểu 2: Cơ cấu đóng góp bàn thắng theo Vị trí thi đấu và Giải đấu

### 1. Mục tiêu và nội dung
* **Nội dung:** So sánh tỷ trọng giữa số bàn thắng (`Goals`) và kiến tạo (`Assists`) của các tuyến thi đấu (`Main_Position`: Attack, Midfield, Defender) trên từng giải đấu bóng đá châu Âu.

### 2. Các bước thực hiện chi tiết

#### Bước 1: Thêm các biểu đồ phân tích cơ cấu
1. Tạo một trang báo cáo mới trên Looker Studio (`Trang` -> `Thêm trang mới`).
2. Nhấp menu **Thêm biểu đồ** và chọn 3 dạng trực quan:
   * **Bảng tổng hợp (Pivot Table):** Hiển thị dạng bảng lưới chéo đa chiều có thanh nhiệt (heatmap).
   * **Biểu đồ cột chồng 100% (100% Stacked Column Chart):** So sánh tỷ lệ phần trăm phân bổ bàn thắng theo vị trí.
   * **Biểu đồ kết hợp cột và đường (Combo Chart):** So sánh tổng bàn thắng với số phút thi đấu.

#### Bước 2: Thiết lập cấu hình cho Bảng tổng hợp (Pivot Table)
1. Nhấp chọn biểu đồ Bảng tổng hợp.
2. Tại bảng **Thiết lập**:
   * **Phương diện hàng (Row Dimension):** Chọn trường `Competition_Name` (Giải đấu).
   * **Phương diện cột (Column Dimension):** Chọn trường `Main_Position` (Vị trí thi đấu).
   * **Chỉ số (Metric):** Chọn `Goals` (SUM).
3. Tại thẻ **Kiểu**:
   * Chọn định dạng số liệu có thanh nhiệt (Heatmap) để làm nổi bật các ô có số lượng bàn thắng vượt trội.

#### Bước 3: Thiết lập cho Biểu đồ Cột chồng 100% và Biểu đồ Kết hợp
1. Nhấp chọn biểu đồ Cột chồng 100%:
   * **Phương diện:** Chọn `Competition_Name`.
   * **Phương diện phân tích (Breakdown Dimension):** Chọn `Main_Position`.
   * **Chỉ số:** Chọn `Goals`.
2. Nhấp chọn biểu đồ Kết hợp cột và đường:
   * **Phương diện:** Chọn `Main_Position`.
   * **Chỉ số cột (Bars):** Chọn `Goals`.
   * **Chỉ số đường (Lines):** Chọn `Assists`.
3. Đổi tên hiển thị các trường và bật hiển thị nhãn số liệu trong thẻ Kiểu.

---

## 4.3.3 Báo biểu 3: Phân bố Sức chứa Sân vận động và Bàn thắng theo Cấp Quốc gia và Câu lạc bộ với tính năng Khoan sâu (Drill-down)

### 1. Mục tiêu và nội dung
* **Nội dung:** Theo dõi tổng số bàn thắng và sức chứa sân vận động của các câu lạc bộ, hỗ trợ tính năng khoan sâu (Drill-down) từ cấp Quốc gia giải đấu (`Competition_Country`) xuống chi tiết từng Câu lạc bộ (`Club_Name`).

### 2. Các bước thực hiện chi tiết

#### Bước 1: Tạo trường đã tính (Calculated Field) phân biệt Câu lạc bộ
1. Tại khung **Dữ liệu** ở bên phải, nhấp nút **Thêm trường** (Add field) -> chọn **Thêm trường đã tính** (Add calculated field).
2. Trong cửa sổ công thức:
   * **Tên trường:** Nhập `Club_Country`.
   * **Công thức:** Nhập biểu thức nối chuỗi:
     ```sql
     CONCAT(Competition_Country, " - ", Club_Name)
     ```
3. Nhấp nút **Lưu** (Save) và nhấp nút **Xong** (Done).

#### Bước 2: Thêm các biểu đồ trực quan hóa
1. Thêm một trang báo cáo mới (`Trang 3`).
2. Nhấp menu **Thêm biểu đồ**, chọn 3 biểu đồ:
   * **Biểu đồ cột (Column Chart)**
   * **Biểu đồ đường (Line Chart)**
   * **Bảng dữ liệu phẳng (Table)**

#### Bước 3: Thiết lập cấu hình tính năng Khoan sâu (Drill-down)
1. Nhấp chuột chọn biểu đồ Cột.
2. Tại bảng **Thiết lập**:
   * Tại mục **Phương diện**, nhấp chọn trường `Competition_Country`.
   * Bật công tắc **Xem chi tiết** (Drill-down) sang trạng thái **BẬT (ON)**.
   * Nhấp nút **Thêm phương diện** nằm ngay bên dưới và chọn trường tính toán vừa tạo: `Club_Country`.
   * Tại mục **Chỉ số (Metric):** Kéo trường `Goals` vào và đặt hàm tổng hợp là `SUM`.
   * Kéo thêm chỉ số thứ hai: `Stadium_Seats` với hàm `AVERAGE`.

#### Bước 4: Kiểm tra và trải nghiệm tính năng Drill-down
1. Nhấp nút **Xem** (View) ở góc trên bên phải màn hình để chuyển sang chế độ người dùng xem báo cáo.
2. Tại Biểu đồ Cột đang hiển thị mức Quốc gia (`England`, `Spain`, `Germany`, `Italy`, `France`):
   * Nhấp chuột vào biểu tượng mũi tên trỏ xuống (`Khoan sâu` / `Drill down`) ở góc trên biểu đồ.
   * Biểu đồ lập tức chuyển đổi cấp độ hiển thị từ các Quốc gia sang danh sách chi tiết các Câu lạc bộ trực thuộc (`Manchester City`, `Arsenal`, `Real Madrid`, `Bayern Munich`...) với số bàn thắng và sức chứa sân tương ứng.
   * Nhấp mũi tên trỏ lên (`Khoan lên` / `Drill up`) để quay trở lại cấp độ Quốc gia tổng quát.
