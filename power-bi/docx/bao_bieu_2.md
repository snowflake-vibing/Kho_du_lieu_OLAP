### 4.2.2 Báo biểu 2

**Nội dung:** Phân tích tiềm năng người chơi và câu lạc bộ thông qua sản lượng bàn thắng, kiến tạo của các đội bóng gắn với nhóm Top 10 chân sút hàng đầu, đánh giá tác động của Top 20 sân vận động đến mật độ bàn thắng, theo dõi biến thiên bàn thắng qua từng tháng và tra cứu hồ sơ nhân trắc học chi tiết của cầu thủ gồm độ tuổi, chân thuận và quốc tịch.

**Bước 1:** Tạo một trang report mới tương tự Báo biểu 1 bằng cách nhấp dấu cộng ở thanh điều hướng phía dưới và đặt tên là **Báo biểu 2**. Điều chỉnh kích thước Canvas settings sang **Custom** với Width `1920 px`, Height `1080 px`. Tạo một **Text box** tiêu đề đặt ở mép trên trang báo cáo với nội dung: **`BÁO BIỂU: PHÂN TÍCH TIỀM NĂNG NGƯỜI CHƠI VÀ CÂU LẠC BỘ`**, định dạng chữ in đậm cỡ `18 pt` và căn giữa.

*Hình 4.24. Text box tiêu đề của Báo biểu 2*

**Bước 2:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành hàng ngang ngay dưới tiêu đề, gán các thước đo từ `FACT Player Match Perf` vào ô **Fields** và đặt Title tương ứng:
* ● Card 1: Kéo thước đo **`Distinct Matches Played`**, đặt Title là `Matches Played`.
* ● Card 2: Kéo thước đo **`Assists`**, đặt Title là `Assists`.
* ● Card 3: Kéo thước đo **`Goals`**, đặt Title là `Goals`.
* ● Card 4: Kéo thước đo **`Minutes Played`**, đặt Title là `Total Minutes Played`.

*Hình 4.25. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 2*

**Bước 3:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển sang kiểu **Dropdown** và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo từng cầu thủ.
* ● Slicer 2: Kéo **`DIM Club.Club Name`** vào ô Field để lọc theo câu lạc bộ.
* ● Slicer 3: Kéo **`DIM Time.Season`** vào ô Field để lọc theo mùa giải.
* ● Slicer 4: Kéo **`DIM Time.Month`** vào ô Field để lọc theo tháng thi đấu.

*Hình 4.26. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 2*

**Bước 4:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào góc trên bên trái trang báo cáo và thiết lập:
* ● Tại mục **Y-axis**, kéo trường **`DIM Club.Club Name`**.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Goals`** và **`Assists`**.
* ● Tại khung **Filters on this visual**, kéo `DIM Player.Player Name` vào thiết lập bộ lọc **Top N** chọn **Top 10** theo giá trị **`Goals`** rồi nhấn Apply filter.
* ● Sắp xếp giảm dần theo `Goals` và đặt Title cho biểu đồ là **`Hỏa lực tấn công của các CLB`**.

*Hình 4.27. Cấu hình bộ lọc Top N và kết quả Clustered bar chart hỏa lực các CLB*

**Bước 5:** Kéo thả một biểu đồ kết hợp **Line and clustered column chart** vào góc trên bên phải trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Game.Stadium`**.
* ● Tại mục **Column y-axis**, kéo thước đo **`Distinct Matches Played`** để biểu diễn số trận đấu diễn ra tại mỗi sân vận động.
* ● Tại mục **Line y-axis**, kéo thước đo **`Goals`** để biểu diễn tổng số bàn thắng ghi được tại sân vận động đó.
* ● Tại khung **Filters on this visual**, chọn trường `DIM Game.Stadium`, thiết lập Filter type là **Top N** chọn **Top 20** theo giá trị **`Goals`** rồi nhấn Apply filter.
* ● Sắp xếp giảm dần theo `Distinct Matches Played` và đặt Title là **`Số lượng tổ chức vs Bàn thắng ghi được`**.

*Hình 4.28. Cấu hình bộ lọc Top 20 sân vận động và kết quả biểu đồ kết hợp*

**Bước 6:** Kéo thả một biểu đồ vùng **Area chart** vào góc dưới bên trái trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Time.Month`** và **`DIM Time.Year`**.
* ● Tại mục **Y-axis**, kéo thước đo **`Goals`**.
* ● Bật **Data labels** để hiển thị con số bàn thắng tại từng điểm mốc thời gian và đặt Title là **`Biến thiên bàn thắng theo tháng`**.

*Hình 4.29. Cấu hình và kết quả Area chart biến thiên bàn thắng theo tháng*

**Bước 7:** Kéo thả một bảng dữ liệu chi tiết **Table** vào góc dưới bên phải trang báo cáo và kéo lần lượt các trường vào mục **Columns**:
* ● Kéo các thuộc tính hồ sơ cầu thủ từ `DIM Player`: **`Player Name`**, **`Age`**, **`Foot`**, **`Country Of Citizenship`**.
* ● Kéo 2 thước đo hiệu suất từ `FACT Player Match Perf`: **`Assists`** và **`Goals`**.
* ● Nhấp chuột vào tiêu đề cột `Assists` trên bảng để sắp xếp giảm dần theo số kiến tạo và đặt Title cho bảng là **`Bảng thông tin người chơi`**.

*Hình 4.30. Cấu hình và kết quả Table thông tin người chơi*

**Bước 8:** Điều chỉnh lại vị trí và kích thước các biểu đồ cho phù hợp với bố cục tổng thể của trang báo cáo, kiểm thử tính năng lọc chéo đồng bộ giữa câu lạc bộ, sân vận động và hồ sơ cầu thủ.

*Hình 4.31. Kết quả hoàn chỉnh của Báo biểu 2*
