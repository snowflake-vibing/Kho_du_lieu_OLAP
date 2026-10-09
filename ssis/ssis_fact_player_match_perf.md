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

### Khối 7: `Lookup Game Info` (Tra cứu Trận đấu lấy Đội nhà / Đội khách)
* **Tab General**: Cache mode **`Full cache`**, Connection **`OLE DB`**, No matching entries **`Ignore failure`**.
* **Tab Connection**: Tùy chọn **Use results of an SQL query**:
  ```sql
  SELECT Game_ID, Home_Club_ID, Away_Club_ID FROM dbo.DIM_Game
  ```
* **Tab Columns**:
  * Nối `dc_game_id` $\rightarrow$ `Game_ID`.
  * Tích chọn `Home_Club_ID` $\rightarrow$ Output Alias: **`lk_home_club_id`**.
  * Tích chọn `Away_Club_ID` $\rightarrow$ Output Alias: **`lk_away_club_id`**.

---

### Khối 8: `Derived Column` - Fact Calculations & Time_ID (GOM DUY NHẤT 1 KHỐI)
* **Tên khối**: `Derived Column - Fact Calculations`
* **Mục đích**: Tập trung toàn bộ logic tạo khóa `Time_ID` (`YYYYMMDD`), tính toán chỉ số độ đo (Measures), xử lý cờ động sân nhà/sân khách và thay thế giá trị `NULL` trực tiếp (không tạo cột `*_Final` dư thừa).

| Derived Column Name | Derived Column | Expression | Data Type | Length |
| :--- | :--- | :--- | :--- | :--- |
| **`Time_ID`** | Add as new column | `ISNULL(dc_date_str) \|\| LEN(TRIM(dc_date_str)) < 10 ? 19000101 : (DT_I4)(SUBSTRING(dc_date_str, 1, 4) + SUBSTRING(dc_date_str, 6, 2) + SUBSTRING(dc_date_str, 9, 2))` | `[DT_I4]` | - |
| **`Goal_Contributions`** | Add as new column | `dc_goals + dc_assists` | `[DT_I4]` | - |
| **`Is_Starter`** | Add as new column | `dc_minutes_played >= 45 ? 1 : 0` | `[DT_I4]` | - |
| **`Is_Home_Game`** | Add as new column | `!ISNULL(lk_home_club_id) && dc_player_club_id == lk_home_club_id ? 1 : 0` | `[DT_I4]` | - |
| **`Opponent_Club_ID`** | Add as new column | `!ISNULL(lk_home_club_id) && dc_player_club_id == lk_home_club_id ? lk_away_club_id : lk_home_club_id` | `[DT_I4]` | - |
| **`Player_ID`** | Add as new column | `ISNULL(lk_player_id) ? -1 : lk_player_id` | `[DT_I4]` | - |
| **`Club_ID`** | Add as new column | `ISNULL(lk_club_id) ? -1 : lk_club_id` | `[DT_I4]` | - |
| **`Competition_ID`** | Add as new column | `ISNULL(lk_competition_id) \|\| LEN(TRIM(lk_competition_id)) == 0 ? "UNKNOWN" : lk_competition_id` | `[DT_WSTR]` | **100** |

---

### Khối 9: `OLE DB Destination` (Nạp dữ liệu vào bảng FACT_Player_Match_Perf)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[FACT_Player_Match_Perf]`.
* **Cấu hình Fast Load quan trọng**:
  * **Rows per batch**: `50000`
  * **Maximum insert commit size**: `50000`
  * Tick chọn: **`Table lock`** và **`Check constraints`**.
* **Mappings (Ánh xạ gọn gàng 100% khớp tên cột)**:

| Cột Luồng SSIS (Input Column) | Cột Đích SQL Server (Target Column) | Kiểu Dữ Liệu CSDL |
| :--- | :--- | :--- |
| `Player_ID` | **`Player_ID`** | `INT` |
| `Club_ID` | **`Club_ID`** | `INT` |
| `Opponent_Club_ID` | **`Opponent_Club_ID`** | `INT` |
| `Competition_ID` | **`Competition_ID`** | `NVARCHAR(100)` |
| `dc_game_id` | **`Game_ID`** | `INT` |
| `Time_ID` | **`Time_ID`** | `INT` |
| `dc_minutes_played` | **`Minutes_Played`** | `INT` |
| `dc_goals` | **`Goals`** | `INT` |
| `dc_assists` | **`Assists`** | `INT` |
| `Goal_Contributions` | **`Goal_Contributions`** | `INT` |
| `dc_yellow_cards` | **`Yellow_Cards`** | `INT` |
| `dc_red_cards` | **`Red_Cards`** | `INT` |
| `Is_Starter` | **`Is_Starter`** | `INT` |
| `Is_Home_Game` | **`Is_Home_Game`** | `INT` |

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

