# Báo biểu 2: Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh (Scouting Elite Clubs & Top Offensive Threats)
> **Nền tảng:** Google Data Studio (Looker Studio)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv`  
> **Kích thước Canvas:** Full HD `1920 x 1080 px` (Tỷ lệ 16:9), Màu nền xám khói `#F8FAFC`  
> **Đối ứng với Power BI:** [03_power_bi_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/power-bi/03_power_bi_bao_bieu_2.md)

---

## 1. Mục tiêu Nghiệp vụ và Ý nghĩa Trinh sát Chiến thuật

* **Mục tiêu chuyên môn:** Giải quyết bài toán then chốt của ban huấn luyện và bộ phận phân tích chiến thuật: **"Tra cứu xem kẻ nào đang mạnh nhất, đối thủ sở hữu những họng pháo nào nguy hiểm nhất để lên phương án dè chừng (bắt chết, phong tỏa) hoặc học hỏi bài bản tấn công!"**
* **Khai thác sâu các đặc tính trinh sát của cầu thủ:**
  * **`Player_Country` (Quốc tịch):** Nhận diện trường phái đào tạo bóng đá (Bắc Âu thể lực càn lướt, Nam Mỹ kỹ thuật ma thuật, Tây Âu chiến thuật hiện đại).
  * **`Sub_Position` (Vị trí thi đấu chi tiết):** Xác định mũi nhọn là Trung phong cắm (`Centre-Forward`), Tiền đạo dạt biên (`Left Winger` / `Right Winger`) hay Tiền vệ công (`Attacking Midfield`) để phòng ngự đúng hướng đánh.
  * **`Foot` (Chân thuận):** Nhận diện các "kèo trái ma thuật" (`left`) hay thuận chân phải (`right`) để hậu vệ biên biết đường be góc sút, cấm ngoặt bóng vào trung lộ.
  * **`Age` (Độ tuổi):** Đánh giá độ tuổi sung mãn đỉnh cao (Peak 24 - 28 tuổi: Haaland 26, Mbappé 28, Vinicius 26) hay kinh nghiệm dày dạn (33 - 38 tuổi: Salah 34, Lewandowski 38, Griezmann 35) để lên phương án đua thể lực hoặc bắt bài độ tinh quái.
* **Bức tranh vĩ mô:** Xếp hạng các CLB có hỏa lực mạnh nhất châu Âu (`Club_Name`), các chảo lửa nổ nhiều bàn nhất (`Stadium_Name`) và nhịp điệu phong độ theo thời gian.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080 px)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [BANNER TIÊU ĐỀ] HỒ SƠ CHIẾN THUẬT & TRINH SÁT KẺ MẠNH (ELITE CLUBS & TOP OFFENSIVE THREATS) (Font: 20pt Bold, Center)   |
| Tọa độ: X = 20 px, Y = 15 px | Kích thước: Width = 1880 px, Height = 55 px                                              |
+-------------------------------------------------------------------------------------------------------------------------+
| [Card 1: Tổng Số Trận]    | [Card 2: Tổng Bàn Thắng]  | [Card 3: Tổng Kiến Tạo]     | [Card 4: Tổng Đóng Góp G+A]       |
| COUNT_DISTINCT(Appearances)| SUM(Goals)               | SUM(Assists)                | SUM(Goal_Contributions)           |
| (W: 455, H: 95, X: 20)    | (W: 455, H: 95, X: 495)   | (W: 455, H: 95, X: 970)     | (W: 455, H: 95, X: 1445)          |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Bộ lọc 1: Mùa giải]      | [Bộ lọc 2: Giải đấu]      | [Bộ lọc 3: Vị trí chi tiết] | [Bộ lọc 4: Chân thuận]            |
| Season (Dropdown)         | Competition_Name (Drop)   | Sub_Position (Dropdown)     | Foot (Dropdown)                   |
| (W: 455, H: 75, X: 20)    | (W: 455, H: 75, X: 495)   | (W: 455, H: 75, X: 970)     | (W: 455, H: 75, X: 1445)          |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI | BIỂU ĐỒ THANH NGANG (BAR CHART)]    | [Ô 2: TRÊN - PHẢI | COMBO CHART 2 TRỤC Y (CỘT & ĐƯỜNG)]       |
| Top 10 CLB có hỏa lực tấn công mạnh nhất Châu Âu        | Chảo lửa Thánh địa: Số trận vs Bàn thắng ghi được             |
| Dimension: Club_Name, Metric: SUM(Goals)                | Dimension: Stadium_Name, Bars: Matches, Lines: Goals          |
| Tọa độ: X = 20 px, Y = 300 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 300 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI | BIỂU ĐỒ VÙNG (TIME SERIES AREA)]    | [Ô 4: DƯỚI - PHẢI | BẢNG TRINH SÁT CẦU THỦ (SCOUTING TABLE)]  |
| Biến thiên Bàn thắng theo Dòng thời gian Mùa & Tháng    | Bảng Trinh sát Mũi nhọn (Tên, CLB, Quốc tịch, Vị trí, Chân,  |
| Dimension: Full_Date (hoặc Year/Month), Metric: Goals   | Tuổi, Goals, Assists, Goal Contributions kèm Data Bars)       |
| Tọa độ: X = 20 px, Y = 695 px | W = 925 px, H = 385 px  | Tọa độ: X = 975 px, Y = 695 px | W = 925 px, H = 385 px       |
+---------------------------------------------------------+---------------------------------------------------------------+
```

---

## 3. Hướng dẫn Thiết lập Từng Bước Chi tiết

### Bước 1: Khởi tạo Trang Báo cáo
1. Trong báo cáo Looker Studio, chọn **Thêm trang (Add page)**.
2. Đổi tên trang thành: `Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh`.
3. Menu **Trang** $\rightarrow$ **Cài đặt trang hiện tại** $\rightarrow$ tab **Kiểu**:
   * **Nền trang:** Màu xám khói `#F8FAFC`.
   * **Kích thước Canvas:** `Custom`, `Width = 1920 px`, `Height = 1080 px`.

---

### Bước 2: Tạo Banner Tiêu đề Trang (Top Banner)
1. Thêm **Hộp văn bản (Text box)** tại: `X = 20 px`, `Y = 15 px`, `Width = 1880 px`, `Height = 55 px`.
2. Nội dung: `BÁO BIỂU 2: HỒ SƠ CHIẾN THUẬT & TRINH SÁT KẺ MẠNH (ELITE CLUBS & TOP OFFENSIVE THREATS)`.
3. Font: **Roboto / Arial**, Cỡ chữ **`20 pt` Bold**, Căn giữa (**Center**), Màu `#0F172A`, Nền `#FFFFFF`, Bo viền `10 px`.

---

### Bước 3: Tạo Khối 4 Thẻ KPI Tấn công (Scorecards)
Menu **Thêm biểu đồ** $\rightarrow$ **Thẻ chỉ số (Scorecard)**, hàng `Y = 95 px`, `Height = 95 px`, `Width = 455 px`:

#### 1. Thẻ 1: Tổng Số Trận Quan Sát (Distinct Matches)
* **Vị trí:** `X = 20 px`.
* **Chỉ số (Metric):** Tạo trường tính toán hoặc kéo `Appearance_ID` với phép tổng hợp **`COUNT_DISTINCT`** (hoặc `COUNT`). Đổi tên: `Tổng Số Trận Quan Sát`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Màu nền `#EFF6FF` (Pastel Blue), Bo góc `10 px`.

#### 2. Thẻ 2: Tổng Bàn Thắng (Total Goals)
* **Vị trí:** `X = 495 px`.
* **Chỉ số (Metric):** `Goals` (SUM). Đổi tên: `Tổng Bàn Thắng`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#F0FDF4` (Pastel Green), Bo góc `10 px`.

#### 3. Thẻ 3: Tổng Kiến Tạo (Total Assists)
* **Vị trí:** `X = 970 px`.
* **Chỉ số (Metric):** `Assists` (SUM). Đổi tên: `Tổng Kiến Tạo`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#FFFBEB` (Pastel Amber), Bo góc `10 px`.

#### 4. Thẻ 4: Tổng Đóng Góp Bàn Thắng (Goal Contributions)
* **Vị trí:** `X = 1445 px`.
* **Chỉ số (Metric):** `Goal_Contributions` (SUM). Đổi tên: `Tổng Đóng Góp G+A`.
* **Kiểu (Style):** Cỡ chữ **`35 pt` Bold**, Nền `#FAF5FF` (Pastel Purple), Bo góc `10 px`.

---

### Bước 4: Thiết lập 4 Bộ lọc Tương tác (Controls)
Menu **Thêm bộ điều khiển (Add a control)** $\rightarrow$ hàng `Y = 210 px`, `Height = 75 px`, `Width = 455 px`:

1. **Bộ lọc 1: Mùa giải (Season):** `X = 20 px`, Loại `Drop-down list`, Control field: `Season`.
2. **Bộ lọc 2: Giải đấu (Competition):** `X = 495 px`, Loại `Drop-down list`, Control field: `Competition_Name`.
3. **Bộ lọc 3: Vị trí chi tiết (Sub Position):** `X = 970 px`, Loại `Drop-down list`, Control field: `Sub_Position`.
4. **Bộ lọc 4: Chân thuận (Foot):** `X = 1445 px`, Loại `Drop-down list`, Control field: `Foot`.

---

### Bước 5: Ô 1 (Trên - Trái) – Biểu đồ Thanh Ngang: Top 10 CLB Hỏa lực Mạnh nhất Châu Âu
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ thanh ngang (Bar chart)**.
2. Vị trí & Kích thước: `X = 20 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Club_Name` (Đổi tên: `Câu lạc bộ`).
   * **Chỉ số (Metric):** `Goals` (SUM, Đổi tên: `Bàn thắng`).
   * **Sắp xếp (Sort):** `Goals` giảm dần (**Descending**).
   * **Số lượng thanh (Bars):** Chọn `10` (Top 10 CLB: *Man City, Bayern Munich, PSV, Real Madrid, Arsenal, Liverpool...*).
4. **Kiểu (Style):**
   * Tiêu đề: `Top 10 CLB có Hỏa lực Tấn công Mạnh nhất Châu Âu`.
   * Màu thanh: Xanh dương hiện đại `#2563EB`.
   * Bật **Hiển thị nhãn dữ liệu (Show data labels): ON**.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 6: Ô 2 (Trên - Phải) – Combo Chart 2 Trục Y: Thánh địa Sân vận động Bùng nổ Bàn thắng
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ kết hợp cột và đường (Combo chart)**.
2. Vị trí & Kích thước: `X = 975 px`, `Y = 300 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện (Dimension):** `Stadium_Name` (Đổi tên: `Sân vận động`).
   * **Chỉ số chuỗi 1 (Cột - Trục Y trái):** `Appearance_ID` (COUNT_DISTINCT, Đổi tên: `Số trận tổ chức`) hoặc `Stadium_Seats`.
   * **Chỉ số chuỗi 2 (Đường - Trục Y phải):** `Goals` (SUM, Đổi tên: `Bàn thắng ghi được`).
   * **Sắp xếp (Sort):** `Goals` giảm dần, giới hạn Top 10 thánh địa (*Giuseppe Meazza, Olimpico di Roma, Etihad Stadium, Allianz Arena, Santiago Bernabéu...*).
4. **Kiểu (Style):**
   * Tiêu đề: `Chảo lửa Thánh địa: Số trận Tổ chức vs Bàn thắng Ghi được`.
   * Chuỗi 1 (Cột): Màu xanh dương `#2563EB`.
   * Chuỗi 2 (Đường): Màu đỏ cam rực lửa `#EF4444`, độ dày đường 3px, bật điểm mút (Show points).
   * Bật **Trục Y phụ (Secondary Y-axis)** cho chuỗi Đường để so sánh 2 thang đo độc lập.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 7: Ô 3 (Dưới - Trái) – Biểu đồ Vùng Dòng Thời gian (Time Series / Area Chart)
1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Biểu đồ chuỗi thời gian (Time series chart)** (hoặc **Biểu đồ vùng / Area chart**).
2. Vị trí & Kích thước: `X = 20 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập (Setup):**
   * **Phương diện thời gian (Time Dimension):** `Full_Date` (hoặc `Year` kết hợp `Month`).
   * **Chỉ số (Metric):** `Goals` (SUM, Đổi tên: `Bàn thắng ghi được`).
   * **Sắp xếp:** Thời gian tăng dần (**Ascending**).
4. **Kiểu (Style):**
   * Tiêu đề: `Biến thiên Bàn thắng theo Chu kỳ Thời gian trong Mùa giải`.
   * Kiểu đường: Chọn **Vùng (Area)**, tô bóng mờ (Transparency ~50%).
   * Màu đường: Xanh Navy `#1D4ED8`, bật điểm mút (Points).
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

### Bước 8: Ô 4 (Dưới - Phải) – Bảng Trinh Sát Đặc Tính Chiến Thuật Cầu Thủ (Tactical Scouting Table)

Bảng tra cứu trực diện thông tin chiến thuật của từng mũi nhọn nguy hiểm nhất để ban huấn luyện lên phương án phong tỏa:

1. Menu **Thêm biểu đồ** $\rightarrow$ chọn **Bảng (Table)**.
2. Vị trí & Kích thước: `X = 975 px`, `Y = 695 px`, `Width = 925 px`, `Height = 385 px`.
3. **Thiết lập dữ liệu (Setup):**
   * **Phương diện (Dimensions):** Kéo lần lượt 6 trường:
     1. `Player_Name` (Đổi tên: `Player Name` / `Tên cầu thủ`).
     2. `Club_Name` (Đổi tên: `Club Name` / `CLB`).
     3. `Player_Country` (Đổi tên: `Nationality` / `Quốc tịch`).
     4. `Sub_Position` (Đổi tên: `Position` / `Vị trí`).
     5. `Foot` (Đổi tên: `Foot` / `Chân thuận`).
     6. `Age` (Đổi tên: `Age` / `Tuổi`).
   * **Chỉ số (Metrics):** Kéo 3 thước đo:
     1. `Goals` (SUM, Đổi tên: `Goals` / `Bàn thắng`).
     2. `Assists` (SUM, Đổi tên: `Assists` / `Kiến tạo`).
     3. `Goal_Contributions` (SUM, Đổi tên: `Goal Contributions` / `G+A`).
   * **Sắp xếp (Sort):** `Goal_Contributions` giảm dần (**Descending**).
4. **Kiểu hiển thị (Style):**
   * Tiêu đề: `Bảng Trinh Sát Đặc Tính Chiến Thuật của các Mũi Nhọn Nguy Hiểm`.
   * **Thanh dữ liệu trực quan cho Goal Contributions:** Tại mục Chỉ số `Goal_Contributions`, chọn định dạng **Thanh (Bar)**, màu xanh dương `#2563EB`, bật hiển thị cả số bên cạnh thanh.
   * **Định dạng dòng:** Bật màu dòng xen kẽ (Zebra striping) nhạt `#F8FAFC`.
   * **Phân trang (Pagination):** Bật phân trang `10 - 15 dòng/trang`.
   * Nền `#FFFFFF`, Viền `#CBD5E1`, Bo góc `10 px`.

---

## 4. Kết quả Nghiệm thu và Giá trị Trinh sát Chiến thuật

| Player Name | Club Name | Nationality | Position | Foot | Age | Goals | Assists | Goal Contributions |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Erling Haaland** | Manchester City | Norway | Centre-Forward | left | 26 | 81 | 14 | **95** |
| **Kylian Mbappé** | Paris Saint-Germain | France | Centre-Forward | right | 28 | 71 | 16 | **87** |
| **Mohamed Salah** | Liverpool FC | Egypt | Right Winger | left | 34 | 50 | 28 | **78** |
| **Luuk de Jong** | PSV Eindhoven | Netherlands | Centre-Forward | right | 36 | 48 | 21 | **69** |
| **Mauro Icardi** | Galatasaray | Argentina | Centre-Forward | right | 33 | 50 | 18 | **68** |
| **Robert Lewandowski** | FC Barcelona | Poland | Centre-Forward | right | 38 | 51 | 16 | **67** |
| **Lautaro Martínez** | Inter Milan | Argentina | Centre-Forward | right | 29 | 50 | 16 | **66** |
| **Vinicius Junior** | Real Madrid | Brazil | Left Winger | right | 26 | 38 | 26 | **64** |

* **Bắt bài chân thuận:** Nhận diện ngay Mohamed Salah (Right Winger nhưng thuận chân trái) để hậu vệ biên be góc trong cấm ngoặt bóng dứt điểm.
* **Đua thể lực theo tuổi:** Nhận diện dàn sao đỉnh cao (Haaland 26 tuổi, Mbappé 28 tuổi) cần kèm chặt tốc độ, trong khi các lão tướng (Lewandowski 38 tuổi, Salah 34 tuổi) cần cảnh giác độ tinh quái chọn vị trí trong vòng cấm.
