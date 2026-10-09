# HƯỚNG DẪN SSAS - PHẦN 1: KHỞI TẠO PROJECT & KẾT NỐI DATA SOURCE

---

## 1. MỤC TIÊU HUẤN LUYỆN & CẤU HÌNH
Tài liệu hướng dẫn khởi tạo dự án **SQL Server Analysis Services (SSAS Multidimensional Project)** trong Visual Studio (SSDT) và thiết lập kết nối **Data Source** tới cơ sở dữ liệu Kho dữ liệu `DW_Football_Analytics`.

---

## 2. QUY TRÌNH THỰC HIỆN TỪNG BƯỚC

### Bước 1: Khởi tạo Project SSAS mới trong Visual Studio
1. Mở **Visual Studio 2022 / SSDT**.
2. Chọn **Create a new project**.
3. Trong ô tìm kiếm, nhập `Analysis Services Multidimensional`.
4. Chọn mẫu project: **Analysis Services Multidimensional and Data Mining Project**.
5. Nhấn **Next**.
6. Điền thông tin cấu hình:
   - **Project name**: `DW_Football_SSAS`
   - **Location**: `D:\Kho_du_lieu_OLAP`
   - Check vào ô *Place solution and project in the same directory*.
7. Nhấn **Create** để tạo dự án.

---

### Bước 2: Khởi tạo Data Source kết nối Data Warehouse
1. Trong cửa sổ **Solution Explorer**, nhấp chuột phải vào thư mục **Data Sources** $\rightarrow$ chọn **New Data Source...**
2. Cửa sổ **Data Source Wizard** hiển thị $\rightarrow$ Nhấn **Next >**.
3. Tại màn hình **Select how to define the connection**:
   - Chọn **Create a data source based on an existing or new connection**.
   - Nhấn nút **New...** để mở hộp thoại **Connection Manager**.
4. Thiết lập tham số kết nối SQL Server:
   - **Provider**: `Native OLE DB\Microsoft OLE DB Driver for SQL Server` (hoặc `SQL Server Native Client 11.0`).
   - **Server name**: `localhost` (hoặc tên máy tính chứa SQL Server, ví dụ: `DESKTOP-SQLSERVER`).
   - **Authentication**: Chọn `Use Windows Authentication` (hoặc `Use SQL Server Authentication` nhập username/password SQL Server).
   - **Select or enter a database name**: Chọn cơ sở dữ liệu **`DW_Football_Analytics`**.
   - Nhấn **Test Connection** để đảm bảo kết nối thành công (`Test connection succeeded`).
   - Nhấn **OK**.
5. Quay lại cửa sổ Wizard, chọn kết nối vừa tạo $\rightarrow$ Nhấn **Next >**.

---

### Bước 3: Cấu hình Impersonation Information (Xác thực tài khoản)
1. Tại màn hình **Impersonation Information**:
   - Chọn tùy chọn **Use the service account** (sử dụng tài khoản dịch vụ của SSAS Engine) hoặc **Use credentials of the current user**.
2. Nhấn **Next >**.
3. Nhập tên Data Source Name: **`DS_DW_Football_Analytics`**.
4. Nhấn **Finish** để hoàn tất wizard.
5. Kiểm tra file `DS_DW_Football_Analytics.ds` đã xuất hiện dưới mục **Data Sources** trong Solution Explorer.

---

## 3. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Project `DW_Football_SSAS` tạo thành công trong Visual Studio.
- [x] Data Source `DS_DW_Football_Analytics` được tạo và Test Connection thành công.
- [x] Chuỗi kết nối chỉ định chính xác database `DW_Football_Analytics`.
