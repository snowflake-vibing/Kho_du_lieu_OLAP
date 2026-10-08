# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_TIME (THỜI GIAN)

> **Bảng đích:** `[dbo].[DIM_Time]`  
> **Tệp dữ liệu nguồn:** `games.csv` (hoặc `appearances.csv`)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`100`** (`[DT_WSTR, 100]`) cho 100% các cột chuỗi trong `DIM_Time`, đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```
[1. Flat File Source (games.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu dc_date & dc_season 100)]
       │
       ▼
[3. Derived Column (Bóc tách Time_ID YYYYMMDD, Full_Date, Day, Month, Quarter, Year, Season, Is_Weekend)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ 9 cột thời gian)]
       │
       ▼ (Output: Valid_Time)
[5. Sort (Sort Ascending theo Time_ID & Distinct loại trùng ngày)]
       │
       ▼
[6. OLE DB Destination (dbo.DIM_Time - Table lock, Fast Load)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc thuộc tính ngày từ `games.csv`)
* **Connection Manager**: `FF_Time` (Code page `65001 - UTF-8`).
* **Selected Columns**: `date`, `season`.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100)
* `date` $\rightarrow$ **`dc_date`** (`[DT_WSTR]`, Length: **100**)
* `season` $\rightarrow$ **`dc_season`** (`[DT_WSTR]`, Length: **100**)

### Khối 3: `Derived Column` (Bóc tách thuộc tính thời gian)

| Cột Sinh ra | Data Type | Length | Biểu thức tính toán SSIS (Expression) |
| :--- | :--- | :--- | :--- |
| **`Time_ID`** | `[DT_I4]` | - | `(YEAR((DT_DATE)dc_date) * 10000) + (MONTH((DT_DATE)dc_date) * 100) + DAY((DT_DATE)dc_date)` |
| **`Full_Date`** | `[DT_WSTR]` | **100** | `dc_date` |
| **`Day`** | `[DT_I4]` | - | `DATEPART("dd", (DT_DBTIMESTAMP)dc_date)` |
| **`Month`** | `[DT_I4]` | - | `DATEPART("mm", (DT_DBTIMESTAMP)dc_date)` |
| **`Quarter`** | `[DT_I4]` | - | `DATEPART("qq", (DT_DBTIMESTAMP)dc_date)` |
| **`Year`** | `[DT_I4]` | - | `DATEPART("yy", (DT_DBTIMESTAMP)dc_date)` |
| **`Day_Of_Week`** | `[DT_WSTR]` | **100** | Tên thứ trong tuần |
| **`Season`** | `[DT_WSTR]` | **100** | `"Mùa " + dc_season` (Ví dụ: `"Mùa 2023"`) |
| **`Is_Weekend`** | `[DT_I4]` | - | `DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 1 \|\| DATEPART("dw", (DT_DBTIMESTAMP)dc_date) == 7 ? 1 : 0` |

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ 9 CỘT THỜI GIAN)
* **Input Columns**: Đưa ĐẦY ĐỦ 9 CỘT (`dc_date`, `dc_season`, `Time_ID`, `Full_Date`, `Day`, `Month`, `Quarter`, `Year`, `Season`) vào Input.
* **Output Name**: `Valid_Time`
* **Condition Expression**:
  ```c
  !ISNULL(dc_date) && LEN(TRIM(dc_date)) > 0 &&
  !ISNULL(dc_season) && LEN(TRIM(dc_season)) > 0 &&
  !ISNULL(Time_ID) && Time_ID > 0 &&
  !ISNULL(Full_Date) && LEN(TRIM(Full_Date)) > 0 &&
  !ISNULL(Day) && Day > 0 &&
  !ISNULL(Month) && Month > 0 &&
  !ISNULL(Quarter) && Quarter > 0 &&
  !ISNULL(Year) && Year > 0 &&
  !ISNULL(Season) && LEN(TRIM(Season)) > 0
  ```
* **Default Output Name**: `Invalid_Time`

### Khối 5: `Sort` (Khử trùng lặp theo Time_ID)
* **Input Path**: Chọn nhánh **`Valid_Time`**.
* **Sort Column**: Tick chọn `Time_ID` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Time]`.
* **Mappings**: Ánh xạ đầy đủ các thuộc tính ngày, tháng, năm vào `dbo.DIM_Time`.
