# KẾ HOẠCH CHỈNH SỬA SSAS & MDX TRONG VISUAL STUDIO / SSMS (TỪ BẢN CŨ SANG BẢN MỚI)

> **Tài liệu đối chiếu:**
> - **Bản cũ (`Bài tập (1).docx` — Chương 3 cũ):** Xây dựng **5 Database Dimensions** từ các bảng gốc (vẫn dùng cột tĩnh `DIM_Club.Coach_Name`, `DIM_Player.Age`, `DIM_Time.Season`), **1 Measure Group** duy nhất (`FACT_Player_Match_Perf`), truy vấn theo `[DIM Player].[Player Name]` (dễ gộp nhầm cầu thủ trùng tên), còn sót tên DB mẫu `TMDB_Movie_DataWareHouse` ở Mục 3.2 và lỗi copy-paste mô tả ở Mục 3.4.2–3.4.4, chỉ có **10 câu truy vấn** với một số câu lệch yêu cầu Chương 1 mới.
> - **Bản mới (`Chuong_3_SSAS.docx`):** Chuẩn hóa theo Chương 1 mới (`Bao_cao_OLAP.docx`) và lược đồ `DW_Football_Transfermarkt` (Chương 2 mới) với **6 Dimensions** (thêm Fact Dimension `DIM_Appearance_Context`), **4 Measure Groups** (**13 Base Measures**), **9 Cube Dimensions** (4 vai trò Role-Playing cho `DIM_Club`), **13 Calculated Measures**, **6 Named Calculations** trong DSV, **Named Query** `FACT_Player_Match_Perf` & `FACT_Club_Match_Official`, cùng đầy đủ **15 câu truy vấn** chuẩn hóa trên **3 công cụ** (Cube Browser, Excel PivotTable, MDX).
> - **Bộ tài liệu triển khai chi tiết liên quan:** [ssas_overview.md](ssas_overview.md) · [ssas_dsv_dims.md](ssas_dsv_dims.md) · [ssas_cube_measures.md](ssas_cube_measures.md) · [ssas_hierarchies_relations.md](ssas_hierarchies_relations.md) · [ssas_deploy_mdx.md](ssas_deploy_mdx.md) · [../mdx/README.md](../mdx/README.md) · [../mdx/checklist.md](../mdx/checklist.md).

---

## 1. TỔNG QUAN THAY ĐỔI (BẢN CŨ `Bài tập (1).docx` $\rightarrow$ BẢN MỚI `Chuong_3_SSAS`)

| Hạng mục | Bản cũ (`Bài tập (1).docx`) | Bản mới (`Chuong_3_SSAS`) | Hành động chỉnh sửa trên Visual Studio / GitHub |
| :--- | :--- | :--- | :--- |
| **1. Data Source (`.ds`)** | Trỏ `DESKTOP-9B88R8P.DW_Football_Transfermarkt`, văn bản còn sót `TMDB_Movie_DataWareHouse` | **`DW_Football_Transfermarkt.ds`** trỏ `localhost` / `DW_Football_Transfermarkt`, Impersonation `Use the service account` | Rà soát chuỗi kết nối trên `DW_Football_Transfermarkt.ds`, loại bỏ hoàn toàn dấu vết tên mẫu cũ |
| **2. Data Source View (`.dsv`)** | 6 bảng vật lý, tự nối tay `Opponent_Club_ID → Club_ID` trên DSV | 6 bảng vật lý + **6 Named Calculations** (`Time_ID`, `Total_Match_Goals`, `Season_Label`, `Is_Youth_2004`, `Year_Quarter_Key`, `Year_Month_Key`) + Logical FK `DIM_Game.Time_ID → DIM_Time.Time_ID` + **Replace `FACT_Player_Match_Perf` thành Named Query** (`Player_Age_At_Match`, `Club_Manager_Name`) + **Named Query mới `FACT_Club_Match_Official`** (`14.560` dòng) | Refresh DSV theo lược đồ mới, tạo 6 Named Calculations, tạo 2 Named Queries và thiết lập đủ khóa chính/khóa ngoại logic |
| **3. Database Dimensions (`.dim`)** | **5 Dimensions**, dùng tất cả cột cũ (`Coach_Name`, `Age`, `DIM_Time.Season`), dùng `Player Name` làm thuộc tính truy vấn | **6 Dimensions** (bổ sung Fact Dimension **`DIM_Appearance_Context`**), xóa 3 cột đã loại bỏ, thêm `Is Youth 2004`, `Year Quarter Key`, `Year Month Key`; đặt `DIM_Player.Player ID` có `NameColumn = Player_Name` (giữ định danh duy nhất cho 51 tên trùng trên 108 hồ sơ) | Sửa 5 `.dim` hiện có và tạo mới `DIM_Appearance_Context.dim` |
| **4. Phân cấp & Khóa ghép** | `Year → Quarter → Month → Day` dùng `KeyColumns` nhiều cột (`Year`, `Quarter, Year`…); `Round → Game ID` không tách mùa; lỗi copy-paste mô tả ở `3.4.2–3.4.4` | **5 User-Defined Hierarchies** chuẩn hóa: `Calendar Hierarchy` (dùng DSV Named Calculations `Year_Quarter_Key`, `Year_Month_Key`), `Position Hierarchy`, `Nationality Hierarchy`, `Season Round Hierarchy` (`Round` dùng khóa ghép `(Season, Round)` tách 55 tên vòng lặp), `Competition Hierarchy` | Cấu hình lại `Hierarchies`, `KeyColumns`/`NameColumn` và `Attribute Relationships` (`Rigid`/`Flexible`) xóa cảnh báo tam giác vàng |
| **5. Xử lý NULL & Unknown** | Chưa thiết lập `NullProcessing`; lọc cứng `[0]`, `"Unknown"` trong từng câu MDX | Bảng quy ước chuẩn **`NullProcessing = UnknownMember`** (`Unknown`) trên các chiều/cột nullable (`DIM_Club`, `DIM_Competition`, `DIM_Player`, `DIM_Appearance_Context`, `Opponent_Club_ID`) và **`Preserve`** trên các độ đo gốc | Cấu hình `UnknownMember = Visible` và `NullProcessing` trên từng Dimension / Measure Group |
| **6. Cube & Measure Groups** | **1 Measure Group** (`FACT_Player_Match_Perf`), đếm trận bằng `DISTINCTCOUNT(Game ID)` trên bảng lượt ra sân | **4 Measure Groups** & **13 Base Measures**: `FACT Player Match Perf` (210.747 dòng), `FACT Player Distinct` (`Distinct Player Count`), `FACT Club Match Official` (14.560 dòng), `DIM Game` (7.280 dòng) | Bổ sung `FACT_Club_Match_Official` và `DIM_Game` làm Measure Group tables, tách Measure Group `FACT Player Distinct` |
| **7. Dimension Usage & Role-Playing** | 5 Cube Dimensions liên kết Star Schema đơn | **9 Cube Dimensions × 4 Measure Groups**: nhân bản `DIM_Club` thành 4 vai trò (`DIM Club`, `DIM Opponent Club`, `DIM Home Club`, `DIM Away Club`) + `DIM Appearance Context` (Fact Relationship); giữ `IgnoreUnrelatedDimensions = True` | Thiết lập ma trận Dimension Usage và `Null Processing = UnknownMember` tại giao điểm `DIM Opponent Club × FACT Player Match Perf` |
| **8. Calculated Measures** | Khai báo rời rạc trong từng câu (`WITH MEMBER Pct Of England Goals`, `QoQ Goals Growth`, `Stadium Capacity Cleaned`, `Distinct Matches Played`, `ROUND(..., 1)`) | **13 Calculated Measures** tập trung tại tab **Calculations**: `Goal Contributions`, `Avg Minutes Played`, `Goals Per 90`, `Goal Contributions Per 90`, `Avg/Max/Min Height Cm`, `Pct Of Country Goals`, `Stadium Seats Value`, **`Covered Match Count`**, **`Goals Per Match`**, **`Yellow Cards Per Match`**, **`Red Cards Per Match`** | Dọn công thức cũ rời rạc, dán toàn bộ MDX Script chuẩn hóa tự chủ, bảo vệ chia cho 0 bằng `IIF` / `ISEMPTY` |
| **9. Deploy & Đối chiếu kho** | Chỉ kiểm tra Deploy 0 errors/warnings | Deploy + chạy MDX đối soát 2 mùa (`2022/2023`, `2023/2024`) khớp SQL Server Chương 2, giải thích 282 trận giải `UCOL` (`0` lượt ra sân) | Deploy (`Do Full`) và đối soát bảng tổng mùa giải trên SSMS |
| **10. Bộ truy vấn nghiệp vụ** | **10 câu cũ** (`3.7.1–3.7.10`), một số câu dùng `Player Name` / `DIM Time.Season` / toán tử dễ lỗi trên Cube Browser | **15 câu đầy đủ (`query_01`–`query_15`)** đặt trực tiếp trong `mdx/` (bỏ chia sang `archive/`), thêm 5 câu mở rộng (`Q02`, `Q10`, `Q13`, `Q14`, `Q15`), thay thế `Q07/Q08` cũ, đồng bộ T-SQL + Cube Browser + Excel + MDX + bảng kết quả thực tế | Viết lại & bổ sung đủ 15 cặp `.md` / `.mdx` trong `mdx/`, lưu vết nháp cũ vào `mdx/archive/legacy_v1/` |

---

## 2. CHUẨN BỊ TRƯỚC KHI MỞ VISUAL STUDIO

1. **Sao lưu project SSAS cũ:**
   - Tạo bản sao lưu toàn bộ thư mục project `SSAS_Football_Transfermarkt` (các tệp `.dwproj`, `.ds`, `.dsv`, `.dim`, `.cube`) trước khi sửa cấu trúc DSV và Cube để dễ đối chiếu nếu cần khôi phục.
2. **Xác nhận dữ liệu SQL Server `DW_Football_Transfermarkt` từ Chương 2:**
   - Bảo đảm SSIS đã nạp đủ 6 bảng theo `schema_warehouse.sql` (không còn `DIM_Club.Coach_Name`, `DIM_Player.Age`, `DIM_Time.Season`, `FACT_Player_Match_Perf.Goal_Contributions`, `Is_Starter`, `Market_Value_In_EUR`):
     - `DIM_Club`: **272** dòng (247 CLB chính + 25 CLB bổ sung từ `cleaned_games.csv`)
     - `DIM_Player`: **7.069** dòng (`Date_Of_Birth` kiểu `DATE`)
     - `DIM_Competition`: **13** dòng
     - `DIM_Game`: **7.280** dòng (chứa `Season`, `Home/Away_Club_Goals`, `Home/Away_Club_Manager_Name`)
     - `DIM_Time`: **488** dòng (`Time_ID, Full_Date, Year, Quarter, Month, Day, Day_Of_Week, Is_Weekend`)
     - `FACT_Player_Match_Perf`: **210.747** lượt ra sân (`Appearance_ID NVARCHAR(100)` PK)
3. **Dọn sạch sai sót tham chiếu từ bản cũ:**
   - Trong tài liệu báo cáo và tên đối tượng SSAS, thống nhất tên nguồn là **`DW_Football_Transfermarkt`**, Data Source là `DW_Football_Transfermarkt.ds`, DSV là `DW_Football_Transfermarkt.dsv`, loại bỏ hoàn toàn các tên bị sót từ template cũ (`TMDB_Movie_DataWareHouse`).

---

## 3. CHỈNH SỬA DATA SOURCE & DATA SOURCE VIEW (`DW_Football_Transfermarkt.ds` / `.dsv`)

> Tham chiếu chi tiết từng bước: [ssas_overview.md](ssas_overview.md) và [ssas_dsv_dims.md](ssas_dsv_dims.md).

### Bước 1: Chuẩn hóa Data Source (`DW_Football_Transfermarkt.ds`)
- Mở `DW_Football_Transfermarkt.ds`, cập nhật **Connection String** về SQL Server đang chứa kho dữ liệu chuẩn (`Server = localhost` hoặc instance thực hành; `Initial Catalog = DW_Football_Transfermarkt`; `Integrated Security = SSPI` — Windows Authentication), bấm **Test Connection** $\rightarrow$ `Succeeded`.
- Tại tab **Impersonation Information**, giữ **`Use the service account`** (hoặc Windows account có quyền đọc `db_datareader` trên `DW_Football_Transfermarkt`).

### Bước 2: Refresh DSV & Bổ sung 6 Named Calculations
- Mở **`DW_Football_Transfermarkt.dsv`**, bấm biểu tượng **Refresh Data Source View** để xóa metadata các cột cũ đã bị lược bỏ và nhận các cột mới trên `DIM_Game`.
- Bấm phải từng bảng $\rightarrow$ **New Named Calculation...** để bổ sung đủ 6 cột tính toán:
  1. Trên **`DIM_Game`**:
     - `Time_ID` (`INT`): `YEAR([Date]) * 10000 + MONTH([Date]) * 100 + DAY([Date])`
     - `Total_Match_Goals` (`INT`): `ISNULL([Home_Club_Goals], 0) + ISNULL([Away_Club_Goals], 0)`
     - `Season_Label` (`VARCHAR(9)`): `CAST([Season] AS VARCHAR(4)) + '/' + CAST([Season] + 1 AS VARCHAR(4))`
  2. Trên **`DIM_Player`**:
     - `Is_Youth_2004` (`INT`): `CASE WHEN [Date_Of_Birth] >= '2004-01-01' THEN 1 ELSE 0 END`
  3. Trên **`DIM_Time`** *(bắt buộc do `schema_warehouse.sql` chỉ lưu 8 cột gốc `Time_ID..Is_Weekend`)*:
     - `Year_Quarter_Key` (`INT`): `[Year] * 10 + [Quarter]` *(phục vụ phân cấp lịch và Câu 10)*
     - `Year_Month_Key` (`INT`): `[Year] * 100 + [Month]` *(phục vụ phân cấp lịch và Câu 12)*
- Trên sơ đồ DSV, kéo cột **`DIM_Game.Time_ID`** thả sang **`DIM_Time.Time_ID`** để tạo **Logical Relationship** nối cấp trận đấu sang chiều thời gian.

### Bước 3: Chuyển `FACT_Player_Match_Perf` sang Named Query (tính động tuổi & HLV theo trận)
- Do bản mới bỏ cột tĩnh `DIM_Player.Age` và `DIM_Club.Coach_Name`, bấm phải bảng `FACT_Player_Match_Perf` trong DSV $\rightarrow$ **Replace Table $\rightarrow$ With New Named Query...**, dán câu lệnh SQL ở [ssas_dsv_dims.md (Bước 3)](ssas_dsv_dims.md) nối `FACT_Player_Match_Perf` với `DIM_Player` và `DIM_Game` để sinh động `Player_Age_At_Match` và `Club_Manager_Name` trên đúng **210.747 lượt ra sân**.
- Bấm phải cột `Appearance_ID` chọn **Set Logical Primary Key**, giữ nguyên 6 khóa ngoại ra 5 bảng chiều (`Club_ID`, `Opponent_Club_ID`, `Player_ID`, `Competition_ID`, `Game_ID`, `Time_ID`).

### Bước 4: Tạo mới Named Query `FACT_Club_Match_Official` (phục vụ Câu 10)
- Bấm phải vùng trống trong DSV $\rightarrow$ **New Named Query...**, đặt tên **`FACT_Club_Match_Official`**, viết `UNION ALL` giữa đội chủ nhà (`'_H'`) và đội khách (`'_A'`) từ `dbo.DIM_Game` (`14.560` dòng = `7.280` trận $\times$ 2 đội), đặt Logical Primary Key là **`Club_Match_Key`**.
- Tạo Logical Relationships từ `FACT_Club_Match_Official` tới `DIM_Club` (`Club_ID`, `Opponent_Club_ID`), `DIM_Competition` (`Competition_ID`), `DIM_Game` (`Game_ID`) và `DIM_Time` (`Time_ID`).

---

## 4. CHỈNH SỬA 5 DIMENSIONS CŨ & TẠO DIMENSION THỨ 6 (`DIM_Appearance_Context`)

> Tham chiếu chi tiết thuộc tính: [ssas_dsv_dims.md (Mục 3)](ssas_dsv_dims.md).

1. **`DIM_Club.dim`**:
   - Xóa thuộc tính `Coach Name` (không còn tồn tại trên `DIM_Club`).
   - Kiểm tra thuộc tính khóa **`Club ID`**: `KeyColumns = Club_ID`, `NameColumn = Club_Name`; giữ đủ `Club Name`, `Stadium Name`, `Stadium Seats`, `Squad Size`.
   - Cấu hình `UnknownMember = Visible`, `UnknownMemberName = Unknown`.
2. **`DIM_Competition.dim`**:
   - Giữ 4 thuộc tính (`Competition ID`, `Competition Name`, `Country Name`, `Competition Type`).
   - Đặt `KeyColumns NullProcessing = UnknownMember` cho `Country Name` để giữ đủ 3 giải cúp châu Âu (`CL`, `EL`, `UCOL`) có giá trị `NULL` ở quốc gia.
3. **`DIM_Game.dim`**:
   - Kéo bổ sung toàn bộ các thuộc tính mới từ DSV: `Competition ID`, `Season` (`KeyColumns = Season`, `NameColumn = Season_Label`), `Date`, `Home Club ID`, `Away Club ID`, `Home Club Goals`, `Away Club Goals`, `Total Match Goals`, `Home Club Manager Name`, `Away Club Manager Name` (giữ `Game ID`, `Round`, `Stadium`).
4. **`DIM_Player.dim`**:
   - Xóa thuộc tính `Age`.
   - Kéo thêm thuộc tính **`Is Youth 2004`** (từ Named Calculation).
   - **Sửa bắt buộc thuộc tính khóa `Player ID`**: đặt `KeyColumns = Player_ID` và **`NameColumn = Player_Name`** (hiển thị tên dễ đọc nhưng khóa theo mã duy nhất, khắc phục việc 51 tên trùng trên 108 hồ sơ bị gộp nhầm khi truy vấn bằng `Player Name` ở bản cũ).
   - Giữ đủ `Player Name`, `Date Of Birth`, `Country Of Citizenship`, `Main Position`, `Sub Position`, `Foot`, `Height In Cm`.
5. **`DIM_Time.dim`**:
   - Xóa thuộc tính `Season` (đã chuyển đúng về `DIM_Game.Season`).
   - Kéo bổ sung **`Year Quarter Key`** và **`Year Month Key`** (từ 2 Named Calculations trên `DIM_Time`).
6. **Tạo mới `DIM_Appearance_Context.dim` (Fact Dimension thứ 6)**:
   - Bấm phải **Dimensions $\rightarrow$ New Dimension...**, chọn main table là Named Query `FACT_Player_Match_Perf`, khóa chính `Appearance_ID`.
   - Đưa vào 4 thuộc tính: `Appearance ID` (đặt `AttributeHierarchyVisible = False` tránh phình cây metadata `210.747` mã), `Is Home Game`, `Player Age At Match`, `Club Manager Name`.

---

## 5. CHỈNH SỬA PHÂN CẤP (HIERARCHIES), KHÓA GHÉP & XỬ LÝ NULL

> Tham chiếu sơ đồ đầy đủ: [ssas_hierarchies_relations.md](ssas_hierarchies_relations.md).

### 5.1. Chuẩn hóa 5 User-Defined Hierarchies & Khóa ghép
1. **`DIM_Time.dim` — `Calendar Hierarchy`** (`Year` $\rightarrow$ `Quarter` $\rightarrow$ `Month` $\rightarrow$ `Day`):
   - Thay khóa ghép nhiều cột kiểu cũ ở `Bài tập (1).docx` bằng khóa kỳ tính trong DSV:
     - `Quarter`: `KeyColumns = Year_Quarter_Key (Integer)`, `NameColumn = Quarter (WChar)`, `OrderBy = Key`.
     - `Month`: `KeyColumns = Year_Month_Key (Integer)`, `NameColumn = Month (WChar)`, `OrderBy = Key`.
     - `Day`: `KeyColumns = Time_ID (Integer)`, `NameColumn = Day (WChar)`, `OrderBy = Key`.
   - Cấu hình **Attribute Relationships** (`Rigid`): `Time ID` $\rightarrow$ `Day` $\rightarrow$ `Month` $\rightarrow$ `Quarter` $\rightarrow$ `Year`; `Time ID` $\rightarrow$ `Full Date`; `Time ID` $\rightarrow$ `Day Of Week` $\rightarrow$ `Is Weekend`.
2. **`DIM_Player.dim` — `Position Hierarchy` & `Nationality Hierarchy`**:
   - Tạo **`Position Hierarchy`**: `Main Position` $\rightarrow$ `Sub Position` $\rightarrow$ `Player ID` (thay `Player Name`).
   - Tạo **`Nationality Hierarchy`**: `Country Of Citizenship` $\rightarrow$ `Main Position` $\rightarrow$ `Player ID`.
   - Attribute Relationships (`Flexible`): `Player ID` $\rightarrow$ `Sub Position` $\rightarrow$ `Main Position`, `Player ID` $\rightarrow$ `Country Of Citizenship`.
3. **`DIM_Game.dim` — `Season Round Hierarchy`** (`Season` $\rightarrow$ `Round` $\rightarrow$ `Game ID`):
   - Bản cũ chỉ có `Round → Game ID` nên gộp nhầm **55 tên vòng đấu** (`1. Matchday`, `Final`, `last 16 1st leg`…) trùng giữa hai mùa 2022 và 2023.
   - Bắt buộc thêm cấp `Season` lên trên `Round`, đặt thuộc tính `Round` với **`KeyColumns = (Season, Round)`**, **`NameColumn = Round`**, `OrderBy = Key`.
   - Attribute Relationships: `Game ID` $\rightarrow$ `Round` $\rightarrow$ `Season`; `Game ID` $\rightarrow$ `Competition ID`, `Stadium`, `Date`.
4. **`DIM_Competition.dim` — `Competition Hierarchy`**:
   - Khắc phục lỗi copy-paste của bản cũ (`3.4.4`): tạo đúng phân cấp **`Competition Type` $\rightarrow$ `Country Name` $\rightarrow$ `Competition Name` $\rightarrow$ `Competition ID`**.

### 5.2. Thiết lập `NullProcessing` và `UnknownMember`
- Trên các chiều có giá trị thiếu (`DIM_Club`: 25 CLB bổ sung thiếu sân/sức chứa/quy mô; `DIM_Competition`: 3 giải quốc tế thiếu quốc gia; `DIM_Player`: `2/124/2/107/121` hồ sơ thiếu ngày sinh/chân thuận/vị trí phụ/quốc tịch/chiều cao; `DIM_Appearance_Context`: `33` lượt thiếu tuổi, `58` lượt thiếu tên HLV): đặt **`KeyColumns NullProcessing = UnknownMember`**, hiển thị thành viên `Unknown` để tách lọc an toàn trong MDX (`EXCEPT(..., { ...[Unknown] })`) thay vì ép về `0` như bản cũ.
- Trên tất cả Base Measures kiểu `Sum`: đặt `NullProcessing = Preserve` để phân biệt thiếu dữ liệu với số `0`.

---

## 6. TÁI CẤU TRÚC CUBE, 4 MEASURE GROUPS, ROLE-PLAYING & CALCULATED MEASURES

> Tham chiếu chi tiết: [ssas_cube_measures.md](ssas_cube_measures.md) và [ssas_hierarchies_relations.md](ssas_hierarchies_relations.md).

### 6.1. Nâng cấp từ 1 lên 4 Measure Groups (13 Base Measures)
1. **Measure Group 1 — `FACT Player Match Perf`** (`210.747` dòng): giữ 5 độ đo cộng dồn (`Minutes Played`, `Goals`, `Assists`, `Yellow Cards`, `Red Cards`), đổi tên độ đo đếm dòng từ `FACT Player Match Perf Count` sang **`Appearance Count`** (`Count of rows`), bỏ `Goal Contributions` vật lý (chuyển sang Calculated Measure).
2. **Measure Group 2 — `FACT Player Distinct`**: trong tab **Cube Structure**, chọn **New Measure...**, `Usage = Distinct count`, `Source table = FACT_Player_Match_Perf`, `Source column = Player_ID`, đặt tên **`Distinct Player Count`** (phục vụ Câu 13).
3. **Measure Group 3 — `FACT Club Match Official`** (`14.560` dòng): thêm bảng Named Query `FACT_Club_Match_Official` làm Measure Group mới, giữ `Official Team Goals` (`Sum`) và `Official Team Match Count` (`Count`) (phục vụ Câu 10).
4. **Measure Group 4 — `DIM Game`** (`7.280` dòng): thêm `DIM_Game` làm Measure Group mới, giữ `Official Match Count` (`Count`), `Home Club Goals` (`Sum`), `Away Club Goals` (`Sum`), `Total Match Goals` (`Sum`) (phục vụ Câu 11, Câu 14 và đối soát toàn kho).

### 6.2. Cấu hình tab Dimension Usage (9 Cube Dimensions × 4 Measure Groups)
- Từ Database Dimension `DIM_Club`, bấm **Add Cube Dimension** để có đủ **4 Role-Playing Dimensions**: `DIM Club` (`Club_ID`), `DIM Opponent Club` (`Opponent_Club_ID`), `DIM Home Club` (`Home_Club_ID`), `DIM Away Club` (`Away_Club_ID`).
- Thêm **`DIM Appearance Context`** liên kết **Fact Relationship** (`Appearance_ID`) với `FACT Player Match Perf` và `FACT Player Distinct`.
- Kiểm tra đủ ma trận 9 Cube Dimensions × 4 Measure Groups theo [Bảng Dimension Usage](ssas_hierarchies_relations.md), giữ `IgnoreUnrelatedDimensions = True` và đặt `Null Processing = UnknownMember` tại ô `DIM Opponent Club × FACT Player Match Perf`.

### 6.3. Chuẩn hóa 13 Calculated Measures trong tab `Calculations`
- Xóa các biểu thức cũ viết rời rạc trong từng bài tập (`Pct Of England Goals`, `QoQ Goals Growth`, `Stadium Capacity Cleaned`, `Distinct Matches Played`).
- Nhập đầy đủ bộ **13 Calculated Measures** từ [ssas_cube_measures.md (Mục 4)](ssas_cube_measures.md):
  - `Goal Contributions` (Câu 3), `Avg Minutes Played` (Câu 4), `Goals Per 90` & `Goal Contributions Per 90` (Câu 8 mới);
  - `Avg Height Cm`, `Max Height Cm`, `Min Height Cm` dùng `EXISTING CrossJoin([DIM Player].[Player ID], ...)` + bỏ `ROUND(..., 1)` cũ để giữ độ chính xác 2 chữ số thập phân (Câu 6);
  - `Pct Of Country Goals` (Câu 7), `Stadium Seats Value` dùng `DIM Home Club` (Câu 11);
  - Bộ 4 độ đo theo trận cho Câu 09 & Câu 12: **`Covered Match Count`** (`COUNT(NONEMPTY(EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS, [Measures].[Appearance Count]))`), **`Goals Per Match`**, **`Yellow Cards Per Match`**, **`Red Cards Per Match`**.

---

## 7. DEPLOY, PROCESS & ĐỐI CHIẾU TỔNG THỂ CUBE

> Tham chiếu: [ssas_deploy_mdx.md](ssas_deploy_mdx.md).

1. Trong Visual Studio 2022, mở **Project Properties $\rightarrow$ Deployment**: đặt `Server = localhost`, `Database = SSAS_Football_Transfermarkt`, `Processing Option = Do Full`.
2. Nhấn **F5** (**Build $\rightarrow$ Deploy Solution**), xác nhận **`Deployment Completed Successfully`** (`0 errors, 0 warnings`).
3. Mở **SSMS $\rightarrow$ Analysis Services $\rightarrow$ `SSAS_Football_Transfermarkt` $\rightarrow$ New Query $\rightarrow$ MDX**, chạy truy vấn đối soát theo `[DIM Game].[Season]` và kiểm chứng khớp 100% số liệu tổng kho:

| Mùa giải | Số trận (`Official Match Count`) | Lượt ra sân (`Appearance Count`) | Cầu thủ (`Distinct Player Count`) | Số phút (`Minutes Played`) | Bàn thắng (`Goals`) | Kiến tạo (`Assists`) | Thẻ vàng (`Yellow Cards`) | Thẻ đỏ (`Red Cards`) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2022/2023` (`2022`) | 3.691 | 106.281 | 5.296 | 6.848.543 | 9.563 | 7.340 | 14.478 | 455 |
| `2023/2024` (`2023`) | 3.589 | 104.466 | 5.239 | 6.714.184 | 9.610 | 7.399 | 14.216 | 372 |
| **Tổng toàn kho** | **7.280** | **210.747** | **7.069** | **13.562.727** | **19.173** | **14.739** | **28.694** | **827** |

> **Lưu ý kiểm định:** Giải `UCOL` có **282 trận** trong `DIM_Game` (141 trận mùa 2022/2023 và 141 trận mùa 2023/2024) nhưng `0` lượt ra sân trong `FACT_Player_Match_Perf`. Nhờ tách Measure Group `DIM Game` và `FACT Player Match Perf`, thống kê cấp trận giữ đủ `7.280` trận trong khi cấp cầu thủ phản ánh đúng `210.747` lượt.

---

## 8. KẾ HOẠCH CHỈNH SỬA & CHUYỂN ĐỔI BỘ TRUY VẤN (10 CÂU CŨ $\rightarrow$ 15 CÂU MỚI)

### 8.1. Bảng ánh xạ từ 10 câu cũ (`Bài tập (1).docx`) sang 15 câu mới (`mdx/query_01`–`query_15`)

| Câu mới (`mdx/`) | Nguồn từ `Bài tập (1).docx` | Phân loại thay đổi | Measure Group chính |
| :--- | :--- | :--- | :--- |
| **[query_01](../mdx/query_01.md)** | `3.7.1` (Câu 1 cũ) | **Nâng cấp / Sửa lỗi** | `FACT Player Match Perf` |
| **[query_02](../mdx/query_02.md)** | *(chưa có trong bản cũ)* | **Bổ sung mới** | `FACT Player Match Perf` |
| **[query_03](../mdx/query_03.md)** | `3.7.2` (Câu 2 cũ) | **Nâng cấp / Sửa lỗi** | `FACT Player Match Perf` |
| **[query_04](../mdx/query_04.md)** | `3.7.3` (Câu 3 cũ) | **Nâng cấp / Sửa lỗi** | `FACT Player Match Perf` + `Context` |
| **[query_05](../mdx/query_05.md)** | `3.7.4` (Câu 4 cũ) | **Mở rộng nghiệp vụ** | `FACT Player Match Perf` |
| **[query_06](../mdx/query_06.md)** | `3.7.5` (Câu 5 cũ) | **Nâng cấp / Sửa lỗi** | `FACT Player Match Perf` |
| **[query_07](../mdx/query_07.md)** | `3.7.6` (Câu 6 cũ) | **Nâng cấp / Sửa lỗi** | `FACT Player Match Perf` |
| **[query_08](../mdx/query_08.md)** | `3.7.8` (Câu 8 cũ — Top 10 CLB & `QoQ Goals Growth`) | **Thay thế nghiệp vụ mới** | `FACT Player Match Perf` |
| **[query_09](../mdx/query_09.md)** | `3.7.7` (Câu 7 cũ — `INTERSECT` Top 30 cuối tuần & ngày thường) | **Thay thế nghiệp vụ mới** | `FACT Player Match Perf` + `Context` |
| **[query_10](../mdx/query_10.md)** | *(chưa có trong bản cũ)* | **Bổ sung mới** | `FACT Club Match Official` |
| **[query_11](../mdx/query_11.md)** | `3.7.9` (Câu 9 cũ) | **Tái cấu trúc đúng Grain** | `DIM Game` + `DIM Home Club` |
| **[query_12](../mdx/query_12.md)** | `3.7.10` (Câu 10 cũ) | **Thay đổi & Mở rộng độ đo** | `FACT Player Match Perf` + `Context` |
| **[query_13](../mdx/query_13.md)** | *(chưa có trong bản cũ)* | **Bổ sung mới** | `FACT Player Match Perf` + `FACT Player Distinct` |
| **[query_14](../mdx/query_14.md)** | *(chưa có trong bản cũ)* | **Bổ sung mới** | `DIM Game` + `DIM Home/Away Club` |
| **[query_15](../mdx/query_15.md)** | *(chưa có trong bản cũ)* | **Bổ sung mới** | `FACT Player Match Perf` |

### 8.2. Quy tắc chuẩn hóa bắt buộc khi viết lại 3 công cụ (Cube Browser, Excel PivotTable, MDX)
1. **Định danh bằng khóa `&[...]` và `Player ID`:** Thay toàn bộ `[DIM Player].[Player Name]` thành `[DIM Player].[Player ID]` (hiển thị tên nhưng giữ khóa duy nhất), thay `[GB1]` / `[2023/2024]` / `[1]` / `[England]` thành cú pháp khóa chuẩn `&[GB1]`, `&[2023]`, `&[1]`, `&[England]`.
2. **Đúng bảng nguồn sau tái thiết kế:** Dùng `[DIM Game].[Season]` thay `[DIM Time].[Season]`; dùng `[DIM Appearance Context].[Player Age At Match]`, `[Is Home Game]`, `[Club Manager Name]` cho ngữ cảnh trận đấu; dùng DSV Named Calculations `[DIM Time].[Year Quarter Key]` (Câu 10) và `[DIM Time].[Year Month Key]` (Câu 12).
3. **Đồng nhất Cube Browser & Excel PivotTable:**
   - Trên **Cube Browser (SSDT)**: chỉ dùng các toán tử thực sự có trong giao diện (`Equal`, `Not Equal`, `In`, `Not In`, `Contains`, `Begins With`, `Range`, `Custom`), bỏ hoàn toàn toán tử không tồn tại ở bản cũ.
   - Trên **Excel PivotTable**: với trường hợp một trường hàng cần hai bộ lọc Value Filter đồng thời (như Câu 8: `Minutes Played >= 900` và `Top 10 by Goals Per 90`), dùng **PivotTable Analyze $\rightarrow$ Fields, Items, & Sets $\rightarrow$ Create Set Using MDX...**.
4. **Chuẩn hóa T-SQL đối chiếu:** Vì `Year_Quarter_Key` và `Year_Month_Key` là DSV Named Calculations trên `DIM_Time`, trong T-SQL đối chiếu ở Câu 10 và Câu 12 phải tính inline bằng `t.[Year] * 10 + t.[Quarter]` và `t.[Year] * 100 + t.[Month]`.

### 8.3. Chi tiết chỉnh sửa & mốc kiểm chứng cho từng câu (Q01–Q15)

1. **Câu 01 ([query_01.md](../mdx/query_01.md) | [query_01.mdx](../mdx/query_01.mdx)):** Đổi `Player Name` $\rightarrow$ `[DIM Player].[Player ID].[Player ID].MEMBERS`, đổi `[DIM Time].[Season].[2023/2024]` $\rightarrow$ `[DIM Game].[Season].&[2023]`, `[DIM Competition].[Competition ID].[GB1]` $\rightarrow$ `&[GB1]`. **Mốc kiểm chứng:** Top 10 ghi bàn Ngoại Hạng Anh 2023/2024 (Erling Haaland dẫn đầu: **27 bàn**).
2. **Câu 02 ([query_02.md](../mdx/query_02.md) | [query_02.mdx](../mdx/query_02.mdx)):** *Thêm mới* — `TOPCOUNT(..., 10, [Measures].[Assists])` trên `Player ID`, lát cắt `Main Position = &Midfield` và `Competition Type = &domestic_league`. **Mốc kiểm chứng:** Kevin De Bruyne dẫn đầu (**28 kiến tạo**); đồng hạng 18 kiến tạo ở nhóm cuối top 10 xếp ổn định theo `Player_ID` tăng dần.
3. **Câu 03 ([query_03.md](../mdx/query_03.md) | [query_03.mdx](../mdx/query_03.mdx)):** Đổi `Player Name` $\rightarrow$ `Player ID`, lát cắt `[DIM Game].[Season].&[2023]`, giữ `Goal Contributions > 20` và `ORDER(..., BDESC)`. **Mốc kiểm chứng:** Đúng **99 cầu thủ** (không bị gộp nhầm như khi dùng `Player Name`).
4. **Câu 04 ([query_04.md](../mdx/query_04.md) | [query_04.mdx](../mdx/query_04.mdx)):** Bỏ `[DIM Player].[Age]` và phân loại `Career Stage`; chuyển sang `[DIM Appearance Context].[Player Age At Match]`, đổi `FACT Player Match Perf Count` $\rightarrow$ `Appearance Count`, dùng `WITH SET [ValidAgeMembers]` loại `[Unknown]`, sửa `MEMBERVALUE` $\rightarrow$ `MEMBER_VALUE`, bỏ `ROUND(..., 2)` trong công thức (định dạng `#,##0.00`). **Mốc kiểm chứng:** **28 độ tuổi hợp lệ** (`15–42` tuổi) trong năm 2023.
5. **Câu 05 ([query_05.md](../mdx/query_05.md) | [query_05.mdx](../mdx/query_05.mdx)):** Mở rộng từ 5 vị trí tấn công sang toàn bộ `[DIM Player].[Sub Position]` hợp lệ (`EXCEPT(..., { [Unknown] })`) trên trục hàng, 3 giá trị chân thuận (`&[left]`, `&[right]`, `&[both]`) trên trục cột, dùng `NON EMPTY` và `ORDER(..., BDESC)`. **Mốc kiểm chứng:** **13 vị trí chi tiết** × **3 chân thuận**.
6. **Câu 06 ([query_06.md](../mdx/query_06.md) | [query_06.mdx](../mdx/query_06.mdx)):** Đưa `Avg Height Cm`, `Max Height Cm`, `Min Height Cm` vào tab `Calculations` với `EXISTING CrossJoin([DIM Player].[Player ID], FILTER(... > 0))` và `EXCEPT(..., { [Unknown] })`; trong MDX truy vấn chỉ giữ `SELECT ... ON COLUMNS, ORDER(EXCEPT([Main Position], {[Unknown]}), [Goals], BDESC) ON ROWS`. **Mốc kiểm chứng:** **4 tuyến chính** (`Forward`, `Midfield`, `Defender`, `Goalkeeper`), tính chiều cao TB trên từng cầu thủ duy nhất thay vì trung bình gia quyền theo lượt ra sân.
7. **Câu 07 ([query_07.md](../mdx/query_07.md) | [query_07.mdx](../mdx/query_07.mdx)):** Đổi `Pct Of England Goals` $\rightarrow$ `Pct Of Country Goals`, dùng `EXCEPT([Country Of Citizenship], {[Unknown]})` kết hợp `ORDER(NONEMPTY(...))` trên lát cắt `[DIM Competition].[Country Name].&[England]` (giữ phần Pareto 80% qua `TOPPERCENT` ở hướng dẫn Cube Browser/Excel). **Mốc kiểm chứng:** **75 quốc tịch** hợp lệ ghi bàn tại Anh; nhóm Pareto 80% gồm **18 quốc tịch**.
8. **Câu 08 ([query_08.md](../mdx/query_08.md) | [query_08.mdx](../mdx/query_08.mdx)):** *Thay thế Câu 8 cũ* — dùng `TOPCOUNT(FILTER(NONEMPTY([Player ID], ([Minutes Played], [Season].&[2023])), [Minutes Played] >= 900), 10, [Measures].[Goals Per 90])` trên lát cắt `[DIM Game].[Season].&[2023]`. **Mốc kiểm chứng:** **2.960 cầu thủ** đạt ngưỡng $\ge 900$ phút; Serhou Guirassy dẫn đầu (**1,14 bàn/90 phút** với 28 bàn / 2.214 phút; xếp hạng dùng tỷ lệ đầy đủ chưa làm tròn).
9. **Câu 09 ([query_09.md](../mdx/query_09.md) | [query_09.mdx](../mdx/query_09.mdx)):** *Thay thế Câu 7 cũ* — đối chiếu Sân nhà (`Is_Home_Game = 1`) vs Sân khách (`Is_Home_Game = 0`) vào cuối tuần (`[DIM Time].[Is Weekend].&[1]`) qua `CrossJoin` 5 độ đo (`Goals`, `Yellow Cards`, `Covered Match Count`, `Goals Per Match`, `Yellow Cards Per Match`) × `Is Home Game`, xếp giảm dần theo `Goals`. **Mốc kiểm chứng:** **207 CLB** ra sân cuối tuần (tổng bàn sân nhà **7.592** vs sân khách **6.048**; Man City Nhà: `2,63` bàn/trận, `1,13` thẻ vàng/trận).
10. **Câu 10 ([query_10.md](../mdx/query_10.md) | [query_10.mdx](../mdx/query_10.mdx)):** *Thêm mới* — dùng Measure Group `FACT Club Match Official`, cắt `[DIM Club].[Club ID].&[418]` (Real Madrid), `CrossJoin` giữa `[DIM Time].[Year Quarter Key]` và `[DIM Opponent Club].[Club ID]` (loại `Unknown`). **Mốc kiểm chứng:** **101 trận**, **216 bàn chính thức** (sau khi loại luân lưu) trên **92 cặp** quý – đối thủ.
11. **Câu 11 ([query_11.md](../mdx/query_11.md) | [query_11.mdx](../mdx/query_11.mdx)):** Chuyển từ `FACT_Player_Match_Perf` sang Measure Group **`DIM Game`** + Role-Playing **`DIM Home Club`**, xuất `[Measures].[Stadium Seats Value]` và `[Measures].[Official Match Count]`, lọc `[Stadium Seats Value] > 60000` (sửa `>=` thành `>` đúng yêu cầu Chương 1). **Mốc kiểm chứng:** **23 CLB sân nhà** có sức chứa $> 60.000$ chỗ, tổng **993 trận sân nhà**.
12. **Câu 12 ([query_12.md](../mdx/query_12.md) | [query_12.mdx](../mdx/query_12.mdx)):** *Thay thế Câu 10 cũ* — thống kê toàn bộ tổ hợp hợp lệ `Club × Club Manager Name × Year Month Key` (dùng `WITH SET [ValidManagers]` loại `Unknown` trên `DIM Appearance Context`, bỏ `GENERATE + TOPCOUNT`), xuất 5 độ đo gồm `Yellow Cards`, `Red Cards`, `Covered Match Count`, `Yellow Cards Per Match`, `Red Cards Per Match`. **Mốc kiểm chứng:** **3.967 tổ hợp** thực tế (loại **58 lượt ra sân thuộc 2 trận thiếu tên HLV**; AS Roma – José Mourinho `202305`: `3,13` vàng/trận; Union Berlin – Urs Fischer `202210`: `0,13` đỏ/trận).
13. **Câu 13 ([query_13.md](../mdx/query_13.md) | [query_13.mdx](../mdx/query_13.mdx)):** *Thêm mới* — kết hợp `Appearance Count` (`FACT Player Match Perf`) và `Distinct Player Count` (`FACT Player Distinct`) theo `CrossJoin([DIM Club].[Club ID], [DIM Club].[Squad Size])`, giữ lại `Unknown` ở `Squad Size` để không bỏ sót 8 CLB bổ sung có lượt ra sân. **Mốc kiểm chứng:** **235 CLB** có lượt ra sân (gồm **8 CLB bổ sung** mang giá trị `Unknown`).
14. **Câu 14 ([query_14.md](../mdx/query_14.md) | [query_14.mdx](../mdx/query_14.mdx)):** *Thêm mới* — lọc trên Measure Group **`DIM Game`** (`FILTER([DIM Game].[Game ID].[Game ID].MEMBERS, [Measures].[Total Match Goals] >= 5)`) rồi mới `*` với `Round`, `Stadium`, `DIM Home Club`, `DIM Away Club` và bọc `NONEMPTY(..., [Measures].[Official Match Count])` để tránh bùng nổ tích Descartes. **Mốc kiểm chứng:** **1.196 trận** có từ 5 bàn trở lên (**582** trận mùa 2022/2023 và **614** trận mùa 2023/2024; tối đa **10 bàn**).
15. **Câu 15 ([query_15.md](../mdx/query_15.md) | [query_15.mdx](../mdx/query_15.mdx)):** *Thêm mới* — định nghĩa `WITH SET [YouthPlayers2004]` dùng `CDate([DIM Player].[Date Of Birth].CURRENTMEMBER.NAME) >= CDate("2004-01-01")` đưa vào Subcube `FROM (SELECT [YouthPlayers2004] ON COLUMNS FROM [DW Football Transfermarkt])`, thống kê `Goals`, `Yellow Cards`, `Red Cards` theo `[DIM Time].[Full Date]`. **Mốc kiểm chứng:** **676 cầu thủ trẻ**, thi đấu trên **441 ngày**, ghi tổng cộng **403 bàn**.

---

## 9. TỔ CHỨC THƯ MỤC GITHUB & CHECKLIST KIỂM ĐỊNH

### 9.1. Cấu trúc đồng bộ trên GitHub (`ssas/` và `mdx/`)
- **`ssas/`**:
  - `ssas_overview.md` (Project & Data Source)
  - `ssas_dsv_dims.md` (DSV, 6 Named Calculations, 2 Named Queries & 6 Dimensions)
  - `ssas_cube_measures.md` (4 Measure Groups, 13 Base Measures & 13 Calculated Measures)
  - `ssas_hierarchies_relations.md` (9 Cube Dimensions × 4 Measure Groups, 5 Hierarchies & NullProcessing)
  - `ssas_deploy_mdx.md` (Deploy, đối soát 2 mùa & bảng tổng hợp 15 câu)
  - `ke_hoach_chinh_sua_ssas_mdx.md` *(tài liệu kế hoạch chuyển đổi này)*
- **`mdx/`**:
  - Đặt tập trung đủ 15 cặp `query_01.md/.mdx` $\rightarrow$ `query_15.md/.mdx` ngay trong `mdx/` (không tách 5 câu sang `archive/`).
  - Cập nhật `README.md` (bảng mục lục 15 câu + lưu ý DSV Named Calculations) và `checklist.md` (ma trận kỹ thuật MDX `G1–G7`, kiểm định độ phức tạp thực tế).
  - Toàn bộ tài liệu nháp của lược đồ cũ (`doc_query_*.md`, `archive/query_*.md`, `test.md`, `Bao_Cao_Double_Check_Query_10_11.xlsx`) chuyển vào [`../mdx/archive/legacy_v1/`](../mdx/archive/legacy_v1/) để lưu vết.

### 9.2. Checklist nghiệm thu trước khi chốt báo cáo
- [x] `DW_Football_Transfermarkt.dsv` đủ 6 bảng + 6 Named Calculations + 2 Named Queries (`FACT_Player_Match_Perf`, `FACT_Club_Match_Official`).
- [x] Đủ 6 Database Dimensions (có `DIM_Appearance_Context`) và 9 Cube Dimensions (có 4 Role-Playing `DIM_Club`).
- [x] 5 phân cấp không còn cảnh báo `Attribute Relationships`, `Quarter` / `Month` dùng `Year_Quarter_Key` / `Year_Month_Key`, `Round` dùng khóa ghép `(Season, Round)`.
- [x] Deploy `SSAS_Football_Transfermarkt` thành công (0 errors, 0 warnings), đối soát 2 mùa `2022/2023` & `2023/2024` khớp `100%` Chương 2.
- [x] Toàn bộ 15 câu MDX và bảng số liệu trong `mdx/query_01..15.*` khớp `1-1` với `Chuong_3_SSAS.docx`, 0 còn dấu vết lược đồ cũ (`Age`, `Coach_Name`, `Goal_Contributions` vật lý, `TMDB_Movie_DataWareHouse`).
