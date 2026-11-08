# 4.3 Quá trình lập báo biểu bằng công cụ Google Data Studio (Looker Studio)

Tài liệu này hướng dẫn chi tiết quy trình xây dựng hệ thống báo biểu trực quan hóa dữ liệu trên nền tảng đám mây **Google Data Studio (Looker Studio)** dựa trên tệp dữ liệu phẳng đã được trích xuất từ kho dữ liệu ở mục 4.1.2.

---

## 4.3.1 Báo biểu 1: Thống kê chi tiết các sự vụ rủi ro trong khoảng thời gian xác định (15 ngày đầu tháng)

### 1. Mục tiêu và nội dung
* **Nội dung:** Giám sát và thống kê biến động số lượng các sự vụ rủi ro/giao dịch gian lận diễn ra từ ngày **01/01/2025 đến ngày 15/01/2025** thông qua bộ 3 biểu đồ đồng bộ: Cột đứng, Hình tròn và Đường xu hướng.

### 2. Các bước thực hiện chi tiết

#### Bước 1: Khởi tạo và thêm các visual lên trang báo cáo
1. Tại cửa sổ làm việc của báo cáo trống trên Looker Studio, quan sát thanh menu phía trên và nhấp chuột vào nút **Thêm biểu đồ** (Add a chart).
2. Lần lượt chọn và kéo thả 3 loại biểu đồ vào Canvas:
   * **Biểu đồ cột (Column Chart):** Đặt ở nửa bên trái.
   * **Biểu đồ hình tròn (Pie Chart):** Đặt ở góc trên bên phải.
   * **Biểu đồ chuỗi thời gian / đường (Line Chart):** Đặt ở góc dưới bên phải.

#### Bước 2: Thiết lập cấu hình dữ liệu cho Biểu đồ Cột
1. Nhấp chuột chọn biểu đồ cột vừa thêm.
2. Tại bảng điều khiển **Thiết lập** (Setup) ở cạnh phải màn hình:
   * **Phương diện (Dimension):** Kéo trường `Day` thả vào ô Phương diện.
   * **Chỉ số (Metric):** Kéo trường `Record Count` (hoặc `Transaction_ID` với hàm `COUNT`) thả vào ô Chỉ số.

#### Bước 3: Tạo và áp dụng các bộ lọc chuyên sâu (Filters)
Để chỉ hiển thị đúng các giao dịch rủi ro trong 15 ngày đầu tiên, ta cần tạo 2 bộ lọc kết hợp:
1. Tại bảng Thiết lập, cuộn xuống mục **Bộ lọc biểu đồ** (Chart Filter) -> nhấp **Thêm bộ lọc** (Add a filter) -> nhấp **Tạo bộ lọc** (Create a filter).
2. **Tạo bộ lọc thứ nhất - `Fraud`:**
   * **Tên bộ lọc:** Nhập `Fraud`.
   * **Quy tắc:** Chọn `Bao gồm` (Include).
   * **Trường:** Chọn `Is_Fraud` (hoặc cờ chỉ báo rủi ro).
   * **Điều kiện:** Chọn `Bằng (=)`.
   * **Giá trị:** Nhập `1`.
   * Nhấp nút **Lưu** (Save).
3. **Tạo bộ lọc thứ hai - `15 days`:**
   * Nhấp chuột tiếp tục vào **Thêm bộ lọc** -> chọn **Tạo bộ lọc**.
   * **Tên bộ lọc:** Nhập `15 days`.
   * **Quy tắc:** Chọn `Bao gồm` (Include).
   * **Trường:** Chọn `Day`.
   * **Điều kiện:** Chọn `Nhỏ hơn hoặc bằng (<=)`.
   * **Giá trị:** Nhập `15`.
   * Nhấp nút **Lưu** (Save).

#### Bước 4: Cấu hình quy tắc sắp xếp (Sort)
1. Tại bảng Thiết lập của biểu đồ cột, cuộn đến mục **Sắp xếp** (Sort):
   * Nhấp vào trường sắp xếp hiện tại và chọn lại thuộc tính `Day`.
   * Tích chọn tùy chọn **Tăng dần** (Ascending) để các ngày từ ngày 1 đến ngày 15 hiển thị theo đúng thứ tự thời gian tự nhiên.

#### Bước 5: Cấu hình đồng bộ cho Biểu đồ Tròn và Biểu đồ Đường
1. Nhấp chuột chọn Biểu đồ Tròn:
   * Phương diện: Chọn `Day`.
   * Chỉ số: Chọn `Record Count`.
   * Bộ lọc: Áp dụng cả 2 bộ lọc đã lưu ở Bước 3 là `Fraud` và `15 days`.
2. Nhấp chuột chọn Biểu đồ Đường:
   * Phương diện: Chọn `Day`.
   * Chỉ số: Chọn `Record Count`.
   * Sắp xếp: Chọn `Day` theo chiều Tăng dần.
   * Bộ lọc: Áp dụng cả 2 bộ lọc `Fraud` và `15 days`.

#### Bước 6: Đổi tên nhãn hiển thị và định dạng thẩm mỹ
1. Tại ô Chỉ số của từng biểu đồ, di chuột vào chữ `Record Count`, nhấp vào biểu tượng cây bút chì chỉnh sửa -> đổi tên hiển thị thành `Giao dịch gian lận`.
2. Chuyển sang thẻ **Kiểu** (Style):
   * Tích chọn ô **Hiển thị nhãn dữ liệu** (Show data labels) để hiển thị con số trên đỉnh các cột và điểm mút của đường.
   * Đặt màu sắc chủ đạo là xanh navy và cam cảnh báo.

---

## 4.3.2 Báo biểu 2: Thống kê số lượng giao dịch rủi ro trên tổng số giao dịch theo danh mục đối tượng

### 1. Mục tiêu và nội dung
* **Nội dung:** So sánh tỷ trọng giữa số lượng giao dịch bình thường và giao dịch rủi ro phát sinh trên từng danh mục ngành hàng/đối tượng (`Merchant_Category`).

### 2. Các bước thực hiện chi tiết

#### Bước 1: Thêm các biểu đồ phân tích cơ cấu
1. Tạo một trang báo cáo mới trên Looker Studio (`Trang` -> `Thêm trang mới`).
2. Nhấp menu **Thêm biểu đồ** và chọn 3 dạng trực quan:
   * **Bảng tổng hợp (Pivot Table):** Hiển thị dạng bảng lưới chéo đa chiều có thanh nhiệt (heatmap).
   * **Biểu đồ cột chồng 100% (100% Stacked Column Chart):** So sánh tỷ lệ phần trăm phân bổ 0 và 1.
   * **Biểu đồ kết hợp cột và đường (Combo Chart):** So sánh tổng số lượng với số vụ rủi ro.

#### Bước 2: Thiết lập cấu hình cho Bảng tổng hợp (Pivot Table)
1. Nhấp chọn biểu đồ Bảng tổng hợp.
2. Tại bảng **Thiết lập**:
   * **Phương diện hàng (Row Dimension):** Chọn trường `Merchant_Category` (Danh mục ngành hàng/đối tượng).
   * **Phương diện cột (Column Dimension):** Chọn trường `Is_Fraud` (Trạng thái rủi ro: 0 là bình thường, 1 là gian lận).
   * **Chỉ số (Metric):** Chọn `Record Count`.
3. Tại thẻ **Kiểu**:
   * Chọn định dạng số liệu có thanh nhiệt (Heatmap) để làm nổi bật các ô có giá trị lớn bằng màu đậm hơn.

#### Bước 3: Thiết lập cho Biểu đồ Cột chồng 100% và Biểu đồ Kết hợp
1. Nhấp chọn biểu đồ Cột chồng 100%:
   * **Phương diện:** Chọn `Merchant_Category`.
   * **Phương diện phân tích (Breakdown Dimension):** Chọn `Is_Fraud`.
   * **Chỉ số:** Chọn `Record Count`.
2. Nhấp chọn biểu đồ Kết hợp cột và đường:
   * **Phương diện:** Chọn `Merchant_Category`.
   * **Chỉ số cột (Bars):** Chọn `Record Count` (Tổng giao dịch).
   * **Chỉ số đường (Lines):** Chọn `Is_Fraud` (Tổng số vụ gian lận).
3. Đổi tên hiển thị các trường và bật hiển thị nhãn số liệu trong thẻ Kiểu.

---

## 4.3.3 Báo biểu 3: Phân bố số tiền rủi ro theo Tiểu bang (State) và Thành phố (City) với tính năng xem chi tiết (Drill-down)

### 1. Mục tiêu và nội dung
* **Nội dung:** Theo dõi tổng số tiền thiệt hại phân bổ theo cấp địa lý, hỗ trợ tính năng khoan sâu (Drill-down) từ cấp Vùng/Tiểu bang xuống chi tiết từng Thành phố trực thuộc.
* **Xử lý trùng lặp:** Do có nhiều thành phố ở các bang khác nhau trùng tên nhau (ví dụ: Arlington, Springfield), cần tạo một trường thuộc tính tính toán mới kết hợp cả Tên Bang và Tên Thành phố để đảm bảo phân nhóm chính xác.

### 2. Các bước thực hiện chi tiết

#### Bước 1: Tạo trường đã tính (Calculated Field) để phân biệt Thành phố
1. Tại khung **Dữ liệu** ở bên phải, nhấp chuột vào nút **Thêm trường** (Add field) -> chọn **Thêm trường đã tính** (Add calculated field).
2. Trong cửa sổ soạn thảo công thức:
   * **Tên trường (Field Name):** Nhập `State_City`.
   * **Công thức (Formula):** Nhập biểu thức nối chuỗi:
     ```sql
     CONCAT(Transaction_State, " - ", Transaction_City)
     ```
3. Nhấp nút **Lưu** (Save) và nhấp nút **Xong** (Done) để hoàn tất. Trường mới `State_City` xuất hiện trong danh sách dữ liệu.

#### Bước 2: Thêm các biểu đồ trực quan hóa
1. Thêm một trang báo cáo mới (`Trang 3`).
2. Nhấp menu **Thêm biểu đồ**, chọn 3 biểu đồ:
   * **Biểu đồ cột (Column Chart)**
   * **Biểu đồ đường (Line Chart)**
   * **Bảng dữ liệu phẳng (Table)**

#### Bước 3: Thiết lập cấu hình tính năng Khoan sâu (Drill-down)
1. Nhấp chuột chọn biểu đồ Cột.
2. Tại bảng **Thiết lập**:
   * Tại mục **Phương diện**, nhấp chọn trường `Transaction_State`.
   * Bật công tắc **Xem chi tiết** (Drill-down) sang trạng thái **BẬT (ON)**.
   * Nhấp vào nút **Thêm phương diện** nằm ngay bên dưới và chọn trường tính toán vừa tạo: `State_City`.
   * Tại mục **Chỉ số (Metric):** Kéo trường `Transaction_Amount` vào và đặt hàm tổng hợp là `SUM`.
   * Tại mục **Bộ lọc:** Áp dụng bộ lọc `Fraud` (`Is_Fraud = 1`) để chỉ tính tiền của các sự vụ rủi ro.

#### Bước 4: Tạo bộ lọc giới hạn Top khu vực có thiệt hại cao nhất
1. Để bảng báo cáo không bị quá tải bởi hàng trăm thành phố nhỏ, tạo thêm bộ lọc giới hạn:
   * Bộ lọc `State_Most_Fraud_Amount` hoặc cấu hình mục **Sắp xếp** theo `Transaction_Amount` Giảm dần (Descending), giới hạn số hàng hiển thị là `10` hoặc `15`.
2. Lần lượt áp dụng cấu hình trên cho Biểu đồ Đường và Bảng dữ liệu.

#### Bước 5: Kiểm tra và trải nghiệm tính năng Drill-down
1. Nhấp nút **Xem** (View) ở góc trên bên phải màn hình để chuyển sang chế độ người dùng xem báo cáo.
2. Tại Biểu đồ Cột đang hiển thị mức Bang (`Transaction_State`):
   * Quan sát thanh công cụ nhỏ ở góc trên bên phải của biểu đồ, nhấp chuột vào biểu tượng mũi tên trỏ xuống (`Khoan sâu` / `Drill down`).
   * Biểu đồ lập tức chuyển đổi cấp độ hiển thị từ các Bang sang danh sách chi tiết các Thành phố trực thuộc (`State_City`) với số tiền thiệt hại tương ứng.
   * Nhấp mũi tên trỏ lên (`Khoan lên` / `Drill up`) để quay trở lại cấp độ Bang tổng quát.
