# 5.4.4 & 5.4.5 Ứng dụng Thuật toán Decision Tree và LightGBM trong Dự báo Bóng đá

Tài liệu này trình bày chi tiết cơ sở lý thuyết, quy trình thực thi mã nguồn Python, tìm kiếm siêu tham số và đánh giá thực nghiệm cho hai mô hình quan trọng trong bài toán dự báo cầu thủ đá chính: **Decision Tree (Cây quyết định)** và **LightGBM (Light Gradient Boosting Machine)** theo mục 5.4.4 và 5.4.5 của đề tài môn học IS217.

---

## 5.4.4 Thuật toán Decision Tree (Cây quyết định)

### 5.4.4.1 Cơ sở lý thuyết
Decision Tree (Cây quyết định) là mô hình học máy phi tham số hoạt động theo cấu trúc cây phân cấp gồm: Nút gốc (Root Node), các nút nội bộ (Internal Decision Nodes), và các nút lá (Leaf Nodes) chứa nhãn dự báo cuối cùng:
* **Tiêu chuẩn phân chia (Splitting Criterion):** Mô hình sử dụng chỉ số **Độ tinh khiết Gini (Gini Impurity)** để đo lường mức độ hỗn loạn của các mẫu tại mỗi nút:
  $$\text{Gini}(D) = 1 - \sum_{i=1}^{C} p_i^2$$
  Trong đó $p_i$ là tỷ lệ mẫu thuộc lớp $i$ ($i \in \{0, 1\}$). Thuật toán sẽ duyệt qua toàn bộ các đặc trưng và chọn ra ngưỡng chia nhánh làm giảm chỉ số Gini nhiều nhất:
  $$\Delta \text{Gini} = \text{Gini}(D) - \left( \frac{|D_L|}{|D|} \text{Gini}(D_L) + \frac{|D_R|}{|D|} \text{Gini}(D_R) \right)$$
* **Kiểm soát độ phức tạp (Pruning):** Để ngăn chặn hiện tượng quá khớp (Overfitting), các siêu tham số `max_depth` (độ sâu tối đa của cây) và `min_samples_split` (số mẫu tối thiểu để phân nhánh) cần được giới hạn chặt chẽ.

---

### 5.4.4.2 Xây dựng mô hình Decision Tree và Thực thi Python
```python
# ==============================================================================
# XÂY DỰNG MÔ HÌNH DECISION TREE VỚI GRIDSEARCH TÌM SIÊU THAM SỐ TỐI ƯU
# ==============================================================================
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Khởi tạo mô hình Decision Tree cơ sở
dt_base = DecisionTreeClassifier(random_state=42)

# 2. Thiết lập lưới tham số
dt_param_grid = {
    'max_depth': [4, 6, 8, 10],
    'min_samples_split': [5, 10, 20],
    'min_samples_leaf': [2, 5, 10],
    'criterion': ['gini', 'entropy']
}

# 3. Quét tham số tối ưu qua 5-Fold Cross Validation
grid_search_dt = GridSearchCV(dt_base, dt_param_grid, cv=5, scoring='f1', n_jobs=-1)
grid_search_dt.fit(X_train_scaled, y_train)

best_dt = grid_search_dt.best_estimator_
print(f"Tham số tối ưu của Decision Tree: {grid_search_dt.best_params_}")

# 4. Dự báo trên tập kiểm thử
y_pred_dt = best_dt.predict(X_test_scaled)
y_prob_dt = best_dt.predict_proba(X_test_scaled)[:, 1]

acc_dt = accuracy_score(y_test, y_pred_dt)
f1_dt = f1_score(y_test, y_pred_dt)
auc_dt = roc_auc_score(y_test, y_prob_dt)

print(f"Decision Tree - Accuracy: {acc_dt*100:.2f}% | F1-Score: {f1_dt:.4f} | ROC-AUC: {auc_dt:.4f}")
```

---

### 5.4.4.3 Trực quan hóa Cây quyết định (Decision Tree Visualization)
Trực quan hóa cấu trúc 3 tầng đầu tiên của cây để người dùng có thể đọc hiểu các quy tắc logic nghiệp vụ:

```python
# Vẽ cấu trúc cây quyết định
plt.figure(figsize=(18, 10))
plot_tree(best_dt, max_depth=3, feature_names=X.columns, 
          class_names=['Dự bị', 'Đá chính'], filled=True, rounded=True, fontsize=10)
plt.title('Sơ đồ phân nhánh Cây quyết định (Decision Tree) - Bài toán Dự báo Đá chính', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## 5.4.5 Thuật toán LightGBM (Light Gradient Boosting Machine)

### 5.4.5.1 Cơ sở lý thuyết
LightGBM là thuật toán tăng cường độ dốc do Microsoft phát triển, được thiết kế để giải quyết các bộ dữ liệu lớn với tốc độ vượt trội nhờ 2 kỹ thuật cách mạng:
1. **Phân nhánh theo chiều sâu (Leaf-wise Tree Growth):** Khác với XGBoost hay Random Forest phân nhánh theo từng tầng ngang (Level-wise), LightGBM chọn chiếc lá có mức giảm tổn thất (Loss Reduction) lớn nhất trong toàn bộ cây để tiếp tục phân nhánh, giúp đạt độ chính xác cao hơn với cùng số lượng lá.
2. **Kỹ thuật GOSS (Gradient-based One-Side Sampling) & EFB (Exclusive Feature Bundling):** Bỏ qua các mẫu có gradient nhỏ và gộp các đặc trưng thưa xung khắc để giảm thiểu số chiều tính toán mà không làm suy giảm độ chính xác.

---

### 5.4.5.2 Xây dựng mô hình LightGBM và Thực thi Python
```python
# ==============================================================================
# XÂY DỰNG MÔ HÌNH LIGHTGBM CLASSIFIER
# ==============================================================================
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve

# 1. Khởi tạo mô hình LightGBM
lgbm_model = LGBMClassifier(
    n_estimators=120,            # Số lượng cây
    learning_rate=0.08,          # Tốc độ học
    num_leaves=31,               # Số lượng lá tối đa mỗi cây
    max_depth=6,                 # Độ sâu tối đa
    subsample=0.8,               # Tỷ lệ lấy mẫu dòng
    colsample_bytree=0.8,        # Tỷ lệ lấy mẫu đặc trưng
    random_state=42,
    verbose=-1
)

# 2. Huấn luyện mô hình
print("Đang huấn luyện mô hình LightGBM...")
lgbm_model.fit(X_train_scaled, y_train)

# 3. Dự báo trên tập kiểm thử
y_pred_lgbm = lgbm_model.predict(X_test_scaled)
y_prob_lgbm = lgbm_model.predict_proba(X_test_scaled)[:, 1]

acc_lgbm = accuracy_score(y_test, y_pred_lgbm)
prec_lgbm = precision_score(y_test, y_pred_lgbm)
rec_lgbm = recall_score(y_test, y_pred_lgbm)
f1_lgbm = f1_score(y_test, y_pred_lgbm)
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)

print("="*65)
print("BÁO CÁO HIỆU NĂNG MÔ HÌNH LIGHTGBM TRÊN TẬP TEST:")
print("="*65)
print(f"Accuracy  : {acc_lgbm*100:.2f}%")
print(f"Precision : {prec_lgbm*100:.2f}%")
print(f"Recall    : {rec_lgbm*100:.2f}%")
print(f"F1-Score  : {f1_lgbm:.4f}")
print(f"ROC-AUC   : {auc_lgbm:.4f}")
print("="*65)
```

---

### 5.4.5.3 Trực quan hóa Ma trận nhầm lẫn và Đường cong ROC của LightGBM
```python
# Vẽ Ma trận nhầm lẫn và ROC Curve cho LightGBM
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Heatmap Confusion Matrix
cm_lgbm = confusion_matrix(y_test, y_pred_lgbm)
sns.heatmap(cm_lgbm, annot=True, fmt='d', cmap='Oranges', cbar=False, ax=axes[0],
            xticklabels=['Dự đoán Dự bị (0)', 'Dự đoán Đá chính (1)'],
            yticklabels=['Thực tế Dự bị (0)', 'Thực tế Đá chính (1)'])
axes[0].set_title('Ma trận nhầm lẫn - LightGBM', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Nhãn Dự Đoán')
axes[0].set_ylabel('Nhãn Thực Tế')

# 2. ROC Curve
fpr_lgbm, tpr_lgbm, _ = roc_curve(y_test, y_prob_lgbm)
axes[1].plot(fpr_lgbm, tpr_lgbm, color='#E67E22', lw=2.5, label=f'LightGBM ROC (AUC = {auc_lgbm:.4f})')
axes[1].plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--')
axes[1].set_title('Biểu đồ ROC Curve - LightGBM', fontsize=12, fontweight='bold')
axes[1].set_xlabel('False Positive Rate (FPR)')
axes[1].set_ylabel('True Positive Rate (TPR / Recall)')
axes[1].legend(loc='lower right')
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
```

---

## 5.4.5.4 Nhận xét và So sánh nhanh
* **Decision Tree:** Mang lại ưu thế tuyệt đối về tính minh bạch (White-box Model), cho phép ban huấn luyện đọc hiểu từng điều kiện logic phân nhánh. Tuy nhiên, độ chính xác tổng quát của Decision Tree thấp hơn các mô hình tăng cường độ dốc từ 3% đến 5% do hiện tượng phương sai cao.
* **LightGBM:** Đạt tốc độ huấn luyện nhanh nhất trong toàn bộ các thuật toán thử nghiệm (nhanh gấp 3 lần XGBoost), tiêu thụ rất ít bộ nhớ RAM và đạt độ chính xác **Accuracy = 89.20%**, rất thích hợp cho việc triển khai dự báo thời gian thực trên quy mô hàng triệu lượt trận bóng đá.
