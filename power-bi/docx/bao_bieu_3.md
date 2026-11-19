### 4.2.3 Báo biểu 3

**Nội dung:** Thống kê và giám sát tình hình kỷ luật thẻ phạt gồm thẻ vàng và thẻ đỏ, cường độ hoạt động và tải trọng thi đấu theo câu lạc bộ, phân tích xếp hạng đóng góp bàn thắng của Top 8 câu lạc bộ qua các tháng, khảo sát tương quan tải trọng thi đấu với thẻ vàng theo độ tuổi cầu thủ và phân bố thẻ đỏ theo vị trí chi tiết trên sân.

**Bước 1:** Tạo một trang report mới tương tự Báo biểu 1 và 2 bằng cách nhấp dấu cộng ở thanh điều hướng phía dưới và đặt tên là **Báo biểu 3**. Điều chỉnh kích thước Canvas settings sang **Custom** với Width `1920 px`, Height `1080 px`. Tạo một **Text box** tiêu đề đặt ở mép trên trang báo cáo với nội dung: **`BÁO BIỂU: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ`**, định dạng chữ in đậm cỡ `18 pt` và căn giữa.

*Hình 4.32. Text box tiêu đề của Báo biểu 3*

**Bước 2:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành hàng ngang ngay dưới tiêu đề, gán các thước đo từ `FACT Player Match Perf` vào ô **Fields** và đặt Title tương ứng:
* ● Card 1: Kéo thước đo **`Yellow Cards`**, đặt Title là `Yellow Cards`.
* ● Card 2: Kéo thước đo **`Red Cards`**, đặt Title là `Red Cards`.
* ● Card 3: Kéo thước đo **`FACT Player Match Perf Count`**, đặt Title là `Total Appearances`.
* ● Card 4: Kéo thước đo **`Minutes Played`**, đặt Title là `Total Minutes Played`.

*Hình 4.33. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 3*

**Bước 3:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển sang kiểu **Dropdown** và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo tên cầu thủ.
* ● Slicer 2: Kéo **`DIM Competition.Competition Name`** vào ô Field để lọc theo giải đấu.
* ● Slicer 3: Kéo **`DIM Time.Season`** vào ô Field để lọc theo mùa giải.
* ● Slicer 4: Kéo **`DIM Player.Sub Position`** vào ô Field để lọc theo vị trí thi đấu chi tiết.

*Hình 4.34. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 3*

**Bước 4:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào góc trên bên trái trang báo cáo và thiết lập:
* ● Tại mục **Y-axis**, kéo trường **`DIM Club.Club Name`**.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Yellow Cards`** và **`Red Cards`**.
* ● Sắp xếp giảm dần theo `Yellow Cards` và đặt Title là **`Thẻ đỏ và vàng của các CLB`**.

*Hình 4.35. Cấu hình và kết quả Clustered bar chart thẻ đỏ và vàng của các CLB*

**Bước 5:** Kéo thả một biểu đồ vùng xếp chồng **Stacked area chart** vào góc trên bên phải trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Time.Season`** và **`DIM Time.Month`**.
* ● Tại mục **Y-axis**, kéo thước đo **`Goal Contributions`**.
* ● Tại mục **Legend**, kéo trường **`DIM Club.Club Name`**.
* ● Tại khung **Filters on this visual**, chọn trường `DIM Club.Club Name`, thiết lập Filter type là **Top N** chọn **Top 8** theo giá trị **`Goal Contributions`** rồi nhấn Apply filter, đặt Title là **`Xếp hạng đóng góp bàn thắng của các CLB qua các tháng`**.

*Hình 4.36. Cấu hình bộ lọc Top 8 CLB và kết quả Stacked area chart*

**Bước 6:** Kéo thả một biểu đồ kết hợp **Line and clustered column chart** vào góc dưới bên trái trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Player.Age`**.
* ● Tại mục **Column y-axis**, kéo thước đo **`Minutes Played`** để biểu diễn khối lượng thời gian thi đấu theo từng độ tuổi.
* ● Tại mục **Line y-axis**, kéo thước đo **`Yellow Cards`** để vẽ đường biểu diễn số thẻ vàng phát sinh ở mỗi lứa tuổi.
* ● Sắp xếp giảm dần theo `Minutes Played` và đặt Title là **`Tương quan tải trọng thi đấu và thẻ vàng theo độ tuổi`**.

*Hình 4.37. Cấu hình và kết quả biểu đồ tương quan tải trọng và thẻ vàng theo độ tuổi*

**Bước 7:** Kéo thả một biểu đồ vành khuyên **Donut chart** vào góc dưới bên phải trang báo cáo và thiết lập:
* ● Tại mục **Legend**, kéo trường **`DIM Player.Sub Position`**.
* ● Tại mục **Values**, kéo thước đo **`Red Cards`**.
* ● Sắp xếp giảm dần theo `Red Cards`, bật **Detail labels** hiển thị `Category, percent of total` và đặt Title là **`Phân bố thẻ đỏ theo vị trí chi tiết trên sân`**.

*Hình 4.38. Cấu hình và kết quả Donut chart phân bố thẻ đỏ theo vị trí chi tiết*

**Bước 8:** Điều chỉnh lại vị trí và kích thước các biểu đồ cho phù hợp với bố cục tổng thể của trang báo cáo, kiểm thử tính năng lọc chéo đồng bộ khi chọn từng vị trí thi đấu hoặc câu lạc bộ.

*Hình 4.39. Kết quả hoàn chỉnh của Báo biểu 3*
