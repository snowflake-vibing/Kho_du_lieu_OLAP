# 5.1 Phân tích tập dữ liệu gốc, Tiền xử lý dữ liệu và Khám phá dữ liệu (EDA)

Tài liệu này hướng dẫn chi tiết toàn bộ quy trình tiền xử lý, thống kê mô tả và khám phá dữ liệu trực quan (Exploratory Data Analysis - EDA) bằng ngôn ngữ **Python** trên môi trường Jupyter Notebook / Google Colab theo cấu trúc Chương 5 của tài liệu đề tài IS217.

---

## 5.1.1 Tiền xử lý dữ liệu (Data Preprocessing)

Trước khi đưa vào các thuật toán Machine Learning, tập dữ liệu gốc thường chứa các thuộc tính dạng chuỗi thời gian gộp, địa chỉ gộp, hoặc các giá trị khuyết thiếu cần được làm sạch và chuẩn hóa.

### Bước 1: Cài đặt và nạp các thư viện Python chuyên dụng
Mở môi trường Jupyter Notebook và thực thi khối mã import các thư viện:

```python
# ==============================================================================
# BƯỚC 1: IMPORT CÁC THƯ VIỆN KHOA HỌC DỮ LIỆU
# ==============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập hiển thị đồ thị và định dạng số
%matplotlib inline
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

print("Đã nạp thành công các thư viện cơ bản!")
```

Tiến hành đọc tập dữ liệu gốc từ tệp CSV:
```python
# Đọc tập dữ liệu từ đường dẫn
file_path = "dataset.csv"  # Thay bằng đường dẫn thực tế của tập dữ liệu
df = pd.read_csv(file_path)

# Hiển thị kích thước ban đầu và 5 dòng đầu tiên
print(f"Kích thước tập dữ liệu gốc: {df.shape[0]} dòng, {df.shape[1]} cột.")
df.head()
```

---

### Bước 2: Kiểm tra dữ liệu khuyết thiếu (Null) và trùng lặp (Duplicates)
Kiểm tra tính toàn vẹn của dữ liệu để đảm bảo không bị sai lệch trong quá trình huấn luyện:

```python
# ==============================================================================
# BƯỚC 2: KIỂM TRA DỮ LIỆU THIẾU VÀ TRÙNG LẶP
# ==============================================================================
# 1. Kiểm tra số dòng trùng lặp hoàn toàn
duplicate_count = df.duplicated().sum()
print(f"Số lượng bản ghi trùng lặp hoàn toàn: {duplicate_count}")
if duplicate_count > 0:
    df = df.drop_duplicates()
    print("-> Đã loại bỏ các bản ghi trùng lặp.")

# 2. Kiểm tra giá trị Null / Missing theo từng cột
null_report = pd.DataFrame({
    'Kiểu dữ liệu': df.dtypes,
    'Số lượng Null': df.isnull().sum(),
    'Tỷ lệ Null (%)': (df.isnull().sum() / len(df)) * 100
})
print("Báo cáo giá trị khuyết thiếu:")
print(null_report[null_report['Số lượng Null'] > 0])
```

---

### Bước 3: Phân rã thuộc tính thời gian (Date & Time)
Các trường ngày và giờ gộp cần được tách thành các thành phần số học riêng biệt để mô hình có thể nhận diện được các chu kỳ hành vi (theo ngày trong tháng, theo khung giờ trong ngày):

```python
# ==============================================================================
# BƯỚC 3: PHÂN RÃ CỘT TRANSACTION_DATE VÀ TRANSACTION_TIME
# ==============================================================================
# 1. Chuyển đổi và phân rã cột Transaction_Date thành Day, Month, Year
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
df['Day'] = df['Transaction_Date'].dt.day
df['Month'] = df['Transaction_Date'].dt.month
df['Year'] = df['Transaction_Date'].dt.year

# 2. Phân rã cột Transaction_Time thành Hour, Minute, Second
# (Giả định định dạng 'HH:MM:SS')
time_split = df['Transaction_Time'].astype(str).str.split(':', expand=True)
df['Hour'] = time_split[0].astype(int)
df['Minute'] = time_split[1].astype(int)
df['Second'] = time_split[2].astype(int)

# 3. Xóa bỏ 2 cột gốc dạng chuỗi ban đầu để tinh gọn dữ liệu
df.drop(columns=['Transaction_Date', 'Transaction_Time'], inplace=True)

print("Đã tách thành công các trường thời gian: Day, Month, Year, Hour, Minute, Second.")
```

---

### Bước 4: Phân rã thuộc tính vị trí địa lý (Location)
Tách chuỗi vị trí gộp `City, State` thành 2 thuộc tính độc lập để hỗ trợ phân nhóm chính xác:

```python
# ==============================================================================
# BƯỚC 4: PHÂN RÃ VỊ TRÍ ĐỊA LÝ THÀNH CITY VÀ STATE
# ==============================================================================
# Giả định cột Transaction_Location có định dạng "Thành phố, Bang"
if 'Transaction_Location' in df.columns:
    location_split = df['Transaction_Location'].astype(str).str.split(',', expand=True)
    df['City'] = location_split[0].str.strip()
    df['State'] = location_split[1].str.strip() if location_split.shape[1] > 1 else 'Unknown'
    
    # Xóa cột gộp ban đầu
    df.drop(columns=['Transaction_Location'], inplace=True)

# Hiển thị lại 5 dòng dữ liệu và thông tin kiểu dữ liệu sau khi xử lý
print("Cấu trúc bảng dữ liệu sau khi tiền xử lý:")
df.info()
df.head()
```

---

## 5.1.2 Thống kê mô tả (Descriptive Statistics)

Sử dụng phương thức `describe()` để phân tích các thông số định lượng (Trung bình, Độ lệch chuẩn, Min, Phân vị 25%, 50%, 75%, Max):

```python
# ==============================================================================
# 5.1.2 THỐNG KÊ MÔ TẢ DỮ LIỆU ĐỊNH LƯỢNG
# ==============================================================================
numeric_summary = df.describe().T
numeric_summary['skewness'] = df.skew(numeric_only=True)
print("Bảng thống kê mô tả định lượng và độ lệch (Skewness):")
numeric_summary[['count', 'mean', 'std', 'min', '50%', 'max', 'skewness']]
```

---

## 5.1.3 Trực quan hóa dữ liệu (Exploratory Data Analysis - EDA)

Thực hiện vẽ các biểu đồ chuyên sâu để phát hiện quy luật phân bố và các yếu tố tương quan tới biến mục tiêu `Is_Fraud` (hoặc `Fraud Indicator`).

### a) Phân bố tỷ lệ lớp gian lận và tỷ lệ gian lận theo giới tính
Biểu đồ này giúp xác định ngay mức độ mất cân bằng lớp (Imbalanced Data) của bài toán:

```python
# ==============================================================================
# ĐỒ THỊ 1: PHÂN BỐ LỚP MỤC TIÊU VÀ TỶ LỆ THEO GIỚI TÍNH
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Phân bố nhãn lớp Is_Fraud (0: Bình thường, 1: Gian lận)
fraud_counts = df['Is_Fraud'].value_counts()
fraud_percentages = df['Is_Fraud'].value_counts(normalize=True) * 100

bars = axes[0].bar(['Bình thường (0)', 'Gian lận (1)'], fraud_counts.values, color=['#2b5c8f', '#d9534f'], width=0.5)
axes[0].set_title('Phân bố tỷ lệ Giao dịch Gian lận vs Bình thường', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Số lượng bản ghi')
for bar, pct in zip(bars, fraud_percentages.values):
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 500, f"{yval:,} ({pct:.2f}%)", ha='center', va='bottom', fontweight='bold')

# 2. Tỷ lệ gian lận phân bổ theo Giới tính (Customer_Gender)
if 'Customer_Gender' in df.columns:
    gender_fraud = df.groupby('Customer_Gender')['Is_Fraud'].mean() * 100
    sns.barplot(x=gender_fraud.index, y=gender_fraud.values, ax=axes[1], palette='Blues_d')
    axes[1].set_title('Tỷ lệ rủi ro gian lận theo Giới tính (%)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Tỷ lệ rủi ro (%)')
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')

plt.tight_layout()
plt.show()
```

---

### b) Thống kê tỷ lệ gian lận theo từng giờ trong ngày và từng ngày trong tháng
Phát hiện các khung giờ và mốc ngày có tần suất rủi ro cao bất thường:

```python
# ==============================================================================
# ĐỒ THỊ 2: TỶ LỆ GIAN LẬN THEO KHUNG GIỜ VÀ THEO NGÀY TRONG THÁNG
# ==============================================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# 1. Tỷ lệ gian lận theo từng giờ trong ngày (Hour 0 - 23)
hourly_fraud = df.groupby('Hour')['Is_Fraud'].agg(['count', 'sum'])
hourly_fraud['rate'] = (hourly_fraud['sum'] / hourly_fraud['count']) * 100

axes[0].plot(hourly_fraud.index, hourly_fraud['rate'], marker='o', linewidth=2.5, color='#d9534f', label='Tỷ lệ rủi ro (%)')
axes[0].set_title('Tỷ lệ giao dịch gian lận theo từng Khung giờ trong ngày (0h - 23h)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Giờ trong ngày')
axes[0].set_ylabel('Tỷ lệ gian lận (%)')
axes[0].set_xticks(range(0, 24))
axes[0].grid(True, linestyle='--', alpha=0.6)

# Làm nổi bật các mốc giờ cao điểm (0h, 4h, 9h, 17h)
peak_hours = [0, 4, 9, 17]
for h in peak_hours:
    if h in hourly_fraud.index:
        val = hourly_fraud.loc[h, 'rate']
        axes[0].scatter(h, val, color='black', s=80, zorder=5)
        axes[0].annotate(f"{h}h ({val:.2f}%)", (h, val + 0.1), fontweight='bold', color='black')

# 2. Số lượng giao dịch gian lận theo từng ngày trong tháng
daily_fraud = df[df['Is_Fraud'] == 1].groupby('Day')['Is_Fraud'].count()
axes[1].bar(daily_fraud.index, daily_fraud.values, color='#337ab7', alpha=0.85)
axes[1].set_title('Số lượng sự vụ gian lận theo Ngày trong tháng', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Ngày trong tháng')
axes[1].set_ylabel('Số vụ gian lận')
axes[1].set_xticks(daily_fraud.index)
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
```

---

### c) Phân bổ số tiền giao dịch và tỷ lệ gian lận theo loại thiết bị
Phân tích xem kẻ gian có xu hướng thực hiện giao dịch với số tiền lớn hơn bình thường hay không, và loại thiết bị nào bị lợi dụng nhiều nhất:

```python
# ==============================================================================
# ĐỒ THỊ 3: PHÂN BỔ SỐ TIỀN THEO LỚP VÀ TỶ LỆ THEO LOẠI THIẾT BỊ
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Phân bổ số tiền giao dịch (Transaction Amount) theo nhãn gian lận (Boxplot log scale)
sns.boxplot(x='Is_Fraud', y='Transaction_Amount', data=df, ax=axes[0], palette=['#337ab7', '#d9534f'])
axes[0].set_title('Phân bổ Số tiền giao dịch theo Lớp gian lận', fontsize=12, fontweight='bold')
axes[0].set_xticklabels(['Bình thường (0)', 'Gian lận (1)'])
axes[0].set_ylabel('Số tiền giao dịch')

# 2. Tỷ lệ gian lận theo Loại thiết bị giao dịch (Device_Type)
if 'Device_Type' in df.columns or 'Device_Type_Name' in df.columns:
    dev_col = 'Device_Type' if 'Device_Type' in df.columns else 'Device_Type_Name'
    device_fraud = df.groupby(dev_col)['Is_Fraud'].mean() * 100
    sns.barplot(x=device_fraud.index, y=device_fraud.values, ax=axes[1], palette='mako')
    axes[1].set_title('Tỷ lệ giao dịch gian lận theo Loại thiết bị (%)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Tỷ lệ gian lận (%)')
    axes[1].tick_params(axis='x', rotation=30)
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontweight='bold')

plt.tight_layout()
plt.show()
```

---

## 5.1.4 Nhận xét rút ra từ quá trình EDA
1. **Mất cân bằng lớp nghiêm trọng:** Lớp đa số (giao dịch bình thường) chiếm tới trên 95% - 98% tập dữ liệu, trong khi lớp thiểu số (gian lận) chỉ chiếm từ 2% - 5%. Do đó, không thể dùng độ đo Accuracy đơn thuần để đánh giá mô hình, mà bắt buộc phải sử dụng các độ đo nhạy bén như **Precision**, **Recall**, **F1-Score** và **AUC-ROC**.
2. **Khung giờ rủi ro cao:** Tỷ lệ gian lận có xu hướng bùng phát mạnh vào các khung giờ đêm muộn và rạng sáng (**0h**, **4h**) khi hệ thống kiểm soát của người dùng lỏng lẻo, cùng với khung giờ cao điểm mua sắm (**9h**, **17h**).
3. **Đặc trưng số tiền và thiết bị:** Các giao dịch gian lận có phương sai số tiền rất lớn, kẻ gian thường nhắm vào các hạn mức giao dịch tối đa cho phép. Tỷ lệ rủi ro giữa các thiết bị phân bổ tương đối đồng đều nhưng thiết bị di động (Mobile Web / App) chiếm tần suất tuyệt đối về số lượng.
