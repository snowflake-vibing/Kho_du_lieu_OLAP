# 4.3 Hướng dẫn Toàn diện từ A–Z: Thiết kế 3 Báo biểu trên Google Data Studio (Looker Studio) cho Người Mới Bắt Đầu

Tài liệu này được biên soạn **chi tiết từng cú nhấp chuột (click-by-click)** dành cho người lần đầu sử dụng **Google Data Studio (Looker Studio)**, giúp bạn chuyển đổi mượt mà từ tư duy Power BI sang giao diện Web của Google, từ bước **nạp dữ liệu CSV**, **cài đặt giao diện chuẩn Full HD**, đến **thiết kế hoàn chỉnh 3 Báo biểu** đồng bộ 100% với Power BI.

> [!NOTE]
> **Nguồn dữ liệu sử dụng:** Tệp phẳng **`Football_Report_Data.csv`** (`210,747` dòng, ~74 MB, chuẩn UTF-8) đã được xuất sẵn tại `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`.
> *(Chi tiết 3 báo biểu tách riêng có thể tham khảo thêm tại thư mục [google-data-studio/](file:///d:/Kho_du_lieu_OLAP/google-data-studio/README.md)).*

---

## PHẦN 1: TƯ DUY KHÁC BIỆT GIỮA POWER BI VÀ LOOKER STUDIO (DÀNH CHO NGƯỜI MỚI)

Nếu bạn đã quen Power BI Desktop, hãy nắm **6 quy tắc vàng** này để không bị bỡ ngỡ khi mở Looker Studio:

| Thao tác / Khái niệm | Trong **Power BI Desktop** | Trong **Google Data Studio (Looker Studio)** |
| :--- | :--- | :--- |
| **1. Kết nối dữ liệu** | *Connect live* trực tiếp vào SSAS Cube (`localhost`) | Looker Studio chạy trên Web nên dùng **File Upload** tải tệp **`Football_Report_Data.csv`** lên Google Cloud |
| **2. Bảng cấu hình bên phải** | Gồm **Data** + **Visualizations** (chia làm *Build visual* và *Format visual*) | Bảng Properties bên phải chia làm 2 tab rõ rệt:<br>• Tab **`Setup`** *(Thiết lập)*: Kéo **Dimension** (Chữ/Ngày), **Metric** (Số đo), **Sort**, **Filter**.<br>• Tab **`Style`** *(Kiểu)*: Đổi màu, bật nhãn số, bo góc, cỡ chữ, số thanh hiển thị. |
| **3. Xóa `Record Count` thừa** | Kéo gì hiện nấy | Looker Studio tự động nhét **`Record Count`** vào ô **Metric** mỗi khi bạn tạo biểu đồ mới. Hãy rê chuột vào chữ `Record Count` $\rightarrow$ bấm dấu **`✕`** để xóa đi rồi mới kéo `Goals`, `Assists`... vào! |
| **4. Đổi tên cột & phép tính** | Bấm đúp tên trường hoặc sửa trong Cube | Rê chuột lên **bên trái tên trường** trong ô `Dimension` hoặc `Metric` sẽ hiện **biểu tượng cây bút chì (`✏️`)** $\rightarrow$ Bấm vào đó để đổi tên tiếng Việt, đổi `Sum` / `Average` / `Count Distinct` hoặc đổi kiểu Ngày tháng! |
| **5. Lọc Top 10 (Top N)** | Vào khung Filters $\rightarrow$ chọn *Top N* | **Không có mục Top N trong Filter!** Thay vào đó:<br>• Ở tab **`Setup`** $\rightarrow$ **Sort** theo `Goals` **Descending** (Giảm dần).<br>• Sang tab **`Style`** $\rightarrow$ tìm mục **Bars** (hoặc **Number of bars**) $\rightarrow$ gõ số **`10`**. |
| **6. Slicer (Bộ lọc tương tác)** | Chọn visual *Slicer* trong Visualizations | Trên thanh menu trên cùng, bấm **`Add a control`** *(Thêm bộ điều khiển)* $\rightarrow$ chọn **`Drop-down list`** *(Danh sách thả xuống)*, rồi kéo trường cần lọc vào ô **Control field**. |

---

## PHẦN 2: QUY TRÌNH NẠP DỮ LIỆU & TẠO TRƯỜNG TÍNH TOÁN CHUẨN (BẮT BUỘC LÀM ĐẦU TIÊN)

### Bước 1: Tạo Báo cáo trống và Upload tệp `Football_Report_Data.csv`
1. Mở trình duyệt (Chrome/Edge), truy cập: [https://lookerstudio.google.com/](https://lookerstudio.google.com/) và đăng nhập tài khoản Google.
2. Ở góc trên bên trái, bấm nút **`+ Create`** *(Tạo)* $\rightarrow$ chọn **`Report`** *(Báo cáo)*.
3. Hộp thoại **Add data to report** *(Thêm dữ liệu vào báo cáo)* tự động bật lên:
   * Tại tab **Connect to data**, gõ vào ô tìm kiếm từ khóa **`File Upload`** (hoặc cuộn xuống chọn biểu tượng **File Upload**).
   * Bấm **Authorize** *(Ủy quyền)* nếu là lần đầu sử dụng.
   * Nhấp **`CLICK TO UPLOAD FILES`** $\rightarrow$ tìm chọn tệp:
     `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`
   * Chờ khoảng 15–30 giây cho thanh tiến trình chạy xong và hiện chữ màu xanh **`Uploaded`** *(Đã tải lên)*.
   * Nhấp nút **`Add`** *(Thêm)* ở góc dưới bên phải $\rightarrow$ chọn **`ADD TO REPORT`** *(Thêm vào báo cáo)*.
4. Giao diện thiết kế mở ra kèm 1 bảng mẫu có sẵn ở giữa trang $\rightarrow$ **Nhấp chọn bảng mẫu đó và nhấn phím `Delete`** trên bàn phím để có trang trắng tinh.

---

### Bước 2: Kiểm tra Kiểu dữ liệu & Tạo 2 Trường Tính Toán (Calculated Fields) để khớp 100% số liệu Cube SSAS
Ở cột **`Data`** ngoài cùng bên phải (danh sách các cột của `Football_Report_Data.csv`):

1. **Kiểm tra kiểu dữ liệu (Rất quan trọng):**
   * Nhìn vào biểu tượng bên trái tên trường: `ABC` = Chữ (Text), `123` = Số (Number), `📅` = Ngày (Date).
   * Đảm bảo `Goals`, `Assists`, `Goal_Contributions`, `Minutes_Played`, `Yellow_Cards`, `Red_Cards`, `Stadium_Seats`, `Age` đều có biểu tượng **`123`**.
   * Đảm bảo `Full_Date` có biểu tượng **`📅`**. *(Nếu thấy là `ABC`, bấm menu **Resource** $\rightarrow$ **Manage added data sources** $\rightarrow$ **Edit** để chỉnh lại kiểu thành Date).*
2. **Tạo Calculated Field 1 – `Total Coaches` (ra đúng `175` HLV, loại bỏ `'Unknown Coach'`):**
   * Ở đáy cột **Data** bên phải cùng, bấm **`+ Add a field`** $\rightarrow$ **`Add calculated field`**.
   * **Field Name:** `Total Coaches`
   * **Formula:**
     ```sql
     COUNT_DISTINCT(CASE WHEN Coach_Name != "Unknown Coach" THEN Coach_Name ELSE NULL END)
     ```
   * Bấm **`Save`** *(Lưu)* $\rightarrow$ **`Done`** *(Xong)*.
3. **Tạo Calculated Field 2 – `Distinct Matches` (ra đúng `6,965` trận đấu):**
   * Bấm **`+ Add a field`** $\rightarrow$ **`Add calculated field`**.
   * **Field Name:** `Distinct Matches`
   * **Formula:**
     ```sql
     COUNT_DISTINCT(Game_ID)
     ```
   * Bấm **`Save`** $\rightarrow$ **`Done`**.
4. *(Tùy chọn)* **Tạo Bộ lọc tái sử dụng `Valid_Goals` (Chỉ lấy cầu thủ có ghi bàn `Goals > 0`):**
   * Có thể tạo ngay khi thiết kế biểu đồ ở Bước dưới, hoặc bấm **Resource** $\rightarrow$ **Manage filters** $\rightarrow$ **Add a filter**:
     * **Name:** `Scorers_Only` | **Include** $\rightarrow$ `Goals` $\rightarrow$ **Greater than (`>`)** $\rightarrow$ `0` $\rightarrow$ **Save**.

---

## PHẦN 3: HƯỚNG DẪN DESIGN GIAO DIỆN ĐẸP CHUẨN FULL HD (`1920 x 1080 px`)

Looker Studio mặc định trang rất nhỏ (`1200 x 900`), nếu không chỉnh rộng ra thì đặt 3–4 biểu đồ sẽ bị dính chùm và cắt chữ (`...`). Bạn hãy thiết lập bộ khung chuẩn sau cho **cả 3 trang**:

### Bước 1: Cài đặt Kích thước Canvas & Nền xám hiện đại
1. Trên thanh menu trên cùng, chọn **`Page`** *(Trang)* $\rightarrow$ **`Current page settings`** *(Cài đặt trang hiện tại)*.
2. Ở bảng bên phải, chuyển sang tab **`Style`** *(Kiểu)*:
   * **Display mode** *(Chế độ hiển thị)*: Chọn **`Fit to width`** *(Khớp với chiều rộng)* để khi xem toàn màn hình luôn sắc nét.
   * **Canvas size** *(Kích thước Canvas)*: Chọn **`Custom`** *(Tùy chỉnh)*, nhập:
     * **Width:** **`1920`**
     * **Height:** **`1080`**
3. Đóng bảng cài đặt trang. Vào menu **`Theme and layout`** *(Chủ đề và bố cục)* trên thanh công cụ:
   * Tab **Theme**: Chọn mẫu **`Simple`** (hoặc giữ mặc định), bấm nút **`Customize`** *(Tùy chỉnh)*:
     * **Report background:** Chọn mã màu **`#F8FAFC`** (xám khói nhạt, làm nổi bật các khung biểu đồ trắng).
     * **Component background:** Chọn màu trắng **`#FFFFFF`**, **Component border:** **`#CBD5E1`**.
   * Tab **Layout**:
     * Mục **Snap to:** Chọn **`Grid`** (giúp kéo thả các biểu đồ thẳng hàng tự động).
     * **Grid size:** Đặt **`10 px`**.

### Bước 2: Quy tắc Design "Thẻ Card & Biểu đồ Nổi khối" (Áp dụng chung cho mọi Visual)
Khi cần chỉnh vị trí chính xác từng pixel hoặc bo góc đẹp như Power BI, bạn nhấp chọn visual $\rightarrow$ sang tab **`Style`**:
1. **Bo góc & Viền (Background and border):** Cuộn xuống cuối tab **`Style`**:
   * **Background:** Màu trắng `#FFFFFF` (riêng 4 thẻ KPI trên cùng dùng màu Pastel nhạt: `#EFF6FF`, `#FAF5FF`, `#F0FDF4`, `#FFFBEB`).
   * **Border radius:** Nhập **`10`** (`10 px` bo tròn 4 góc).
   * **Border weight:** `1 px`, **Border color:** `#CBD5E1`.
   * Tích chọn **Add border shadow** *(Thêm đổ bóng)* để biểu đồ nổi khối 3D nhẹ.
2. **Đặt Tọa độ & Kích thước chính xác (không cần căn bằng mắt):**
   * Cuộn xuống dưới cùng của tab **`Style`** $\rightarrow$ tìm mục **`Position`** *(Vị trí)* hoặc nhìn bảng **Position** ngay dưới thẻ Style để gõ trực tiếp 4 thông số **`X`**, **`Y`**, **`Width`**, **`Height`**!
3. **Bật Tiêu đề Biểu đồ (Chart Header):**
   * Looker Studio **không tự bật sẵn tiêu đề** như Power BI!
   * Để thêm tiêu đề cho biểu đồ: Dùng công cụ **`Text`** (biểu tượng chữ `A` trong ô vuông trên thanh công cụ) đặt lên trên đầu biểu đồ (hoặc dùng **Title** trong `Style` $\rightarrow$ `Chart Header` $\rightarrow$ chọn *Always show*, và thêm hộp Text tiêu đề cỡ `16–18 pt Bold` màu `#0F172A` cho đồng nhất).

---

## PHẦN 4: THIẾT KẾ CHI TIẾT 3 BÁO BIỂU (ĐỒNG BỘ 100% VỚI POWER BI)

### 4.3.1 Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp (Grouping and Totals Report)
> **Tên trang:** `Báo biểu 1 - Grouping & Totals`  
> **Mục tiêu:** Đáp ứng tiêu chí *"1 report dạng Grouping and Totals"* với bộ ba visual **Stacked Bar + Stacked Column + Pivot Table** và bộ cột mới (`Coach_Name`, `Competition_Type`, `Competition_Country`, `Match_Round`, `Quarter`).

#### 1. Tạo Banner Tiêu đề & 4 Thẻ KPI (Scorecards) ở phần đầu trang
* **Banner Tiêu đề:** Bấm biểu tượng **Text (`A`)**, vẽ khung tại `X=20, Y=15, W=1880, H=55`, gõ:
  `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG`
  *(Font `Roboto`, `20 pt Bold`, Căn giữa, Nền `#FFFFFF`, Viền `#CBD5E1`, Border radius `10`).*
* **4 Thẻ KPI (`Add a chart` $\rightarrow$ `Scorecard`):** Đặt cùng hàng `Y=85, H=90, W=455`:
  1. **Thẻ 1 (`X=20`):** Xóa `Record Count` $\rightarrow$ kéo **`Distinct Matches`** vào **Metric** $\rightarrow$ bấm `✏️` đổi tên: `Tổng Số Trận Quản Trị` *(ra `6,965`)*. Style: Nền `#EFF6FF`, cỡ số `35 pt Bold`, bật **Compact numbers: OFF**.
  2. **Thẻ 2 (`X=495`):** Kéo **`Total Coaches`** vào **Metric** $\rightarrow$ đổi tên: `Tổng Số HLV Trưởng` *(ra `175`)*. Style: Nền `#FAF5FF`, cỡ số `35 pt Bold`.
  3. **Thẻ 3 (`X=970`):** Kéo **`Goals`** (phép tính `Sum`) $\rightarrow$ đổi tên: `Tổng Bàn Thắng` *(ra `19.17K` khi bật **Compact numbers: ON**)*. Style: Nền `#F0FDF4`.
  4. **Thẻ 4 (`X=1445`):** Kéo **`Goal_Contributions`** (`Sum`) $\rightarrow$ đổi tên: `Tổng Đóng Góp G+A` *(ra `33.91K`)*. Style: Nền `#FFFBEB`.

#### 2. Tạo 4 Bộ lọc (`Add a control` $\rightarrow$ `Drop-down list`)
Đặt hàng ngang `Y=190, H=75, W=455`:
* **Bộ lọc 1 (`X=20`):** Control field = `Season` *(Mùa giải)*.
* **Bộ lọc 2 (`X=495`):** Control field = `Competition_Type` *(Loại giải: Quốc nội vs Cúp Châu lục)*.
* **Bộ lọc 3 (`X=970`):** Control field = `Competition_Country` *(Quốc gia giải đấu)*.
* **Bộ lọc 4 (`X=1445`):** Control field = `Quarter` *(Quý thi đấu Q1–Q4)*.

#### 3. Thiết kế Bộ ba Visual (Thân trang)
1. **Visual 1 (Trên Trái – `Stacked bar chart`):** Đặt tại `X=20, Y=280, W=860, H=380`.
   * **Tab `Setup`:**
     * **Dimension:** Kéo `Competition_Type` $\rightarrow$ gạt công tắc **Drill down** sang **ON** $\rightarrow$ bấm **Add dimension** thêm lần lượt: `Competition_Country` $\rightarrow$ `Competition_Name` $\rightarrow$ `Match_Round`.
     * **Metric:** Xóa `Record Count`, kéo **`Goals`** (`Sum`) và **`Assists`** (`Sum`).
     * **Sort:** `Goals` $\rightarrow$ **Descending**.
     * **Chart interactions:** Tích chọn **`Cross-filtering`** *(để bấm vào giải đấu sẽ lọc luôn bảng HLV bên phải)*.
   * **Tab `Style`:**
     * Chọn kiểu thanh xếp chồng **Stacked bars** (nếu mới tạo là thanh nhóm cạnh nhau thì tích chọn ô **Stacked** trong `Style`).
     * Màu sắc: Series #1 (`Goals`) = `#2563EB` (Xanh dương), Series #2 (`Assists`) = `#06B6D4` (Xanh Cyan).
     * Tích **`Show data labels`** để hiện số liệu trực tiếp trên thanh.

2. **Visual 2 (Dưới Trái – `Stacked column chart`):** Đặt tại `X=20, Y=680, W=860, H=380`.
   * **Tab `Setup`:**
     * **Dimension:** Kéo `Season` $\rightarrow$ bật **Drill down: ON** $\rightarrow$ bấm **Add dimension** thêm `Quarter`.
     * **Metric:** Kéo **`Goals`** (`Sum`) và **`Assists`** (`Sum`).
     * **Chart interactions:** Tích chọn **`Cross-filtering`**.
   * **Tab `Style`:** Đảm bảo tích **Stacked**, màu `#2563EB` & `#06B6D4`, tích **`Show data labels`**.

3. **Visual 3 (Bên Phải – `Pivot table with subtotals` – Chuẩn Grouping & Totals):** Đặt tại `X=900, Y=280, W=1000, H=780`.
   * **Menu chọn:** `Add a chart` $\rightarrow$ kéo xuống nhóm *Pivot table* $\rightarrow$ chọn **`Pivot table with heat map`** hoặc **`Pivot table with bars`** (hoặc `Pivot table` thường rồi bật Bar).
   * **Tab `Setup`:**
     * **Row dimension:** Kéo lần lượt 3 cấp: `Coach_Name` $\rightarrow$ `Club_Name` $\rightarrow$ `Player_Name`.
     * **Column dimension:** Để trống.
     * **Metric:** Xóa `Record Count`, kéo 4 thước đo: `Goals` (`Sum`), `Assists` (`Sum`), `Goal_Contributions` (`Sum`), `Distinct Matches`.
     * **Sorting:** Row #1 sắp xếp theo `Goals` **Descending** (để các HLV hàng đầu như *Pep Guardiola, Xabi Alonso, Arteta...* lên đầu).
     * **Filter:** *(Khuyên dùng)* Tạo Filter loại bỏ `Coach_Name != "Unknown Coach"` nếu chỉ muốn xem HLV có tên tuổi.
   * **Tab `Style` (BƯỚC QUAN TRỌNG NHẤT ĐỂ CÓ GROUPING & TOTALS):**
     * Cuộn tìm mục **Row subtotals** *(Tổng phụ theo hàng)* $\rightarrow$ Tích chọn **Show subtotals**!
     * Tìm mục **Grand total** $\rightarrow$ Tích chọn **Show grand total** cho Rows!
     * Mục **Header:** Nền xanh Navy **`#0F172A`**, chữ Trắng **`#FFFFFF` Bold**.
     * Tại cột thứ 3 (`Goal_Contributions`): Ở mục *Column #3*, đổi từ *Number* sang **`Bar`** (Thanh dữ liệu xanh `#2563EB`) và tích **Show number**.

---

### 4.3.2 Báo biểu 2: Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh (Scouting Elite Clubs & Top Threats)
> **Cách tạo trang mới:** Bấm **`Page`** $\rightarrow$ **`New page`**, đổi tên thành `Báo biểu 2 - Trinh sát Chiến thuật`. Cài đặt lại Canvas `1920 x 1080` (hoặc bấm `Page` $\rightarrow$ `Duplicate page` từ Trang 1 rồi xóa 3 visual thân trang đi để đỡ mất công dựng lại Banner + 4 Cards + 4 Controls!).

* **4 Thẻ KPI (`Y=85, H=90`):** `Distinct Matches` (`6,965`), `Goals` (`19.17K`), `Assists` (`14.74K`), `Goal_Contributions` (`33.91K`).
* **4 Bộ lọc (`Y=190, H=75`):** `Season`, `Competition_Name`, `Sub_Position` *(Vị trí chi tiết)*, `Foot` *(Chân thuận: left/right)*.
* **Lưới 2x2 ở thân trang (`Y=280` trở xuống, mỗi ô `W=925, H=380`):**
  1. **Ô 1 (Trên Trái – `Bar chart` Top 10 CLB Hỏa lực):**
     * `Setup`: Dimension = `Club_Name`; Metric = `Goals` (`Sum`), `Assists` (`Sum`); Sort = `Goals` Descending; Filter = `Scorers_Only`.
     * `Style`: **Number of bars = `10`**, tích **Show data labels**.
  2. **Ô 2 (Trên Phải – `Combo chart` 2 Trục Y: Chảo lửa Sân vận động):**
     * `Setup`: Dimension = `Stadium_Name`; Metric #1 = `Distinct Matches`, Metric #2 = `Goals` (`Sum`); Sort = `Goals` Descending.
     * `Style`: **Number of bars = `10`**; Series #1 (`Distinct Matches`) = **Bars**; Series #2 (`Goals`) = **Line** và tại **Axis** chọn **`Right`** *(Trục phải)* để 2 thang đo không đè nhau!
  3. **Ô 3 (Dưới Trái – `Area chart` Biến thiên Bàn thắng theo Thời gian):**
     * `Setup`: Dimension = `Full_Date` $\rightarrow$ bấm `✏️` chọn **Type: Date & Time $\rightarrow$ `Year Month`** (để vẽ trục tháng liên tục theo năm); Metric = `Goals` (`Sum`).
     * `Style`: Tích **Show points**, chọn màu xanh `#2563EB`.
  4. **Ô 4 (Dưới Phải – `Table with bars` Bảng Trinh sát Mũi nhọn Cầu thủ):**
     * `Setup`: Dimension = `Player_Name`, `Player_Country`, `Sub_Position`, `Foot`, `Age`; Metric = `Goals`, `Assists`, `Goal_Contributions`; Sort = `Goal_Contributions` Descending.
     * `Style`: Cột `Goal_Contributions` chọn hiển thị **Bar** + **Show number**, Header màu `#0F172A` chữ trắng.

---

### 4.3.3 Báo biểu 3: Kỷ luật Thẻ phạt & Tải trọng Thi đấu (Discipline & Physical Workload)
> **Tên trang:** `Báo biểu 3 - Kỷ luật & Thể lực`

* **4 Thẻ KPI (`Y=85, H=90`):** `Yellow_Cards` (`Sum`), `Red_Cards` (`Sum`), `Appearance_ID` (`Count`, đổi tên `Tổng Lượt Ra Sân` = `210.75K`), `Minutes_Played` (`Sum` = `13.56M`).
* **4 Bộ lọc (`Y=190, H=75`):** `Season`, `Competition_Name`, `Competition_Country`, `Main_Position`.
* **Lưới 2x2 ở thân trang (`W=925, H=380` mỗi ô):**
  1. **Ô 1 (Trên Trái – `Stacked bar chart` Top 10 CLB Nhiều thẻ nhất):**
     * `Setup`: Dimension = `Club_Name`; Metric = `Yellow_Cards` (`Sum`), `Red_Cards` (`Sum`); Sort = `Yellow_Cards` Descending.
     * `Style`: Tích **Stacked**, **Number of bars = `10`**, đổi màu `Yellow_Cards` = Vàng hổ phách **`#F59E0B`**, `Red_Cards` = Đỏ **`#EF4444`**, bật **Show data labels**.
  2. **Ô 2 (Trên Phải – `Line chart` Biến động Phút thi đấu theo Giải qua Mùa giải):**
     * `Setup`: Dimension = `Season`; Breakdown Dimension = `Competition_Name`; Metric = `Minutes_Played` (`Sum`).
     * `Style`: Mục *Breakdown dimension* chỉnh số dòng tối đa = `5`–`6` giải đấu lớn cho đỡ rối dây; tích **Show points**.
  3. **Ô 3 (Dưới Trái – `Combo chart` 2 Trục Y: Thể lực & Thẻ phạt theo Độ tuổi):**
     * `Setup`: Dimension = `Age` *(Sort Ascending theo `Age`)*; Metric #1 = `Minutes_Played` (`Sum`), Metric #2 = `Yellow_Cards` (`Sum`).
     * `Style`: Series #1 (`Minutes_Played`) = **Bars** (Axis: `Left`); Series #2 (`Yellow_Cards`) = **Line** (Axis: **`Right`**).
  4. **Ô 4 (Dưới Phải – `Donut chart` Phân bổ Thẻ đỏ theo Vị trí Chi tiết):**
     * `Setup`: Dimension = `Sub_Position`; Metric = `Red_Cards` (`Sum`).
     * `Style`: Kéo thanh trượt **Donut** ở đầu tab Style lên **`50%`** để tạo lỗ tròn ở giữa, **Slices = `8`**, bật hiển thị phần trăm (`Percentage`).

---

## PHẦN 5: KIỂM TRA CHÉO & XUẤT BÁO CÁO (CHẾ ĐỘ VIEW)

1. Nhấp nút **`View`** *(Xem)* màu xanh ở góc trên bên phải màn hình để thoát chế độ thiết kế và trải nghiệm như người dùng cuối.
2. **Kiểm tra 3 điểm chốt:**
   * Bấm vào thanh `uefa-champions-league` trên Visual 1 (Trang 1) $\rightarrow$ Kiểm tra xem 4 thẻ KPI và Bảng Pivot Table HLV có tự động lọc theo Cúp C1 không.
   * Bấm nút mũi tên **`↓` (Drill down)** ở góc trên phải Visual 1 để khoan từ `international_cup` xuống tới `Match_Round` (`Final`, `Semi-Finals`).
   * Bấm vào tab **Share** (góc trên phải) $\rightarrow$ chọn **Download report** (xuất PDF nộp bài) hoặc lấy link chia sẻ cho giảng viên xem trực tuyến!
