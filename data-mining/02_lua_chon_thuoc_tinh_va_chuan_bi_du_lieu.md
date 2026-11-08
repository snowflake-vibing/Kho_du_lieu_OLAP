# 5.3 Lựa chọn thuộc tính (Feature Selection) và Chuẩn bị dữ liệu huấn luyện

Tài liệu này hướng dẫn chi tiết quy trình lựa chọn đặc trưng (Feature Selection), mã hóa biến phân loại danh mục (One-Hot Encoding), phân tách biến mục tiêu $y = \text{Is\_Starter}$, phân chia tập Train/Test theo tỷ lệ chuẩn 80/20 có phân tầng (Stratified Sampling) và chuẩn hóa thang đo đặc trưng (Feature Scaling) theo mục 5.3 của đề tài môn học IS217.

---

## 1. Định nghĩa bài toán khai thác dữ liệu trong Bóng đá Châu Âu

Trong bóng đá chuyên nghiệp, việc dự đoán trước một cầu thủ có khả năng được huấn luyện viên điền tên vào danh sách **Đội hình xuất phát đá chính (`Is_Starter = 1`)** hay phải ngồi ghế **Dự bị (`Is_Starter = 0`)** có ý nghĩa chiến lược cực kỳ to lớn. Bài toán này hỗ trợ:
1. **Ban huấn luyện và Chuyên gia thể lực:** Đánh giá mức độ sẵn sàng thi đấu dựa trên phong độ, thể lực tích lũy và bối cảnh đối đầu.
2. **Bộ phận Scouting và Phân tích hiệu suất:** Nhận diện các cầu thủ tiềm năng có khả năng cạnh tranh suất đá chính thường xuyên trong đội một.

* **Biến mục tiêu (Target Variable $y$):** Cờ chỉ báo `Is_Starter` ($y \in \{0, 1\}$).
* **Bài toán:** Phân loại nhị phân (Binary Classification).

---

## 2. Quy trình thực hiện từng bước bằng Python

### Bước 1: Lựa chọn thuộc tính đặc trưng và loại bỏ các cột định danh
Các trường ID định danh và chuỗi tên riêng ngẫu nhiên cần được loại bỏ để tránh gây hiện tượng học vẹt (Overfitting) cho các mô hình cây quyết định:

```python
# ==============================================================================
# BƯỚC 1: LỌC BỎ CỘT ĐỊNH DANH VÀ GIỮ LẠI TẬP ĐẶC TRƯNG Ý NGHĨA
# ==============================================================================
# Danh sách các cột định danh hoặc trùng lặp không tham gia mô hình hóa
cols_to_drop = [
    'Appearance_ID', 
    'Player_ID', 
    'Club_ID', 
    'Competition_ID', 
    'Time_ID',
    'Player_Name', 
    'Club_Name', 
    'Stadium_Name', 
    'Coach_Name',
    'Competition_Name', 
    'Competition_Country', 
    'Player_Country',
    'Full_Date', 
    'Sub_Position'  # Đã có Main_Position đại diện cho tuyến thi đấu chính
]

# Tạo DataFrame sạch chỉ chứa các đặc trưng phân tích
df_model = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

print(f"Kích thước DataFrame sau khi loại bỏ cột định danh: {df_model.shape}")
print("Danh sách các cột được giữ lại:")
print(list(df_model.columns))
```

---

### Bước 2: Mã hóa biến phân loại danh mục bằng One-Hot Encoding
Chuyển đổi các biến danh mục dạng chuỗi (`Main_Position`, `Foot`, `Competition_Type`) thành các vector số nhị phân (0 và 1) bằng hàm `pd.get_dummies()` với `drop_first=True` để tránh hiện tượng đa cộng tuyến:

```python
# ==============================================================================
# BƯỚC 2: MÃ HÓA BIẾN PHÂN LOẠI (ONE-HOT ENCODING)
# ==============================================================================
categorical_features = ['Main_Position', 'Foot', 'Competition_Type']
# Lọc những cột thực sự tồn tại
categorical_features = [col for col in categorical_features if col in df_model.columns]

# Thực hiện One-Hot Encoding
df_encoded = pd.get_dummies(df_model, columns=categorical_features, drop_first=True, dtype=int)

print(f"Kích thước ma trận sau khi One-Hot Encoding: {df_encoded.shape[0]} dòng, {df_encoded.shape[1]} cột.")
df_encoded.head()
```

---

### Bước 3: Phân tách Ma trận đặc trưng ($X$) và Vector nhãn mục tiêu ($y$)
```python
# ==============================================================================
# BƯỚC 3: PHÂN TÁCH FEATURES (X) VÀ TARGET (Y)
# ==============================================================================
target_col = 'Is_Starter'

# Ma trận biến độc lập (Features)
X = df_encoded.drop(columns=[target_col])

# Vector biến phụ thuộc (Target)
y = df_encoded[target_col]

print(f"Kích thước ma trận đặc trưng X: {X.shape}")
print(f"Kích thước vector nhãn mục tiêu y: {y.shape}")
print("Phân bổ tần số của nhãn mục tiêu:")
print(y.value_counts())
```

---

### Bước 4: Phân chia tập dữ liệu Huấn luyện (Train) và Kiểm thử (Test) theo tỷ lệ 80/20
Sử dụng phương pháp lấy mẫu phân tầng (`stratify=y`) để đảm bảo tỷ lệ giữa cầu thủ đá chính (1) và dự bị (0) được bảo toàn đồng nhất trên cả 2 tập Train và Test:

```python
# ==============================================================================
# BƯỚC 4: CHIA TẬP DỮ LIỆU TRAIN / TEST THEO TỶ LỆ 80/20
# ==============================================================================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20,          # 20% dữ liệu để kiểm thử độc lập
    random_state=42,         # Cố định seed ngẫu nhiên
    stratify=y               # Bảo toàn tỷ lệ nhãn phân lớp
)

print(f"Số lượng mẫu tập Huấn luyện (X_train): {X_train.shape[0]:,} mẫu ({X_train.shape[1]} đặc trưng)")
print(f"Số lượng mẫu tập Kiểm thử   (X_test) : {X_test.shape[0]:,} mẫu ({X_test.shape[1]} đặc trưng)")
```

---

### Bước 5: Chuẩn hóa thang đo đặc trưng bằng `StandardScaler`
Các thuật toán như Logistic Regression (trong Stacking Classifier) và Gradient Boosting đạt tốc độ hội tụ nhanh hơn khi các đặc trưng định lượng được chuẩn hóa về cùng phân phối chuẩn có kỳ vọng bằng 0 và phương sai bằng 1:

```python
# ==============================================================================
# BƯỚC 5: CHUẨN HÓA THANG ĐO ĐẶC TRƯNG (FEATURE SCALING)
# ==============================================================================
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit trên tập Train và Transform trên cả Train và Test để tránh rò rỉ dữ liệu (Data Leakage)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Đã hoàn tất chuẩn hóa thang đo đặc trưng bằng StandardScaler!")
print("Dữ liệu sẵn sàng nạp vào các mô hình Machine Learning!")
```

---

### Bước 6: Bảng xác nhận tính sẵn sàng của tập dữ liệu
```python
# In bảng kiểm tra phân bổ
check_summary = pd.DataFrame({
    'Tập dữ liệu': ['Tập Train (80%)', 'Tập Test (20%)', 'Toàn bộ tập dữ liệu'],
    'Tổng số lượt ra sân': [len(y_train), len(y_test), len(y)],
    'Số lượt Đá chính (1)': [y_train.sum(), y_test.sum(), y.sum()],
    'Tỷ lệ Đá chính (%)': [
        (y_train.sum() / len(y_train)) * 100,
        (y_test.sum() / len(y_test)) * 100,
        (y.sum() / len(y)) * 100
    ]
})

print(check_summary.to_string(index=False))
```
