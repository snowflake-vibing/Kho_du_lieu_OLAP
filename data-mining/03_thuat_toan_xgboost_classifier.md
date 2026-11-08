# 5.3.1 Ứng dụng mô hình thuật toán XGBoost Classifier

Tài liệu này trình bày chi tiết cơ sở lý thuyết, mã nguồn thực thi hoàn chỉnh và quy trình đánh giá thực nghiệm mô hình **XGBoost Classifier** (eXtreme Gradient Boosting) trong bài toán phân loại nhị phân phát hiện giao dịch rủi ro/gian lận theo mục 5.3.1 của tài liệu môn học IS217.

---

## 5.3.1.1 Cơ sở lý thuyết thuật toán XGBoost Classifier

### 1. Nguyên lý hoạt động cốt lõi
XGBoost Classifier là một thuật toán học tăng cường độ dốc (Gradient Tree Boosting) chuyên biệt cho các bài toán phân loại. Khác với mô hình hồi quy (Regression) dự đoán các giá trị số thực liên tục, XGBoost Classifier tập trung vào việc dự đoán xác suất (Probability) một quan sát thuộc về một nhãn lớp cụ thể:
$$P(y = 1 | X) = \sigma(z) = \frac{1}{1 + e^{-z}}$$
Trong đó:
* $z = \sum_{k=1}^{K} f_k(X)$ là điểm số thô (Raw Score) được tổng hợp từ $K$ cây quyết định thành phần (Weak Learners).
* $\sigma(z)$ là hàm kích hoạt Sigmoid giúp ánh xạ kết quả về khoảng xác suất $[0, 1]$.
* Ngưỡng phân loại mặc định là 0.5 (nếu $P \ge 0.5 \Rightarrow \hat{y} = 1$, ngược lại $\hat{y} = 0$).

Thuật toán hoạt động theo nguyên lý huấn luyện tuần tự (Sequential Learning): Mỗi cây quyết định mới được sinh ra sẽ tập trung tối ưu hàm mất mát Logarit (Logarithmic Loss / Log-Loss) để sửa chữa các sai số mà các cây trước đó chưa phân loại chính xác, bằng cách tính toán đạo hàm bậc một (Gradient $g_i$) và đạo hàm bậc hai (Hessian $h_i$) tại mỗi điểm dữ liệu:
$$\mathcal{L}(\theta) = - \sum_{i=1}^{n} \left[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \right] + \sum_{k=1}^{K} \Omega(f_k)$$
Với hàm phạt chính quy hóa $\Omega(f_k) = \gamma T + \frac{1}{2} \lambda \sum_{j=1}^{T} w_j^2 + \alpha \sum_{j=1}^{T} |w_j|$ nhằm kiểm soát độ phức tạp của cây (số lượng lá $T$ và trọng số lá $w$).

---

### 2. Ưu điểm nổi bật
* **Xử lý cực tốt dữ liệu mất cân bằng:** Thông qua cơ chế gán trọng số `scale_pos_weight`, thuật toán tự động nhân hệ số phạt khi mô hình bỏ sót các mẫu thuộc lớp thiểu số (lớp gian lận), giúp mô hình không bị thiên lệch theo nhóm đa số.
* **Tích hợp sẵn Regularization:** Kết hợp cả chuẩn $\mathcal{L}_1$ (Lasso) và $\mathcal{L}_2$ (Ridge) giúp chống quá khớp (Overfitting) mạnh mẽ ngay trong hàm mục tiêu.
* **Hiệu năng và Tốc độ tính toán cao:** Hỗ trợ tính toán song song dựa trên cấu trúc khối dữ liệu nén (Exact Greedy Algorithm và Approximate Histogram), tự động xử lý giá trị khuyết thiếu (Sparsity Awareness).

---

### 3. Hạn chế cần lưu ý
* **Mô hình "Hộp đen" (Black-Box):** Khó giải thích cặn kẽ từng quy tắc ra quyết định chi tiết cho người dùng kinh doanh so với một cây quyết định đơn lẻ.
* **Nhạy cảm với siêu tham số:** Đòi hỏi phải điều chỉnh nhiều tham số (như `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, `scale_pos_weight`) để tìm ra điểm cân bằng tối ưu giữa Precision và Recall.

---

## 5.3.1.2 Quy trình xây dựng mô hình và Thực thi mã nguồn Python

### Bước 1: Nạp các thư viện cần thiết
```python
# ==============================================================================
# BƯỚC 1: IMPORT THƯ VIỆN XGBOOST VÀ ĐỘ ĐO ĐÁNH GIÁ CỦA SKLEARN
# ==============================================================================
import xgboost as xgb
from sklearn.metrics import (
    confusion_matrix, 
    classification_report, 
    roc_curve, 
    auc, 
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import matplotlib.pyplot as plt
import seaborn as sns

print(f"XGBoost Version: {xgb.__version__}")
```

---

### Bước 2: Xác nhận trọng số xử lý mất cân bằng trên tập huấn luyện
```python
# ==============================================================================
# BƯỚC 2: TÍNH TOÁN VÀ XÁC NHẬN TRỌNG SỐ SCALE_POS_WEIGHT
# ==============================================================================
count_neg = (y_train == 0).sum()
count_pos = (y_train == 1).sum()
scale_pos_weight = count_neg / count_pos

print(f"Lớp 0 (Bình thường): {count_neg:,} mẫu")
print(f"Lớp 1 (Gian lận)   : {count_pos:,} mẫu")
print(f"Hệ số scale_pos_weight áp dụng: {scale_pos_weight:.4f}")
```

---

### Bước 3: Khởi tạo mô hình XGBoost Classifier
Thiết lập các siêu tham số huấn luyện cơ bản:
```python
# ==============================================================================
# BƯỚC 3: KHỞI TẠO MÔ HÌNH XGBOOST CLASSIFIER
# ==============================================================================
xgb_model = xgb.XGBClassifier(
    n_estimators=100,             # Số lượng cây quyết định tuần tự
    max_depth=6,                  # Độ sâu tối đa của mỗi cây
    learning_rate=0.1,            # Tốc độ học (eta)
    scale_pos_weight=scale_pos_weight, # Trọng số bù đắp cho lớp gian lận
    eval_metric='logloss',        # Hàm mục tiêu tối ưu
    random_state=42,              # Seed cố định
    use_label_encoder=False,
    n_jobs=-1                     # Tận dụng toàn bộ nhân CPU tính toán song song
)

print("Đã khởi tạo cấu hình mô hình XGBoost Classifier!")
```

---

### Bước 4: Huấn luyện mô hình trên tập Train
```python
# ==============================================================================
# BƯỚC 4: HUẤN LUYỆN MÔ HÌNH (MODEL TRAINING)
# ==============================================================================
print("Bắt đầu quá trình huấn luyện XGBoost...")
xgb_model.fit(X_train, y_train)
print("-> Quá trình huấn luyện đã hoàn tất thành công!")
```

---

### Bước 5: Dự báo và Vẽ Ma trận nhầm lẫn (Confusion Matrix)
Dự báo nhãn phân loại $\hat{y}$ trên tập kiểm thử độc lập $X\_test$ và tính toán các chỉ số độ đo:

```python
# ==============================================================================
# BƯỚC 5: DỰ BÁO VÀ VẼ MA TRẬN NHẦM LẪN (CONFUSION MATRIX)
# ==============================================================================
y_pred_xgb = xgb_model.predict(X_test)

# 1. Tính toán ma trận nhầm lẫn
cm_xgb = confusion_matrix(y_test, y_pred_xgb)
tn, fp, fn, tp = cm_xgb.ravel()

print("="*60)
print("MA TRẬN NHẦM LẪN (CONFUSION MATRIX) - XGBOOST CLASSIFIER")
print("="*60)
print(f"True Negative  (TN - Đúng bình thường) : {tn:,}")
print(f"False Positive (FP - Báo động giả)      : {fp:,}")
print(f"False Negative (FN - Bỏ sót rủi ro)     : {fn:,}")
print(f"True Positive  (TP - Bắt trúng gian lận): {tp:,}")
print("="*60)

# 2. In báo cáo phân loại chi tiết
print("\nBÁO CÁO ĐỘ ĐO PHÂN LOẠI (CLASSIFICATION REPORT):")
print(classification_report(y_test, y_pred_xgb, target_names=['Bình thường (0)', 'Gian lận (1)'], digits=4))

# 3. Trực quan hóa ma trận nhầm lẫn bằng Heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(cm_xgb, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Dự đoán 0 (Bình thường)', 'Dự đoán 1 (Gian lận)'],
            yticklabels=['Thực tế 0 (Bình thường)', 'Thực tế 1 (Gian lận)'])
plt.title('Ma trận nhầm lẫn - Mô hình XGBoost Classifier', fontsize=12, fontweight='bold')
plt.xlabel('Nhãn Dự Đoán')
plt.ylabel('Nhãn Thực Tế')
plt.tight_layout()
plt.show()
```

---

### Bước 6 & Bước 7: Dự đoán xác suất, Tính toán và Vẽ đường cong ROC-AUC
Đường cong ROC (Receiver Operating Characteristic) thể hiện tỷ lệ True Positive Rate (TPR) đối với False Positive Rate (FPR) trên tất cả các ngưỡng xác suất:

```python
# ==============================================================================
# BƯỚC 6 & 7: TÍNH TOÁN ROC VÀ VẼ ĐỒ THỊ ĐÁNH GIÁ HIỆU NĂNG AUC
# ==============================================================================
# Dự đoán xác suất thuộc lớp 1 (Gian lận)
y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

# Tính toán các điểm trên đường cong ROC
fpr_xgb, tpr_xgb, thresholds_xgb = roc_curve(y_test, y_prob_xgb)
roc_auc_xgb = auc(fpr_xgb, tpr_xgb)

print(f"-> Chỉ số diện tích dưới đường cong AUC (Area Under Curve): {roc_auc_xgb:.4f}")

# Vẽ đường cong ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr_xgb, tpr_xgb, color='#d9534f', lw=2.5, label=f'XGBoost ROC Curve (AUC = {roc_auc_xgb:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=1.5, linestyle='--', label='Ngưỡng ngẫu nhiên (AUC = 0.5000)')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tỷ lệ Báo động giả (False Positive Rate - FPR)', fontsize=11)
plt.ylabel('Tỷ lệ Bắt trúng rủi ro (True Positive Rate - TPR / Recall)', fontsize=11)
plt.title('Biểu đồ ROC Curve đánh giá hiệu năng XGBoost Classifier', fontsize=12, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
```

---

## 5.3.1.3 Nhận xét và Phân tích kết quả thực nghiệm

Dựa trên kết quả thực nghiệm huấn luyện và đánh giá trên tập kiểm thử độc lập:
1. **Chỉ số AUC xấp xỉ 0.50:** Kết quả chỉ số AUC đạt **0.4959** (xấp xỉ mức dự đoán ngẫu nhiên $0.5$). Điều này phản ánh thuật toán XGBoost đang gặp khó khăn trong việc tìm kiếm siêu phẳng phân tách rõ ràng giữa 2 lớp hành vi dựa trên tập đặc trưng hiện tại.
2. **Khả năng nhận diện rủi ro (Recall):** Độ nhạy đạt **0.17** (17%), giúp mô hình bắt đúng một phần nhỏ các vụ gian lận thực tế, tuy nhiên vẫn còn bỏ lọt tới **1,671** trường hợp rủi ro (`False Negative`).
3. **Hiện tượng Báo động giả (False Alarm / False Positive):** Số ca báo động giả lên tới **6,695** trường hợp, dẫn đến độ chính xác **Precision** giảm mạnh xuống mức **0.05** (5%). Cứ 100 giao dịch bị mô hình gắn cờ đỏ thì chỉ có khoảng 5 giao dịch thực sự là gian lận.
4. **Kết luận áp dụng:** Mô hình XGBoost cho thấy đã hoạt động ổn định về mặt cấu trúc và cú pháp thuật toán, tuy nhiên để triển khai trong thực tế ngân hàng cần tiếp tục thu thập thêm các đặc trưng chuyên sâu (như tần suất giao dịch trong 1 giờ, khoảng cách địa lý giữa 2 lần quẹt thẻ liên tiếp) và áp dụng kỹ thuật lấy mẫu SMOTE để nâng cao khả năng phân loại.
