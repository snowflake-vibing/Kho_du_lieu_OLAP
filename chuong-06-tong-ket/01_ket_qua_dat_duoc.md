# 6.1 Kết quả đạt được

## Kho dữ liệu và tích hợp dữ liệu

Nhóm thiết kế mô hình hình sao với bảng sự kiện `FACT_Player_Match_Perf` và năm chiều `DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`. Mỗi dòng sự kiện biểu diễn một lượt ra sân của một cầu thủ trong một trận. Các độ đo như số phút, bàn thắng, kiến tạo và số thẻ có thể tổng hợp theo những chiều phân tích này. [Lược đồ kho dữ liệu](../docs/schema_dbdiagram.dbml) · [Định nghĩa bảng sự kiện](../docs/fact_player_match_perf.md)

Quy trình SSIS quy định thứ tự nạp các bảng chiều trước bảng sự kiện, chuyển đổi kiểu dữ liệu và tra cứu khóa ngoại. Ma trận đối chiếu ghi lại ánh xạ từ CSV qua các bước biến đổi đến cột đích, giúp truy vết khi dữ liệu nạp có sai khác. [Luồng nạp SSIS](../ssis/ssis_main.md) · [Ma trận đối chiếu dữ liệu](../docs/cross_checking_matrix.md)

## Phân tích OLAP và báo biểu

Nhóm xây dựng cube `DW Football Transfermarkt` để tổng hợp chỉ số, lọc theo các chiều và phân tích ở nhiều mức chi tiết. Bộ tài liệu MDX ghi lại các câu hỏi nghiệp vụ, trong đó có phân tích bàn thắng và số trận theo sân thi đấu. [Thước đo của cube](../ssas/ssas_cube_measures.md) · [Danh mục truy vấn MDX](../mdx/README.md)

Tệp Power BI gồm ba trang về cơ cấu giải đấu và hiệu suất thi đấu, đóng góp tấn công, và kỷ luật cùng khối lượng thi đấu. Kho lưu trữ cũng có hướng dẫn dựng ba báo biểu tương ứng trên Looker Studio từ dữ liệu CSV. [Tệp Power BI](../power-bi/Kho_du_lieu_OLAP.pbix) · [Hướng dẫn Looker Studio](../google-data-studio/README.md)

## Thí nghiệm khai thác dữ liệu

Chương 5 dùng 425.673 lượt ra sân trong giai đoạn 2022–2024 để xây dựng và kiểm tra bài toán ước lượng khả năng một lượt ra sân kéo dài ít nhất 60 phút. Trên tập kiểm tra năm 2024, ROC-AUC của bốn mô hình nằm trong khoảng 0,512–0,517. Ở ngưỡng 0,5, cả bốn mô hình và baseline đều dự đoán lớp dương cho mọi lượt. Kết quả này cho thấy các đặc trưng bối cảnh đang dùng chỉ tách hai nhóm ở mức hạn chế. [Bảng kết quả và mã tái lập](../chuong-05-khai-thac-du-lieu/03_so_sanh_ket_qua.md)
