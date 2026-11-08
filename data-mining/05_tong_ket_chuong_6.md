# CHƯƠNG 6: TỔNG KẾT ĐỒ ÁN MÔN HỌC (IS217)

Tài liệu này tổng hợp toàn bộ các kết quả đạt được, phân tích những thuận lợi, khó khăn trong suốt quá trình triển khai dự án kho dữ liệu và đề xuất định hướng phát triển trong tương lai theo đúng cấu trúc chuẩn của Chương 6 trong đề tài môn học IS217 - Kho dữ liệu và OLAP.

---

## 6.1 Kết quả đạt được

Trải qua toàn bộ các giai đoạn từ thu thập dữ liệu thô, thiết kế kiến trúc kho, lập trình trích xuất và biến đổi (ETL), xây dựng khối đa chiều (Cube), phân tích truy vấn nâng cao đến lập báo biểu trực quan và khai thác dữ liệu (Data Mining), nhóm đã hoàn thành xuất sắc các mục tiêu đề ra:

1. **Thiết kế kiến trúc Kho dữ liệu chuẩn hóa:**
   * Nắm vững phương pháp luận thiết kế kho dữ liệu theo lược đồ hình sao (Star Schema) và lược đồ bông tuyết (Snowflake Schema).
   * Phân tách mạch lạc giữa các bảng sự kiện (Fact Table) lưu trữ thước đo định lượng và các bảng chiều (Dimension Tables) chứa các thuộc tính ngữ cảnh nghiệp vụ.
2. **Làm chủ quy trình ETL với SSIS:**
   * Xây dựng thành công các Data Flow Task và Control Flow Task tự động hóa trong SQL Server Integration Services (SSIS).
   * Xử lý triệt để các vấn đề làm sạch dữ liệu: Chuẩn hóa kiểu dữ liệu, khử trùng lặp, xử lý giá trị NULL, bóc tách chuỗi thời gian và vị trí địa lý.
3. **Phát triển khối phân tích đa chiều SSAS:**
   * Xây dựng Cube đa chiều trong SQL Server Analysis Services, thiết kế các cây phân cấp (Hierarchies) phục vụ thao tác khoan sâu (Drill-down) và cuộn lên (Roll-up).
   * Định nghĩa các Calculated Members và Named Sets bằng ngôn ngữ MDX để tính toán các chỉ số tăng trưởng chuỗi thời gian (QoQ, MoM, YoY) hoàn toàn tự chủ.
4. **Truy vấn đa chiều và Đối soát dữ liệu 3 chiều:**
   * Viết thành thạo các câu lệnh truy vấn phức tạp bằng ngôn ngữ MDX trong SQL Server Management Studio (SSMS).
   * Thực hiện đối soát chéo đồng quy 3 chiều (MDX trong SSMS - Khối Cube Browser SSDT - PivotTable Excel) đảm bảo số lượng dòng, số cột và giá trị từng ô khớp chính xác 100%.
5. **Trực quan hóa dữ liệu chuyên nghiệp (Power BI & Looker Studio):**
   * Thiết kế 3 trang Dashboard đa chiều trên Power BI Desktop kết nối trực tiếp (Live Connection) với SSAS Cube.
   * Xây dựng hệ thống báo cáo trên Google Data Studio (Looker Studio) với các bộ lọc phân cấp và tính năng khoan sâu Drill-down linh hoạt.
6. **Ứng dụng Data Mining vào bài toán dự báo rủi ro:**
   * Thực hiện thành công quy trình tiền xử lý, phân tích khám phá dữ liệu (EDA), mã hóa One-Hot Encoding và phân chia tập dữ liệu huấn luyện.
   * Huấn luyện và đánh giá thực nghiệm hai mô hình học máy hiện đại: **XGBoost Classifier** và **Random Forest**, phân tích sâu sắc mối quan hệ đánh đổi (Trade-off) giữa độ nhạy (Recall) và tỷ lệ báo động giả (False Positive) trên dữ liệu mất cân bằng.

---

## 6.2 Thuận lợi

Trong quá trình thực hiện đồ án, nhóm đã gặp nhiều điều kiện thuận lợi:
* **Hệ sinh thái công cụ đồng bộ của Microsoft:** Sự liên kết chặt chẽ giữa SQL Server, SSIS, SSAS, Visual Studio SSDT, Excel PivotTable và Power BI giúp luồng dữ liệu di chuyển liền mạch và hạn chế tối đa các lỗi chuyển đổi định dạng.
* **Tài liệu học tập và tham khảo phong phú:** Nguồn tài liệu giảng dạy môn học IS217, các bài báo cáo mẫu của các khóa trước cùng cộng đồng khoa học dữ liệu quốc tế hỗ trợ rất nhanh chóng trong việc tra cứu cú pháp và thuật toán.
* **Sự phối hợp nhóm chặt chẽ:** Các thành viên trong nhóm chủ động phân chia công việc rõ ràng, theo sát tiến độ tuần và hoàn thành các mốc bàn giao đúng thời hạn quy định.

---

## 6.3 Khó khăn

Bên cạnh những thuận lợi, nhóm cũng đối mặt với một số thách thức thực tế:
1. **Thiếu kinh nghiệm thực chiến ban đầu:** Ở giai đoạn đầu của đồ án, do chưa có nhiều kinh nghiệm thực tế về SSIS và cấu hình thuộc tính Dimension trong SSAS, nhóm đã phải chạy lại và sửa đổi cấu hình dự án nhiều lần để đạt được kết quả đồng bộ cuối cùng.
2. **Quy mô thuộc tính dữ liệu lớn:** Do giới hạn thời gian môn học và tài nguyên tính toán cục bộ, nhóm chưa thể khai thác toàn bộ 100% các thuộc tính phụ trong tập dữ liệu gốc mà phải tiến hành chọn lọc các đặc trưng cốt lõi nhất.
3. **Thách thức từ dữ liệu mất cân bằng nghiêm trọng (Severe Class Imbalance):**
   * Tỷ lệ các sự vụ rủi ro/gian lận trong thực tế chỉ chiếm một phần rất nhỏ (<5%).
   * Khi huấn luyện mô hình Data Mining, các thuật toán dễ rơi vào trạng thái dự đoán thiên vị lớp đa số, khiến chỉ số AUC chỉ dao động quanh ngưỡng 0.5 và tỷ lệ báo động giả (False Positive) còn cao.

---

## 6.4 Hướng phát triển trong tương lai

Để nâng tầm đồ án từ một bài tập lớn môn học thành một giải pháp phần mềm doanh nghiệp hoàn chỉnh, nhóm định hướng các mục tiêu mở rộng:

1. **Nâng cấp kiến trúc dữ liệu lên nền tảng đám mây (Cloud Data Lakehouse):**
   * Chuyển đổi kho dữ liệu từ SQL Server cục bộ sang kiến trúc hiện đại trên Cloud (như Microsoft Fabric, Azure Synapse Analytics hoặc Snowflake) để xử lý dữ liệu lớn theo thời gian thực (Streaming ETL).
2. **Cải tiến mô hình Data Mining và AI:**
   * Áp dụng các kỹ thuật cân bằng dữ liệu nâng cao như **SMOTE** (Synthetic Minority Over-sampling Technique) kết hợp **Tomek Links** để giảm thiểu nhiễu và tăng cường chất lượng mẫu lớp thiểu số.
   * Tích hợp kiến trúc học tổ hợp xếp chồng (**Stacking Classifier**) hoặc các mô hình học sâu (**Deep Neural Networks / TabNet**) để khai thác các mối quan hệ phi tuyến tính phức tạp giữa các trường dữ liệu.
   * Tiến hành tinh chỉnh siêu tham số tự động (Hyperparameter Tuning) bằng công cụ **Optuna** hoặc **RandomizedSearchCV** để tối ưu hóa hàm mục tiêu F1-Score và Precision-Recall AUC (PR-AUC).
3. **Xây dựng hệ thống cảnh báo và phản hồi thời gian thực:**
   * Tích hợp mô hình máy học đã huấn luyện vào hệ thống API dịch vụ (sử dụng FastAPI / Flask) để chấm điểm rủi ro (Risk Scoring) theo thời gian thực ngay khi giao dịch vừa phát sinh.
   * Tự động gửi cảnh báo qua Email/SMS/Webhook cho người quản trị khi phát hiện giao dịch có điểm số bất thường vượt ngưỡng an toàn.
