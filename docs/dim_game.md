# BẢNG CHIỀU: DIM_GAME (THÔNG TIN TRẬN ĐẤU)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Game` lưu trữ chi tiết bối cảnh tổ chức trận đấu, bao gồm vòng đấu, mã hai đội bóng đối đầu (Đội nhà vs Đội khách), tỷ số kết quả trận đấu và tên sân vận động diễn ra.

* **Tên bảng:** `dbo.DIM_Game`
* **Loại bảng:** Dimension Table (SCD Type 1)
* **Khóa chính (PK):** `Game_ID` (Natural Key từ hệ thống Transfermarkt)
* **Mô hình khóa:** **Natural Key (ID Trực tiếp)** - Không sử dụng Surrogate Key (`Game_SK`).
* **Quy tắc độ dài Chuỗi (String Length Standard):** Áp dụng nghiêm ngặt chuẩn **`NVARCHAR(100)`** hoặc **`NVARCHAR(200)`** cho 100% các cột chuỗi.
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Game_ID`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Game_ID` | `INT` | `PRIMARY KEY`, `NOT NULL` | Mã định danh trận đấu duy nhất từ Transfermarkt |
| Thuộc tính | `Round` | `NVARCHAR(100)` | `NULL` | Vòng đấu hoặc giai đoạn thi đấu (*Matchday 1, Quarter-Finals, Final...*) |
| Thuộc tính | `Home_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội chủ nhà |
| Thuộc tính | `Away_Club_ID` | `INT` | `NULL` | Mã câu lạc bộ đóng vai trò đội khách |
| Thuộc tính | `Home_Club_Goals` | `INT` | `CHECK (Home_Club_Goals >= 0)` | Số bàn thắng ghi được của đội chủ nhà |
| Thuộc tính | `Away_Club_Goals` | `INT` | `CHECK (Away_Club_Goals >= 0)` | Số bàn thắng ghi được của đội khách |
| Thuộc tính | `Stadium` | `NVARCHAR(200)` | `NULL` | Tên sân vận động diễn ra trận đấu |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

### 3.1. Các cột được giữ lại và chuyển thành thuộc tính DW (Maintained & Mapped)

| Cột thuộc tính nguồn (Kaggle) | Kiểu dữ liệu Kaggle | Cột thuộc tính đích (DW) | Kiểu dữ liệu DW | Đánh giá & Quy tắc chuyển đổi SSIS |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | `Int64` | `Game_ID` | `INT` | **Giữ nguyên:** Mã định danh trận đấu chính xác (PK) |
| `round` | `string` | `Round` | `NVARCHAR(100)` | **Giữ nguyên:** Tên vòng đấu, ép kiểu `[DT_WSTR, 100]` |
| `home_club_id` | `Int64` | `Home_Club_ID` | `INT` | **Giữ nguyên:** Mã CLB chủ nhà |
| `away_club_id` | `Int64` | `Away_Club_ID` | `INT` | **Giữ nguyên:** Mã CLB khách |
| `home_club_goals` | `Int64` | `Home_Club_Goals` | `INT` | **Giữ nguyên:** Tỷ số bàn thắng đội nhà |
| `away_club_goals` | `Int64` | `Away_Club_Goals` | `INT` | **Giữ nguyên:** Tỷ số bàn thắng đội khách |
| `stadium` | `string` | `Stadium` | `NVARCHAR(200)` | **Giữ nguyên:** Tên sân vận động, ép kiểu `[DT_WSTR, 200]` |

---

## 4. LÝ DO LOẠI BỎ CỘT SEASON KHỎI DIM_GAME
* Thuộc tính **Season (Mùa giải)** đã được quản lý tập trung và phân rã chi tiết trong bảng Chiều thời gian **`DIM_Time.Season`**.
* Việc không lưu `Season` trong `DIM_Game` giúp triệt tiêu dữ liệu dư thừa (data redundancy) và tuân thủ đúng chuẩn chuẩn hóa Star Schema.
