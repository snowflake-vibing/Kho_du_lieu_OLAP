# HƯỚNG DẪN CẤU HÌNH DATA FLOW: FACT_PLAYER_MATCH_PERF (LƯỢT RA SÂN)

> **Bảng đích:** `[dbo].[FACT_Player_Match_Perf]`  
> **Tệp dữ liệu nguồn:** `cleaned_appearances.csv` (210.747 dòng, 11 cột)  
> **Cơ sở dữ liệu:** `DW_Football_Transfermarkt` (`CM_DW_Football`)  
> **Thay đổi cốt lõi:** Bỏ khối `Data Conversion`, khai báo kiểu ở `FF_Appearances → Advanced`, kiểm tra trùng khóa `appearance_id` trước Lookup, chuyển tất cả `Lookup` sang `Redirect rows to no match output`, bổ sung `Lookup Time` và nhánh đối chiếu ngày/mã giải với `DIM_Game`, bỏ `Goal_Contributions` và `Is_Starter`, giữ `Appearance_ID` tự sinh (`IDENTITY`) và nạp mã gốc vào `Source_Appearance_ID`.

---

## 1. SƠ ĐỒ LUỒNG DỮ LIỆU (DATA FLOW ARCHITECTURE)

```text
[1. Flat File Source (FF_Appearances: cleaned_appearances.csv)] ──(Error Output)──► [Ghi lỗi nguồn]
        │
        ▼
[2. Conditional Split (Valid_Appearances / Rejected_Rows)] ────(Rejected_Rows)─────► [Ghi lý do từ chối]
        │ (Valid_Appearances)
        ▼
[3. Sort (appearance_id ASC + toàn bộ cột, loại dòng lặp hoàn toàn)]
        │
        ▼
[4. Script Component (Gom theo appearance_id: nhóm 1 dòng / nhiều dòng)] ──────────► [Nhánh rà soát trùng]
        │ (Nhóm 1 dòng hợp lệ)
        ▼
[5. Lookup Player (DIM_Player)] ──────(No Match Output)────────────────────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[6. Lookup Club (DIM_Club)] ──────────(No Match Output)────────────────────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[7. Lookup Game (DIM_Game)] ──────────(No Match Output)────────────────────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[8. Lookup Competition (DIM_Competition)] ──(No Match Output)──────────────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[9. Lookup Time (DIM_Time)] ──────────(No Match Output)────────────────────────────► [Ghi lỗi Lookup]
        │ (Match Output)
        ▼
[10. Multicast (Đối chiếu ngày & mã giải với DIM_Game)]
   ├──(Nhánh đối chiếu)──► [Conditional Split (Kiểm tra lệch/thiếu)] ──────────────► [Ghi nhận sai lệch]
   └──(Nhánh nạp chính)
        │
        ▼
[11. Derived Column (Tính Opponent_Club_ID & Is_Home_Game, giữ NULL nếu không khớp 2 đội)]
        │
        ▼
[12. Row Count] ──► [OLE DB Destination (dbo.FACT_Player_Match_Perf - Fast Load, Keep nulls, tắt Keep identity)]
```

---

## 2. CHI TIẾT CẤU HÌNH TỪNG BƯỚC

### Bước 1: Tạo `Data Flow Task` và `Flat File Connection Manager` (`FF_Appearances`)

1. Trong Control Flow, kéo **Data Flow Task** vào bên ngoài `Sequence Container: Load Dimensions` (nối bằng `Success` sau khi nạp đủ năm chiều), đổi tên thành **`FACT_Player_Match_Perf`** và mở tab **Data Flow**.
2. Kéo **Flat File Source** vào vùng thiết kế, mở **Flat File Source Editor → Connection Manager → New…** để tạo **`FF_Appearances`**.
3. Trong tab **General**: chọn `cleaned_appearances.csv` trong thư mục `ssis_input` (hoặc cấu hình `Expressions → ConnectionString` dùng tham số `InputFolder`), chọn **Delimited**, Code page **65001 (UTF-8)**, Text qualifier **`"`**, bật **Column names in the first data row**.
4. Trong tab **Columns**: kiểm tra dấu phân cách cột `{Comma}` và dòng `{CR}{LF}`.

### Bước 2: Khai báo kiểu dữ liệu ở tab `Advanced` của `FF_Appearances`

Tên cột đầu ra giữ nguyên theo CSV và được dùng trực tiếp ở các thành phần tiếp theo:

| Cột CSV | Kiểu dữ liệu SSIS | Cột đích hoặc cách sử dụng |
| :--- | :--- | :--- |
| `appearance_id` | `DT_STR (100)` | `Source_Appearance_ID` |
| `game_id`, `player_id`, `player_club_id` | `DT_I4` | Khóa đầu vào cho các Lookup |
| `date` | `DT_DBDATE` | Đối chiếu với ngày từ `DIM_Game` |
| `competition_id` | `DT_WSTR (100)` | Đối chiếu với mã giải từ `DIM_Game` |
| `goals`, `assists`, `minutes_played`, `yellow_cards`, `red_cards` | `DT_I4` | `Goals`, `Assists`, `Minutes_Played`, `Yellow_Cards`, `Red_Cards` |

*(Mã lượt ra sân giữ nguyên dạng chuỗi có dấu gạch dưới, ví dụ `3836749_129991`, dài 12–15 ký tự ASCII. Khi kiểm tra Preview cần phân biệt độ đo `0` có thật và ô thiếu cần giữ `NULL`).*

### Bước 3: Kiểm tra Preview và cấu hình `Flat File Source`

- Chọn **Preview** trong `FF_Appearances`, kiểm tra đúng 11 cột và các ô trống, rồi bấm **OK**.
- Trong **Flat File Source Editor**:
  - Bật **Retain null values from the source as null values in the data flow** và kiểm tra các cột đầu ra ở tab **Columns**. Nếu SSIS yêu cầu đồng bộ metadata, xác nhận và kiểm tra lại ánh xạ.
  - Vào tab **Error Output**, đặt `Error` và `Truncation` thành **Redirect row** cho các cột cần kiểm soát, nối đầu ra lỗi sang đích ghi lỗi của luồng.

### Bước 4: Tách dòng hợp lệ bằng `Conditional Split`

- Nối đầu ra hợp lệ của `Flat File Source` vào **Conditional Split**.
- Thêm dòng **Order 1** với **Output Name**: **`Valid_Appearances`**, nhập biểu thức:

```c
!ISNULL(appearance_id) && LEN(TRIM(appearance_id)) > 0
&& !ISNULL(game_id) && game_id > 0
&& !ISNULL(player_id) && player_id > 0
&& !ISNULL(player_club_id) && player_club_id > 0
&& (ISNULL(minutes_played) || minutes_played >= 0)
&& (ISNULL(goals) || goals >= 0)
&& (ISNULL(assists) || assists >= 0)
&& (ISNULL(yellow_cards) || yellow_cards >= 0)
&& (ISNULL(red_cards) || red_cards >= 0)
```

- Đặt **Default Output Name** là **`Rejected_Rows`** và nối sang đích ghi lý do kiểm tra.

### Bước 5: Sắp xếp và xử lý dòng lặp (`Sort` + `Script Component`)

1. Nối nhánh `Valid_Appearances` vào **Sort** (`Sort Input`).
2. Chọn `appearance_id` làm cột sắp xếp tăng dần (`Ascending`). Dùng toàn bộ các cột đầu vào trong tập khóa sắp xếp và bật **Remove rows with duplicate sort values** để nhận diện và loại dòng lặp hoàn toàn.
3. Nếu hai dòng cùng `appearance_id` nhưng khác nội dung, dùng **Script Component** sau `Sort` để gom các dòng liên tiếp theo `appearance_id`: chuyển nhóm một dòng tới `Lookup Player` và nhóm nhiều dòng tới nhánh rà soát trước khi chọn bản ghi; xử lý nhóm cuối khi luồng kết thúc.

### Bước 6: Chuỗi 5 khối `Lookup` xác nhận khóa ngoại

Tất cả 5 khối `Lookup` dùng chung thiết lập tại tab **General** và **Connection**:
- **Cache mode**: `Full cache`
- **Connection type**: `OLE DB connection manager` (`CM_DW_Football`)
- **Specify how to handle rows with no matching entries**: **`Redirect rows to no match output`**
- Với mọi **Lookup No Match Output**, nối sang nhánh ghi lỗi (lưu `appearance_id`, khóa tra cứu và tên phép tra).

| Thứ tự | Tên khối Lookup | Bảng tra cứu | Khóa nối (`Input` $\rightarrow$ `Lookup`) | Cột đầu ra & Output Alias |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `Lookup Player` | `dbo.DIM_Player` | `player_id` $\rightarrow$ `Player_ID` | `Player_ID` $\rightarrow$ `FK_Player_ID` |
| 2 | `Lookup Club` | `dbo.DIM_Club` | `player_club_id` $\rightarrow$ `Club_ID` | `Club_ID` $\rightarrow$ `FK_Club_ID` |
| 3 | `Lookup Game` | `dbo.DIM_Game` | `game_id` $\rightarrow$ `Game_ID` | `Game_ID` $\rightarrow$ `FK_Game_ID`<br>`Competition_ID` $\rightarrow$ `Game_Competition_ID`<br>`Date` $\rightarrow$ `Game_Date`<br>`Season` $\rightarrow$ `Game_Season`<br>`Home_Club_ID` $\rightarrow$ `Game_Home_Club_ID`<br>`Away_Club_ID` $\rightarrow$ `Game_Away_Club_ID` |
| 4 | `Lookup Competition` | `dbo.DIM_Competition` | `Game_Competition_ID` $\rightarrow$ `Competition_ID` | `Competition_ID` $\rightarrow$ `FK_Competition_ID` |
| 5 | `Lookup Time` | `dbo.DIM_Time` | `Game_Date` $\rightarrow$ `Full_Date` | `Time_ID` $\rightarrow$ `FK_Time_ID` |

*(Nối **Lookup Match Output** của khối trước sang khối tiếp theo đúng theo thứ tự từ 1 đến 5).*

### Bước 7: Đối chiếu ngày và mã giải từ hai nguồn

- Sau `Lookup Time`, đối chiếu `date` và `competition_id` của lượt ra sân với `Game_Date` và `Game_Competition_ID` lấy từ `DIM_Game`.
- Có thể dùng **Multicast** để giữ một nhánh nạp chính và một nhánh **Conditional Split** ghi lại các trường hợp thiếu hoặc khác nhau giữa hai nguồn.
- Trong nhánh nạp chính, ngày (`FK_Time_ID`) và mã giải (`FK_Competition_ID`) dùng cho khóa fact lấy từ phép tra theo trận.

### Bước 8: Tính mã đối thủ và vai trò sân nhà bằng `Derived Column`

Nối nhánh nạp chính tới **Derived Column**, thêm 2 cột ở chế độ **`<add as new column>`**:

| Cột mới | Expression |
| :--- | :--- |
| `Opponent_Club_ID` | `FK_Club_ID == Game_Home_Club_ID ? Game_Away_Club_ID : (FK_Club_ID == Game_Away_Club_ID ? Game_Home_Club_ID : NULL(DT_I4))` |
| `Is_Home_Game` | `FK_Club_ID == Game_Home_Club_ID ? 1 : (FK_Club_ID == Game_Away_Club_ID ? 0 : NULL(DT_I4))` |

*(Nếu CLB cầu thủ khác cả đội nhà và đội khách, giữ `NULL` ở cả hai trường và ghi nhận bằng nhánh đối soát. Không tính `Goal_Contributions` và `Is_Starter`).*

### Bước 9: Kết nối `OLE DB Destination` và ánh xạ (`[dbo].[FACT_Player_Match_Perf]`)

- Kéo **OLE DB Destination**, nối từ `Derived Column`.
- **Connection Manager**: `CM_DW_Football`.
- **Data access mode**: `Table or view - fast load`, chọn bảng **`[dbo].[FACT_Player_Match_Perf]`**.
- Bật **Keep nulls** và **Check constraints**.
- **Để trống ánh xạ `Appearance_ID` và giữ `Keep identity` tắt** để SQL Server tự sinh khóa chính.
- **Mappings (13 cột)**:

| Cột đầu ra trong Data Flow | Cột đích SQL Server |
| :--- | :--- |
| *(Không ánh xạ — SQL Server tự sinh `IDENTITY`)* | `Appearance_ID` |
| `appearance_id` | `Source_Appearance_ID` |
| `FK_Player_ID`, `FK_Club_ID` | `Player_ID`, `Club_ID` |
| `FK_Competition_ID`, `FK_Game_ID`, `FK_Time_ID` | `Competition_ID`, `Game_ID`, `Time_ID` |
| `Opponent_Club_ID`, `Is_Home_Game` | `Opponent_Club_ID`, `Is_Home_Game` |
| `minutes_played`, `goals`, `assists` | `Minutes_Played`, `Goals`, `Assists` |
| `yellow_cards`, `red_cards` | `Yellow_Cards`, `Red_Cards` |

- Vào **Error Output**, nối nhánh lỗi đến đích ghi nhận. Khi chạy thử, đặt **Row Count** trước đích và ở các nhánh lỗi để kiểm tra số dòng.

---

## 3. CHẠY LẠI CÙNG MỘT LÔ KHI GIỮ DỮ LIỆU

Khi giữ dữ liệu đã nạp (bỏ qua `Drop All Tables` và `Create All Tables`):

1. Thêm bước `Lookup Source_Appearance_ID` tra cột `appearance_id` vào `dbo.FACT_Player_Match_Perf(Source_Appearance_ID)`.
2. Đưa các mã đã có (`Match Output`) vào nhánh đếm riêng (`Row Count`).
3. Chỉ chèn các mã chưa có (`No Match Output`) vào đích với ràng buộc `UNIQUE` trên `Source_Appearance_ID`.
4. Đối chiếu lại số lượt ra sân và tổng độ đo sau lần chạy thứ hai để bảo đảm không nạp trùng.

---

## 4. ĐỐI SOÁT SỐ DÒNG VÀ ĐỘ ĐO TRONG SQL SERVER

- Mốc số dòng kỳ vọng: **210.747** lượt nếu tất cả các dòng hợp lệ; `Appearance_ID` tự sinh và mỗi `Source_Appearance_ID` chỉ xuất hiện một lần.
- Đối chiếu số đầu vào với số đã nạp, số đã có (khi chạy lại), số lặp đã xử lý, số bị từ chối, khóa tham chiếu và số lượt sân nhà/sân khách bị thiếu.

```sql
-- Kiểm tra trùng Source_Appearance_ID
SELECT Source_Appearance_ID, COUNT_BIG(*) AS So_Dong
FROM dbo.FACT_Player_Match_Perf
GROUP BY Source_Appearance_ID
HAVING COUNT_BIG(*) > 1;

-- Đối chiếu lượt ra sân và tổng độ đo theo giải đấu và mùa giải
SELECT f.Competition_ID, g.Season, COUNT_BIG(*) AS Luot_Ra_San,
       SUM(f.Minutes_Played) AS Phut, SUM(f.Goals) AS Ban,
       SUM(f.Assists) AS Kien_Tao, SUM(f.Yellow_Cards) AS The_Vang,
       SUM(f.Red_Cards) AS The_Do
FROM dbo.FACT_Player_Match_Perf AS f
JOIN dbo.DIM_Game AS g ON g.Game_ID = f.Game_ID
GROUP BY f.Competition_ID, g.Season
ORDER BY f.Competition_ID, g.Season;
```

- **Tổng tham chiếu trên 210.747 lượt ra sân**: **13.562.727** phút, **19.173** bàn, **14.739** kiến tạo, **28.694** thẻ vàng và **827** thẻ đỏ. Nếu có dòng bị từ chối, dùng số liệu từ nhánh lỗi để giải thích chênh lệch.
