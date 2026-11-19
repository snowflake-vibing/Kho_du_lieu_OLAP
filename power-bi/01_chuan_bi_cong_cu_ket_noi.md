# 4.1 Chuẩn bị công cụ và thiết lập kết nối báo biểu Kho dữ liệu Bóng đá Châu Âu

Tài liệu này hướng dẫn chi tiết quy trình chuẩn bị môi trường và thiết lập kết nối dữ liệu từ Kho dữ liệu Bóng đá Châu Âu (Data Warehouse / SSAS / SQL Server) đến hai nền tảng lập báo biểu trực quan: **Power BI Desktop** và **Google Data Studio (Looker Studio)** theo chuẩn môn học IS217 - Kho dữ liệu và OLAP.

---

## 4.1.1 Chuẩn bị và kết nối công cụ Power BI Desktop

Power BI Desktop là công cụ phân tích và trực quan hóa dữ liệu kinh doanh của Microsoft, hỗ trợ kết nối trực tiếp (Live Connection) tới khối đa chiều SQL Server Analysis Services (**SSAS Cube: `[DW Football Transfermarkt]`**) để khai thác toàn bộ cấu trúc các chiều phân tích (`DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`) và các Calculated Measures (như `QoQ Goals Growth`, `Avg Minutes Played`, `Goal Contributions`, `Distinct Matches Played`, `Stadium Capacity Cleaned`) đã được xây dựng từ các chương trước.

### Bước 1: Cài đặt phần mềm Power BI Desktop
1. Trên thanh tác vụ Windows (Taskbar) hoặc nhấn phím `Windows`, mở ứng dụng **Microsoft Store**.
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
   * **Server:** Nhập `localhost` (hoặc `.` hoặc tên máy tính: `DESKTOP-9B88R8P`).
   * **Database (optional):** Nhập `SSAS_Football_Transfermarkt` (hoặc `DW Football SSAS`).
   * **Phương thức kết nối:** Tích chọn tùy chọn **Connect live** (Kết nối trực tiếp tới mô hình dữ liệu đa chiều SSAS thay vì Import dữ liệu, giúp báo cáo tự động cập nhật và giữ nguyên tính toán Cube).
5. Nhấp nút **OK** để xác nhận kết nối.

---

### Bước 3: Lựa chọn Cube và nạp cấu trúc dữ liệu bóng đá
1. Cửa sổ **Navigator** hiển thị danh sách các khối Cube có trong Database SSAS đã chọn.
2. Tích chọn khối Cube phân tích chính: **`[DW Football Transfermarkt]`**.
3. Khung bên phải sẽ hiển thị toàn bộ cây đối tượng của kho dữ liệu bóng đá:
   * **Measures (Thước đo):** `Goals`, `Assists`, `Goal Contributions`, `Minutes Played`, `Yellow Cards`, `Red Cards`, `Distinct Matches Played`, `FACT Player Match Perf Count`, `QoQ Goals Growth`, v.v.
   * **DIM Player:** `Player Name`, `Age`, `Main Position`, `Sub Position`, `Foot`, `Height In Cm`, `Country Of Citizenship`.
   * **DIM Club:** `Club Name`, `Stadium Name`, `Stadium Seats`, `Coach Name`, `Squad Size`.
   * **DIM Competition:** `Competition Name`, `Country Name`, `Competition Type`.
   * **DIM Game:** `Round`, `Home Club Goals`, `Away Club Goals`, `Stadium`.
   * **DIM Time:** `Hierarchy` (`Year` -> `Quarter` -> `Month` -> `Day`), `Season`, `Day Of Week`, `Is Weekend`.
4. Nhấp nút **Load** (hoặc nút **OK**) ở góc dưới cùng bên phải.
5. Power BI Desktop kết nối thành công và chuyển về giao diện Report Canvas. Khung **Data** ở mép phải màn hình sẽ hiển thị đầy đủ các Dimension và Measure sẵn sàng để kéo thả tạo các trang Dashboard.

---

## 4.1.2 Chuẩn bị và trích xuất dữ liệu cho Google Data Studio (Looker Studio)

Google Data Studio (nay là **Looker Studio**) là nền tảng báo cáo trực tuyến trên đám mây của Google (`https://lookerstudio.google.com/`). Vì chạy trên cloud nên Looker Studio **không thể kết nối trực tiếp vào SQL Server `localhost`** trên máy cá nhân. Để tách biệt hoàn toàn với kho dữ liệu SSAS (`DW_Football_Transfermarkt`) và loại bỏ thao tác ghép bảng phức tạp trên web, dự án sử dụng một **Database SQL Server riêng biệt** là **`DW_Football_LookerStudio`** được khởi tạo từ script [setup_dw_football_looker_studio.sql](file:///d:/Kho_du_lieu_OLAP/warehouse-database/setup_dw_football_looker_studio.sql).

### Bước 1: Khởi tạo (hoặc làm mới) Database riêng `DW_Football_LookerStudio`
1. Mở phần mềm **SQL Server Management Studio (SSMS)** và kết nối tới `localhost` (Windows Authentication).
2. Mở tệp [setup_dw_football_looker_studio.sql](file:///d:/Kho_du_lieu_OLAP/warehouse-database/setup_dw_football_looker_studio.sql) (hoặc chạy bằng `sqlcmd -S localhost -E -C -f 65001 -i warehouse-database\setup_dw_football_looker_studio.sql`) để tạo Database **`DW_Football_LookerStudio`** gồm 3 bảng chuẩn hóa sẵn cho Looker Studio:
   * **`dbo.Looker_Football_Flat`** (`210,747` dòng): Bảng phẳng đầy đủ từng lượt ra sân, đã `JOIN` sẵn 5 bảng Dimension + `Opponent_Club_Name`, chuẩn hóa lại cờ `Is_Starter`/`Is_Home_Game` về `0/1` và tính sẵn các cột `Club_Country`, `Match_Venue`, `Lineup_Role`, `Appearances`.
   * **`dbo.Looker_Player_Season_Summary`** (`13,493` dòng): Bảng tổng hợp theo Cầu thủ × CLB × Giải đấu × Mùa giải (nhẹ, tiện đưa lên Google Sheets).
   * **`dbo.Looker_Club_Matchup_Summary`** (`6,827` dòng): Bảng tổng hợp đối đầu CLB × Đối thủ × Mùa giải.

---

### Bước 2: Truy vấn dữ liệu từ `DW_Football_LookerStudio`
1. Trong SSMS, mở **New Query** (`Ctrl + N`), chọn Database **`DW_Football_LookerStudio`**.
2. Chạy câu lệnh đơn giản lấy toàn bộ bảng phẳng đã chuẩn bị sẵn:

```sql
SELECT * FROM dbo.Looker_Football_Flat;
```

*(Nếu cần xuất lại nhanh bằng Python giữ chuẩn UTF-8 cho tên cầu thủ châu Âu và tiếng Việt không dấu/có dấu, có thể đọc trực tiếp từ bảng `DW_Football_LookerStudio.dbo.Looker_Football_Flat` ra tệp `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`.)*

---

### Bước 3: Kiểm tra tệp CSV đầu ra
* Tệp dữ liệu đã được xuất sẵn tại: `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv` (chuẩn **UTF-8**, `210,747` dòng dữ liệu, nằm dưới giới hạn `100 MB` của trình tải lên Looker Studio).

---

### Bước 4: Tải dữ liệu lên Google Data Studio (Looker Studio)
1. Khởi động trình duyệt web (Google Chrome hoặc Microsoft Edge), truy cập: `https://lookerstudio.google.com/`.
2. Đăng nhập bằng tài khoản Google.
3. Tại giao diện trang chủ, nhấp nút **+ Create** (Tạo) $\rightarrow$ **Report** (hoặc **Blank Report / Báo cáo trống**).
4. Hộp thoại **Add data to report** (Thêm dữ liệu vào báo cáo) tự động hiện ra:
   * Trong danh sách **Google Connectors**, tìm và chọn **File Upload** (Tải tệp lên).
   * Nhấp **Click to upload files** (Nhấp để tải tệp lên) và chọn tệp `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`.
   * Đợi trạng thái chuyển sang màu xanh **Uploaded** (Đã tải lên) *(thường mất 15–30 giây vì file ~74 MB)*.
5. Nhấp nút **Add** (Thêm) ở góc dưới bên phải $\rightarrow$ chọn **Add to report** (Thêm vào báo cáo).
6. Giao diện thiết kế Looker Studio mở ra với bảng nguồn **`Football_Report_Data.csv`** sẵn sàng ở cột **Data** bên phải.
