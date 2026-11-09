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
   * Mở rộng mục **Canvas settings** -> Tại ô **Type**, chọn tỷ lệ chuẩn **16:9** (hoặc chọn **Custom** với `Width: 1280 px`, `Height: 720 px`).
   * **Canvas background**: Giữ nguyên mặc định nguyên bản của Power BI, tuyệt đối không chỉnh màu hay độ trong suốt.

> **MẸO NHẬP TỌA ĐỘ VÀ KÍCH THƯỚC CHUẨN XÁC TỪNG PIXEL:**
> Để visual nằm đúng vị trí và không bao giờ bị thiếu chỗ hay đè lên nhau, sau khi tạo mỗi visual:
> Nhấp chọn visual -> Tại khung **Visualizations**, chọn tab **General** -> Mở rộng mục **Properties**:
> * **Size:** Nhập **Width** (Chiều rộng) và **Height** (Chiều cao).
> * **Position:** Nhập **Horizontal** (Tọa độ ngang X) và **Vertical** (Tọa độ dọc Y).

---

### Bước 3: Tạo Banner Tiêu đề báo cáo (Title Header)
1. Trên thanh Ribbon **Insert**, nhấp chuột vào biểu tượng **Text box**.
2. Nhập nội dung tiêu đề:
   `BÁO BIỂU 1: PHÂN TÍCH HIỆU SUẤT GHI BÀN & ĐÓNG GÓP KIẾN TẠO CỦA CẦU THỦ CHÂU ÂU`
3. Bôi đen toàn bộ đoạn văn bản vừa nhập:
   * Thiết lập Font: `Segoe UI`, Cỡ chữ: `15 pt`, In đậm (**Bold**), Căn lề giữa (**Center**).
4. Thiết lập vị trí và kích thước tại **Properties**:
   * **Size:** `Width = 1250 px`, `Height = 45 px`
   * **Position:** `Horizontal = 15 px`, `Vertical = 10 px`

---

### Bước 4: Tạo khối 4 Thẻ KPI chỉ số tổng quan (Card Visuals)
Tạo 4 thẻ Card đặt thẳng hàng ngang ngay phía dưới Banner tiêu đề (Y = 65 px, Chiều cao = 85 px):

1. **Card 1: Tổng số Bàn thắng (Total Goals)**:
   * Tại khung **Visualizations**, nhấp chọn biểu tượng **Card**.
   * Kéo thước đo `[Measures].[Goals]` từ thư mục Measures thả vào ô **Fields**.
   * Đổi tên hiển thị thành `Tổng Bàn Thắng`.
   * Định dạng: Tab **Format visual** -> **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**). Category label: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 15 px`, `Vertical = 65 px`).
2. **Card 2: Tổng số Kiến tạo (Total Assists)**:
   * Nhấp chọn biểu tượng **Card**, kéo thước đo `[Measures].[Assists]` thả vào ô **Fields**, đổi tên thành `Tổng Kiến Tạo`.
   * Định dạng: **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**). Category label: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 333 px`, `Vertical = 65 px`).
3. **Card 3: Tổng Đóng góp Bàn thắng (Goal Contributions)**:
   * Nhấp chọn biểu tượng **Card**, kéo thước đo `[Measures].[Goal Contributions]` (hoặc `[Goals] + [Assists]`) thả vào ô **Fields**, đổi tên thành `Tổng Đóng Góp (G+A)`.
   * Định dạng: **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**). Category label: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 651 px`, `Vertical = 65 px`).
4. **Card 4: Hiệu suất Phút / Bàn thắng (Mins Per Goal)**:
   * Nhấp chọn biểu tượng **Card**, kéo thước đo `[Measures].[Minutes Played]` thả vào ô **Fields**, đổi tên thành `Số phút / Bàn thắng`.
   * Định dạng: **Callout value**: Font `Segoe UI`, Cỡ chữ `26 pt`, In đậm (**Bold**), hiển thị 1 chữ số thập phân (`#,##0.0`). Category label: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 295 px`, `Height = 85 px`), Position (`Horizontal = 970 px`, `Vertical = 65 px`).

---

### Bước 5: Thêm 3 Bộ lọc tương tác đa chiều (Slicers)
Tạo 3 Slicer đặt thành hàng ngang ngay dưới khối KPI (Y = 160 px, Chiều cao = 50 px) giúp người dùng lọc dữ liệu nhanh:
1. **Slicer 1 (Mùa giải):**
   * Thêm visual **Slicer**, kéo trường `DIM Time [Season]` vào ô **Field**, chọn kiểu hiển thị **Dropdown**.
   * Định dạng: Slicer header: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 390 px`, `Height = 50 px`), Position (`Horizontal = 15 px`, `Vertical = 160 px`).
2. **Slicer 2 (Giải đấu):**
   * Thêm visual **Slicer**, kéo trường `DIM Competition [Competition Name]` vào ô **Field**, chọn kiểu **Dropdown**.
   * Định dạng: Slicer header: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**); Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 420 px`, `Height = 50 px`), Position (`Horizontal = 445 px`, `Vertical = 160 px`).
3. **Slicer 3 (Vị trí thi đấu):**
   * Thêm visual **Slicer**, kéo trường `DIM Player [Main Position]` vào ô **Field**, chọn kiểu **Tile** (nút bấm nhanh).
   * Định dạng: Values: Font `Segoe UI`, Cỡ chữ `10 pt`.
   * **Properties:** Size (`Width = 390 px`, `Height = 50 px`), Position (`Horizontal = 875 px`, `Vertical = 160 px`).

---

### Bước 6: Tạo Biểu đồ thanh ngang Top 10 Chân sút ghi bàn nhiều nhất (Clustered Bar Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Clustered bar chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 475 px`, `Height = 485 px`
   * **Position:** `Horizontal = 15 px`, `Vertical = 220 px`
3. Kéo thả các trường từ khung **Data**:
   * **Vùng Y-axis (Trục tung):** Tìm chiều `DIM Player`, kéo thuộc tính `Player Name` thả vào ô **Y-axis**.
   * **Vùng X-axis (Trục hoành):** Kéo thước đo `Goals` thả vào ô **X-axis**.
   * **Vùng Tooltips:** Kéo thêm các thước đo `Assists`, `Goal Contributions` (hoặc `Minutes Played`) để khi di chuột vào mỗi thanh của cầu thủ sẽ hiển thị bổ sung số pha kiến tạo và tổng đóng góp bàn thắng. *(Lưu ý: Chế độ Connect Live với SSAS Cube chỉ nhận các Thước đo - Measures vào ô Tooltips phẳng, không thả trực tiếp các thuộc tính văn bản Dimension như Club Name hay Main Position).*
4. **Thiết lập bộ lọc Top 10 Cầu thủ:**
   * Tại khung **Filters**, mục **Filters on this visual** -> nhấp mở rộng `Player Name`.
   * Chọn **Top N**, tại ô **Show items** nhập `10`, tại ô **By value** kéo thước đo `Goals` vào và nhấp **Apply filter**.
5. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Nhập `Top 10 Cầu thủ ghi nhiều bàn thắng nhất Châu Âu`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Data labels**: Bật **On**, cỡ chữ `9 pt`.
   * **Values** trên trục Y và trục X: Font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 7: Tạo Biểu đồ vành khăn Cơ cấu đóng góp bàn thắng theo Vị trí (Donut Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Donut chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 350 px`, `Height = 235 px`
   * **Position:** `Horizontal = 505 px`, `Vertical = 220 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng Legend:** Tìm chiều `DIM Player`, kéo thuộc tính `Main Position` (Attack, Midfield, Defender) thả vào ô **Legend**.
   * **Vùng Values:** Kéo thước đo `Goal Contributions` (hoặc `Goals`) thả vào ô **Values**.
4. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Nhập `Tỷ trọng Đóng góp bàn thắng theo Vị trí thi đấu`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Detail labels**: Chọn `Category, percent of total`, cỡ chữ `9 pt`.
   * **Legend**: Vị trí `Right center`, cỡ chữ `10 pt`.

---

### Bước 8: Tạo Biểu đồ kết hợp Xu hướng Bàn thắng và Kiến tạo qua các Mùa giải (Line and Clustered Column Chart)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Line and clustered column chart**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 395 px`, `Height = 235 px`
   * **Position:** `Horizontal = 870 px`, `Vertical = 220 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng X-axis:** Tìm chiều `DIM Time`, kéo thuộc tính `Season` (Mùa giải: 2021/22, 2022/23, 2023/24) và `Quarter` thả vào ô **X-axis**.
   * **Vùng Column Y-axis (Cột):** Kéo thước đo `Goals` thả vào ô này (đổi tên hiển thị thành `Tổng số Bàn thắng`).
   * **Vùng Line Y-axis (Đường):** Kéo thước đo `Assists` thả vào ô này (đổi tên hiển thị thành `Tổng số Kiến tạo`).
4. **Định dạng visual:**
   * Tab **Format visual** -> **Title**: Nhập `Xu hướng Bàn thắng (Cột) và Kiến tạo (Đường) qua các Mùa giải`, Font `Segoe UI`, Cỡ chữ `12 pt`, In đậm (**Bold**), Căn giữa (**Center**).
   * **Data labels**: Bật **On** cho cả Cột và Đường, cỡ chữ `9 pt`.
   * Trục X và Trục Y: Font `Segoe UI`, cỡ chữ `10 pt`.

---

### Bước 9: Tạo Bảng Ma trận chi tiết phong độ cầu thủ (Matrix Visual)
1. Tại khung **Visualizations**, nhấp chọn biểu tượng **Matrix**.
2. Thiết lập kích thước và vị trí tại **Properties**:
   * **Size:** `Width = 760 px`, `Height = 235 px`
   * **Position:** `Horizontal = 505 px`, `Vertical = 470 px`
3. Kéo thả các trường dữ liệu:
   * **Vùng Rows:** Kéo lần lượt `DIM Player [Player Name]` và `DIM Club [Club Name]` vào ô **Rows**.
   * **Vùng Values:** Kéo các thước đo: `Minutes Played`, `Goals`, `Assists`, `Goal Contributions`, `Yellow Cards`.
4. **Định dạng bảng Matrix:**
   * Đổi tên các cột: `Số phút`, `Bàn thắng`, `Kiến tạo`, `G+A`, `Thẻ vàng`.
   * Tab **Format visual** -> **Column headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * **Row headers**: Font `Segoe UI`, Cỡ chữ `10 pt`, In đậm (**Bold**).
   * **Values**: Font `Segoe UI`, Cỡ chữ `10 pt`.

---

### Bước 10: Kết quả và Nhận xét phân tích
* **Kết quả trực quan:** Dashboard hiển thị đồng bộ và mượt mà. Khi người dùng nhấp chọn mùa giải `2023` hoặc giải đấu `Premier League`, toàn bộ 4 thẻ KPI, Top 10 chân sút (Erling Haaland, Mohamed Salah, Harry Kane...), cơ cấu vị trí và bảng ma trận lập tức tự động lọc theo giải đấu đã chọn.
* **Nhận xét chuyên môn:**
  * Vị trí Tiền đạo (Attack) đóng góp áp đảo trên 65% tổng số bàn thắng, tuy nhiên vị trí Tiền vệ (Midfield) chiếm tới hơn 55% tổng số đường kiến tạo thành bàn.
  * Hiệu suất số phút/bàn thắng của Top 10 chân sút hàng đầu đạt mức ấn tượng dưới 110 phút/bàn, thể hiện sự ổn định vượt trội của các ngôi sao tấn công hàng đầu châu Âu.
