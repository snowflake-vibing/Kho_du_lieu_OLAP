# HƯỚNG DẪN CẤU HÌNH DATA FLOW: DIM_PLAYER (CẦU THỦ)

> **Bảng đích:** `[dbo].[DIM_Player]`  
> **Tệp dữ liệu nguồn:** `cleaned_players.csv` (7.069 dòng, 8 cột)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Bỏ khối `Data Conversion`, khai báo kiểu ở `FF_Player → Advanced`, bỏ cột `Age` khỏi `DIM_Player`, tách ngày sinh kiểu `DATE` qua `Birth_Date` và giữ `NULL` cho ngày sinh/chiều cao bị thiếu.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (FF_Player: cleaned_players.csv)] ──(Error Output: Redirect row)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Derived Column (Tách phần ngày cho Birth_Date từ date_of_birth)]
        │
        ▼
[3. Conditional Split (Valid_Player / Rejected_Rows)] ──(Rejected_Rows)────────────────► [Ghi lý do từ chối]
        │ (Valid_Player)
        ▼
[4. Sort (player_id ASC + toàn bộ cột nạp, Remove rows with duplicate sort values)]
        │
        ▼
[5. Script Component (Tách nhóm 1 dòng / nhóm nhiều dòng trùng khóa khác nội dung)] ───► [Nhánh rà soát trùng]
        │ (Nhóm 1 dòng hợp lệ)
        ▼
[6. OLE DB Destination (dbo.DIM_Player - Fast Load, Keep nulls, Check constraints)] ───► [Ghi lỗi đích]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG BƯỚC

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Player`)

1. Trong Control Flow, kéo **Data Flow Task** vào `Sequence Container: Load Dimensions`, đổi tên thành **`DIM_Player`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Player`**.
3. Trong tab **General**: chọn `cleaned_players.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Player`

Tên cột đầu ra giữ nguyên theo CSV và được dùng trực tiếp ở các thành phần tiếp theo:

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `player_id` | `DT_I4` | `Player_ID` |
| `name` | `DT_WSTR (200)` | `Player_Name` |
| `date_of_birth` | `DT_DBTIMESTAMP` | Đọc chuỗi nguồn có giờ (`YYYY-MM-DD 00:00:00`), lấy phần ngày cho `Date_Of_Birth` |
| `country_of_citizenship` | `DT_WSTR (200)` | `Country_Of_Citizenship` |
| `position` | `DT_WSTR (100)` | `Main_Position` |
| `sub_position` | `DT_WSTR (100)` | `Sub_Position` |
| `foot` | `DT_WSTR (100)` | `Foot` |
| `height_in_cm` | `DT_I4` | `Height_In_Cm` |

*(Các mẫu `date_of_birth` từ notebook có dạng `YYYY-MM-DD 00:00:00`; trong Preview kiểm tra ngày có giờ và các ô trống để phần giờ được bỏ ở `Derived Column`).*

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Player`, kiểm tra đúng số cột, chữ có dấu UTF-8 và các ô trống, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow** và kiểm tra các cột đầu ra ở tab **Columns**. Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và kiểm tra lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Lấy phần ngày sinh bằng `Derived Column`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Derived Column**.
- Thêm cột **`Birth_Date`** ở chế độ **`<add as new column>`** với biểu thức sau (giá trị thiếu đi tiếp dưới dạng `NULL`):

```c
ISNULL(date_of_birth) ? NULL(DT_DBDATE) : (DT_DBDATE)date_of_birth
```

*(Không tính `Age` tĩnh và không điền thay các giá trị mặc định cho tên, quốc tịch, chân thuận hay chiều cao).*

### Bước 5: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra của `Derived Column` vào **Conditional Split**.
- Thêm dòng **Order 1** với **Output Name**: **`Valid_Player`**, nhập biểu thức:

```c
!ISNULL(player_id) && player_id > 0
&& (ISNULL(height_in_cm) || height_in_cm > 0)
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 6: Sắp xếp và xử lý dòng lặp (`Sort` + `Script Component`)

1. Nối nhánh `Valid_Player` vào **Sort** (`Sort Input`).
2. Trong **Sort Editor**: chọn `player_id` làm cột sắp xếp tăng dần (`Ascending`). Để loại dòng lặp hoàn toàn, đưa toàn bộ cột dùng để nạp vào tập khóa sắp xếp, giữ các cột cần thiết ở đầu ra và bật **Remove rows with duplicate sort values**. Kiểm tra tùy chọn so sánh chuỗi của `Sort` để tránh gộp nhầm mã chỉ khác chữ hoa/thường.
3. Sau `Sort`, dùng **Script Component** kiểu **Transformation** với hai đầu ra không đồng bộ: gom các dòng liên tiếp theo khóa `player_id`, chuyển nhóm một dòng tới đích và nhóm nhiều dòng tới nhánh rà soát; xử lý nhóm cuối khi luồng kết thúc.

### Bước 7: Kết nối `OLE DB Destination` và ánh xạ (`[dbo].[DIM_Player]`)

- Kéo **OLE DB Destination**, nối từ đầu ra hợp lệ của `Script Component`.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[DIM_Player]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Mappings (8 cột)**:
  - `player_id` $\rightarrow$ `Player_ID` (`INT`)
  - `name` $\rightarrow$ `Player_Name` (`NVARCHAR(200)`)
  - `Birth_Date` $\rightarrow$ `Date_Of_Birth` (`DATE`)
  - `country_of_citizenship` $\rightarrow$ `Country_Of_Citizenship` (`NVARCHAR(200)`)
  - `position` $\rightarrow$ `Main_Position` (`NVARCHAR(100)`)
  - `sub_position` $\rightarrow$ `Sub_Position` (`NVARCHAR(100)`)
  - `foot` $\rightarrow$ `Foot` (`NVARCHAR(100)`)
  - `height_in_cm` $\rightarrow$ `Height_In_Cm` (`INT`)
- Giữ `NULL` cho ngày sinh hay chiều cao bị thiếu. Vào **Error Output**, chuyển dòng lỗi sang nhánh ghi lỗi rồi bấm **OK**.

---

## 3. ĐỐI SOÁT SAU NẠP

- Tổng số dòng kỳ vọng: **7.069** hồ sơ cầu thủ.
- Kiểm tra mẫu để xác nhận tên có dấu UTF-8, `Date_Of_Birth` dạng `DATE` và các thuộc tính thiếu giữ `NULL`.

```sql
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Player;
```
