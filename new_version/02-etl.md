# Tiền xử lý và nạp dữ liệu

## Ánh xạ từ CSV

- Lọc `games.csv` theo danh sách 13 giải và `season IN (2022, 2023)`. Lấy các lượt ra sân có `game_id` thuộc tập trận đã lọc.
- Giữ `game_id`, `date`, `competition_id` và `season` trong dữ liệu trận đã làm sạch. Tra cứu theo `game_id` để lấy ngày và giải cho fact. Đối chiếu ngày, giải trên `appearances` với `games`; ghi số dòng lệch và kiểm tra mẫu trước khi nạp.
- Sinh `DIM_Time` từ tập ngày duy nhất của các trận đã chọn. Nạp các bảng chiều trước khi nạp fact.
- Bảo toàn `appearance_id` dạng chuỗi từ nguồn đến `Source_Appearance_ID`. Kiểm tra khóa nguồn rỗng và khóa lặp trước khi nạp. Với khóa lặp có số liệu khác nhau, giữ lại để kiểm tra nguyên nhân trước khi chọn bản ghi.
- Lấy `Club_ID` từ `appearances.player_club_id`. So với `Home_Club_ID` và `Away_Club_ID` để xác định đối thủ và vai trò sân nhà hoặc sân khách. Nếu mã CLB không khớp cả hai đội, ghi nhận sai lệch và để trống các trường suy ra.
- Bỏ `Is_Starter` trong phạm vi rút gọn. [Tài liệu fact hiện tại](../docs/fact_player_match_perf.md) dùng ngưỡng 60 phút, nhưng cầu thủ đá chính có thể rời sân sớm. Nếu vẫn giữ câu hỏi này, nối [`game_lineups`](https://github.com/dcaribou/transfermarkt-datasets/blob/master/transfermarkt_datasets/assets/cur_game_lineups.py) theo mã trận, cầu thủ và CLB. Để `NULL` khi thiếu bản ghi đội hình.

## Giá trị thiếu và đối soát

- Giữ `NULL` cho ngày sinh, chiều cao, sức chứa, quy mô đội hình hoặc tỷ số bị thiếu. Loại các giá trị điền thay như `1999-01-01`, `180 cm` và `25` khỏi luồng nạp. Giá trị 0 chỉ có ý nghĩa khi nguồn xác nhận 0.
- Đối soát số dòng hợp lệ, số dòng loại và lý do từ chối. Đếm khóa fact trùng, khóa ngoại không tra cứu được và dòng thiếu vai trò sân nhà hoặc sân khách.
- So tổng phút, bàn, kiến tạo và thẻ giữa dữ liệu sạch với fact theo giải và mùa. Chạy lại cùng một lô để kiểm tra số lượt ra sân và tổng độ đo không tăng vì nạp trùng.
