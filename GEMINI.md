# WORKSPACE RULES VÀ TESTING PROTOCOL

1. **Quy tắc Kiểm tra Thực tế Clean Testing Protocol:**
   - Mỗi lần người dùng yêu cầu kiểm tra hoặc check lại, bắt buộc phải chạy kiểm tra lại từ đầu, không dùng lại kết quả cũ, không phỏng đoán hay khẳng định suông.
   - Viết script kiểm tra, thực thi trực tiếp trên hệ thống và cơ sở dữ liệu thực tế để lấy số liệu chứng minh.
   - Ngay sau khi kiểm tra xong, bắt buộc phải xóa hoàn toàn các file script tạm trong terminal, giữ cho workspace luôn sạch sẽ và đảm bảo mỗi lần kiểm tra tiếp theo là một lần chạy mới hoàn toàn từ đầu.

2. **Quy tắc Thước đo và Cú pháp SSAS:**
   - Mọi câu lệnh MDX, tên thước đo, tên Dimension, Hierarchy và Member phải được kiểm tra thực tế xem có tồn tại trong Cube hay không trước khi hướng dẫn.
   - Tuyệt đối không tạo các thước đo phụ thuộc dây chuyền dễ gãy, luôn ưu tiên tính toán độc lập tự chủ.
   - Đảm bảo tính nhất quán tuyệt đối giữa 3 môi trường gồm: Hướng dẫn giao diện Visual Studio tab Calculations hoặc Browser, Thiết lập PivotTable Excel, và Code MDX trong SSMS.

3. **Quy tắc Đồng bộ Giao diện Excel PivotTable với Phép toán OLAP:**
   - Phân biệt tuyệt đối giữa Lọc phẳng thông thường và Đại số tập hợp OLAP:
     - Với bài toán lọc ngưỡng số học hoặc lấy Top N phẳng: Cho phép dùng `Value Filters` trong Excel.
     - Với bài toán Đại số tập hợp có mệnh đề `SET`, toán tử `INTERSECT`, `UNION`, `EXCEPT` hoặc lọc giao giữa nhiều lát cắt Dimension: BẮT BUỘC hướng dẫn dùng tính năng `PivotTable Analyze` -> `Fields, Items, & Sets` -> `Create Set Using MDX...`. Tuyệt đối không dùng `Value Filters` vì sẽ làm sai lệch bản chất phân tích và sai số dòng dữ liệu.
   - Xử lý Cột rỗng và Giá trị khởi đầu NULL: Đối với các chỉ số chuỗi thời gian như tăng trưởng QoQ, MoM, YoY có kỳ khởi đầu mang giá trị NULL, hướng dẫn Excel bắt buộc phải có bước nhấp chuột phải vào tiêu đề cột và chọn `Hide` để ẩn cột rỗng, đảm bảo số cột số liệu hiển thị trong Excel khớp chính xác 100% với trục COLUMNS của MDX.
   - Đồng bộ Bố cục Dữ liệu: Định dạng bố cục bảng trong Excel theo Report Layout phải thống nhất với bảng nhận xét và kết quả MDX. Ưu tiên dạng bảng danh sách `Show in Tabular Form` và `Do Not Show Subtotals` khi hiển thị nhiều cấp phân loại trên dòng.

4. **Quy tắc Kiểm định Chéo Đồng quy 3 Chiều 3-Way Equivalence Verification:**
   - Khi nghiệm thu bất kỳ câu truy vấn nào, không được chỉ kiểm tra riêng mã MDX.
   - Bắt buộc phải mô phỏng đối soát cả 3 phương diện:
     - Số lượng dòng dữ liệu và danh sách đối tượng: MDX ra N dòng thì Excel và Cube Browser cũng phải ra đúng N dòng đó.
     - Số lượng cột số liệu: Các cột đo lường phải khớp hoàn toàn về số lượng và thứ tự.
     - Giá trị số học từng ô: Mọi con số định lượng và tỷ lệ phần trăm phải trùng khớp tuyệt đối, không có sai lệch.
   - Nếu phát hiện bất kỳ sự vênh nào giữa thao tác Excel, Cube Browser và câu lệnh MDX, kết luận kiểm tra phải là KHÔNG ĐẠT và lập tức điều chỉnh lại tài liệu.

5. **Quy tắc Kỷ luật và Chế tài Nghiêm ngặt (Strict Disciplinary Accountability):**
   - Mọi câu trả lời nghiệm thu của AI nếu chỉ chạy riêng lệnh MDX mà khẳng định đã đối soát 3 chiều thì mặc định bị coi là **VI PHẠM KỶ LUẬT VÀ KHÔNG ĐẠT**.
   - Nghiêm cấm tuyệt đối việc suy diễn toán tử giao diện. Trong Cube Browser của Visual Studio (SSDT), danh sách toán tử chuẩn chỉ gồm: `Equal`, `Not Equal`, `In`, `Not In`, `Contains`, `Begins With`, `Range (Inclusive)`, `Range (Exclusive)`, `Custom`. Tuyệt đối KHÔNG hướng dẫn các toán tử không tồn tại như `Greater Than`, `Less Than`... Đối với các bài toán lọc ngưỡng số học hoặc Top N trong Cube Browser, BẮT BUỘC hướng dẫn dùng toán tử **`Custom`** hoặc kéo **`Named Set`**.
   - Khi tạo thước đo hiển thị giá trị thuộc tính Dimension (như `Stadium Capacity`), BẮT BUỘC dùng cú pháp `MAX(EXISTING [Dimension].[Attribute].[Attribute].MEMBERS, [Dimension].[Attribute].CURRENTMEMBER.MEMBER_VALUE)` để ngăn chặn triệt để lỗi trả về chữ `All` khi thuộc tính không nằm trên trục Rows.
   - Lịch sử các sai phạm thực tế và bài học kỷ luật được ghi nhận vĩnh viễn tại `docs/BIEN_BAN_KIEM_DIEM_AI_SU_CO_QUERY_10_11.md`.
