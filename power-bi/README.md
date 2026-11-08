# CHƯƠNG 4: BÁO CÁO VÀ TRỰC QUAN HÓA DỮ LIỆU BÓNG ĐÁ CHÂU ÂU (POWER BI & LOOKER STUDIO)

Thư mục này chứa toàn bộ tài liệu hướng dẫn chi tiết quy trình chuẩn bị công cụ và thiết kế hệ thống báo biểu trực quan hóa dữ liệu cho **Kho dữ liệu Bóng đá Châu Âu (Football Transfermarkt Data Warehouse)** theo chuẩn môn học **IS217 - Kho dữ liệu và OLAP**, tham chiếu phương pháp luận từ đề tài mẫu `[6]_IS217Q11_23520009_23520753.pdf`.

---

## Danh mục tài liệu hướng dẫn

| STT | Tên tài liệu | Nội dung chính | Khối dữ liệu áp dụng |
| :---: | :--- | :--- | :---: |
| **01** | [01_chuan_bi_cong_cu_ket_noi.md](file:///d:/Kho_du_lieu_OLAP/power-bi/01_chuan_bi_cong_cu_ket_noi.md) | Cài đặt Power BI Desktop; Thiết lập Live Connection trực tiếp tới Cube `[DW Football Transfermarkt]`; Xuất dữ liệu phẳng từ `DW_Football` ra file CSV và nạp vào Google Data Studio | Power BI Desktop, SSMS, Looker Studio |
| **02** | [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md) | **Báo biểu 1:** Phân tích Hiệu suất Ghi bàn và Đóng góp Kiến tạo của Cầu thủ (`Player Performance & Goal Contributions`): 4 KPI Cards, Top 10 Chân sút, Donut Chart vị trí, Combo Chart mùa giải, Matrix chi tiết | Cube `[DW Football Transfermarkt]` |
| **03** | [03_power_bi_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/power-bi/03_power_bi_bao_bieu_2.md) | **Báo biểu 2:** Vận hành Trận đấu, Câu lạc bộ và Tương quan Sân vận động (`Club Match Operations & Stadium Capacity`): Bàn thắng Sân nhà vs Sân khách, Treemap giải đấu, Tương quan sức chứa sân | Cube `[DW Football Transfermarkt]` |
| **04** | [04_power_bi_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/power-bi/04_power_bi_bao_bieu_3.md) | **Báo biểu 3:** Kỷ luật Thẻ phạt, Cường độ Thi đấu và Tải trọng Cầu thủ (`Discipline & Match Load Analysis`): Thẻ vàng, thẻ đỏ, tương quan thời lượng thi đấu và độ tuổi | Cube `[DW Football Transfermarkt]` |
| **05** | [05_looker_studio_bao_bieu.md](file:///d:/Kho_du_lieu_OLAP/power-bi/05_looker_studio_bao_bieu.md) | **Báo biểu Looker Studio (Google Data Studio):** 3 báo biểu trực tuyến trên nền web, cấu hình bộ lọc chân sút chủ lực, bảng tổng hợp phân cấp và tính năng khoan sâu Drill-down từ Quốc gia xuống CLB | Tệp `Football_Report_Data.csv` trên Looker Studio |

---

## Điểm nhấn kỹ thuật nổi bật
1. **Kết nối trực tiếp SSAS Cube (Live Connection):** Khai thác toàn bộ các thước đo tính toán độc lập tự chủ (`QoQ Goals Growth`, `Mins Per Goal`, `Goal Contributions`) và hệ thống phân cấp thời gian (`Year` -> `Quarter` -> `Month` -> `Day`).
2. **Kỹ thuật Drill-down và Cross-Filtering:** Toàn bộ các visual tương tác đồng bộ tức thời khi người dùng nhấp chọn mùa giải, giải đấu hoặc vị trí thi đấu.
3. **Thiết kế báo cáo đa chiều chuẩn doanh nghiệp:** Kết hợp hài hòa giữa thẻ chỉ số KPI tổng quan, biểu đồ xu hướng thời gian và bảng ma trận chi tiết dòng.
