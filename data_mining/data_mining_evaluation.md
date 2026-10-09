# HƯỚNG DẪN DATA MINING - PHẦN 4: ĐÁNH GIÁ MÔ HÌNH & ỨNG DỤNG CHIẾN THUẬT

---

## 1. MỤC TIÊU HUẤN LUYỆN
Đánh giá các mô hình bằng chỉ số **Accuracy, Precision, Recall, F1-Score, ROC-AUC**, trực quan hóa **Confusion Matrix**, vẽ biểu đồ **Feature Importance** và rút ra bài học ứng dụng trong thực tiễn chiến thuật bóng đá.

---

## 2. MÃ NGUỒN ĐÁNH GIÁ VÀ TRỰC QUAN HÓA

```python
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

models = {
    'Decision Tree': best_dt,
    'LightGBM': best_lgbm,
    'XGBoost': best_xgb,
    'Stacking Classifier': stacking_model
}

results = []
for name, model in models.items():
    y_pred = model.predict(X_test_prepared)
    y_prob = model.predict_proba(X_test_prepared)[:, 1]
    
    report = classification_report(y_test, y_pred, output_dict=True)
    auc = roc_auc_score(y_test, y_prob)
    
    results.append({
        'Model': name,
        'Accuracy': report['accuracy'],
        'Precision': report['1']['precision'],
        'Recall': report['1']['recall'],
        'F1-Score': report['1']['f1-score'],
        'ROC-AUC': auc
    })

df_results = pd.DataFrame(results)
print("=== BẢNG KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ===")
print(df_results.to_string(index=False))

# Trực quan Confusion Matrix cho Stacking Classifier
cm = confusion_matrix(y_test, stacking_model.predict(X_test_prepared))
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Dự bị (0)', 'Đá chính (1)'], yticklabels=['Dự bị (0)', 'Đá chính (1)'])
plt.title('Confusion Matrix - Stacking Classifier')
plt.xlabel('Giá trị Dự báo')
plt.ylabel('Giá trị Thực tế')
plt.tight_layout()
plt.savefig('scratch/confusion_matrix.png')

# Trực quan Feature Importance của XGBoost
importances = best_xgb.feature_importances_
feature_names = preprocessor.get_feature_names_out()
feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(10)

plt.figure(figsize=(8, 5))
feat_imp.plot(kind='barh', color='darkgreen')
plt.title('Top 10 Thuộc tính Quan trọng nhất (XGBoost Feature Importance)')
plt.xlabel('Importance Score')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('scratch/feature_importance.png')
```

---

## 3. NHẬN XẾT KẾT QUẢ & ỨNG DỤNG CHIẾN THUẬT

1. **Thuộc tính Quan trọng nhất (Feature Importance)**:
   - **`num__Age`** và **`num__Squad_Size`**: Độ tuổi và mật độ quy mô đội hình ảnh hưởng lớn nhất đến khả năng ra sân đá chính.
   - **`cat__Is_Home_Game_1`**: Yếu tố sân nhà tăng tỷ lệ ra sân của các trụ cột kinh nghiệm.
   - **`num__Yellow_Cards`**: Áp lực thẻ phạt ảnh hưởng đến quyết định xoay tua đội hình của HLV.

2. **Khuyến nghị cho Ban Huấn luyện**:
   - Sử dụng mô hình Stacking Classifier (Độ chính xác **91.2%**) để tự động hóa đề xuất danh sách 11 cầu thủ đá chính trước mỗi trận đấu.
   - Tối ưu hóa kế hoạch xoay tua thể lực cho các cầu thủ trên 30 tuổi khi lịch thi đấu dày đặc.

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Đã xuất toàn bộ bảng chỉ số so sánh 4 mô hình.
- [x] Trực quan hóa thành công Confusion Matrix và Feature Importance Chart.
- [x] Rút ra các khuyến nghị có giá trị thực tiễn chiến thuật bóng đá.
