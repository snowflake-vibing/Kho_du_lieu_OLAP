# 5.4 So sánh và đánh giá mô hình

## Kết quả trên tập kiểm tra năm 2024

Bảng dưới đây được tính trên 145.640 lượt ra sân. Accuracy, Precision, Recall và F1 dùng ngưỡng 0,5 cho lớp thi đấu từ 60 phút trở lên. ROC-AUC và AP (Average Precision) dùng trực tiếp xác suất trước khi áp ngưỡng.

| Mô hình | Accuracy | Precision | Recall | F1 | ROC-AUC | AP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 0,661631 | 0,661631 | 1,000000 | 0,796364 | 0,500000 | 0,661631 |
| Decision Tree | 0,661631 | 0,661631 | 1,000000 | 0,796364 | 0,511802 | 0,669142 |
| XGBoost | 0,661631 | 0,661631 | 1,000000 | 0,796364 | 0,516309 | 0,674041 |
| LightGBM | 0,661631 | 0,661631 | 1,000000 | 0,796364 | 0,516318 | 0,674091 |
| Stacking Classifier | 0,661631 | 0,661631 | 1,000000 | 0,796364 | 0,516548 | 0,674086 |

Ở ngưỡng 0,5, cả năm phương án đều dự đoán lớp dương cho mọi lượt. Ma trận nhầm lẫn của mỗi phương án có **TN = 0, FP = 49.280, FN = 0, TP = 96.360**. Do đó, F1 khoảng 0,796 chủ yếu phản ánh tỷ lệ lớp dương trong tập kiểm tra. LightGBM có AP cao nhất và Stacking có ROC-AUC cao nhất. Mức tăng ROC-AUC của Stacking so với baseline chỉ khoảng 0,017, nên chưa có bằng chứng để chọn Stacking làm mô hình sử dụng thực tế.

## Tái lập bảng kết quả

Chạy tiếp sau [khối huấn luyện](02_huan_luyen_mo_hinh.md).

```python
rows = []
for name, scores in base_test.items():
    prediction = (scores >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, prediction, labels=[0, 1]).ravel()
    rows.append({
        "model": name,
        "accuracy": accuracy_score(y_test, prediction),
        "precision": precision_score(y_test, prediction, zero_division=0),
        "recall": recall_score(y_test, prediction, zero_division=0),
        "f1": f1_score(y_test, prediction, zero_division=0),
        "roc_auc": roc_auc_score(y_test, scores),
        "ap": average_precision_score(y_test, scores),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
    })
results = pd.DataFrame(rows)
print(results.to_string(index=False, float_format=lambda value: f"{value:.6f}"), flush=True)
```

## Hướng cải thiện thí nghiệm

Thêm đặc trưng lịch sử có thể tính trước trận, chẳng hạn số phút trung bình trong các trận trước hoặc số ngày nghỉ kể từ lượt ra sân gần nhất. Tính các đặc trưng với mốc thời gian nhỏ hơn ngày trận cần dự đoán. Chọn ngưỡng trên dữ liệu xác thực và dành kỳ thời gian mới để kiểm tra cấu hình đã chọn. Để chuyển sang bài toán dự đoán đội hình xuất phát, cần bổ sung danh sách đăng ký và đội hình xác nhận của từng trận để xây dựng nhãn trực tiếp.
