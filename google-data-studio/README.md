# HƯỚNG DẪN THIẾT KẾ BÁO BIỂU TRÊN GOOGLE DATA STUDIO (LOOKER STUDIO)
> **Dự án:** Kho dữ liệu Bóng đá Châu Âu (European Football Transfermarkt Data Warehouse)  
> **Môn học:** IS217 - Kho dữ liệu và OLAP  
> **Nền tảng:** Google Data Studio (Looker Studio Cloud)  
> **Nguồn dữ liệu:** `Football_Report_Data.csv` (Xuất phẳng từ Kho dữ liệu `DW_Football`)

---

## 1. Giới thiệu Tổng quan

Thư mục `google-data-studio/` cung cấp tài liệu hướng dẫn thiết kế hoàn chỉnh hệ thống **3 Báo biểu Trực quan hóa Dữ liệu (Executive Dashboards)** trên nền tảng đám mây **Google Data Studio (Looker Studio)**, đối ứng $100\%$ và đồng bộ tuyệt đối với hệ thống 3 báo biểu trên **Power BI Desktop**:

1. **Báo biểu 1 (Chuẩn Grouping & Totals):** [01_looker_studio_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/01_looker_studio_bao_bieu_1.md) — Phân tích Hiệu suất Ghi bàn & Đóng góp Kiến tạo, tích hợp **Báo cáo Phân nhóm và Tổng hợp Đa cấp (Pivot Table with Subtotals & Grand Total: Giải đấu $\rightarrow$ CLB $\rightarrow$ Cầu thủ)** đáp ứng trọn vẹn tiêu chí bắt buộc của đề bài.
2. **Báo biểu 2:** [02_looker_studio_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/02_looker_studio_bao_bieu_2.md) — Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh (Scouting Elite Clubs & Top Offensive Threats): Top 10 CLB hỏa lực, Thánh địa Sân vận động bùng nổ, Dòng thời gian chu kỳ và Bảng Trinh sát đặc tính mũi nhọn (Quốc tịch, Vị trí, Chân thuận, Tuổi, Bàn thắng, Kiến tạo, G+A Data Bars).
3. **Báo biểu 3:** [03_looker_studio_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/03_looker_studio_bao_bieu_3.md) — Kỷ luật Thẻ phạt & Tải trọng Thi đấu (Discipline & Physical Workload): Top 10 CLB nhận thẻ, Biến động tải trọng phút thi đấu qua các mùa giải, Tương quan Thể lực vs Thẻ phạt theo Độ tuổi, và Phân bổ Thẻ đỏ theo Vị trí chi tiết.

---

## 2. Quy trình Xuất Dữ liệu Phẳng từ SQL Server ra CSV

Do Google Data Studio hoạt động trên đám mây của Google và không kết nối trực tiếp với SSAS Multidimensional Cube nội bộ (`localhost`), ta thực hiện xuất bảng dữ liệu phẳng từ CSDL `DW_Football` thông qua SQL Server Management Studio (SSMS).

### Câu lệnh SQL trích xuất dữ liệu:
```sql
USE DW_Football;
GO

SELECT 
    F.Appearance_ID,
    -- Chiều Cầu thủ (DIM_Player)
    P.Player_ID,
    P.Player_Name,
    P.Age,
    P.Main_Position,
    P.Sub_Position,
    P.Foot,
    P.Height_In_Cm,
    P.Country_Of_Citizenship AS Player_Country,
    -- Chiều Câu lạc bộ (DIM_Club)
    C.Club_ID,
    C.Club_Name,
    C.Stadium_Name,
    C.Stadium_Seats,
    C.Coach_Name,
    C.Squad_Size,
    -- Chiều Giải đấu (DIM_Competition)
    Comp.Competition_ID,
    Comp.Competition_Name,
    Comp.Country_Name AS Competition_Country,
    Comp.Competition_Type,
    -- Chiều Thời gian (DIM_Time)
    T.Time_ID,
    T.Full_Date,
    T.Year,
    T.Quarter,
    T.Month,
    T.Day,
    T.Season,
    -- Thước đo định lượng (FACT_Player_Match_Perf)
    F.Minutes_Played,
    F.Goals,
    F.Assists,
    F.Goal_Contributions,
    F.Yellow_Cards,
    F.Red_Cards,
    F.Is_Starter,
    F.Is_Home_Game
FROM FACT_Player_Match_Perf F
INNER JOIN DIM_Player P ON F.Player_ID = P.Player_ID
INNER JOIN DIM_Club C ON F.Club_ID = C.Club_ID
INNER JOIN DIM_Competition Comp ON F.Competition_ID = Comp.Competition_ID
INNER JOIN DIM_Time T ON F.Time_ID = T.Time_ID;
```

### Hướng dẫn lưu file CSV:
1. Nhấp chuột phải vào kết quả truy vấn trong SSMS $\rightarrow$ chọn **Save Results As...**.
2. Lưu tệp với tên: **`Football_Report_Data.csv`** (Encoding UTF-8).
3. Đảm bảo dung lượng và dữ liệu đầy đủ (~155,000 dòng sự kiện thi đấu sạch).

---

## 3. Khởi tạo Báo cáo và Nạp dữ liệu vào Looker Studio

1. Truy cập: [https://lookerstudio.google.com/](https://lookerstudio.google.com/).
2. Chọn **Báo cáo trống (Blank Report)** $\rightarrow$ Chọn trình kết nối **Tải tệp lên (File Upload)**.
3. Chọn tệp `Football_Report_Data.csv` vừa xuất $\rightarrow$ Chờ hệ thống xử lý chuyển sang trạng thái xanh **Đã tải lên (Uploaded)** $\rightarrow$ Bấm **Thêm vào báo cáo (Add to Report)**.
4. **Cấu hình kích thước trang chuẩn Full HD 1920 x 1080 px:**
   * Tại thanh menu trên cùng, chọn **Trang (Page)** $\rightarrow$ **Cài đặt trang hiện tại (Current page settings)**.
   * Chuyển sang tab **Kiểu (Style)** $\rightarrow$ tại mục **Loại hiển thị (Display mode)**: Chọn `Khớp với chiều rộng (Fit to width)`.
   * Tại mục **Kích thước Canvas (Canvas size)**: Chọn `Tùy chỉnh (Custom)`, nhập:
     * **Chiều rộng (Width):** `1920 px`
     * **Chiều cao (Height):** `1080 px`
5. **Màu nền báo cáo:** Chọn màu xám khói hiện đại **`#F8FAFC`** (Slate 50).

---

## 4. Danh mục 3 Báo biểu Chi tiết

| STT | Tệp hướng dẫn | Tên Báo biểu | Điểm nhấn kỹ thuật |
| :---: | :--- | :--- | :--- |
| **01** | [01_looker_studio_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/01_looker_studio_bao_bieu_1.md) | **Hiệu suất Ghi bàn & Kiến tạo (Grouping & Totals Report)** | 4 Scorecards, 2 Controls; thân trang là **2 Bảng Pivot Table with Subtotals đối xứng**: Visual 1 theo Tổ chức (`Competition` -> `Club`) và Visual 2 theo Chiến thuật (`Main Position` -> `Sub Position` -> `Player`), Subtotals & Grand Total ON. |
| **02** | [02_looker_studio_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/02_looker_studio_bao_bieu_2.md) | **Hồ sơ Chiến thuật & Trinh sát Kẻ mạnh** | 4 Scorecards, Top 10 CLB Hỏa lực, Combo Chart Thánh địa Sân vận động (Sức chứa vs Bàn thắng), Area Chart Dòng thời gian, Bảng Trinh sát Cầu thủ với Data Bars (Quốc tịch, Vị trí, Chân thuận, Tuổi). |
| **03** | [03_looker_studio_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/google-data-studio/03_looker_studio_bao_bieu_3.md) | **Kỷ luật Thẻ phạt & Tải trọng Thi đấu** | 4 Scorecards, Stacked Bar Thẻ vàng/Thẻ đỏ theo CLB, Line Chart Biến động tải trọng thể lực qua các mùa giải, Combo Chart Phút & Thẻ theo Độ tuổi, Donut Chart Thẻ đỏ theo Vị trí. |
