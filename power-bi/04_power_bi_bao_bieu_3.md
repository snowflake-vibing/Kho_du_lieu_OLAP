# 4.2.3 Báo biểu 3: Kỷ luật Thẻ phạt, Cường độ Thi đấu và Tải trọng Cầu thủ (Discipline & Match Load Analytics)

Tài liệu hướng dẫn thiết kế **Báo biểu 3** trên **Power BI Desktop** (Live Connection tới Cube `[DW Football Transfermarkt]`), tuân thủ toàn bộ quy chuẩn tại [rule.md](../rule.md): Canvas **1920 x 1080 px**, bố cục **2 tầng** (Tầng trên: Title + KPI Cards + Slicers; Tầng dưới: **lưới 2x2 đúng 4 biểu đồ nâng cao**), cỡ chữ **20 / 15 / 18 / 12 pt**, không có dấu ba chấm (`...`).

---

## 1. Mục tiêu, Ý nghĩa Thống kê và Bài toán Thực tế

### 1.1. Câu hỏi nghiệp vụ
* **CLB / vị trí nào có rủi ro kỷ luật cao nhất?** (`Yellow Cards`, `Red Cards`).
* **Nhận thẻ nhiều là do đá nhiều hay do lối chơi thiếu kỷ luật?** Đặt số thẻ trong tương quan với `Minutes Played`.
* **Độ tuổi nào đang gánh tải trọng thi đấu lớn nhất?** (`Minutes Played` theo `Age`).

### 1.2. Ý nghĩa thống kê
| Thành phần | Vấn đề thống kê được giải quyết |
| :--- | :--- |
| **Thẻ / 90 phút** | Chuẩn hóa theo thời lượng ra sân, khử **Exposure Time Bias**: cầu thủ đá 3.000 phút đương nhiên có nhiều thẻ hơn cầu thủ đá 500 phút. |
| **Scatter Số phút vs Thẻ vàng + 2 đường Median** | Phân tích 2 biến định lượng; điểm nằm **trên** đường xu hướng là cầu thủ nhận thẻ nhiều hơn mức “kỳ vọng” theo thời lượng. Median kháng nhiễu ngoại lai. |
| **Combo chart theo Độ tuổi (2 trục Y)** | Đặt tải trọng (cột) và rủi ro thẻ (đường) trên cùng một trục tuổi để quan sát **đồng biến / nghịch biến**. |

### 1.3. Bài toán thực tế giải quyết
1. **Ban huấn luyện:** Nhận diện cầu thủ “thẻ cao bất thường” (góc trên-trái scatter: ít phút nhưng nhiều thẻ) để điều chỉnh vai trò, tránh treo giò ở trận quan trọng.
2. **Bộ phận y tế – thể lực:** Nhóm tuổi chịu tải trọng cao nhất là nhóm cần luân chuyển (rotation) để phòng chấn thương.
3. **Ban điều hành CLB:** CLB nằm trong Top thẻ phạt có rủi ro bị phạt tiền / án treo giò từ ban tổ chức giải.

---

## 2. Sơ đồ Bố cục Pixel-Perfect (Canvas 1920 x 1080)

```
+-------------------------------------------------------------------------------------------------------------------------+
| [TITLE] BÁO BIỂU 3: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ (20pt Bold)                                  |
| X = 20, Y = 15 | W = 1880, H = 55                                                                                       |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Card 1: Tổng Thẻ Vàng]   | [Card 2: Tổng Thẻ Đỏ]     | [Card 3: Thẻ vàng / 90']    | [Card 4: Tổng Số Phút]            |
| Nền #FFFBEB               | Nền #FEF2F2               | Nền #EFF6FF                 | Nền #F0FDF4                       |
| X=20, Y=80, W=455, H=105  | X=495                     | X=970                       | X=1445                            |
+---------------------------+---------------------------+-----------------------------+-----------------------------------+
| [Slicer 1: Mùa giải] X=20, W=650           | [Slicer 2: Giải đấu] X=690, W=600     | [Slicer 3: Vị trí] X=1310, W=590        |
| Y = 195, H = 75 (chiều cao thoáng đãng, không bị cụt dropdown/tile)                                                         |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 1: TRÊN - TRÁI] Stacked Bar Chart                    | [Ô 2: TRÊN - PHẢI] SCATTER (NÂNG CAO)                         |
| Top 10 CLB nhận nhiều thẻ phạt nhất (Vàng + Đỏ)         | Số phút vs Thẻ vàng – Ma trận rủi ro kỷ luật                  |
| X = 20, Y = 265 | W = 925, H = 385                      | X = 975, Y = 265 | W = 925, H = 385                           |
+---------------------------------------------------------+---------------------------------------------------------------+
| [Ô 3: DƯỚI - TRÁI] COMBO CHART 2 TRỤC (NÂNG CAO)        | [Ô 4: DƯỚI - PHẢI] MATRIX + HEATMAP (NÂNG CAO)                |
| Tải trọng (Cột) vs Thẻ vàng (Đường) theo Độ tuổi        | Hồ sơ kỷ luật chi tiết từng cầu thủ theo CLB                  |
| X = 20, Y = 675 | W = 925, H = 385                      | X = 975, Y = 675 | W = 925, H = 385                           |
+---------------------------------------------------------+---------------------------------------------------------------+
```

> **NHẬP TỌA ĐỘ CHUẨN TỪNG PIXEL:** Chọn visual → tab **General** → **Properties** → nhập **Size** và **Position**.
>
> **HIỆU ỨNG THẺ CHO MỌI VISUAL (trừ KPI Cards):** **Effects** → Background `#FFFFFF` (0%) → Visual border On `#CBD5E1` → **Rounded corners `10 px`**.

---

## 3. Hướng dẫn Từng Bước

### Bước 1: Tạo trang và cấu hình Canvas
1. Nhấp dấu `+`, đổi tên trang thành `Kỷ luật & Tải trọng Thi đấu`.
2. **Format report page** → **Canvas settings**: Custom `1920 x 1080 px` · **Canvas background**: `#F8FAFC`, Transparency **`0%`**.

### Bước 2: Title Banner (Tầng trên)
1. **Insert** → **Text box**: `BÁO BIỂU 3: KỶ LUẬT THẺ PHẠT, CƯỜNG ĐỘ THI ĐẤU & TẢI TRỌNG CẦU THỦ`.
2. `Segoe UI`, **`20 pt`**, **Bold**, `#0F172A`, căn giữa · Effects nền `#FFFFFF`, viền `#CBD5E1`, bo `10 px`.
3. **Properties:** `W = 1880`, `H = 55`, `X = 20`, `Y = 15`.

### Bước 3: 4 Thẻ KPI (Tầng trên)
Chung: **Title** On `15 pt - 18 pt` Bold căn giữa · **Callout value** `35 pt` Bold (cực kỳ nổi bật) `#0F172A` · **Category label** Off · `W = 455`, `H = 95 - 105`, `Y = 80 - 95`.

| Thẻ | Thước đo | Title | Nền / Viền | X |
| :--- | :--- | :--- | :--- | :---: |
| Card 1 | `[Measures].[Yellow Cards]` | `TỔNG THẺ VÀNG` | `#FFFBEB` / `#FCD34D` | 20 |
| Card 2 | `[Measures].[Red Cards]` | `TỔNG THẺ ĐỎ` | `#FEF2F2` / `#FCA5A5` | 495 |
| Card 3 | `[Measures].[Yellow Cards Per 90]` (`#,##0.00`) | `THẺ VÀNG / 90 PHÚT` | `#EFF6FF` / `#93C5FD` | 970 |
| Card 4 | `[Measures].[Minutes Played]` (Display units: Millions) | `TỔNG SỐ PHÚT THI ĐẤU` | `#F0FDF4` / `#86EFAC` | 1445 |

> **Card 3 – thước đo tính toán độc lập** (tab **Calculations** của Cube, không phụ thuộc thước đo trung gian):
> ```mdx
> CREATE MEMBER CURRENTCUBE.[Measures].[Yellow Cards Per 90] AS
>   IIF( [Measures].[Minutes Played] = 0, NULL,
>        [Measures].[Yellow Cards] * 90 / [Measures].[Minutes Played] ),
>   FORMAT_STRING = "#,##0.00", VISIBLE = 1;
> ```

### Bước 4: 3 Slicers (Tầng trên)
Chung: Header `15 pt` Bold, Values `12 pt`, nền `#FFFFFF`, viền `#CBD5E1`, bo `8 px`, `Y = 195 - 210`, **`H = 75 px - 80 px`** (chiều cao thoáng đãng, hiển thị trọn vẹn thanh dropdown và các nút tile, không bị cắt chữ).

| Slicer | Trường | Kiểu | X | W |
| :--- | :--- | :--- | :---: | :---: |
| Mùa giải | `DIM Time [Season]` | Dropdown | 20 | 650 |
| Giải đấu | `DIM Competition [Competition Name]` | Dropdown | 690 | 600 |
| Vị trí thi đấu | `DIM Player [Main Position]` | Tile | 1310 | 590 |

---

### Bước 5 – Ô 1 (Trên - Trái): Stacked Bar Chart – Top 10 CLB nhận nhiều thẻ nhất
1. Visual **Stacked bar chart** · `W = 925`, `H = 385`, `X = 20`, `Y = 265 - 300`.
2. **Y-axis:** `DIM Club [Club Name]` · **X-axis:** `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`.
3. **Filters on this visual:** `Club Name` → **Top N** = `10`, By value `Yellow Cards`.
4. Định dạng:
   * **Title:** `Top 10 CLB nhận nhiều Thẻ phạt nhất Châu Âu`, `18 pt` Bold, căn giữa.
   * **Y-axis (Tên CLB):** `12 pt`, màu **Navy `#0D47A1`**, *Maximum width* đặt `35%` để hiển thị trọn tên CLB.
   * **X-axis (Số thẻ):** `12 pt`, màu **Forest Green `#1B5E20`**.
   * **Bars:** Thẻ vàng `#F59E0B`, Thẻ đỏ `#DC2626` (màu ngữ nghĩa đúng loại thẻ).
   * **Data labels:** On, `12 pt`. **Legend:** Top center, `12 pt`.

### Bước 6 – Ô 2 (Trên - Phải): Scatter Chart – Ma trận Rủi ro Kỷ luật (NÂNG CAO)
1. Visual **Scatter chart** · `W = 925`, `H = 385`, `X = 975`, `Y = 265 - 300`.
2. Trường dữ liệu:
   * **Values:** `DIM Player [Player Name]`.
   * **X-axis:** `[Measures].[Minutes Played]` · **Y-axis:** `[Measures].[Yellow Cards]`.
   * **Size:** `[Measures].[Red Cards]` · **Legend:** `DIM Player [Main Position]`.
3. **Filters on this visual:** `Player Name` → **Top N** = `40`, By value `Yellow Cards`.
4. **Analytics:** **Trend line** On (`#64748B`, nét đứt) · **Median line X** (`Median Số phút`) · **Median line Y** (`Median Thẻ vàng`).
5. Định dạng:
   * **Title:** `Ma trận Rủi ro Kỷ luật: Số phút thi đấu vs Thẻ vàng`, `18 pt` Bold, căn giữa.
   * **X-axis:** Title `Số phút thi đấu`, `12 pt`, màu **Slate `#334155`**.
   * **Y-axis:** Title `Số thẻ vàng`, `12 pt`, màu **Ocean Blue `#1565C0`**.
   * **Markers:** Defender `#10B981`, Midfield `#3B82F6`, Attack `#EF4444`, Goalkeeper `#8B5CF6`.

> **Đọc 4 góc phần tư:** Trên-Trái = **ít phút, nhiều thẻ (rủi ro cao bất thường)** · Trên-Phải = đá nhiều, thẻ nhiều (tương xứng tải trọng) · Dưới-Phải = **đá nhiều, kỷ luật tốt (hình mẫu)** · Dưới-Trái = ít ra sân.

### Bước 7 – Ô 3 (Dưới - Trái): Combo Chart 2 trục – Tải trọng vs Thẻ vàng theo Độ tuổi (NÂNG CAO)
1. Visual **Line and clustered column chart** · `W = 925`, `H = 385`, `X = 20`, `Y = 675 - 695`.
2. **X-axis:** `DIM Player [Age]` · **Column y-axis:** `[Measures].[Minutes Played]` · **Line y-axis:** `[Measures].[Yellow Cards Per 90]`.
3. Định dạng:
   * **Title:** `Tải trọng Thi đấu (Cột) và Thẻ vàng / 90 phút (Đường) theo Độ tuổi`, `18 pt` Bold, căn giữa.
   * **X-axis (Tuổi):** `12 pt`, màu **Slate `#334155`**, Type **Categorical** để hiện đủ từng tuổi.
   * **Y-axis trái (Số phút):** `12 pt`, màu **Forest Green `#1B5E20`**.
   * **Y-axis phải – Secondary (Thẻ/90):** On, `12 pt`, màu **Đỏ `#DC2626`** – mỗi trục một màu, khớp màu chuỗi dữ liệu.
   * **Columns:** `#22C55E` · **Line:** `#DC2626`, stroke 3px, markers On.
   * **Data labels:** On cho Line, `12 pt`. **Legend:** Top center, `12 pt`.

### Bước 8 – Ô 4 (Dưới - Phải): Matrix + Heatmap – Hồ sơ Kỷ luật Cầu thủ (NÂNG CAO)
1. Visual **Matrix** · `W = 925`, `H = 385`, `X = 975`, `Y = 675 - 695`.
2. **Rows:** `DIM Player [Player Name]` → `DIM Club [Club Name]`.
3. **Values:** `[Measures].[Minutes Played]`, `[Measures].[Is Starter]`, `[Measures].[Yellow Cards]`, `[Measures].[Red Cards]`, `[Measures].[Yellow Cards Per 90]`.
4. **Rename for this visual:** `Cầu thủ`, `Câu lạc bộ`, `Số phút thi đấu`, `Số trận đá chính`, `Thẻ vàng`, `Thẻ đỏ`, `Thẻ vàng / 90'`.
5. **Conditional formatting:**
   * `Thẻ vàng` → **Data bars** `#F59E0B`.
   * `Thẻ vàng / 90'` → **Background color** gradient `#FFFFFF` (thấp) → `#FECACA` (cao).
6. Định dạng:
   * **Title:** `Hồ sơ Kỷ luật & Tải trọng Chi tiết từng Cầu thủ theo CLB`, `18 pt` Bold, căn giữa.
   * **Row headers:** `12 pt` Bold, Text wrap **On**, **Stepped layout Off**.
   * **Column headers:** `12 pt` Bold, Text wrap **On**, Auto-size width **On**, nền `#F1F5F9`.
   * **Values:** `12 pt`, Text wrap **On**. **Subtotals:** `12 pt` Bold.

---

## 4. Kết quả và Nhận xét Phân tích
* **Tương tác:** Chọn `Defender` trên Slicer → toàn bộ KPI, Top CLB, scatter rủi ro, combo theo tuổi và bảng chi tiết lọc đồng bộ theo nhóm hậu vệ.
* **Nhận xét chuyên môn:**
  * **Vị trí:** Hậu vệ và tiền vệ chiếm phần lớn tổng số thẻ do nhiệm vụ đánh chặn; tuy nhiên chỉ số **Thẻ vàng / 90'** mới cho biết ai thực sự thiếu kỷ luật sau khi khử yếu tố thời lượng.
  * **Tải trọng theo tuổi:** Nhóm tuổi **24 – 29** gánh phần lớn số phút thi đấu; nếu đường Thẻ/90 không tăng theo thì số thẻ cao của nhóm này chủ yếu do đá nhiều, không phải do lối chơi.
  * **Rủi ro bất thường:** Cầu thủ ở góc Trên-Trái scatter là đối tượng ưu tiên để ban huấn luyện điều chỉnh vai trò.

> [!IMPORTANT]
> Các con số nhận xét phải được đối chiếu lại với kết quả thực tế trên Cube (Clean Testing Protocol) trước khi đưa vào báo cáo nộp.
