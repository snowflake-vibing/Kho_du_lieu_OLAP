# BẢNG CHIỀU: DIM_TIME (THỜI GIAN & MÙA GIẢI)

## 1. TỔNG QUAN & VAI TRÒ TRONG KHO DỮ LIỆU

Bảng `DIM_Time` đóng vai trò là chiều thời gian chuẩn hóa trong Kho dữ liệu, hỗ trợ phân tích đa chiều theo cấp bậc thời gian: Ngày, Thứ trong tuần, Tháng, Quý, Năm và Mùa giải bóng đá.

* **Tên bảng:** `dbo.DIM_Time`
* **Loại bảng:** Dimension Table (Static Calendar Dimension)
* **Khóa chính (PK):** `Time_SK` (Surrogate Key - Auto Identity)
* **Khóa nghiệp vụ (BK):** `Time_ID` (Khóa số nguyên dạng `YYYYMMDD`, ví dụ: `20230815`)
* **Liên kết Star Schema:** Liên kết 1 - N với bảng Sự kiện `FACT_Player_Match_Perf` qua khóa ngoại `Time_SK`.

---

## 2. CẤU TRÚC THUỘC TÍNH (TABLE SCHEMA)

| Khóa / Vai trò | Tên thuộc tính trong DW | Kiểu dữ liệu DW | Ràng buộc / Constraint | Mô tả chi tiết |
| :---: | :--- | :--- | :--- | :--- |
| 🔑 **PK** | `Time_SK` | `INT` | `IDENTITY(1,1)`, `NOT NULL` | Khóa thay thế tự tăng làm khóa chính trong DW |
| 📌 **BK** | `Time_ID` | `INT` | `NOT NULL` | Khóa thời gian dạng số nguyên `YYYYMMDD` (Ví dụ: `20230924`) |
| Thuộc tính | `Full_Date` | `NVARCHAR(50)` | `NULL` | Ngày diễn ra trận đấu đầy đủ định dạng `YYYY-MM-DD` |
| Thuộc tính | `Day_Of_Week` | `NVARCHAR(50)` | `NULL` | Thứ trong tuần (*Monday, Tuesday... Sunday*) |
| Thuộc tính | `Day` | `INT` | `CHECK (Day BETWEEN 1 AND 31)` | Ngày trong tháng (1 - 31) |
| Thuộc tính | `Month` | `INT` | `CHECK (Month BETWEEN 1 AND 12)` | Tháng trong năm (1 - 12) |
| Thuộc tính | `Quarter` | `INT` | `CHECK (Quarter BETWEEN 1 AND 4)` | Quý trong năm (1, 2, 3, 4) |
| Thuộc tính | `Year` | `INT` | `CHECK (Year BETWEEN 2000 AND 2030)` | Năm diễn ra trận đấu |
| Thuộc tính | `Season` | `NVARCHAR(50)` | `NULL` | Chuỗi mùa giải bóng đá (*2022/2023, 2023/2024*) |
| Cờ (Flag) | `Is_Weekend` | `INT` | `CHECK (Is_Weekend IN (0, 1))` | Cờ ngày cuối tuần (`1`: Thứ 7 / Chủ Nhật, `0`: Ngày thường) |

---

## 3. PHÂN TÍCH ĐỐI CHIẾU DỮ LIỆU NGUỒN KAGGLE (KAGGLE CROSS-CHECKING)

* **Nguồn trích xuất thời gian:** Trích xuất từ thuộc tính `date` trong `appearances.csv` và `games.csv`.
* **Đường dẫn dataset gốc:** [Kaggle - Transfermarkt Player Scores](https://www.kaggle.com/datasets/davidcariboo/player-scores)

### 3.1. Các thuộc tính được sinh ra và tính toán chuẩn hóa (Generated Time Attributes)

Trong bộ dữ liệu gốc Kaggle, thuộc tính thời gian chỉ là 1 cột chuỗi ký tự đơn lẻ `date` (`YYYY-MM-DD`). Trong Kho dữ liệu, cột này đã được **phân rã đa chiều** thành các thuộc tính phong phú:

| Cột nguồn (Kaggle) | Thuộc tính DW sinh ra | Kiểu dữ liệu DW | Quy tắc tính toán & Giá trị tạo ra |
| :--- | :--- | :--- | :--- |
| `date` | `Time_ID` | `INT` | **Khóa số nguyên `YYYYMMDD`:** `(YEAR(date) * 10000) + (MONTH(date) * 100) + DAY(date)` |
| `date` | `Full_Date` | `NVARCHAR(50)` | **Chuỗi ngày đầy đủ:** Định dạng chuẩn `YYYY-MM-DD` |
| `date` | `Day_Of_Week` | `NVARCHAR(50)` | **Tên thứ trong tuần:** `DATENAME(dw, date)` (*Monday, Tuesday...*) |
| `date` | `Day` | `INT` | **Ngày trong tháng:** `DAY(date)` (1 - 31) |
| `date` | `Month` | `INT` | **Tháng trong năm:** `MONTH(date)` (1 - 12) |
| `date` | `Quarter` | `INT` | **Quý trong năm:** `DATEPART(quarter, date)` (1 - 4) |
| `date` | `Year` | `INT` | **Năm:** `YEAR(date)` |
| `date` | `Season` | `NVARCHAR(50)` | **Ghép chuỗi Mùa giải:** `Month >= 8 ? Year + "/" + (Year+1) : (Year-1) + "/" + Year` |
| `date` | `Is_Weekend` | `INT` | **Cờ cuối tuần:** `(Day_Of_Week IN ('Saturday', 'Sunday')) ? 1 : 0` |

### 3.2. Đánh giá sự dư thừa của phép tính ngày tháng động trong SQL truyền thống

* **Vấn đề trong SQL truyền thống:** Nếu không tạo `DIM_Time`, mỗi khi chạy câu truy vấn OLAP nhóm theo Tháng/Quý/Thứ/Mùa giải, cơ sở dữ liệu phải liên tục gọi các hàm xử lý chuỗi và thời gian đắt đỏ như `DATEPART()`, `DATENAME()`, `MONTH()`, `YEAR()` trên hàng triệu dòng Fact.
* **Giải pháp Kho dữ liệu:** `DIM_Time` giúp **tính toán sẵn 1 lần (Pre-computed)** toàn bộ cấp bậc thời gian, biến các phép lọc phức tạp thành phép toán JOIN cực nhanh trên khóa số nguyên `Time_ID`.

---

## 4. QUY TRÌNH TẠO & NẠP DỮ LIỆU (POPULATION LOGIC)

1. **Sinh dữ liệu lịch tự động (Calendar Population Script):** Bảng `DIM_Time` được khởi tạo bằng script SQL tự động sinh toàn bộ các ngày từ năm 2020 đến 2030 để đảm bảo tính sẵn sàng tra cứu.
2. **Cấu hình Bản ghi không xác định (Unknown Record Key = -1):**
   * Bản ghi mặc định `Time_SK = -1`, `Time_ID = 19000101`, `Full_Date = '1900-01-01'`, `Season = 'Unknown'` phục vụ tra cứu Lookup khi ngày diễn ra trận đấu bị khuyết.
3. **Lookup trong SSIS Fact Pipeline:** Trong Data Flow `FACT_Player_Match_Perf`, SSIS ghép nối `Derived_Time_ID` từ cột `date` của lượt ra sân với `Time_ID` của `DIM_Time` để lấy `Time_SK`.

---

## 5. KIỂM THỨC VẸN TOÀN & CHẤT LƯỢNG DỮ LIỆU (DATA INTEGRITY)

* **Tính liên tục (No Gaps):** Đảm bảo không bị đứt đoạn ngày trong toàn bộ chuỗi mùa giải từ 2020 đến 2025.
* **Tối ưu hóa hiệu năng OLAP:** Việc phân rã sẵn các thành phần `Day`, `Month`, `Quarter`, `Year`, `Season`, `Is_Weekend` giúp các câu truy vấn phân tích đa chiều chạy cực nhanh mà không cần tính toán lại biểu thức ngày tháng tại thời điểm `SELECT`.
