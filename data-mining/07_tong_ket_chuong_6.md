# CHƯƠNG 6: TỔNG KẾT ĐỒ ÁN KHO DỮ LIỆU BÓNG ĐÁ CHÂU ÂU (FOOTBALL TRANSFERMARKT)

Tài liệu này tổng kết toàn diện các thành quả nghiên cứu, phân tích những thuận lợi, khó khăn trong suốt quá trình xây dựng Kho dữ liệu Bóng đá Châu Âu, đồng thời đề xuất định hướng phát triển trong tương lai theo đúng cấu trúc chuẩn của Chương 6 trong đề tài môn học IS217 - Kho dữ liệu và OLAP.

---

## 6.1 Kết quả đạt được

Trải qua toàn bộ các giai đoạn thực hiện đồ án từ khảo sát dữ liệu thô, thiết kế mô hình chiều, xây dựng gói tích hợp ETL, phát triển khối đa chiều Cube, kiểm định truy vấn MDX, lập báo biểu trực quan đến ứng dụng các mô hình khai thác dữ liệu Machine Learning, nhóm đã đạt được các kết quả nổi bật:

1. **Xây dựng hoàn chỉnh Kho dữ liệu Bóng đá Châu Âu theo Lược đồ Hình sao (Star Schema):**
   * Thiết kế thành công bảng sự kiện `FACT_Player_Match_Perf` lưu trữ hơn **1.2 triệu lượt ra sân** của cầu thủ qua nhiều mùa giải.
   * Chuẩn hóa 5 bảng chiều ngữ cảnh: `DIM_Player` (30.000+ cầu thủ), `DIM_Club` (hơn 400 câu lạc bộ châu Âu), `DIM_Competition` (các giải VĐQG hàng đầu và cúp châu Âu), `DIM_Game` (hơn 60.000 trận đấu) và `DIM_Time` (chuẩn hóa theo cấp Năm, Quý, Tháng, Ngày).
2. **Quy trình trích xuất và biến đổi ETL tự động hóa với SSIS:**
   * Lập trình hoàn chỉnh các luồng dữ liệu Data Flow và luồng điều khiển Control Flow trong Visual Studio SSDT.
   * Xử lý triệt để các vấn đề làm sạch dữ liệu: Chuẩn hóa kiểu dữ liệu, khử trùng lặp khóa tự nhiên, xử lý giá trị NULL ở chiều cao và chân thuận, phân tách thuộc tính thời gian và kết nối khóa ngoại.
3. **Phát triển Khối phân tích đa chiều SSAS Cube (`[DW Football Transfermarkt]`):**
   * Xây dựng thành công Cube đa chiều với các cây phân cấp thời gian (`Hierarchy: Year -> Quarter -> Month -> Day`) và phân cấp địa lý.
   * Thiết lập các thước đo tính toán độc lập tự chủ (**Calculated Members**) như `QoQ Goals Growth`, `Goal Contributions`, `Mins Per Goal` và tập hợp đặt tên (**Named Sets**) như `[Top 10 Clubs 2023]`.
4. **Đối soát Dữ liệu Đồng quy 3 Chiều đạt chuẩn tuyệt đối 100%:**
   * Thực hiện đối soát nghiêm ngặt giữa: Câu lệnh **MDX trong SSMS**, Giao diện đồ họa **Cube Browser SSDT** và Bảng tổng hợp **PivotTable Excel**.
   * Đảm bảo tính nhất quán tuyệt đối về số dòng dữ liệu, số lượng cột đo lường và giá trị số học từng ô trên toàn bộ 15 câu truy vấn nghiệp vụ.
5. **Hệ thống Báo cáo Trực quan hóa Đa nền tảng (Power BI & Looker Studio):**
   * Thiết kế 3 trang Dashboard chuyên nghiệp trên **Power BI Desktop** kết nối Live Connection với SSAS Cube:
     * *Dashboard 1:* Hiệu suất Ghi bàn và Đóng góp Kiến tạo của Cầu thủ.
     * *Dashboard 2:* Vận hành Trận đấu, Hiệu suất CLB và Tương quan Sân vận động.
     * *Dashboard 3:* Kỷ luật Thẻ phạt, Cường độ Thi đấu và Tải trọng Cầu thủ.
   * Xây dựng 3 báo biểu trực tuyến trên **Google Data Studio (Looker Studio)** với các bộ lọc phân cấp và tính năng khoan sâu Drill-down linh hoạt từ Quốc gia xuống Câu lạc bộ.
6. **Ứng dụng Data Mining vào Bài toán Dự báo Đội hình Đá chính:**
   * Thực hiện tiền xử lý, khám phá dữ liệu EDA, mã hóa One-Hot Encoding và chuẩn hóa thang đo trên tập dữ liệu hơn 1.2 triệu lượt ra sân.
   * Huấn luyện và đánh giá thực nghiệm 4 mô hình Machine Learning: **Decision Tree**, **LightGBM**, **XGBoost**, và **Stacking Classifier**.
   * Xác định mô hình Quán quân **Stacking Classifier** đạt **Accuracy = 90.15%**, **F1-Score = 0.9345**, và **ROC-AUC = 0.9520**, đồng thời phân tích chi tiết mức độ quan trọng của các thuộc tính thể lực và phong độ.

---

## 6.2 Thuận lợi

Trong quá trình triển khai dự án, nhóm đã có những điều kiện thuận lợi:
* **Nguồn dữ liệu Transfermarkt phong phú và chuẩn mực:** Dữ liệu bóng đá Transfermarkt cung cấp thông tin chi tiết và có độ tin cậy rất cao về thống kê trận đấu, lịch sử ra sân và thông số cầu thủ.
* **Hệ sinh thái Microsoft BI đồng bộ:** Sự kết hợp hoàn hảo giữa SQL Server Database Engine, SSIS, SSAS, Visual Studio SSDT, Excel và Power BI giúp luồng dữ liệu luân chuyển trơn tru, không gặp rào cản về tương thích định dạng.
* **Tài liệu hướng dẫn môn học IS217 chi tiết:** Nguồn tài liệu giảng dạy của giảng viên và các bài báo cáo mẫu khóa trước định hướng rõ ràng về cấu trúc, tiêu chuẩn kỹ thuật và phương pháp luận khoa học dữ liệu.

---

## 6.3 Khó khăn

Bên cạnh những thuận lợi, nhóm cũng đối mặt với các thách thức kỹ thuật:
1. **Khối lượng dữ liệu ra sân khổng lồ (Big Data):** Bảng `appearances` với hơn 1.2 triệu bản ghi đòi hỏi tối ưu hóa bộ nhớ RAM và thiết lập chỉ mục (Indexes) kỹ lưỡng trong SQL Server để tránh tràn bộ nhớ khi xử lý ETL và huấn luyện mô hình học máy.
2. **Biến động chuyển nhượng cầu thủ giữa mùa bóng:** Một cầu thủ có thể chuyển nhượng từ câu lạc bộ này sang câu lạc bộ khác trong cùng một mùa giải, đòi hỏi bảng Fact phải lưu trữ chính xác `Club_ID` tại thời điểm diễn ra trận đấu thay vì lấy CLB hiện tại của cầu thủ.
3. **Hiện tượng dữ liệu khuyết thiếu ở các cầu thủ trẻ:** Một số cầu thủ trẻ mới lên đội một chưa có đầy đủ thông tin về chiều cao, chân thuận hoặc giá trị thị trường, nhóm đã phải áp dụng kỹ thuật điền giá trị trung vị (Median Imputation) theo từng vị trí thi đấu để đảm bảo độ chính xác.

---

## 6.4 Hướng phát triển trong tương lai

Nhằm nâng cấp hệ sinh thái Kho dữ liệu bóng đá thành một nền tảng phân tích thể thao toàn diện cấp doanh nghiệp, nhóm định hướng các mục tiêu mở rộng:

1. **Tích hợp các chỉ số Nâng cao (Advanced Football Analytics - xG, xA):**
   * Bổ sung các chỉ số hiện đại như Bàn thắng kỳ vọng (**Expected Goals - xG**), Kiến tạo kỳ vọng (**Expected Assists - xA**) và Bản đồ vị trí chạm bóng (Touch Maps / Heatmaps) vào bảng Fact để nâng cao chiều sâu phân tích chiến thuật.
2. **Hệ thống AI Scouting và Tuyển trạch Tài năng trẻ:**
   * Xây dựng thuật toán gợi ý (Recommender System) dựa trên độ tương đồng Cosine (Cosine Similarity) để tự động tìm kiếm các "bản sao" cầu thủ có phong cách thi đấu và chỉ số tương đương các ngôi sao lớn nhưng có mức phí chuyển nhượng thấp hơn.
3. **Mô hình Dự báo Nguy cơ Chấn thương Cầu thủ (Injury Risk Prediction):**
   * Khai thác thuộc tính tải trọng thi đấu liên tục (`Minutes_Played` dồn dập trong 7 ngày) kết hợp với các thuật toán học sâu chuỗi thời gian (LSTM / GRU) để đưa ra cảnh báo sớm về nguy cơ quá tải cơ bắp và chấn thương cho các cầu thủ.
4. **Triển khai ứng dụng Web Dashboard thời gian thực:**
   * Đóng gói mô hình Machine Learning thành các Microservices RESTful API bằng FastAPI / Docker và kết nối với giao diện Web Dashboard tương tác giúp ban huấn luyện có thể tra cứu nhanh trên thiết bị di động ngay trong phòng thay đồ.
