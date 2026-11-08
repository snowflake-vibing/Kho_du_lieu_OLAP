# 4.2.3 Báo biểu 3: Phân tích theo nhóm tuổi khách hàng và loại thiết bị thực hiện

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế hoàn chỉnh **Báo biểu 3 (Dashboard 3)** trên **Power BI Desktop**, tập trung phân tích mối tương quan giữa nhân khẩu học (độ tuổi khách hàng/đối tượng) và phương tiện công nghệ (loại thiết bị giao dịch).

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Phân tích số tiền thiệt hại và số lượng giao dịch rủi ro theo từng nhóm độ tuổi khách hàng và từng loại thiết bị giao dịch (Mobile, Laptop/PC, Tablet, ATM...).
* **Đối tượng theo dõi:**
  * Biểu đồ hình phễu (Funnel Chart) phân bậc mức độ rủi ro số tiền theo các nhóm tuổi (`Age_Group`).
  * Biểu đồ thanh ngang phân cụm (Clustered Bar Chart) so sánh số vụ việc theo từng loại thiết bị (`Device Type`).
  * Biểu đồ kết hợp cột và đường (Line and Clustered Column Chart) so sánh quy mô tổng giá trị giao dịch (cột đứng) với mức độ rủi ro số tiền (đường cong).

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Khởi tạo trang báo cáo và tiêu đề
1. Ở mép dưới cùng cửa sổ Power BI, nhấp chuột vào biểu tượng dấu cộng `+` để thêm trang mới (`Page 3`).
2. Nhấp đúp chuột đổi tên thẻ thành `Báo biểu 3 - Nhân khẩu & Thiết bị`.
3. Kiểm tra kích thước trang tại thẻ **Format report page** -> **Canvas settings** đảm bảo tỷ lệ chuẩn `16:9`.
4. Trên thanh Ribbon **Insert**, nhấp chọn **Text box**, kéo thả lên đỉnh trang báo cáo và nhập tiêu đề:
   `BÁO BIỂU 3: PHÂN TÍCH QUY MÔ SỐ TIỀN VÀ SỐ LƯỢNG RỦI RO THEO ĐỘ TUỔI VÀ LOẠI THIẾT BỊ SỬ DỤNG`
5. Bôi đen văn bản, đặt cỡ chữ `14 pt`, in đậm, căn giữa và bật viền bo tròn thẩm mỹ.

---

### Bước 2: Tạo Biểu đồ hình phễu (Funnel Chart)
Biểu đồ hình phễu giúp nhận diện trực quan nhóm tuổi nào chịu tổn thất thiệt hại nặng nề nhất và mức độ suy giảm dần theo từng bậc nhóm tuổi.

1. Tại khung **Visualizations**, tìm và nhấp chuột vào biểu tượng **Funnel** (biểu đồ hình chiếc phễu thuôn dần xuống dưới).
2. Kéo khung biểu đồ đặt ở góc bên trái trang vẽ, chỉnh kích thước chiếm 35% chiều rộng và kéo dài khoảng 85% chiều cao trang vẽ.
3. Kéo thả các trường dữ liệu từ khung **Data** vào các ô cấu hình:
   * **Vùng Category (Phân loại):** Tìm thuộc tính `Age_Group` (hoặc `Customer Age` được nhóm theo khoảng tuổi: 18-25, 26-35, 36-50, >50) trong chiều khách hàng/đối tượng, kéo thả vào ô **Category**.
   * **Vùng Values (Giá trị):** Kéo thước đo `Total Fraud Amount` (Tổng số tiền gian lận/thiệt hại) thả vào ô **Values**.
4. **Đổi tên và định dạng visual:**
   * Nhấp chuột phải vào trường `Total Fraud Amount` tại ô Values -> chọn **Rename for this visual** -> đổi thành `Số tiền rủi ro`.
   * Chuyển sang tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập nội dung: `Phân cấp thiệt hại rủi ro theo Nhóm tuổi`. Căn giữa, in đậm.
   * Mục **Colors**: Chọn gam màu đơn sắc dải gradient xanh dương hoặc cam đỏ cảnh báo.
   * Mục **Data labels**: Bật **On**, chọn hiển thị giá trị tiền tệ thực tế và tỷ lệ phần trăm so với tầng phễu đầu tiên (`Percent of first`).

---

### Bước 3: Tạo Biểu đồ thanh ngang phân cụm (Clustered Bar Chart)
Biểu đồ thanh ngang giúp so sánh trực quan thứ bậc của các thiết bị có số vụ việc rủi ro phát sinh nhiều nhất.

1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Clustered bar chart** (biểu đồ thanh nằm ngang).
2. Kéo khung đặt ở góc phía trên bên phải của Canvas (ngay bên cạnh biểu đồ phễu).
3. Kéo thả các trường dữ liệu vào các ô cấu hình:
   * **Vùng Y-axis (Trục tung đứng):** Tìm thuộc tính `Device Type` (Loại thiết bị: Mobile Web, Mobile App, Desktop, Tablet, POS...) trong chiều thiết bị, kéo thả vào ô **Y-axis**.
   * **Vùng X-axis (Trục hoành ngang):** Kéo thước đo `Total Fraud` (Tổng số giao dịch rủi ro) thả vào ô **X-axis**.
4. **Đổi tên và định dạng visual:**
   * Nhấp chuột phải vào `Total Fraud` trên X-axis -> đổi tên thành `Số vụ rủi ro`.
   * Tại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập: `Số lượng giao dịch rủi ro theo Loại thiết bị`. Căn giữa, in đậm.
   * Mục **Bars**: Chọn màu sắc thanh (màu đỏ đô hoặc tím than).
   * Mục **Data labels**: Bật công tắc sang **On** để số lượng giao dịch hiển thị rõ ràng ở cuối mỗi thanh ngang.

---

### Bước 4: Tạo Biểu đồ kết hợp cột và đường (Line and Clustered Column Chart)
Biểu đồ kết hợp hiển thị đồng thời hai thang đo: Trục cột biểu diễn quy mô tổng dòng tiền giao dịch, còn trục đường cong biểu diễn quy mô số tiền rủi ro theo từng nhóm tuổi.

1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Line and clustered column chart** (biểu đồ có các cột đứng và một đường cong chạy qua).
2. Kéo khung đặt ở góc phía dưới bên phải Canvas, ngay dưới biểu đồ thanh ngang vừa tạo ở Bước 3.
3. Kéo thả các trường dữ liệu vào các ô cấu hình:
   * **Vùng X-axis (Trục hoành):** Kéo trường `Age_Group` (Nhóm tuổi) thả vào ô **X-axis**.
   * **Vùng Column Y-axis (Trục tung cho Cột):** Kéo thước đo `Total Transaction Amount` (Tổng giá trị giao dịch) thả vào ô **Column Y-axis**.
   * **Vùng Line Y-axis (Trục tung phụ cho Đường):** Kéo thước đo `Total Fraud Amount` (Tổng số tiền gian lận/rủi ro) thả vào ô **Line Y-axis**.
4. **Đổi tên hiển thị:**
   * Đổi `Total Transaction Amount` thành `Tổng doanh số GD (Cột)`.
   * Đổi `Total Fraud Amount` thành `Giá trị rủi ro (Đường)`.
5. **Định dạng visual:**
   * Tại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập nội dung: `Tương quan Tổng giao dịch và Giá trị rủi ro theo Độ tuổi`. Căn giữa, in đậm.
   * Mục **Columns**: Chọn màu cột xanh navy nhạt.
   * Mục **Lines**: Chọn màu đường đỏ tươi nổi bật, tăng độ dày đường lên `3 px`.
   * Mục **Y-axis**: Bật cả hai trục hiển thị rõ ràng thang đo giá trị.
   * Mục **Data labels**: Bật **On** cho cả cột và đường để theo dõi con số chi tiết.

---

### Bước 5: Căn chỉnh vị trí, hoàn thiện bố cục và lưu tệp
1. Điều chỉnh kích thước và khoảng cách giữa các visual trên Canvas:
   * Biểu đồ Funnel chiếm gọn gàng toàn bộ cột dọc bên trái.
   * Phía bên phải chia làm 2 tầng bằng nhau: Tầng trên là Clustered Bar Chart, tầng dưới là Line and Clustered Column Chart.
2. Kiểm tra tính năng lọc chéo: Khi nhấp chuột vào thiết bị `Mobile App` ở biểu đồ thanh ngang, biểu đồ phễu và biểu đồ kết hợp cột đường lập tức cập nhật tương ứng theo riêng đối tượng người dùng Mobile App.
3. Lưu lại toàn bộ Dashboard hoàn chỉnh: Nhấn `Ctrl + S`.
