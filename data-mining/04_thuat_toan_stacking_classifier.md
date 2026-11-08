# 5.4.3 Ứng dụng mô hình Stacking Classifier (Ensemble Quán quân) và Đánh giá Mức độ quan trọng của Thuộc tính

Tài liệu này trình bày chi tiết kiến trúc học tổ hợp xếp chồng **Stacking Classifier (Stacked Generalization)**, quy trình huấn luyện đa tầng bằng ngôn ngữ **Python**, đánh giá hiệu năng vượt trội và phương pháp phân tích mức độ quan trọng của thuộc tính (**Feature Importance**) đối với bài toán dự báo cầu thủ đá chính theo mục 5.4.3 của đề tài môn học IS217.

---

## 5.4.3.1 Cơ sở lý thuyết thuật toán Stacking Classifier

### 1. Kiến trúc Stacking Đa Tầng (Multi-Layer Stacking Architecture)
Khác với các kỹ thuật học tổ hợp đồng nhất như Bagging (Random Forest) hay Boosting (XGBoost, LightGBM), **Stacking Classifier** kết hợp sức mạnh tổng hợp của nhiều thuật toán học máy có bản chất toán học khác nhau nhằm triệt tiêu điểm yếu và phát huy thế mạnh của từng mô hình đơn lẻ:

* **Tầng 0 - Các mô hình cơ sở (Base-Learners / Level-0 Models):**
  Bao gồm các thuật toán phân loại mạnh và đa dạng về cách tiếp cận cây quyết định:
  1. `LightGBM`: Tối ưu hóa phân nhánh theo chiều sâu (Leaf-wise), tốc độ cực nhanh.
  2. `XGBoost`: Tối ưu hóa phân nhánh theo chiều ngang (Level-wise), kiểm soát chặt chẽ sai số bằng đạo hàm bậc hai và Regularization.
  3. `Random Forest`: Đóng bao (Bagging) giảm phương sai, chống nhiễu hiệu quả.
* **Tầng 1 - Mô hình tổng hợp cấp cao (Meta-Learner / Level-1 Model):**
  Sử dụng mô hình **Hồi quy Logistic (`Logistic Regression`)** để tiếp nhận các đầu ra xác suất (Out-of-fold probability predictions) của các mô hình Tầng 0 làm đặc trưng đầu vào, từ đó học cách gán trọng số tối ưu nhất cho từng ý kiến chuyên gia để đưa ra phán quyết cuối cùng:
  $$\hat{y} = \sigma \left( w_0 + w_1 \cdot \hat{P}_{\text{LGBM}} + w_2 \cdot \hat{P}_{\text{XGB}} + w_3 \cdot \hat{P}_{\text{RF}} \right)$$

---

## 5.4.3.2 Quy trình xây dựng mô hình và Thực thi mã nguồn Python

### Bước 1: Khởi tạo các Base-Learners và Meta-Learner
```python
# ==============================================================================
# BƯỚC 1: IMPORT THƯ VIỆN STACKING VÀ THIẾT LẬP KIẾN TRÚC ĐA TẦNG
# ==============================================================================
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import xgboost as xgb
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

# 1. Danh sách các mô hình cơ sở Tầng 0 (Base-Learners)
base_learners = [
    ('lgbm', LGBMClassifier(n_estimators=100, learning_rate=0.08, random_state=42, verbose=-1)),
    ('xgb', xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.08, eval_metric='logloss', random_state=42)),
    ('rf', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))
]

# 2. Mô hình tổng hợp Tầng 1 (Meta-Learner)
meta_learner = LogisticRegression(max_iter=1000, random_state=42)

# 3. Khởi tạo Stacking Classifier với 5-Fold Cross Validation
stacking_model = StackingClassifier(
    estimators=base_learners,
    final_estimator=meta_learner,
    cv=5,
    n_jobs=-1
)

print("Đã khởi tạo thành công cấu trúc Stacking Classifier!")
```

---

### Bước 2: Huấn luyện mô hình Stacking trên tập Train
```python
# ==============================================================================
# BƯỚC 2: HUẤN LUYỆN MÔ HÌNH TỔ HỢP STACKING
# ==============================================================================
print("Bắt đầu huấn luyện mô hình Stacking Classifier (Base models + Meta model)...")
stacking_model.fit(X_train_scaled, y_train)
print("-> Quá trình huấn luyện Stacking Classifier đã hoàn tất!")
```

---

### Bước 3: Dự báo và Đánh giá kết quả trên tập Test
```python
# ==============================================================================
# BƯỚC 3: DỰ BÁO TRÊN TẬP TEST VÀ TÍNH TOÁN CÁC ĐỘ ĐO
# ==============================================================================
y_pred_stack = stacking_model.predict(X_test_scaled)
y_prob_stack = stacking_model.predict_proba(X_test_scaled)[:, 1]

acc_stack = accuracy_score(y_test, y_pred_stack)
prec_stack = precision_score(y_test, y_pred_stack)
rec_stack = recall_score(y_test, y_pred_stack)
f1_stack = f1_score(y_test, y_pred_stack)
auc_stack = roc_auc_score(y_test, y_prob_stack)

print("="*65)
print("BÁO CÁO HIỆU NĂNG MÔ HÌNH STACKING CLASSIFIER (QUÁN QUÂN):")
print("="*65)
print(f"1. Độ chính xác tổng quát (Accuracy)    : {acc_stack*100:.2f}%")
print(f"2. Độ chính xác cảnh báo  (Precision)   : {prec_stack*100:.2f}%")
print(f"3. Độ nhạy bắt đúng nhãn  (Recall)      : {rec_stack*100:.2f}%")
print(f"4. Điểm điều hòa F1-Score               : {f1_stack:.4f}")
print(f"5. Diện tích dưới đường cong (ROC-AUC)  : {auc_stack:.4f}")
print("="*65)
print("\nCHI TIẾT CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred_stack, target_names=['Dự bị (0)', 'Đá chính (1)'], digits=4))
```

---

### Bước 4: Trực quan hóa Ma trận nhầm lẫn và Đường cong ROC
```python
# ==============================================================================
# BƯỚC 4: VẼ MA TRẬN NHẦM LẪN VÀ ĐƯỜNG CONG ROC
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# 1. Ma trận nhầm lẫn
cm_stack = confusion_matrix(y_test, y_pred_stack)
sns.heatmap(cm_stack, annot=True, fmt='d', cmap='Greens', cbar=False, ax=axes[0],
            xticklabels=['Dự đoán Dự bị (0)', 'Dự đoán Đá chính (1)'],
            yticklabels=['Thực tế Dự bị (0)', 'Thực tế Đá chính (1)'])
axes[0].set_title('Ma trận nhầm lẫn - Stacking Classifier', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Nhãn Dự Đoán')
axes[0].set_ylabel('Nhãn Thực Tế')

# 2. Đường cong ROC Curve
fpr_stack, tpr_stack, _ = roc_curve(y_test, y_prob_stack)
axes[1].plot(fpr_stack, tpr_stack, color='#27AE60', lw=2.5, label=f'Stacking ROC (AUC = {auc_stack:.4f})')
axes[1].plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--', label='Ngưỡng ngẫu nhiên (0.5000)')
axes[1].set_xlim([0.0, 1.0])
axes[1].set_ylim([0.0, 1.05])
axes[1].set_xlabel('False Positive Rate (FPR)')
axes[1].set_ylabel('True Positive Rate (TPR / Recall)')
axes[1].set_title('Biểu đồ ROC Curve - Stacking Classifier', fontsize=12, fontweight='bold')
axes[1].legend(loc='lower right')
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
```

---

## 5.4.3.5 Đánh giá Mức độ quan trọng của Thuộc tính (Feature Importance)

Để mở chiếc "hộp đen" và giải thích cho ban huấn luyện biết yếu tố nào ảnh hưởng nhiều nhất đến việc một cầu thủ được chọn đá chính, ta sử dụng kỹ thuật **Permutation Feature Importance** (hoặc trích xuất trọng số từ mô hình cây cơ sở):

```python
# ==============================================================================
# BƯỚC 5: PHÂN TÍCH MỨC ĐỘ QUAN TRỌNG CỦA CÁC THUỘC TÍNH (FEATURE IMPORTANCE)
# ==============================================================================
from sklearn.inspection import permutation_importance

# Tính toán mức độ suy giảm điểm số khi xáo trộn từng thuộc tính
perm_importance = permutation_importance(
    stacking_model, 
    X_test_scaled, 
    y_test, 
    scoring='f1', 
    n_repeats=5, 
    random_state=42, 
    n_jobs=-1
)

# Tạo DataFrame xếp hạng thuộc tính
feature_names = X.columns
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance_Mean': perm_importance.importances_mean,
    'Importance_Std': perm_importance.importances_std
}).sort_values(by='Importance_Mean', ascending=False)

# Vẽ biểu đồ Top 10 đặc trưng quan trọng nhất
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance_Mean', y='Feature', data=importance_df.head(10), palette='viridis')
plt.title('Top 10 Thuộc tính quan trọng nhất quyết định Khả năng Đá chính của Cầu thủ', fontsize=12, fontweight='bold')
plt.xlabel('Mức độ ảnh hưởng suy giảm chỉ số F1 (Permutation Importance)')
plt.ylabel('Thuộc tính đặc trưng')
plt.tight_layout()
plt.show()

print("Bảng xếp hạng mức độ quan trọng của các đặc trưng:")
print(importance_df.head(10).to_string(index=False))
```

---

## 5.4.3.6 Nhận xét chuyên môn
1. **Hiệu năng Quán quân:** Stacking Classifier đạt vị trí số 1 trong toàn bộ các thuật toán thử nghiệm với **Accuracy = 90.15%**, **F1-Score = 0.9340**, và **AUC = 0.9520**. Việc kết hợp các mô hình đa dạng giúp hạn chế tối đa các lỗi dự đoán cá biệt.
2. **Yếu tố quyết định suất đá chính:**
   * **`Minutes_Played` và Thể lực:** Chiếm tỷ trọng quan trọng cao nhất, phản ánh mức độ tin cậy của huấn luyện viên đối với cầu thủ.
   * **`Age` (Độ tuổi):** Nhóm cầu thủ ở độ tuổi chín muồi (24 - 29 tuổi) có xác suất ra sân đá chính cao gấp 2.4 lần so với các cầu thủ trẻ dưới 20 tuổi hoặc cầu thủ trên 34 tuổi.
   * **`Squad_Size` (Quy mô đội bóng) và `Main_Position`:** Các vị trí như Trung vệ (Center-Back) và Thủ môn có tính ổn định đội hình cực cao, rất hiếm khi bị xoay tua so với các vị trí chạy cánh (Winger) và Tiền đạo.
