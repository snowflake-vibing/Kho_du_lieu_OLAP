## 4.2 Quá trình lập báo biểu bằng công cụ Power BI

### 4.2.1 Báo biểu 1

**Nội dung:** Thống kê tổng hợp quy mô tổ chức thi đấu, số lượng huấn luyện viên, hiệu suất tấn công gồm Bàn thắng và Kiến tạo theo cấu trúc phân cấp giải đấu từ Loại giải đấu, Quốc gia, Tên giải đấu đến Vòng đấu, kết hợp tiến trình thời gian từ Năm, Quý, Tháng đến Ngày, đồng thời xây dựng ma trận phân nhóm tổng hợp từ Giải đấu, Câu lạc bộ đến từng Cầu thủ kèm các chỉ số thi đấu và thẻ phạt.

**Bước 1:** Tại màn hình làm việc chính của phần mềm Power BI Desktop, trên thanh công cụ Home, nhấp chuột vào mục **Get data**.

*Hình 4.10. Chọn phương thức lấy dữ liệu của Power BI*

**Bước 2:** Trong danh sách các nguồn dữ liệu hiển thị, chọn nhóm Database và nhấp chọn **SQL Server Analysis Services database**, sau đó nhấn nút **Connect**.

*Hình 4.11. Màn hình chọn SQL Server Analysis Services database*

**Bước 3:** Nhập tên Server là `localhost` hoặc tên máy chủ cục bộ `DESKTOP-9B88R8P`, nhập tên Database là `SSAS_Football_Transfermarkt`, tích chọn chế độ **Connect live** rồi ấn nút **OK**. Trong cửa sổ Navigator, chọn khối đa chiều **`DW Football Transfermarkt`** và nhấn **OK** để kết nối trực tiếp đến Cube OLAP.

*Hình 4.12. Cấu hình kết nối Connect live tới SQL Server Analysis Services database*

**Bước 4:** Điều chỉnh kích thước trang báo cáo cho phù hợp không gian hiển thị đa biểu đồ. Tại khung **Format page** bên phải, mở rộng mục **Canvas settings**, tại ô **Type** chọn **Custom**, thiết lập **Width** là `1920 px` và **Height** là `1080 px`.

*Hình 4.13. Cấu hình Canvas settings chuẩn 1920x1080 cho Báo biểu 1*

**Bước 5:** Trên thẻ **Insert**, chọn **Text box** để tạo khung tiêu đề đặt ở mép trên trang báo cáo. Nhập nội dung tiêu đề: **`BÁO BIỂU: TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO CẤU TRÚC GIẢI ĐẤU & HUẤN LUYỆN VIÊN`**, định dạng chữ in đậm cỡ `18 pt` và căn giữa.

*Hình 4.14. Text box tiêu đề của Báo biểu 1*

**Bước 6:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành một hàng ngang ngay dưới tiêu đề, lần lượt gán các thước đo từ nhóm `FACT Player Match Perf` vào ô **Fields** và đặt Title tương ứng:
* ● Card 1: Kéo thước đo **`Distinct Matches Played`**, đặt Title là `Matches Played`.
* ● Card 2: Kéo thước đo **`Total Coaches`**, đặt Title là `Total Coaches`.
* ● Card 3: Kéo thước đo **`Goals`**, đặt Title là `Goals`.
* ● Card 4: Kéo thước đo **`Assists`**, đặt Title là `Assists`.

*Hình 4.15. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 1*

**Bước 7:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển kiểu hiển thị sang dạng **Dropdown** trong mục Slicer settings và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Competition.Competition Name`** vào ô Field để lọc theo tên giải đấu.
* ● Slicer 2: Kéo **`DIM Competition.Country Name`** vào ô Field để lọc theo quốc gia tổ chức.
* ● Slicer 3: Kéo **`DIM Club.Club Name`** vào ô Field để lọc theo câu lạc bộ.
* ● Slicer 4: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo từng cầu thủ.

*Hình 4.16. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 1*

**Bước 8:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào góc trên bên trái trang báo cáo và thiết lập các thông số:
* ● Tại mục **Y-axis**, kéo lần lượt 4 thuộc tính theo thứ tự phân cấp: `DIM Competition.Competition Type`, `DIM Competition.Country Name`, `DIM Competition.Competition Name` và `DIM Game.Round` để hỗ trợ khoan sâu dữ liệu Drill Down qua 4 cấp độ.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Goals`** và **`Assists`** từ `FACT Player Match Perf`.
* ● Sắp xếp giảm dần theo `Goals`, bật **Data labels** để hiển thị trực tiếp số liệu trên từng thanh và đặt Title là **`Thông tin ghi bàn theo giải đấu & vòng đấu`**.

*Hình 4.17. Cấu hình các trục dữ liệu cho Clustered bar chart phân cấp giải đấu*

*Hình 4.18. Kết quả biểu đồ Clustered bar chart của Báo biểu 1*

**Bước 9:** Kéo thả một biểu đồ kết hợp **Line and stacked column chart** vào góc dưới bên trái trang báo cáo và thiết lập các thông số:
* ● Tại mục **X-axis**, kéo lần lượt phân cấp thời gian từ `DIM Time`: `Year`, `Quarter`, `Month` và `Day`.
* ● Tại mục **Column y-axis**, kéo 2 thước đo **`Goals`** và **`Assists`**.
* ● Tại mục **Line y-axis**, kéo thước đo **`Minutes Played`** để biểu diễn tổng thời lượng thi đấu.
* ● Bật **Secondary y-axis** để tách riêng thang đo thời lượng phút thi đấu với thang đo bàn thắng và kiến tạo, đặt Title là **`Thông tin thi đấu và ghi bàn theo thời gian`**.

*Hình 4.19. Cấu hình Line and stacked column chart chuỗi thời gian*

*Hình 4.20. Kết quả biểu đồ kết hợp chuỗi thời gian của Báo biểu 1*

**Bước 10:** Kéo thả một bảng ma trận **Matrix** vào toàn bộ khu vực cột bên phải trang báo cáo để lập báo cáo dạng phân nhóm và tổng hợp Grouping and Totals:
* ● Tại mục **Rows**, kéo lần lượt 3 cấp phân nhóm: **`DIM Competition.Competition Name`**, **`DIM Club.Club Name`** và **`DIM Player.Player Name`**.
* ● Tại mục **Values**, kéo lần lượt 4 thước đo từ `FACT Player Match Perf`: **`Distinct Matches Played`**, **`Minutes Played`**, **`Red Cards`** và **`Yellow Cards`**.
* ● Kích hoạt dòng **Row subtotals** và **Column grand totals** trong Format visual để tự động tính tổng theo từng giải đấu, từng câu lạc bộ và tổng toàn bảng, đặt Title là **`Ma trận phân nhóm theo giải đấu, câu lạc bộ và người chơi`**.

*Hình 4.21. Cấu hình Rows và Values cho bảng Matrix phân nhóm*

*Hình 4.22. Kết quả bảng Matrix phân nhóm của Báo biểu 1*

**Bước 11:** Điều chỉnh lại vị trí, kích thước và căn lề các biểu đồ cho cân đối trên trang báo cáo, kiểm thử tính năng lọc chéo Cross-filtering giữa các bộ lọc Slicer, biểu đồ giải đấu, chuỗi thời gian và bảng ma trận phân nhóm.

*Hình 4.23. Kết quả hoàn chỉnh của Báo biểu 1*
