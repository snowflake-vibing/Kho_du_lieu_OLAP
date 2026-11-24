# 4.2 Tạo ba báo biểu bằng Power BI

Mở [tệp báo biểu PBIX](../power-bi/Kho_du_lieu_OLAP.pbix) với kết nối SSAS đang hoạt động. Các trường dưới đây bám theo cấu hình của tệp. Dùng khoảng ngày 2022–2024 khi đối chiếu với bản xuất Looker Studio.

## Báo biểu 1. Cơ cấu giải đấu và hiệu suất thi đấu

**Câu hỏi nghiệp vụ.** Bàn thắng, kiến tạo, phút thi đấu và thẻ phân bố thế nào theo giải đấu và thời gian?

| Thành phần | Cấu hình |
| --- | --- |
| Thẻ KPI | Số trận phân biệt, số HLV, bàn thắng, kiến tạo |
| Thanh xếp chồng | Phân cấp loại giải → quốc gia → giải → vòng. Giá trị là bàn thắng và kiến tạo. |
| Cột xếp chồng kết hợp đường | Phân cấp năm → quý → tháng → ngày. Cột là bàn thắng và kiến tạo. Đường là phút thi đấu, dùng trục phụ. |
| Ma trận | Hàng theo giải → CLB → cầu thủ. Giá trị gồm số trận phân biệt, phút, thẻ đỏ và thẻ vàng. |
| Bộ lọc | Giải, quốc gia của giải, CLB, cầu thủ |

Chọn một giải rồi khoan xuống vòng đấu. Kiểm tra ma trận ở cấp cầu thủ và đối chiếu số trận phân biệt ở cấp giải.

## Báo biểu 2. Đóng góp tấn công theo CLB và cầu thủ

**Câu hỏi nghiệp vụ.** CLB và cầu thủ nào đóng góp nhiều bàn thắng hoặc kiến tạo trong phạm vi lọc? Số bàn thay đổi ra sao theo sân và thời gian?

| Thành phần | Cấu hình |
| --- | --- |
| Thẻ KPI | Số trận phân biệt, kiến tạo, bàn thắng, phút thi đấu |
| Thanh xếp chồng | Trục CLB, giá trị bàn thắng và kiến tạo |
| Cột kết hợp đường | Trục sân thi đấu, cột số trận phân biệt, đường số bàn thắng |
| Biểu đồ vùng | Dùng trường tháng và năm với số bàn thắng. Khi phân tích xu hướng liên tục, sắp theo năm rồi tháng hoặc dùng trường năm-tháng. |
| Bảng cầu thủ | Tên, tuổi, chân thuận, quốc tịch, kiến tạo, bàn thắng |
| Bộ lọc | Cầu thủ, CLB, mùa giải, tháng |

Khi trình bày Top 10 CLB, đặt bộ lọc Top N theo độ đo `Goal Contributions` và ghi rõ tiêu chí xếp hạng. Đọc tổng bàn thắng theo sân cùng với số trận tại sân đó.

## Báo biểu 3. Kỷ luật và khối lượng thi đấu

**Câu hỏi nghiệp vụ.** Thẻ phạt tập trung ở CLB và vị trí nào? Tổng phút thi đấu và thẻ vàng thay đổi ra sao theo độ tuổi?

| Thành phần | Cấu hình |
| --- | --- |
| Thẻ KPI | Thẻ vàng, thẻ đỏ, lượt ra sân, tổng phút thi đấu |
| Thanh xếp chồng | CLB theo số thẻ vàng và thẻ đỏ |
| Vùng xếp chồng | Mùa giải và tháng trên trục thời gian, đóng góp bàn thắng phân theo CLB |
| Cột kết hợp đường | Tuổi trên trục ngang, cột tổng phút thi đấu, đường tổng thẻ vàng |
| Vành khuyên | Tổng thẻ đỏ theo vị trí chi tiết |
| Bộ lọc | Cầu thủ, giải, mùa giải, vị trí chi tiết |

Biểu đồ vùng trong PBIX đo đóng góp bàn thắng. Để phân tích khối lượng theo thời gian, có thể bổ sung biểu đồ tháng với tổng phút thi đấu. Để so sánh CLB có khối lượng thi đấu khác nhau, có thể bổ sung tỷ lệ thẻ trên 90 phút và hiển thị tổng phút làm mẫu số.
