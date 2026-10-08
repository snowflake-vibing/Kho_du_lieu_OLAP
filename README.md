# KHO DỮ LIỆU BÓNG ĐÁ CHÂU ÂU (FOOTBALL DATA WAREHOUSE & OLAP ANALYTICS)

> **Môn học:** KHO DỮ LIỆU & OLAP (IS217)  
> **Đồ án / Báo cáo:** Phân Tích Hiệu Suất Thi Đấu Cầu Thủ và Hiệu Quả Vận Hành Câu Lạc Bộ Bóng Đá Châu Âu (2022 - 2024)  
> **Mã nhóm / Bài tập:** BTA11 (MSSV: 24520496 - 24521123)  
> **Tập dữ liệu nguồn:** [Football Data from Transfermarkt (Kaggle)](https://www.kaggle.com/datasets/davidcariboo/player-scores)

---

## 📌 1. TỔNG QUAN DỰ ÁN

Dự án xây dựng một **Kho dữ liệu (Data Warehouse)** hoàn chỉnh theo mô hình Hình sao (Star Schema) kết hợp với quy trình **ETL tự động bằng Microsoft SSIS (SQL Server Integration Services)**. Hệ thống lưu trữ và phân tích khối dữ liệu lịch sử bóng đá quy mô lớn với:
* **7 tệp CSV gốc:** `appearances.csv`, `players.csv`, `clubs.csv`, `competitions.csv`, `games.csv`, `player_valuations.csv`, `club_games.csv`.
* **Dữ liệu đã qua làm sạch trong thư mục [`data/`](data/):** `cleaned_appearances.csv`, `cleaned_clubs.csv`, `cleaned_competitions.csv`, `cleaned_games.csv`, `cleaned_players.csv`.
* **118 thuộc tính tổng cộng** và hơn **1.890.000 lượt ra sân thi đấu** của các cầu thủ chuyên nghiệp.
* **Mục tiêu phân tích:** Đánh giá năng suất ghi bàn/kiến tạo chuẩn hóa 90 phút (P90 Metrics), mối tương quan giữa khối lượng thi đấu và đóng góp chuyên môn, ảnh hưởng của tính kỷ luật (thẻ phạt) và yếu tố sân bãi (sân nhà/sân khách).

---

## 📐 2. KIẾN TRÚC SƠ ĐỒ HÌNH SAO (STAR SCHEMA ERD)

Mô hình Kho dữ liệu được thiết kế gồm **1 bảng Sự kiện (Fact Table)** trung tâm và **5 bảng Chiều (Dimension Tables)** liên kết qua các Khóa thay thế (Surrogate Keys):

```mermaid
erDiagram
    DIM_Player ||--o{ FACT_Player_Match_Perf : "1 - N (Player_SK)"
    DIM_Club ||--o{ FACT_Player_Match_Perf : "1 - N (Club_SK)"
    DIM_Club ||--o{ FACT_Player_Match_Perf : "1 - N (Opponent_Club_SK)"
    DIM_Competition ||--o{ FACT_Player_Match_Perf : "1 - N (Competition_SK)"
    DIM_Game ||--o{ FACT_Player_Match_Perf : "1 - N (Game_SK)"
    DIM_Time ||--o{ FACT_Player_Match_Perf : "1 - N (Time_SK)"

    DIM_Player {
        int Player_SK PK "Surrogate Key (Identity)"
        int Player_ID BK "Natural Key (Kaggle)"
        nvarchar Player_Name "Họ tên cầu thủ"
        nvarchar Date_Of_Birth "Ngày sinh (YYYY-MM-DD)"
        int Age "Tuổi cầu thủ"
        nvarchar Country_Of_Citizenship "Quốc tịch"
        nvarchar Main_Position "Vị trí chính"
        nvarchar Sub_Position "Vị trí chi tiết"
        nvarchar Foot "Chân thuận (Left, Right, Both)"
        int Height_In_Cm "Chiều cao (cm)"
    }

    DIM_Club {
        int Club_SK PK "Surrogate Key (Identity)"
        int Club_ID BK "Natural Key (Kaggle)"
        nvarchar Club_Name "Tên câu lạc bộ"
        nvarchar Stadium_Name "Tên sân vận động"
        int Stadium_Seats "Sức chứa khán đài"
        nvarchar Coach_Name "Huấn luyện viên trưởng"
        int Squad_Size "Quy mô đội hình 1"
    }

    DIM_Competition {
        int Competition_SK PK "Surrogate Key (Identity)"
        nvarchar Competition_ID BK "Mã giải đấu (GB1, ES1, CL...)"
        nvarchar Competition_Name "Tên chính thức giải đấu"
        nvarchar Country_Name "Quốc gia đăng cai"
        nvarchar Competition_Type "domestic_league / international_cup"
    }

    DIM_Game {
        int Game_SK PK "Surrogate Key (Identity)"
        int Game_ID BK "Natural Key (Kaggle)"
        int Season "Mùa giải (2022, 2023, 2024)"
        nvarchar Round "Vòng đấu / Giai đoạn"
        int Home_Club_ID "Mã đội chủ nhà"
        int Away_Club_ID "Mã đội khách"
        int Home_Club_Goals "Số bàn thắng đội nhà"
        int Away_Club_Goals "Số bàn thắng đội khách"
        nvarchar Stadium "Tên sân vận động"
    }

    DIM_Time {
        int Time_SK PK "Surrogate Key (Identity)"
        int Time_ID BK "Khóa YYYYMMDD"
        nvarchar Full_Date "Ngày thi đấu đầy đủ"
        nvarchar Day_Of_Week "Thứ trong tuần"
        int Day "Ngày (1-31)"
        int Month "Tháng (1-12)"
        int Quarter "Quý (1-4)"
        int Year "Năm"
        nvarchar Season "Mùa giải bóng đá"
        int Is_Weekend "Cờ cuối tuần (1/0)"
    }

    FACT_Player_Match_Perf {
        int Appearance_ID PK "Surrogate Key (Identity)"
        int Player_SK FK "Khóa ngoại DIM_Player"
        int Club_SK FK "Khóa ngoại DIM_Club (Chủ quản)"
        int Opponent_Club_SK FK "Khóa ngoại DIM_Club (Đối thủ)"
        int Competition_SK FK "Khóa ngoại DIM_Competition"
        int Game_SK FK "Khóa ngoại DIM_Game"
        int Time_SK FK "Khóa ngoại DIM_Time"
        int Game_ID BK "Mã trận đấu"
        int Minutes_Played "Số phút thi đấu trên sân"
        int Goals "Số bàn thắng ghi được"
        int Assists "Số đường kiến tạo thành bàn"
        int Goal_Contributions "Tổng bàn thắng + kiến tạo"
        int Yellow_Cards "Số thẻ vàng nhận phải"
        int Red_Cards "Số thẻ đỏ nhận phải"
        int Is_Starter "Cờ đá chính (1/0)"
        int Is_Home_Game "Cờ thi đấu sân nhà (1/0)"
    }
```

---

## 🗂️ 3. DANH MỤC HỒ SƠ BẢNG DỮ LIỆU & BẢNG ĐỐI CHIẾU 3 CHIỀU

👉 **Bảng Ma Trận Đối Chiếu 3 Chiều:** 📋 [docs/cross_checking_matrix.md](docs/cross_checking_matrix.md) (Kiểm tra khớp 100% giữa **Data Cleaned CSV** $\leftrightarrow$ **SSIS ETL Blocks** $\leftrightarrow$ **DW Schema Docs**).

| Tên bảng DW | Loại bảng | Mô tả chức năng & Đối chiếu Kaggle | Tệp tài liệu chi tiết |
| :--- | :--- | :--- | :--- |
| **`FACT_Player_Match_Perf`** | Fact Table | Lưu trữ chỉ số đóng góp thi đấu, số phút, bàn thắng, thẻ phạt | 📄 [fact_player_match_perf.md](docs/fact_player_match_perf.md) |
| **`DIM_Player`** | Dimension | Quản lý tiểu sử, vị trí, chân thuận, chiều cao, tuổi tác cầu thủ | 📄 [dim_player.md](docs/dim_player.md) |
| **`DIM_Club`** | Dimension | Quản lý tên CLB, sân vận động, sức chứa, HLV trưởng, quy mô đội hình | 📄 [dim_club.md](docs/dim_club.md) |
| **`DIM_Competition`** | Dimension | Phân loại giải đấu (VĐQG vs Cúp Châu Âu), quốc gia đăng cai | 📄 [dim_competition.md](docs/dim_competition.md) |
| **`DIM_Game`** | Dimension | Chi tiết bối cảnh trận đấu, vòng đấu, đội nhà/khách, tỷ số | 📄 [dim_game.md](docs/dim_game.md) |
| **`DIM_Time`** | Dimension | Phân rã thời gian: Ngày, Thứ, Tháng, Quý, Năm, Mùa giải, Cờ cuối tuần | 📄 [dim_time.md](docs/dim_time.md) |

---

## ⚙️ 4. HƯỚNG DẪN CẤU HÌNH CHI TIẾT TỪNG KHỐI SSIS (SSIS BLOCK GUIDES)

Thư mục [`ssis/`](ssis/) chứa các hướng dẫn cấu hình chi tiết cho từng khối (Flat File Source, Data Conversion, Derived Column, Conditional Split, Sort, OLE DB Destination):

| Đối tượng / Bảng SSIS | Mô tả chi tiết cấu hình khối Data Flow | Tệp tài liệu khối SSIS |
| :--- | :--- | :--- |
| **Tổng quan Kiến trúc & Nguyên tắc 0 Warning** | Chuẩn 6 khối Data Flow & Quy tắc vàng triệt tiêu 100% Warning | ⚙️ [ssis_overview_pipeline.md](ssis/ssis_overview_pipeline.md) |
| **`FACT_Player_Match_Perf`** | Cấu hình nạp Staging Fast Load & Execute SQL Task Populate Fact | ⚙️ [ssis_fact_player_match_perf.md](ssis/ssis_fact_player_match_perf.md) |
| **`DIM_Club`** | Cấu hình ép kiểu, xử lý NULL sân vận động/HLV và khử trùng lặp | ⚙️ [ssis_dim_club.md](ssis/ssis_dim_club.md) |
| **`DIM_Player`** | Cấu hình ép kiểu, tính toán tuổi tác và validation cầu thủ | ⚙️ [ssis_dim_player.md](ssis/ssis_dim_player.md) |
| **`DIM_Competition`** | Cấu hình mã giải đấu `GB1`/`ES1` và phân loại cúp | ⚙️ [ssis_dim_competition.md](ssis/ssis_dim_competition.md) |
| **`DIM_Game`** | Cấu hình nạp bối cảnh trận đấu, vòng đấu và tỷ số | ⚙️ [ssis_dim_game.md](ssis/ssis_dim_game.md) |
| **`DIM_Time`** | Cấu hình bóc tách YYYYMMDD, thứ, tháng, quý, cờ cuối tuần | ⚙️ [ssis_dim_time.md](ssis/ssis_dim_time.md) |

---

## 📊 5. BÁO CÁO 15 CÂU TRUY VẤN NGHIỆP VỤ OLAP

Hệ thống cung cấp **15 câu truy vấn nghiệp vụ đa chiều (OLAP Queries)** bao phủ 100% các thuộc tính trong mô hình Kho dữ liệu.

👉 **Xem toàn bộ câu lệnh T-SQL và giải trình chi tiết:** 📄 [15_queries.md](docs/15_queries.md)
