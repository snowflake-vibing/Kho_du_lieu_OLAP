# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_TIME (THỜI GIAN)

> **Bảng đích:** `[dbo].[DIM_Time]`  
> **Tệp dữ liệu nguồn:** `games.csv` (hoặc `appearances.csv`)  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`100`** (`[DT_WSTR, 100]`) cho 100% các cột chuỗi trong `DIM_Time`, đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
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

---

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100)
* `date` $\rightarrow$ **`dc_date`** (`[DT_WSTR]`, Length: **100**)
* `season` $\rightarrow$ **`dc_season`** (`[DT_WSTR]`, Length: **100**)

---

### Khối 3: `Derived Column` (Bóc tách thuộc tính thời gian)

| Derived Column Name | Derived Column | Expression | Data Type | Length |
| :--- | :--- | :--- | :--- | :--- |
| **`Time_ID`** | Add as new column | `ISNULL(dc_date) \|\| LEN(TRIM(dc_date)) < 10 ? 19000101 : (DT_I4)(SUBSTRING(dc_date, 1, 4) + SUBSTRING(dc_date, 6, 2) + SUBSTRING(dc_date, 9, 2))` | `[DT_I4]` | - |
| **`Full_Date`** | Add as new column | `TRIM(dc_date)` | `[DT_WSTR]` | **100** |
| **`Day`** | Add as new column | `(DT_I4)SUBSTRING(dc_date, 9, 2)` *(hoặc `DATEPART("dd", (DT_DBTIMESTAMP)dc_date)`)* | `[DT_I4]` | - |
| **`Month`** | Add as new column | `(DT_I4)SUBSTRING(dc_date, 6, 2)` *(hoặc `DATEPART("mm", (DT_DBTIMESTAMP)dc_date)`)* | `[DT_I4]` | - |
| **`Quarter`** | Add as new column | `(DT_I4)SUBSTRING(dc_date, 6, 2) <= 3 ? 1 : ((DT_I4)SUBSTRING(dc_date, 6, 2) <= 6 ? 2 : ((DT_I4)SUBSTRING(dc_date, 6, 2) <= 9 ? 3 : 4))` | `[DT_I4]` | - |
| **`Year`** | Add as new column | `(DT_I4)SUBSTRING(dc_date, 1, 4)` *(hoặc `DATEPART("yy", (DT_DBTIMESTAMP)dc_date)`)* | `[DT_I4]` | - |
| **`Day_Of_Week`** | Add as new column | `DATENAME("dw", (DT_DATE)dc_date)` | `[DT_WSTR]` | **100** |
| **`Season`** | Add as new column | `FINDSTRING(dc_season, "Mùa", 1) > 0 ? dc_season : "Mùa " + TRIM(dc_season)` | `[DT_WSTR]` | **100** |
| **`Is_Weekend`** | Add as new column | `DATEPART("dw", (DT_DATE)dc_date) == 1 \|\| DATEPART("dw", (DT_DATE)dc_date) == 7 ? 1 : 0` | `[DT_I4]` | - |

---

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

---

### Khối 5: `Sort` (Khử trùng lặp theo Time_ID)
* **Input Path**: Chọn nhánh **`Valid_Time`**.
* **Sort Column**: Tick chọn `Time_ID` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

---

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`).
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Time]`.
* **Mappings**: Ánh xạ đầy đủ 9 thuộc tính ngày, tháng, năm vào `dbo.DIM_Time`:
  * `Time_ID` $\rightarrow$ **`Time_ID`** (`INT`)
  * `Full_Date` $\rightarrow$ **`Full_Date`** (`NVARCHAR(100)`)
  * `Day_Of_Week` $\rightarrow$ **`Day_Of_Week`** (`NVARCHAR(100)`)
  * `Day` $\rightarrow$ **`Day`** (`INT`)
  * `Month` $\rightarrow$ **`Month`** (`INT`)
  * `Quarter` $\rightarrow$ **`Quarter`** (`INT`)
  * `Year` $\rightarrow$ **`Year`** (`INT`)
  * `Season` $\rightarrow$ **`Season`** (`NVARCHAR(100)`)
  * `Is_Weekend` $\rightarrow$ **`Is_Weekend`** (`INT`)
