# BẢNG SỰ KIỆN: FACT_PLAYER_MATCH_PERF (HIỆU SUẤT TRẬN ĐẤU CỦA CẦU THỦ)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `FACT_Player_Match_Perf` là bảng Sự kiện trung tâm (Central Fact Table) trong sơ đồ hình sao (Star Schema) của Kho dữ liệu bóng đá. Bảng này lưu trữ chi tiết mức độ đóng góp chuyên môn, chỉ số hiệu suất thi đấu, số phút có mặt trên sân, các sự kiện bàn thắng, kiến tạo, thẻ phạt của từng cầu thủ trong mỗi lượt ra sân thi đấu.

* **Tên bảng:** `dbo.FACT_Player_Match_Perf`
* **Loại bảng:** Fact Table (Transactional Grain: Single Player Appearance per Match)
* **Mức độ hạt (Grain):** Mỗi bản ghi đại diện cho **1 lượt ra sân thi đấu của 1 cầu thủ trong 1 trận đấu cụ thể**.
* **Khóa chính (PK):** `Appearance_ID` (Tự tăng Identity)
* **Số lượng Khóa ngoại (FK):** 6 khóa ngoại tự nhiên liên kết tới 5 bảng Chiều (`DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`).
* **Mô hình khóa:** **Natural Keys (ID trực tiếp)** - Loại bỏ hoàn toàn Surrogate Keys (`*_SK`).

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA & MEASURES)

| Khóa / Độ đo | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Appearance_ID` | `INT` | `IDENTITY(1,1)`, `PRIMARY KEY` | Mã định danh lượt ra sân tự tăng |
| 🔗 **FK 1** | `Player_ID` | `INT` | `NOT NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Player` | Khóa ngoại tra cứu thông tin cầu thủ |
| 🔗 **FK 2** | `Club_ID` | `INT` | `NOT NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Club` | Khóa ngoại tra cứu câu lạc bộ chủ quản của cầu thủ |
| 🔗 **FK 3** | `Opponent_Club_ID` | `INT` | `NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Club` | Khóa ngoại tra cứu câu lạc bộ đối thủ |
| 🔗 **FK 4** | `Competition_ID` | `NVARCHAR(100)` | `NOT NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Competition` | Khóa ngoại tra cứu thông tin giải đấu |
| 🔗 **FK 5** | `Game_ID` | `INT` | `NOT NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Game` | Khóa ngoại tra cứu chi tiết trận đấu |
| 🔗 **FK 6** | `Time_ID` | `INT` | `NOT NULL`, `FOREIGN KEY` $\rightarrow$ `DIM_Time` | Khóa ngoại tra cứu thời gian diễn ra trận đấu (`YYYYMMDD`) |
| 📊 **Measure** | `Minutes_Played` | `INT` | `DEFAULT 0, CHECK >= 0` | Số phút trực tiếp thi đấu trên sân |
| 📊 **Measure** | `Goals` | `INT` | `DEFAULT 0, CHECK >= 0` | Số bàn thắng cầu thủ ghi được |
| 📊 **Measure** | `Assists` | `INT` | `DEFAULT 0, CHECK >= 0` | Số đường chuyền kiến tạo thành bàn |
| 📊 **Measure** | `Goal_Contributions` | `INT` | `DEFAULT 0` | Tổng đóng góp bàn thắng (`Goals + Assists`) |
| 📊 **Measure** | `Yellow_Cards` | `INT` | `DEFAULT 0, CHECK >= 0` | Số thẻ vàng cầu thủ phải nhận trong trận |
| 📊 **Measure** | `Red_Cards` | `INT` | `DEFAULT 0, CHECK >= 0` | Số thẻ đỏ cầu thủ phải nhận trong trận |
| 🚩 **Flag** | `Is_Starter` | `INT` / `BIT` | `CHECK (Is_Starter IN (0, 1))` | Cờ đá chính (`1`: Đá chính $\ge 60$ phút, `0`: Ghế dự bị) |
| 🚩 **Flag** | `Is_Home_Game` | `INT` / `BIT` | `CHECK (Is_Home_Game IN (0, 1))` | Cờ sân nhà (`1`: Thi đấu sân nhà, `0`: Thi đấu sân khách) |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

### 3.1. Các cột được chuyển thành Khóa tự nhiên và Độ đo trong Fact

| Cột nguồn (Kaggle) | Tệp CSV nguồn | Cột đích (DW Fact) | Vai trò / Kiểu dữ liệu | Đánh giá & Biến đổi SSIS ETL |
| :--- | :--- | :--- | :--- | :--- |
| `player_id` | `appearances.csv` | `Player_ID` | Foreign Key (`INT`) | SSIS Lookup `DIM_Player` $\rightarrow$ Lấy `Player_ID` |
| `player_club_id` | `appearances.csv` | `Club_ID` | Foreign Key (`INT`) | SSIS Lookup `DIM_Club` $\rightarrow$ Lấy `Club_ID` |
| `game_id` + `player_club_id` | `appearances.csv` | `Opponent_Club_ID` | Foreign Key (`INT`) | Lookup `DIM_Game` lấy `Home/Away_Club_ID` $\rightarrow$ Xác định Đội đối thủ |
| `competition_id` | `appearances.csv` | `Competition_ID` | Foreign Key (`NVARCHAR`) | SSIS Lookup `DIM_Competition` $\rightarrow$ Lấy `Competition_ID` |
| `game_id` | `appearances.csv` | `Game_ID` | Foreign Key (`INT`) | SSIS Lookup / Direct Match `DIM_Game` $\rightarrow$ Lấy `Game_ID` |
| `date` | `appearances.csv` | `Time_ID` | Foreign Key (`INT`) | SSIS Derived Column: `YYYYMMDD` int format $\rightarrow$ Khóa ngoại `DIM_Time` |
| `minutes_played` | `appearances.csv` | `Minutes_Played` | Measure (`INT`) | **Giữ nguyên:** Số phút thi đấu trên sân |
| `goals` | `appearances.csv` | `Goals` | Measure (`INT`) | **Giữ nguyên:** Số bàn thắng ghi được |
| `assists` | `appearances.csv` | `Assists` | Measure (`INT`) | **Giữ nguyên:** Số đường kiến tạo thành bàn |
| Calculated | - | `Goal_Contributions` | Measure (`INT`) | **Thêm mới:** `Goals + Assists` |
| `yellow_cards` | `appearances.csv` | `Yellow_Cards` | Measure (`INT`) | **Giữ nguyên:** Số thẻ vàng nhận phải |
| `red_cards` | `appearances.csv` | `Red_Cards` | Measure (`INT`) | **Giữ nguyên:** Số thẻ đỏ nhận phải |
| Calculated | - | `Is_Starter` | Flag (`INT` / `BIT`) | **Thêm mới:** `minutes_played >= 60 ? 1 : 0` |
| Calculated | - | `Is_Home_Game` | Flag (`INT` / `BIT`) | **Thêm mới:** `player_club_id == Home_Club_ID ? 1 : 0` |

---

## 4. QUY TRÌNH NẠP DỮ LIỆU SSIS ETL TỐI ƯU (BỎ QUA STAGING)

Quy trình nạp bảng Sự kiện `FACT_Player_Match_Perf` cho 1.89 triệu dòng được nạp **TRỰC TIẾP từ `appearances.csv`** qua **Luồng Tối Ưu 9 Khối trong Data Flow Task**:
1. **Source:** `Flat File Source (appearances.csv)`.
2. **Transformations:** Ép kiểu (`Data Conversion`), Lọc hợp lệ (`Conditional Split`), Tra cứu 4 Khối Lookup (`Player`, `Club`, `Competition`, `Game Info`), 1 Khối `Derived Column` duy nhất tính toán `Time_ID`, `Is_Starter`, `Is_Home_Game`, `Opponent_Club_ID`.
3. **Destination:** `OLE DB Destination` (`Fast Load 50.000 rows/batch`, `Table Lock`).
