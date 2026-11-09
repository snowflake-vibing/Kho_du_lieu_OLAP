# 4.1 Chuẩn bị công cụ và thiết lập kết nối báo biểu Kho dữ liệu Bóng đá Châu Âu

Tài liệu này hướng dẫn chi tiết quy trình chuẩn bị môi trường và thiết lập kết nối dữ liệu từ Kho dữ liệu Bóng đá Châu Âu (Data Warehouse / SSAS / SQL Server) đến hai nền tảng lập báo biểu trực quan: **Power BI Desktop** và **Google Data Studio (Looker Studio)** theo chuẩn môn học IS217 - Kho dữ liệu và OLAP.

---

## 4.1.1 Chuẩn bị và kết nối công cụ Power BI Desktop

Power BI Desktop là công cụ phân tích và trực quan hóa dữ liệu kinh doanh của Microsoft, hỗ trợ kết nối trực tiếp (Live Connection) tới khối đa chiều SQL Server Analysis Services (**SSAS Cube: `[DW Football Transfermarkt]`**) để khai thác toàn bộ cấu trúc các chiều phân tích (`DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`) và các Calculated Measures (như `QoQ Goals Growth`, `Mins Per Goal`, `Goal Contributions`) đã được xây dựng từ các chương trước.

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
   * **Measures (Thước đo):** `Goals`, `Assists`, `Goal Contributions`, `Minutes Played`, `Yellow Cards`, `Red Cards`, `Is Starter`, `Stadium Seats`, `QoQ Goals Growth`, v.v.
   * **DIM Player:** `Player Name`, `Age`, `Main Position`, `Sub Position`, `Foot`, `Height In Cm`, `Country Of Citizenship`.
   * **DIM Club:** `Club Name`, `Stadium Name`, `Stadium Seats`, `Coach Name`, `Squad Size`.
   * **DIM Competition:** `Competition Name`, `Country Name`, `Competition Type`.
   * **DIM Game:** `Round`, `Home Club Goals`, `Away Club Goals`, `Stadium`.
   * **DIM Time:** `Hierarchy` (`Year` -> `Quarter` -> `Month` -> `Day`), `Season`, `Day Of Week`, `Is Weekend`.
4. Nhấp nút **Load** (hoặc nút **OK**) ở góc dưới cùng bên phải.
5. Power BI Desktop kết nối thành công và chuyển về giao diện Report Canvas. Khung **Data** ở mép phải màn hình sẽ hiển thị đầy đủ các Dimension và Measure sẵn sàng để kéo thả tạo các trang Dashboard.

---

## 4.1.2 Chuẩn bị và trích xuất dữ liệu cho Google Data Studio (Looker Studio)

Google Data Studio (nay là Looker Studio) là nền tảng báo cáo trực tuyến trên nền web của Google. Do hoạt động trên đám mây, Looker Studio cần kết nối dữ liệu thông qua tệp tin `.csv` được trích xuất từ cơ sở dữ liệu kho hoặc kết nối Cloud SQL.

### Bước 1: Kết nối SQL Server Database Engine
1. Mở phần mềm **SQL Server Management Studio (SSMS)**.
2. Trong cửa sổ **Connect to Server**:
   * **Server type:** Chọn `Database Engine`.
   * **Server name:** Chọn hoặc nhập tên máy chủ SQL Server cục bộ.
   * **Authentication:** Chọn `Windows Authentication`.
3. Nhấp nút **Connect**.

---

### Bước 2: Soạn thảo và thực thi câu lệnh SQL trích xuất dữ liệu bóng đá phẳng
1. Trên thanh công cụ của SSMS, nhấp nút **New Query** (hoặc nhấn tổ hợp phím `Ctrl + N`).
2. Tại hộp thoại chọn cơ sở dữ liệu ở góc trên bên trái, chọn đúng Database kho dữ liệu: `DW_Football`.
3. Viết câu lệnh truy vấn `SELECT` kết hợp bảng Fact `FACT_Player_Match_Perf` và các bảng Dimension bằng mệnh đề `INNER JOIN` để tạo bảng dữ liệu phân tích bóng đá phẳng chứa đầy đủ các thuộc tính và thước đo:

```sql
-- ==============================================================================
-- TRÍCH XUẤT DỮ LIỆU PHẲNG PHỤC VỤ LẬP BÁO BIỂU LOOKER STUDIO
-- CSDL: DW_Football | Kho dữ liệu Bóng đá Châu Âu
-- ==============================================================================
SELECT 
    F.Appearance_ID,
    -- Thông tin Cầu thủ
    P.Player_ID,
    P.Player_Name,
    P.Age,
    P.Main_Position,
    P.Sub_Position,
    P.Foot,
    P.Height_In_Cm,
    P.Country_Of_Citizenship AS Player_Country,
    -- Thông tin Câu lạc bộ
    C.Club_ID,
    C.Club_Name,
    C.Stadium_Name,
    C.Stadium_Seats,
    C.Coach_Name,
    C.Squad_Size,
    -- Thông tin Giải đấu
    Comp.Competition_ID,
    Comp.Competition_Name,
    Comp.Country_Name AS Competition_Country,
    Comp.Competition_Type,
    -- Thông tin Thời gian
    T.Time_ID,
    T.Full_Date,
    T.Year,
    T.Quarter,
    T.Month,
    T.Day,
    T.Season,
    -- Thước đo hiệu suất thi đấu
    F.Minutes_Played,
    F.Goals,
    F.Assists,
    F.Goal_Contributions,
    F.Yellow_Cards,
    F.Red_Cards,
    F.Is_Starter,
    F.Is_Home_Game
FROM FACT_Player_Match_Perf F
INNER JOIN DIM_Player P ON F.Player_ID = P.Player_ID
INNER JOIN DIM_Club C ON F.Club_ID = C.Club_ID
INNER JOIN DIM_Competition Comp ON F.Competition_ID = Comp.Competition_ID
INNER JOIN DIM_Time T ON F.Time_ID = T.Time_ID;
```

4. Nhấp nút **Execute** (hoặc nhấn phím `F5`) để thực thi câu lệnh truy vấn.

---

### Bước 3: Lưu kết quả truy vấn dưới định dạng tệp CSV
1. Khi câu lệnh thực thi xong, kết quả hiển thị tại khung **Results** ở phía dưới.
2. Nhấp chuột phải vào ô góc trên cùng bên trái của lưới kết quả (ô vuông giao giữa tiêu đề dòng và tiêu đề cột).
3. Trong menu ngữ cảnh xuất hiện, nhấp chuột chọn **Save Results As...**.
4. Trong hộp thoại lưu tệp:
   * **Save in:** Chọn thư mục lưu trữ (ví dụ: `D:\Kho_du_lieu_OLAP\football\cleaned_data\`).
   * **File name:** Đặt tên tệp dữ liệu: `Football_Report_Data.csv`.
   * **Save as type:** Đảm bảo chọn định dạng **CSV (Comma delimited) (*.csv)**.
5. Nhấp nút **Save** để hoàn tất việc xuất tệp.
6. Mở thư mục chứa tệp, kiểm tra dữ liệu để đảm bảo file sạch và không bị lỗi ký tự.

---

### Bước 4: Tải dữ liệu lên Google Data Studio (Looker Studio)
1. Khởi động trình duyệt web (Google Chrome hoặc Microsoft Edge), truy cập vào đường dẫn:
   `https://lookerstudio.google.com/`
2. Đăng nhập bằng tài khoản Google.
3. Tại giao diện trang chủ của Looker Studio, nhấp chuột vào nút **Báo cáo trống** (Blank Report) có biểu tượng dấu cộng `+`.
4. Hộp thoại **Thêm dữ liệu vào báo cáo** (Add data to report) tự động xuất hiện:
   * Trong danh sách các trình kết nối của Google (Google Connectors), tìm và nhấp chọn **Tải tệp lên** (File Upload).
   * Nhấp chuột vào nút **Nhấp để tải lên** (Click to upload) và điều hướng đến tệp `.csv` vừa xuất ở Bước 3 (`Football_Report_Data.csv`).
   * Chờ hệ thống tải lên và xử lý tệp cho đến khi trạng thái chuyển sang màu xanh **Đã tải lên** (Uploaded).
5. Nhấp nút **Thêm** (Add) ở góc dưới cùng bên phải.
6. Khi hộp thoại xác nhận quyền hiển thị, nhấp chọn **Thêm vào báo cáo** (Add to Report) để hoàn tất.
7. Giao diện thiết kế của Looker Studio xuất hiện sẵn sàng cho việc thiết kế các báo biểu trực quan hóa bóng đá.
