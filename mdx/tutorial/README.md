# GIÁO TRÌNH LÝ THUYẾT & THỰC HÀNH TRUY VẤN ĐA CHIỀU MDX (MULTIDIMENSIONAL EXPRESSIONS)

> **Môn học**: Kho Dữ Liệu & Phân Tích Dữ Liệu Lớn (Data Warehouse & OLAP)  
> **Hệ quản trị áp dụng**: Microsoft SQL Server Analysis Services (SSAS Multidimensional)  
> **Cube thực hành**: `[DW Football Transfermarkt]`  
> **Tài liệu tham khảo chính**: Microsoft OLE DB for OLAP Specification, Fast Track to MDX, The Definitive Guide to DAX/MDX.

---

## 📖 DANH MỤC 11 CHƯƠNG CHUYÊN ĐỀ LÝ THUYẾT & VÍ DỤ NÂNG CAO

Giáo trình được module hóa thành **11 chương chuyên đề độc lập**, mỗi chương đều chứa giải thích cặn kẽ bản chất toán học, sơ đồ trực quan, phân tích cú pháp chi tiết, **ví dụ mã MDX phức tạp thực tế** và **bảng kết quả dự kiến (Expected Output Table)** bóc tách đầy đủ mọi trường hợp biên:

| Chương | Tên Chuyên Đề | Kỹ thuật & Hàm MDX Trọng Tâm | Bài Toán Nghiệp Vụ Thực Tế |
| :---: | :--- | :--- | :--- |
| **01** | [Chương 01: Tổng quan về Ngôn ngữ MDX & Mô hình Siêu khối](01_tong_quan_mdx.md) | `Hypercube`, `Sparsity`, `Curse of Dimensionality` | Ma trận hiệu năng tấn công bóc tách đồng thời 4 góc nhìn CLB, Mùa giải, Tuyến thi đấu và Độ đo. |
| **02** | [Chương 02: 8 Khái niệm Cốt lõi trong Mô hình Đa chiều](02_khai_niem_cot_loi.md) | `Cube`, `Dim`, `Hierarchy`, `Member [All]`, `Tuple`, `Set`, `Cell` | So sánh đóng góp bàn thắng cá nhân của Haaland và Mbappe với tổng số toàn CLB và toàn cầu. |
| **03** | [Chương 03: So sánh Chuyên sâu: SQL (Quan hệ) vs MDX (Đa chiều)](03_so_sanh_sql_vs_mdx.md) | Đối chiếu 10 tiêu chí học thuật, `SELECT-FROM-WHERE` | Cùng một bài toán phân tích giải Cúp: Đối chiếu T-SQL (Window Functions + PIVOT) vs MDX. |
| **04** | [Chương 04: Cấu trúc Cú pháp Cơ bản & Trục Tọa độ (Axes & Slicer)](04_cu_phap_co_ban_va_truc_toa_do.md) | `AXIS(0)`, `AXIS(1)`, `Slicer WHERE`, `NON EMPTY` | Báo cáo ma trận 3 CLB London, kiểm chứng triệt tiêu ô thưa (`NON EMPTY`) và triệt tiêu cặp kết hợp vô lý. |
| **05** | [Chương 05: Thành viên Tính toán & Tập hợp Đặt tên (`WITH MEMBER/SET`)](05_thanh_vien_tinh_toan_with_member_set.md) | `WITH MEMBER`, `WITH SET`, `FORMAT_STRING`, `SOLVE_ORDER` | Hệ thống tính điểm kỷ luật quy đổi, chỉ số đóng góp trên 90 phút (P90) và Calculated Member trên Dimension. |
| **06** | [Chương 06: Điều hướng Phân cấp & Quan hệ Cây (Hierarchical Navigation)](06_dieu_huong_phan_cap_hierarchical_navigation.md) | `.Children`, `.Parent`, `Descendants()`, Cờ `SELF_AND_BEFORE` | Báo cáo phân cấp thời gian đa tầng (Năm $\to$ Quý $\to$ Tháng) kết hợp bóc tách vị trí tiền đạo con. |
| **07** | [Chương 07: Phân tích Chuỗi Thời gian (Time Series / Time Intelligence)](07_chuoi_thoi_gian_time_intelligence.md) | `.PrevMember`, `ParallelPeriod()`, `YTD()`, `QoQ`, `YoY` | Bảng theo dõi phong độ Real Madrid qua 8 quý liên tiếp: Tăng trưởng QoQ, YoY và tích lũy YTD. |
| **08** | [Chương 08: Đại số Tập hợp & Xử lý Không gian Đa chiều (Set Algebra)](08_dai_so_tap_hop_set_algebra.md) | `CROSSJOIN (*)`, `UNION (+)`, `INTERSECT`, `EXCEPT (-)` | Nhận diện các "Đội bóng ưu tú toàn diện": Giao tập hợp Top sân nhà/khách và loại trừ đội bạo lực thẻ đỏ. |
| **09** | [Chương 09: Lọc Dữ liệu & Sắp xếp (Filtering & Sorting)](09_loc_va_sap_xep_filter_order.md) | `FILTER()` đa điều kiện, `ORDER()` với `ASC`, `DESC`, `BDESC` | Phân tích cầu thủ tấn công kỷ luật cao; đối chiếu thực nghiệm giữa sắp xếp có thứ bậc (`DESC`) và phẳng (`BDESC`). |
| **10** | [Chương 10: Xếp hạng Đầu - Cuối, Nguyên lý Pareto & Hàm `GENERATE()`](10_xep_hang_pareto_generate_ranking.md) | `TOPCOUNT`, `TOPPERCENT` (Pareto 80/20), `GENERATE()` | Giải quyết triệt để bài toán *"Top 2 chân sút xuất sắc nhất của TỪNG câu lạc bộ"* bằng vòng lặp `GENERATE`. |
| **11** | [Chương 11: Các Hàm Thống kê & Biểu thức Logic Nghiệp vụ](11_thong_ke_va_logic_nghiep_vu.md) | `AVG`, `MAX`, `MIN`, `DISTINCTCOUNT`, `EXISTING`, `CASE WHEN` | Thống kê thể hình (Chiều cao Min/Max/TB) và phân hạng năng lực chuyên môn bằng `CASE WHEN` đa nhánh. |

---

## 🎯 HƯỚNG DẪN SỬ DỤNG VÀ THỰC THI TRONG BÁO CÁO

1. **Khi viết báo cáo môn học / thuyết trình**:
   - Mỗi chương có thể được sử dụng làm một phần lý thuyết hoàn chỉnh trong chương Báo cáo Thực hiện MDX.
   - Có thể sao chép trực tiếp các bảng kết quả giả lập và sơ đồ khối minh họa vào bài viết.
2. **Khi thực thi mã trên SQL Server Management Studio (SSMS)**:
   - Mở SSMS, kết nối tới SSAS (Analysis Services).
   - Chuột phải vào Cube `[DW Football Transfermarkt]`, chọn **New Query** $\to$ **MDX**.
   - Sao chép toàn bộ khối mã MDX trong từng chương tương ứng và nhấn **F5 (Execute)** để đối chiếu kết quả trực quan trên OLAP Grid.
