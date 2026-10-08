# HƯỚNG DẪN CẤU HÌNH KHỐI (BLOCKS) SSIS ETL: DIM_COMPETITION (GIẢI ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Competition]`  
> **Tệp dữ liệu nguồn:** `cleaned_competitions.csv` (hoặc `competitions.csv`)  
> **Database:** `DW_Football_Analytics`  
> **Chuẩn độ dài Chuỗi (String Length Standard):** Chỉ sử dụng duy nhất chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), đảm bảo **100% SẠCH WARNING**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```
[1. Flat File Source (competitions.csv)]
       │
       ▼
[2. Data Conversion (Ép kiểu DT_WSTR 100/200)]
       │
       ▼
[3. Derived Column (Chuẩn hóa Competition_Type & Xử lý NULL Country_Name)]
       │
       ▼
[4. Conditional Split (Validation kiểm tra thuộc tính Giải đấu)]
       │
       ▼ (Output: Valid_Competition)
[5. Sort (Sort Ascending theo Competition_ID & Distinct loại trùng)]
       │
       ▼
[6. OLE DB Destination (dbo.DIM_Competition - Table lock, Fast Load)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG KHỐI (BLOCK BY BLOCK CONFIGURATION)

### Khối 1: `Flat File Source` (Đọc file `cleaned_competitions.csv`)
* **Connection Manager**: `FF_Competition` (Code page `65001 - UTF-8`, Text qualifier `"`).
* **Selected Columns** (4 cột): `competition_id`, `name`, `country_name`, `type`.
* **Output Column Length**: Đặt **200** cho tất cả các cột chuỗi.

### Khối 2: `Data Conversion` (Ép kiểu dữ liệu chuẩn 100 / 200)

| Cột Nguồn | Output Alias | Data Type | Length | Ghi chú chuyển đổi |
| :--- | :--- | :--- | :--- | :--- |
| `competition_id` | **`dc_competition_id`** | Unicode string `[DT_WSTR]` | **100** | Mã giải đấu ngắn (BK như `GB1`, `ES1`, `CL`) |
| `name` | **`dc_name`** | Unicode string `[DT_WSTR]` | **200** | Tên thương hiệu giải đấu |
| `country_name` | **`dc_country_name`** | Unicode string `[DT_WSTR]` | **200** | Quốc gia đăng cai |
| `type` | **`dc_type`** | Unicode string `[DT_WSTR]` | **100** | Phân loại (*domestic_league, international_cup*) |

### Khối 3: `Derived Column` (Chuẩn hóa dữ liệu & Xử lý NULL)

* **`der_country_name`** (`[DT_WSTR]`, 200):  
  `ISNULL(dc_country_name) || LEN(TRIM(dc_country_name)) == 0 ? "Europe" : TRIM(dc_country_name)`
* **`der_competition_type`** (`[DT_WSTR]`, 100):  
  `ISNULL(dc_type) || LEN(TRIM(dc_type)) == 0 ? "domestic_league" : TRIM(dc_type)`

### Khối 4: `Conditional Split` (Validation kiểm tra dữ liệu)
* **Input Columns**: Đưa ĐẦY ĐỦ 4 CỘT (`dc_competition_id`, `dc_name`, `der_country_name`, `der_competition_type`) vào Input.
* **Output Name**: `Valid_Competition`
* **Condition Expression**:
  ```c
  !ISNULL(dc_competition_id) && LEN(TRIM(dc_competition_id)) > 0 &&
  !ISNULL(dc_name) && LEN(TRIM(dc_name)) > 0
  ```
* **Default Output Name**: `Invalid_Competition`

### Khối 5: `Sort` (Khử trùng lặp theo Competition_ID)
* **Input Path**: Chọn nhánh **`Valid_Competition`**.
* **Pass Through Columns**: Tick chọn cả 4 cột.
* **Sort Column**: Tick chọn `dc_competition_id` (Sort Type: `Ascending`, Sort Order: `1`).
* **Option quan trọng**: Tick chọn **`Remove rows with duplicate sort values`**.

### Khối 6: `OLE DB Destination` (Nạp dữ liệu vào SQL Server)
* **Connection Manager**: OLE DB Connection đến `DW_Football_Analytics`.
* **Data Access Mode**: `Table or view - fast load`.
* **Table**: `[dbo].[DIM_Competition]`.
* **Mappings**:
  * `dc_competition_id` $\rightarrow$ **`Competition_ID`** (`nvarchar(100)`)
  * `dc_name` $\rightarrow$ **`Competition_Name`** (`nvarchar(200)`)
  * `der_country_name` $\rightarrow$ **`Country_Name`** (`nvarchar(200)`)
  * `der_competition_type` $\rightarrow$ **`Competition_Type`** (`nvarchar(100)`)
