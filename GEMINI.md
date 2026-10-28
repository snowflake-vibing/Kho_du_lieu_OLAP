# WORKSPACE RULES & TESTING PROTOCOL

1. **Quy tắc Kiểm tra Thực tế (Clean Testing Protocol):**
   - Mỗi lần người dùng yêu cầu kiểm tra (check lại), bắt buộc phải chạy kiểm tra lại từ đầu, không dùng lại kết quả cũ, không phỏng đoán hay khẳng định suông.
   - Viết script kiểm tra, thực thi trực tiếp trên hệ thống và cơ sở dữ liệu thực tế để lấy số liệu chứng minh.
   - Ngay sau khi kiểm tra xong, bắt buộc phải xóa hoàn toàn các file script tạm trong terminal, giữ cho workspace luôn sạch sẽ và đảm bảo mỗi lần kiểm tra tiếp theo là một lần chạy mới hoàn toàn từ đầu.

2. **Quy tắc Thước đo & Cú pháp SSAS:**
   - Mọi câu lệnh MDX, tên thước đo, tên Dimension, Hierarchy và Member phải được kiểm tra thực tế xem có tồn tại trong Cube hay không trước khi hướng dẫn.
   - Tuyệt đối không tạo các thước đo phụ thuộc dây chuyền dễ gãy (ưu tiên tính toán độc lập, tự chủ).
   - Đảm bảo tính nhất quán tuyệt đối giữa: Hướng dẫn giao diện Visual Studio (Calculations / Browser), Thiết lập PivotTable Excel, và Code MDX trong SSMS.
