# CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN VỀ DỮ LIỆU

---

## 1.1. Tổng quan về dữ liệu

### 1.1.1. Mô tả về dữ liệu
- **Tên tập dữ liệu:** *Football Data from Transfermarkt* (thu thập & chuẩn hóa từ chuyên trang Transfermarkt, tác giả David Cariboo trên Kaggle).
- **Quy mô dữ liệu:** Gồm **7 tệp CSV** với tổng cộng **118 thuộc tính (cột)**, lưu trữ hơn **1.890.000 lượt ra sân thi đấu**.
- **Danh sách 7 tệp dữ liệu gốc:**
  1. `appearances.csv` (13 cột): Chi tiết lượt ra sân từng trận của cầu thủ (phút thi đấu, bàn thắng, kiến tạo, thẻ phạt...).
  2. `players.csv` (26 cột): Thông tin tiểu sử và nhân trắc học (họ tên, ngày sinh, quốc tịch, vị trí, chân thuận, chiều cao...).
  3. `clubs.csv` (17 cột): Thông tin các câu lạc bộ (tên CLB, tên sân vận động, sức chứa, HLV trưởng, quy mô đội hình...).
  4. `competitions.csv` (11 cột): Phân loại các giải đấu (mã giải, tên giải, quốc gia đăng cai, loại giải VĐQG / Cúp Châu Âu...).
  5. `games.csv` (23 cột): Thông tin chi tiết các trận đấu (mã trận, mùa giải, vòng đấu, ngày thi đấu, đội nhà, đội khách...).
  6. `player_valuations.csv` (13 cột): Lịch sử định giá thị trường của cầu thủ.
  7. `club_games.csv` (15 cột): Thống kê kết quả trận đấu cấp câu lạc bộ (bàn thắng, bàn thua, cờ thắng/thua/sân nhà/sân khách...).
- **Mục đích & Ứng dụng:** 
  - Phân tích khám phá (EDA), đánh giá hiệu suất đóng góp (Goals, Assists, P90 Metrics).
  - Phân tích mối tương quan giữa số phút thi đấu thực tế và hiệu quả đóng góp bàn thắng.
  - Đo lường ảnh hưởng của sân nhà/sân khách và tính kỷ luật (thẻ phạt) đến kết quả.
  - Cung cấp khối dữ liệu OLAP đa chiều cho ban quản trị CLB xây dựng chiến lược chuyển nhượng và đội hình.
- **Link Dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

---

### 1.1.2. Thuộc tính của dữ liệu nguồn (Flat File Sources cho ETL)

Dưới đây là mô tả các thuộc tính cốt lõi trong các tệp tin CSV nguồn được sử dụng làm Flat File Sources cho quy trình ETL:

#### a. Bảng `appearances` (Chi tiết lượt ra sân)
| STT | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 1 | `appearance_id` | Varchar | Mã định danh lượt ra sân |
| 2 | `game_id` | Int | Mã trận đấu (liên kết `games`) |
| 3 | `player_id` | Int | Mã cầu thủ (liên kết `players`) |
| 4 | `player_club_id` | Int | Mã câu lạc bộ cầu thủ thi đấu |
| 5 | `date` | Date | Ngày diễn ra trận đấu |
| 6 | `competition_id` | Varchar | Mã giải đấu (liên kết `competitions`) |
| 7 | `goals` | Int | Số bàn thắng ghi được trong trận |
| 8 | `assists` | Int | Số đường kiến tạo trong trận |
| 9 | `minutes_played` | Int | Số phút trực tiếp thi đấu |
| 10 | `yellow_cards` | Int | Số thẻ vàng phải nhận |
| 11 | `red_cards` | Int | Số thẻ đỏ phải nhận |

#### b. Bảng `players` (Thông tin cầu thủ)
| STT | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 1 | `player_id` | Int | Mã định danh cầu thủ |
| 2 | `name` | Varchar | Họ và tên đầy đủ |
| 3 | `date_of_birth` | Date | Ngày tháng năm sinh |
| 4 | `country_of_citizenship` | Varchar | Quốc tịch đăng ký thi đấu |
| 5 | `position` | Varchar | Vị trí thi đấu tổng quát (*Goalkeeper, Defender, Midfield, Attack*) |
| 6 | `sub_position` | Varchar | Vị trí chi tiết (*Centre-Back, Right Winger, Striker...*) |
| 7 | `foot` | Varchar | Chân thuận (*Left, Right, Both*) |
| 8 | `height_in_cm` | Int | Chiều cao thực tế (cm) |

#### c. Bảng `clubs` (Thông tin câu lạc bộ)
| STT | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 1 | `club_id` | Int | Mã định danh câu lạc bộ |
| 2 | `name` | Varchar | Tên đầy đủ câu lạc bộ |
| 3 | `stadium_name` | Varchar | Tên sân vận động nhà |
| 4 | `stadium_seats` | Int | Sức chứa tối đa của khán đài |
| 5 | `coach_name` | Varchar | Họ tên Huấn luyện viên trưởng |
| 6 | `squad_size` | Int | Số lượng cầu thủ đăng ký đội 1 |

#### d. Bảng `competitions` (Thông tin giải đấu)
| STT | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 1 | `competition_id` | Varchar | Mã giải đấu (Khóa chính: *GB1, ES1, CL...*) |
| 2 | `name` | Varchar | Tên chính thức của giải đấu |
| 3 | `country_name` | Varchar | Quốc gia đăng cai (*England, Spain, Europe...*) |
| 4 | `type` | Varchar | Loại hình (*domestic_league, international_cup*) |

#### e. Bảng `games` (Thông tin trận đấu)
| STT | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 1 | `game_id` | Int | Mã định danh trận đấu |
| 2 | `competition_id` | Varchar | Mã giải đấu diễn ra trận đấu |
| 3 | `season` | Int | Mùa giải (*2022, 2023*) |
| 4 | `round` | Varchar | Vòng đấu hoặc giai đoạn thi đấu |
| 5 | `date` | Date | Ngày diễn ra trận đấu |
| 6 | `home_club_id` | Int | Mã câu lạc bộ chủ nhà |
| 7 | `away_club_id` | Int | Mã câu lạc bộ khách |

---

### 1.1.3. Tiền xử lý dữ liệu
1. **Import thư viện:** Nạp các thư viện xử lý dữ liệu (`pandas`, `numpy`...).
2. **Đọc dữ liệu nguồn:** Tải dữ liệu từ các file CSV gốc.
3. **Khai báo tham số phạm vi (Scope):** Lọc phạm vi mùa giải (*2022/2023, 2023/2024*) và các giải đấu trọng điểm.
4. **Khử trùng lặp & Bảo đảm vẹn toàn tham chiếu:** Loại bỏ bản ghi trùng, kiểm tra liên kết khóa ngoại giữa các bảng.
5. **Chuẩn hóa & Xử lý dữ liệu:** Chuẩn hóa kiểu dữ liệu, xử lý giá trị khuyết (NULL), định dạng chuẩn ngày tháng (`YYYY-MM-DD`).
6. **Chọn lọc thuộc tính:** Trích xuất các cột cần thiết cho mô hình Kho dữ liệu.
7. **Xuất tệp dữ liệu sạch:** Lưu các file CSV đã làm sạch sẵn sàng cho quy trình SSIS ETL.

---

### 1.1.4. Hướng chủ đề nghiên cứu
**Chủ đề trọng tâm:** *Xây dựng Kho dữ liệu Phân tích Hiệu suất Thi đấu Cầu thủ và Hiệu quả Vận hành Câu lạc bộ Bóng đá Châu Âu.*

**Các mục tiêu nghiệp vụ chính:**
- **Đánh giá hiệu suất P90:** Tính toán năng suất ghi bàn/kiến tạo chuẩn hóa theo 90 phút.
- **Phân tích hiệu quả thực tế:** Nhận diện cầu thủ thi đấu bùng nổ, đóng góp lớn vào thành tích đội bóng.
- **Yếu tố môi trường & Kỷ luật:** Đo lường tác động của yếu tố sân bãi (sân nhà/sân khách), độ tuổi, vị trí đến thẻ phạt và hiệu suất.
- **Phân tích nguồn lực:** So sánh đóng góp giữa cầu thủ nội địa và ngoại binh.
- **Hỗ trợ quyết định chiến lược:** Cung cấp mô hình OLAP đa chiều cho ban quản trị CLB trong công tác chuyển nhượng và xếp đội hình.

---

## 1.2. Xây dựng kho dữ liệu

### 1.2.1. Thiết kế lược đồ (Star Schema)
Kho dữ liệu được thiết kế theo **Lược đồ Hình sao (Star Schema)** gồm **1 Bảng Sự kiện (Fact Table)** và **5 Bảng Chiều (Dimension Tables)**:

```text
                  ┌──────────────────┐
                  │    DIM_Player    │
                  └────────┬─────────┘
                           │
 ┌──────────────────┐      │      ┌──────────────────┐
 │     DIM_Club     ├──────┼──────┤  DIM_Competition │
 └──────────────────┘      │      └──────────────────┘
                           │
              ┌────────────┴────────────┐
              │  FACT_Player_Match_Perf │
              └────────────┬────────────┘
                           │
 ┌──────────────────┐      │      ┌──────────────────┐
 │     DIM_Game     ├──────┴──────┤     DIM_Time     │
 └──────────────────┘             └──────────────────┘
```

#### Mã Code DBDiagram.io (DBML Script):
```dbml
// Copy đoạn code này dán trực tiếp vào https://dbdiagram.io để sinh ERD tự động

Table DIM_Player {
  Player_ID int [primary key]
  Player_Name nvarchar(200)
  Date_Of_Birth nvarchar(100)
  Age int
  Country_Of_Citizenship nvarchar(200)
  Main_Position nvarchar(100)
  Sub_Position nvarchar(100)
  Foot nvarchar(100)
  Height_In_Cm int
}

Table DIM_Club {
  Club_ID int [primary key]
  Club_Name nvarchar(200)
  Stadium_Name nvarchar(200)
  Stadium_Seats int
  Coach_Name nvarchar(200)
  Squad_Size int
}

Table DIM_Competition {
  Competition_ID nvarchar(100) [primary key]
  Competition_Name nvarchar(200)
  Country_Name nvarchar(200)
  Competition_Type nvarchar(100)
}

Table DIM_Game {
  Game_ID int [primary key]
  Round nvarchar(100)
  Home_Club_ID int
  Away_Club_ID int
  Home_Club_Goals int
  Away_Club_Goals int
  Stadium nvarchar(200)
}

Table DIM_Time {
  Time_ID int [primary key]
  Full_Date nvarchar(100)
  Day_Of_Week nvarchar(100)
  Day int
  Month int
  Quarter int
  Year int
  Season nvarchar(100)
  Is_Weekend int
}

Table FACT_Player_Match_Perf {
  Appearance_ID int [pk, increment]
  Player_ID int [not null, ref: > DIM_Player.Player_ID]
  Club_ID int [not null, ref: > DIM_Club.Club_ID]
  Opponent_Club_ID int [ref: > DIM_Club.Club_ID]
  Competition_ID nvarchar(100) [not null, ref: > DIM_Competition.Competition_ID]
  Game_ID int [not null, ref: > DIM_Game.Game_ID]
  Time_ID int [not null, ref: > DIM_Time.Time_ID]
  Minutes_Played int
  Goals int
  Assists int
  Goal_Contributions int
  Yellow_Cards int
  Red_Cards int
  Is_Starter int
  Is_Home_Game int
}
```

---

### 1.2.2. Chi tiết các bảng trong kho dữ liệu

#### 1.2.2.1. Bảng `FACT_Player_Match_Perf`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Appearance_ID` | Int | Mã sự kiện lượt ra sân |
| 🗝 FK | `Player_ID` | Int | Mã cầu thủ (khóa ngoại `DIM_Player`) |
| 🗝 FK | `Club_ID` | Int | Mã câu lạc bộ của cầu thủ (khóa ngoại `DIM_Club`) |
| 🗝 FK | `Opponent_Club_ID` | Int | Mã câu lạc bộ đối thủ |
| 🗝 FK | `Competition_ID` | Nvarchar | Mã giải đấu (khóa ngoại `DIM_Competition`) |
| 🗝 FK | `Time_ID` | Int | Mã thời gian dạng YYYYMMDD (khóa ngoại `DIM_Time`) |
| 🗝 FK | `Game_ID` | Int | Mã trận đấu (khóa ngoại `DIM_Game`) |
| Measure | `Minutes_Played` | Int | Số phút trực tiếp thi đấu trên sân |
| Measure | `Goals` | Int | Số bàn thắng ghi được |
| Measure | `Assists` | Int | Số đường kiến tạo thành bàn |
| Measure | `Goal_Contributions` | Int | Tổng đóng góp bàn thắng (`Goals + Assists`) |
| Measure | `Yellow_Cards` | Int | Số thẻ vàng phải nhận |
| Measure | `Red_Cards` | Int | Số thẻ đỏ phải nhận |
| Flag | `Is_Starter` | Bit | Cờ đá chính (`1`: Đá chính, `0`: Dự bị) |
| Flag | `Is_Home_Game` | Bit | Cờ sân nhà (`1`: Sân nhà, `0`: Sân khách) |

#### 1.2.2.2. Bảng `DIM_Player`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Player_ID` | Int | Mã định danh cầu thủ |
| | `Player_Name` | Nvarchar | Họ và tên đầy đủ |
| | `Date_Of_Birth` | Date | Ngày tháng năm sinh |
| | `Age` | Int | Tuổi cầu thủ |
| | `Country_Of_Citizenship` | Nvarchar | Quốc tịch đăng ký thi đấu |
| | `Main_Position` | Nvarchar | Vị trí thi đấu chính (*Goalkeeper, Defender, Midfield, Attack*) |
| | `Sub_Position` | Nvarchar | Vị trí chi tiết (*Centre-Back, Left Winger, Centre-Forward...*) |
| | `Foot` | Nvarchar | Chân thuận (*Left, Right, Both*) |
| | `Height_In_Cm` | Int | Chiều cao thực tế (cm) |

#### 1.2.2.3. Bảng `DIM_Club`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Club_ID` | Int | Mã định danh câu lạc bộ |
| | `Club_Name` | Nvarchar | Tên câu lạc bộ |
| | `Stadium_Name` | Nvarchar | Tên sân vận động nhà |
| | `Stadium_Seats` | Int | Sức chứa tối đa sân vận động |
| | `Coach_Name` | Nvarchar | Họ tên Huấn luyện viên trưởng |
| | `Squad_Size` | Int | Số lượng cầu thủ đăng ký đội 1 |

#### 1.2.2.4. Bảng `DIM_Competition`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Competition_ID` | Varchar(10) | Mã giải đấu (*GB1, ES1, CL...*) |
| | `Competition_Name` | Varchar(100) | Tên chính thức giải đấu (*Premier League, La Liga...*) |
| | `Country_Name` | Varchar(100) | Quốc gia / Khu vực đăng cai |
| | `Competition_Type` | Varchar(50) | Phân loại (*domestic_league, international_cup*) |

#### 1.2.2.5. Bảng `DIM_Game`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Game_ID` | Int | Mã định danh trận đấu |
| | `Round` | Nvarchar | Vòng đấu hoặc giai đoạn thi đấu |
| | `Home_Club_ID` | Int | Mã câu lạc bộ chủ nhà |
| | `Away_Club_ID` | Int | Mã câu lạc bộ khách |
| | `Home_Club_Goals` | Int | Số bàn thắng của đội chủ nhà |
| | `Away_Club_Goals` | Int | Số bàn thắng của đội khách |
| | `Stadium` | Nvarchar | Tên sân vận động diễn ra trận đấu |

#### 1.2.2.6. Bảng `DIM_Time`
| Khóa | Tên thuộc tính | Kiểu dữ liệu | Mô tả thuộc tính |
| :---: | :--- | :--- | :--- |
| 🔑 PK | `Time_ID` | Int | Mã thời gian dạng YYYYMMDD |
| | `Full_Date` | Varchar(20) | Ngày thi đấu đầy đủ (*YYYY-MM-DD*) |
| | `Day_Of_Week` | Varchar(50) | Thứ trong tuần (*Monday, Tuesday...*) |
| | `Day` | Int | Ngày trong tháng (1 – 31) |
| | `Month` | Int | Tháng trong năm (1 – 12) |
| | `Quarter` | Int | Quý trong năm (1 – 4) |
| | `Year` | Int | Năm diễn ra trận đấu |
| | `Season` | Varchar(20) | Mùa giải bóng đá (*2022/2023, 2023/2024*) |
| Flag | `Is_Weekend` | Int | Cờ cuối tuần (`1`: Thứ 7 / Chủ Nhật, `0`: Ngày thường) |

---

### 1.2.3. Quy trình chuyển đổi SSIS ETL cho từng bảng DIM và FACT

Dưới đây là tổng hợp chi tiết cơ chế hoạt động của khối **Derived Column** và quy trình luồng dữ liệu SSIS Data Flow cho từng bảng Chiều (DIM) và bảng Sự kiện (FACT):

| Tên Bảng DW | Sử Dụng Khối `Derived Column` | Cơ Chế Hoạt Động Của `Derived Column` | Các Cột Sinh Mới / Xử Lý Trong SSIS |
| :--- | :---: | :--- | :--- |
| **`DIM_Competition`** | **Có** | **Replace Existing Column** *(Không sinh cột mới trong DW)* | Xử lý làm sạch NULL: `country_name` $\rightarrow$ `"Europe"`, `type` $\rightarrow$ `"domestic_league"`. |
| **`DIM_Club`** | **Có** | **Replace Existing Column** *(Không sinh cột mới trong DW)* | Xử lý làm sạch NULL: `stadium_name` $\rightarrow$ `"Unknown Stadium"`, `coach_name` $\rightarrow$ `"Unknown Coach"`, `stadium_seats` $\rightarrow$ `0`. |
| **`DIM_Player`** | **Có** | **Add as New Column & Replace Column** | **Sinh cột mới `Age`** từ `date_of_birth`; làm sạch NULL cho `Player_Name`, `Country_Of_Citizenship`, `Foot`, `Height_In_Cm`. |
| **`DIM_Game`** | **Có** | **Replace Existing Column** *(Không sinh cột mới trong DW)* | Xử lý làm sạch NULL: `stadium` $\rightarrow$ `"Unknown Stadium"`, `home_club_goals` $\rightarrow$ `0`, `away_club_goals` $\rightarrow$ `0`. |
| **`DIM_Time`** | **Có** | **Add as New Columns** *(Sinh tập hợp cột thuộc tính lịch)* | **Sinh 9 cột mới:** `Time_ID` (`YYYYMMDD`), `Full_Date`, `Day`, `Month`, `Quarter`, `Year`, `Day_Of_Week`, `Season`, `Is_Weekend`. |
| **`FACT_Player_Match_Perf`** | **Có** | **Add as New Columns** *(Sinh cờ nhận diện & độ đo tính toán)* | **Sinh 4 chỉ số/cờ mới:** `Goal_Contributions`, `Is_Starter`, `Is_Home_Game`, `Opponent_Club_ID` và gán mặc định `-1` cho bản ghi tra cứu khuyết. |

#### Chi tiết quy trình nạp dữ liệu SSIS Data Flow từng bảng:

1. **`DIM_Competition` (4 cột):**
   - `Flat File Source (cleaned_competitions.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Gán mặc định NULL)` $\rightarrow$ `Conditional Split (Validation 4 cột)` $\rightarrow$ `Sort (Unique Competition_ID)` $\rightarrow$ `OLE DB Destination`.
2. **`DIM_Club` (6 cột):**
   - `Flat File Source (cleaned_clubs.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Gán mặc định NULL)` $\rightarrow$ `Conditional Split (Validation 6 cột)` $\rightarrow$ `Sort (Unique Club_ID)` $\rightarrow$ `OLE DB Destination`.
3. **`DIM_Player` (9 cột):**
   - `Flat File Source (cleaned_players.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Sinh cột Age & Gán mặc định NULL)` $\rightarrow$ `Conditional Split (Validation 9 cột)` $\rightarrow$ `Sort (Unique Player_ID)` $\rightarrow$ `OLE DB Destination`.
4. **`DIM_Game` (7 cột):**
   - `Flat File Source (cleaned_games.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Gán mặc định NULL)` $\rightarrow$ `Conditional Split (Validation 7 cột)` $\rightarrow$ `Sort (Unique Game_ID)` $\rightarrow$ `OLE DB Destination`.
5. **`DIM_Time` (9 cột):**
   - `Flat File Source (games.csv/appearances.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Bóc tách 9 cột thời gian & Time_ID YYYYMMDD)` $\rightarrow$ `Conditional Split (Validation 9 cột)` $\rightarrow$ `Sort (Unique Time_ID)` $\rightarrow$ `OLE DB Destination`.
6. **`FACT_Player_Match_Perf`:**
   - `Flat File Source (appearances.csv)` $\rightarrow$ `Data Conversion` $\rightarrow$ `Derived Column (Prep der_time_id)` $\rightarrow$ `Conditional Split (Validation 11 cột)` $\rightarrow$ `5 Khối Lookup (Player, Club, Competition, Time, Game Info)` $\rightarrow$ `Derived Column (Tính Goal_Contributions, Is_Starter, Is_Home_Game, Opponent_Club_ID)` $\rightarrow$ `OLE DB Destination (Fast Load 50.000 rows/batch)`.

---

## 1.3. Các câu truy vấn nghiệp vụ (15 OLAP Queries)

Để phục vụ việc khai thác đa chiều và đảm bảo mọi thuộc tính được thiết kế trong bảng Sự kiện (FACT) và các bảng Chiều (DIM) đều có ý nghĩa thực tế, hệ thống 15 câu truy vấn nghiệp vụ dưới đây được diễn giải rõ ràng, dễ hiểu và bao phủ 100% các trường thuộc tính trong Kho dữ liệu:

1. Thống kê 10 cầu thủ có số bàn thắng (Goals) nhiều nhất tại giải đấu có mã giải Competition_ID = 'GB1' (Giải Ngoại Hạng Anh - Competition_Name) trong mùa giải Season 2023/2024. [Thuộc tính: Player_Name, Goals, Competition_ID, Competition_Name, Season]
2. Liệt kê 10 cầu thủ ở vị trí Tiền vệ (Main_Position) có số đường kiến tạo (Assists) nhiều nhất tại các giải đấu thuộc phân loại giải Vô địch Quốc gia (Competition_Type = 'domestic_league'). [Thuộc tính: Player_Name, Assists, Main_Position, Competition_Type]
3. Thống kê tổng số phút thi đấu (Minutes_Played) và tổng đóng góp bàn thắng (Goal_Contributions) của các cầu thủ có trên 20 lần góp công vào bàn thắng trong mùa giải Season 2023/2024. [Thuộc tính: Player_Name, Minutes_Played, Goal_Contributions, Season]
4. Thống kê tổng số bàn thắng (Goals), số đường kiến tạo (Assists) và tổng số phút thi đấu trung bình (Minutes_Played) của các cầu thủ phân theo từng độ tuổi (Age) trong năm 2023 (Year). [Thuộc tính: Age, Goals, Assists, Minutes_Played, Year]
5. So sánh tổng số bàn thắng ghi được (Goals) giữa các cầu thủ thuận chân Trái, chân Phải và Hai chân (Foot) theo từng vị trí thi đấu chi tiết (Sub_Position). [Thuộc tính: Foot, Sub_Position, Goals]
6. Thống kê chiều cao trung bình (Height_In_Cm), tổng bàn thắng (Goals) và tổng số thẻ vàng (Yellow_Cards) của các cầu thủ theo từng vị trí thi đấu chính (Main_Position). [Thuộc tính: Height_In_Cm, Main_Position, Goals, Yellow_Cards]
7. Thống kê tổng số bàn thắng (Goals) của các cầu thủ theo từng quốc tịch (Country_Of_Citizenship) khi thi đấu tại các giải đấu có quốc gia đăng cai là nước Anh (Country_Name = 'England'). [Thuộc tính: Country_Of_Citizenship, Country_Name, Goals]
8. Liệt kê danh sách các cầu thủ ghi nhiều bàn thắng nhất (Goals) khi vào sân từ băng ghế dự bị (Is_Starter = 0) và tổng số phút thi đấu (Minutes_Played) khi không đá chính của họ. [Thuộc tính: Player_Name, Is_Starter, Goals, Minutes_Played]
9. So sánh tổng số bàn thắng (Goals) và tổng số thẻ vàng (Yellow_Cards) của từng câu lạc bộ (Club_Name) khi thi đấu trên sân nhà so với khi thi đấu trên sân khách (Is_Home_Game) vào dịp cuối tuần (Is_Weekend = 1) so với ngày thường (Day_Of_Week). [Thuộc tính: Club_Name, Is_Home_Game, Goals, Yellow_Cards, Is_Weekend, Day_Of_Week]
10. Thống kê tổng số bàn thắng (Goals) mà câu lạc bộ có mã Club_ID = 418 (Real Madrid - Club_Name) đã ghi vào lưới của từng câu lạc bộ đối thủ (Opponent_Club_ID) phân theo từng Quý trong năm (Quarter). [Thuộc tính: Club_ID, Club_Name, Opponent_Club_ID, Goals, Quarter]
11. Thống kê số lượng trận đấu (Game_ID) đã diễn ra tại các sân vận động nhà (Stadium_Name) của câu lạc bộ (Club_Name) có sức chứa khán đài (Stadium_Seats) trên 60.000 khán giả. [Thuộc tính: Stadium_Name, Stadium_Seats, Club_Name, Game_ID]
12. Thống kê tổng số thẻ vàng (Yellow_Cards) và thẻ đỏ (Red_Cards) của các đội bóng (Club_Name) phân theo từng Huấn luyện viên trưởng (Coach_Name) qua từng tháng trong năm (Month). [Thuộc tính: Coach_Name, Club_Name, Yellow_Cards, Red_Cards, Month]
13. Thống kê tổng số lượt ra sân thi đấu (Appearance_ID) và số lượng cầu thủ (Player_ID) của các câu lạc bộ (Club_Name) phân theo quy mô số lượng cầu thủ đăng ký trong đội hình (Squad_Size). [Thuộc tính: Appearance_ID, Player_ID, Squad_Size, Club_Name]
14. Thống kê các trận đấu (Game_ID) kịch tính có tổng số bàn thắng của đội chủ nhà (Home_Club_Goals) và đội khách (Away_Club_Goals) từ 5 bàn trở lên giữa câu lạc bộ chủ nhà (Home_Club_ID) và câu lạc bộ khách (Away_Club_ID), diễn ra tại từng sân vận động (Stadium) qua các vòng đấu (Round). [Thuộc tính: Home_Club_ID, Away_Club_ID, Home_Club_Goals, Away_Club_Goals, Stadium, Round, Game_ID]
15. Thống kê số lượng bàn thắng (Goals) và thẻ phạt (Yellow_Cards, Red_Cards) của các cầu thủ trẻ sinh từ ngày 01/01/2004 (Date_Of_Birth) theo ngày thi đấu (Full_Date, Day) thuộc mã thời gian (Time_ID). [Thuộc tính: Date_Of_Birth, Time_ID, Full_Date, Day, Goals, Yellow_Cards, Red_Cards]
