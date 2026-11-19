## 4.2 Quá trình lập báo biểu bằng công cụ Power BI

### 4.2.1 Báo biểu 1

**Nội dung:** Thống kê tổng hợp quy mô tổ chức thi đấu, số lượng huấn luyện viên và hiệu suất tấn công gồm Bàn thắng và Kiến tạo theo cấu trúc phân cấp giải đấu từ Loại giải đấu, Quốc gia, Tên giải đấu đến Vòng đấu, kết hợp theo tiến trình thời gian từ Năm, Quý, Tháng đến Ngày và tương quan với tổng thời lượng thi đấu trên sân.

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

**Bước 6:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành một hàng ngang ngay dưới tiêu đề, lần lượt gán các thước đo từ nhóm `FACT Player Match Perf` vào ô **Fields**:
* ● Card 1: Kéo thước đo **`Distinct Matches Played`** để hiển thị tổng số trận đấu.
* ● Card 2: Kéo thước đo **`Total Coaches`** để hiển thị tổng số huấn luyện viên.
* ● Card 3: Kéo thước đo **`Goals`** để hiển thị tổng số bàn thắng.
* ● Card 4: Kéo thước đo **`Assists`** để hiển thị tổng số pha kiến tạo.

*Hình 4.15. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 1*

**Bước 7:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển kiểu hiển thị sang dạng **Dropdown** trong mục Slicer settings và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Competition.Competition Name`** vào ô Field để lọc theo tên giải đấu.
* ● Slicer 2: Kéo **`DIM Competition.Country Name`** vào ô Field để lọc theo quốc gia tổ chức.
* ● Slicer 3: Kéo **`DIM Club.Club Name`** vào ô Field để lọc theo câu lạc bộ.
* ● Slicer 4: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo từng cầu thủ.

*Hình 4.16. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 1*

**Bước 8:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào khu vực bên trái trang báo cáo và thiết lập các trường dữ liệu:
* ● Tại mục **Y-axis**, kéo lần lượt 4 thuộc tính theo thứ tự phân cấp: `DIM Competition.Competition Type`, `DIM Competition.Country Name`, `DIM Competition.Competition Name` và `DIM Game.Round` để hỗ trợ khoan sâu dữ liệu Drill Down qua 4 cấp độ.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Goals`** và **`Assists`** từ `FACT Player Match Perf`.
* ● Bật **Data labels** để hiển thị trực tiếp số bàn thắng và kiến tạo trên từng thanh biểu đồ.

*Hình 4.17. Cấu hình các trục dữ liệu cho Clustered bar chart phân cấp giải đấu*

*Hình 4.18. Kết quả biểu đồ Clustered bar chart của Báo biểu 1*

**Bước 9:** Kéo thả một biểu đồ kết hợp **Line and stacked column chart** vào khu vực bên phải trang báo cáo và thiết lập các trường dữ liệu:
* ● Tại mục **X-axis**, kéo lần lượt phân cấp thời gian từ `DIM Time`: `Year`, `Quarter`, `Month` và `Day`.
* ● Tại mục **Column y-axis**, kéo 2 thước đo **`Goals`** và **`Assists`**.
* ● Tại mục **Line y-axis**, kéo thước đo **`Minutes Played`** để biểu diễn tổng thời lượng thi đấu.
* ● Mở rộng mục Format visual, bật **Secondary y-axis** để tách riêng thang đo thời lượng phút thi đấu với thang đo bàn thắng và kiến tạo.

*Hình 4.19. Cấu hình Line and stacked column chart chuỗi thời gian*

*Hình 4.20. Kết quả biểu đồ kết hợp chuỗi thời gian của Báo biểu 1*

**Bước 10:** Điều chỉnh lại vị trí, kích thước và căn lề các biểu đồ cho cân đối trên trang báo cáo, kiểm thử tính năng lọc chéo Cross-filtering giữa các bộ lọc Slicer và các biểu đồ.

*Hình 4.21. Kết quả hoàn chỉnh của Báo biểu 1*
