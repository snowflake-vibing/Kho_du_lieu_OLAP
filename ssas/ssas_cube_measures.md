# HƯỚNG DẪN SSAS - PHẦN 3: THIẾT LẬP CUBE & ĐỊNH NGHĨA MEASURES

---

## 1. MỤC TIÊU HUẤN LUYỆN
Khởi tạo OLAP Cube **`DW_Football_Cube`** từ `FACT_Player_Match_Perf`, định nghĩa danh sách các **Measures (Độ đo)** cộng dồn và xây dựng các **Calculated Measures (Độ đo tính toán)** qua ngôn ngữ MDX.

---

## 2. BƯỚC 1: KHỞI TẠO CUBE `DW_Football_Cube`

1. Trong Solution Explorer, chuột phải vào **Cubes** $\rightarrow$ chọn **New Cube...**
2. Nhấn **Next >** tại màn hình Welcome Wizard.
3. Chọn **Use existing tables** $\rightarrow$ Nhấn **Next >**.
4. Tại màn hình **Select Measure Group Tables**:
   - Tick chọn duy nhất bảng **`FACT_Player_Match_Perf`**.
   - Nhấn **Next >**.
5. Tại màn hình **Select Measures**:
   - Tick chọn các thuộc tính dùng làm Measure:
     - `Minutes Played` (Hàm Sum)
     - `Goals` (Hàm Sum)
     - `Assists` (Hàm Sum)
     - `Goal Contributions` (Hàm Sum)
     - `Yellow Cards` (Hàm Sum)
     - `Red Cards` (Hàm Sum)
     - `Is Starter` (Hàm Sum)
     - `Is Home Game` (Hàm Sum)
     - `FACT Player Match Perf Count` (Hàm Count - Đếm số lượt ra sân)
6. Tại màn hình **Select Existing Dimensions**:
   - Tick chọn đầy đủ 5 Dimensions đã tạo: `DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`.
7. Đặt tên Cube: **`DW_Football_Cube`** $\rightarrow$ Nhấn **Finish**.

---

## 3. BƯỚC 2: ĐỊNH NGHĨA VÀ ĐỔI TÊN MEASURES

Chỉnh sửa tiêu đề các Measure trong tab **Cube Structure** để hiển thị thân thiện trên báo cáo:

| Tên Gốc trong SSAS | Tên Hiển Thị Rõ Ràng (Caption) | Aggregation Function | Format String |
| :--- | :--- | :--- | :--- |
| `Goals` | **`Total Goals`** | Sum | `#,##0` |
| `Assists` | **`Total Assists`** | Sum | `#,##0` |
| `Goal Contributions` | **`Total Goal Contributions`** | Sum | `#,##0` |
| `Minutes Played` | **`Total Minutes Played`** | Sum | `#,##0` |
| `Yellow Cards` | **`Total Yellow Cards`** | Sum | `#,##0` |
| `Red Cards` | **`Total Red Cards`** | Sum | `#,##0` |
| `Is Starter` | **`Total Starter Appearances`** | Sum | `#,##0` |
| `Is Home Game` | **`Total Home Appearances`** | Sum | `#,##0` |
| `FACT Player Match Perf Count` | **`Total Appearances`** | Count | `#,##0` |

---

## 4. BƯỚC 3: ĐỊNH NGHĨA CALCULATED MEASURES (MDX CALCULATIONS)

Mở tab **Calculations** trong Cube Editor, thêm các câu lệnh tính toán MDX:

### 1. Số phút thi đấu trung bình mỗi trận (Avg Minutes Per Match)
```mdx
CREATE MEMBER CURRENTCUBE.[Measures].[Avg Minutes Per Match] AS
    IIF([Measures].[Total Appearances] = 0, 0,
        [Measures].[Total Minutes Played] / [Measures].[Total Appearances]
    ),
FORMAT_STRING = "#,##0.0",
VISIBLE = 1,
ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';
```

### 2. Tỷ lệ đóng góp bàn thắng (Goal Contribution Rate per 90 Mins)
```mdx
CREATE MEMBER CURRENTCUBE.[Measures].[Contributions Per 90 Mins] AS
    IIF([Measures].[Total Minutes Played] = 0, 0,
        ([Measures].[Total Goal Contributions] * 90.0) / [Measures].[Total Minutes Played]
    ),
FORMAT_STRING = "#,##0.00",
VISIBLE = 1,
ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';
```

### 3. Tỷ lệ Đá chính (Starter Rate %)
```mdx
CREATE MEMBER CURRENTCUBE.[Measures].[Starter Rate Percent] AS
    IIF([Measures].[Total Appearances] = 0, 0,
        ([Measures].[Total Starter Appearances] * 1.0) / [Measures].[Total Appearances]
    ),
FORMAT_STRING = "Percent",
VISIBLE = 1,
ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';
```

---

## 5. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Cube `DW_Football_Cube` khởi tạo thành công với Measure Group `FACT_Player_Match_Perf`.
- [x] Định dạng Format String (`#,##0`, `Percent`, `#,##0.00`) gán chuẩn xác cho từng Measure.
- [x] Thêm thành công 3 Calculated Measures bằng MDX trong tab Calculations.
