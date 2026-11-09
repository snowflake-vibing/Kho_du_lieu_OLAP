# KHO LƯU TRỮ CÁC CÂU TRUY VẤN MDX DỰ PHÒNG (ARCHIVE)

Thư mục này lưu trữ **5 câu truy vấn MDX dự phòng / mở rộng** không nằm trong danh sách 10 câu nộp chính thức cho Giảng viên.

Toàn bộ các câu truy vấn này đều đã được xây dựng hoàn thiện theo cấu trúc chuẩn 5 phần (hướng dẫn 3 công cụ Cube Browser, Excel PivotTable, SSMS MDX; bảng kết quả dự kiến; phân tích độ phức tạp thuật toán và đối chiếu kết quả).

---

## DANH SÁCH CÁC CÂU TRUY VẤN LƯU TRỮ

| File | Tên nghiệp vụ & Đề tài phân tích | Kỹ thuật MDX chính | Lý do lưu trữ dự phòng |
| :---: | :--- | :--- | :--- |
| [`query_02.md`](query_02.md) | Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG | `TOPCOUNT`, `CROSSJOIN`, `NON EMPTY` | Tương đồng dạng bài xếp hạng với Query 01; ưu tiên chọn Query 01 và 03 để tối ưu tính đa dạng. |
| [`query_08.md`](query_08.md) | Top 15 "Sát thủ hiệu suất săn bàn" (thi đấu ít phút nhất để ghi $\ge 15$ bàn) | `BOTTOMCOUNT`, `FILTER`, `WITH MEMBER` | Kỹ thuật xếp hạng ngược `BOTTOMCOUNT` kết hợp thước đo tự tính `[Mins Per Goal]`. |
| [`query_13.md`](query_13.md) | Top 15 CLB có quy mô đội hình lớn nhất và lực lượng cầu thủ thực chiến | `DISTINCTCOUNT`, `EXISTING`, `TOPCOUNT` | Kỹ thuật `DISTINCTCOUNT` đã được thể hiện toàn diện hơn ở Query 11 (kết hợp `COALESCEEMPTY`). |
| [`query_14.md`](query_14.md) | Top 15 trận cầu mưa bàn thắng nhiều nhất qua các vòng đấu | `TOPCOUNT`, `ORDER (BDESC)`, `CROSSJOIN` | Kỹ thuật lọc ngưỡng `FILTER` và sắp xếp `ORDER` đã được thể hiện sâu sắc hơn ở Query 03 và 04. |
| [`query_15.md`](query_15.md) | Top 15 tài năng trẻ sinh từ 01/01/2004 ghi nhiều bàn nhất | `TOPCOUNT`, `FILTER (Date Of Birth)`, `CROSSJOIN` | Phân tích tập trung vào lát cắt độ tuổi và thời gian sinh của lứa cầu thủ trẻ. |
