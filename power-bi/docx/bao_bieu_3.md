### 4.2.3 Báo biểu 3

**Nội dung:** Thống kê và giám sát tình hình kỷ luật thẻ phạt gồm thẻ vàng và thẻ đỏ, cường độ hoạt động và tải trọng thi đấu theo câu lạc bộ, phân tích xu hướng tích lũy đóng góp bàn thắng qua các mùa giải, khảo sát tương quan thời lượng thi đấu với số thẻ phạt theo độ tuổi cầu thủ và cơ cấu tỷ trọng thẻ đỏ theo vị trí thi đấu chi tiết.

**Bước 1:** Tạo một trang report mới tương tự Báo biểu 1 và 2 bằng cách nhấp dấu cộng ở thanh điều hướng phía dưới và đặt tên là **Báo biểu 3**. Điều chỉnh kích thước Canvas settings sang **Custom** với Width `1920 px`, Height `1080 px`. Tạo một **Text box** tiêu đề đặt ở mép trên trang báo cáo với nội dung: **`BÁO BIỂU: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ`**, định dạng chữ in đậm cỡ `18 pt` và căn giữa.

*Hình 4.30. Text box tiêu đề của Báo biểu 3*

**Bước 2:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành hàng ngang ngay dưới tiêu đề và gán các thước đo từ `FACT Player Match Perf` vào ô **Fields**:
* ● Card 1: Kéo thước đo **`Yellow Cards`** để hiển thị tổng số thẻ vàng.
* ● Card 2: Kéo thước đo **`Red Cards`** để hiển thị tổng số thẻ đỏ.
* ● Card 3: Kéo thước đo **`FACT Player Match Perf Count`** để hiển thị tổng lượt cầu thủ ra sân.
* ● Card 4: Kéo thước đo **`Minutes Played`** để hiển thị tổng thời lượng thi đấu.

*Hình 4.31. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 3*

**Bước 3:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển sang kiểu **Dropdown** và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo tên cầu thủ.
* ● Slicer 2: Kéo **`DIM Competition.Competition Name`** vào ô Field để lọc theo giải đấu.
* ● Slicer 3: Kéo **`DIM Time.Season`** vào ô Field để lọc theo mùa giải.
* ● Slicer 4: Kéo **`DIM Player.Sub Position`** vào ô Field để lọc theo vị trí thi đấu chi tiết.

*Hình 4.32. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 3*

**Bước 4:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào góc trên bên trái trang báo cáo và thiết lập:
* ● Tại mục **Y-axis**, kéo trường **`DIM Club.Club Name`**.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Yellow Cards`** và **`Red Cards`**.
* ● Sắp xếp giảm dần theo `Yellow Cards` để nhận diện nhanh các câu lạc bộ nhận nhiều thẻ phạt nhất.

*Hình 4.33. Cấu hình và kết quả Clustered bar chart so sánh thẻ phạt theo CLB*

**Bước 5:** Kéo thả một biểu đồ vùng xếp chồng **Stacked area chart** vào góc trên bên phải trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Time.Season`** và **`DIM Time.Month`**.
* ● Tại mục **Y-axis**, kéo thước đo **`Goal Contributions`**.
* ● Tại mục **Legend**, kéo trường **`DIM Club.Club Name`** để phân tách đóng góp bàn thắng và kiến tạo của từng câu lạc bộ qua thời gian.

*Hình 4.34. Cấu hình và kết quả Stacked area chart đóng góp bàn thắng theo CLB*

**Bước 6:** Kéo thả một biểu đồ kết hợp **Line and clustered column chart** vào góc dưới bên trái trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Player.Age`**.
* ● Tại mục **Column y-axis**, kéo thước đo **`Minutes Played`** để biểu diễn khối lượng thời gian thi đấu theo từng độ tuổi.
* ● Tại mục **Line y-axis**, kéo thước đo **`Yellow Cards`** để vẽ đường biểu diễn số thẻ vàng phát sinh ở mỗi lứa tuổi.

*Hình 4.35. Cấu hình và kết quả biểu đồ kết hợp Thời lượng thi đấu và Thẻ vàng theo độ tuổi*

**Bước 7:** Kéo thả một biểu đồ vành khuyên **Donut chart** vào góc dưới bên phải trang báo cáo và thiết lập:
* ● Tại mục **Legend**, kéo trường **`DIM Player.Sub Position`**.
* ● Tại mục **Values**, kéo thước đo **`Red Cards`**.
* ● Mở rộng Format visual $\rightarrow$ **Detail labels** $\rightarrow$ tại Label contents chọn **Category, percent of total** để hiển thị tỷ trọng phần trăm thẻ đỏ theo từng vị trí chiến thuật.

*Hình 4.36. Cấu hình và kết quả Donut chart cơ cấu thẻ đỏ theo vị trí thi đấu*

**Bước 8:** Điều chỉnh lại vị trí và kích thước các biểu đồ cho phù hợp với bố cục tổng thể của trang báo cáo, kiểm thử tính năng lọc chéo đồng bộ khi chọn từng vị trí thi đấu hoặc câu lạc bộ.

*Hình 4.37. Kết quả hoàn chỉnh của Báo biểu 3*
