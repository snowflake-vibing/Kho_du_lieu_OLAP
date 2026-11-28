# HƯỚNG DẪN CẤU HÌNH DATA FLOW: DIM_TIME (NGÀY THI ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Time]`  
> **Tệp dữ liệu nguồn:** `cleaned_time.csv` (7.280 dòng, 1 cột `date`)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Bỏ khối `Data Conversion`, bỏ cột `Season` (chuyển sang `DIM_Game`), đọc `date` kiểu `DT_DBDATE`, dùng `Sort` gom 7.280 dòng thành **488** ngày duy nhất và dùng **2 khối `Derived Column`** tính các khóa phụ `Year_Quarter_Key`, `Year_Month_Key`, `Day_Of_Week` (`INT`, Thứ Hai = 1 .. Chủ nhật = 7) và `Is_Weekend`.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (FF_Time: cleaned_time.csv)] ──(Error Output: Redirect row)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Conditional Split (Valid_Time / Rejected_Rows)] ──(Rejected_Rows)───────────────► [Ghi lý do từ chối]
        │ (Valid_Time)
        ▼
[3. Sort (date ASC, Remove rows with duplicate sort values: 7.280 -> 488 ngày)]
        │
        ▼
[4. Derived Column 1 (Time_ID, Year, Quarter, Month, Day, Day_Of_Week)]
        │
        ▼
[5. Derived Column 2 (Year_Quarter_Key, Year_Month_Key, Is_Weekend)]
        │
        ▼
[6. OLE DB Destination (dbo.DIM_Time - Fast Load, Keep nulls, Check constraints)] ──► [Ghi lỗi đích]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG BƯỚC

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Time`)

1. Trong Control Flow, kéo **Data Flow Task** vào `Sequence Container: Load Dimensions`, đổi tên thành **`DIM_Time`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Time`**.
3. Trong tab **General**: chọn `cleaned_time.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Time`

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `date` | `DT_DBDATE` | `Full_Date` và đầu vào để tính các thuộc tính thời gian |

*(Lưu ý: nếu tệp CSV thực tế có thêm cột phụ như `Time_ID`, bỏ chọn cột phụ đó ở tab `Columns` của `Flat File Source` để tránh dư cột đầu vào).*

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Time`, kiểm tra đúng cột `date` và định dạng ngày, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow** và kiểm tra cột đầu ra ở tab **Columns**. Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và kiểm tra lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row**, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Conditional Split**.
- Thêm dòng **Order 1** với **Output Name**: **`Valid_Time`**, nhập biểu thức:

```c
!ISNULL(date)
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 5: Sắp xếp và khử trùng lặp ngày bằng `Sort`

- Nối nhánh `Valid_Time` vào **Sort** (`Sort Input`).
- Trong **Sort Editor**: chọn `date` làm cột sắp xếp tăng dần (`Ascending`) và bật **Remove rows with duplicate sort values** để giữ một dòng cho mỗi ngày.
- Đối chiếu số dòng: **7.280** dòng đầu vào được gộp thành **488** ngày duy nhất (tương ứng **6.792** lần lặp được gộp).

### Bước 6: Tạo thuộc tính lịch bằng `Derived Column` thứ nhất

Kéo **Derived Column** nối sau `Sort`, chọn **`<add as new column>`** cho từng thuộc tính:

| Cột mới | Expression |
| :--- | :--- |
| `Time_ID` | `YEAR([date]) * 10000 + MONTH([date]) * 100 + DAY([date])` |
| `Year` | `YEAR([date])` |
| `Quarter` | `DATEPART("qq", [date])` |
| `Month` | `MONTH([date])` |
| `Day` | `DAY([date])` |
| `Day_Of_Week` | `((DATEDIFF("dd", (DT_DBDATE)"1900-01-01", [date]) % 7 + 7) % 7) + 1` |

*(Công thức `Day_Of_Week` lấy thứ Hai làm ngày `1` và Chủ nhật là ngày `7`, độc lập với thiết lập `DATEFIRST` của SQL Server).*

### Bước 7: Tính khóa sắp xếp và cờ cuối tuần bằng `Derived Column` thứ hai

Kéo **Derived Column** thứ hai nối sau `Derived Column` thứ nhất, sử dụng các cột `Year`, `Quarter`, `Month` và `Day_Of_Week` vừa tạo ở chế độ **`<add as new column>`**:

| Cột mới | Expression |
| :--- | :--- |
| `Year_Quarter_Key` | `[Year] * 10 + [Quarter]` |
| `Year_Month_Key` | `[Year] * 100 + [Month]` |
| `Is_Weekend` | `[Day_Of_Week] >= 6 ? 1 : 0` |

### Bước 8: Kết nối `OLE DB Destination` và ánh xạ (`[dbo].[DIM_Time]`)

- Kéo **OLE DB Destination**, nối từ `Derived Column` thứ hai.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[DIM_Time]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Mappings (10 cột)**:
  - `date` $\rightarrow$ `Full_Date` (`DATE`)
  - `Time_ID` $\rightarrow$ `Time_ID` (`INT`)
  - `Year` $\rightarrow$ `Year` (`INT`)
  - `Quarter` $\rightarrow$ `Quarter` (`INT`)
  - `Year_Quarter_Key` $\rightarrow$ `Year_Quarter_Key` (`INT`)
  - `Month` $\rightarrow$ `Month` (`INT`)
  - `Year_Month_Key` $\rightarrow$ `Year_Month_Key` (`INT`)
  - `Day` $\rightarrow$ `Day` (`INT`)
  - `Day_Of_Week` $\rightarrow$ `Day_Of_Week` (`INT`)
  - `Is_Weekend` $\rightarrow$ `Is_Weekend` (`INT`)
- Mở **Error Output**, chuyển dòng lỗi sang nhánh ghi lỗi rồi bấm **OK**.

---

## 3. ĐỐI SOÁT SAU NẠP

- Tổng số dòng kỳ vọng: **488** ngày duy nhất.
- Kiểm tra `Time_ID` theo dạng `YYYYMMDD`, `Full_Date` kiểu `DATE` và `Is_Weekend = 1` ở thứ Bảy (`6`) và Chủ nhật (`7`).

```sql
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Time;
```
