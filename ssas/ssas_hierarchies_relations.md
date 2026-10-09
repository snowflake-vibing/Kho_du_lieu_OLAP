# HƯỚNG DẪN SSAS - PHẦN 4: QUAN HỆ CHIỀU (DIMENSION RELATIONSHIPS) & PHÂN CẤP DỮ LIỆU (HIERARCHIES)

---

## 1. MỤC TIÊU HUẤN LUYỆN
Cấu hình tab **Dimension Relationships** trong Cube Editor và xây dựng các **User-Defined Hierarchies (Phân cấp người dùng)** để phục vụ thao tác **Drill-down / Roll-up** trên Cube.

---

## 2. BƯỚC 1: THIẾT LẬP QUAN HỆ CHIỀU (DIMENSION RELATIONSHIPS)

1. Mở Cube Editor `DW_Football_Cube.cube` $\rightarrow$ Chọn tab **Dimension Relationships**.
2. Kiểm tra quan hệ giữa Measure Group `FACT Player Match Perf` và các Dimensions:

| Dimension | Relationship Type | Dimension Table Key Column | Fact Table Foreign Key Column |
| :--- | :--- | :--- | :--- |
| **`DIM_Player`** | Regular | `Player_ID` | `Player_ID` |
| **`DIM_Club`** | Regular | `Club_ID` | `Player_Club_ID` |
| **`DIM_Competition`** | Regular | `Competition_ID` | `Competition_ID` |
| **`DIM_Game`** | Regular | `Game_ID` | `Game_ID` |
| **`DIM_Time`** | Regular | `Time_ID` | `Time_ID` |

3. Nếu có quan hệ chưa nhận dạng tự động:
   - Nhấp vào ô giao giữa Measure Group và Dimension $\rightarrow$ Chọn biểu tượng `...` (Ellipsis).
   - Chọn **Relationship type**: `Regular`.
   - Chọn **Granularity attribute**: Khóa chính của bảng Dim.
   - Chọn **Relationship columns**: Nối tương ứng khóa ngoại của Fact với khóa chính của Dim.

---

## 3. BƯỚC 2: XÂY DỰNG CÁC PHÂN CẤP DỮ LIỆU (HIERARCHIES)

Mở từng tệp `.dim` trong thư mục Dimensions để kéo thả tạo Hierarchies:

### 1. Phân cấp Thời gian (`Time Hierarchy` trong `DIM_Time.dim`)
- **Tên Phân cấp**: `Calendar Hierarchy`
- **Các Cấp độ (Levels)**:
  1. Level 1: **`Season`** (Mùa giải)
  2. Level 2: **`Year`** (Năm)
  3. Level 3: **`Quarter`** (Quý)
  4. Level 4: **`Month`** (Tháng)
  5. Level 5: **`Full_Date`** (Ngày thi đấu đầy đủ)

### 2. Phân cấp Vị trí Cầu thủ (`Player Position Hierarchy` trong `DIM_Player.dim`)
- **Tên Phân cấp**: `Position Hierarchy`
- **Các Cấp độ (Levels)**:
  1. Level 1: **`Main_Position`** (Vị trí chính: Attack, Midfield, Defender, Goalkeeper)
  2. Level 2: **`Sub_Position`** (Vị trí chi tiết: Striker, Centre-Back...)
  3. Level 3: **`Player_Name`** (Cầu thủ)

### 3. Phân cấp Giải đấu & Quốc gia (`Competition Hierarchy` trong `DIM_Competition.dim`)
- **Tên Phân cấp**: `Competition Hierarchy`
- **Các Cấp độ (Levels)**:
  1. Level 1: **`Competition_Type`** (Loại giải: domestic_league / international_cup)
  2. Level 2: **`Country_Name`** (Quốc gia)
  3. Level 3: **`Competition_Name`** (Tên giải đấu)

### 4. Phân cấp Trận đấu (`Game Hierarchy` trong `DIM_Game.dim`)
- **Tên Phân cấp**: `Game Round Hierarchy`
- **Các Cấp độ (Levels)**:
  1. Level 1: **`Round`** (Vòng đấu)
  2. Level 2: **`Game_ID`** (Mã trận đấu)

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Đủ 5 quan hệ Regular Relationships trong tab Dimension Relationships.
- [x] Tạo thành công 4 Phân cấp người dùng (Hierarchies) chuẩn xác.
- [x] Không còn cảnh báo Attribute Relationships warning trên SSDT.
