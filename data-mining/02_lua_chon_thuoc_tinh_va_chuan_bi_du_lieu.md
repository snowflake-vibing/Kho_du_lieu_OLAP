# 5.2 Lựa chọn thuộc tính (Feature Selection) và Chuẩn bị dữ liệu huấn luyện

Tài liệu này hướng dẫn chi tiết các bước lựa chọn đặc trưng, mã hóa biến phân loại (Encoding), phân tách biến mục tiêu, chia tập Train/Test theo tỷ lệ chuẩn 80/20 và kỹ thuật tính toán trọng số lớp để xử lý bài toán dữ liệu mất cân bằng (Imbalanced Data) theo mục 5.2 của tài liệu môn học IS217.

---

## 1. Mục tiêu và ý nghĩa kỹ thuật
* **Loại bỏ nhiễu định danh:** Các trường mã định danh ID (như mã giao dịch, số tài khoản, mã khách hàng) là các biến duy nhất ngẫu nhiên, không mang tính quy luật hành vi. Nếu giữ lại, mô hình sẽ bị ghi nhớ máy móc (overfitting) thay vì học được quy luật chung.
* **Mã hóa One-Hot Encoding:** Chuyển đổi các biến phân loại danh mục (Categorical variables) như loại giao dịch, danh mục đối tác, thiết bị sang dạng vector nhị phân (0 và 1) để các thuật toán cây quyết định và gradient boosting tính toán được khoảng cách và chia nhánh.
* **Phân tầng Train/Test (Stratification):** Đảm bảo tỷ lệ phần trăm giữa lớp gian lận (1) và lớp bình thường (0) trong tập Train và tập Test luôn đồng nhất với tập gốc.
* **Xử lý mất cân bằng bằng `scale_pos_weight`:** Cân bằng hàm mất mát loss function cho XGBoost bằng cách phạt nặng hơn khi phân loại sai nhãn thiểu số.

---

## 2. Quy trình thực hiện từng bước bằng Python

### Bước 1 & Bước 2: Loại bỏ các cột không cần thiết và tạo DataFrame sạch
Tiếp tục từ DataFrame đã được tiền xử lý ở mục 5.1, tiến hành lọc bỏ các thuộc tính định danh:

```python
# ==============================================================================
# BƯỚC 1 & 2: LOẠI BỎ CỘT ĐỊNH DANH VÀ TẠO DATAFRAME TINH GỌN
# ==============================================================================
# Danh sách các cột không đóng góp vào quy luật dự báo cần loại bỏ
cols_to_drop = [
    'Transaction_ID', 
    'Account_Number', 
    'Customer_ID', 
    'Merchant_ID', 
    'Merchant_Name',
    'City'  # Nếu số lượng thành phố quá lớn gây bùng nổ số chiều
]

# Chỉ xóa những cột thực sự tồn tại trong DataFrame
existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
df_cleaned = df.drop(columns=existing_cols_to_drop)

print(f"Kích thước sau khi loại bỏ cột không cần thiết: {df_cleaned.shape}")
print("Danh sách các cột được giữ lại cho Data Mining:")
print(list(df_cleaned.columns))
```

---

### Bước 3: Mã hóa dữ liệu danh mục bằng One-Hot Encoding
Áp dụng hàm `pd.get_dummies()` với tham số `drop_first=True` để tránh hiện tượng đa cộng tuyến (Dummy Variable Trap):

```python
# ==============================================================================
# BƯỚC 3: MÃ HÓA BIẾN PHÂN LOẠI (ONE-HOT ENCODING)
# ==============================================================================
# Tự động xác định danh sách các cột kiểu phân loại (object hoặc category)
categorical_cols = df_cleaned.select_dtypes(include=['object', 'category']).columns.tolist()
print("Các cột kiểu phân loại cần mã hóa:", categorical_cols)

# Thực hiện One-Hot Encoding
df_encoded = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True, dtype=int)

print(f"Kích thước ma trận dữ liệu sau khi One-Hot Encoding: {df_encoded.shape[0]} dòng, {df_encoded.shape[1]} cột.")
df_encoded.head()
```

---

### Bước 4: Tách tập biến đặc trưng (Features - X) và biến mục tiêu (Target - Y)
Xác định biến nhãn phân loại nhị phân `Is_Fraud` làm nhãn mục tiêu $Y$, toàn bộ các cột còn lại làm không gian đặc trưng $X$:

```python
# ==============================================================================
# BƯỚC 4: TÁCH FEATURES (X) VÀ TARGET (Y)
# ==============================================================================
target_column = 'Is_Fraud'

# Tập biến độc lập (Features)
X = df_encoded.drop(columns=[target_column])

# Tập biến mục tiêu (Target)
y = df_encoded[target_column]

print(f"Kích thước ma trận đặc trưng X: {X.shape}")
print(f"Kích thước vector nhãn mục tiêu y: {y.shape}")
print("Tần số các lớp trong biến mục tiêu y:")
print(y.value_counts())
```

---

### Bước 5: Phân chia tập dữ liệu huấn luyện (Train) và kiểm thử (Test) theo tỷ lệ 80/20
Sử dụng hàm `train_test_split` từ thư viện `sklearn.model_selection` với tham số `stratify=y` để bảo toàn tỷ lệ nhãn:

```python
# ==============================================================================
# BƯỚC 5: PHÂN CHIA TẬP TRAIN VÀ TEST (80% TRAIN / 20% TEST)
# ==============================================================================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20,         # 20% dữ liệu để đánh giá độc lập
    random_state=42,        # Cố định seed ngẫu nhiên để tái lặp kết quả
    stratify=y              # Bảo toàn tỷ lệ lớp gian lận trên cả 2 tập
)

print(f"Tập huấn luyện (X_train): {X_train.shape[0]} dòng, {X_train.shape[1]} đặc trưng.")
print(f"Tập kiểm thử   (X_test) : {X_test.shape[0]} dòng, {X_test.shape[1]} đặc trưng.")
```

---

### Bước 6: Tính toán trọng số xử lý mất cân bằng lớp (`scale_pos_weight`) cho XGBoost
Trong bài toán phát hiện gian lận ngân hàng, tỷ lệ gian lận thường chỉ chiếm dưới 5% toàn bộ tập dữ liệu. Nếu không xử lý, mô hình sẽ có xu hướng dự đoán toàn bộ là "Bình thường" (0) để đạt độ chính xác ảo trên 95%.

Công thức tính hệ số trọng số `scale_pos_weight` chuẩn trong XGBoost:
$$\text{scale\_pos\_weight} = \frac{\text{Số lượng mẫu lớp âm tính (Negative - Lớp 0)}}{\text{Số lượng mẫu lớp dương tính (Positive - Lớp 1)}}$$

Đoạn mã Python tính toán tự động:
```python
# ==============================================================================
# BƯỚC 6: TÍNH TOÁN TRỌNG SỐ SCALE_POS_WEIGHT
# ==============================================================================
num_neg = (y_train == 0).sum()
num_pos = (y_train == 1).sum()

scale_pos_weight_value = num_neg / num_pos

print(f"Số mẫu lớp âm tính (Bình thường - 0): {num_neg:,}")
print(f"Số mẫu lớp dương tính (Gian lận - 1)  : {num_pos:,}")
print(f"-> Hệ số scale_pos_weight tính toán được: {scale_pos_weight_value:.4f}")
```

---

### Bước 7: Kiểm tra và xác nhận cấu trúc dữ liệu trước khi huấn luyện
In bảng tổng hợp xác nhận tỷ lệ phân chia và tính sẵn sàng của dữ liệu:

```python
# ==============================================================================
# BƯỚC 7: KIỂM TRA TỶ LỆ PHÂN CHIA VÀ XÁC NHẬN SẴN SÀNG
# ==============================================================================
check_df = pd.DataFrame({
    'Tập dữ liệu': ['Tập Train (Huấn luyện)', 'Tập Test (Kiểm thử)', 'Toàn bộ tập gốc'],
    'Tổng số mẫu': [len(y_train), len(y_test), len(y)],
    'Số ca Gian lận (1)': [y_train.sum(), y_test.sum(), y.sum()],
    'Tỷ lệ Gian lận (%)': [
        (y_train.sum() / len(y_train)) * 100,
        (y_test.sum() / len(y_test)) * 100,
        (y.sum() / len(y)) * 100
    ]
})

print("Bảng xác nhận phân bổ tập Train và Test:")
print(check_df.to_string(index=False))
print("\n=> Dữ liệu đã chuẩn hóa 100% và sẵn sàng nạp vào các mô hình XGBoost và Random Forest!")
```
