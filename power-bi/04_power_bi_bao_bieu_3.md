# 4.2.3 Báo biểu 3: Báo biểu Kỷ luật Thẻ phạt, Cường độ Thi đấu & Tải trọng Cầu thủ

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 3** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 3:**
> Giám sát toàn diện tình hình kỷ luật sân cỏ [Thẻ vàng, Thẻ đỏ], phân tích mức độ quyết liệt của các CLB, cơ cấu thẻ đỏ theo vị trí thi đấu chi tiết [Sub Position], tương quan giữa độ tuổi cầu thủ với thời lượng ra sân và số thẻ phạt, cùng xu hướng tích lũy đóng góp bàn thắng [Goal Contributions] của các CLB qua các mùa giải.

---

## 1. Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live trực tiếp từ SSAS.
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước Custom `1920 x 1080 px` [chuẩn Full HD 16:9], Canvas Background màu sáng `#F8FAFC`.

---

## 2. Danh mục Thành phần Trực quan trên Báo biểu 3

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

## 3. Quy trình Thiết lập Chi tiết Từng bước trên Power BI

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

## 4. Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 3

1. **Rủi ro thẻ đỏ theo vị trí chiến thuật:** Biểu đồ Donut chỉ ra thẻ đỏ tập trung chủ yếu ở hai vị trí trọng yếu nơi hàng thủ: Trung vệ [Centre-Back] và Tiền vệ phòng ngự [Defensive Midfield] do thường xuyên phải thực hiện các pha phạm lỗi chiến thuật ngăn chặn bàn thắng.
2. **Quy luật thể lực và tâm lý theo độ tuổi:** Giai đoạn 24 đến 29 tuổi gánh tải trọng thi đấu lớn nhất [Minutes Played đạt đỉnh] và nhận số lượng thẻ vàng nhiều nhất. Tuy nhiên, tỷ lệ thẻ phạt trên số phút ra sân của các cầu thủ trẻ dưới 21 tuổi lại cao hơn do sự non nớt và nóng vội trong các pha tranh chấp.
3. **Mối liên hệ giữa kỷ luật và thành tích:** Biểu đồ Stacked Area chứng minh các câu lạc bộ duy trì được tỷ lệ đóng góp bàn thắng ổn định qua từng tháng đều là những đội bóng giữ được kỷ luật fair-play và bảo toàn được lực lượng qua các giai đoạn căng thẳng của mùa giải.
