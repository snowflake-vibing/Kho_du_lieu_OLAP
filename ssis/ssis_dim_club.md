# HƯỚNG DẪN CẤU HÌNH DATA FLOW: DIM_CLUB (CÂU LẠC BỘ)

> **Bảng đích:** `[dbo].[DIM_Club]`  
> **Tệp dữ liệu nguồn:** `cleaned_clubs.csv` (247 dòng, 6 cột) và nguồn bổ sung từ `cleaned_games.csv` (25 CLB)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Bỏ khối `Data Conversion`, khai báo kiểu ở `FF_Club → Advanced`, bỏ cột `Coach_Name` (HLV theo trận lấy ở `DIM_Game`), giữ `NULL` cho giá trị thiếu và bổ sung 25 CLB chỉ xuất hiện trong dữ liệu trận để đạt **272 CLB**.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

### 1.1. Luồng chính: Nạp hồ sơ chuẩn từ `cleaned_clubs.csv` (247 CLB)

```text
[1. Flat File Source (FF_Club: cleaned_clubs.csv)] ──(Error Output: Redirect row)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Conditional Split (Valid_Club / Rejected_Rows)] ──(Rejected_Rows)───────────────► [Ghi lý do từ chối]
        │ (Valid_Club)
        ▼
[3. Sort (club_id ASC + toàn bộ cột nạp, Remove rows with duplicate sort values)]
        │
        ▼
[4. Script Component (Tách nhóm 1 dòng / nhóm nhiều dòng trùng khóa khác nội dung)] ──► [Nhánh rà soát trùng]
        │ (Nhóm 1 dòng hợp lệ)
        ▼
[5. OLE DB Destination (dbo.DIM_Club - Fast Load, Keep nulls, Check constraints)] ──► [Ghi lỗi đích]
```

### 1.2. Luồng bổ sung: Bổ sung 25 CLB từ `cleaned_games.csv` (tổng 272 CLB)

*(Có thể đặt trong một Data Flow Task bổ sung chạy `Success` sau `DIM_Club` và nối `Success` tới `DIM_Game` cùng với `DIM_Competition`).*

```text
[1. Flat File Source (FF_Game: cleaned_games.csv)]
        │
        ▼
[2. Multicast]
   ├──► [Nhánh Đội nhà: home_club_id, home_club_name, date, game_id]
   └──► [Nhánh Đội khách: away_club_id, away_club_name, date, game_id]
        │
        ▼
[3. Union All (Đổi tên đầu ra: Club_ID, Club_Name, Match_Date, Game_ID)]
        │
        ▼
[4. Derived Column (Tạo cờ ưu tiên dòng có tên CLB)]
        │
        ▼
[5. Sort (Club_ID ASC, cờ có tên DESC, Match_Date DESC, Game_ID DESC)]
        │
        ▼
[6. Script Component (Đầu ra đồng bộ loại trừ: giữ dòng đầu mỗi Club_ID)]
        │
        ▼
[7. Lookup (Tra Club_ID vào dbo.DIM_Club)] ──(Match Output: đã có)──► [Bỏ qua]
        │ (Lookup No Match Output)
        ▼
[8. Derived Column (Stadium_Name, Stadium_Seats, Squad_Size = NULL)]
        │
        ▼
[9. OLE DB Destination (dbo.DIM_Club - Fast Load, Keep nulls, Check constraints)]
```

---

## 2. CHI TIẾT CẤU HÌNH LUỒNG CHÍNH (`cleaned_clubs.csv`)

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Club`)

1. Trong Control Flow, kéo **Data Flow Task** vào `Sequence Container: Load Dimensions`, đổi tên thành **`DIM_Club`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Club`**.
3. Trong tab **General**: chọn `cleaned_clubs.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Club`

Tên cột đầu ra giữ nguyên theo CSV và được dùng trực tiếp ở các thành phần tiếp theo:

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `club_id` | `DT_I4` | `Club_ID` |
| `name` | `DT_WSTR (200)` | `Club_Name` |
| `stadium_name` | `DT_WSTR (200)` | `Stadium_Name` |
| `stadium_seats` | `DT_I4` | `Stadium_Seats` |
| `coach_name` | `DT_WSTR (200)` | Trường nguồn, bỏ chọn ở tab `Columns` nếu không dùng (HLV theo trận lấy từ `DIM_Game`) |
| `squad_size` | `DT_I4` | `Squad_Size` |

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Club` để kiểm tra đủ số cột, chữ có dấu UTF-8 và các ô trống, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow**.
  - Vào tab **Columns**, kiểm tra danh sách cột đầu ra (có thể bỏ chọn `coach_name`). Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và rà lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Conditional Split**.
- Thêm nhánh **Order 1** với **Output Name**: **`Valid_Club`**, nhập biểu thức:

```c
!ISNULL(club_id) && club_id > 0
&& (ISNULL(stadium_seats) || stadium_seats >= 0)
&& (ISNULL(squad_size) || squad_size >= 0)
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 5: Sắp xếp và xử lý dòng lặp (`Sort` + `Script Component`)

1. Nối nhánh `Valid_Club` vào **Sort** (`Sort Input`).
2. Trong **Sort Editor**: chọn `club_id` làm cột sắp xếp tăng dần (`Ascending`). Để loại dòng lặp hoàn toàn, đưa toàn bộ cột dùng để nạp vào tập khóa sắp xếp, giữ các cột cần thiết ở đầu ra và bật **Remove rows with duplicate sort values**. Kiểm tra tùy chọn so sánh chuỗi của `Sort` để tránh gộp nhầm mã chỉ khác chữ hoa/thường.
3. Sau `Sort`, kéo **Script Component** kiểu **Transformation** với hai đầu ra không đồng bộ: gom các dòng liên tiếp theo khóa `club_id`, chuyển nhóm một dòng tới đích và nhóm nhiều dòng tới nhánh rà soát; xử lý nhóm cuối khi luồng kết thúc.

### Bước 6: Cấu hình `OLE DB Destination` (`[dbo].[DIM_Club]`)

- Kéo **OLE DB Destination**, nối từ đầu ra hợp lệ của `Script Component`.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[DIM_Club]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Mappings (5 cột)**:
  - `club_id` $\rightarrow$ `Club_ID`
  - `name` $\rightarrow$ `Club_Name`
  - `stadium_name` $\rightarrow$ `Stadium_Name`
  - `stadium_seats` $\rightarrow$ `Stadium_Seats`
  - `squad_size` $\rightarrow$ `Squad_Size`
- Mở **Error Output**, chuyển dòng lỗi sang nhánh ghi lỗi rồi bấm **OK**.

---

## 3. CHI TIẾT LUỒNG BỔ SUNG CLB TỪ `cleaned_games.csv`

Để không làm mất các lượt ra sân của những CLB có mặt trong dữ liệu trận nhưng thiếu trong `cleaned_clubs.csv` (notebook phát hiện **25 mã bổ sung** liên quan đến **76 lượt ra sân**), thực hiện thêm các bước sau:

1. **Tạo hai nhánh từ `FF_Game`**:
   - Thêm **Flat File Source** dùng `FF_Game` (cấu hình theo [ssis_dim_game.md](ssis_dim_game.md)).
   - Nối vào **Multicast** và chia thành 2 nhánh: lấy `home_club_id`, `home_club_name`, `date`, `game_id` ở nhánh 1 và `away_club_id`, `away_club_name`, `date`, `game_id` ở nhánh 2.
2. **Gộp và chuẩn hóa cột bằng `Union All`**:
   - Ghép hai nhánh vào **Union All**, đổi tên ngay trong cột đầu ra thành `Club_ID`, `Club_Name`, `Match_Date`, `Game_ID`.
3. **Chọn một hồ sơ đại diện cho mỗi `Club_ID`**:
   - Thêm **Derived Column** tạo cờ ưu tiên cho dòng có tên CLB (có dữ liệu, không `NULL`/rỗng).
   - Dùng **Sort** sắp xếp theo: `Club_ID` tăng dần (`ASC`), cờ có tên giảm dần (`DESC`), `Match_Date` giảm dần (`DESC`), rồi `Game_ID` giảm dần (`DESC`).
   - Dùng **Script Component** kiểu **Transformation** với đầu ra đồng bộ kiểu loại trừ trên luồng đã sắp xếp: chọn `Club_ID` làm cột chỉ đọc, khai báo biến lưu mã vừa gặp trong component; trong `Input0_ProcessInputRow`, chỉ gọi `DirectRowTo...` cho dòng đầu của mỗi `Club_ID` (giữ mã kể cả khi dữ liệu trận thiếu tên).
4. **Chỉ giữ các `Club_ID` chưa có trong `DIM_Club`**:
   - Nạp hồ sơ chuẩn từ `cleaned_clubs.csv` trước, sau đó dùng **Lookup** tra `Club_ID` bổ sung vào `dbo.DIM_Club` và chỉ giữ **`Lookup No Match Output`**.
   - *(Khuyến nghị Control Flow)*: có thể tách thành một Data Flow Task bổ sung chạy `Success` sau `DIM_Club` và nối tác vụ này tới `DIM_Game` để việc tra cứu mã đội ở `DIM_Game` chỉ bắt đầu khi `DIM_Club` đã đầy đủ.
5. **Ánh xạ các cột thiếu bằng `NULL`**:
   - Trong nhánh bổ sung, thêm **Derived Column** tạo 3 cột với giá trị `NULL` giữ nguyên kiểu:
     - `Stadium_Name`: `NULL(DT_WSTR,200)`
     - `Stadium_Seats`: `NULL(DT_I4)`
     - `Squad_Size`: `NULL(DT_I4)`
   - Nối vào **OLE DB Destination** (`CM_DW_Football`, `Table or view - fast load`, `[dbo].[DIM_Club]`, bật `Keep nulls` và `Check constraints`), ánh xạ 5 cột (`Club_ID`, `Club_Name`, `Stadium_Name`, `Stadium_Seats`, `Squad_Size`).

---

## 4. ĐỐI SOÁT SAU NẠP

- Tổng số dòng kỳ vọng: **272** hồ sơ (**247** CLB từ `cleaned_clubs.csv` + **25** mã CLB bổ sung từ `cleaned_games.csv`).
- Các dòng bổ sung phải giữ `NULL` ở `Stadium_Name`, `Stadium_Seats` và `Squad_Size`.

```sql
SELECT COUNT_BIG(*) AS So_Dong FROM dbo.DIM_Club;
```
