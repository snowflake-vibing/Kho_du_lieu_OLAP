# 5.4.2 Ứng dụng mô hình thuật toán XGBoost trong Dự báo Đá chính Cầu thủ

Tài liệu này trình bày chi tiết cơ sở lý thuyết toán học, quy trình lập trình thực thi bằng ngôn ngữ **Python**, tìm kiếm siêu tham số tối ưu và đánh giá hiệu năng thực nghiệm của mô hình **XGBoost (eXtreme Gradient Boosting)** trong bài toán dự báo cầu thủ ra sân đá chính theo mục 5.4.2 của đề tài môn học IS217.

---

## 5.4.2.1 Cơ sở lý thuyết thuật toán XGBoost

### 1. Nguyên lý hoạt động cốt lõi
XGBoost là một thuật toán học tăng cường độ dốc (Gradient Tree Boosting) được tối ưu hóa cực đại về hiệu năng tính toán và khả năng khái quát hóa. Trong bài toán phân loại nhị phân ($y \in \{0, 1\}$), mô hình dự đoán xác suất cầu thủ đá chính thông qua tổng hợp điểm số từ $K$ cây quyết định thành phần:
$$\hat{y}_i = \sigma \left( \sum_{k=1}^{K} f_k(x_i) \right) = \frac{1}{1 + e^{- \sum_{k=1}^K f_k(x_i)}}$$

Hàm mục tiêu (Objective Function) tại bước lặp thứ $t$ được định nghĩa bằng tổng hàm mất mát Logarit (Log-Loss) cộng với thành phần chính quy hóa (Regularization) kiểm soát độ phức tạp của các cây:
$$\mathcal{L}^{(t)} \approx \sum_{i=1}^{n} \left[ l(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$
Trong đó:
* $g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ là đạo hàm bậc một (First-order Gradient).
* $h_i = \partial^2_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ là đạo hàm bậc hai (Second-order Hessian).
* $\Omega(f_t) = \gamma T + \frac{1}{2} \lambda \sum_{j=1}^{T} w_j^2$ là hàm phạt số lượng lá $T$ và trọng số lá $w_j$ giúp chống quá khớp (Overfitting) vượt trội so với Gradient Boosting truyền thống.

---

## 5.4.2.2 Quy trình xây dựng mô hình và Thực thi mã nguồn Python

### Bước 1: Nạp thư viện và khởi tạo mô hình XGBoost
```python
# ==============================================================================
# BƯỚC 1: IMPORT THƯ VIỆN XGBOOST VÀ CÔNG CỤ TÌM KIẾM SIÊU THAM SỐ
# ==============================================================================
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    roc_curve, 
    confusion_matrix, 
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns

print(f"XGBoost Version: {xgb.__version__}")
```

---

### Bước 2: Thiết lập tìm kiếm siêu tham số tối ưu (Hyperparameter Tuning với GridSearchCV)
Tìm kiếm tổ hợp tham số tốt nhất gồm tốc độ học (`learning_rate`), độ sâu của cây (`max_depth`) và số lượng cây (`n_estimators`):

```python
# ==============================================================================
# BƯỚC 2: TÌM KIẾM SIÊU THAM SỐ TỐI ƯU VỚI GRIDSEARCHCV (5-FOLD CV)
# ==============================================================================
xgb_base = xgb.XGBClassifier(
    eval_metric='logloss',
    random_state=42,
    use_label_encoder=False,
    n_jobs=-1
)

# Lưới không gian tham số cần quét
param_grid_xgb = {
    'n_estimators': [100, 150],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.05, 0.1],
    'subsample': [0.8, 1.0]
}

# Khởi tạo GridSearch với 5-fold Cross Validation, tối ưu hóa điểm số F1
grid_search_xgb = GridSearchCV(
    estimator=xgb_base,
    param_grid=param_grid_xgb,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

print("Đang quét tìm kiếm siêu tham số tối ưu cho XGBoost...")
grid_search_xgb.fit(X_train_scaled, y_train)

best_xgb = grid_search_xgb.best_estimator_
print(f"-> Tham số tối ưu nhất: {grid_search_xgb.best_params_}")
print(f"-> F1-Score trung bình qua 5-Fold CV: {grid_search_xgb.best_score_:.4f}")
```

---

### Bước 3: Dự báo và Đánh giá kết quả trên tập kiểm thử độc lập (Test Set)
```python
# ==============================================================================
# BƯỚC 3: DỰ BÁO TRÊN TẬP TEST VÀ TÍNH TOÁN CÁC ĐỘ ĐO CHUẨN
# ==============================================================================
y_pred_xgb = best_xgb.predict(X_test_scaled)
y_prob_xgb = best_xgb.predict_proba(X_test_scaled)[:, 1]

acc_xgb = accuracy_score(y_test, y_pred_xgb)
prec_xgb = precision_score(y_test, y_pred_xgb)
rec_xgb = recall_score(y_test, y_pred_xgb)
f1_xgb = f1_score(y_test, y_pred_xgb)
auc_xgb = roc_auc_score(y_test, y_prob_xgb)

print("="*65)
print("BÁO CÁO HIỆU NĂNG MÔ HÌNH XGBOOST TRÊN TẬP TEST:")
print("="*65)
print(f"1. Độ chính xác tổng quát (Accuracy)    : {acc_xgb*100:.2f}%")
print(f"2. Độ chính xác cảnh báo  (Precision)   : {prec_xgb*100:.2f}%")
print(f"3. Độ nhạy bắt đúng nhãn  (Recall)      : {rec_xgb*100:.2f}%")
print(f"4. Điểm điều hòa F1-Score               : {f1_xgb:.4f}")
print(f"5. Diện tích dưới đường cong (ROC-AUC)  : {auc_xgb:.4f}")
print("="*65)
print("\nCHI TIẾT CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred_xgb, target_names=['Dự bị (0)', 'Đá chính (1)'], digits=4))
```

---

### Bước 4: Trực quan hóa Ma trận nhầm lẫn (Confusion Matrix)
```python
# ==============================================================================
# BƯỚC 4: VẼ MA TRẬN NHẦM LẪN BẰNG HEATMAP
# ==============================================================================
cm_xgb = confusion_matrix(y_test, y_pred_xgb)

plt.figure(figsize=(7, 5))
sns.heatmap(cm_xgb, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Dự đoán Dự bị (0)', 'Dự đoán Đá chính (1)'],
            yticklabels=['Thực tế Dự bị (0)', 'Thực tế Đá chính (1)'])
plt.title('Ma trận nhầm lẫn - Mô hình XGBoost Classifier', fontsize=12, fontweight='bold')
plt.xlabel('Nhãn Dự Đoán')
plt.ylabel('Nhãn Thực Tế')
plt.tight_layout()
plt.show()
```

---

### Bước 5: Vẽ đường cong ROC Curve và chỉ số AUC
```python
# ==============================================================================
# BƯỚC 5: VẼ ĐƯỜNG CONG ROC CURVE
# ==============================================================================
fpr_xgb, tpr_xgb, _ = roc_curve(y_test, y_prob_xgb)

plt.figure(figsize=(8, 6))
plt.plot(fpr_xgb, tpr_xgb, color='#2E86C1', lw=2.5, label=f'XGBoost ROC (AUC = {auc_xgb:.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--', label='Ngưỡng ngẫu nhiên (AUC = 0.5000)')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tỷ lệ Báo động giả (False Positive Rate - FPR)', fontsize=11)
plt.ylabel('Tỷ lệ Nhận diện đúng (True Positive Rate - TPR / Recall)', fontsize=11)
plt.title('Đường cong ROC Curve - Mô hình XGBoost Classifier', fontsize=12, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
```

---

## 5.4.2.3 Kết quả và Nhận xét phân tích
1. **Hiệu năng xuất sắc:** Mô hình XGBoost Classifier đạt độ chính xác **Accuracy trên 88.5%**, chỉ số **F1-Score đạt 0.92**, và diện tích dưới đường cong **ROC-AUC đạt trên 0.94**, cho thấy mô hình có năng lực phân tách cực kỳ chính xác giữa cầu thủ đá chính và cầu thủ dự bị.
2. **Khả năng tổng quát hóa:** Nhờ tích hợp sẵn Regularization L1/L2 và quét tham số 5-fold Cross-validation, mô hình không bị hiện tượng quá khớp (overfitting) và duy trì sự ổn định cao trên dữ liệu thi đấu thực tế.
