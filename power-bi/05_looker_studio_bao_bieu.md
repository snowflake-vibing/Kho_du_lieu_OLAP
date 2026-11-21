# 4.3 Hướng dẫn Toàn diện từ A–Z: Thiết kế 3 Báo biểu trên Google Data Studio (Looker Studio) cho Người Mới Bắt Đầu

Tài liệu này hướng dẫn **từng cú nhấp chuột (click-by-click)** bằng **giao diện Tiếng Việt** của **Google Data Studio (Looker Studio)**, giúp bạn chuyển đổi mượt mà từ tư duy Power BI sang nền tảng Web của Google: từ bước **nạp tệp CSV**, **tạo tập dữ liệu**, **căn chỉnh giao diện Full HD**, đến **thiết kế hoàn chỉnh 3 Báo biểu** đồng bộ 100% với Power BI.

> [!NOTE]
> **Nguồn dữ liệu sử dụng:** Tệp phẳng **`Football_Report_Data.csv`** (`210,747` dòng, ~64.2 MB, chuẩn UTF-8 — xuất trực tiếp 100% các cột gốc từ `DW_Football_Transfermarkt`, không chứa cột tự chế dư thừa) lưu tại:  
> [Football_Report_Data.csv](file:///D:/Kho_du_lieu_OLAP/football/cleaned_data/Football_Report_Data.csv) (`D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`)
>
> *(Chi tiết 3 báo biểu tách riêng có thể tham khảo thêm tại thư mục [google-data-studio/](file:///d:/Kho_du_lieu_OLAP/google-data-studio/README.md)).*

---

## PHẦN 1: TƯ DUY KHÁC BIỆT GIỮA POWER BI VÀ LOOKER STUDIO

Nếu bạn đã quen Power BI Desktop, hãy nắm **6 điểm khác biệt cốt lõi** này trên giao diện Tiếng Việt của Looker Studio:

| Thao tác / Khái niệm | Trong **Power BI Desktop** | Trong **Looker Studio (Giao diện Tiếng Việt)** |
| :--- | :--- | :--- |
| **1. Kết nối dữ liệu** | *Connect live* trực tiếp tới SSAS Cube (`localhost`) | Chọn trình kết nối **`Tải tệp lên`** (`File Upload`) để nạp tệp `Football_Report_Data.csv` lên Google Cloud |
| **2. Bảng cấu hình bên phải** | Gồm **Data** + **Visualizations** (*Build* / *Format*) | Bảng Thuộc tính bên phải chia làm 2 tab rõ rệt:<br>• Tab **`Thiết lập`** *(Setup)*: Kéo **Phương diện** (Chữ/Ngày), **Chỉ số** (Số đo), **Sắp xếp**, **Bộ lọc**.<br>• Tab **`Kiểu`** *(Style)*: Đổi màu, bật nhãn số, bo góc, cỡ chữ, số thanh hiển thị. |
| **3. Xóa `Record Count` thừa** | Kéo gì hiện nấy | Looker Studio tự chèn **`Record Count`** *(hoặc Số lượng bản ghi)* vào ô **Chỉ số**. Hãy rê chuột vào nó $\rightarrow$ bấm dấu **`✕`** để xóa đi rồi mới kéo `Goals`, `Assists`... vào! |
| **4. Đổi tên cột & phép tính** | Bấm đúp tên trường hoặc sửa trong Cube | Rê chuột lên **bên trái tên trường** trong ô `Phương diện` hoặc `Chỉ số` sẽ hiện **biểu tượng cây bút chì (`✏️`)** $\rightarrow$ Bấm vào đó để đổi tên tiếng Việt, chọn **`Tổng`** *(Sum)* / **`Trung bình`** *(Average)* / **`Đếm phân biệt`** *(Count Distinct)* hoặc đổi kiểu Ngày tháng! |
| **5. Lọc Top 10 (Top N)** | Vào khung Filters $\rightarrow$ chọn *Top N* | **Không có mục Top N trong Bộ lọc!** Thay vào đó:<br>• Ở tab **`Thiết lập`** $\rightarrow$ **Sắp xếp** theo `Goals` **`Giảm dần`**.<br>• Sang tab **`Kiểu`** $\rightarrow$ tìm mục **Thanh** *(Bars)* $\rightarrow$ sửa **Số lượng thanh** thành **`10`**. |
| **6. Tạo Bộ lọc (Slicer)** | Chọn visual *Slicer* trong Visualizations | Trên thanh công cụ phía trên, bấm **`Thêm bộ điều khiển`** $\rightarrow$ chọn **`Danh sách thả xuống`**, rồi kéo trường cần lọc vào ô **Trường điều khiển**. |

---

## PHẦN 2: QUY TRÌNH NẠP DỮ LIỆU & TẠO TRƯỜNG TÍNH TOÁN CHUẨN

### Bước 1: Tạo Báo cáo trống, Tạo Tập dữ liệu và Tải tệp `Football_Report_Data.csv`

1. Mở trình duyệt (Chrome/Edge), truy cập: [https://lookerstudio.google.com/](https://lookerstudio.google.com/) và đăng nhập tài khoản Google.
2. Ở góc trên bên trái, bấm nút **`+ Tạo`** $\rightarrow$ chọn **`Báo cáo`**.
3. Hộp thoại **Thêm dữ liệu vào báo cáo** tự động bật lên:
   * Tại tab **Kết nối với dữ liệu**, tìm và chọn **`Tải tệp lên`** *(File Upload)*.
   * Bấm **Ủy quyền** *(Authorize)* nếu đây là lần đầu bạn sử dụng.
   * **Tạo tập dữ liệu chứa tệp:** Nếu màn hình hiện thông báo *"Tạo tập dữ liệu để thêm tệp"*, bạn bấm nút **`Tạo tập dữ liệu`** màu xanh $\rightarrow$ đặt tên bất kỳ (ví dụ: `Football_DW`) $\rightarrow$ bấm **`Tạo`**.
   * Bấm nút **`Nhấp để tải tệp lên`** $\rightarrow$ chọn tệp:  
     `D:\Kho_du_lieu_OLAP\football\cleaned_data\Football_Report_Data.csv`
   * Chờ 15–30 giây để thanh tải chạy xong và hiện chữ màu xanh **`Đã tải lên`**.
   * Nhấp nút **`Thêm`** ở góc dưới bên phải $\rightarrow$ chọn **`Thêm vào báo cáo`**.
4. Giao diện thiết kế mở ra kèm 1 bảng mẫu có sẵn ở giữa trang $\rightarrow$ **Nhấp chọn bảng mẫu đó và nhấn phím `Delete`** trên bàn phím để làm sạch trang.

---

### Bước 2: Kiểm tra Kiểu dữ liệu & Tạo 2 Trường Tính Toán (Khớp 100% số liệu Cube SSAS)

Nhìn sang cột **`Dữ liệu`** ngoài cùng bên phải (danh sách các cột của `Football_Report_Data.csv`):

1. **Kiểm tra & Chuẩn hóa Kiểu dữ liệu (`Tài nguyên` $\rightarrow$ `Quản lý các nguồn dữ liệu đã thêm` $\rightarrow$ `Chỉnh sửa`):**
   * **Nhóm Cột Số đo (Giữ kiểu `Số` `123`):** `Goals`, `Assists`, `Goal_Contributions`, `Minutes_Played`, `Yellow_Cards`, `Red_Cards`, `Stadium_Seats`, `Age`, `Height_In_Cm`, `Squad_Size`, `Home_Club_Goals`, `Away_Club_Goals`.
   * **Nhóm Cột Mã ID & Thời gian tách lẻ (Chuyển sang kiểu `Văn bản` `ABC`):** Vì Looker Studio tự nhận các cột số nguyên là `Số` (Metric) và **không cho chuyển trực tiếp số lẻ `2022`, `08`, `3` sang `Ngày và giờ`**, bạn đổi tất cả các cột sau sang **`Văn bản`** để dùng làm bộ lọc/phân nhóm mà không bị cộng tổng `SUM`:
     * Mã ID: `Appearance_ID`, `Player_ID`, `Club_ID`, `Opponent_Club_ID`, `Competition_ID`, `Game_ID`, `Home_Club_ID`, `Away_Club_ID`, `Time_ID`.
     * Thời gian tách lẻ: `Year`, `Quarter`, `Month`, `Day`.
   * **Nhóm Cột Ngày chuẩn (Kiểu `Ngày` `📅`):**
     * `Full_Date` & `Date_Of_Birth`: Đã ở chuẩn `YYYYMMDD` (`20220805`, `19910509`) nên giữ kiểu **`Ngày`** *(khi cần xem theo Năm/Quý/Tháng kiểu thời gian liên tục, chỉ cần kéo `Full_Date` rồi bấm `✏️` chọn `Năm` / `Quý` / `Tháng`)*.
2. **Tạo các Trường Tính Toán tương ứng với Calculated Measures trong Cube SSAS (Bấm `+ Thêm trường` $\rightarrow$ `Thêm trường được tính` ở đáy cột `Dữ liệu`):**
   * **Trường 1 – `Total Coaches`** *(ra đúng `175` HLV trưởng, loại bỏ `'Unknown Coach'`)*:
     ```sql
     COUNT_DISTINCT(CASE WHEN Coach_Name != "Unknown Coach" THEN Coach_Name ELSE NULL END)
     ```
   * **Trường 2 – `Distinct Matches Played`** *(ra đúng `6,965` trận đấu duy nhất)*:
     ```sql
     COUNT_DISTINCT(Game_ID)
     ```
   * **Trường 3 – `Avg Minutes Played`** *(ra đúng `64.35` phút trung bình mỗi lượt ra sân)*:
     ```sql
     SUM(Minutes_Played) / COUNT(Appearance_ID)
     ```
   * **Trường 4 – `Stadium Capacity Cleaned`** *(lấy đúng sức chứa thực tế của sân vận động, tránh bị nhân dồn theo số lượt cầu thủ)*:
     ```sql
     MAX(Stadium_Seats)
     ```
   * **Trường 5 – `Total Appearances`** *(thay thế `Record Count`, ra đúng `210,747` lượt ra sân)*:
     ```sql
     COUNT(Appearance_ID)
     ```
3. **Tạo Bộ lọc dùng chung `Scorers_Only` (Chỉ lấy cầu thủ ghi bàn `Goals > 0`):**
   * Vào menu **`Tài nguyên`** $\rightarrow$ **`Quản lý bộ lọc`** $\rightarrow$ **`Thêm bộ lọc`**:
   * **Tên:** `Scorers_Only` | Chọn **`Bao gồm`** $\rightarrow$ Trường **`Goals`** $\rightarrow$ Điều kiện **`Lớn hơn (>)`** $\rightarrow$ Giá trị **`0`** $\rightarrow$ **`Lưu`**.

---

## PHẦN 3: HƯỚNG DẪN DESIGN GIAO DIỆN ĐẸP CHUẨN FULL HD (`1920 x 1080 px`)

Mặc định trang Looker Studio khá nhỏ, cần chỉnh rộng ra chuẩn `1920 x 1080 px` để đặt các biểu đồ thoáng đẹp, không bị cắt chữ (`...`).

### Bước 1: Cài đặt Kích thước Trang & Giao diện Tổng thể
1. Trên thanh menu trên cùng, chọn **`Trang`** $\rightarrow$ **`Cài đặt trang hiện tại`**.
2. Ở bảng bên phải, chuyển sang tab **`Kiểu`**:
   * **Chế độ hiển thị:** Chọn **`Khớp với chiều rộng`** *(hiển thị sắc nét toàn màn hình)*.
   * **Kích thước Canvas:** Chọn **`Tùy chỉnh`**, nhập:
     * **Chiều rộng:** **`1920`**
     * **Chiều cao:** **`1080`**
3. Bấm nút **`Giao diện và bố cục`** trên thanh công cụ:
   * Tab **`Giao diện`**: Bấm nút **`Tùy chỉnh`**:
     * **Nền báo cáo:** Chọn màu xám khói nhạt **`#F8FAFC`**.
     * **Nền thành phần:** Chọn màu trắng **`#FFFFFF`**, **Đường viền thành phần:** **`#CBD5E1`**.
   * Tab **`Bố cục`**:
     * Mục **Bám vào:** Chọn **`Lưới`** (`Grid`), **Kích thước lưới:** **`10 px`** *(giúp kéo thả thẳng hàng chuẩn xác)*.

### Bước 2: Quy tắc Design "Nổi khối & Căn tọa độ chuẩn" cho mọi Biểu đồ
Khi chọn bất kỳ biểu đồ nào rồi chuyển sang tab **`Kiểu`**:
1. **Bo góc, Viền & Đổ bóng (Mục `Nền và đường viền` ở cuối tab `Kiểu`):**
   * **Nền:** Trắng `#FFFFFF` *(riêng 4 Thẻ điểm KPI trên cùng dùng màu Pastel nhạt: `#EFF6FF`, `#FAF5FF`, `#F0FDF4`, `#FFFBEB`)*.
   * **Bán kính đường viền (Bo góc):** Nhập **`10`** (`10 px`).
   * **Độ dày đường viền:** `1 px`, **Màu đường viền:** `#CBD5E1`.
   * Tích chọn **`Thêm bóng đường viền`** để tạo hiệu ứng thẻ nổi 3D.
2. **Đặt Tọa độ & Kích thước chính xác:**
   * Cuộn xuống dưới cùng của tab **`Kiểu`** (hoặc khung **Vị trí** ngay bên dưới) để nhập thẳng 4 thông số: **`X`**, **`Y`**, **`Rộng`**, **`Cao`** mà không cần căn bằng tay.
3. **Thêm Tiêu đề cho Biểu đồ:**
   * Looker Studio không tự bật sẵn tiêu đề lớn như Power BI. Bạn bấm biểu tượng **`Văn bản`** *(chữ `A` trong ô vuông)* trên thanh công cụ để vẽ tiêu đề đặt phía trên hoặc lồng vào góc trên khung biểu đồ (`16–18 pt Đậm`, màu `#0F172A`), hoặc bật **`Tiêu đề biểu đồ`** $\rightarrow$ **`Luôn hiển thị`** trong tab `Kiểu`.

---

## PHẦN 4: THIẾT KẾ CHI TIẾT 3 BÁO BIỂU (ĐỒNG BỘ 100% VỚI POWER BI)

### 4.3.1 Báo biểu 1: Báo cáo Phân nhóm & Tổng hợp (Grouping and Totals Report)
> **Tên trang:** `Báo biểu 1 - Grouping & Totals`  
> **Mục tiêu:** Đáp ứng tiêu chí *"1 report dạng Grouping and Totals"* với bộ ba visual **Biểu đồ thanh xếp chồng + Biểu đồ cột xếp chồng + Bảng tổng hợp Pivot** và bộ cột mới (`Coach_Name`, `Competition_Type`, `Country_Name`, `Round`, `Quarter`).

#### 1. Tạo Banner Tiêu đề & 4 Thẻ điểm KPI (Scorecards) ở đầu trang
* **Banner Tiêu đề:** Bấm công cụ **`Văn bản`**, vẽ khung tại `X=20, Y=15, Rộng=1880, Cao=55`, nhập:  
  `BÁO BIỂU 1: BÁO CÁO PHÂN NHÓM & TỔNG HỢP HIỆU SUẤT TẤN CÔNG THEO GIẢI ĐẤU, THỜI GIAN & HLV TRƯỞNG`  
  *(Font `Roboto`, `20 pt Đậm`, Căn giữa, Nền `#FFFFFF`, Viền `#CBD5E1`, Bán kính đường viền `10`).*
* **4 Thẻ điểm KPI (`Thêm biểu đồ` $\rightarrow$ `Thẻ điểm`):** Đặt hàng ngang `Y=85, Cao=90, Rộng=455`:
  1. **Thẻ 1 (`X=20`):** Xóa `Record Count` $\rightarrow$ kéo **`Distinct Matches Played`** vào ô **Chỉ số** $\rightarrow$ bấm `✏️` đổi tên: `Tổng Số Trận Quản Trị` *(hiển thị `6,965`)*. Tab `Kiểu`: Nền `#EFF6FF`, cỡ số `35 pt Đậm`, bỏ tích **`Rút gọn số`**.
  2. **Thẻ 2 (`X=495`):** Kéo **`Total Coaches`** vào **Chỉ số** $\rightarrow$ đổi tên: `Tổng Số HLV Trưởng` *(hiển thị `175`)*. Tab `Kiểu`: Nền `#FAF5FF`, cỡ số `35 pt Đậm`.
  3. **Thẻ 3 (`X=970`):** Kéo **`Goals`** (phép tính `Tổng`) $\rightarrow$ đổi tên: `Tổng Bàn Thắng` *(bật **`Rút gọn số`** để hiện `19.17K`)*. Tab `Kiểu`: Nền `#F0FDF4`.
  4. **Thẻ 4 (`X=1445`):** Kéo **`Goal_Contributions`** (`Tổng`) $\rightarrow$ đổi tên: `Tổng Đóng Góp G+A` *(bật **`Rút gọn số`** để hiện `33.91K`)*. Tab `Kiểu`: Nền `#FFFBEB`.

#### 2. Tạo 4 Bộ lọc (`Thêm bộ điều khiển` $\rightarrow$ `Danh sách thả xuống`)
Đặt hàng ngang `Y=190, Cao=75, Rộng=455`:
* **Bộ lọc 1 (`X=20`):** Trường điều khiển = `Season` *(Mùa giải)*.
* **Bộ lọc 2 (`X=495`):** Trường điều khiển = `Competition_Type` *(Loại giải: Quốc nội vs Cúp Châu lục)*.
* **Bộ lọc 3 (`X=970`):** Trường điều khiển = `Country_Name` *(Quốc gia giải đấu)*.
* **Bộ lọc 4 (`X=1445`):** Trường điều khiển = `Quarter` *(Quý thi đấu Q1–Q4)*.

#### 3. Thiết kế Bộ ba Visual (Thân trang)

1. **Visual 1 (Trên Trái – `Biểu đồ thanh xếp chồng`):** Đặt tại `X=20, Y=280, Rộng=860, Cao=380`.
   * **Tab `Thiết lập`:**
     * **Phương diện:** Kéo `Competition_Type` $\rightarrow$ gạt công tắc **`Khoan sâu`** sang **BẬT** $\rightarrow$ bấm **`Thêm phương diện`** thêm lần lượt: `Country_Name` $\rightarrow$ `Competition_Name` $\rightarrow$ `Round`.
     * **Chỉ số:** Xóa `Record Count`, kéo **`Goals`** (`Tổng`) và **`Assists`** (`Tổng`).
     * **Sắp xếp:** `Goals` $\rightarrow$ **`Giảm dần`**.
     * **Tương tác với biểu đồ:** Tích chọn **`Áp dụng bộ lọc`** *(để bấm vào giải đấu sẽ lọc luôn bảng HLV bên phải)*.
   * **Tab `Kiểu`:**
     * Tích chọn **`Thanh xếp chồng`** *(nếu biểu đồ đang đứng cạnh nhau)*.
     * Màu sắc: Chuỗi #1 (`Goals`) = `#2563EB` (Xanh dương), Chuỗi #2 (`Assists`) = `#06B6D4` (Xanh Cyan).
     * Tích chọn **`Hiển thị nhãn dữ liệu`** để hiện con số trực tiếp trên từng thanh.

2. **Visual 2 (Dưới Trái – `Biểu đồ cột xếp chồng`):** Đặt tại `X=20, Y=680, Rộng=860, Cao=380`.
   * **Tab `Thiết lập`:**
     * **Phương diện:** Kéo `Season` $\rightarrow$ gạt **`Khoan sâu`: BẬT** $\rightarrow$ bấm **`Thêm phương diện`** thêm `Quarter`.
     * **Chỉ số:** Kéo **`Goals`** (`Tổng`) và **`Assists`** (`Tổng`).
     * **Tương tác với biểu đồ:** Tích chọn **`Áp dụng bộ lọc`**.
   * **Tab `Kiểu`:** Tích **`Xếp chồng`**, màu `#2563EB` & `#06B6D4`, tích **`Hiển thị nhãn dữ liệu`**.

3. **Visual 3 (Bên Phải – `Bảng tổng hợp có tổng phụ` – Chuẩn Grouping & Totals):** Đặt tại `X=900, Y=280, Rộng=1000, Cao=780`.
   * **Menu chọn:** `Thêm biểu đồ` $\rightarrow$ nhóm *Bảng tổng hợp* $\rightarrow$ chọn **`Bảng tổng hợp`** *(Pivot table)* hoặc **`Bảng tổng hợp có bản đồ nhiệt`**.
   * **Tab `Thiết lập`:**
     * **Phương diện hàng:** Kéo lần lượt 3 cấp: `Coach_Name` $\rightarrow$ `Club_Name` $\rightarrow$ `Player_Name`.
     * **Phương diện cột:** Để trống.
     * **Chỉ số:** Xóa `Record Count`, kéo 4 thước đo: `Goals` (`Tổng`), `Assists` (`Tổng`), `Goal_Contributions` (`Tổng`), `Distinct Matches Played`.
     * **Sắp xếp:** Hàng số 1 sắp xếp theo `Goals` **`Giảm dần`** *(để Pep Guardiola, Xabi Alonso, Arteta... lên đầu)*.
   * **Tab `Kiểu` (BƯỚC QUAN TRỌNG NHẤT ĐỂ ĐẠT CHUẨN GROUPING & TOTALS):**
     * Mục **Tổng phụ của hàng** *(Row subtotals)* $\rightarrow$ Tích chọn **`Hiển thị tổng phụ`**!
     * Mục **Tổng cộng** *(Grand total)* $\rightarrow$ Tích chọn **`Hiển thị tổng cộng`** cho Hàng!
     * Mục **Tiêu đề bảng:** Nền xanh Navy **`#0F172A`**, chữ Trắng **`#FFFFFF` Đậm**.
     * Tại cột thứ 3 (`Goal_Contributions`): Mục *Cột #3*, đổi từ *Số* sang **`Thanh`** *(Bar)* màu `#2563EB` và tích **`Hiển thị số`**.

---

### 4.3.2 Báo biểu 2: Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh (Scouting Elite Clubs & Top Threats)
> **Mẹo tạo trang nhanh:** Bấm **`Trang`** $\rightarrow$ **`Sao chép trang`** từ Trang 1, đổi tên thành `Báo biểu 2 - Trinh sát Chiến thuật`, rồi xóa 3 biểu đồ thân trang đi để giữ nguyên Banner + 4 Thẻ điểm + 4 Bộ lọc!

* **4 Thẻ điểm KPI (`Y=85, Cao=90`):** `Distinct Matches Played` (`6,965`), `Goals` (`19.17K`), `Assists` (`14.74K`), `Goal_Contributions` (`33.91K`).
* **4 Bộ lọc (`Y=190, Cao=75`):** `Season`, `Competition_Name`, `Sub_Position` *(Vị trí chi tiết)*, `Foot` *(Chân thuận: left/right)*.
* **Lưới 2x2 ở thân trang (`Y=280` trở xuống, mỗi ô `Rộng=925, Cao=380`):**

| Vị trí | Loại Biểu đồ | Tab `Thiết lập` (Setup) | Tab `Kiểu` (Style) |
| :--- | :--- | :--- | :--- |
| **Trên Trái** (`X=20, Y=280`) | **Biểu đồ thanh** *(Bar chart)* — Top 10 CLB Hỏa lực | **Phương diện:** `Club_Name`<br>**Chỉ số:** `Goals` (`Tổng`), `Assists` (`Tổng`)<br>**Sắp xếp:** `Goals` `Giảm dần`<br>**Bộ lọc:** `Scorers_Only` | **Số lượng thanh:** `10`<br>Tích **`Hiển thị nhãn dữ liệu`** |
| **Trên Phải** (`X=975, Y=280`) | **Biểu đồ kết hợp** *(Combo chart)* — Chảo lửa Sân vận động | **Phương diện:** `Stadium_Name`<br>**Chỉ số:** `Distinct Matches Played`, `Goals` (`Tổng`)<br>**Sắp xếp:** `Goals` `Giảm dần` | **Số lượng thanh:** `10`<br>Chuỗi #1 (`Distinct Matches Played`): **`Thanh`**<br>Chuỗi #2 (`Goals`): **`Đường`**, **Trục:** **`Phải`** |
| **Dưới Trái** (`X=20, Y=680`) | **Biểu đồ vùng** *(Area chart)* — Biến thiên Bàn thắng | **Phương diện:** `Full_Date` $\rightarrow$ bấm `✏️` chọn **Loại: Ngày và giờ $\rightarrow$ `Năm Tháng`**<br>**Chỉ số:** `Goals` (`Tổng`) | Tích **`Hiển thị điểm`**, màu xanh `#2563EB` |
| **Dưới Phải** (`X=975, Y=680`) | **Bảng có thanh màu** *(Table with bars)* — Trinh sát Cầu thủ | **Phương diện:** `Player_Name`, `Country_Of_Citizenship`, `Sub_Position`, `Foot`, `Age`<br>**Chỉ số:** `Goals`, `Assists`, `Goal_Contributions`<br>**Sắp xếp:** `Goal_Contributions` `Giảm dần` | Cột `Goal_Contributions` chọn hiển thị **`Thanh`** + **`Hiển thị số`**<br>Tiêu đề bảng nền `#0F172A` chữ trắng |

---

### 4.3.3 Báo biểu 3: Kỷ luật Thẻ phạt & Tải trọng Thi đấu (Discipline & Physical Workload)
> **Tên trang:** `Báo biểu 3 - Kỷ luật & Thể lực`

* **4 Thẻ điểm KPI (`Y=85, Cao=90`):** `Yellow_Cards` (`Tổng`), `Red_Cards` (`Tổng`), `Total Appearances` (`210.75K`), `Minutes_Played` (`Tổng` = `13.56M`).
* **4 Bộ lọc (`Y=190, Cao=75`):** `Season`, `Competition_Name`, `Country_Name`, `Main_Position`.
* **Lưới 2x2 ở thân trang (`Rộng=925, Cao=380` mỗi ô):**

| Vị trí | Loại Biểu đồ | Tab `Thiết lập` (Setup) | Tab `Kiểu` (Style) |
| :--- | :--- | :--- | :--- |
| **Trên Trái** (`X=20, Y=280`) | **Biểu đồ thanh xếp chồng** — Top 10 CLB Nhiều thẻ | **Phương diện:** `Club_Name`<br>**Chỉ số:** `Yellow_Cards` (`Tổng`), `Red_Cards` (`Tổng`)<br>**Sắp xếp:** `Yellow_Cards` `Giảm dần` | Tích **`Thanh xếp chồng`**, **Số lượng thanh:** `10`<br>Màu: Vàng `#F59E0B` & Đỏ `#EF4444`<br>Tích **`Hiển thị nhãn dữ liệu`** |
| **Trên Phải** (`X=975, Y=280`) | **Biểu đồ đường** *(Line chart)* — Phút thi đấu theo Giải | **Phương diện:** `Season`<br>**Phương diện phân tích:** `Competition_Name`<br>**Chỉ số:** `Minutes_Played` (`Tổng`) | Giới hạn tối đa `5–6` dòng giải đấu lớn cho thoáng<br>Tích **`Hiển thị điểm`** |
| **Dưới Trái** (`X=20, Y=680`) | **Biểu đồ kết hợp** *(Combo chart)* — Thể lực & Thẻ theo Tuổi | **Phương diện:** `Age` *(Sắp xếp `Tăng dần` theo `Age`)*<br>**Chỉ số:** `Minutes_Played` (`Tổng`), `Yellow_Cards` (`Tổng`) | Chuỗi #1 (`Minutes_Played`): **`Thanh`** (Trục `Trái`)<br>Chuỗi #2 (`Yellow_Cards`): **`Đường`** (Trục **`Phải`**) |
| **Dưới Phải** (`X=975, Y=680`) | **Biểu đồ hình khuyên** *(Donut chart)* — Thẻ đỏ theo Vị trí | **Phương diện:** `Sub_Position`<br>**Chỉ số:** `Red_Cards` (`Tổng`) | Kéo thanh trượt **Hình khuyên** lên **`50%`**<br>**Số lát cắt:** `8`, hiển thị tỷ lệ `%` |

---

## PHẦN 5: KIỂM TRA TƯƠNG TÁC & XUẤT BÁO CÁO (CHẾ ĐỘ XEM)

1. Nhấp nút **`Xem`** màu xanh ở góc trên bên phải màn hình để chuyển sang chế độ người dùng cuối.
2. **Kiểm tra 3 điểm chốt:**
   * Bấm vào thanh `uefa-champions-league` trên Visual 1 (Trang 1) $\rightarrow$ 4 Thẻ điểm KPI và Bảng tổng hợp Pivot HLV phải tự động lọc theo Cúp C1.
   * Bấm nút mũi tên **`↓` (Khoan sâu)** ở góc trên phải Visual 1 để khoan từ `international_cup` xuống tới `Round` (`Final`, `Semi-Finals`).
   * Bấm nút **`Chia sẻ`** (góc trên phải) $\rightarrow$ chọn **`Tải xuống báo cáo`** (xuất tệp PDF nộp bài) hoặc sao chép đường dẫn chia sẻ trực tuyến cho giảng viên.
