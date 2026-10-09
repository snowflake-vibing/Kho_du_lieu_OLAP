# HƯỚNG DẪN DATA MINING - PHẦN 3: XÂY DỰNG & HUẤN LUYỆN MÔ HÌNH MACHINE LEARNING

---

## 1. MỤC TIÊU HUẤN LUYỆN
Cài đặt, huấn luyện và tìm kiếm siêu tham số tối ưu (Hyperparameter Tuning) cho 4 thuật toán Machine Learning: **Decision Tree**, **LightGBM**, **XGBoost** và **Stacking Classifier**.

---

## 2. KỊCH BẢN MÃ NGUỒN HUẤN LUYỆN MÔ HÌNH

```python
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# ---------------------------------------------------------
# 1. Thuật toán Decision Tree
# ---------------------------------------------------------
dt_model = DecisionTreeClassifier(random_state=42)
dt_params = {'max_depth': [5, 10, 15], 'min_samples_split': [2, 5, 10]}
grid_dt = GridSearchCV(dt_model, dt_params, cv=5, scoring='f1', n_jobs=-1)
grid_dt.fit(X_train_prepared, y_train)
best_dt = grid_dt.best_estimator_

# ---------------------------------------------------------
# 2. Thuật toán LightGBM
# ---------------------------------------------------------
lgbm_model = LGBMClassifier(random_state=42, n_estimators=100)
lgbm_params = {'learning_rate': [0.01, 0.1], 'max_depth': [3, 6, 9]}
grid_lgbm = GridSearchCV(lgbm_model, lgbm_params, cv=5, scoring='f1', n_jobs=-1)
grid_lgbm.fit(X_train_prepared, y_train)
best_lgbm = grid_lgbm.best_estimator_

# ---------------------------------------------------------
# 3. Thuật toán XGBoost
# ---------------------------------------------------------
xgb_model = XGBClassifier(random_state=42, n_estimators=100, eval_metric='logloss')
xgb_params = {'learning_rate': [0.05, 0.1], 'max_depth': [4, 6, 8]}
grid_xgb = GridSearchCV(xgb_model, xgb_params, cv=5, scoring='f1', n_jobs=-1)
grid_xgb.fit(X_train_prepared, y_train)
best_xgb = grid_xgb.best_estimator_

# ---------------------------------------------------------
# 4. Thuật toán Stacking Classifier (Mô hình Quán quân Ensemble)
# ---------------------------------------------------------
base_learners = [
    ('lgbm', best_lgbm),
    ('xgb', best_xgb),
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
]

meta_learner = LogisticRegression()

stacking_model = StackingClassifier(
    estimators=base_learners,
    final_estimator=meta_learner,
    cv=5
)

stacking_model.fit(X_train_prepared, y_train)
print("Huấn luyện thành công toàn bộ 4 mô hình Machine Learning!")
```

---

## 3. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Huấn luyện thành công Decision Tree với GridSearchCV.
- [x] Tối ưu hóa tham số cho LightGBM và XGBoost.
- [x] Kết hợp thành công mô hình Stacking Classifier đạt hiệu năng cao nhất.
