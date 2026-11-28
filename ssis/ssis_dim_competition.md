# HƯỚNG DẪN CẤU HÌNH DATA FLOW: DIM_COMPETITION (GIẢI ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Competition]`  
> **Tệp dữ liệu nguồn:** `cleaned_competitions.csv` (13 dòng, 4 cột)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Bỏ khối `Data Conversion` và khối `Derived Column`; khai báo kiểu ở `FF_Competition → Advanced`, giữ nguyên `NULL` cho `Country_Name` của các giải quốc tế và giữ nguyên tên cột CSV.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (FF_Competition: cleaned_competitions.csv)] ──(Error Output: Redirect row)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Conditional Split (Valid_Competition / Rejected_Rows)] ──(Rejected_Rows)─────────────────────► [Ghi lý do từ chối]
        │ (Valid_Competition)
        ▼
[3. Sort (competition_id ASC + toàn bộ cột nạp, Remove rows with duplicate sort values)]
        │
        ▼
[4. Script Component (Tách nhóm 1 dòng / nhóm nhiều dòng trùng khóa khác nội dung)] ────────► [Nhánh rà soát trùng]
        │ (Nhóm 1 dòng hợp lệ)
        ▼
[5. OLE DB Destination (dbo.DIM_Competition - Fast Load, Keep nulls, Check constraints)] ────────► [Ghi lỗi đích]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG BƯỚC

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Competition`)

1. Trong Control Flow, kéo **Data Flow Task** vào `Sequence Container: Load Dimensions`, đổi tên thành **`DIM_Competition`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Competition`**.
3. Trong tab **General**: chọn `cleaned_competitions.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Competition`

Tên cột đầu ra giữ nguyên theo CSV và được dùng trực tiếp ở các thành phần tiếp theo:

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `competition_id` | `DT_WSTR (100)` | `Competition_ID` |
| `name` | `DT_WSTR (200)` | `Competition_Name` |
| `country_name` | `DT_WSTR (200)` | `Country_Name` |
| `type` | `DT_WSTR (100)` | `Competition_Type` |

*(Kiểm tra các mã giải như `GB1` hoặc `CL` được đọc dưới dạng chuỗi; với các giải quốc tế, ô `Country_Name` có thể trống và được giữ `NULL` theo nguồn).*

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Competition`, kiểm tra đúng số cột, chữ có dấu UTF-8 và các ô trống, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow** và kiểm tra các cột đầu ra ở tab **Columns**. Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và kiểm tra lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Conditional Split**.
- Thêm dòng **Order 1** với **Output Name**: **`Valid_Competition`**, nhập biểu thức:

```c
!ISNULL(competition_id) && LEN(TRIM(competition_id)) > 0
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 5: Sắp xếp và xử lý dòng lặp (`Sort` + `Script Component`)

1. Nối nhánh `Valid_Competition` vào **Sort** (`Sort Input`).
2. Trong **Sort Editor**: chọn `competition_id` làm cột sắp xếp tăng dần (`Ascending`). Để loại dòng lặp hoàn toàn, đưa toàn bộ cột dùng để nạp vào tập khóa sắp xếp, giữ các cột cần thiết ở đầu ra và bật **Remove rows with duplicate sort values**. Kiểm tra tùy chọn so sánh chuỗi của `Sort` để tránh gộp nhầm hai mã chỉ khác chữ hoa và chữ thường.
3. Sau `Sort`, dùng **Script Component** kiểu **Transformation** với hai đầu ra không đồng bộ: gom các dòng liên tiếp theo khóa `competition_id`, chuyển nhóm một dòng tới đích và nhóm nhiều dòng tới nhánh rà soát; xử lý nhóm cuối khi luồng kết thúc.

### Bước 6: Kết nối `OLE DB Destination` và ánh xạ (`[dbo].[DIM_Competition]`)

- Kéo **OLE DB Destination**, nối từ đầu ra hợp lệ của `Script Component`.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[DIM_Competition]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Mappings (4 cột)**:
  - `competition_id` $\rightarrow$ `Competition_ID` (`NVARCHAR(100)`)
  - `name` $\rightarrow$ `Competition_Name` (`NVARCHAR(200)`)
  - `country_name` $\rightarrow$ `Country_Name` (`NVARCHAR(200)`)
  - `type` $\rightarrow$ `Competition_Type` (`NVARCHAR(100)`)
- Mở **Error Output**, chuyển dòng lỗi sang nhánh ghi lỗi rồi bấm **OK**.

---

## 3. ĐỐI SOÁT SAU NẠP

- Tổng số dòng kỳ vọng: **13** giải đấu.
- Kiểm tra mã giải ở dạng chuỗi và `Country_Name` của các giải quốc tế giữ nguyên `NULL` theo nguồn.

```sql
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Competition;
```
