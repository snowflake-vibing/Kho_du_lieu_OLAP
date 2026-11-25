# 6.2–6.3 Thuận lợi và khó khăn

## 6.2 Thuận lợi

- **Dữ liệu có mã liên kết.** Các mã cầu thủ, trận đấu, câu lạc bộ và giải đấu cho phép ghép dữ liệu và truy vết bản ghi. Bảng lượt ra sân cung cấp sẵn số phút, bàn thắng, kiến tạo và thẻ.
- **Mô hình hình sao có mức chi tiết rõ ràng.** Cùng một lượt ra sân có thể được phân tích theo nhiều chiều. Khi chỉ tiêu hoặc bộ lọc thay đổi, nhóm có thể truy vết đến bảng nguồn tương ứng.
- **Tài liệu và tệp triển khai có thể đối chiếu.** Repo lưu sơ đồ kho dữ liệu, hướng dẫn SSIS, cấu hình SSAS, truy vấn MDX và tệp Power BI, tạo căn cứ kiểm tra khi sửa một bước. [Ma trận đối chiếu](../docs/cross_checking_matrix.md) · [Hướng dẫn triển khai cube](../ssas/ssas_deploy_mdx.md)

## 6.3 Khó khăn và giới hạn

| Vấn đề | Ảnh hưởng và cách xử lý |
| --- | --- |
| Ngày có nhiều định dạng | Ngày trong CSV lượt ra sân dùng tháng/ngày/năm, trong khi CSV trận dùng năm-tháng-ngày. Cần khai báo định dạng rõ ràng trước khi xác định kỳ. Năm dương lịch và mùa giải cần có bộ lọc riêng. |
| Cầu thủ có thể đổi CLB trong mùa | Phân tích lịch sử cần dùng CLB trong bản ghi lượt ra sân. Dùng CLB hiện tại có thể gán nhầm thành tích trước chuyển nhượng. |
| Tổng hợp trên nhiều mức | Một trận có nhiều lượt ra sân và có thể xuất hiện ở nhiều nhóm CLB. Phải đếm phân biệt mã trận tại cấp tổng đang xem để tránh đếm lặp. |
| Báo biểu dùng nguồn khác nhau | Power BI dùng cube, còn Looker Studio dùng bản xuất CSV. Khi so sánh, cần khớp thời điểm tải dữ liệu, bộ lọc, đơn vị tính và cách xử lý giá trị thiếu. |
| Nhãn học máy và phạm vi mẫu | Cờ `Is_Starter` của ETL dựa trên mốc 60 phút. Dữ liệu huấn luyện chỉ bao gồm cầu thủ có lượt ra sân, nên kết quả áp dụng cho thời lượng của lượt ra sân quan sát được. |

Các quy tắc về CLB, khóa trận và nhãn được mô tả trong [tài liệu bảng sự kiện](../docs/fact_player_match_perf.md), [luồng ETL bảng sự kiện](../ssis/ssis_fact_player_match_perf.md) và [phần tiền xử lý](../chuong-05-khai-thac-du-lieu/01_mo_ta_va_tien_xu_ly.md).
