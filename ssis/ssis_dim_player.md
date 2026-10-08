# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_PLAYER (CẦU THỦ)

> **Bảng đích:** `[dbo].[DIM_Player]`  
> **Tệp dữ liệu nguồn:** `cleaned_players.csv` (hoặc `players.csv`)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Chỉ sử dụng duy nhất chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```
[1. Flat File Source (cleaned_players.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4 & DT_WSTR 100/200)]
       │
       ▼
[3. Derived Column (Tính toán Age & Xử lý NULL Name, Country, Position, Foot, Height)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ 9 cột)]
       │
       ▼ (Output: Valid_Player)
[5. Sort (Sort Ascending theo Player_ID & Distinct loại trùng)]
       │
       ▼
[6. OLE DB Destination (dbo.DIM_Player - Table lock, Fast Load)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc file `cleaned_players.csv`)
* **Connection Manager**: `FF_Player` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (8 cột): `player_id`, `name`, `date_of_birth`, `country_of_citizenship`, `position`, `sub_position`, `foot`, `height_in_cm`.
* **Output Column Length**: Đặt **200** cho tất cả các cột chuỗi.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `player_id` | **`dc_player_id`** | Four-byte signed integer `[DT_I4]` | - | Mã cầu thủ tự nhiên (BK) |
| `name` | **`dc_player_name`** | Unicode string `[DT_WSTR]` | **200** | Họ và tên cầu thủ |
| `date_of_birth` | **`dc_date_of_birth`** | Unicode string `[DT_WSTR]` | **100** | Ngày sinh (YYYY-MM-DD) |
| `country_of_citizenship` | **`dc_country`** | Unicode string `[DT_WSTR]` | **200** | Quốc tịch thi đấu |
| `position` | **`dc_main_position`** | Unicode string `[DT_WSTR]` | **100** | Vị trí chính (*Goalkeeper, Defender...*) |
| `sub_position` | **`dc_sub_position`** | Unicode string `[DT_WSTR]` | **100** | Vị trí chi tiết (*Centre-Back...*) |
| `foot` | **`dc_foot`** | Unicode string `[DT_WSTR]` | **100** | Chân thuận (*Left, Right, Both*) |
| `height_in_cm` | **`dc_height_in_cm`** | Four-byte signed integer `[DT_I4]` | - | Chiều cao tính bằng cm |

### Khối 3: `Derived Column` (Tính toán thuộc tính & Xử lý NULL)

* **`der_age`** (`[DT_I4]`):  
  `ISNULL(dc_date_of_birth) || LEN(TRIM(dc_date_of_birth)) == 0 ? 25 : DATEDIFF("yy", (DT_DBTIMESTAMP)dc_date_of_birth, GETDATE())`
* **`der_player_name`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_player_name) || LEN(TRIM(dc_player_name)) == 0 ? "Unknown Player" : TRIM(dc_player_name)`
* **`der_country`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_country) || LEN(TRIM(dc_country)) == 0 ? "Unknown" : TRIM(dc_country)`
* **`der_foot`** (`[DT_WSTR]`, 100):  
  `ISNULL(dc_foot) || LEN(TRIM(dc_foot)) == 0 ? "Unknown" : TRIM(dc_foot)`
* **`der_height`** (`[DT_I4]`):  
  `ISNULL(dc_height_in_cm) || dc_height_in_cm < 150 || dc_height_in_cm > 220 ? 175 : dc_height_in_cm`

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 9 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 9 CỘT (`dc_player_id`, `der_player_name`, `dc_date_of_birth`, `der_age`, `der_country`, `dc_main_position`, `dc_sub_position`, `der_foot`, `der_height`) vào Input.
* **Output Name**: `Valid_Player`
* **Condition Expression**:
  ```c
  !ISNULL(dc_player_id) && dc_player_id > 0 &&
  !ISNULL(der_player_name) && LEN(TRIM(der_player_name)) > 0 &&
  !ISNULL(dc_date_of_birth) && LEN(TRIM(dc_date_of_birth)) > 0 &&
  !ISNULL(der_age) && der_age > 0 &&
  !ISNULL(der_country) && LEN(TRIM(der_country)) > 0 &&
  !ISNULL(dc_main_position) && LEN(TRIM(dc_main_position)) > 0 &&
  !ISNULL(dc_sub_position) && LEN(TRIM(dc_sub_position)) > 0 &&
  !ISNULL(der_foot) && LEN(TRIM(der_foot)) > 0 &&
  !ISNULL(der_height) && der_height > 0
  ```
* **Default Output Name**: `Invalid_Player`

### Khối 5: `Sort` (Khử trùng lặp theo Player_ID)
* **Input Path**: Chọn nhánh **`Valid_Player`**.
* **Pass Through Columns**: Tick chọn tất cả 9 cột thuộc tính.
* **Sort Column**: Tick chọn `dc_player_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Player]`.
* **Mappings**:
  * `dc_player_id` $\rightarrow$ **`Player_ID`** (`int`)
  * `der_player_name` $\rightarrow$ **`Player_Name`** (`nvarchar(200)`)
  * `dc_date_of_birth` $\rightarrow$ **`Date_Of_Birth`** (`nvarchar(100)`)
  * `der_age` $\rightarrow$ **`Age`** (`int`)
  * `der_country` $\rightarrow$ **`Country_Of_Citizenship`** (`nvarchar(200)`)
  * `dc_main_position` $\rightarrow$ **`Main_Position`** (`nvarchar(100)`)
  * `dc_sub_position` $\rightarrow$ **`Sub_Position`** (`nvarchar(100)`)
  * `der_foot` $\rightarrow$ **`Foot`** (`nvarchar(100)`)
  * `der_height` $\rightarrow$ **`Height_In_Cm`** (`int`)
