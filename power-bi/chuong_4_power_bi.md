# Chương 4: Quá trình Lập Báo biểu bằng Công cụ Power BI

Chương này trình bày toàn diện quy trình xây dựng hệ thống 3 báo biểu trực quan hóa dữ liệu kinh doanh thông minh [Business Intelligence] bằng phần mềm **Microsoft Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS Multidimensional Cube `[DW Football Transfermarkt]`.

---

## 4.1 Giới thiệu Công cụ Power BI & Kiến trúc Kết nối SSAS Live Connection

Trong hệ thống giải pháp BI của Microsoft, Power BI Desktop là công cụ phân tích và trực quan hóa hàng đầu. Khi làm việc với khối dữ liệu đa chiều SSAS, Power BI hỗ trợ cơ chế kết nối trực tiếp **Live Connection** mang lại các lợi thế kỹ thuật vượt trội:
* **Tối ưu hóa hiệu năng tính toán:** Toàn bộ các phép toán tổng hợp, tính toán độ đo phức tạp [Measures] và các biểu thức đa chiều MDX đều được thực thi trực tiếp trên máy chủ SSAS thông qua hai động cơ Storage Engine và Formula Engine.
* **Tiết kiệm tài nguyên Client:** Không cần sao chép dữ liệu chi tiết vào tệp `.pbix`, giúp tệp Power BI cực kỳ nhỏ gọn và thời gian khởi động báo cáo tức thì.
* **Cập nhật dữ liệu thời gian thực:** Mọi sự thay đổi về cấu trúc Dimension, Hierarchy, Calculated Measures hoặc dữ liệu trong SSAS Cube đều được phản ánh đồng bộ trên Power BI ngay sau khi làm mới.

---

## 4.2 Cấu hình Môi trường và Khởi tạo Kết nối Live Connection

Quy trình thiết lập kết nối từ Power BI Desktop đến khối cơ sở dữ liệu đa chiều SSAS `DW Football Transfermarkt` được tiến hành qua các bước chuẩn tắc:

1. **Khởi tạo kết nối:** Khởi động Power BI Desktop, tại thẻ **Home** $\rightarrow$ nhấp chọn **Get data** $\rightarrow$ chọn **SQL Server Analysis Services database**.

*Hình 4.1. Giao diện chọn nguồn dữ liệu SQL Server Analysis Services database trên Power BI*

2. **Khai báo thông số kết nối:** Nhập Server là `localhost` [hoặc tên máy tính cá nhân `DESKTOP-9B88R8P`], nhập Database là `SSAS_Football_Transfermarkt`. Tại tùy chọn Connection mode, tích chọn **Connect live** rồi nhấn **OK**.

*Hình 4.2. Khai báo thông tin kết nối Connect live đến SSAS Database*

3. **Chọn Cube phân tích:** Cửa sổ Navigator xuất hiện, nhấp chọn khối đa chiều **`DW Football Transfermarkt`** và nhấn **OK**.

*Hình 4.3. Chọn Cube DW Football Transfermarkt trong cửa sổ Navigator*

4. **Kiểm tra Metadata:** Khung Data bên phải màn hình Power BI hiển thị đầy đủ danh sách 5 Dimensions [`DIM Player`, `DIM Club`, `DIM Competition`, `DIM Game`, `DIM Time`] cùng toàn bộ các Measures và Calculated Measures sẵn sàng để kéo thả.

---

### 4.3.43 Báo biểu 1: Báo biểu Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu & Huấn luyện viên

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 1** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 1:**
> Thống kê tổng hợp quy mô tổ chức thi đấu, số lượng huấn luyện viên và hiệu suất tấn công [Bàn thắng, Kiến tạo] theo cấu trúc đa tầng phân cấp giải đấu [Loại giải đấu $\rightarrow$ Quốc gia $\rightarrow$ Giải đấu $\rightarrow$ Vòng đấu] và tiến trình chuỗi thời gian [Năm $\rightarrow$ Quý $\rightarrow$ Tháng $\rightarrow$ Ngày] kết hợp với thời lượng thi đấu [Minutes Played].

---

#### 4.3.43.1 Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live [kết nối trực tiếp đến khối cơ sở dữ liệu SSAS Multidimensional].
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước tùy chỉnh Custom `1920 x 1080 px` [tỷ lệ chuẩn 16:9], Canvas Background màu sáng `#F8FAFC`.

---

#### 4.3.43.2 Danh mục Thành phần Trực quan trên Báo biểu 1

Báo biểu 1 được bố cục khoa học gồm 11 visual trực quan:

| STT | Tên thành phần Visual | Loại trực quan [Visual Type] | Thuộc tính / Độ đo ánh xạ | Vai trò nghiệp vụ |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Banner Tiêu đề | TextBox | Tiêu đề báo biểu | Định danh nghiệp vụ Dashboard |
| **2** | Card Tổng trận đấu | Card | `Distinct Matches Played` | Đo lường tổng số trận đấu |
| **3** | Card Tổng HLV | Card | `Total Coaches` | Thống kê số lượng HLV tham gia |
| **4** | Card Tổng bàn thắng | Card | `Goals` | Đo lường tổng số pha lập công |
| **5** | Card Tổng kiến tạo | Card | `Assists` | Đo lường tổng số đường chuyền thành bàn |
| **6** | Slicer Tên giải đấu | Slicer [Dropdown] | `DIM Competition.Competition Name` | Lọc dữ liệu theo từng giải đấu |
| **7** | Slicer Quốc gia | Slicer [Dropdown] | `DIM Competition.Country Name` | Lọc dữ liệu theo quốc gia tổ chức |
| **8** | Slicer Câu lạc bộ | Slicer [Dropdown] | `DIM Club.Club Name` | Lọc dữ liệu theo câu lạc bộ |
| **9** | Slicer Cầu thủ | Slicer [Dropdown] | `DIM Player.Player Name` | Lọc dữ liệu theo cá nhân cầu thủ |
| **10** | Biểu đồ Phân cấp giải đấu | Clustered Bar Chart | Category: Type $\rightarrow$ Country $\rightarrow$ Comp $\rightarrow$ Round<br>Y: `Goals`, `Assists` | Phân tích hiệu suất theo thứ bậc giải |
| **11** | Biểu đồ Chuỗi thời gian | Line & Stacked Column Combo Chart | X: Year $\rightarrow$ Quarter $\rightarrow$ Month $\rightarrow$ Day<br>Column Y: `Goals`, `Assists`<br>Line Y: `Minutes Played` | Tương quan thời lượng và bàn thắng |

---

#### 4.3.43.3 Quy trình Thiết lập Chi tiết Từng bước trên Power BI

### Bước 1: Khởi tạo kết nối dữ liệu từ SSAS Database
1. Khởi động phần mềm **Microsoft Power BI Desktop**.
2. Tại thanh Ribbon thẻ **Home**, nhấp chọn **Get data** $\rightarrow$ nhấp chọn **SQL Server Analysis Services database**.

*Hình 4.1. Chọn phương thức kết nối SQL Server Analysis Services database trên Power BI*

3. Cửa sổ kết nối xuất hiện:
   * **Server:** Nhập `localhost` [hoặc tên máy tính cá nhân].
   * **Database:** Nhập `SSAS_Football_Transfermarkt`.
   * **Connection mode:** Tích chọn vào mục **Connect live**.
   * Nhấp nút **OK**.

*Hình 4.2. Khai báo thông số kết nối Connect live đến SSAS Database*

4. Cửa sổ Navigator hiển thị danh mục khối đa chiều, nhấp chọn khối **`DW Football Transfermarkt`** rồi nhấn **OK**.

*Hình 4.3. Chọn Cube DW Football Transfermarkt trong cửa sổ Navigator*

---

### Bước 2: Cấu hình kích thước trang báo cáo [Canvas Settings]
1. Trong giao diện thiết kế, quan sát thanh bảng điều khiển bên phải, nhấp vào biểu tượng **Format page** [hình cây cọ lăn sơn].
2. Mở rộng mục **Canvas settings**:
   * Tại ô **Type**, nhấp chọn kiểu **Custom**.
   * Thiết lập **Width** là `1920 px`.
   * Thiết lập **Height** là `1080 px`.
3. Mở rộng mục **Canvas background**, chọn màu nền xám sáng nhạt `#F8FAFC` để tôn vinh độ tương phản của các biểu đồ.

*Hình 4.4. Cấu hình Canvas settings chuẩn Full HD 1920x1080 cho Báo biểu 1*

---

### Bước 3: Tạo Banner Tiêu đề cho Báo biểu 1
1. Trên thanh Ribbon, chọn thẻ **Insert** $\rightarrow$ nhấp chọn **Text box**.
2. Thiết lập tọa độ vị trí và kích thước cho Text box:
   * Vị trí: `x = 20 px`, `y = 10 px`.
   * Kích thước: `Width = 1880 px`, `Height = 70 px`.
3. Nhập nội dung tiêu đề: **`BÁO BIỂU: TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU & HUẤN LUYỆN VIÊN`**.
4. Định dạng chữ in hoa đậm, font chữ Segoe UI / Arial, cỡ chữ `18 pt`, màu xanh tím than đậm `#1B365D`, căn lề chính giữa.

*Hình 4.5. Tạo và định dạng Text box tiêu đề cho Báo biểu 1*

---

### Bước 4: Tạo và cấu hình hàng thẻ chỉ số KPI tổng quan [Cards Row]
Kéo thả 4 visual dạng **Card** từ khung Visualizations vào hàng ngang ngay dưới banner tiêu đề [tọa độ `y = 100 px`, chiều cao `Height = 100 px`, chiều rộng `Width = 450 px`]:
1. **Card 1 [Tổng số trận đấu]:** Kéo thước đo `FACT Player Match Perf.Distinct Matches Played` vào ô **Fields/Values**. Chuột phải vào tên trường chọn **Rename for this visual** đổi thành `Tổng số trận đấu`. Vị trí: `x = 20 px`.
2. **Card 2 [Tổng số Huấn luyện viên]:** Kéo thước đo `FACT Player Match Perf.Total Coaches` vào ô **Fields/Values**. Đổi tên hiển thị thành `Tổng số Huấn luyện viên`. Vị trí: `x = 492 px`.
3. **Card 3 [Tổng số Bàn thắng]:** Kéo thước đo `FACT Player Match Perf.Goals` vào ô **Fields/Values**. Đổi tên hiển thị thành `Tổng số Bàn thắng`. Vị trí: `x = 959 px`.
4. **Card 4 [Tổng số Kiến tạo]:** Kéo thước đo `FACT Player Match Perf.Assists` vào ô **Fields/Values**. Đổi tên hiển thị thành `Tổng số Kiến tạo`. Vị trí: `x = 1433 px`.

*Hình 4.6. Cấu hình các thẻ Card KPI đo lường quy mô và sản lượng tấn công*

*Hình 4.7. Kết quả hiển thị hàng thẻ Card KPI Báo biểu 1*

---

### Bước 5: Tạo và cấu hình hàng bộ lọc động tương tác [Slicers Row]
Kéo thả 4 visual dạng **Slicer** vào hàng thứ hai [tọa độ `y = 225 px`, chiều cao `Height = 75 px`, chiều rộng `Width = 450 px`]:
1. **Slicer 1 [Tên giải đấu]:** Kéo thuộc tính `DIM Competition.Competition Name` vào ô **Field**. Vào mục Format visual $\rightarrow$ Slicer settings $\rightarrow$ Style chọn **Dropdown**. Vị trí: `x = 20 px`.
2. **Slicer 2 [Quốc gia tổ chức]:** Kéo thuộc tính `DIM Competition.Country Name` vào ô **Field**, định dạng kiểu Dropdown. Vị trí: `x = 494 px`.
3. **Slicer 3 [Câu lạc bộ]:** Kéo thuộc tính `DIM Club.Club Name` vào ô **Field**, định dạng kiểu Dropdown. Vị trí: `x = 961 px`.
4. **Slicer 4 [Cầu thủ]:** Kéo thuộc tính `DIM Player.Player Name` vào ô **Field**, định dạng kiểu Dropdown có thanh Search tìm kiếm nhanh. Vị trí: `x = 1433 px`.

*Hình 4.8. Cấu hình hàng Slicer bộ lọc động cho Báo biểu 1*

*Hình 4.9. Kết quả hàng Slicer bộ lọc Báo biểu 1*

---

### Bước 6: Tạo và cấu hình Biểu đồ phân cấp giải đấu [Clustered Bar Chart]
1. Tại khung Visualizations, nhấp chọn biểu tượng **Clustered bar chart** [biểu đồ thanh ngang theo cụm] và kéo đặt vào khu vực bên trái [tọa độ `x = 20 px`, `y = 320 px`, `Width = 920 px`, `Height = 384 px`].
2. Cấu hình các trục dữ liệu:
   * **Trục danh mục [Y-axis / Category]:** Kéo lần lượt 4 cấp thuộc tính theo đúng thứ tự phân tầng:
     - Cấp 1: `DIM Competition.Competition Type` [Loại giải: domestic_league, international_cup...].
     - Cấp 2: `DIM Competition.Country Name` [Quốc gia tổ chức].
     - Cấp 3: `DIM Competition.Competition Name` [Tên giải đấu cụ thể].
     - Cấp 4: `DIM Game.Round` [Vòng đấu / Chặng thi đấu].
   * **Trục giá trị đo lường [X-axis]:** Kéo 2 độ đo `FACT Player Match Perf.Goals` và `FACT Player Match Perf.Assists`.
3. Định dạng biểu đồ:
   * Vào Format visual $\rightarrow$ **Data labels** $\rightarrow$ Bật **On** để hiển thị rõ ràng con số bàn thắng và kiến tạo trên từng thanh.
   * Cấu hình màu sắc cột: Màu xanh dương đậm cho `Goals` và màu cam san hô cho `Assists`.
   * Tính năng Drill Down trên góc biểu đồ cho phép người xem nhấp đúp chuột để khám phá từ loại giải xuống từng quốc gia, giải đấu và từng vòng đấu chi tiết.

*Hình 4.10. Cấu hình cấu trúc phân tầng 4 cấp và độ đo cho biểu đồ Clustered bar chart*

*Hình 4.11. Kết quả biểu đồ Clustered bar chart phân cấp giải đấu*

---

### Bước 7: Tạo và cấu hình Biểu đồ kết hợp chuỗi thời gian [Combo Chart]
1. Tại khung Visualizations, chọn biểu tượng **Line and stacked column chart** [biểu đồ kết hợp cột chồng và đường] và đặt vào khu vực bên phải [tọa độ `x = 963 px`, `y = 319 px`, `Width = 920 px`, `Height = 385 px`].
2. Cấu hình các trục dữ liệu:
   * **Trục thời gian [X-axis]:** Kéo lần lượt phân cấp thời gian: `DIM Time.Year` $ightarrow$ `DIM Time.Quarter` $ightarrow$ `DIM Time.Month` $ightarrow$ `DIM Time.Day`.
   * **Trục cột đo lường [Column y-axis]:** Kéo `FACT Player Match Perf.Goals` và `FACT Player Match Perf.Assists`.
   * **Trục đường biểu diễn [Line y-axis]:** Kéo thước đo `FACT Player Match Perf.Minutes Played`.
3. Định dạng nâng cao:
   * Vào Format visual $\rightarrow$ mở rộng mục **Y-axis**, bật tính năng **Secondary y-axis** [trục tung phụ bên phải] để tách riêng thang đo phút thi đấu độc lập với thang đo số bàn thắng/kiến tạo.
   * Bật **Data labels** cho cả hai trục để theo dõi biến động chính xác.

*Hình 4.12. Cấu hình biểu đồ Line and stacked column chart theo chuỗi thời gian*

*Hình 4.13. Kết quả biểu đồ kết hợp chuỗi thời gian Báo biểu 1*

---

### Bước 8: Căn chỉnh bố cục tổng thể và Kiểm thử tương tác
1. Chọn tất cả các visual trên trang, vào thẻ **Format** trên thanh Ribbon $ightarrow$ sử dụng tính năng **Align** [Align Top, Distribute Horizontally] để bảo đảm khoảng cách lề và giữa các visual chuẩn xác từng pixel.
2. Kiểm thử tương tác chéo [Cross-filtering]: Nhấp chuột vào thanh giải đấu `England` trên biểu đồ phân cấp, toàn bộ các Card và biểu đồ thời gian lập tức chuyển sang ngữ cảnh riêng của bóng đá Anh.

*Hình 4.14. Kết quả giao diện hoàn chỉnh của Báo biểu 1 trên Power BI Desktop*

---

### 4.3.4 Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 1

Từ các số liệu trực quan hóa trên Báo biểu 1, nhóm rút ra các nhận định phân tích nghiệp vụ sâu sắc:
1. **Phân bổ quy mô giải đấu:** Các giải đấu Vô địch Quốc gia [domestic_league] chiếm hơn $85\%$ tổng số trận đấu và tổng số bàn thắng, giữ vai trò nền tảng cho toàn bộ hoạt động bóng đá đỉnh cao châu Âu.
2. **Sức mạnh hỏa lực các giải đấu hàng đầu:** Ngoại Hạng Anh [Premier League] và LaLiga [Tây Ban Nha] dẫn đầu toàn châu lục về tổng sản lượng bàn thắng và kiến tạo, đồng thời quy tụ số lượng huấn luyện viên trưởng danh tiếng đông đảo nhất.
3. **Tính chu kỳ thi đấu theo mùa:** Biểu đồ kết hợp chuỗi thời gian vạch rõ hai giai đoạn bùng nổ bàn thắng mạnh mẽ nhất trong năm: Giai đoạn tháng 12 đến tháng 1 [lịch thi đấu mùa đông dày đặc] và giai đoạn tháng 4 đến tháng 5 [giai đoạn đua tranh vô địch và trụ hạng khốc liệt].
4. **Tương quan giữa thể lực và hiệu quả tấn công:** Đường biểu diễn số phút thi đấu [Minutes Played] tỷ lệ thuận hoàn hảo với số lượng bàn thắng, khẳng định chiều sâu đội hình và khả năng duy trì thể lực liên tục là nhân tố quyết định đến sự bùng nổ bàn thắng của các đội bóng.

---

### 4.4.44 Báo biểu 2: Báo biểu Phân tích Tiềm năng Người chơi và Câu lạc bộ

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 2** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 2:**
> Phân tích chuyên sâu năng lực ghi bàn, kiến tạo và tiềm năng phát triển của từng cầu thủ gắn liền với câu lạc bộ chủ quản, đánh giá tác động của yếu tố địa điểm thi đấu [Sân vận động] đến mật độ bàn thắng, theo dõi nhịp điệu phong độ săn bàn qua từng tháng/năm, và tra cứu hồ sơ nhân trắc học chi tiết [Độ tuổi, Chân thuận, Quốc tịch].

---

#### 4.4.44.1 Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live trực tiếp từ SSAS.
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước Custom `1920 x 1080 px` [chuẩn Full HD 16:9], Canvas Background màu sáng `#F8FAFC`.

---

#### 4.4.44.2 Danh mục Thành phần Trực quan trên Báo biểu 2

Báo biểu 2 tích hợp 13 visual trực quan được sắp xếp cân đối:

| STT | Tên thành phần Visual | Loại trực quan | Thuộc tính / Độ đo ánh xạ | Vai trò nghiệp vụ |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Banner Tiêu đề | TextBox | Tiêu đề báo biểu 2 | Định danh nghiệp vụ Dashboard |
| **2** | Card Tổng trận đấu | Card | `Distinct Matches Played` | Tổng số trận trong phạm vi lọc |
| **3** | Card Tổng kiến tạo | Card | `Assists` | Tổng số pha kiến tạo thành bàn |
| **4** | Card Tổng bàn thắng | Card | `Goals` | Tổng số bàn thắng ghi được |
| **5** | Card Tổng thời lượng | Card | `Minutes Played` | Tổng thời lượng thi đấu trên sân |
| **6** | Slicer Cầu thủ | Slicer [Dropdown] | `DIM Player.Player Name` | Tra cứu chi tiết từng cá nhân cầu thủ |
| **7** | Slicer Câu lạc bộ | Slicer [Dropdown] | `DIM Club.Club Name` | Lọc toàn bộ báo cáo theo CLB |
| **8** | Slicer Mùa giải | Slicer [Dropdown] | `DIM Time.Season` | Lọc theo mùa 2022/2023 hoặc 2023/2024 |
| **9** | Slicer Tháng | Slicer [Dropdown] | `DIM Time.Month` | Lọc biến động theo tháng |
| **10** | Biểu đồ Hỏa lực CLB | Clustered Bar Chart | Y: `Club Name`<br>X: `Goals`, `Assists` | So sánh sức mạnh tấn công giữa các CLB |
| **11** | Biểu đồ Sân vận động & Bàn thắng | Line & Clustered Column Combo Chart | X: `Stadium`<br>Column Y: `Matches Played`<br>Line Y: `Goals` | Tương quan số trận và bàn thắng theo SVĐ |
| **12** | Biểu đồ Vùng xu hướng bàn thắng | Area Chart | X: `Month`, `Year`<br>Y: `Goals` | Nhịp điệu săn bàn qua từng tháng trong năm |
| **13** | Bảng hồ sơ chi tiết cầu thủ | Table [tableEx] | `Player Name`, `Age`, `Foot`, `Country`, `Assists`, `Goals` | Tra cứu nhân trắc học và hiệu suất cá nhân |

---

#### 4.4.44.3 Quy trình Thiết lập Chi tiết Từng bước trên Power BI

### Bước 1: Tạo trang báo cáo mới và Cấu hình Canvas
1. Tại thanh điều hướng chân trang Power BI, nhấp vào dấu cộng [+] để thêm một trang mới và đổi tên thành **Báo biểu 2**.
2. Tại bảng điều khiển Format page ở khung bên phải, chọn **Canvas settings** $\rightarrow$ Type chọn **Custom** $\rightarrow$ thiết lập Width `1920 px`, Height `1080 px`.

*Hình 4.15. Khởi tạo trang report Báo biểu 2 và cấu hình Canvas chuẩn 1920x1080*

---

### Bước 2: Tạo Banner Tiêu đề cho Báo biểu 2
1. Chọn thẻ **Insert** $\rightarrow$ chọn **Text box**, đặt tại vị trí `x = 10 px`, `y = 10 px` với kích thước `Width = 1880 px`, `Height = 70 px`.
2. Nhập tiêu đề: **`BÁO BIỂU: PHÂN TÍCH TIỀM NĂNG NGƯỜI CHƠI VÀ CÂU LẠC BỘ`**.
3. Định dạng chữ in hoa đậm, font Segoe UI / Arial, cỡ `18 pt`, màu xanh tím than `#1B365D`, căn giữa.

*Hình 4.16. Tạo và định dạng Text box tiêu đề cho Báo biểu 2*

---

### Bước 3: Tạo và cấu hình hàng thẻ chỉ số KPI [Cards Row]
Kéo thả 4 visual dạng **Card** vào hàng trên cùng [tọa độ `y = 90 px`, chiều cao `Height = 90 px`, chiều rộng `Width = 455 px`]:
1. **Card 1 [Tổng số trận đấu]:** Kéo `FACT Player Match Perf.Distinct Matches Played` vào ô **Values**. Đổi tên hiển thị thành `Tổng số trận đấu`. Vị trí: `x = 20 px`.
2. **Card 2 [Tổng số Kiến tạo]:** Kéo `FACT Player Match Perf.Assists` vào ô **Values**. Đổi tên hiển thị thành `Tổng số Kiến tạo`. Vị trí: `x = 495 px`.
3. **Card 3 [Tổng số Bàn thắng]:** Kéo `FACT Player Match Perf.Goals` vào ô **Values**. Đổi tên hiển thị thành `Tổng số Bàn thắng`. Vị trí: `x = 970 px`.
4. **Card 4 [Tổng số Phút thi đấu]:** Kéo `FACT Player Match Perf.Minutes Played` vào ô **Values**. Đổi tên hiển thị thành `Tổng thời lượng thi đấu`. Vị trí: `x = 1445 px`.

*Hình 4.17. Cấu hình và kết quả 4 thẻ Card KPI Báo biểu 2*

---

### Bước 4: Tạo và cấu hình hàng bộ lọc đa chiều [Slicers Row]
Kéo thả 4 visual dạng **Slicer** vào hàng thứ hai [tọa độ `y = 200 px`, chiều cao `Height = 75 px`, chiều rộng `Width = 455 px`]:
1. **Slicer 1 [Cầu thủ]:** Kéo `DIM Player.Player Name` vào ô **Field**, định dạng Dropdown kèm ô tìm kiếm Search. Vị trí: `x = 20 px`.
2. **Slicer 2 [Câu lạc bộ]:** Kéo `DIM Club.Club Name` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 495 px`.
3. **Slicer 3 [Mùa giải]:** Kéo `DIM Time.Season` vào ô **Field**, định dạng Dropdown [lựa chọn mùa 2022/2023 hoặc 2023/2024]. Vị trí: `x = 969 px`.
4. **Slicer 4 [Tháng]:** Kéo `DIM Time.Month` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 1445 px`.

*Hình 4.18. Cấu hình hàng Slicer bộ lọc cho Báo biểu 2*

---

### Bước 5: Tạo Biểu đồ Hỏa lực theo CLB [Clustered Bar Chart]
1. Chọn biểu tượng **Clustered bar chart** và đặt tại vị trí `x = 20 px`, `y = 300 px`, `Width = 925 px`, `Height = 385 px`.
2. Cấu hình các trục:
   * **Trục tung [Y-axis]:** Kéo `DIM Club.Club Name`.
   * **Trục hoành [X-axis]:** Kéo `FACT Player Match Perf.Goals` và `FACT Player Match Perf.Assists`.
3. Nhấp vào nút tùy chọn dấu ba chấm [...] ở góc biểu đồ $ightarrow$ chọn **Sort axis** $ightarrow$ chọn **Sort by Goals** $ightarrow$ chọn **Sort descending** để xếp các CLB có số bàn thắng nhiều nhất lên đầu bảng.

*Hình 4.19. Cấu hình và kết quả Clustered bar chart so sánh sức mạnh hỏa lực các CLB*

---

### Bước 6: Tạo Biểu đồ Sân vận động và Bàn thắng [Combo Chart]
1. Chọn biểu tượng **Line and clustered column chart** và đặt tại vị trí `x = 975 px`, `y = 300 px`, `Width = 925 px`, `Height = 385 px`.
2. Cấu hình các trục:
   * **Trục hoành [X-axis]:** Kéo thuộc tính `DIM Game.Stadium`.
   * **Cột đo lường [Column y-axis]:** Kéo `FACT Player Match Perf.Distinct Matches Played` [Số trận đấu diễn ra].
   * **Đường biểu diễn [Line y-axis]:** Kéo `FACT Player Match Perf.Goals` [Tổng số bàn thắng nổ ra tại sân].
3. Giúp phân tích mối tương quan: Nhận diện những sân bóng có mật độ bàn thắng trung bình mỗi trận cao vượt trội.

*Hình 4.20. Cấu hình và kết quả biểu đồ kết hợp Sân vận động và Bàn thắng*

---

### Bước 7: Tạo Biểu đồ Vùng xu hướng bàn thắng [Area Chart]
1. Chọn biểu tượng **Area chart** [biểu đồ vùng] và đặt tại góc dưới bên trái [vị trí `x = 21 px`, `y = 696 px`, `Width = 930 px`, `Height = 385 px`].
2. Cấu hình các trục:
   * **Trục hoành [X-axis]:** Kéo `DIM Time.Month` và `DIM Time.Year`.
   * **Trục tung [Y-axis]:** Kéo `FACT Player Match Perf.Goals`.
3. Bật hiệu ứng chuyển màu Gradient dưới đường diện tích để làm nổi bật sự thăng trầm của nhịp điệu ghi bàn qua từng tháng thi đấu.

*Hình 4.21. Cấu hình và kết quả Area chart thể hiện nhịp điệu ghi bàn theo chuỗi thời gian*

---

### Bước 8: Tạo Bảng hồ sơ chi tiết cầu thủ [Table]
1. Chọn biểu tượng **Table** và đặt tại góc dưới bên phải [vị trí `x = 976 px`, `y = 696 px`, `Width = 924 px`, `Height = 385 px`].
2. Kéo lần lượt các trường thông tin vào ô **Columns**:
   * `DIM Player.Player Name` [Tên cầu thủ].
   * `DIM Player.Age` [Độ tuổi].
   * `DIM Player.Foot` [Chân thuận: Right, Left, Both].
   * `DIM Player.Country Of Citizenship` [Quốc tịch].
   * `FACT Player Match Perf.Assists` [Tổng kiến tạo].
   * `FACT Player Match Perf.Goals` [Tổng bàn thắng].
3. Nhấp vào tiêu đề cột `Goals` trên bảng để sắp xếp giảm dần, đưa các siêu sao săn bàn hàng đầu thế giới lên vị trí dẫn đầu.

*Hình 4.22. Cấu hình và kết quả Table hồ sơ chi tiết cầu thủ*

---

### Bước 9: Hoàn thiện bố cục và Kiểm thử tương tác
Căn chỉnh cân đối các visual và kiểm thử tính năng lọc tương tác: Khi người dùng nhấp chọn một CLB [ví dụ Manchester City] trên biểu đồ thanh ngang, toàn bộ biểu đồ sân vận động, biểu đồ vùng và bảng hồ sơ lập tức lọc hiển thị riêng các thông số của CLB đó.

*Hình 4.23. Kết quả giao diện hoàn chỉnh của Báo biểu 2 trên Power BI Desktop*

---

### 4.4.4 Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 2

1. **Phân hóa sức mạnh tấn công của các CLB:** Các thế lực hàng đầu như Manchester City, Real Madrid, Bayern Munich, Paris Saint-Germain áp đảo tuyệt đối về số lượng bàn thắng và kiến tạo, phản ánh chiều sâu đội hình và triết lý bóng đá tấn công chủ động.
2. **Hiệu ứng Sân vận động [Home Advantage]:** Các sân vận động tổ chức nhiều trận đấu thường đi kèm tổng bàn thắng cao. Tuy nhiên, một số sân vận động có mật độ bàn thắng trung bình rất cao [trên 3.5 bàn/trận], tạo nên thương hiệu của những hiểm địa sôi động nhất.
3. **Đặc tính nhân trắc học của các chân sút:** Bảng hồ sơ cho thấy phần lớn cầu thủ ghi bàn thuận chân phải [Right], nhưng nhóm cầu thủ thuận chân trái [Left] lại có tỷ lệ kiến tạo thành bàn và tạo đột biến cực cao từ hành lang cánh. Độ tuổi sung mãn nhất của các chân sút chủ lực phân bổ trong khoảng 23 đến 30 tuổi.

---

### 4.5.45 Báo biểu 3: Báo biểu Kỷ luật Thẻ phạt, Cường độ Thi đấu & Tải trọng Cầu thủ

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 3** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 3:**
> Giám sát toàn diện tình hình kỷ luật sân cỏ [Thẻ vàng, Thẻ đỏ], phân tích mức độ quyết liệt của các CLB, cơ cấu thẻ đỏ theo vị trí thi đấu chi tiết [Sub Position], tương quan giữa độ tuổi cầu thủ với thời lượng ra sân và số thẻ phạt, cùng xu hướng tích lũy đóng góp bàn thắng [Goal Contributions] của các CLB qua các mùa giải.

---

#### 4.5.45.1 Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live trực tiếp từ SSAS.
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước Custom `1920 x 1080 px` [chuẩn Full HD 16:9], Canvas Background màu sáng `#F8FAFC`.

---

#### 4.5.45.2 Danh mục Thành phần Trực quan trên Báo biểu 3

Báo biểu 3 tích hợp 13 visual trực quan phân tích kỷ luật và thể lực:

| STT | Tên thành phần Visual | Loại trực quan | Thuộc tính / Độ đo ánh xạ | Vai trò nghiệp vụ |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Banner Tiêu đề | TextBox | Tiêu đề báo biểu 3 | Định danh nghiệp vụ Dashboard |
| **2** | Card Tổng thẻ vàng | Card | `Yellow Cards` | Tổng số thẻ vàng bị phạt |
| **3** | Card Tổng thẻ đỏ | Card | `Red Cards` | Tổng số thẻ đỏ bị truất quyền thi đấu |
| **4** | Card Tổng lượt ra sân | Card | `FACT Player Match Perf Count` | Tổng số lượt cầu thủ thi đấu |
| **5** | Card Tổng thời lượng | Card | `Minutes Played` | Tổng thời lượng thi đấu trên sân |
| **6** | Slicer Cầu thủ | Slicer [Dropdown] | `DIM Player.Player Name` | Lọc theo cá nhân cầu thủ |
| **7** | Slicer Tên giải đấu | Slicer [Dropdown] | `DIM Competition.Competition Name` | Lọc theo giải đấu cụ thể |
| **8** | Slicer Mùa giải | Slicer [Dropdown] | `DIM Time.Season` | Lọc theo mùa bóng |
| **9** | Slicer Vị trí chi tiết | Slicer [Dropdown] | `DIM Player.Sub Position` | Lọc theo vị trí thi đấu chi tiết |
| **10** | Biểu đồ Thẻ phạt theo CLB | Clustered Bar Chart | Y: `Club Name`<br>X: `Yellow Cards`, `Red Cards` | So sánh kỷ luật giữa các CLB |
| **11** | Biểu đồ Vùng xếp chồng G+A | Stacked Area Chart | X: `Season`, `Month`<br>Y: `Goal Contributions`<br>Series: `Club Name` | Tích lũy đóng góp bàn thắng theo thời gian |
| **12** | Biểu đồ Phút & Thẻ theo tuổi | Line & Clustered Column Combo Chart | X: `Age`<br>Column Y: `Minutes Played`<br>Line Y: `Yellow Cards` | Tương quan tải trọng và rủi ro thẻ phạt |
| **13** | Biểu đồ Cơ cấu Thẻ đỏ | Donut Chart | Category: `Sub Position`<br>Y: `Red Cards` | Tỷ trọng thẻ đỏ theo vị trí chiến thuật |

---

#### 4.5.45.3 Quy trình Thiết lập Chi tiết Từng bước trên Power BI

### Bước 1: Tạo trang báo cáo mới và Cấu hình Canvas
1. Nhấp vào dấu cộng [+] để tạo trang mới và đổi tên thành **Báo biểu 3**.
2. Tại bảng Format page ở khung bên phải, chọn **Canvas settings** $\rightarrow$ Type chọn **Custom** $\rightarrow$ Width `1920 px`, Height `1080 px`.

*Hình 4.24. Khởi tạo trang report Báo biểu 3 và cấu hình Canvas chuẩn 1920x1080*

---

### Bước 2: Tạo Banner Tiêu đề cho Báo biểu 3
1. Chọn thẻ **Insert** $\rightarrow$ chọn **Text box**, đặt tại vị trí `x = 10 px`, `y = 10 px` với kích thước `Width = 1880 px`, `Height = 70 px`.
2. Nhập nội dung: **`BÁO BIỂU: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ`**.
3. Định dạng chữ in hoa đậm, font Segoe UI / Arial, cỡ `18 pt`, màu xanh tím than `#1B365D`, căn giữa.

*Hình 4.25. Tạo Text box tiêu đề cho Báo biểu 3*

---

### Bước 3: Tạo và cấu hình hàng thẻ chỉ số KPI Kỷ luật & Thể lực [Cards Row]
Kéo thả 4 visual dạng **Card** vào hàng trên cùng [tọa độ `y = 90 px`, chiều cao `Height = 90 px`, chiều rộng `Width = 455 px`]:
1. **Card 1 [Tổng thẻ vàng]:** Kéo `FACT Player Match Perf.Yellow Cards` vào ô **Values**. Đổi tên hiển thị thành `Tổng thẻ vàng`. Vị trí: `x = 20 px`.
2. **Card 2 [Tổng thẻ đỏ]:** Kéo `FACT Player Match Perf.Red Cards` vào ô **Values**. Đổi tên hiển thị thành `Tổng thẻ đỏ`. Vị trí: `x = 495 px`.
3. **Card 3 [Tổng lượt ra sân]:** Kéo `FACT Player Match Perf.FACT Player Match Perf Count` vào ô **Values**. Đổi tên hiển thị thành `Tổng lượt ra sân`. Vị trí: `x = 970 px`.
4. **Card 4 [Tổng thời lượng]:** Kéo `FACT Player Match Perf.Minutes Played` vào ô **Values**. Đổi tên hiển thị thành `Tổng thời lượng thi đấu`. Vị trí: `x = 1445 px`.

*Hình 4.26. Cấu hình và kết quả 4 thẻ Card KPI Báo biểu 3*

---

### Bước 4: Tạo và cấu hình hàng bộ lọc tương tác [Slicers Row]
Kéo thả 4 visual dạng **Slicer** vào hàng thứ hai [tọa độ `y = 200 px`, chiều cao `Height = 75 px`, chiều rộng `Width = 455 px`]:
1. **Slicer 1 [Cầu thủ]:** Kéo `DIM Player.Player Name` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 20 px`.
2. **Slicer 2 [Giải đấu]:** Kéo `DIM Competition.Competition Name` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 495 px`.
3. **Slicer 3 [Mùa giải]:** Kéo `DIM Time.Season` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 969 px`.
4. **Slicer 4 [Vị trí chi tiết]:** Kéo `DIM Player.Sub Position` vào ô **Field**, định dạng Dropdown. Vị trí: `x = 1445 px`.

*Hình 4.27. Cấu hình hàng Slicer bộ lọc cho Báo biểu 3*

---

### Bước 5: Tạo Biểu đồ Thẻ phạt theo CLB [Clustered Bar Chart]
1. Chọn biểu tượng **Clustered bar chart** và đặt tại vị trí `x = 20 px`, `y = 300 px`, `Width = 925 px`, `Height = 385 px`.
2. Cấu hình các trục:
   * **Trục tung [Y-axis]:** Kéo `DIM Club.Club Name`.
   * **Trục hoành [X-axis]:** Kéo `FACT Player Match Perf.Yellow Cards` và `FACT Player Match Perf.Red Cards`.
3. Sắp xếp giảm dần theo số thẻ vàng. Biểu đồ giúp so sánh mức độ quyết liệt trong lối chơi và kỷ luật sân cỏ giữa các câu lạc bộ.

*Hình 4.28. Cấu hình và kết quả Clustered bar chart kỷ luật thẻ phạt CLB*

---

### Bước 6: Tạo Biểu đồ Vùng xếp chồng G+A theo CLB [Stacked Area Chart]
1. Chọn biểu tượng **Stacked area chart** [biểu đồ vùng xếp chồng] và đặt tại vị trí `x = 975 px`, `y = 300 px`, `Width = 925 px`, `Height = 385 px`.
2. Cấu hình các trục:
   * **Trục hoành [X-axis]:** Kéo `DIM Time.Season` và `DIM Time.Month`.
   * **Trục tung [Y-axis]:** Kéo `FACT Player Match Perf.Goal Contributions`.
   * **Chuỗi phân loại [Legend / Series]:** Kéo `DIM Club.Club Name`.
3. Thể hiện sự đóng góp thị phần bàn thắng và kiến tạo tích lũy của từng đội bóng trong bức tranh tổng thể qua các tháng.

*Hình 4.29. Cấu hình và kết quả Stacked area chart tích lũy đóng góp bàn thắng*

---

### Bước 7: Tạo Biểu đồ Phút thi đấu và Thẻ vàng theo Độ tuổi [Combo Chart]
1. Chọn biểu tượng **Line and clustered column chart** và đặt tại góc dưới bên trái [vị trí `x = 21 px`, `y = 696 px`, `Width = 930 px`, `Height = 385 px`].
2. Cấu hình các trục:
   * **Trục hoành [X-axis]:** Kéo `DIM Player.Age`.
   * **Cột đo lường [Column y-axis]:** Kéo `FACT Player Match Perf.Minutes Played`.
   * **Đường biểu diễn [Line y-axis]:** Kéo `FACT Player Match Perf.Yellow Cards`.
3. Giúp phát hiện mối tương quan: Lứa tuổi nào gánh khối lượng thi đấu nặng nhất và lứa tuổi nào có rủi ro nhận thẻ cao nhất.

*Hình 4.30. Cấu hình và kết quả biểu đồ thể lực và thẻ vàng theo độ tuổi*

---

### Bước 8: Tạo Biểu đồ Cơ cấu Thẻ đỏ theo Vị trí thi đấu [Donut Chart]
1. Chọn biểu tượng **Donut chart** [biểu đồ vành khuyên] và đặt tại góc dưới bên phải [vị trí `x = 976 px`, `y = 696 px`, `Width = 924 px`, `Height = 385 px`].
2. Cấu hình các vùng:
   * **Phân loại [Legend / Category]:** Kéo `DIM Player.Sub Position`.
   * **Giá trị [Values]:** Kéo `FACT Player Match Perf.Red Cards`.
3. Vào Format visual $\rightarrow$ Data labels $\rightarrow$ Label contents chọn **Category, percent of total** để hiển thị trực tiếp tỷ trọng phần trăm thẻ đỏ của từng vị trí.

*Hình 4.31. Cấu hình và kết quả Donut chart cơ cấu thẻ đỏ theo vị trí thi đấu*

---

### Bước 9: Hoàn thiện bố cục và Kiểm thử tương tác
Căn chỉnh các visual cân đối và kiểm thử lọc chéo: Khi lọc `Sub Position` = `Centre-Back` [Trung vệ], biểu đồ theo độ tuổi lập tức phản ánh khối lượng phút thi đấu và thẻ phạt của riêng các trung vệ, đồng thời biểu đồ CLB làm rõ đội bóng nào có hàng thủ nhận nhiều thẻ phạt nhất.

*Hình 4.32. Kết quả giao diện hoàn chỉnh của Báo biểu 3 trên Power BI Desktop*

---

### 4.5.4 Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 3

1. **Rủi ro thẻ đỏ theo vị trí chiến thuật:** Biểu đồ Donut chỉ ra thẻ đỏ tập trung chủ yếu ở hai vị trí trọng yếu nơi hàng thủ: Trung vệ [Centre-Back] và Tiền vệ phòng ngự [Defensive Midfield] do thường xuyên phải thực hiện các pha phạm lỗi chiến thuật ngăn chặn bàn thắng.
2. **Quy luật thể lực và tâm lý theo độ tuổi:** Giai đoạn 24 đến 29 tuổi gánh tải trọng thi đấu lớn nhất [Minutes Played đạt đỉnh] và nhận số lượng thẻ vàng nhiều nhất. Tuy nhiên, tỷ lệ thẻ phạt trên số phút ra sân của các cầu thủ trẻ dưới 21 tuổi lại cao hơn do sự non nớt và nóng vội trong các pha tranh chấp.
3. **Mối liên hệ giữa kỷ luật và thành tích:** Biểu đồ Stacked Area chứng minh các câu lạc bộ duy trì được tỷ lệ đóng góp bàn thắng ổn định qua từng tháng đều là những đội bóng giữ được kỷ luật fair-play và bảo toàn được lực lượng qua các giai đoạn căng thẳng của mùa giải.

---

## 4.6 Đánh giá Tổng hợp và Khả năng Tương tác Đa chiều

Hệ thống 3 báo biểu Power BI kết nối SSAS Live Connection tạo thành một giải pháp phân tích Business Intelligence hoàn chỉnh cho bóng đá chuyên nghiệp:
1. **Khả năng Drill Down linh hoạt:** Cho phép đào sâu dữ liệu từ cấp độ loại giải $\rightarrow$ quốc gia $\rightarrow$ giải đấu $\rightarrow$ vòng đấu, hoặc từ năm $\rightarrow$ quý $\rightarrow$ tháng $\rightarrow$ ngày chỉ bằng các thao tác nhấp chuột trực quan.
2. **Tính năng lọc chéo tức thì [Cross-filtering & Highlighting]:** Người dùng có thể nhấp vào bất kỳ đối tượng nào [một thanh CLB, một lát cắt vị trí thi đấu, một điểm thời gian] để toàn bộ trang báo cáo lọc động theo ngữ cảnh được chọn.
3. **Tốc độ phản hồi và hiệu năng tối ưu:** Tốc độ phản hồi của hệ thống báo cáo luôn đạt mức dưới 1 giây đối với mọi thao tác tương tác nhờ cơ chế tối ưu hóa truy vấn của SSAS Cube.
