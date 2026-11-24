# 5.3–5.4 Chuẩn bị dữ liệu và huấn luyện mô hình

## Chia tập theo thời gian

| Tập | Năm | Mục đích |
| --- | --- | --- |
| Huấn luyện | 2022 | Học bộ mã hóa và mô hình cơ sở |
| Tập cho mô hình tầng hai | 2023 | Tạo xác suất ngoài tập huấn luyện của mô hình cơ sở để huấn luyện Stacking |
| Kiểm tra | 2024 | Đánh giá cuối cùng với cùng tập và cùng ngưỡng cho mọi mô hình |

Tách cả trận theo thời gian để một trận chỉ xuất hiện trong một tập. Mã hóa one-hot chỉ học danh mục từ năm 2022 và bỏ qua danh mục mới khi biến đổi. Số phút, bàn thắng, kiến tạo và thẻ của chính trận cần dự đoán được loại khỏi tập đặc trưng. ID trận và cầu thủ chỉ dùng kiểm tra dữ liệu.

## Mô hình

| Mô hình | Cách sử dụng |
| --- | --- |
| Baseline | Dùng tỷ lệ lớp dương từ tập huấn luyện làm xác suất cho mọi mẫu |
| Decision Tree | Giới hạn độ sâu 6 và tối thiểu 100 mẫu mỗi lá |
| XGBoost | Boosting với 120 cây, độ sâu 4 và tốc độ học 0,05 |
| LightGBM | Boosting với 120 cây, tối đa 15 lá và tối thiểu 100 mẫu một lá |
| Stacking Classifier | Dùng Logistic Regression học từ xác suất của ba mô hình cơ sở trên năm 2023 |

Thí nghiệm dùng cấu hình cố định. Tập 2024 chỉ được dùng để đánh giá. Nối tiếp [khối tiền xử lý](01_mo_ta_va_tien_xu_ly.md) với đoạn mã sau.

```python
columns = ["competition_id", "venue_role", "match_month"]
train, calibration, test = (data.loc[data["year"].eq(year)] for year in (2022, 2023, 2024))
assert not set(train["game_id"]) & set(calibration["game_id"])
assert not (set(train["game_id"]) | set(calibration["game_id"])) & set(test["game_id"])
encoder = ColumnTransformer([("context", OneHotEncoder(handle_unknown="ignore"), columns)])
x_train = encoder.fit_transform(train[columns])
x_calibration = encoder.transform(calibration[columns])
x_test = encoder.transform(test[columns])
target = "is_starter_proxy"
y_train, y_calibration, y_test = (frame[target] for frame in (train, calibration, test))

models = {
    "Baseline": DummyClassifier(strategy="prior"),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, min_samples_leaf=100, random_state=42),
    "XGBoost": xgboost.XGBClassifier(
        n_estimators=120, max_depth=4, learning_rate=0.05,
        eval_metric="logloss", random_state=42, n_jobs=2,
    ),
    "LightGBM": lightgbm.LGBMClassifier(
        n_estimators=120, num_leaves=15, learning_rate=0.05,
        min_child_samples=100, random_state=42, n_jobs=2, verbosity=-1,
    ),
}
base_calibration = {}
base_test = {}
for name, model in models.items():
    model.fit(x_train, y_train)
    base_calibration[name] = model.predict_proba(x_calibration)[:, 1]
    base_test[name] = model.predict_proba(x_test)[:, 1]

base_names = ["Decision Tree", "XGBoost", "LightGBM"]
stack = LogisticRegression(random_state=42)
stack.fit(np.column_stack([base_calibration[name] for name in base_names]), y_calibration)
base_test["Stacking Classifier"] = stack.predict_proba(
    np.column_stack([base_test[name] for name in base_names])
)[:, 1]
```
