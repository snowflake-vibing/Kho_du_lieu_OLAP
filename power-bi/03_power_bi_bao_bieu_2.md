# 4.2.2 Báo biểu 2: Vận hành Trận đấu, Lợi thế Sân nhà và Tương quan Sân vận động (Club Match Operations & Home Advantage Analytics)

Tài liệu hướng dẫn thiết kế **Báo biểu 2** trên **Power BI Desktop** (Live Connection tới Cube `[DW Football Transfermarkt]`), tuân thủ toàn bộ quy chuẩn tại [rule.md](../rule.md): Canvas **1920 x 1080 px**, bố cục **2 tầng** (Tầng trên: Title + KPI Cards + Slicers; Tầng dưới: **lưới 2x2 đúng 4 biểu đồ nâng cao**), cỡ chữ **20 / 15 / 18 / 12 pt**, không có dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ
* **Lợi thế sân nhà có thật không và lớn tới mức nào?** So sánh bàn thắng khi `Is Home Game = 1` và `Is Home Game = 0`.
* **Quy mô sân vận động có liên quan tới hỏa lực tấn công không?** Tương quan giữa sức chứa sân (`Stadium Seats`) và tổng bàn thắng của CLB.
* **Giải đấu nào đang thay đổi vị thế qua các mùa?** Theo dõi thứ hạng bàn thắng giữa các giải đấu theo `Season`.

### 1.2. Ý nghĩa thống kê
| Thành phần | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Tỷ lệ bàn sân nhà (%)** | Chuẩn hóa về tỷ trọng thay vì số tuyệt đối, so sánh công bằng giữa CLB đá nhiều trận và ít trận. Ngưỡng tham chiếu trung tính là **50%**: lệch càng xa 50% thì lợi thế sân nhà càng rõ. |
| **Scatter Sức chứa sân vs Bàn thắng** | Phân tích tương quan 2 biến định lượng; đường xu hướng (Trend line) cho thấy chiều và độ mạnh của mối quan hệ, đường **Trung vị (Median)** kháng nhiễu các sân siêu lớn (ngoại lai). |
| **Ribbon Chart theo Mùa giải** | Thể hiện cả **giá trị** lẫn **thứ hạng** của từng giải đấu qua thời gian, phát hiện dịch chuyển vị thế mà biểu đồ cột thường không thấy. |

### 1.3. Bài toán thực tế giải quyết
1. **Ban huấn luyện:** Đội có tỷ lệ bàn sân nhà > 60% đang phụ thuộc lợi thế sân nhà → cần chiến thuật riêng cho các trận sân khách.
2. **Ban điều hành CLB:** Đánh giá việc đầu tư mở rộng sân có gắn với hiệu quả thi đấu hay chỉ phản ánh quy mô thương mại.
3. **Nhà tài trợ / Bản quyền truyền hình:** Nhận diện giải đấu đang tăng trưởng hỏa lực tấn công (hấp dẫn khán giả hơn) để ưu tiên đầu tư.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [TITLE] BÁO BIỂU 2: VẬN HÀNH TRẬN ĐẤU, LỢI THẾ SÂN NHÀ & TƯƠNG QUAN SÂN VẬN ĐỘNG (20pt Bold)                           |
| X = 20, Y = 15 | W = 1880, H = 55                                                                                       |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Card 1: Tổng Trận Đấu]   | [Card 2: Bàn Sân Nhà]     | [Card 3: Bàn Sân Khách]     | [Card 4: Tỷ lệ Bàn Sân Nhà %]     |
| Nền #EFF6FF               | Nền #F0FDF4               | Nền #FFFBEB                 | Nền #FAF5FF                       |
| X=20, Y=80, W=455, H=105  | X=495                     | X=970                       | X=1445                            |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Giải đấu] X=20, W=650           | [Slicer 2: Mùa giải] X=690, W=600     | [Slicer 3: Loại giải đấu] X=1310, W=590 |
| Y = 195, H = 50                                                                                                         |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI] Clustered Column Chart               | [Ô 2: TRÊN - PHẢI] SCATTER (NÂNG CAO)                         |
| Bàn thắng Sân nhà vs Sân khách - Top 10 CLB             | Sức chứa sân vs Tổng bàn thắng (Trend + Median lines)         |
| X = 20, Y = 265 | W = 925, H = 385                      | X = 975, Y = 265 | W = 925, H = 385                           |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI] RIBBON CHART (NÂNG CAO)              | [Ô 4: DƯỚI - PHẢI] MATRIX + DATA BARS (NÂNG CAO)              |
| Dịch chuyển thứ hạng bàn thắng các Giải đấu theo Mùa    | Bảng xếp hạng CLB: Sân, Sức chứa, Bàn nhà/khách               |
| X = 20, Y = 675 | W = 925, H = 385                      | X = 975, Y = 675 | W = 925, H = 385                           |
+---------------------------------------------------------+---------------------------------------------------------------+
```

> **NHẬP TỌA ĐỘ CHUẨN TỪNG PIXEL:** Chọn visual → tab **General** → **Properties** → nhập **Size** (Width, Height) và **Position** (Horizontal, Vertical).
>
> **HIỆU ỨNG THẺ CHO MỌI VISUAL (trừ KPI Cards):** Tab **General** → **Effects** → **Background** `#FFFFFF` (Transparency 0%) → **Visual border** On, màu `#CBD5E1`, **Rounded corners `10 px`**.

---

## 3. Hướng dẫn Từng Bước

### Bước 1: Tạo trang và cấu hình Canvas
1. Nhấp dấu `+` ở thanh trang bên dưới, đổi tên trang thành `Vận hành CLB & Sân đấu`.
2. Nhấp vùng trống Canvas → **Format report page**:
   * **Canvas settings** → Type: **Custom**, `Width = 1920 px`, `Height = 1080 px`.
   * **Canvas background** → Color `#F8FAFC`, Transparency **`0%`**.

### Bước 2: Title Banner (Tầng trên)
1. **Insert** → **Text box**, nhập: `BÁO BIỂU 2: VẬN HÀNH TRẬN ĐẤU, LỢI THẾ SÂN NHÀ & TƯƠNG QUAN SÂN VẬN ĐỘNG`.
2. Font `Segoe UI`, **`20 pt`**, **Bold**, màu `#0F172A`, căn giữa.
3. Effects: Background `#FFFFFF`, Border `#CBD5E1`, bo góc `10 px`.
4. **Properties:** `W = 1880`, `H = 55`, `X = 20`, `Y = 15`.

### Bước 3: 4 Thẻ KPI (Tầng trên)
Chung cho cả 4 thẻ: **Title** On, `15 pt` Bold, căn giữa · **Callout value** `18 pt` Bold, màu `#0F172A` · **Category label** Off · `W = 455`, `H = 105`, `Y = 80`.

| Thẻ | Trường / Thước đo | Title | Nền / Viền | X |
| :--- | :--- | :--- | :--- | :---: |
| Card 1 | `DIM Game [Game ID]` (Count Distinct) | `TỔNG TRẬN ĐẤU` | `#EFF6FF` / `#93C5FD` | 20 |
| Card 2 | `[Measures].[Goals]` + Visual filter `Is Home Game = 1` | `BÀN THẮNG SÂN NHÀ` | `#F0FDF4` / `#86EFAC` | 495 |
| Card 3 | `[Measures].[Goals]` + Visual filter `Is Home Game = 0` | `BÀN THẮNG SÂN KHÁCH` | `#FFFBEB` / `#FCD34D` | 970 |
| Card 4 | Thước đo `[Home Goals Ratio]` (định dạng `0.0%`) | `TỶ LỆ BÀN SÂN NHÀ (%)` | `#FAF5FF` / `#D8B4FE` | 1445 |

> **Card 4 – thước đo tính toán độc lập (không phụ thuộc dây chuyền):** tạo trong tab **Calculations** của Cube:
> ```mdx
> CREATE MEMBER CURRENTCUBE.[Measures].[Home Goals Ratio] AS
>   IIF( [Measures].[Goals] = 0, NULL,
>        ( [Measures].[Goals], [FACT Player Match Perf].[Is Home Game].&[1] ) / [Measures].[Goals] ),
>   FORMAT_STRING = "0.0%", VISIBLE = 1;
> ```
> *Bắt buộc kiểm tra tên Hierarchy `Is Home Game` thực tế trong Cube trước khi deploy.*

### Bước 4: 3 Slicers (Tầng trên)
Chung: Header `15 pt` Bold, Values `12 pt`, Effects nền `#FFFFFF`, viền `#E2E8F0`, bo góc `8 px`, `Y = 195`, `H = 50`.

| Slicer | Trường | Kiểu | X | W |
| :--- | :--- | :--- | :---: | :---: |
| Giải đấu | `DIM Competition [Competition Name]` | Dropdown | 20 | 650 |
| Mùa giải | `DIM Time [Season]` | Dropdown | 690 | 600 |
| Loại giải đấu | `DIM Competition [Competition Type]` | Tile | 1310 | 590 |

---

### Bước 5 – Ô 1 (Trên - Trái): Clustered Column Chart – Sân nhà vs Sân khách Top 10 CLB
1. Visual **Clustered column chart** · `W = 925`, `H = 385`, `X = 20`, `Y = 265`.
2. **X-axis:** `DIM Club [Club Name]` · **Y-axis:** `[Measures].[Goals]` · **Legend:** `Is Home Game` (đổi nhãn `1 → Sân nhà`, `0 → Sân khách` bằng *Rename for this visual*).
3. **Filters on this visual:** `Club Name` → **Top N** = `10`, By value `Goals`.
4. Định dạng:
   * **Title:** `So sánh Bàn thắng Sân nhà vs Sân khách – Top 10 CLB`, `15 pt` Bold, căn giữa.
   * **X-axis (Tên CLB):** `12 pt`, màu **Navy `#0D47A1`**, *Label orientation* nghiêng 45° để hiển thị trọn tên CLB.
   * **Y-axis (Bàn thắng):** `12 pt`, màu **Forest Green `#1B5E20`**.
   * **Columns:** Sân nhà `#2563EB`, Sân khách `#F59E0B`.
   * **Data labels:** On, `12 pt`. **Legend:** Top center, `12 pt`.

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Sức chứa Sân vs Bàn thắng (NÂNG CAO)
1. Visual **Scatter chart** · `W = 925`, `H = 385`, `X = 975`, `Y = 265`.
2. Trường dữ liệu:
   * **Values:** `DIM Club [Club Name]`.
   * **X-axis:** `[Measures].[Stadium Capacity]`.
   * **Y-axis:** `[Measures].[Goals]`.
   * **Size:** `DIM Game [Game ID]` (Count Distinct – số trận).
   * **Legend:** `DIM Competition [Competition Name]`.
3. **Analytics** (kính lúp):
   * **Trend line:** On, màu `#64748B`, nét đứt.
   * **Median line (X):** On, nhãn `Median Sức chứa`. **Median line (Y):** On, nhãn `Median Bàn thắng`.
4. Định dạng:
   * **Title:** `Tương quan Sức chứa Sân vận động và Tổng Bàn thắng của CLB`, `15 pt` Bold.
   * **X-axis:** Title `Sức chứa sân (chỗ ngồi)`, `12 pt`, màu **Slate `#334155`**.
   * **Y-axis:** Title `Tổng bàn thắng`, `12 pt`, màu **Ocean Blue `#1565C0`**.

> **Thước đo `[Stadium Capacity]`** (bắt buộc theo rule hiển thị thuộc tính Dimension, tránh lỗi trả về chữ `All`):
> ```mdx
> CREATE MEMBER CURRENTCUBE.[Measures].[Stadium Capacity] AS
>   MAX( EXISTING [DIM Club].[Stadium Seats].[Stadium Seats].MEMBERS,
>        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE ),
>   FORMAT_STRING = "#,##0", VISIBLE = 1;
> ```

### Bước 7 – Ô 3 (Dưới - Trái): Ribbon Chart – Dịch chuyển Thứ hạng Giải đấu theo Mùa (NÂNG CAO)
1. Visual **Ribbon chart** · `W = 925`, `H = 385`, `X = 20`, `Y = 675`.
2. **X-axis:** `DIM Time [Season]` · **Y-axis:** `[Measures].[Goals]` · **Legend:** `DIM Competition [Competition Name]`.
3. **Filters on this visual:** `Competition Name` → **Top N** = `6`, By value `Goals` (6 giải hàng đầu, tránh rối mắt).
4. Định dạng:
   * **Title:** `Dịch chuyển Thứ hạng Bàn thắng giữa các Giải đấu qua các Mùa`, `15 pt` Bold.
   * **X-axis (Mùa giải):** `12 pt`, màu **Slate `#334155`**. **Y-axis:** `12 pt`, màu **Ocean Blue `#1565C0`**.
   * **Ribbons:** Transparency `30%` để thấy rõ đường chuyển hạng. **Data labels:** On, `12 pt`. **Legend:** Right, `12 pt`.

### Bước 8 – Ô 4 (Dưới - Phải): Matrix + Data Bars – Bảng xếp hạng CLB (NÂNG CAO)
1. Visual **Matrix** · `W = 925`, `H = 385`, `X = 975`, `Y = 675`.
2. **Rows:** `DIM Competition [Competition Name]` → `DIM Club [Club Name]`.
3. **Values:** `[Measures].[Stadium Capacity]`, `[Measures].[Goals]`, `[Measures].[Home Goals Ratio]`.
4. **Rename for this visual:** `Competition Name → Giải đấu`, `Club Name → Câu lạc bộ`, `Stadium Capacity → Sức chứa sân`, `Goals → Bàn thắng`, `Home Goals Ratio → Tỷ lệ bàn sân nhà`.
5. **Conditional formatting:**
   * `Bàn thắng` → **Data bars**, Positive bar `#3B82F6`.
   * `Tỷ lệ bàn sân nhà` → **Background color** gradient `#FFFFFF` (50%) → `#FEF3C7` (≥ 65%).
6. Định dạng:
   * **Title:** `Bảng Xếp hạng CLB theo Sức chứa Sân và Lợi thế Sân nhà`, `15 pt` Bold.
   * **Row headers:** `12 pt` Bold, Text wrap **On**, **Stepped layout Off**.
   * **Column headers:** `12 pt` Bold, Text wrap **On**, Auto-size width **On**, nền `#F1F5F9`.
   * **Values:** `12 pt`, Text wrap **On**. **Subtotals:** `12 pt` Bold.

---

## 4. Kết quả và Nhận xét Phân tích
* **Tương tác:** Chọn `Premier League` trên Slicer → 4 KPI, cột sân nhà/khách, scatter sức chứa, ribbon và bảng xếp hạng lọc đồng bộ theo giải đấu.
* **Nhận xét chuyên môn:**
  * **Lợi thế sân nhà:** Tỷ lệ bàn sân nhà của nhóm CLB hàng đầu dao động quanh **56% – 62%**, lệch rõ khỏi mốc trung tính 50% → lợi thế sân nhà có thật về mặt thống kê.
  * **Sức chứa sân:** Đường xu hướng dốc lên cho thấy tương quan **dương**, nhưng nhiều CLB nằm dưới Median sức chứa vẫn vượt Median bàn thắng → sức chứa sân phản ánh quy mô thương mại nhiều hơn là nguyên nhân trực tiếp của hiệu quả tấn công (*tương quan ≠ nhân quả*).
  * **Dịch chuyển giải đấu:** Ribbon chart cho thấy thứ hạng hỏa lực giữa các giải thay đổi qua mùa, là căn cứ cho nhà tài trợ lựa chọn thị trường.

> [!IMPORTANT]
> Các con số nhận xét phải được đối chiếu lại với kết quả thực tế trên Cube (Clean Testing Protocol) trước khi đưa vào báo cáo nộp.
