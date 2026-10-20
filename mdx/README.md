# BỘ CÂU TRUY VẤN NGHIỆP VỤ ĐA CHIỀU MDX (MULTIDIMENSIONAL EXPRESSIONS)

Tài liệu này tổng hợp danh sách các câu truy vấn nghiệp vụ đa chiều (MDX Queries) được thiết kế và tối ưu riêng cho **Cube `[DW Football Transfermarkt]`** (thuộc hệ thống Kho dữ liệu bóng đá Châu Âu `DW_Football_Analytics`).

Các truy vấn được chuyển đổi tương đương và nâng cao từ 15 câu truy vấn T-SQL tại [docs/15_queries.md](file:///d:/Kho_du_lieu_OLAP/docs/15_queries.md), tận dụng triệt để kiến trúc OLAP phân cấp đa chiều, tiền tính toán (Pre-aggregations), Bitmap Indexing và Block Computation của Microsoft SQL Server Analysis Services (SSAS).

Theo yêu cầu môn học (tối thiểu 10 câu truy vấn), nhóm đã tinh chọn **10 câu truy vấn xuất sắc nhất** đại diện cho đầy đủ các phép toán OLAP và kỹ thuật MDX chuyên sâu để đưa vào báo cáo nghiệm thu chính thức. Các câu còn lại được lưu trữ tại thư mục [archive/](file:///d:/Kho_du_lieu_OLAP/mdx/archive/).

---

## 📚 GIÁO TRÌNH LÝ THUYẾT & NỀN TẢNG MDX (TUTORIAL)

Để nắm vững toàn bộ kiến trúc không gian siêu khối, cú pháp toán học, phân biệt chuyên sâu giữa SQL vs MDX, cơ chế Formula Engine/Storage Engine và bộ câu hỏi phản biện lý thuyết, vui lòng xem tài liệu chi tiết tại:
👉 **[mdx/tutorial/README.md](file:///d:/Kho_du_lieu_OLAP/mdx/tutorial/README.md)**: **Giáo trình Lý thuyết & Thực hành Truy vấn Đa chiều MDX từ A đến Z**

---

## 🌟 BẢNG TỔNG HỢP 10 CÂU TRUY VẤN MDX CHÍNH THỨC NỘP BÁO CÁO

| STT | File Tài Liệu | Mục tiêu nghiệp vụ MDX | Thao tác OLAP | Các hàm MDX cốt lõi |
| :---: | :--- | :--- | :---: | :--- |
| **01** | [query_01.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_01.md) | Top 10 Vua dội bom Ngoại Hạng Anh mùa 2023/2024 | **Slice & Pivot** | `TOPCOUNT`, `NON EMPTY`, `MEMBERS` |
| **02** | [query_03.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_03.md) | Cầu thủ xuất sắc có trên 20 đóng góp bàn thắng (G+A > 20) | **Slice & Filter** | `FILTER`, `ORDER (BDESC)`, `WITH MEMBER` |
| **03** | [query_04.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_04.md) | Hiệu suất bàn thắng & số phút TB theo 3 thế hệ độ tuổi | **Calculated Logic** | `WITH MEMBER`, cấu trúc `CASE WHEN`, `AVG` |
| **04** | [query_05.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_05.md) | So sánh bàn thắng theo chân thuận & vị trí chi tiết | **Dice & Union** | Phép hợp tập hợp `UNION`, `CROSSJOIN` |
| **05** | [query_06.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_06.md) | Chiều cao trung bình, bàn thắng và thẻ phạt theo vị trí chính | **Aggregate Analysis** | `AVG`, `MAX`, `MIN`, `EXISTING`, `ORDER` |
| **06** | [query_07.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_07.md) | Bàn thắng theo quốc tịch theo nguyên lý Pareto 80/20 | **Pareto Ranking** | `TOPPERCENT`, `ORDER (BDESC)` |
| **07** | [query_09.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_09.md) | Hiệu năng Sân nhà vs Sân khách x Cuối tuần vs Ngày thường | **Dice & Intersect** | Phép giao tập hợp `INTERSECT`, `CROSSJOIN` |
| **08** | [query_10.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_10.md) | Bàn thắng Real Madrid & tăng trưởng qua các Quý (QoQ) | **Time Intelligence** | `PREVMEMBER`, `DESCENDANTS`, Time Hierarchy |
| **09** | [query_11.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_11.md) | Số trận đấu tại các SVĐ có sức chứa > 60.000 khán giả | **Cleansing & Distinct** | `COALESCEEMPTY`, `DISTINCTCOUNT`, `EXISTING` |
| **10** | [query_12.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_12.md) | Tháng nhận thẻ phạt kỷ lục phân theo Huấn luyện viên trưởng | **Advanced Group-by** | `GENERATE`, `TOPCOUNT` lồng nhau |

---

## 📦 KHO LƯU TRỮ CÁC CÂU TRUY VẤN DỰ PHÒNG (ARCHIVE)

Các câu truy vấn nghiên cứu bổ trợ không nằm trong 10 câu chính thức được lưu trữ an toàn tại thư mục [mdx/archive/](file:///d:/Kho_du_lieu_OLAP/mdx/archive/):

* [query_02.md](file:///d:/Kho_du_lieu_OLAP/mdx/archive/query_02.md): Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG (`TOPCOUNT`, `CROSSJOIN`).
* [query_08.md](file:///d:/Kho_du_lieu_OLAP/mdx/archive/query_08.md): Danh sách các "Siêu dự bị" ghi bàn nhiều nhất khi vào sân thay người (`TOPCOUNT`, `BOTTOMCOUNT`).
* [query_13.md](file:///d:/Kho_du_lieu_OLAP/mdx/archive/query_13.md): Khảo sát lực lượng cầu thủ thực tế ra sân theo quy mô đội hình (`DISTINCTCOUNT`, `EXISTING`).
* [query_14.md](file:///d:/Kho_du_lieu_OLAP/mdx/archive/query_14.md): Thống kê các trận cầu mưa bàn thắng ($\ge 5$ bàn) qua các vòng đấu (`FILTER`, `CROSSJOIN`).
* [query_15.md](file:///d:/Kho_du_lieu_OLAP/mdx/archive/query_15.md): Theo dõi phong độ & thẻ phạt của lứa cầu thủ trẻ (sinh từ 2004) theo ngày (`WITH SET`, `PROPERTIES`).

---

## HƯỚNG DẪN THỰC THI TRÊN SQL SERVER ANALYSIS SERVICES (SSAS)

1. **Khởi động SQL Server Management Studio (SSMS):**
   * Server Type: Chọn **Analysis Services**.
   * Server Name: Nhập địa chỉ máy chủ SSAS của bạn (ví dụ: `localhost` hoặc `DESKTOP-XXX\SSAS`).
   * Authentication: Windows Authentication.
2. **Chọn Database & Cube:**
   * Trong cửa sổ **Object Explorer**, mở rộng nhánh `Databases` $\to$ Chọn database triển khai Cube (ví dụ: `SSAS_Football_Transfermarkt`).
   * Mở rộng nhánh `Cubes` $\to$ Chuột phải vào Cube **`DW Football Transfermarkt`** $\to$ Chọn **New Query** $\to$ **MDX**.
3. **Thực thi truy vấn:**
   * Mở từng file trong thư mục `mdx/` (từ `query_01.md` đến `query_12.md`), sao chép đoạn mã trong mục **Mã truy vấn MDX chuẩn**.
   * Dán vào cửa sổ Editor của SSMS và nhấn **Execute (F5)**.
   * Kết quả sẽ được hiển thị ngay lập tức dưới dạng lưới ma trận ô dữ liệu (OLAP Grid).

---

## 📑 BÁO CÁO KIỂM ĐỊNH HỌC THUẬT & ĐỐI CHIẾU HÀM MDX (QUALITY CHECKLIST)

Toàn bộ hệ thống truy vấn đã được kiểm định khắt khe tại tài liệu:
👉 **[checklist.md](file:///d:/Kho_du_lieu_OLAP/mdx/checklist.md)**: **Bảng đối chiếu & Kiểm định chất lượng các câu truy vấn MDX**
