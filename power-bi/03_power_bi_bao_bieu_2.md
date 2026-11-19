# 4.2.2 Báo biểu 2: Báo biểu Phân tích Tiềm năng Người chơi và Câu lạc bộ

Tài liệu này hướng dẫn chi tiết quy trình thiết lập **Báo biểu 2** trên phần mềm **Power BI Desktop**, kết nối trực tiếp [Connect Live] tới khối cơ sở dữ liệu đa chiều SSAS `[DW Football Transfermarkt]`.

> [!NOTE]
> **NỘI DUNG VÀ MỤC TIÊU NGHIỆP VỤ BÁO BIỂU 2:**
> Phân tích chuyên sâu năng lực ghi bàn, kiến tạo và tiềm năng phát triển của từng cầu thủ gắn liền với câu lạc bộ chủ quản, đánh giá tác động của yếu tố địa điểm thi đấu [Sân vận động] đến mật độ bàn thắng, theo dõi nhịp điệu phong độ săn bàn qua từng tháng/năm, và tra cứu hồ sơ nhân trắc học chi tiết [Độ tuổi, Chân thuận, Quốc tịch].

---

## 1. Thông tin chung & Thiết lập Môi trường Kết nối

* **Công cụ thực hiện:** Microsoft Power BI Desktop.
* **Phương thức kết nối:** Connect live trực tiếp từ SSAS.
* **Server Name:** `localhost` [hoặc tên máy tính `DESKTOP-9B88R8P`].
* **Database Catalog:** `SSAS_Football_Transfermarkt`.
* **Cube OLAP:** `DW Football Transfermarkt`.
* **Cấu hình Canvas:** Kích thước Custom `1920 x 1080 px` [chuẩn Full HD 16:9], Canvas Background màu sáng `#F8FAFC`.

---

## 2. Danh mục Thành phần Trực quan trên Báo biểu 2

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

## 3. Quy trình Thiết lập Chi tiết Từng bước trên Power BI

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

## 4. Phân tích Kết quả và Nhận xét Nghiệp vụ Báo biểu 2

1. **Phân hóa sức mạnh tấn công của các CLB:** Các thế lực hàng đầu như Manchester City, Real Madrid, Bayern Munich, Paris Saint-Germain áp đảo tuyệt đối về số lượng bàn thắng và kiến tạo, phản ánh chiều sâu đội hình và triết lý bóng đá tấn công chủ động.
2. **Hiệu ứng Sân vận động [Home Advantage]:** Các sân vận động tổ chức nhiều trận đấu thường đi kèm tổng bàn thắng cao. Tuy nhiên, một số sân vận động có mật độ bàn thắng trung bình rất cao [trên 3.5 bàn/trận], tạo nên thương hiệu của những hiểm địa sôi động nhất.
3. **Đặc tính nhân trắc học của các chân sút:** Bảng hồ sơ cho thấy phần lớn cầu thủ ghi bàn thuận chân phải [Right], nhưng nhóm cầu thủ thuận chân trái [Left] lại có tỷ lệ kiến tạo thành bàn và tạo đột biến cực cao từ hành lang cánh. Độ tuổi sung mãn nhất của các chân sút chủ lực phân bổ trong khoảng 23 đến 30 tuổi.
