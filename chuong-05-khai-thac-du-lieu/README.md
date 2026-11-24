# Chương 5. Quá trình khai thác dữ liệu

Thí nghiệm dùng dữ liệu Transfermarkt trong repo để ước lượng khả năng một cầu thủ **thi đấu từ 60 phút trở lên, với điều kiện cầu thủ đó có lượt ra sân**. Mốc 60 phút lấy từ cờ `Is_Starter` trong ETL. Cờ này chỉ phản ánh thời lượng quan sát được và chưa xác nhận cầu thủ có mặt trong đội hình xuất phát.

| Tài liệu | Nội dung |
| --- | --- |
| [01. Mô tả và tiền xử lý](01_mo_ta_va_tien_xu_ly.md) | Nguồn dữ liệu, thu hẹp phạm vi, kiểm tra chất lượng và thống kê theo năm |
| [02. Huấn luyện mô hình](02_huan_luyen_mo_hinh.md) | Chia tập theo thời gian, mô hình đối chứng và bốn mô hình phân loại |
| [03. So sánh kết quả](03_so_sanh_ket_qua.md) | Bảng điểm thực nghiệm trên năm 2024, ma trận nhầm lẫn và cách diễn giải |

Cấu trúc chương tham khảo Chương 5 của báo cáo IS217.Q11 của Lê Nguyễn Thúy An và Phạm Nhật Khoa. Mã và bảng kết quả của chương này sử dụng dữ liệu bóng đá. Chạy các khối Python theo thứ tự từ 01 đến 03 trong cùng một notebook hoặc tiến trình Python.
