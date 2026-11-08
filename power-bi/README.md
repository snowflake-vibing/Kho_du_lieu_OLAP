# CHƯƠNG 4: BÁO CÁO VÀ TRỰC QUAN HÓA DỮ LIỆU (POWER BI & LOOKER STUDIO)

Thư mục này chứa toàn bộ tài liệu hướng dẫn chi tiết quy trình chuẩn bị công cụ và thiết kế hệ thống báo biểu trực quan hóa dữ liệu theo chuẩn môn học **IS217 - Kho dữ liệu và OLAP**, tham chiếu từ đề tài mẫu `[27]_IS217Q13_23520698_23521417.pdf`.

---

## Danh mục tài liệu hướng dẫn

| STT | Tên tài liệu | Nội dung chính | Công cụ sử dụng |
| :---: | :--- | :--- | :---: |
| **01** | [01_chuan_bi_cong_cu_ket_noi.md](file:///d:/Kho_du_lieu_OLAP/power-bi/01_chuan_bi_cong_cu_ket_noi.md) | Cài đặt Power BI Desktop; Thiết lập Live Connection tới SSAS Cube; Xuất dữ liệu kho ra file CSV phẳng và nạp vào Google Data Studio | Power BI Desktop, SSMS, Looker Studio |
| **02** | [02_power_bi_bao_bieu_1.md](file:///d:/Kho_du_lieu_OLAP/power-bi/02_power_bi_bao_bieu_1.md) | **Báo biểu 1:** Thống kê tổng hợp số lượng, quy mô và xu hướng phân bổ theo vị trí và phân loại (Matrix, 2 Pie Charts, Clustered Column Chart) | Power BI Desktop (Live Connection SSAS) |
| **03** | [03_power_bi_bao_bieu_2.md](file:///d:/Kho_du_lieu_OLAP/power-bi/03_power_bi_bao_bieu_2.md) | **Báo biểu 2:** Phân tích chi tiết biến động theo chuỗi thời gian và khung giờ (Matrix, Donut Chart, Line Chart với 2 Average Lines) | Power BI Desktop (Live Connection SSAS) |
| **04** | [04_power_bi_bao_bieu_3.md](file:///d:/Kho_du_lieu_OLAP/power-bi/04_power_bi_bao_bieu_3.md) | **Báo biểu 3:** Phân tích theo nhóm tuổi khách hàng và loại thiết bị thực hiện (Funnel Chart, Clustered Bar Chart, Line & Clustered Column Chart) | Power BI Desktop (Live Connection SSAS) |
| **05** | [05_looker_studio_bao_bieu.md](file:///d:/Kho_du_lieu_OLAP/power-bi/05_looker_studio_bao_bieu.md) | **Báo biểu Looker Studio (Google Data Studio):** Xây dựng 3 báo biểu web, cấu hình bộ lọc kết hợp, trường tính toán `CONCAT(...)`, và tính năng Drill-down | Google Data Studio (Looker Studio Web) |

---

## Điểm nhấn kỹ thuật nổi bật
1. **Live Connection tới SSAS Cube:** Tận dụng triệt để các Calculated Member, Named Sets, và Hierarchies đã được xây dựng và kiểm định từ khối OLAP.
2. **Kỹ thuật Drill-down đa cấp:** Cho phép người dùng linh hoạt xem dữ liệu từ mức tổng quan (Bang/Năm) tới chi tiết (Thành phố/Ngày/Giờ).
3. **Analytics Lines:** Tích hợp đường trung bình chuẩn (Average Line) trên biểu đồ đường giúp người quản trị phát hiện ngay các bất thường và đột biến dữ liệu.
