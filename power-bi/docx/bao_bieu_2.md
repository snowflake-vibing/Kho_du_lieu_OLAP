### 4.2.2 Báo biểu 2

**Nội dung:** Phân tích tiềm năng người chơi và câu lạc bộ thông qua sản lượng bàn thắng, kiến tạo của các đội bóng, đánh giá tác động của sân vận động đến mật độ bàn thắng, theo dõi nhịp điệu săn bàn qua từng tháng và tra cứu hồ sơ nhân trắc học chi tiết của cầu thủ gồm độ tuổi, chân thuận và quốc tịch.

**Bước 1:** Tạo một trang report mới tương tự Báo biểu 1 bằng cách nhấp dấu cộng ở thanh điều hướng phía dưới và đặt tên là **Báo biểu 2**. Điều chỉnh kích thước Canvas settings sang **Custom** với Width `1920 px`, Height `1080 px`. Tạo một **Text box** tiêu đề đặt ở mép trên trang báo cáo với nội dung: **`BÁO BIỂU: PHÂN TÍCH TIỀM NĂNG NGƯỜI CHƠI VÀ CÂU LẠC BỘ`**, định dạng chữ in đậm cỡ `18 pt` và căn giữa.

*Hình 4.22. Text box tiêu đề của Báo biểu 2*

**Bước 2:** Kéo thả 4 thẻ chỉ số tổng quan dạng **Card** đặt thành hàng ngang ngay dưới tiêu đề và gán các thước đo từ `FACT Player Match Perf` vào ô **Fields**:
* ● Card 1: Kéo thước đo **`Distinct Matches Played`** để hiển thị tổng số trận đấu.
* ● Card 2: Kéo thước đo **`Assists`** để hiển thị tổng số kiến tạo.
* ● Card 3: Kéo thước đo **`Goals`** để hiển thị tổng số bàn thắng.
* ● Card 4: Kéo thước đo **`Minutes Played`** để hiển thị tổng số phút thi đấu trên sân.

*Hình 4.23. Cấu hình và kết quả hàng thẻ Card KPI của Báo biểu 2*

**Bước 3:** Kéo thả 4 bộ lọc dạng **Slicer** đặt thành hàng ngang phía dưới các thẻ Card, chuyển sang kiểu **Dropdown** và gán lần lượt các trường dữ liệu:
* ● Slicer 1: Kéo **`DIM Player.Player Name`** vào ô Field để lọc theo từng cầu thủ.
* ● Slicer 2: Kéo **`DIM Club.Club Name`** vào ô Field để lọc theo câu lạc bộ.
* ● Slicer 3: Kéo **`DIM Time.Season`** vào ô Field để lọc theo mùa giải.
* ● Slicer 4: Kéo **`DIM Time.Month`** vào ô Field để lọc theo tháng thi đấu.

*Hình 4.24. Cấu hình hàng Slicer bộ lọc tương tác của Báo biểu 2*

**Bước 4:** Kéo thả một biểu đồ thanh ngang **Clustered bar chart** vào góc trên bên trái trang báo cáo và thiết lập:
* ● Tại mục **Y-axis**, kéo trường **`DIM Club.Club Name`**.
* ● Tại mục **X-axis**, kéo 2 thước đo **`Goals`** và **`Assists`**.
* ● Mở menu More options ở góc biểu đồ, chọn **Sort axis** $\rightarrow$ chọn **Goals** $\rightarrow$ chọn **Sort descending** để xếp các câu lạc bộ ghi nhiều bàn thắng nhất lên đầu.

*Hình 4.25. Cấu hình và kết quả Clustered bar chart so sánh bàn thắng và kiến tạo theo CLB*

**Bước 5:** Kéo thả một biểu đồ kết hợp **Line and clustered column chart** vào góc trên bên phải trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Game.Stadium`**.
* ● Tại mục **Column y-axis**, kéo thước đo **`Distinct Matches Played`** để biểu diễn số trận đấu diễn ra tại mỗi sân vận động.
* ● Tại mục **Line y-axis**, kéo thước đo **`Goals`** để biểu diễn tổng số bàn thắng ghi được tại sân vận động đó.

*Hình 4.26. Cấu hình và kết quả biểu đồ kết hợp Sân vận động và Bàn thắng*

**Bước 6:** Kéo thả một biểu đồ vùng **Area chart** vào góc dưới bên trái trang báo cáo và thiết lập:
* ● Tại mục **X-axis**, kéo trường **`DIM Time.Month`** và **`DIM Time.Year`**.
* ● Tại mục **Y-axis**, kéo thước đo **`Goals`** để theo dõi nhịp điệu và xu hướng ghi bàn qua chuỗi thời gian.

*Hình 4.27. Cấu hình và kết quả Area chart xu hướng ghi bàn theo thời gian*

**Bước 7:** Kéo thả một bảng dữ liệu chi tiết **Table** vào góc dưới bên phải trang báo cáo và kéo lần lượt các trường vào mục **Columns**:
* ● Kéo các thuộc tính hồ sơ cầu thủ từ `DIM Player`: **`Player Name`**, **`Age`**, **`Foot`**, **`Country Of Citizenship`**.
* ● Kéo 2 thước đo hiệu suất từ `FACT Player Match Perf`: **`Assists`** và **`Goals`**.
* ● Nhấp chuột vào tiêu đề cột `Goals` trên bảng để sắp xếp giảm dần danh sách cầu thủ theo số bàn thắng.

*Hình 4.28. Cấu hình và kết quả Table hồ sơ chi tiết cầu thủ*

**Bước 8:** Điều chỉnh lại vị trí và kích thước các biểu đồ cho phù hợp với bố cục tổng thể của trang báo cáo, kiểm thử tính năng lọc chéo đồng bộ giữa câu lạc bộ, sân vận động và hồ sơ cầu thủ.

*Hình 4.29. Kết quả hoàn chỉnh của Báo biểu 2*
