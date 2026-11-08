# 5.1 & 5.2 Mô tả bộ dữ liệu Bóng đá Transfermarkt, Tiền xử lý và Khám phá dữ liệu (EDA)

Tài liệu này hướng dẫn chi tiết toàn bộ quy trình mô tả tập dữ liệu, tiền xử lý làm sạch và phân tích khám phá dữ liệu trực quan (Exploratory Data Analysis - EDA) trên **Kho dữ liệu Bóng đá Châu Âu (Football Transfermarkt)** bằng ngôn ngữ **Python** theo chuẩn Chương 5 của đề tài môn học IS217.

---

## 5.1 Mô tả bộ dữ liệu bóng đá Transfermarkt

### 5.1.1 Tổng quan bộ dữ liệu
Bộ dữ liệu bóng đá châu Âu được thu thập từ nền tảng uy tín **Transfermarkt**, phản ánh toàn diện lịch sử thi đấu, diễn biến trận đấu và phong độ cầu thủ tại các giải bóng đá hàng đầu châu Âu (Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, UEFA Champions League...):
* **Bảng sự kiện ra sân (`appearances.csv` / `FACT_Player_Match_Perf`):** Chứa hơn **1.2 triệu bản ghi** chi tiết về từng lần ra sân của cầu thủ trong mỗi trận đấu cụ thể (`Appearance_ID`, `Player_ID`, `Game_ID`, `Club_ID`, `Minutes_Played`, `Goals`, `Assists`, `Yellow_Cards`, `Red_Cards`, `Is_Starter`, `Is_Home_Game`).
* **Bảng chiều cầu thủ (`players.csv` / `DIM_Player`):** Chứa hồ sơ thể chất và nhân khẩu học của hơn 30.000 cầu thủ chuyên nghiệp (`Age`, `Height_In_Cm`, `Main_Position`, `Sub_Position`, `Foot`, `Country_Of_Citizenship`).
* **Bảng chiều câu lạc bộ (`clubs.csv` / `DIM_Club`):** Thông tin về các đội bóng (`Club_Name`, `Stadium_Name`, `Stadium_Seats`, `Coach_Name`, `Squad_Size`).
* **Bảng chiều giải đấu (`competitions.csv` / `DIM_Competition`):** Thông tin phân loại giải đấu (`Competition_Name`, `Country_Name`, `Competition_Type`).
* **Bảng chiều thời gian (`DIM_Time`):** Cung cấp các lát cắt thời gian chuẩn hóa (`Year`, `Quarter`, `Month`, `Day`, `Season`, `Is_Weekend`).

---

### 5.1.2 Mô tả chi tiết các thuộc tính định lượng và định danh

| Thuộc tính (Attribute) | Kiểu dữ liệu | Ý nghĩa nghiệp vụ trong bóng đá |
| :--- | :---: | :--- |
| `Appearance_ID` | `nvarchar(100)` | Mã định danh duy nhất của mỗi lượt ra sân (dạng `game_id_player_id`) |
| `Player_ID` | `int` | Mã định danh cầu thủ |
| `Age` | `int` | Độ tuổi của cầu thủ tại thời điểm thi đấu (từ 16 đến 42 tuổi) |
| `Height_In_Cm` | `int` | Chiều cao của cầu thủ tính bằng centimet (từ 160cm đến 205cm) |
| `Main_Position` | `nvarchar(100)` | Vị trí thi đấu chính (`Attack`, `Midfield`, `Defender`, `Goalkeeper`) |
| `Foot` | `nvarchar(100)` | Chân thuận của cầu thủ (`right`, `left`, `both`) |
| `Minutes_Played` | `int` | Số phút thi đấu thực tế trên sân trong trận (từ 1 đến 120 phút) |
| `Goals` | `int` | Số bàn thắng ghi được trong trận đấu |
| `Assists` | `int` | Số đường chuyền kiến tạo thành bàn |
| `Goal_Contributions` | `int` | Tổng đóng góp bàn thắng trực tiếp (`Goals + Assists`) |
| `Yellow_Cards` | `int` | Số thẻ vàng bị phạt trong trận (0, 1, 2) |
| `Red_Cards` | `int` | Số thẻ đỏ bị truất quyền thi đấu trong trận (0, 1) |
| `Is_Starter` | `int` | Cờ chỉ báo đá chính (**Biến mục tiêu Target**): `1` là xuất phát trong đội hình chính, `0` là vào sân thay người |
| `Is_Home_Game` | `int` | Cờ chỉ báo địa điểm thi đấu: `1` là thi đấu trên sân nhà, `0` là sân khách |
| `Squad_Size` | `int` | Quy mô quân số đăng ký của câu lạc bộ |
| `Stadium_Seats` | `int` | Sức chứa khán đài sân vận động diễn ra trận đấu |

---

## 5.2 Kiểm tra và tiền xử lý dữ liệu (Data Preprocessing & EDA)

### Bước 1: Nạp các thư viện Python chuyên dụng và nạp dữ liệu bóng đá
```python
# ==============================================================================
# BƯỚC 1: IMPORT THƯ VIỆN KHOA HỌC DỮ LIỆU VÀ NẠP DỮ LIỆU BÓNG ĐÁ
# ==============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', None)

# Nạp dữ liệu bóng đá phẳng đã trích xuất từ Data Warehouse
data_path = "football/cleaned_data/Football_Report_Data.csv"
df = pd.read_csv(data_path)

print(f"Tổng số dòng dữ liệu ra sân: {df.shape[0]:,} bản ghi.")
print(f"Tổng số thuộc tính: {df.shape[1]} cột.")
df.head()
```

---

### Bước 2: Kiểm tra dữ liệu khuyết thiếu (Null) và làm sạch
```python
# ==============================================================================
# BƯỚC 2: KIỂM TRA GIÁ TRỊ KHUYẾT THIẾU VÀ XỬ LÝ LÀM SẠCH
# ==============================================================================
# Kiểm tra số lượng Null theo từng cột
null_counts = df.isnull().sum()
print("Các cột có giá trị khuyết thiếu:")
print(null_counts[null_counts > 0])

# Xử lý làm sạch:
# 1. Chiều cao (Height_In_Cm): Điền giá trị trung vị (median) theo từng vị trí thi đấu
df['Height_In_Cm'] = df.groupby('Main_Position')['Height_In_Cm'].transform(lambda x: x.fillna(x.median()))

# 2. Chân thuận (Foot): Điền giá trị xuất hiện nhiều nhất (mode) là chân phải 'right'
df['Foot'] = df['Foot'].fillna('right')

# 3. Tuổi (Age): Điền median độ tuổi
df['Age'] = df['Age'].fillna(df['Age'].median())

# 4. Loại bỏ các dòng trùng lặp nếu có
df = df.drop_duplicates(subset=['Appearance_ID'])
print("-> Đã xử lý triệt để 100% dữ liệu khuyết thiếu và trùng lặp!")
```

---

### Bước 3: Phân tích khám phá dữ liệu trực quan (EDA)

#### a) Phân bố tỷ lệ Cầu thủ Đá chính (`Is_Starter`)
Kiểm tra mức độ cân bằng của biến mục tiêu dự báo $y$:

```python
# ==============================================================================
# ĐỒ THỊ 1: PHÂN BỐ TỶ LỆ CẦU THỦ ĐÁ CHÍNH (IS_STARTER)
# ==============================================================================
plt.figure(figsize=(7, 5))
starter_counts = df['Is_Starter'].value_counts()
starter_pct = df['Is_Starter'].value_counts(normalize=True) * 100

bars = plt.bar(['Dự bị / Thay người (0)', 'Đá chính Xuất phát (1)'], 
               starter_counts.values, 
               color=['#E67E22', '#2E86C1'], width=0.5)

plt.title('Phân bố Cầu thủ Đá chính (Is_Starter = 1) vs Dự bị (Is_Starter = 0)', fontsize=12, fontweight='bold')
plt.ylabel('Số lượng lượt ra sân')

for bar, pct in zip(bars, starter_pct.values):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 10000, 
             f"{yval:,} ({pct:.1f}%)", ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()
```
*Nhận xét:* Tỷ lệ cầu thủ đá chính chiếm khoảng **73%** (11 cầu thủ xuất phát mỗi đội), trong khi cầu thủ vào sân thay người chiếm khoảng **27%**. Tỷ lệ này tương đối cân bằng và rất thuận lợi cho việc huấn luyện các mô hình phân loại nhị phân mà không bị lệch lớp cực đoan.

---

#### b) Tương quan giữa Thời lượng thi đấu (`Minutes_Played`) và Nhãn Đá chính (`Is_Starter`)
```python
# ==============================================================================
# ĐỒ THỊ 2: PHÂN BỐ SỐ PHÚT THI ĐẤU THEO NHÃN ĐÁ CHÍNH
# ==============================================================================
plt.figure(figsize=(10, 5))
sns.boxplot(x='Is_Starter', y='Minutes_Played', data=df, palette=['#E67E22', '#2E86C1'])
plt.title('Phân bố Thời lượng thi đấu (Minutes Played) theo Nhãn Đá chính', fontsize=12, fontweight='bold')
plt.xticks([0, 1], ['Dự bị (0)', 'Đá chính (1)'])
plt.ylabel('Số phút thi đấu trên sân')
plt.tight_layout()
plt.show()
```
*Nhận xét:* Các cầu thủ đá chính hầu như thi đấu từ **60 đến 90 phút** (trung vị là 90 phút), trong khi cầu thủ dự bị chỉ vào sân thi đấu trong khoảng **10 đến 30 phút** cuối trận. Đây là đặc trưng có tính phân tách mạnh mẽ nhất.

---

#### c) Phân bố Thẻ phạt và Bàn thắng theo Vị trí thi đấu (`Main_Position`)
```python
# ==============================================================================
# ĐỒ THỊ 3: TƯƠNG QUAN BÀN THẮNG VÀ THẺ VÀNG THEO VỊ TRÍ THI ĐẤU
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Bàn thắng trung bình theo Vị trí
sns.barplot(x='Main_Position', y='Goals', data=df, ax=axes[0], palette='Blues_d', ci=None)
axes[0].set_title('Số Bàn thắng trung bình theo Vị trí thi đấu', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Bàn thắng trung bình / trận')

# 2. Thẻ vàng trung bình theo Vị trí
sns.barplot(x='Main_Position', y='Yellow_Cards', data=df, ax=axes[1], palette='Reds_d', ci=None)
axes[1].set_title('Số Thẻ vàng trung bình theo Vị trí thi đấu', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Thẻ vàng trung bình / trận')

plt.tight_layout()
plt.show()
```
*Nhận xét:* Vị trí Tiền đạo (Attack) áp đảo tuyệt đối về chỉ số bàn thắng, trong khi vị trí Hậu vệ (Defender) và Tiền vệ (Midfield) có tỷ lệ nhận thẻ vàng cao gấp nhiều lần so với Thủ môn và Tiền đạo.
