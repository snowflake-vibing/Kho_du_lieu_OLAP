# 4.2.1 Báo biểu 1: Báo biểu Tổng hợp Hiệu suất Tấn công theo Cấu trúc Giải đấu & Huấn luyện viên

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 1** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 1:**
> Thống kê tổng hợp quy mô tổ chức thi đấu, số lượng huấn luyện viên và hiệu suất tấn công [Bàn thắng, Kiến tạo] theo cấu trúc đa tầng phân cấp giải đấu [Loại giải đấu $\rightarrow$ Quốc gia $\rightarrow$ Giải đấu $\rightarrow$ Vòng đấu] và tiến trình chuỗi thời gian [Năm $\rightarrow$ Quý $\rightarrow$ Tháng $\rightarrow$ Ngày] kết hợp với thời lượng thi đấu [Minutes Played].

---

## 1. Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live [kết nối trực tiếp đến khối cơ sở dữ liệu SSAS Multidimensional].
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước tùy chỉnh Custom `1920 x 1080 px` [tỷ lệ chuẩn 16:9], Canvas Background màu sáng `#F8FAFC`.

---

## 2. Danh mục Thành phần Trực quan trên Báo biểu 1

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

## 3. Quy trình Thiết lập Chi tiết Từng bước trên Power BI

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

## 4. Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 1

Từ các số liệu trực quan hóa trên Báo biểu 1, nhóm rút ra các nhận định phân tích nghiệp vụ sâu sắc:
1. **Phân bổ quy mô giải đấu:** Các giải đấu Vô địch Quốc gia [domestic_league] chiếm hơn $85\%$ tổng số trận đấu và tổng số bàn thắng, giữ vai trò nền tảng cho toàn bộ hoạt động bóng đá đỉnh cao châu Âu.
2. **Sức mạnh hỏa lực các giải đấu hàng đầu:** Ngoại Hạng Anh [Premier League] và LaLiga [Tây Ban Nha] dẫn đầu toàn châu lục về tổng sản lượng bàn thắng và kiến tạo, đồng thời quy tụ số lượng huấn luyện viên trưởng danh tiếng đông đảo nhất.
3. **Tính chu kỳ thi đấu theo mùa:** Biểu đồ kết hợp chuỗi thời gian vạch rõ hai giai đoạn bùng nổ bàn thắng mạnh mẽ nhất trong năm: Giai đoạn tháng 12 đến tháng 1 [lịch thi đấu mùa đông dày đặc] và giai đoạn tháng 4 đến tháng 5 [giai đoạn đua tranh vô địch và trụ hạng khốc liệt].
4. **Tương quan giữa thể lực và hiệu quả tấn công:** Đường biểu diễn số phút thi đấu [Minutes Played] tỷ lệ thuận hoàn hảo với số lượng bàn thắng, khẳng định chiều sâu đội hình và khả năng duy trì thể lực liên tục là nhân tố quyết định đến sự bùng nổ bàn thắng của các đội bóng.
