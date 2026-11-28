# HƯỚNG DẪN SSAS - PHẦN 1: KHỞI TẠO PROJECT & KẾT NỐI DATA SOURCE

---

## 1. MỤC TIÊU & PHẠM VI

Tài liệu hướng dẫn khởi tạo dự án **SQL Server Analysis Services (SSAS Multidimensional Project)** trong **Visual Studio 2022** và thiết lập kết nối **Data Source** tới cơ sở dữ liệu kho dữ liệu **`DW_Football_Transfermarkt`** đã được nạp từ quy trình SSIS (Chương 2).

| Thành phần | Giá trị chuẩn hóa |
| :--- | :--- |
| **SQL Server Database (nguồn)** | `DW_Football_Transfermarkt` |
| **SSAS Project / Database Name** | `SSAS_Football_Transfermarkt` |
| **Data Source** | `DW_Football_Transfermarkt.ds` |
| **Data Source View** | `DW_Football_Transfermarkt.dsv` |
| **OLAP Cube** | `DW Football Transfermarkt` |

> **Nâng cấp từ bản cũ (`Bài tập (1).docx`)?** Xem lộ trình chỉnh sửa chi tiết từng bước cho SSAS và 15 câu truy vấn MDX tại [ke_hoach_chinh_sua_ssas_mdx.md](./ke_hoach_chinh_sua_ssas_mdx.md).

---

## 2. QUY TRÌNH THỰC HIỆN TỪNG BƯỚC

### Bước 1: Khởi tạo Project SSAS mới trong Visual Studio 2022
1. Mở **Visual Studio 2022** (đã cài tiện ích *Microsoft Analysis Services Projects*).
2. Chọn **Create a new project**.
3. Trong ô tìm kiếm, nhập `Analysis Services`.
4. Chọn mẫu: **Analysis Services Multidimensional Project** (hoặc *Analysis Services Multidimensional and Data Mining Project* tùy phiên bản SSDT).
5. Nhấn **Next**.
6. Điền thông tin cấu hình tại màn hình **Configure your new project**:
   - **Project name**: `SSAS_Football_Transfermarkt`
   - **Location**: `D:\Kho_du_lieu_OLAP`
   - Tích chọn *Place solution and project in the same directory*.
7. Nhấn **Create** để tạo dự án. Kiểm tra **Solution Explorer** đã hiển thị đầy đủ các thư mục `Data Sources`, `Data Source Views`, `Cubes`, `Dimensions`, `Roles`…

---

### Bước 2: Khởi tạo Data Source kết nối `DW_Football_Transfermarkt`
1. Trong **Solution Explorer**, nhấp chuột phải vào thư mục **Data Sources** $\rightarrow$ chọn **New Data Source...**
2. Cửa sổ **Data Source Wizard** hiển thị $\rightarrow$ nhấn **Next >**.
3. Tại màn hình **Select how to define the connection**:
   - Chọn **Create a data source based on an existing or new connection**.
   - Nhấn nút **New...** để mở hộp thoại **Connection Manager**.
4. Thiết lập tham số kết nối SQL Server:
   - **Provider**: `Native OLE DB\Microsoft OLE DB Driver for SQL Server` (hoặc `SQL Server Native Client`).
   - **Server name**: `localhost` (hoặc tên instance SQL Server cục bộ chứa kho dữ liệu thực hành).
   - **Authentication**: chọn `Use Windows Authentication`.
   - **Select or enter a database name**: chọn **`DW_Football_Transfermarkt`**.
   - Nhấn **Test Connection** để xác nhận `Test connection succeeded`, sau đó nhấn **OK**.
5. Quay lại Wizard, chọn kết nối vừa tạo $\rightarrow$ nhấn **Next >**.

---

### Bước 3: Cấu hình Impersonation Information & hoàn tất
1. Tại màn hình **Impersonation Information**:
   - Chọn **Use the service account** để dịch vụ SSAS dùng tài khoản dịch vụ đọc dữ liệu từ SQL Server lúc Process (hoặc dùng Windows credentials có quyền `db_datareader` trên `DW_Football_Transfermarkt`).
2. Nhấn **Next >**.
3. Đặt **Data source name**: **`DW_Football_Transfermarkt`**, kiểm tra chuỗi kết nối ở khung **Preview** và nhấn **Finish**.
4. Kiểm tra tệp `DW_Football_Transfermarkt.ds` đã xuất hiện trong thư mục **Data Sources** của Solution Explorer.

---

## 3. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Project `SSAS_Football_Transfermarkt` được tạo bằng mẫu Multidimensional Project trong Visual Studio 2022.
- [x] Data Source `DW_Football_Transfermarkt.ds` kiểm tra `Test Connection` thành công tới SQL Server.
- [x] Chuỗi kết nối trỏ đúng cơ sở dữ liệu `DW_Football_Transfermarkt` (khớp Chương 2).
