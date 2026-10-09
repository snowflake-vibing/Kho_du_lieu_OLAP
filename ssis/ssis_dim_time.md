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
[3. Derived Column (Bóc tách 7 thuộc tính thời gian: Time_ID, Day, Month, Quarter, Year, Is_Weekend, Day_Of_Week)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra toàn bộ thuộc tính thời gian)]
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

### Khối 3: `Derived Column` (Bóc tách 7 thuộc tính thời gian - Theo chuẩn IS217)
*(Lưu ý: `Full_Date` và `Season` được ánh xạ trực tiếp từ `dc_date` và `dc_season` ở khối Destination, không tạo mới ở đây).*

| Derived Column Name | Derived Column | Expression |
| :--- | :--- | :--- |
| **`Time_ID`** | `<add as new column>` | `(YEAR((DT_DATE)dc_date) * 10000) + (MONTH((DT_DATE)dc_date) * 100) + DAY((DT_DATE)dc_date)` |
| **`Day`** | `<add as new column>` | `DATEPART("dd",(DT_DBTIMESTAMP)dc_date)` |
| **`Month`** | `<add as new column>` | `DATEPART("mm",(DT_DBTIMESTAMP)dc_date)` |
| **`Quarter`** | `<add as new column>` | `DATEPART("qq",(DT_DBTIMESTAMP)dc_date)` |
| **`Year`** | `<add as new column>` | `DATEPART("yy",(DT_DBTIMESTAMP)dc_date)` |
| **`Is_Weekend`** | `<add as new column>` | `DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 1 \|\| DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 7 ? 1 : 0` |
| **`Day_Of_Week`** | `<add as new column>` | `(DT_WSTR,50)(DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 1 ? "Sunday" : DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 2 ? "Monday" : DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 3 ? "Tuesday" : DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 4 ? "Wednesday" : DATEPART("dw",(DT_DBTIMESTAMP)dc_date) == 5 ? "Thursday" : "Saturday")` |

---

### Khối 4: `Conditional Split` (Validation kiểm tra TOÀN BỘ CỘT THỜI GIAN)
* **Input Columns**: Đưa ĐẦY ĐỦ các cột vào Input.
* **Output Name**: `Valid_Time`
* **Condition Expression**:
  ```c
  !ISNULL(dc_date) && LEN(TRIM(dc_date)) > 0 &&
  !ISNULL(dc_season) && LEN(TRIM(dc_season)) > 0 &&
  !ISNULL(Time_ID) && Time_ID > 0 &&
  !ISNULL(Day) && Day > 0 &&
  !ISNULL(Month) && Month > 0 &&
  !ISNULL(Quarter) && Quarter > 0 &&
  !ISNULL(Year) && Year > 0 &&
  !ISNULL(Day_Of_Week) && LEN(TRIM(Day_Of_Week)) > 0
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
* **Mappings**:
  * `Time_ID` *(từ Derived Column)* $\rightarrow$ **`Time_ID`** (`INT`)
  * `dc_date` *(truyền thẳng từ Data Conversion)* $\rightarrow$ **`Full_Date`** (`NVARCHAR(100)`)
  * `Day_Of_Week` *(từ Derived Column)* $\rightarrow$ **`Day_Of_Week`** (`NVARCHAR(100)`)
  * `Day` *(từ Derived Column)* $\rightarrow$ **`Day`** (`INT`)
  * `Month` *(từ Derived Column)* $\rightarrow$ **`Month`** (`INT`)
  * `Quarter` *(từ Derived Column)* $\rightarrow$ **`Quarter`** (`INT`)
  * `Year` *(từ Derived Column)* $\rightarrow$ **`Year`** (`INT`)
  * `dc_season` *(truyền thẳng từ Data Conversion)* $\rightarrow$ **`Season`** (`NVARCHAR(100)`)
  * `Is_Weekend` *(từ Derived Column)* $\rightarrow$ **`Is_Weekend`** (`INT`)
