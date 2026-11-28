# HƯỚNG DẪN CẤU HÌNH DATA FLOW: DIM_GAME (TRẬN ĐẤU)

> **Bảng đích:** `[dbo].[DIM_Game]`  
> **Tệp dữ liệu nguồn:** `cleaned_games.csv` (7.280 dòng, 14 cột)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Mở rộng lên 12 cột đích (bổ sung `Competition_ID`, `Season`, `Date`, `Home_Club_Manager_Name`, `Away_Club_Manager_Name`), bỏ `Data Conversion` và `Derived Column` điền giả, thêm 3 khối `Lookup` xác nhận khóa ngoại sau `Sort`/`Script Component`.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (FF_Game: cleaned_games.csv)] ──(Error Output: Redirect row)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Conditional Split (Valid_Game / Rejected_Rows)] ──(Rejected_Rows)───────────────► [Ghi lý do từ chối]
        │ (Valid_Game)
        ▼
[3. Sort (game_id ASC + toàn bộ cột nạp, Remove rows with duplicate sort values)]
        │
        ▼
[4. Script Component (Tách nhóm 1 dòng / nhóm nhiều dòng trùng khóa khác nội dung)] ► [Nhánh rà soát trùng]
        │ (Nhóm 1 dòng hợp lệ)
        ▼
[5. Lookup Game Competition (dbo.DIM_Competition)] ──(No Match Output)─────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[6. Lookup Home Club (dbo.DIM_Club)] ────────────────(No Match Output)─────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[7. Lookup Away Club (dbo.DIM_Club)] ────────────────(No Match Output)─────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[8. OLE DB Destination (dbo.DIM_Game - Fast Load, Keep nulls, Check constraints)] ──► [Ghi lỗi đích]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG BƯỚC

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Game`)

1. Trong Control Flow, kéo **Data Flow Task** vào `Sequence Container: Load Dimensions` (chạy sau khi `DIM_Club` và `DIM_Competition` thành công qua **Logical AND**), đổi tên thành **`DIM_Game`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Game`**.
3. Trong tab **General**: chọn `cleaned_games.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Game`

Tên cột đầu ra giữ nguyên theo CSV và được dùng trực tiếp ở các thành phần tiếp theo:

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `game_id` | `DT_I4` | `Game_ID` |
| `competition_id` | `DT_WSTR (100)` | `Competition_ID` |
| `season` | `DT_I4` | `Season` |
| `round` | `DT_WSTR (100)` | `Round` |
| `date` | `DT_DBDATE` | `Date` |
| `home_club_id`, `away_club_id` | `DT_I4` | `Home_Club_ID`, `Away_Club_ID` |
| `home_club_goals`, `away_club_goals` | `DT_I4` | `Home_Club_Goals`, `Away_Club_Goals` |
| `stadium` | `DT_WSTR (200)` | `Stadium` |
| `home_club_name`, `away_club_name` | `DT_WSTR (200)` | Dùng trong nhánh bổ sung `DIM_Club` (không ánh xạ vào `DIM_Game`) |
| `home_club_manager_name`, `away_club_manager_name` | `DT_WSTR (200)` | `Home_Club_Manager_Name`, `Away_Club_Manager_Name` |

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Game`, kiểm tra đúng 14 cột, chữ có dấu UTF-8 và các ô trống, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow** và kiểm tra danh sách cột đầu ra ở tab **Columns**. Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và kiểm tra lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Conditional Split**.
- Thêm dòng **Order 1** với **Output Name**: **`Valid_Game`**, nhập biểu thức:

```c
!ISNULL(game_id) && game_id > 0
&& !ISNULL(competition_id) && LEN(TRIM(competition_id)) > 0
&& !ISNULL(season) && !ISNULL(date)
&& !ISNULL(home_club_id) && home_club_id > 0
&& !ISNULL(away_club_id) && away_club_id > 0
&& home_club_id != away_club_id
&& (ISNULL(home_club_goals) || home_club_goals >= 0)
&& (ISNULL(away_club_goals) || away_club_goals >= 0)
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 5: Sắp xếp và xử lý dòng lặp (`Sort` + `Script Component`)

1. Nối nhánh `Valid_Game` vào **Sort** (`Sort Input`).
2. Trong **Sort Editor**: chọn `game_id` làm cột sắp xếp tăng dần (`Ascending`). Để loại dòng lặp hoàn toàn, đưa toàn bộ cột dùng để nạp vào tập khóa sắp xếp, giữ các cột cần thiết ở đầu ra và bật **Remove rows with duplicate sort values**. Kiểm tra tùy chọn so sánh chuỗi của `Sort` để tránh gộp nhầm mã chỉ khác chữ hoa/thường.
3. Sau `Sort`, dùng **Script Component** kiểu **Transformation** với hai đầu ra không đồng bộ: gom các dòng liên tiếp theo khóa `game_id`, chuyển nhóm một dòng tới bước Lookup và nhóm nhiều dòng tới nhánh rà soát; xử lý nhóm cuối khi luồng kết thúc.

### Bước 6: Tra cứu giải đấu và hai đội bằng 3 khối `Lookup`

Kéo 3 khối **Lookup** nối tiếp nhau từ đầu ra hợp lệ của `Script Component`:

- **Cấu hình chung (tab General & Connection)**:
  - **Cache mode**: `Full cache`
  - **Connection type**: `OLE DB connection manager` (`CM_DW_Football`)
  - **Specify how to handle rows with no matching entries**: `Redirect rows to no match output`
- **Khóa nối từng Lookup (tab Columns)**:

| Tên khối Lookup | Bảng tra cứu | Khóa nối (`Input` $\rightarrow$ `Lookup`) |
| :--- | :--- | :--- |
| `Lookup Game Competition` | `dbo.DIM_Competition` | `competition_id` $\rightarrow$ `Competition_ID` |
| `Lookup Home Club` | `dbo.DIM_Club` | `home_club_id` $\rightarrow$ `Club_ID` |
| `Lookup Away Club` | `dbo.DIM_Club` | `away_club_id` $\rightarrow$ `Club_ID` |

- Nối **Lookup Match Output** của khối trước sang khối tiếp theo; nối **Lookup No Match Output** của từng phép tra sang nhánh ghi lỗi (lưu `game_id`, mã đang tra và tên phép tra cứu). Chỉ đưa các dòng ở `Match Output` của `Lookup Away Club` sang `OLE DB Destination`.

### Bước 7: Kết nối `OLE DB Destination` và ánh xạ (`[dbo].[DIM_Game]`)

- Kéo **OLE DB Destination**, nối từ `Match Output` của `Lookup Away Club`.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[DIM_Game]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Mappings (12 cột)**:
  - `game_id` $\rightarrow$ `Game_ID` (`INT`)
  - `competition_id` $\rightarrow$ `Competition_ID` (`NVARCHAR(100)`)
  - `season` $\rightarrow$ `Season` (`INT`)
  - `round` $\rightarrow$ `Round` (`NVARCHAR(100)`)
  - `date` $\rightarrow$ `Date` (`DATE`)
  - `home_club_id` $\rightarrow$ `Home_Club_ID` (`INT`)
  - `away_club_id` $\rightarrow$ `Away_Club_ID` (`INT`)
  - `home_club_goals` $\rightarrow$ `Home_Club_Goals` (`INT`)
  - `away_club_goals` $\rightarrow$ `Away_Club_Goals` (`INT`)
  - `stadium` $\rightarrow$ `Stadium` (`NVARCHAR(200)`)
  - `home_club_manager_name` $\rightarrow$ `Home_Club_Manager_Name` (`NVARCHAR(200)`)
  - `away_club_manager_name` $\rightarrow$ `Away_Club_Manager_Name` (`NVARCHAR(200)`)
- Giữ `NULL` cho tỷ số bị thiếu và để hai cột `home_club_name`, `away_club_name` ở ngoài ánh xạ (vì chúng được dùng cho nhánh bổ sung `DIM_Club`).
- Mở **Error Output**, chuyển dòng lỗi sang nhánh ghi lỗi rồi bấm **OK**.

---

## 3. ĐỐI SOÁT SAU NẠP

- Tổng số dòng kỳ vọng: **7.280** trận đấu thuộc mùa `2022`, `2023`, với `Competition_ID`, `Home_Club_ID` và `Away_Club_ID` hợp lệ.

```sql
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Game;
```
