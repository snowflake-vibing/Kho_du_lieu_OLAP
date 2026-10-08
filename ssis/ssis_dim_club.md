# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_CLUB (CÂU LẠC BỘ)

> **Bảng đích:** `[dbo].[DIM_Club]`  
> **Tệp dữ liệu nguồn:** `cleaned_clubs.csv` (hoặc `clubs.csv`)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`200`** (`[DT_WSTR, 200]`) cho 100% các cột chuỗi của bảng Club, đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```
[1. Flat File Source (clubs.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_I4 & DT_WSTR 200)]
       │
       ▼
[3. Derived Column (Xử lý NULL Stadium_Name, Coach_Name, Stadium_Seats)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ 6 cột)]
       │
       ▼ (Output: Valid_Club)
[5. Sort (Sort Ascending theo Club_ID & Distinct loại trùng)]
       │
       ▼
[6. OLE DB Destination (dbo.DIM_Club - Table lock, Fast Load)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc file `cleaned_clubs.csv`)
* **Connection Manager**: `FF_Club` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (6 cột): `club_id`, `name`, `stadium_name`, `stadium_seats`, `coach_name`, `squad_size`.
* **Output Column Length**: Đặt **200** cho tất cả các cột kiểu chuỗi ký tự.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `club_id` | **`dc_club_id`** | Four-byte signed integer `[DT_I4]` | - | Mã CLB tự nhiên (BK) |
| `name` | **`dc_club_name`** | Unicode string `[DT_WSTR]` | **200** | Tên câu lạc bộ |
| `stadium_name` | **`dc_stadium_name`** | Unicode string `[DT_WSTR]` | **200** | Tên sân vận động nhà |
| `stadium_seats` | **`dc_stadium_seats`** | Four-byte signed integer `[DT_I4]` | - | Sức chứa tối đa khán đài |
| `coach_name` | **`dc_coach_name`** | Unicode string `[DT_WSTR]` | **200** | Họ tên Huấn luyện viên |
| `squad_size` | **`dc_squad_size`** | Four-byte signed integer `[DT_I4]` | - | Số lượng cầu thủ đội 1 |

### Khối 3: `Derived Column` (Xử lý NULL & Gán mặc định)

* **`der_stadium_name`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_stadium_name) || LEN(TRIM(dc_stadium_name)) == 0 ? "Unknown Stadium" : TRIM(dc_stadium_name)`
* **`der_coach_name`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_coach_name) || LEN(TRIM(dc_coach_name)) == 0 ? "Unknown Coach" : TRIM(dc_coach_name)`
* **`der_stadium_seats`** (`[DT_I4]`):  
  `ISNULL(dc_stadium_seats) ? 0 : dc_stadium_seats`

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 6 CỘT)
* **Input Columns**: Đưa ĐẦY ĐỦ 6 CỘT (`dc_club_id`, `dc_club_name`, `der_stadium_name`, `der_stadium_seats`, `der_coach_name`, `dc_squad_size`) vào Input.
* **Output Name**: `Valid_Club`
* **Condition Expression**:
  ```c
  !ISNULL(dc_club_id) && dc_club_id > 0 &&
  !ISNULL(dc_club_name) && LEN(TRIM(dc_club_name)) > 0 &&
  !ISNULL(der_stadium_name) && LEN(TRIM(der_stadium_name)) > 0 &&
  !ISNULL(der_stadium_seats) && der_stadium_seats >= 0 &&
  !ISNULL(der_coach_name) && LEN(TRIM(der_coach_name)) > 0 &&
  !ISNULL(dc_squad_size) && dc_squad_size >= 0
  ```
* **Default Output Name**: `Invalid_Club`

### Khối 5: `Sort` (Khử trùng lặp theo Club_ID)
* **Input Path**: Chọn nhánh **`Valid_Club`**.
* **Pass Through Columns**: Tick chọn cả 6 cột.
* **Sort Column**: Tick chọn `dc_club_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Club]`.
* **Mappings**:
  * `dc_club_id` $\rightarrow$ **`Club_ID`** (`int`)
  * `dc_club_name` $\rightarrow$ **`Club_Name`** (`nvarchar(200)`)
  * `der_stadium_name` $\rightarrow$ **`Stadium_Name`** (`nvarchar(200)`)
  * `der_stadium_seats` $\rightarrow$ **`Stadium_Seats`** (`int`)
  * `der_coach_name` $\rightarrow$ **`Coach_Name`** (`nvarchar(200)`)
  * `dc_squad_size` $\rightarrow$ **`Squad_Size`** (`int`)
