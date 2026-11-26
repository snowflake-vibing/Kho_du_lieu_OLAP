# Kế hoạch chỉnh sửa kho dữ liệu bóng đá

Giữ mô hình hình sao gồm `FACT_Player_Match_Perf` và năm bảng chiều. Một dòng fact tương ứng với một lượt ra sân của một cầu thủ trong một trận. Phạm vi báo cáo là 13 giải trong hai mùa 2022/23 và 2023/24 theo bộ lọc ở Chương 1.

| Tài liệu | Việc cần làm |
| --- | --- |
| [01. Mô hình và kiểu dữ liệu](01-mo-hinh.md) | Chốt khóa, cấp độ chi tiết và vị trí lưu mùa giải. |
| [02. Tiền xử lý và nạp dữ liệu](02-etl.md) | Giữ mã nguồn, xử lý dữ liệu thiếu và đối soát sau nạp. |
| [03. Truy vấn OLAP và báo cáo](03-olap-va-bao-cao.md) | Chọn câu hỏi vừa sức, kiểm tra cách tổng hợp và đồng bộ Chương 1. |

Thứ tự triển khai đề xuất là chốt lược đồ, cập nhật ETL, nạp lại dữ liệu, rồi đối chiếu SQL với cube. Các mục bên dưới là đề xuất cho lần chỉnh sửa tiếp theo.

Nguồn đối chiếu: [Transfermarkt trên Kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores) · [Danh mục dữ liệu của tác giả](https://github.com/dcaribou/transfermarkt-datasets/blob/master/README.md).
