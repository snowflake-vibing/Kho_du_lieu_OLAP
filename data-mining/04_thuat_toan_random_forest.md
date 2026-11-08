# 5.3.2 Ứng dụng mô hình thuật toán Random Forest và So sánh hiệu năng mô hình

Tài liệu này trình bày chi tiết cơ sở lý thuyết, quy trình thực thi mã nguồn Python, kết quả thực nghiệm của thuật toán **Random Forest**, đồng thời thực hiện phân tích so sánh đối chiếu đa chiều giữa **Random Forest** và **XGBoost Classifier** theo mục 5.3.2 của tài liệu môn học IS217.

---

## 5.3.2.1 Cơ sở lý thuyết thuật toán Random Forest

### 1. Nguyên lý hoạt động cốt lõi
Random Forest (Rừng ngẫu nhiên) là thuật toán học máy có giám sát thuộc nhóm học tổ hợp (Ensemble Learning), hoạt động dựa trên sự kết hợp của hai kỹ thuật nền tảng:
1. **Bootstrap Aggregating (Bagging):** Tạo ra $B$ tập dữ liệu con (Bootstrap samples) bằng phương pháp lấy mẫu ngẫu nhiên có hoàn lại (Sampling with replacement) từ tập huấn luyện gốc. Mỗi cây quyết định (Decision Tree) trong rừng sẽ được huấn luyện độc lập trên một tập mẫu con này.
2. **Phương pháp Không gian con ngẫu nhiên (Random Subspace Method):** Tại mỗi nút (node) trong quá trình phát triển của một cây, thuật toán chỉ chọn ngẫu nhiên một tập con gồm $m$ đặc trưng (thông thường $m = \sqrt{p}$, với $p$ là tổng số đặc trưng ban đầu) để tìm ra thuộc tính phân chia tốt nhất (dựa trên chỉ số Gini Impurity hoặc Entropy), thay vì quét qua toàn bộ các thuộc tính.

**Cơ chế dự đoán cuối cùng (Majority Voting):**
Sau khi toàn bộ $B$ cây trong rừng đã được huấn luyện, khi có một mẫu kiểm thử mới $x$, mỗi cây $T_b$ sẽ đưa ra một phiếu bầu (Vote) về nhãn lớp dự đoán $\hat{y}_b$. Quyết định phân loại cuối cùng của toàn bộ rừng được xác định thông qua nguyên tắc biểu quyết theo đa số:
$$\hat{y} = \text{mode} \left\{ \hat{y}_1, \hat{y}_2, \dots, \hat{y}_B \right\}$$
Hoặc lấy giá trị xác suất trung bình:
$$P(y = 1 | x) = \frac{1}{B} \sum_{b=1}^{B} P_b(y = 1 | x)$$

---

### 2. Ưu điểm và Hạn chế của Random Forest

#### Ưu điểm:
* **Khả năng giảm phương sai (Variance Reduction):** Nhờ việc tổng hợp ý kiến từ hàng trăm cây quyết định có độ tương quan thấp (Low Correlation), Random Forest giảm thiểu đáng kể hiện tượng quá khớp (Overfitting) so với một cây quyết định đơn lẻ.
* **Độ bền vững cao:** Hoạt động ổn định trên các tập dữ liệu có số chiều lớn mà không đòi hỏi phải cắt tỉa cây (Pruning).
* **Đánh giá mức độ quan trọng của đặc trưng (Feature Importance):** Cho phép đo lường mức độ suy giảm chỉ số Gini (Mean Decrease Gini) của từng biến trong toàn bộ quá trình chia nhánh.

#### Hạn chế:
* **Chi phí tài nguyên và Tốc độ suy luận:** Việc lưu trữ và tính toán dự đoán qua hàng trăm cây tốn nhiều bộ nhớ RAM và có độ trễ lớn hơn các mô hình tuyến tính đơn giản.
* **Hiện tượng thiên lệch lớp đa số (Majority Class Bias):** Khi đối mặt với tập dữ liệu mất cân bằng nghiêm trọng (tỷ lệ lớp gian lận cực thấp), các cây thành phần trong Random Forest có xu hướng ưu tiên chia nhánh để tối ưu độ chính xác tổng thể, dẫn đến việc bỏ sót hoặc đánh giá thấp các trường hợp thuộc lớp thiểu số nếu không can thiệp trọng số lớp (`class_weight='balanced'`).

---

## 5.3.2.2 Quy trình xây dựng mô hình và Thực thi mã nguồn Python

Để đảm bảo tính công bằng và khách quan khi so sánh, mô hình Random Forest được huấn luyện trên cùng một tập dữ liệu phân chia $X\_train, y\_train, X\_test, y\_test$ đã sử dụng ở mô hình XGBoost Classifier.

### Bước 1 & Bước 2: Khởi tạo và Huấn luyện mô hình Random Forest
```python
# ==============================================================================
# BƯỚC 1 & 2: KHỞI TẠO VÀ HUẤN LUYỆN MÔ HÌNH RANDOM FOREST
# ==============================================================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix, 
    classification_report, 
    roc_curve, 
    auc, 
    roc_auc_score
)
import matplotlib.pyplot as plt
import seaborn as sns

# Khởi tạo mô hình Random Forest với 100 cây quyết định
rf_model = RandomForestClassifier(
    n_estimators=100,             # Số lượng cây trong rừng
    max_depth=None,               # Phát triển cây tối đa cho đến khi các lá thuần nhất
    min_samples_split=2,          # Số mẫu tối thiểu để tiếp tục phân nhánh
    min_samples_leaf=1,           # Số mẫu tối thiểu tại nút lá
    random_state=42,              # Cố định seed ngẫu nhiên
    n_jobs=-1                     # Sử dụng toàn bộ nhân CPU tính toán song song
)

print("Bắt đầu huấn luyện Random Forest...")
rf_model.fit(X_train, y_train)
print("-> Huấn luyện Random Forest hoàn tất!")
```

---

### Bước 3: Tính toán và Vẽ Ma trận nhầm lẫn (Confusion Matrix)
```python
# ==============================================================================
# BƯỚC 3: DỰ BÁO VÀ VẼ MA TRẬN NHẦM LẪN (RANDOM FOREST)
# ==============================================================================
y_pred_rf = rf_model.predict(X_test)

# Tính toán ma trận nhầm lẫn
cm_rf = confusion_matrix(y_test, y_pred_rf)
tn_rf, fp_rf, fn_rf, tp_rf = cm_rf.ravel()

print("="*60)
print("MA TRẬN NHẦM LẪN (CONFUSION MATRIX) - RANDOM FOREST")
print("="*60)
print(f"True Negative  (TN - Đúng bình thường) : {tn_rf:,}")
print(f"False Positive (FP - Báo động giả)      : {fp_rf:,}")
print(f"False Negative (FN - Bỏ sót rủi ro)     : {fn_rf:,}")
print(f"True Positive  (TP - Bắt trúng gian lận): {tp_rf:,}")
print("="*60)

print("\nBÁO CÁO ĐỘ ĐO PHÂN LOẠI RANDOM FOREST:")
print(classification_report(y_test, y_pred_rf, target_names=['Bình thường (0)', 'Gian lận (1)'], digits=4))

# Vẽ đồ thị Heatmap cho Ma trận nhầm lẫn
plt.figure(figsize=(7, 5))
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', cbar=False,
            xticklabels=['Dự đoán 0 (Bình thường)', 'Dự đoán 1 (Gian lận)'],
            yticklabels=['Thực tế 0 (Bình thường)', 'Thực tế 1 (Gian lận)'])
plt.title('Ma trận nhầm lẫn - Mô hình Random Forest', fontsize=12, fontweight='bold')
plt.xlabel('Nhãn Dự Đoán')
plt.ylabel('Nhãn Thực Tế')
plt.tight_layout()
plt.show()
```

---

### Bước 4: Dự đoán xác suất, Tính toán và Vẽ đường cong ROC-AUC
```python
# ==============================================================================
# BƯỚC 4: TÍNH TOÁN ROC VÀ VẼ BIỂU ĐỒ ĐÁNH GIÁ HIỆU NĂNG AUC
# ==============================================================================
# Dự đoán xác suất nhãn lớp 1
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

# Tính toán điểm ROC
fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, y_prob_rf)
roc_auc_rf = auc(fpr_rf, tpr_rf)

print(f"-> Chỉ số diện tích dưới đường cong AUC của Random Forest: {roc_auc_rf:.4f}")

# Vẽ đồ thị đường cong ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr_rf, tpr_rf, color='#2ca02c', lw=2.5, label=f'Random Forest ROC (AUC = {roc_auc_rf:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=1.5, linestyle='--', label='Ngưỡng ngẫu nhiên (AUC = 0.5000)')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tỷ lệ Báo động giả (False Positive Rate - FPR)', fontsize=11)
plt.ylabel('Tỷ lệ Bắt trúng rủi ro (True Positive Rate - TPR / Recall)', fontsize=11)
plt.title('Biểu đồ ROC Curve đánh giá hiệu năng Random Forest', fontsize=12, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
```

---

## 5.3.2.3 So sánh đối chiếu toàn diện giữa XGBoost và Random Forest

Dưới đây là bảng tổng hợp các chỉ số định lượng đo lường thực tế giữa hai mô hình trên cùng một tập kiểm thử:

| Tiêu chí đánh giá / Chỉ số | Mô hình XGBoost Classifier | Mô hình Random Forest | Chênh lệch & Đánh giá |
| :--- | :---: | :---: | :--- |
| **Diện tích dưới đường cong (AUC)** | **0.4959** | 0.4936 | XGBoost nhỉnh hơn (+0.0023), cả hai đều xấp xỉ mức ngẫu nhiên |
| **Độ nhạy bắt gian lận (Recall - Lớp 1)** | 0.1700 (17%) | **0.2700 (27%)** | **Random Forest vượt trội (+10%)**, bắt thêm được 189 ca gian lận |
| **Số ca gian lận bắt trúng (True Positive - TP)** | 342 ca | **536 ca** | Random Forest bắt trúng nhiều hơn |
| **Số ca gian lận bị bỏ sót (False Negative - FN)** | 1,671 ca | **1,477 ca** | Random Forest bỏ sót ít hơn 194 ca |
| **Số ca báo động giả (False Positive - FP)** | **6,695 ca** | 10,091 ca | **XGBoost tối ưu hơn nhiều**, ít hơn **3,396** ca làm phiền khách hàng |
| **Độ chính xác cảnh báo (Precision - Lớp 1)** | 0.0500 (5%) | 0.0500 (5%) | Tương đương nhau ở mức thấp do mất cân bằng lớp |
| **Tốc độ huấn luyện và tối ưu bộ nhớ** | **Rất nhanh (Song song)** | Chậm hơn, tốn nhiều RAM | XGBoost tối ưu tài nguyên tốt hơn |

### Phân tích chuyên sâu về bài toán đánh đổi trong vận hành thực tế:
1. **Ưu thế về khả năng "bắt tội phạm" của Random Forest:**
   * Random Forest thể hiện độ nhạy (Recall) cao hơn đáng kể (0.27 so với 0.17 của XGBoost), giúp hệ thống nhận diện được 536 vụ việc gian lận so với 342 vụ của XGBoost. Điều này giúp ngăn chặn thêm được một lượng thất thoát tài sản thực tế cho ngân hàng.
2. **Cái giá phải trả về tỷ lệ Báo động giả (False Positive Alarm):**
   * Tuy nhiên, sự gia tăng về độ nhạy của Random Forest đi kèm với một hệ quả tiêu cực rất lớn: Mô hình này đã phân loại nhầm tới **10,091 giao dịch bình thường thành gian lận** (so với 6,695 ca của XGBoost).
   * Trong thực tế vận hành ngân hàng, việc khóa tài khoản hoặc chặn giao dịch nhầm tới hơn 10,000 khách hàng vô tội sẽ gây bức xúc nghiêm trọng, làm tắc nghẽn bộ phận chăm sóc khách hàng (Call Center) và gia tăng chi phí vận hành.
3. **Kết luận lựa chọn mô hình:**
   * **Xét về hiệu quả vận hành tổng thể:** **XGBoost Classifier** là sự lựa chọn hợp lý hơn nhờ khả năng kiểm soát số lượng cảnh báo giả tốt hơn nhiều, đồng thời hỗ trợ cơ chế gán trọng số linh hoạt để tinh chỉnh ngưỡng phân loại (Threshold Tuning) theo từng giai đoạn kinh doanh.
