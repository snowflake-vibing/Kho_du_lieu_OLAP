# HƯỚNG DẪN DATA MINING - PHẦN 2: TIỀN XỬ LÝ DỮ LIỆU & FEATURE ENGINEERING

---

## 1. MỤC TIÊU HUẤN LUYỆN
Trích xuất dữ liệu từ Kho SQL Server `DW_Football_Analytics`, tiến hành tiền xử lý, xử lý giá trị khuyết (Missing Values), mã hóa thuộc tính (Encoding) và phân chia tập dữ liệu Train/Test.

---

## 2. KỊCH BẢN MÃ NGUỒN PYTHON PREPROCESSING

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pyodbc

# 1. Kết nối Data Warehouse SQL Server trích xuất dataset
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=DW_Football_Analytics;"
    "Trusted_Connection=yes;"
)
query = """
SELECT 
    f.Appearance_ID,
    p.Age,
    p.Height_In_Cm,
    p.Main_Position,
    p.Foot,
    c.Squad_Size,
    f.Is_Home_Game,
    f.Yellow_Cards,
    f.Red_Cards,
    f.Is_Starter
FROM FACT_Player_Match_Perf f
JOIN DIM_Player p ON f.Player_ID = p.Player_ID
JOIN DIM_Club c ON f.Club_ID = c.Club_ID
"""
df = pd.read_sql(query, pyodbc.connect(conn_str))

# 2. Phân tách Feature Matrix X và Target Vector y
X = df.drop(columns=['Appearance_ID', 'Is_Starter'])
y = df['Is_Starter']

# 3. Phân loại thuộc tính Số (Numerical) và Phân loại (Categorical)
num_features = ['Age', 'Height_In_Cm', 'Squad_Size', 'Yellow_Cards', 'Red_Cards']
cat_features = ['Main_Position', 'Foot', 'Is_Home_Game']

# 4. Thiết lập Pipeline Tiền xử lý Dữ liệu
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_features),
    ('cat', cat_pipeline, cat_features)
])

# 5. Phân chia tập dữ liệu Train (80%) và Test (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 6. Biến đổi dữ liệu qua Preprocessor
X_train_prepared = preprocessor.fit_transform(X_train)
X_test_prepared = preprocessor.transform(X_test)

print(f"Dataset Shape: {df.shape}")
print(f"X_train Shape: {X_train_prepared.shape}, X_test Shape: {X_test_prepared.shape}")
```

---

## 3. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Đã trích xuất thành công dataset từ SQL Server.
- [x] Đã xử lý triệt để các giá trị NULL bằng SimpleImputer.
- [x] Đã chuẩn hóa dữ liệu số bằng StandardScaler và mã hóa dữ liệu phân loại bằng OneHotEncoder.
- [x] Tập Train/Test phân chia theo tỷ lệ 80:20 bảo đảm phân bố lớp cân bằng (Stratified).
