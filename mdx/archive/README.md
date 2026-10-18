# KHO LƯU TRỮ CÁC CÂU TRUY VẤN MDX DỰ PHÒNG (ARCHIVE)

Thư mục này lưu trữ **5 câu truy vấn MDX dự phòng / mở rộng** không nằm trong danh sách 10 câu nộp chính thức cho Giảng viên.

Toàn bộ các câu truy vấn này đều đã được xây dựng hoàn thiện theo cấu trúc chuẩn 5 phần (hướng dẫn 3 công cụ Cube Browser, Excel PivotTable, SSMS MDX; bảng kết quả dự kiến; phân tích độ phức tạp thuật toán và đối chiếu kết quả).

---

## DANH SÁCH CÁC CÂU TRUY VẤN LƯU TRỮ

| File | Tên nghiệp vụ & Đề tài phân tích | Kỹ thuật MDX chính | Lý do lưu trữ dự phòng |
| :---: | :--- | :--- | :--- |
| [`query_02.md`](query_02.md) | Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG | `TOPCOUNT`, `CROSSJOIN`, `NON EMPTY` | Tương đồng dạng bài xếp hạng với Query 01; ưu tiên chọn Query 01 và 03 để tối ưu tính đa dạng. |
| [`query_08.md`](query_08.md) | Top 15 "Siêu dự bị" ghi nhiều bàn nhất khi thay người | `TOPCOUNT`, `BOTTOMCOUNT`, Slicing | Dạng bài xếp hạng hai đầu đã có các kỹ thuật tương tự ở các câu xếp hạng khác. |
| [`query_13.md`](query_13.md) | Khảo sát lực lượng cầu thủ theo quy mô đội hình | `DISTINCTCOUNT`, `EXISTING`, Measure Count | Kỹ thuật `DISTINCTCOUNT` đã được thể hiện toàn diện hơn ở Query 11 (kết hợp `COALESCEEMPTY`). |
| [`query_14.md`](query_14.md) | Thống kê các trận cầu mưa bàn thắng ($\ge 5$ bàn) | `FILTER`, `CROSSJOIN`, `ORDER` | Kỹ thuật lọc ngưỡng `FILTER` đã được thể hiện sâu sắc hơn ở Query 03 (kết hợp `ORDER BDESC`). |
| [`query_15.md`](query_15.md) | Theo dõi phong độ & thẻ phạt lứa cầu thủ trẻ theo ngày | `WITH SET`, `PROPERTIES`, `ORDER` | Mang tính chất tra cứu bảng phẳng thuộc tính Member Properties hơn là phân tích tổng hợp đa chiều. |
