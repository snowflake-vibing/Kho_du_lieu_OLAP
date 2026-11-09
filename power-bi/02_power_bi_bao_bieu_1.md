# 4.2.1 Báo biểu 1: Phân tích Hiệu suất Ghi bàn và Đóng góp Kiến tạo của Cầu thủ (Player Performance & Goal Contributions)

Tài liệu này hướng dẫn chi tiết từng thao tác click chuột để thiết kế hoàn chỉnh **Báo biểu 1 (Dashboard 1)** trên phần mềm **Power BI Desktop**, kết nối trực tiếp (Live Connection) với khối dữ liệu SSAS `[DW Football Transfermarkt]`.

---

## 1. Mục tiêu và nội dung phân tích
* **Nội dung:** Giám sát và đánh giá phong độ, hiệu suất ghi bàn (`Goals`), năng lực kiến tạo (`Assists`), tổng mức đóng góp bàn thắng (`Goal Contributions = Goals + Assists`) và thời lượng thi đấu (`Minutes Played`) của các cầu thủ theo vị trí thi đấu, câu lạc bộ và giải đấu qua các mùa giải.
* **Đối tượng theo dõi:**
  * Khối KPI Cards hiển thị tổng quan 4 chỉ số cốt lõi: Tổng Bàn Thắng, Tổng Kiến Tạo, Tổng G+A và Hiệu suất Số phút / Bàn thắng (`Mins Per Goal`).
  * Biểu đồ thanh ngang (Clustered Bar Chart): Top 10 Cầu thủ ghi nhiều bàn thắng nhất Châu Âu.
  * Biểu đồ vành khăn (Donut Chart): Cơ cấu đóng góp bàn thắng phân bổ theo Vị trí thi đấu chính (`Main_Position`: Attack, Midfield, Defender).
  * Biểu đồ kết hợp cột và đường (Line and Clustered Column Chart): Xu hướng bàn thắng và kiến tạo qua các mùa giải (`Season`) và các quý trong năm (`Quarter`).
  * Bảng ma trận đa cấp (Matrix Visual): Bảng tra cứu phong độ chi tiết từng cầu thủ theo Câu lạc bộ và Vị trí.
  * Hệ thống bộ lọc cắt lát (Slicers): Mùa giải (`Season`), Giải đấu (`Competition_Name`), Vị trí thi đấu (`Main_Position`).

---

## 2. Hướng dẫn các bước thiết lập chi tiết trên giao diện Power BI

### Bước 1: Khởi động Power BI Desktop và Thiết lập Kết nối Live Connection tới SSAS Cube
1. Khởi động phần mềm **Power BI Desktop** từ màn hình Desktop, thanh Taskbar hoặc Menu Start của Windows.
2. Tại màn hình khởi động (Splash screen/Welcome screen), nhấp chuột vào dấu **X** ở góc trên bên phải hộp thoại chào mừng để đóng lại và đi vào giao diện thiết kế chính.
3. Quan sát dải Ribbon trên cùng tại thẻ **Home**, nhấp chuột vào biểu tượng **Get data** (hoặc nhấp vào mũi tên xổ xuống tại nút Get data).
4. Trong danh mục các nguồn dữ liệu xuất hiện, nhấp chuột chọn dòng **SQL Server Analysis Services database** (nếu không thấy, nhấp vào *More...* -> chọn mục *Database* ở cột trái -> nhấp chọn *SQL Server Analysis Services database* -> nhấp nút **Connect**).
5. Hộp thoại cấu hình kết nối **SQL Server Analysis Services database** xuất hiện trên màn hình:
   * **Server:** Nhập địa chỉ máy chủ SSAS cục bộ của bạn, nhập dấu chấm `.` (đại diện cho localhost) hoặc nhập `localhost` hoặc tên máy tính của bạn (ví dụ: `DESKTOP-ABCXYZ`).
   * **Database (optional):** Nhập chính xác tên cơ sở dữ liệu phân tích SSAS đã được deploy từ Visual Studio: `DW Football SSAS` (hoặc `DW_Football_SSAS`).
   * **Data Connectivity mode (Phương thức kết nối):** Tích chọn tùy chọn **Connect live** (Kết nối trực tiếp tới mô hình dữ liệu đa chiều SSAS Cube để khai thác tức thì toàn bộ các Calculated Member, Named Sets và Hierarchy mà không cần Import dữ liệu).
   * Nhấp nút **OK** để tiến hành kết nối.
6. Cửa sổ điều hướng **Navigator** xuất hiện hiển thị cấu trúc của máy chủ SSAS:
   * Nhấp chuột mở rộng cơ sở dữ liệu `DW Football SSAS`.
   * Tích chọn khối Cube phân tích chính: **`[DW Football Transfermarkt]`**.
   * Quan sát khung xem trước bên phải để kiểm tra toàn bộ cấu trúc: Thư mục thước đo **Measures** (`Goals`, `Assists`, `Goal Contributions`, `Minutes Played`...) và các chiều phân tích (`DIM Player`, `DIM Club`, `DIM Competition`, `DIM Game`, `DIM Time`).
   * Nhấp nút **Load** (hoặc nút **OK**) ở góc dưới cùng bên phải để hoàn tất việc kết nối.
7. Power BI nạp thành công cấu trúc Cube và chuyển về giao diện thiết kế Report Canvas. Khung **Data** ở mép phải màn hình xuất hiện đầy đủ cây đối tượng sẵn sàng kéo thả.

---

### Bước 2: Cấu hình kích thước trang báo cáo (Canvas Settings)
1. Tại thanh tab trang ở mép dưới cùng của màn hình, nhấp đúp chuột vào nhãn `Page 1` và đổi tên thành: `Hiệu suất Cầu thủ`.
2. Nhấp chuột vào một khoảng trống bất kỳ trên trang vẽ Canvas để đảm bảo không visual nào đang được chọn.
3. Tại khung công cụ bên phải, nhấp chọn biểu tượng cây cọ sơn **Format report page** (Định dạng trang báo cáo):
   * Mở rộng mục **Canvas settings** -> Tại ô **Type**, nhấp mở danh sách thả xuống và chọn tỷ lệ chuẩn **16:9** (hoặc chọn **Custom** với chiều rộng `Width: 1280 px`, chiều cao `Height: 720 px`).

---

### Bước 3: Tạo Banner Tiêu đề báo cáo (Title Header)
1. Trên thanh Ribbon **Insert**, nhấp chuột vào biểu tượng **Text box**.
2. Kéo khung Text box đặt ở sát mép trên cùng của trang báo cáo (vị trí `X: 10`, `Y: 10`, `Width: 1260`, `Height: 50`).
3. Nhập nội dung tiêu đề:
   `BÁO BIỂU 1: PHÂN TÍCH HIỆU SUẤT GHI BÀN & ĐÓNG GÓP KIẾN TẠO CỦA CẦU THỦ CHÂU ÂU`
4. Bôi đen toàn bộ đoạn văn bản vừa nhập:
   * Thiết lập Font: `Segoe UI`, Cỡ chữ: `15 pt`, In đậm (**Bold**), Căn lề giữa (**Center**).

---

### Bước 4: Tạo khối 4 Thẻ KPI chỉ số tổng quan (Card Visuals)
Tạo 4 thẻ Card đặt thẳng hàng ngay phía dưới Banner tiêu đề để người xem nắm bắt ngay bức tranh toàn cảnh:

1. **Card 1: Tổng số Bàn thắng (Total Goals)**:
   * Tại khung **Visualizations**, nhấp chọn biểu tượng **Card** (hoặc *New Card*).
   * Kéo thước đo `[Measures].[Goals]` từ thư mục Measures thả vào ô **Fields**.
   * Đổi tên hiển thị: Nhấp đúp vào trường vừa thả, đổi tên thành `Tổng Bàn Thắng`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
2. **Card 2: Tổng số Kiến tạo (Total Assists)**:
   * Nhấp chọn biểu tượng **Card**, đặt cạnh Card 1.
   * Kéo thước đo `[Measures].[Assists]` thả vào ô **Fields**, đổi tên thành `Tổng Kiến Tạo`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
3. **Card 3: Tổng Đóng góp Bàn thắng (Goal Contributions)**:
   * Nhấp chọn biểu tượng **Card**, đặt cạnh Card 2.
   * Kéo thước đo `[Measures].[Goal Contributions]` (hoặc `[Goals] + [Assists]`) thả vào ô **Fields**, đổi tên thành `Tổng Đóng Góp (G+A)`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**).
4. **Card 4: Hiệu suất Phút / Bàn thắng (Mins Per Goal)**:
   * Nhấp chọn biểu tượng **Card**, đặt cạnh Card 3.
   * Kéo thước đo `[Measures].[Minutes Played]` kết hợp tính toán số phút cần thiết để ghi 1 bàn thắng thả vào ô **Fields**, đổi tên thành `Số phút / Bàn thắng`.
   * Định dạng: Vào tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**), hiển thị 1 chữ số thập phân (`#,##0.0`).

---

### Bước 5: Tạo Biểu đồ thanh ngang Top 10 Chân sút ghi bàn nhiều nhất (Clustered Bar Chart)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Clustered bar chart** (biểu đồ thanh ngang nằm ở góc trái).
2. Kéo khung đặt ở góc phía dưới bên trái màn hình.
3. Kéo thả các trường từ khung **Data**:
   * **Vùng Y-axis (Trục tung):** Tìm chiều `DIM Player`, kéo thuộc tính `Player Name` thả vào ô **Y-axis**.
   * **Vùng X-axis (Trục hoành):** Kéo thước đo `Goals` thả vào ô **X-axis**.
   * **Vùng Tooltips:** Kéo thêm các trường `Assists`, `DIM Club [Club Name]`, `DIM Player [Main Position]` để khi di chuột hiển thị đầy đủ thông tin hỗ trợ.
4. **Thiết lập bộ lọc Top 10 Cầu thủ:**
   * Tại khung **Filters** (bên cạnh khung Visualizations), tìm mục **Filters on this visual** -> nhấp mở rộng mục `Player Name`.
   * Tại mục **Filter type**, mở danh sách thả xuống và chọn **Top N**.
   * Tại ô **Show items**, nhập số `10`.
   * Tại ô **By value**, kéo thước đo `Goals` thả vào ô này.
   * Nhấp nút **Apply filter**.
5. **Định dạng visual:**
   * Tab **Format visual** -> Mục **Title**: Bật **On**, nhập: `Top 10 Cầu thủ ghi nhiều bàn thắng nhất Châu Âu`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * Mục **Data labels**: Bật **On** để hiển thị số bàn thắng cụ thể ở cuối mỗi thanh ngang, cỡ chữ `9 pt`.
   * Mục **Values** trên trục Y và trục X: Font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 6: Tạo Biểu đồ vành khăn Cơ cấu đóng góp bàn thắng theo Vị trí (Donut Chart)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Donut chart**.
2. Kéo khung đặt ở khoảng giữa trang báo cáo.
3. Kéo thả các trường dữ liệu:
   * **Vùng Legend:** Tìm chiều `DIM Player`, kéo thuộc tính `Main Position` (Attack, Midfield, Defender) thả vào ô **Legend**.
   * **Vùng Values:** Kéo thước đo `Goal Contributions` (hoặc `Goals`) thả vào ô **Values**.
4. **Định dạng visual:**
   * Tab **Format visual** -> Mục **Title**: Bật **On**, nhập: `Tỷ trọng Đóng góp bàn thắng theo Vị trí thi đấu`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * Mục **Detail labels**: Chọn **Label contents** là `Category, percent of total` (Hiển thị tên vị trí và tỷ lệ %), cỡ chữ `9 pt`.
   * Mục **Legend**: Đặt vị trí **Position** là `Right center`, cỡ chữ `10 pt`.

---

### Bước 7: Tạo Biểu đồ kết hợp Xu hướng Bàn thắng và Kiến tạo qua các Mùa giải (Line and Clustered Column Chart)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Line and clustered column chart** (biểu đồ cột kết hợp đường).
2. Kéo khung đặt ở góc trên bên phải màn hình.
3. Kéo thả các trường dữ liệu:
   * **Vùng X-axis:** Tìm chiều `DIM Time`, kéo thuộc tính `Season` (Mùa giải: 2021/22, 2022/23, 2023/24) và `Quarter` thả vào ô **X-axis**.
   * **Vùng Column Y-axis (Cột):** Kéo thước đo `Goals` thả vào ô này.
   * **Vùng Line Y-axis (Đường):** Kéo thước đo `Assists` thả vào ô này.
4. **Đổi tên và định dạng visual:**
   * Đổi tên cột thành `Tổng số Bàn thắng`.
   * Đổi tên đường thành `Tổng số Kiến tạo`.
   * Tab **Format visual** -> Mục **Title**: Bật **On**, nhập: `Xu hướng Bàn thắng (Cột) và Kiến tạo (Đường) qua các Mùa giải`. Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * Mục **Data labels**: Bật **On** cho cả Cột và Đường, cỡ chữ `9 pt`.
   * Trục X và Trục Y: Font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 8: Tạo Bảng Ma trận chi tiết phong độ cầu thủ (Matrix Visual)
1. Tại khung **Visualizations**, nhấp chuột vào biểu tượng **Matrix**.
2. Kéo khung đặt ở góc dưới bên phải trang Canvas.
3. Kéo thả các trường dữ liệu:
   * **Vùng Rows:** Kéo lần lượt `DIM Player [Player Name]` và `DIM Club [Club Name]` vào ô **Rows**.
   * **Vùng Values:** Kéo các thước đo: `Minutes Played`, `Goals`, `Assists`, `Goal Contributions`, `Yellow Cards`.
4. **Định dạng bảng Matrix:**
   * Vào tab **Format visual**:
   * Mục **Column headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * Mục **Values**: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * Đổi tên các cột hiển thị: `Số phút`, `Bàn thắng`, `Kiến tạo`, `G+A`, `Thẻ vàng`.

---

### Bước 9: Thêm các bộ lọc tương tác đa chiều (Slicers)
Thêm 3 Slicer điều khiển đặt gọn gàng ở cột bên trái hoặc góc trên trang (Định dạng tiêu đề Slicer header: Font `Segoe UI`, cỡ chữ `10 pt`, in đậm; Giá trị Values: cỡ chữ `10 pt`):
1. **Slicer 1 (Mùa giải):** Kéo `DIM Time [Season]` vào visual **Slicer**, thiết lập kiểu hiển thị là **Dropdown**.
2. **Slicer 2 (Giải đấu):** Kéo `DIM Competition [Competition Name]` vào visual **Slicer**, kiểu **Dropdown**.
3. **Slicer 3 (Vị trí thi đấu):** Kéo `DIM Player [Main Position]` vào visual **Slicer**, kiểu **Tile** (nút bấm nhanh).

---

### Bước 10: Kết quả và Nhận xét phân tích
* **Kết quả trực quan:** Dashboard hiển thị đồng bộ và mượt mà. Khi người dùng nhấp chọn mùa giải `2023` hoặc giải đấu `Premier League`, toàn bộ 4 thẻ KPI, Top 10 chân sút (Erling Haaland, Mohamed Salah, Harry Kane...), cơ cấu vị trí và bảng ma trận lập tức tự động lọc theo giải đấu đã chọn.
* **Nhận xét chuyên môn:**
  * Vị trí Tiền đạo (Attack) đóng góp áp đảo trên 65% tổng số bàn thắng, tuy nhiên vị trí Tiền vệ (Midfield) chiếm tới hơn 55% tổng số đường kiến tạo thành bàn.
  * Hiệu suất số phút/bàn thắng của Top 10 chân sút hàng đầu đạt mức ấn tượng dưới 110 phút/bàn, thể hiện sự ổn định vượt trội của các ngôi sao tấn công hàng đầu châu Âu.
