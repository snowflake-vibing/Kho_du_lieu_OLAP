# HƯỚNG DẪN SSAS - PHẦN 4: DIMENSION USAGE, PHÂN CẤP & XỬ LÝ NULL

---

## 1. MỤC TIÊU

Cấu hình chuẩn xác **Dimension Usage** (bao gồm 4 **Role-Playing Dimensions** của `DIM_Club`), các **User-Defined Hierarchies**, **Attribute Relationships**, khóa ghép chống trùng kỳ/vòng đấu và quy tắc xử lý giá trị thiếu (`NullProcessing` / `UnknownMember`).

---

## 2. CẤU HÌNH DIMENSION USAGE (9 CUBE DIMENSIONS × 4 MEASURE GROUPS)

Trong tab **Dimension Usage** của Cube `DW Football Transfermarkt.cube`, từ cùng Database Dimension `DIM_Club`, tạo đủ 4 Role-Playing Cube Dimensions gồm `DIM Club`, `DIM Opponent Club`, `DIM Home Club` và `DIM Away Club`:

| Cube Dimension | `FACT Player Match Perf` | `FACT Player Distinct` | `FACT Club Match Official` | `DIM Game` (MG) |
| :--- | :--- | :--- | :--- | :--- |
| **`DIM Player`** | Regular (`Player_ID`) | Regular (`Player_ID`) | *Không liên kết* | *Không liên kết* |
| **`DIM Club`** | Regular (`Club_ID`) | Regular (`Club_ID`) | Regular (`Club_ID`) | *Không liên kết* |
| **`DIM Opponent Club`** | Regular (`Opponent_Club_ID`) | Regular (`Opponent_Club_ID`) | Regular (`Opponent_Club_ID`) | *Không liên kết* |
| **`DIM Home Club`** | *Không liên kết* | *Không liên kết* | *Không liên kết* | Regular (`Home_Club_ID`) |
| **`DIM Away Club`** | *Không liên kết* | *Không liên kết* | *Không liên kết* | Regular (`Away_Club_ID`) |
| **`DIM Competition`** | Regular (`Competition_ID`) | Regular (`Competition_ID`) | Regular (`Competition_ID`) | Regular (`Competition_ID`) |
| **`DIM Game`** | Regular (`Game_ID`) | Regular (`Game_ID`) | Regular (`Game_ID`) | Fact (`Game_ID`) |
| **`DIM Time`** | Regular (`Time_ID`) | Regular (`Time_ID`) | Regular (`Time_ID`) | Regular (`Time_ID`) |
| **`DIM Appearance Context`** | Fact (`Appearance_ID`) | Fact (`Appearance_ID`) | *Không liên kết* | *Không liên kết* |

- Giữ `IgnoreUnrelatedDimensions = True` trên các Measure Group để không nhân bản giá trị khi truy vấn trên chiều không liên quan.
- Tại ô giao `DIM Opponent Club` × `FACT Player Match Perf`, vào **Advanced** $\rightarrow$ đặt `Null Processing = UnknownMember`.

---

## 3. XÂY DỰNG PHÂN CẤP & ATTRIBUTE RELATIONSHIPS

### 1. `DIM_Time.dim` — `Calendar Hierarchy`
- **Các cấp độ**: `Year` $\rightarrow$ `Quarter` $\rightarrow$ `Month` $\rightarrow$ `Day` (không chứa `Season`).
- **Khóa kỳ tính trong DSV, phân biệt quý và tháng giữa các năm (2022–2024)**:
  - `Quarter`: `KeyColumns = Year_Quarter_Key (Integer)`, `NameColumn = Quarter (WChar)`, `OrderBy = Key`.
  - `Month`: `KeyColumns = Year_Month_Key (Integer)`, `NameColumn = Month (WChar)`, `OrderBy = Key`.
  - `Day`: `KeyColumns = Time_ID (Integer)`, `NameColumn = Day (WChar)`, `OrderBy = Key`.
- **Attribute Relationships** (`RelationshipType = Rigid`):
  `Time ID` $\rightarrow$ `Day` $\rightarrow$ `Month` $\rightarrow$ `Quarter` $\rightarrow$ `Year`; đồng thời `Time ID` $\rightarrow$ `Full Date` và `Time ID` $\rightarrow$ `Day Of Week` $\rightarrow$ `Is Weekend`.

### 2. `DIM_Player.dim` — `Position Hierarchy` & `Nationality Hierarchy`
- **`Position Hierarchy`**: `Main Position` $\rightarrow$ `Sub Position` $\rightarrow$ `Player ID`.
- **`Nationality Hierarchy`**: `Country Of Citizenship` $\rightarrow$ `Main Position` $\rightarrow$ `Player ID`.
- **Attribute Relationships** (`Flexible`): `Player ID` $\rightarrow$ `Sub Position` $\rightarrow$ `Main Position`, và `Player ID` $\rightarrow$ `Country Of Citizenship`.

### 3. `DIM_Game.dim` — `Season Round Hierarchy`
- **Các cấp độ**: `Season` $\rightarrow$ `Round` $\rightarrow$ `Game ID`.
- **Khóa ghép chống trùng tên vòng**: Vì có **55 tên vòng đấu** (`1. Matchday`, `Final`, `last 16 1st leg`…) xuất hiện ở cả hai mùa 2022 và 2023, cấu hình thuộc tính `Round` với **`KeyColumns = (Season, Round)`**, **`NameColumn = Round`**, `OrderBy = Key`.
- **Attribute Relationships**: `Game ID` $\rightarrow$ `Round` $\rightarrow$ `Season`; và `Game ID` $\rightarrow$ `Competition ID`, `Stadium`, `Date`.

### 4. `DIM_Competition.dim` — `Competition Hierarchy`
- **Các cấp độ**: `Competition Type` $\rightarrow$ `Country Name` $\rightarrow$ `Competition Name` $\rightarrow$ `Competition ID`.

---

## 4. QUY ƯỚC XỬ LÝ GIÁ TRỊ THIẾU (`NullProcessing` & `UnknownMember`)

| Đối tượng / Thuộc tính | Số dòng NULL | Thiết lập SSAS | Tác dụng khi truy vấn |
| :--- | :--- | :--- | :--- |
| `DIM_Club` (`Stadium_Name/Seats`, `Squad_Size`) | 25 CLB bổ sung | `UnknownMember = Visible (Unknown)`; `NullProcessing = UnknownMember` | Tách riêng CLB bổ sung từ `games.csv`, không biến NULL thành 0. |
| `DIM_Competition.Country_Name` | 3 giải (`CL`, `EL`, `UCOL`) | `NullProcessing = UnknownMember (Unknown)` | Bảo toàn `Competition Hierarchy` cho các cúp châu Âu. |
| `DIM_Player` (`Date_Of_Birth`, `Foot`, `Sub_Position`, `Country`, `Height`) | 2 / 124 / 2 / 107 / 121 | `KeyColumns NullProcessing = UnknownMember` | Dễ lọc bỏ `Unknown` khi tính trung bình chiều cao (Câu 6) hoặc chân thuận (Câu 5). |
| `DIM_Appearance_Context` (`Player_Age_At_Match`, `Club_Manager_Name`) | 33 / 58 lượt | `NullProcessing = UnknownMember (Unknown)` | Loại sạch bản ghi thiếu tuổi (Câu 4) hoặc thiếu tên HLV (Câu 12). |
| `FACT_Player_Match_Perf.Opponent_Club_ID` | 0 thực tế | `Measure Group NullProcessing = UnknownMember` | An toàn khóa ngoại theo DDL. |
| Các độ đo gốc (`Minutes_Played`, `Goals`, `Assists`, `Yellow/Red_Cards`) | 0 thực tế | `Measure NullProcessing = Preserve` | Phân biệt thiếu dữ liệu với số 0. |

---

## 5. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Đủ 9 Cube Dimensions (gồm 4 Role-Playing `DIM_Club`) nối chính xác với 4 Measure Groups.
- [x] Không còn cảnh báo tam giác vàng trên `Attribute Relationships` của 5 phân cấp.
- [x] Đã xử lý an toàn khóa ghép `Quarter`/`Month`/`Round` và toàn bộ các trường hợp `NULL`.
