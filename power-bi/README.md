# CHƯƠNG 4: BÁO CÁO VÀ TRỰC QUAN HÓA DỮ LIỆU BÓNG ĐÁ CHÂU ÂU (POWER BI & LOOKER STUDIO)

Thư mục này chứa toàn bộ tài liệu hướng dẫn chi tiết quy trình chuẩn bị công cụ và thiết kế hệ thống báo biểu trực quan hóa dữ liệu cho **Kho dữ liệu Bóng đá Châu Âu (Football Transfermarkt Data Warehouse)** theo chuẩn môn học **IS217 - Kho dữ liệu và OLAP**, tham chiếu phương pháp luận từ đề tài mẫu `[6]_IS217Q11_23520009_23520753.pdf`.

---

## Danh mục tài liệu hướng dẫn

| STT | Tên tài liệu | Nội dung chính | Khối dữ liệu áp dụng |
| :---: | :--- | :--- | :---: |
| **01** | [01_chuan_bi_cong_cu_ket_noi.md](file:///d:/Kho_du_lieu_OLAP/power-bi/01_chuan_bi_cong_cu_ket_noi.md) | Cài đặt Power BI Desktop; Thiết lập Live Connection trực tiếp tới Cube `[DW Football Transfermarkt]`; Xuất dữ liệu phẳng từ `DW_Football` ra file CSV và nạp vào Google Data Studio | Power BI Desktop, SSMS, Looker Studio |
| **02** | [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md) | **Báo biểu 1:** Hiệu suất Ghi bàn & Kiến tạo: 4 KPI Cards, Slicers; lưới 2x2: Top 10 Chân sút, Scatter 4 góc phần tư, Hierarchical Treemap Drill-down, Matrix + Data Bars | Cube `[DW Football Transfermarkt]` |
| **03** | [03_power_bi_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/power-bi/03_power_bi_bao_bieu_2.md) | **Báo biểu 2:** Đối đầu Trực tiếp & Kỳ phùng Địch thủ (`DIM Club` vs `Opponent Club` - Truy vấn 10 Role-Playing Dimension): 4 KPI Cards, Slicers; lưới 2x2: Top 10 Đối thủ bị thủng lưới nhiều nhất, Scatter Ma trận khắc chế đối đầu, Cột cụm lịch sử đối đầu theo mùa, Ma trận đối đầu chéo Head-to-Head Heatmap | Cube `[DW Football Transfermarkt]` |
| **04** | [04_power_bi_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/power-bi/04_power_bi_bao_bieu_3.md) | **Báo biểu 3:** Kỷ luật & Tải trọng: 4 KPI Cards, Slicers; lưới 2x2: Top 10 CLB nhiều thẻ, Scatter Ma trận rủi ro kỷ luật, Combo 2 trục theo Độ tuổi, Matrix + Heatmap | Cube `[DW Football Transfermarkt]` |
| **05** | [05_looker_studio_bao_bieu.md](file:///d:/Kho_du_lieu_OLAP/power-bi/05_looker_studio_bao_bieu.md) | **Báo biểu Looker Studio (Google Data Studio):** 3 báo biểu trực tuyến trên nền web, cấu hình bộ lọc chân sút chủ lực, bảng tổng hợp phân cấp và tính năng khoan sâu Drill-down từ Quốc gia xuống CLB | Tệp `Football_Report_Data.csv` trên Looker Studio |
| **Theme** | [theme_rule_md.json](file:///d:/Kho_du_lieu_OLAP/power-bi/theme_rule_md.json) | **File Theme tự động:** Nạp vào Power BI Desktop (Tab `View` $\rightarrow$ `Browse for themes`) để áp dụng tự động toàn bộ cỡ chữ (Title 18pt, KPI 35pt, Axis 12pt) và bo viền 10px | Power BI Desktop Theme |

---

## Quy chuẩn thiết kế chung (theo [rule.md](../rule.md))
* **Canvas:** 1920 x 1080 px, nền `#F8FAFC`; mọi visual nền `#FFFFFF`, viền `#CBD5E1`, bo góc 10 px.
* **Bố cục 2 tầng:** Tầng trên = Title + KPI Cards + Slicers (H = 75 - 80 px thoáng đãng, không bị cụt dropdown/tile); Tầng dưới = 4 biểu đồ nâng cao linh hoạt diện tích trực quan.
* **Cỡ chữ:** Title trang 20 pt · Title visual 18 pt Bold · Giá trị Callout Card 35 pt Bold (cực kỳ nổi bật) · Dữ liệu/trục/nhãn 12 pt.
* **Màu:** Card nền pastel sáng, chữ đen; trục danh mục và trục số đo dùng màu khác nhau.
* **Không có dấu ba chấm (`...`)** ở bất kỳ visual nào.

---

## Điểm nhấn kỹ thuật nổi bật
1. **Kết nối trực tiếp SSAS Cube (Live Connection):** Khai thác toàn bộ các thước đo tính toán độc lập tự chủ (`QoQ Goals Growth`, `Mins Per Goal`, `Goal Contributions`) và hệ thống phân cấp thời gian (`Year` -> `Quarter` -> `Month` -> `Day`).
2. **Kỹ thuật Drill-down và Cross-Filtering:** Toàn bộ các visual tương tác đồng bộ tức thời khi người dùng nhấp chọn mùa giải, giải đấu hoặc vị trí thi đấu.
3. **Thiết kế báo cáo đa chiều chuẩn doanh nghiệp:** Kết hợp hài hòa giữa thẻ chỉ số KPI tổng quan, biểu đồ xu hướng thời gian và bảng ma trận chi tiết dòng.
