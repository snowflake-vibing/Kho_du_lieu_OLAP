# 4.2.1 Báo biểu 1: Thống kê tổng hợp số lượng, quy mô và xu hướng phân bổ theo vị trí và phân loại

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế hoàn chỉnh **Báo biểu 1 (Dashboard 1)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp với khối dữ liệu SSAS.

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Thống kê tổng hợp rủi ro giao dịch, số tiền và xu hướng phân bổ hàng ngày theo từng vị trí địa lý (State/City) và loại hình phân loại giao dịch.
* **Đối tượng theo dõi:**
  * Bảng ma trận đa chiều (Matrix) phân rã theo Ngày (`Day`) và Phân cấp Địa lý (`PhanCapLocation`).
  * Cơ cấu số vụ rủi ro/giao dịch theo từng Bang/Khu vực (Pie Chart 1).
  * Cơ cấu tổng quy mô số tiền theo từng loại hình giao dịch (Pie Chart 2).
  * Biểu đồ cột phân cụm (Clustered Column Chart) so sánh tương quan chéo giữa Loại hình và Khu vực địa lý.

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Kết nối dữ liệu vào Report
1. Khởi động Power BI Desktop, tạo một tệp báo cáo mới (`File` -> `New`).
2. Trên thanh Ribbon **Home**, nhấp chuột vào biểu tượng **Get data** -> chọn **SQL Server Analysis Services database**.
3. Nhập tên máy chủ tại ô **Server** (ví dụ: `.` hoặc `localhost`), nhập tên database SSAS tại ô **Database**.
4. Tích chọn tùy chọn **Connect live**, nhấp nút **OK**.
5. Trong cửa sổ Navigator, chọn Cube phân tích và nhấp nút **OK**.

---

### Bước 2: Cấu hình kích thước trang báo cáo (Canvas Settings)
1. Nhấp chuột vào một khoảng trống bất kỳ trên trang vẽ báo cáo (Canvas) để đảm bảo không visual nào được chọn.
2. Tại khung công cụ bên phải, nhấp vào biểu tượng cây cọ sơn **Format report page** (Định dạng trang báo cáo).
3. Nhấp mở rộng mục **Canvas settings**:
   * Tại ô **Type**: Nhấp mở danh sách thả xuống và chọn **16:9** (hoặc chọn **Custom** nếu muốn tùy chỉnh chiều rộng `Width: 1280 px`, chiều cao `Height: 720 px` hoặc `900 px` để chứa đủ nhiều biểu đồ).
4. Nhấp mở rộng mục **Canvas background**:
   * Thiết lập **Color**: Chọn màu xám nhạt (ví dụ `#F5F5F5`) hoặc giữ màu trắng.
   * Kéo thanh **Transparency** về `0%` để màu nền có hiệu lực.

---

### Bước 3: Tạo Text Box tiêu đề báo cáo (Label)
1. Trên thanh Ribbon **Insert**, nhấp chuột vào biểu tượng **Text box**.
2. Một khung văn bản xuất hiện trên Canvas. Nhấp giữ chuột vào khung để di chuyển lên sát mép trên cùng của trang báo cáo và kéo dãn chiều rộng sang hai bên.
3. Nhấp đúp chuột vào bên trong Text box và nhập nội dung tiêu đề:
   `BÁO BIỂU 1: THỐNG KÊ TỔNG HỢP RỦI RO, QUY MÔ SỐ TIỀN VÀ XU HƯỚNG THEO VỊ TRÍ VÀ LOẠI HÌNH GIAO DỊCH`
4. Bôi đen toàn bộ đoạn văn bản vừa nhập:
   * Đặt cỡ chữ: Chọn **14 pt** hoặc **16 pt**.
   * Đặt định dạng: Nhấp chọn biểu tượng chữ **B** (Bold) để in đậm.
   * Màu chữ: Chọn màu xanh đậm hoặc đen xám chuyên nghiệp.
5. Tại khung Format Text box bên phải: Vào mục **Effects** -> chuyển công tắc **Visual border** sang **On**, bo góc 4px để tạo đường viền bo tròn nhẹ.

---

### Bước 4: Tạo biểu đồ Ma trận đa cấp (Matrix Visual)
Biểu đồ Matrix cho phép xem chi tiết dữ liệu ở cấp độ dòng đa tầng (drill-down).

1. Tại khung **Visualizations** ở góc trên bên phải, nhấp chuột vào biểu tượng **Matrix** (biểu đồ lưới có các hàng và cột phân cấp).
2. Một khung Matrix trống xuất hiện trên trang vẽ. Kéo khung đặt ở góc phía trên bên trái và căn chỉnh chiều rộng chiếm khoảng 60% trang báo cáo.
3. Kéo thả các trường dữ liệu từ khung **Data** (bên phải) vào các ô cấu hình của Matrix:
   * **Vùng Rows (Dòng):**
     * Tìm và kéo trường `Day` (từ chiều thời gian `DIM Time`) thả vào ô **Rows**.
     * Tìm và kéo phân cấp địa lý `PhanCapLocationTransaction` (hoặc lần lượt `Transaction State`, `Transaction City` từ chiều địa lý) thả vào ô **Rows** ngay bên dưới trường `Day`.
   * **Vùng Values (Giá trị):** Lần lượt kéo các thước đo đo lường từ thư mục Measures thả vào ô **Values**:
     1. `Total Transaction` (Tổng số lượng giao dịch)
     2. `Total Fraud` (Tổng số giao dịch gian lận/bất thường)
     3. `Total Transaction Amount` (Tổng số tiền giao dịch)
     4. `Total Fraud Amount` (Tổng số tiền gian lận)
     5. `Average Transaction Amount` (Số tiền giao dịch trung bình)
     6. `Average Fraud Amount` (Số tiền gian lận trung bình)
4. **Đổi tên hiển thị các cột trong bảng Matrix:**
   * Tại vùng Values, nhấp chuột phải vào từng trường (hoặc nhấp đúp) -> chọn **Rename for this visual**:
     * Đổi `Total Transaction` thành `Tổng GD`.
     * Đổi `Total Fraud` thành `Số vụ rủi ro`.
     * Đổi `Total Transaction Amount` thành `Tổng giá trị (VND/$)`.
     * Đổi `Total Fraud Amount` thành `Giá trị rủi ro`.
     * Đổi `Average Transaction Amount` thành `TB GD`.
     * Đổi `Average Fraud Amount` thành `TB Rủi ro`.
5. **Định dạng bảng Matrix:**
   * Chọn visual Matrix, chuyển sang tab **Format visual**:
   * Mục **Style presets**: Chọn kiểu **Alternating rows** (hàng xen kẽ màu để dễ đọc).
   * Mục **Column headers**: Đặt Font in đậm (Bold), nền màu xanh nhạt.
   * Mục **Subtotals**: Bật hoặc tắt Row subtotals tùy theo nhu cầu hiển thị tổng dòng.

---

### Bước 5: Tạo Biểu đồ tròn 1 (Pie Chart - Phân bổ theo Khu vực/Bang)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Pie chart**.
2. Kéo khung biểu đồ tròn đặt vào góc phía trên bên phải trang báo cáo (ngang hàng với Matrix).
3. Kéo thả các trường dữ liệu từ khung Data vào ô cấu hình:
   * **Vùng Legend (Chú giải):** Kéo thuộc tính `Transaction State` (hoặc `Tên Bang / Khu Vực`) thả vào ô **Legend**.
   * **Vùng Values (Giá trị):** Kéo thước đo `Total Fraud` (hoặc `Số lượng giao dịch rủi ro`) thả vào ô **Values**.
4. **Định dạng visual:**
   * Tại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập nội dung: `Tỷ lệ số vụ rủi ro theo Bang/Khu vực`. Đặt căn giữa (Center), chữ in đậm.
   * Mục **Detail labels**: Chọn **Label contents** là `Category, percent of total` (Hiển thị tên phân loại và phần trăm tổng thể).
   * Mục **Legend**: Đặt vị trí **Position** là `Right center` (ở giữa cạnh phải).

---

### Bước 6: Tạo Biểu đồ tròn 2 (Pie Chart - Phân bổ theo Loại hình giao dịch)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Pie chart** để thêm biểu đồ tròn thứ hai.
2. Kéo khung đặt ngay bên dưới Biểu đồ tròn 1.
3. Kéo thả các trường dữ liệu vào ô cấu hình:
   * **Vùng Legend:** Kéo thuộc tính `Transaction Type` (Loại hình giao dịch: POS, Online, ATM, Transfer...) thả vào ô **Legend**.
   * **Vùng Values:** Kéo thước đo `Total Amount Fraud` (hoặc `Total Fraud Amount`) thả vào ô **Values**.
4. **Định dạng visual:**
   * Tại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập nội dung: `Tỷ lệ tổn thất số tiền theo Loại hình giao dịch`. Căn giữa, in đậm.
   * Mục **Detail labels**: Chọn **Label contents** là `Category, percent of total`.
   * Mục **Legend**: Đặt vị trí là `Bottom center` hoặc `Right center`.

---

### Bước 7: Tạo Biểu đồ cột phân cụm (Clustered Column Chart)
Biểu đồ so sánh tương quan số lượng rủi ro giữa các loại hình giao dịch trên từng Bang.

1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Clustered column chart** (biểu đồ cột phân cụm đứng).
2. Kéo biểu đồ đặt ở nửa dưới trang Canvas, trải dài ở cạnh dưới của Matrix và Pie Charts.
3. Kéo thả các trường dữ liệu vào các ô cấu hình:
   * **Vùng X-axis (Trục hoành):** Kéo trường `Transaction Type` (Loại giao dịch) thả vào ô **X-axis**.
   * **Vùng Y-axis (Trục tung):** Kéo thước đo `Total Fraud` (Tổng số giao dịch rủi ro) thả vào ô **Y-axis**.
   * **Vùng Legend (Phân cụm cột):** Kéo trường `Transaction State` (Tiểu bang / Khu vực) thả vào ô **Legend**.
4. **Đổi tên hiển thị và định dạng:**
   * Nhấp chuột phải vào trường `Total Fraud` trên ô Y-axis -> chọn **Rename for this visual** -> đổi thành `Số lượng vụ việc`.
   * Tại tab **Format visual**:
   * Mục **Title**: Bật **On**, nhập: `So sánh số lượng giao dịch rủi ro theo Loại hình và Khu vực`. Căn giữa, in đậm.
   * Mục **Data labels**: Bật công tắc sang **On** để hiển thị con số chính xác trên đầu mỗi cột.
   * Mục **X-axis**: Đặt cỡ chữ 10 pt, bật tiêu đề trục.
   * Mục **Y-axis**: Đặt cỡ chữ 10 pt.

---

### Bước 8: Căn chỉnh bố cục tổng thể và kiểm tra tính tương tác
1. **Căn chỉnh vị trí (Align):** Giữ phím `Ctrl`, nhấp chọn lần lượt các biểu đồ -> trên thanh Ribbon chuyển sang tab **Format** -> chọn **Align** -> chọn **Distribute horizontally** hoặc **Align top** để các khung biểu đồ thẳng hàng, ngay ngắn và cân đối.
2. **Kiểm tra tính tương tác (Cross-filtering):**
   * Nhấp chuột vào một lát cắt (slice) trên Pie Chart (ví dụ: Bang New York hoặc Loại hình Online) -> Kiểm tra xem bảng Matrix và biểu đồ Clustered Column Chart có tự động làm nổi bật (highlight) hoặc lọc dữ liệu tương ứng hay không.
   * Nhấp chuột lần nữa vào lát cắt để bỏ chọn.
3. Vào menu **File** -> chọn **Save As** -> lưu tệp báo cáo với tên `IS217_Bao_Bieu_PowerBI.pbix`.
