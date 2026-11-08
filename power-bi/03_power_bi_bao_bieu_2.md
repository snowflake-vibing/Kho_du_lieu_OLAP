# 4.2.2 Báo biểu 2: Phân tích chi tiết biến động theo chuỗi thời gian và khung giờ

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế **Báo biểu 2 (Dashboard 2)** trên **Power BI Desktop**, tập trung phân tích hành vi và xu hướng dữ liệu theo trục chuỗi thời gian (Time Series) và các khung giờ trong ngày.

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Phân tích chi tiết dữ liệu giao dịch theo từng mốc thời gian diễn ra (Ngày, Giờ) nhằm phát hiện các khung giờ cao điểm có nguy cơ rủi ro bất thường hoặc biến động đột biến.
* **Đối tượng theo dõi:**
  * Bảng ma trận thời gian (Matrix) phân rã theo phân cấp `PhanCapTime`.
  * Biểu đồ vành khăn (Donut Chart) thể hiện tỷ trọng rủi ro theo từng Giờ (`Hour`) trong 24 giờ.
  * Biểu đồ đường kép (Line Chart) biểu diễn xu hướng song song giữa Tổng số lượng giao dịch và Số lượng rủi ro kèm 2 đường mức trung bình chuẩn (Average Lines).

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Tạo trang báo cáo mới và thiết lập tiêu đề
1. Ở mép dưới cùng của cửa sổ Power BI Desktop, nhấp chuột vào dấu cộng `+` bên cạnh thẻ `Page 1` để tạo một trang báo cáo mới (`Page 2`).
2. Nhấp đúp chuột vào tên thẻ `Page 2`, nhập tên mới là `Báo biểu 2 - Chuỗi thời gian`.
3. Nhấp vào khoảng trống Canvas, tại khung **Format report page** bên phải:
   * **Canvas settings:** Chọn Type là `16:9` (hoặc giữ đồng bộ với Page 1).
4. Trên thanh Ribbon **Insert**, nhấp nút **Text box**, kéo khung đặt ở đầu trang và nhập nội dung:
   `BÁO BIỂU 2: PHÂN TÍCH CHI TIẾT DỮ LIỆU GIAO DỊCH VÀ XU HƯỚNG THEO QUÃNG THỜI GIAN VÀ KHUNG GIỜ`
5. Bôi đen văn bản, đặt cỡ chữ `14 pt`, in đậm (Bold), căn lề giữa và bật viền bo tròn nhẹ tại thẻ Effects.

---

### Bước 2: Tạo biểu đồ Ma trận chi tiết theo thời gian (Matrix Visual)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Matrix**.
2. Kéo khung đặt ở góc phía trên bên trái trang vẽ, chỉnh kích thước chiếm 50% chiều rộng màn hình.
3. Kéo thả các trường dữ liệu từ khung **Data** vào các ô cấu hình của Matrix:
   * **Vùng Rows (Dòng):** Tìm chiều thời gian `DIM Time`, kéo phân cấp `PhanCapTime` (gồm các cấp độ `Year` -> `Month` -> `Day` -> `Hour`) thả vào ô **Rows**.
   * **Vùng Values (Giá trị):** Lần lượt kéo 4 thước đo từ thư mục Measures thả vào ô **Values**:
     1. `Total Transaction` (Tổng số giao dịch)
     2. `Total Transaction Fraud` (Tổng số giao dịch rủi ro/gian lận)
     3. `Total Transaction Amount` (Tổng doanh số giao dịch)
     4. `Total Fraud Amount` (Tổng giá trị thiệt hại rủi ro)
4. **Đổi tên hiển thị cho các cột:**
   * Nhấp chuột phải vào từng trường trong ô Values -> chọn **Rename for this visual**:
     * Đổi `Total Transaction` thành `Tổng số GD`.
     * Đổi `Total Transaction Fraud` thành `Số GD Rủi ro`.
     * Đổi `Total Transaction Amount` thành `Tổng giá trị`.
     * Đổi `Total Fraud Amount` thành `Giá trị Rủi ro`.
5. **Định dạng bảng:**
   * Vào tab **Format visual** -> **Style presets**: Chọn `Alternating rows`.
   * Mục **Row headers**: Bật **Stepped layout** (thụt lề phân cấp) sang **On** và thiết lập thụt dòng 12px để hiển thị cây thời gian rõ ràng khi nhấn nút drill-down mở rộng các cấp.

---

### Bước 3: Tạo Biểu đồ vành khăn (Donut Chart - Phân bổ theo Giờ)
Biểu đồ giúp nhận diện trực quan tỷ trọng rủi ro tập trung vào các khung giờ nào trong ngày (ví dụ các khung giờ rạng sáng 0h-4h hoặc giờ tan tầm 17h-19h).

1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Donut chart** (biểu đồ hình tròn rỗng tâm).
2. Kéo khung đặt ở góc phía trên bên phải trang báo cáo, bên cạnh bảng Matrix.
3. Kéo thả các trường dữ liệu vào các ô cấu hình:
   * **Vùng Legend (Chú giải):** Tìm thuộc tính `Hour` (Giờ trong ngày từ 0 đến 23) trong chiều thời gian, kéo thả vào ô **Legend**.
   * **Vùng Values (Giá trị):** Kéo thước đo `Total Transaction Fraud` (hoặc `Total Fraud`) thả vào ô **Values**.
4. **Đổi tên và định dạng visual:**
   * Nhấp chuột phải vào trường `Total Transaction Fraud` tại ô Values -> chọn **Rename for this visual** -> đổi thành `Số vụ rủi ro`.
   * Vào tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập nội dung: `Tỷ lệ giao dịch rủi ro theo Khung giờ trong ngày`. In đậm, căn giữa.
   * Mục **Detail labels**: Chọn **Label contents** là `All detail labels` (hiển thị cả Giờ, số lượng vụ việc và tỷ lệ %).
   * Mục **Legend**: Đặt **Position** là `Right center` để danh sách các giờ hiển thị gọn gàng bên phải.

---

### Bước 4: Tạo Biểu đồ đường kép (Line Chart) kèm 2 Đường trung bình chuẩn
Biểu đồ đường hiển thị biến động liên tục theo ngày và cho phép so sánh đường thực tế với mức trung bình chuẩn (Average Line).

1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Line chart** (biểu đồ đường).
2. Kéo khung đặt ở nửa dưới trang Canvas, kéo dãn chiều rộng phủ toàn bộ trang báo cáo.
3. Kéo thả các trường dữ liệu vào các ô cấu hình:
   * **Vùng X-axis (Trục hoành):** Kéo phân cấp `PhanCapTime` (hoặc trường `Day` / `Date`) thả vào ô **X-axis**.
   * **Vùng Y-axis (Trục tung):** Lần lượt kéo 2 thước đo thả vào ô **Y-axis**:
     1. `Total Transaction`
     2. `Total Fraud`
4. **Đổi tên hiển thị:**
   * Đổi `Total Transaction` thành `Tổng giao dịch thực tế`.
   * Đổi `Total Fraud` thành `Giao dịch rủi ro thực tế`.
5. **Thiết lập 2 Đường trung bình chuẩn (Average Lines) trong Analytics Pane:**
   * Chọn visual Line Chart vừa tạo.
   * Tại khung bên phải, nhấp vào tab **Analytics** (biểu tượng chiếc kính lúp phóng to có đường đồ thị chéo).
   * Tìm và nhấp mở rộng mục **Average line**:
     * Nhấp chuột vào nút **+ Add line** lần thứ nhất:
       * Tại ô **Series**: Chọn thước đo `Tổng giao dịch thực tế`.
       * Tại ô **Color**: Chọn màu xanh dương nhạt.
       * Tại ô **Style**: Chọn nét đứt đoạn (`Dashed`).
       * Chuyển công tắc **Data label** sang **On** để hiển thị giá trị trung bình trên đường.
     * Nhấp chuột vào nút **+ Add line** lần thứ hai:
       * Tại ô **Series**: Chọn thước đo `Giao dịch rủi ro thực tế`.
       * Tại ô **Color**: Chọn màu đỏ nổi bật.
       * Tại ô **Style**: Chọn nét chấm gạch (`Dotted`).
       * Chuyển công tắc **Data label** sang **On**.
6. **Định dạng hiển thị Line Chart:**
   * Chuyển lại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập: `Xu hướng biến động giao dịch theo ngày và so sánh với mức trung bình`.
   * Mục **Lines**: Đặt độ dày đường (`Stroke width`) là `3 px`.
   * Mục **Markers** (Điểm đánh dấu): Bật **On**, chọn hình tròn nhỏ tại các mốc ngày.

---

### Bước 5: Căn chỉnh vị trí và hoàn thiện Báo biểu 2
1. Sử dụng tính năng **Align** trên dải Ribbon Format để căn chỉnh mép trên của Matrix và Donut Chart thẳng hàng tuyệt đối.
2. Kiểm tra tính năng Drill-down trên trục X của Line Chart: Nhấp vào biểu tượng hai mũi tên trỏ xuống `Click to turn on Drill down` để trải nghiệm mở rộng từ Năm -> Tháng -> Ngày -> Giờ.
3. Lưu lại tiến độ làm việc bằng tổ hợp phím `Ctrl + S`.
