# Truy vấn OLAP và báo cáo

## Các câu hỏi nên giữ

| Câu hỏi | Cách đối chiếu |
| --- | --- |
| Top cầu thủ ghi bàn theo giải và mùa | Cộng `Goals` từ fact, nhóm theo `Player_ID` và lọc mùa từ `DIM_Game`. |
| Kiến tạo theo vị trí | Cộng `Assists` theo vị trí trong hồ sơ cầu thủ. Mô tả kết quả theo vị trí ghi trong hồ sơ nguồn. |
| Đóng góp bàn thắng trên 90 phút | Tính `90.0 × (SUM(Goals) + SUM(Assists)) / SUM(Minutes_Played)` trong ngữ cảnh lọc hiện tại. Trả về trống khi tổng phút bằng 0. |
| Thành tích sân nhà và sân khách | Tổng hợp trên các dòng fact đã xác định được vai trò CLB trong trận. |
| Xu hướng bàn thắng theo thời gian | Drill-down theo năm, quý, tháng và ngày. Dùng khóa tháng có năm đi kèm để phân biệt tháng của các năm khác nhau. |

Với phạm vi rút gọn, bỏ câu 8 về đá chính và câu 11–13 nếu cắt sức chứa, HLV và quy mô đội hình. Số câu ở đây theo mục 1.3 của Chương 1 đã rà soát. Nếu giữ câu về HLV, lấy HLV theo từng đội từ `games.home_club_manager_name` và `games.away_club_manager_name`.

## Kiểm tra đúng cấp độ tổng hợp

- Đếm lượt ra sân bằng số dòng fact. Khi câu hỏi yêu cầu đếm trận hoặc cầu thủ từ fact, dùng distinct count theo `Game_ID` hoặc `Player_ID`.
- Câu 14 về trận có ít nhất 5 bàn phải kiểm tra một dòng mỗi trận trong `DIM_Game`. Nếu cần tổng bàn chính thức của một CLB theo đối thủ như câu 10, chọn bàn của đội chủ nhà hoặc đội khách theo mã CLB, rồi cộng mỗi trận một lần. `SUM(Goals)` của fact thống kê bàn ghi nhận cho cầu thủ.
- Đối chiếu SQL với cube trên cùng giải, mùa và bộ lọc. Kiểm tra một trận có nhiều lượt ra sân để xác nhận số trận vẫn là 1. Nếu giữ phân tích chiều cao, tính trung bình theo cầu thủ duy nhất trong tập lọc và bỏ giá trị thiếu.

## Cập nhật Chương 1

- Ghi rõ cấp độ chi tiết của fact và các chiều dưới sơ đồ. Đồng bộ danh sách cột, kiểu dữ liệu và câu hỏi với phiên bản thực sự được nạp vào cube.
- Ghi rõ phiên bản hoặc ngày tải Kaggle và 5 tệp CSV dùng trong ETL gồm `appearances`, `players`, `clubs`, `competitions`, `games`. `DIM_Time` được sinh từ ngày thi đấu. Nếu còn nhắc `club_games`, mô tả đúng `hosting` là sân nhà hoặc sân khách và `is_win` là cờ thắng.
- Nếu phần mục tiêu còn đề cập định giá cầu thủ, thu gọn mục tiêu đó khỏi phạm vi hiện tại. Phân tích giá trị thị trường theo thời gian cần dữ liệu `player_valuations` có ngày định giá.
