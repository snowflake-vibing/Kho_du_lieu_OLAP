# 4.1 Chuẩn bị công cụ và thiết lập kết nối báo biểu

Tài liệu này hướng dẫn chi tiết quy trình chuẩn bị môi trường và thiết lập kết nối dữ liệu từ kho dữ liệu (Data Warehouse / SSAS / SQL Server) đến hai nền tảng lập báo biểu trực quan: **Power BI Desktop** và **Google Data Studio (Looker Studio)** theo chuẩn môn học IS217 - Kho dữ liệu và OLAP.

---

## 4.1.1 Chuẩn bị và kết nối công cụ Power BI Desktop

Power BI Desktop là công cụ phân tích và trực quan hóa dữ liệu kinh doanh của Microsoft, hỗ trợ kết nối trực tiếp (Live Connection) tới khối đa chiều SQL Server Analysis Services (SSAS Cube) để tận dụng toàn bộ cấu trúc Dimension, Hierarchy, và Calculated Measures đã xây dựng ở các chương trước.

### Bước 1: Cài đặt phần mềm Power BI Desktop
1. Trên thanh tác vụ Windows (Taskbar) hoặc phím `Windows`, mở ứng dụng **Microsoft Store**.
2. Tại thanh tìm kiếm ở phía trên, nhập từ khóa `Power BI Desktop` và nhấn phím `Enter`.
3. Trong kết quả tìm kiếm, nhấp chuột chọn ứng dụng chính thức **Power BI Desktop** do *Microsoft Corporation* phát hành.
4. Nhấp nút **Install** (hoặc **Get**) để hệ thống tự động tải về và cài đặt phiên bản mới nhất.
5. Sau khi quá trình cài đặt hoàn tất, nhấp nút **Open** để khởi động Power BI Desktop.

---

### Bước 2: Thiết lập kết nối Live Connection tới SQL Server Analysis Services (SSAS)
1. Tại màn hình làm việc chính của Power BI Desktop, quan sát thanh công cụ **Home** trên dải Ribbon ở mép trên màn hình.
2. Nhấp chuột vào biểu tượng **Get data** (hoặc nhấp mũi tên xổ xuống tại mục Get data).
3. Trong menu danh sách các nguồn dữ liệu xuất hiện, nhấp chọn **SQL Server Analysis Services database** (hoặc chọn *More...* -> danh mục *Database* -> chọn *SQL Server Analysis Services database* -> nhấp **Connect**).
4. Hộp thoại **SQL Server Analysis Services database** xuất hiện:
   * **Server:** Nhập tên máy chủ SSAS của bạn (ví dụ: `localhost` hoặc tên máy tính cục bộ như `DESKTOP-ABCXYZ` hoặc `.` nếu là default instance).
   * **Database (optional):** Nhập chính xác tên cơ sở dữ liệu SSAS đã deploy từ Visual Studio (ví dụ: `DW Football SSAS` hoặc `Bank_Fraud_SSAS`).
   * **Phương thức kết nối:** Tích chọn tùy chọn **Connect live** (Kết nối trực tiếp tới mô hình dữ liệu đa chiều SSAS thay vì Import dữ liệu, giúp báo cáo tự động cập nhật và giữ nguyên tính toán Cube).
5. Nhấp nút **OK** để xác nhận kết nối.

---

### Bước 3: Lựa chọn Cube và nạp cấu trúc dữ liệu
1. Cửa sổ **Navigator** hiển thị danh sách các khối Cube có trong Database SSAS đã chọn.
2. Tích chọn khối Cube phân tích chính (ví dụ: `[DW Football Transfermarkt]` hoặc `[Bank Transaction Fraud Cube]`).
3. Khung bên phải sẽ hiển thị cây đối tượng gồm danh sách các thước đo (**Measures**) và các chiều phân tích (**Dimensions**) cùng các phân cấp phân tích (**Hierarchies**).
4. Nhấp nút **Load** (hoặc nút **OK**) ở góc dưới cùng bên phải.
5. Power BI Desktop kết nối thành công và chuyển về giao diện Report Canvas. Khung **Data** (hoặc **Fields**) ở mép phải màn hình sẽ xuất hiện đầy đủ các Dimension và Measure sẵn sàng để kéo thả tạo báo cáo.

---

## 4.1.2 Chuẩn bị và trích xuất dữ liệu cho Google Data Studio (Looker Studio)

Google Data Studio (nay là Looker Studio) là nền tảng báo cáo trực tuyến trên nền web của Google. Do hoạt động trên đám mây, Looker Studio cần kết nối dữ liệu thông qua tệp tin `.csv` được trích xuất từ cơ sở dữ liệu kho hoặc kết nối Cloud SQL.

### Bước 1: Kết nối SQL Server Database Engine
1. Mở phần mềm **SQL Server Management Studio (SSMS)**.
2. Trong cửa sổ **Connect to Server**:
   * **Server type:** Chọn `Database Engine`.
   * **Server name:** Chọn hoặc nhập tên máy chủ SQL Server cục bộ.
   * **Authentication:** Chọn `Windows Authentication` (hoặc `SQL Server Authentication`).
3. Nhấp nút **Connect**.

---

### Bước 2: Soạn thảo và thực thi câu lệnh SQL trích xuất dữ liệu phẳng
1. Trên thanh công cụ của SSMS, nhấp nút **New Query** (hoặc nhấn tổ hợp phím `Ctrl + N`).
2. Tại hộp thoại chọn cơ sở dữ liệu ở góc trên bên trái, chọn đúng Database kho dữ liệu (Data Warehouse).
3. Viết câu lệnh truy vấn `SELECT` kết hợp bảng Fact và các bảng Dimension bằng mệnh đề `INNER JOIN` để tạo bảng dữ liệu phân tích phẳng chứa đầy đủ các thuộc tính và thước đo cần lập báo biểu:

```sql
-- Ví dụ câu truy vấn trích xuất dữ liệu giao dịch ngân hàng / kho dữ liệu:
SELECT 
    F.Transaction_ID,
    F.Transaction_Date,
    F.Transaction_Time,
    F.Transaction_Amount,
    F.Is_Fraud,
    TT.Transaction_Type_Name,
    M.Merchant_Name,
    M.Merchant_Category,
    L.Transaction_City,
    L.Transaction_State,
    D.Device_Type_Name,
    C.Customer_Age,
    C.Customer_Gender
FROM FACT_TRANSACTION F
INNER JOIN DIM_TRANSACTION_TYPE TT ON F.Transaction_Type_ID = TT.Transaction_Type_ID
INNER JOIN DIM_MERCHANT M ON F.Merchant_ID = M.Merchant_ID
INNER JOIN DIM_LOCATION L ON F.Location_ID = L.Location_ID
INNER JOIN DIM_DEVICE D ON F.Device_ID = D.Device_ID
INNER JOIN DIM_CUSTOMER C ON F.Customer_ID = C.Customer_ID;
```

*(Hoặc đối với dữ liệu Bóng đá Football Transfermarkt, thực hiện JOIN giữa `FACT_Player_Match_Perf` với `DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`).*

4. Nhấp nút **Execute** (hoặc nhấn phím `F5`) để thực thi câu lệnh truy vấn.

---

### Bước 3: Lưu kết quả truy vấn dưới định dạng tệp CSV
1. Khi câu lệnh thực thi xong, kết quả hiển thị tại khung **Results** ở phía dưới.
2. Nhấp chuột phải vào ô góc trên cùng bên trái của lưới kết quả (ô vuông giao giữa tiêu đề dòng và tiêu đề cột).
3. Trong menu ngữ cảnh xuất hiện, nhấp chuột chọn **Save Results As...**.
4. Trong hộp thoại lưu tệp:
   * **Save in:** Chọn thư mục lưu trữ an toàn (ví dụ: `D:\Kho_du_lieu_OLAP\data\`).
   * **File name:** Đặt tên tệp dữ liệu (ví dụ: `Report_Extracted_Data.csv`).
   * **Save as type:** Đảm bảo chọn định dạng **CSV (Comma delimited) (*.csv)**.
5. Nhấp nút **Save** để hoàn tất việc xuất tệp.
6. Mở thư mục chứa tệp, nhấp đúp để mở file bằng Notepad hoặc Excel nhằm kiểm tra các dòng dữ liệu và hàng tiêu đề không bị lỗi font hoặc lỗi ký tự phân cách.

---

### Bước 4: Tải dữ liệu lên Google Data Studio (Looker Studio)
1. Khởi động trình duyệt web (Google Chrome hoặc Microsoft Edge), truy cập vào đường dẫn:
   `https://lookerstudio.google.com/`
2. Đăng nhập bằng tài khoản Google.
3. Tại giao diện trang chủ của Looker Studio, nhấp chuột vào nút **Báo cáo trống** (Blank Report) có biểu tượng dấu cộng `+`.
4. Hộp thoại **Thêm dữ liệu vào báo cáo** (Add data to report) tự động xuất hiện:
   * Trong danh sách các trình kết nối của Google (Google Connectors), tìm và nhấp chọn **Tải tệp lên** (File Upload).
   * Nhấp chuột vào nút **Nhấp để tải lên** (Click to upload) và điều hướng đến tệp `.csv` vừa xuất ở Bước 3 (`Report_Extracted_Data.csv`).
   * Chờ hệ thống xử lý tệp cho đến khi trạng thái chuyển sang màu xanh **Đã tải lên** (Uploaded).
5. Nhấp nút **Thêm** (Add) ở góc dưới cùng bên phải.
6. Khi hộp thoại xác nhận quyền hiển thị, nhấp chọn **Thêm vào báo cáo** (Add to Report) để hoàn tất.
7. Giao diện thiết kế của Looker Studio xuất hiện với trang vẽ báo cáo trống và thanh công cụ thuộc tính ở bên phải.
