# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: FACT_PLAYER_MATCH_PERF (LUỒNG TỐI ƯU 9 KHỐI)

> **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`  
> **Tệp dữ liệu nguồn:** `appearances.csv` (hoặc `STG_Appearances` - 1.89 triệu lượt ra sân)  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Phương pháp ETL:** Pure Data Flow Task (Nạp trực tiếp qua chuỗi **Lookup Transformations** & 1 khối **Derived Column** duy nhất ở cuối luồng).  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU DATA FLOW (OPTIMIZED 9-BLOCK PIPELINE)

```text
[1. Flat File Source (appearances.csv) / OLE DB Source (STG_Appearances)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4, DT_WSTR 100/200)]
       │
       ▼
[3. Conditional Split (Validation kiểm tra dữ liệu hợp lệ)]
       │
       ▼ (Output: Valid_Appearance)
[4. Lookup Player (Tra cứu DIM_Player lấy Player_ID)]
       │
       ▼
[5. Lookup Club (Tra cứu DIM_Club lấy Club_ID)]
       │
       ▼
[6. Lookup Competition (Tra cứu DIM_Competition lấy Competition_ID)]
       │
       ▼
[7. Lookup Game Info (Tra cứu DIM_Game lấy Home_Club_ID & Away_Club_ID)]
       │
       ▼
[8. Derived Column - Fact Calculations & Time_ID (GOM TOÀN BỘ LOGIC TÍNH TOÁN VÀO 1 KHỐI DUY NHẤT)]
       │
       ▼
[9. OLE DB Destination (dbo.FACT_Player_Match_Perf - Fast Load 50.000 rows/batch, Table Lock)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc tệp `appearances.csv`)
* **Connection Manager**: `FF_Appearances` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (11 cột): `appearance_id`, `game_id`, `player_id`, `player_club_id`, `date` (hoặc `date_str`), `competition_id`, `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards`.
* **Output Column Length**: Thiết lập **100** cho tất cả các cột kiểu chuỗi (`appearance_id`, `date`, `competition_id`).

---

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `appearance_id` | **`dc_appearance_id`** | Unicode string `[DT_WSTR]` | **100** | Mã lượt ra sân |
| `game_id` | **`dc_game_id`** | Four-byte signed integer `[DT_I4]` | - | Mã trận đấu |
| `player_id` | **`dc_player_id`** | Four-byte signed integer `[DT_I4]` | - | Mã cầu thủ |
| `player_club_id` | **`dc_player_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã câu lạc bộ |
| `date` / `date_str` | **`dc_date_str`** | Unicode string `[DT_WSTR]` | **100** | Chuỗi ngày đấu (`YYYY-MM-DD`) |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** | Mã giải đấu |
| `goals` | **`dc_goals`** | Four-byte signed integer `[DT_I4]` | - | Số bàn thắng |
| `assists` | **`dc_assists`** | Four-byte signed integer `[DT_I4]` | - | Số đường kiến tạo |
| `minutes_played` | **`dc_minutes_played`** | Four-byte signed integer `[DT_I4]` | - | Phút thi đấu |
| `yellow_cards` | **`dc_yellow_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ vàng |
| `red_cards` | **`dc_red_cards`** | Four-byte signed integer `[DT_I4]` | - | Số thẻ đỏ |

---

### Khối 3: `Conditional Split` (Validation kiểm tra dữ liệu hợp lệ)
* **Input Columns**: Tick ĐẦY ĐỦ 11 CỘT.
* **Output Name**: `Valid_Appearance`
* **Condition Expression**:
  ```c
  !ISNULL(dc_appearance_id) && LEN(TRIM(dc_appearance_id)) > 0 &&
  !ISNULL(dc_game_id) && dc_game_id > 0 &&
  !ISNULL(dc_player_id) && dc_player_id > 0 &&
  !ISNULL(dc_player_club_id) && dc_player_club_id > 0 &&
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 &&
  !ISNULL(dc_date_str) && LEN(TRIM(dc_date_str)) >= 10 &&
  !ISNULL(dc_goals) && dc_goals >= 0 &&
  !ISNULL(dc_assists) && dc_assists >= 0 &&
  !ISNULL(dc_minutes_played) && dc_minutes_played >= 0 &&
  !ISNULL(dc_yellow_cards) && dc_yellow_cards >= 0 &&
  !ISNULL(dc_red_cards) && dc_red_cards >= 0
  ```
* **Default Output Name**: `Invalid_Appearance`

---

### Khối 4: `Lookup Player` (Tra cứu Cầu thủ - DIM_Player)
* **Tab General**: Cache mode **`Full cache`**, Connection **`OLE DB`**, No matching entries **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Player]`**.
* **Tab Columns**: Nối `dc_player_id` $\rightarrow$ `Player_ID`. Tích chọn `Player_ID` $\rightarrow$ Output Alias: **`lk_player_id`**.

---

### Khối 5: `Lookup Club` (Tra cứu Câu lạc bộ Cầu thủ - DIM_Club)
* **Tab General**: Cache mode **`Full cache`**, Connection **`OLE DB`**, No matching entries **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Club]`**.
* **Tab Columns**: Nối `dc_player_club_id` $\rightarrow$ `Club_ID`. Tích chọn `Club_ID` $\rightarrow$ Output Alias: **`lk_club_id`**.

---

### Khối 6: `Lookup Competition` (Tra cứu Giải đấu - DIM_Competition)
* **Tab General**: Cache mode **`Full cache`**, Connection **`OLE DB`**, No matching entries **`Ignore failure`**.
* **Tab Connection**: Chọn bảng **`[dbo].[DIM_Competition]`**.
* **Tab Columns**: Nối `dc_competition_id` $\rightarrow$ `Competition_ID`. Tích chọn `Competition_ID` $\rightarrow$ Output Alias: **`lk_competition_id`**.

---

### Khối 7: `Lookup Game Info` (Tra cứu Trận đấu lấy Đội nhà & Đội khách)
* **Mục đích:** Trong file nguồn `appearances.csv` chỉ chứa `game_id` và `player_club_id` (đội của cầu thủ), **KHÔNG CÓ** thông tin trận đó ai là Đội nhà, ai là Đội khách, hay Đội đối thủ là ai. Khối này tra cứu vào `DIM_Game` để lấy về **`Home_Club_ID`** và **`Away_Club_ID`**.
* **Cấu hình chi tiết:**
  * **Tab General**: Cache mode **`Full cache`**, Connection **`OLE DB`**, No matching entries **`Ignore failure`**.
  * **Tab Connection**: Chọn tùy chọn **Use results of an SQL query**:
    ```sql
    SELECT Game_ID, Home_Club_ID, Away_Club_ID 
    FROM dbo.DIM_Game
    ```
  * **Tab Columns**:
    * Nối cột đầu vào `dc_game_id` $\rightarrow$ `Game_ID`.
    * Tích chọn ô `Home_Club_ID` $\rightarrow$ Giữ nguyên Output Alias: **`Home_Club_ID`**.
    * Tích chọn ô `Away_Club_ID` $\rightarrow$ Giữ nguyên Output Alias: **`Away_Club_ID`**.

> 💡 **Ví dụ minh họa dễ hiểu:**  
> Trận đấu `Game_ID = 555` giữa **Real Madrid (Home_Club_ID = 10)** và **Barcelona (Away_Club_ID = 20)**.  
> * **Vinicius** (`player_club_id = 10`): Khối 7 nhả ra `Home_Club_ID = 10`, `Away_Club_ID = 20`. Tại Khối 8 (Derived Column), SSIS so sánh `player_club_id (10) == Home_Club_ID (10)` $\rightarrow$ **`Is_Home_Game = 1`** và đối thủ **`Opponent_Club_ID = 20 (Barcelona)`**.  
> * **Lewandowski** (`player_club_id = 20`): Khối 7 nhả ra `Home_Club_ID = 10`, `Away_Club_ID = 20`. SSIS thấy `20 != 10` $\rightarrow$ **`Is_Home_Game = 0`** (sân khách) và đối thủ **`Opponent_Club_ID = 10 (Real Madrid)`**.

---

#### Khối 8: `Derived Column` - Fact Calculations & Time_ID (ĐÚNG 5 CỘT BIẾN ĐỔI CHƯƠNG 1)
* **Tên khối**: `Derived Column - Fact Calculations`
* **Mục đích**: Chỉ tính toán và bóc tách **ĐÚNG 5 CỘT DỮ LIỆU TÍNH TOÁN (DERIVED)** đã quy định trong Chương 1 (`Time_ID`, `Goal_Contributions`, `Is_Starter`, `Is_Home_Game`, `Opponent_Club_ID`). Các cột ID khác (`lk_player_id`, `lk_club_id`, `lk_competition_id`, `dc_game_id`) được truyền thẳng từ khối Lookup/Source sang OLE DB Destination.

| Derived Column Name | Derived Column | Expression | Data Type | Length |
| :--- | :--- | :--- | :--- | :--- |
| **`Time_ID`** | Add as new column | `ISNULL(dc_date_str) \|\| LEN(TRIM(dc_date_str)) < 10 ? 19000101 : (DT_I4)(SUBSTRING(dc_date_str, 1, 4) + SUBSTRING(dc_date_str, 6, 2) + SUBSTRING(dc_date_str, 9, 2))` | `[DT_I4]` | - |
| **`Goal_Contributions`** | Add as new column | `dc_goals + dc_assists` | `[DT_I4]` | - |
| **`Is_Starter`** | Add as new column | `dc_minutes_played >= 60` *(hoặc `dc_minutes_played >= 60 ? 1 : 0`)* | `[DT_BOOL]` | - |
| **`Is_Home_Game`** | Add as new column | `!ISNULL(Home_Club_ID) && dc_player_club_id == Home_Club_ID` *(hoặc `? 1 : 0`)* | `[DT_BOOL]` | - |
| **`Opponent_Club_ID`** | Add as new column | `!ISNULL(Home_Club_ID) && dc_player_club_id == Home_Club_ID ? Away_Club_ID : Home_Club_ID` | `[DT_I4]` | - |

---

### Khối 9: `OLE DB Destination` (Nạp dữ liệu vào bảng FACT_Player_Match_Perf)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[FACT_Player_Match_Perf]`.
* **Cấu hình Fast Load quan trọng**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.
* **Mappings (Ánh xạ chuẩn xác từng cột)**:

| Cột Luồng SSIS (Input Column) | Cột Đích SQL Server (Target Column) | Kiểu Dữ Liệu CSDL |
| :--- | :--- | :--- |
| `lk_player_id` *(từ Lookup Player)* | **`Player_ID`** | `INT` |
| `lk_club_id` *(từ Lookup Club)* | **`Club_ID`** | `INT` |
| `Opponent_Club_ID` *(từ Derived Column)* | **`Opponent_Club_ID`** | `INT` |
| `lk_competition_id` *(từ Lookup Competition)* | **`Competition_ID`** | `NVARCHAR(100)` |
| `dc_game_id` *(từ Data Conversion)* | **`Game_ID`** | `INT` |
| `Time_ID` *(từ Derived Column)* | **`Time_ID`** | `INT` |
| `dc_minutes_played` *(từ Data Conversion)* | **`Minutes_Played`** | `INT` |
| `dc_goals` *(từ Data Conversion)* | **`Goals`** | `INT` |
| `dc_assists` *(từ Data Conversion)* | **`Assists`** | `INT` |
| `Goal_Contributions` *(từ Derived Column)* | **`Goal_Contributions`** | `INT` |
| `dc_yellow_cards` *(từ Data Conversion)* | **`Yellow_Cards`** | `INT` |
| `dc_red_cards` *(từ Data Conversion)* | **`Red_Cards`** | `INT` |
| `Is_Starter` *(từ Derived Column)* | **`Is_Starter`** | `INT` / `BIT` |
| `Is_Home_Game` *(từ Derived Column)* | **`Is_Home_Game`** | `INT` / `BIT` |

---

## 3. TẠI SAO GOM THÀNH 1 KHỐI DERIVED COLUMN LẠI TỐI ƯU HƠN?

1. **Gọn gàng & Trực quan:**  
   Thay vì tách làm 2 khối (1 khối tính `Time_ID` trước Lookup, 1 khối tính chỉ số sau Lookup), việc gom tất cả vào **Khối 8** ngay trước `OLE DB Destination` giúp luồng SSIS giảm từ 11 khối xuống còn **9 khối**, kéo thả dễ dàng và không bị phân tán logic.
2. **Loại bỏ tên biến `*_Final` dư thừa:**  
   Trước đây phải đặt tên `Player_ID_Final`, `Club_ID_Final` để tránh trùng tên với cột Lookup `lk_player_id`. Bây giờ trong khối Derived Column duy nhất, ta đặt thẳng tên cột mới là `Player_ID`, `Club_ID`, `Time_ID` trùng khớp 100% với tên cột bảng đích trong SQL Server.
3. **Hiệu năng cao hơn:**  
   Mỗi khối Transformation trong SSIS Data Flow tiêu tốn thêm tài nguyên bộ nhớ đệm (buffer memory) để trung chuyển dữ liệu giữa các khối. Gom 2 khối Derived Column thành 1 khối giúp giảm 1 bước trung chuyển đệm, tăng tốc độ xử lý cho 1.89 triệu bản ghi.

---

## 4. GIẢI THÍCH VỀ CỘT TIME_ID: CÓ CẦN DÙNG KHỐI LOOKUP TIME KHÔNG?

Có **2 phương án** thiết kế xử lý `Time_ID` tùy theo yêu cầu của bạn:

### Phương án A: Kỹ thuật Smart Surrogate Key (Khuyên dùng - Đã áp dụng ở Luồng 9 Khối trên)
* **Nguyên lý:** Khóa `Time_ID` trong `DIM_Time` được lưu theo định dạng số nguyên `YYYYMMDD` (ví dụ: ngày `2023-05-15` $\rightarrow$ `20230515`).
* **Cách thực hiện:** Khối Derived Column tự động cắt chuỗi ngày `dc_date_str` tạo ra `20230515`. Vì giá trị này **chắc chắn trùng 100%** với `Time_ID` trong `DIM_Time`, ta **KHÔNG CẦN khối `Lookup Time`**.
* **Ưu điểm:** Giảm bớt 1 khối Lookup, tiết kiệm bộ nhớ RAM, chạy nhanh nhất.

### Phương án B: Nếu bắt buộc phải có khối Lookup Time (Theo yêu cầu đồ án/bài tập)
* **Cách thực hiện:** Thêm khối `Lookup Time` chèn vào trước Khối Derived Column:
  * **Lookup Column:** Nối chuỗi ngày `dc_date_str` (`2023-05-15`) sang cột **`Full_Date`** trong `DIM_Time`.
  * **Output Column:** Tích chọn `Time_ID` $\rightarrow$ Output Alias: **`lk_time_id`**.
  * **Tại Derived Column (Khối 8):** Tính `Time_ID` bằng biểu thức: `ISNULL(lk_time_id) ? 19000101 : lk_time_id`.
* **Ưu điểm:** Đảm bảo 100% ngoại khóa `Time_ID` đều đi qua khối Lookup để kiểm tra sự tồn tại trong `DIM_Time`.

