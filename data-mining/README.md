# CHƯƠNG 5 & 6: QUÁ TRÌNH KHAI THÁC DỮ LIỆU (DATA MINING) VÀ TỔNG KẾT ĐỒ ÁN

Thư mục này chứa toàn bộ tài liệu hướng dẫn chi tiết quy trình khám phá dữ liệu (EDA), tiền xử lý, lựa chọn đặc trưng, mã hóa biến, phân chia tập dữ liệu huấn luyện, xây dựng và so sánh các mô hình máy học (**XGBoost Classifier** và **Random Forest**), cùng báo cáo tổng kết đồ án môn học **IS217 - Kho dữ liệu và OLAP**, tham chiếu từ đề tài mẫu `[27]_IS217Q13_23520698_23521417.pdf`.

---

## Danh mục tài liệu hướng dẫn

| STT | Tên tài liệu | Nội dung chính | Công nghệ / Thư viện |
| :---: | :--- | :--- | :---: |
| **01** | [01_tien_xu_ly_va_eda.md](file:///d:/Kho_du_lieu_OLAP/data-mining/01_tien_xu_ly_va_eda.md) | **5.1 Phân tích dataset gốc:** Kiểm tra null/duplicates, bóc tách thời gian (`Day, Month, Year, Hour, Minute, Second`), bóc tách vị trí (`City, State`), thống kê mô tả `describe()`, trực quan hóa EDA phân bố lớp, phân bố theo khung giờ và ngày trong tháng | Python, Pandas, Matplotlib, Seaborn |
| **02** | [02_lua_chon_thuoc_tinh_va_chuan_bi_du_lieu.md](file:///d:/Kho_du_lieu_OLAP/data-mining/02_lua_chon_thuoc_tinh_va_chuan_bi_du_lieu.md) | **5.2 Lựa chọn thuộc tính:** Lọc bỏ các ID định danh, One-Hot Encoding biến phân loại, phân tách $X$ và $y$, chia Train/Test 80/20 có phân tầng (`stratify=y`), công thức tính trọng số `scale_pos_weight` xử lý mất cân bằng dữ liệu | Scikit-learn (`train_test_split`), Pandas |
| **03** | [03_thuat_toan_xgboost_classifier.md](file:///d:/Kho_du_lieu_OLAP/data-mining/03_thuat_toan_xgboost_classifier.md) | **5.3.1 Thuật toán XGBoost Classifier:** Cơ sở lý thuyết Log-loss, Sigmoid, Regularization L1/L2; Quy trình 7 bước huấn luyện Python, Ma trận nhầm lẫn (Confusion Matrix), Classification Report, đường cong ROC và chỉ số AUC (AUC = 0.4959) | `xgboost` (`XGBClassifier`), Scikit-learn Metrics |
| **04** | [04_thuat_toan_random_forest.md](file:///d:/Kho_du_lieu_OLAP/data-mining/04_thuat_toan_random_forest.md) | **5.3.2 Thuật toán Random Forest & So sánh đối chiếu:** Lý thuyết Bagging, Majority Voting; Quy trình 4 bước huấn luyện, Ma trận nhầm lẫn, đường cong ROC và chỉ số AUC (AUC = 0.4936); Bảng so sánh toàn diện giữa Random Forest và XGBoost về đánh đổi giữa Recall và False Positives | Scikit-learn (`RandomForestClassifier`), Matplotlib |
| **05** | [05_tong_ket_chuong_6.md](file:///d:/Kho_du_lieu_OLAP/data-mining/05_tong_ket_chuong_6.md) | **Chương 6: Tổng kết đồ án:** 6.1 Kết quả đạt được; 6.2 Thuận lợi; 6.3 Khó khăn (về dữ liệu mất cân bằng nặng và số chiều lớn); 6.4 Hướng phát triển (Cloud Lakehouse, SMOTE, Stacking, Real-time Risk Scoring) | Báo cáo tổng kết đồ án môn học IS217 |

---

## Tóm tắt kết quả thực nghiệm Data Mining

| Mô hình thuật toán | Diện tích dưới đường cong (AUC) | Độ nhạy bắt rủi ro (Recall) | Độ chính xác cảnh báo (Precision) | Số ca bắt trúng (TP) | Số ca báo động giả (FP) | Đánh giá tổng quan |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **XGBoost Classifier** | **0.4959** | 0.1700 (17%) | 0.0500 (5%) | 342 ca | **6,695 ca** | **Tối ưu hơn trong vận hành**, giảm thiểu 3,396 ca làm phiền khách hàng vô tội |
| **Random Forest** | 0.4936 | **0.2700 (27%)** | 0.0500 (5%) | **536 ca** | 10,091 ca | **Độ nhạy cao hơn (+10%)**, bắt thêm 189 ca gian lận nhưng tỷ lệ báo động giả quá lớn |
