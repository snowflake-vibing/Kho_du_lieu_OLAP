# 4.3 Tạo ba báo biểu bằng Looker Studio

## Tạo báo cáo và cấu hình trường

1. Tạo báo cáo trống, tải lên CSV theo [truy vấn xuất dữ liệu](01_chuan_bi_nguon_du_lieu.md) và thêm nguồn vào báo cáo.
2. Đặt ID thành kiểu văn bản, `Full_Date` thành ngày, các cột phút, bàn, kiến tạo và thẻ thành số. Dùng `Full_Date` làm trường ngày của bộ lọc khoảng thời gian.
3. Tạo thước đo `COUNT_DISTINCT(Game_ID)` và `COUNT_DISTINCT(Appearance_ID)`. Với biểu đồ tháng xuyên năm, dùng độ chi tiết **Year Month** từ `Full_Date`.
4. Kiểm tra các biểu đồ và thẻ KPI trên cùng trang phản hồi theo phạm vi lọc mong muốn.

## Cấu hình ba trang

| Trang | Biểu đồ và cấu hình | Điều khiển |
| --- | --- | --- |
| **1. Cơ cấu giải đấu** | Thanh xếp chồng theo loại giải, quốc gia, giải và vòng với bàn thắng và kiến tạo. Biểu đồ quý dùng tổng bàn và kiến tạo. Pivot theo giải → CLB → cầu thủ, hiển thị số trận, phút và thẻ. | Giải, quốc gia của giải, CLB, cầu thủ |
| **2. Đóng góp tấn công** | Thanh theo CLB, sắp theo tổng đóng góp bàn thắng. Combo theo sân với số trận và bàn thắng. Chuỗi năm-tháng với số bàn. Bảng cầu thủ có tuổi, chân thuận, quốc tịch, bàn và kiến tạo. | Cầu thủ, CLB, mùa giải, khoảng ngày |
| **3. Kỷ luật và khối lượng** | Thanh xếp chồng thẻ vàng và đỏ theo CLB. Xu hướng năm-tháng dùng phút thi đấu khi phân tích khối lượng. Combo theo tuổi dùng phút và thẻ vàng. Vành khuyên dùng số thẻ đỏ theo vị trí. | Cầu thủ, giải, mùa giải, vị trí |

Tham khảo hướng dẫn dựng [trang 1](../google-data-studio/01_looker_studio_bao_bieu_1.md), [trang 2](../google-data-studio/02_looker_studio_bao_bieu_2.md) và [trang 3](../google-data-studio/03_looker_studio_bao_bieu_3.md). Khi tái tạo một visual của Power BI, dùng cùng trường nhóm và thước đo ở cả hai nền tảng. Để đối chiếu biểu đồ vùng trang 3, dùng đóng góp bàn thắng theo năm-tháng và tách chuỗi theo CLB.

## Đối chiếu và trình bày kết quả

1. Chọn cùng khoảng ngày, giải và CLB trên hai hệ thống. Ghi nhận bộ lọc trước khi xuất ảnh hoặc bảng số liệu.
2. Đối chiếu số trận phân biệt, lượt ra sân, số bàn, kiến tạo, phút và thẻ ở cấp toàn trang. Sau đó chọn một CLB hoặc một trận để kiểm tra từng nhóm nhỏ.
3. Nếu số liệu chênh lệch, kiểm tra ngày xử lý cube, ngày xuất CSV, cách tổng hợp cột ID và quy tắc xử lý giá trị trống.
4. Khi nhận xét, nêu kỳ dữ liệu, bộ lọc, chỉ số và nhóm đang so sánh. Với một tháng hoặc mùa chưa đủ dữ liệu, ghi rõ số trận quan sát được trước khi diễn giải xu hướng.
