# CHƯƠNG 5 & 6: KHAI THÁC DỮ LIỆU BÓNG ĐÁ (DATA MINING) VÀ TỔNG KẾT ĐỒ ÁN

Thư mục này chứa toàn bộ tài liệu hướng dẫn chi tiết quy trình khám phá dữ liệu (EDA), tiền xử lý, lựa chọn đặc trưng, mã hóa biến, phân chia tập dữ liệu huấn luyện, xây dựng, tinh chỉnh siêu tham số và so sánh 4 mô hình học máy (**Decision Tree**, **LightGBM**, **XGBoost**, **Stacking Classifier**), cùng báo cáo tổng kết đồ án môn học **IS217 - Kho dữ liệu và OLAP** trên tập dữ liệu **Bóng đá Châu Âu (Football Transfermarkt)**, tham chiếu phương pháp luận từ đề tài mẫu `[6]_IS217Q11_23520009_23520753.pdf`.

---

## Danh mục tài liệu hướng dẫn

| STT | Tên tài liệu | Nội dung chính | Công nghệ / Thư viện |
| :---: | :--- | :--- | :---: |
| **01** | [01_tien_xu_ly_va_eda.md](file:///d:/Kho_du_lieu_OLAP/data-mining/01_tien_xu_ly_va_eda.md) | **5.1 & 5.2 Mô tả bộ dữ liệu và Tiền xử lý:** Khảo sát bảng `appearances` (hơn 1.2M lượt ra sân), làm sạch missing values, phân tích EDA tỷ lệ đá chính (`Is_Starter`), tương quan thời lượng thi đấu, bàn thắng và thẻ phạt theo vị trí | Python, Pandas, Matplotlib, Seaborn |
| **02** | [02_lua_chon_thuoc_tinh_va_chuan_bi_du_lieu.md](file:///d:/Kho_du_lieu_OLAP/data-mining/02_lua_chon_thuoc_tinh_va_chuan_bi_du_lieu.md) | **5.3 Chuẩn bị dữ liệu huấn luyện:** Định nghĩa bài toán phân loại nhị phân `Is_Starter`, Feature Selection lọc bỏ ID, One-Hot Encoding biến danh mục, phân chia Train/Test 80/20 có phân tầng (`stratify=y`), chuẩn hóa với `StandardScaler` | Scikit-learn (`train_test_split`, `StandardScaler`) |
| **03** | [03_thuat_toan_xgboost_classifier.md](file:///d:/Kho_du_lieu_OLAP/data-mining/03_thuat_toan_xgboost_classifier.md) | **5.4.2 Thuật toán XGBoost:** Cơ sở lý thuyết GBDT, hàm mất mát Log-loss và Regularization; Quét siêu tham số bằng `GridSearchCV` 5-fold, Ma trận nhầm lẫn, Classification Report, ROC-AUC (AUC = 0.9415) | `xgboost` (`XGBClassifier`), Scikit-learn Metrics |
| **04** | [04_thuat_toan_stacking_classifier.md](file:///d:/Kho_du_lieu_OLAP/data-mining/04_thuat_toan_stacking_classifier.md) | **5.4.3 Thuật toán Stacking Classifier (Ensemble Quán quân):** Kiến trúc Stacking đa tầng (Base-learners: LightGBM, XGBoost, Random Forest; Meta-learner: Logistic Regression); Đánh giá ROC-AUC (AUC = 0.9520) và phân tích mức độ quan trọng của đặc trưng (**Feature Importance**) | `sklearn.ensemble.StackingClassifier`, `permutation_importance` |
| **05** | [05_thuat_toan_decision_tree_va_lightgbm.md](file:///d:/Kho_du_lieu_OLAP/data-mining/05_thuat_toan_decision_tree_va_lightgbm.md) | **5.4.4 & 5.4.5 Decision Tree và LightGBM:** Lý thuyết CART và trực quan hóa cây quyết định (`plot_tree`); Lý thuyết phân nhánh theo lá (Leaf-wise) của LightGBM, tối ưu hóa tốc độ huấn luyện (~4.5s) | `sklearn.tree.DecisionTreeClassifier`, `lightgbm.LGBMClassifier` |
| **06** | [06_so_sanh_danh_gia_mo_hinh.md](file:///d:/Kho_du_lieu_OLAP/data-mining/06_so_sanh_danh_gia_mo_hinh.md) | **5.4.6 & 5.4.7 Bảng so sánh và Đánh giá tổng thể:** Bảng so sánh đa chỉ số (Accuracy, Precision, Recall, F1, AUC, Train Time); Trực quan hóa đối sánh bằng kỹ thuật Data Melting (`pd.melt`); Đánh giá chuyên sâu và đề xuất ứng dụng chiến thuật | Seaborn (`barplot`), Pandas (`melt`) |
| **07** | [07_tong_ket_chuong_6.md](file:///d:/Kho_du_lieu_OLAP/data-mining/07_tong_ket_chuong_6.md) | **Chương 6: Tổng kết đồ án Kho dữ liệu Bóng đá Châu Âu:** 6.1 Kết quả đạt được; 6.2 Thuận lợi; 6.3 Khó khăn (dữ liệu lớn >1.2M bản ghi, chuyển nhượng giữa mùa); 6.4 Hướng phát triển (AI Scouting, Dự báo chấn thương, Real-time Dashboard) | Báo cáo tổng kết đồ án môn học IS217 |

---

## Bảng so sánh kết quả thực nghiệm tổng hợp

| Thứ hạng | Mô hình Thuật toán | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Thời gian huấn luyện |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 **1** | **Stacking Classifier (Ensemble Quán quân)** | **90.15%** | **91.40%** | **95.60%** | **0.9345** | **0.9520** | ~45.2 giây |
| 🥈 **2** | **LightGBM Classifier** | 89.20% | 90.50% | 95.10% | 0.9274 | 0.9450 | **~4.5 giây (Nhanh nhất)** |
| 🥉 **3** | **XGBoost Classifier** | 88.90% | 90.20% | 94.80% | 0.9244 | 0.9415 | ~14.8 giây |
| **4** | **Decision Tree (CART)** | 85.60% | 87.80% | 92.50% | 0.9009 | 0.8850 | ~2.1 giây |
