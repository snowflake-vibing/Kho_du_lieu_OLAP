# HƯỚNG DẪN POWER BI - PHẦN 2: THIẾT KẾ REPORT 1 - PHÂN TÍCH HIỆU SUẤT & GHI BÀN CẦU THỦ

---

## 1. MỤC TIÊU BÁO CÁO
Báo cáo **Report 1** tập trung vào **Phong độ, Hiệu suất Ghi bàn & Đóng góp Kiến tạo của Cầu thủ** trên khắp các giải đấu Châu Âu qua các mùa giải.

---

## 2. BƯỚC 1: TẠO CÁC CARD VISUALS TỔNG QUAN (KPI HEADER)

1. **Card 1: Tổng số Bàn thắng (Total Goals)**:
   - Visual Type: **Card**.
   - Fields: `[Total Goals]`.
   - Format: Category label Off, Callout value font size 36pt Bold.
2. **Card 2: Tổng số Kiến tạo (Total Assists)**:
   - Visual Type: **Card**.
   - Fields: `[Total Assists]`.
3. **Card 3: Tổng Đóng góp Bàn thắng (Total Goal Contributions)**:
   - Visual Type: **Card**.
   - Fields: `[Total Goal Contributions]`.
4. **Card 4: Số phút/Bàn thắng (Mins Per Goal)**:
   - Visual Type: **Card**.
   - Fields: `[Mins Per Goal]`.
   - Format String: `#,##0.0`.

---

## 3. BƯỚC 2: TẠO CÁC BIỂU ĐỒ NỘI DUNG CHÍNH

### Visual 1: Top 10 Chân sút ghi bàn nhiều nhất (Clustered Bar Chart)
- **Visual Type**: `Clustered Bar Chart`.
- **Y-Axis**: `DIM_Player [Player_Name]`.
- **X-Axis**: `[Total Goals]`.
- **Tooltip**: `[Total Assists]`, `DIM_Club [Club_Name]`, `DIM_Player [Main_Position]`.
- **Filters on visual**: Top N = 10 theo `[Total Goals]`.

### Visual 2: Đóng góp bàn thắng theo Vị trí Thi đấu (Stacked Column Chart)
- **Visual Type**: `Stacked Column Chart`.
- **X-Axis**: `DIM_Player [Main_Position]`.
- **Y-Axis**: `[Total Goals]`, `[Total Assists]`.
- **Legend**: `DIM_Player [Sub_Position]`.

### Visual 3: Xu hướng Bàn thắng theo Mùa giải & Quý (Line and Stacked Column Chart)
- **Visual Type**: `Line and Stacked Column Chart`.
- **Shared Axis**: `DIM_Time [Season]`, `DIM_Time [Quarter]`.
- **Column Values**: `[Total Goals]`.
- **Line Values**: `[Total Assists]`.

---

## 4. BƯỚC 3: THÊM CÁC BỘ LỌC TƯƠNG TÁC (SLICERS)

1. **Slicer 1 (Mùa giải)**: `DIM_Time [Season]` (Kiểu hiển thị Dropdown / Tile).
2. **Slicer 2 (Giải đấu)**: `DIM_Competition [Competition_Name]`.
3. **Slicer 3 (Vị trí thi đấu)**: `DIM_Player [Main_Position]`.
4. **Slicer 4 (Chân thuận)**: `DIM_Player [Foot]`.

---

## 5. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] 4 Card Visual KPI hiển thị đúng số liệu tổng quát.
- [x] Top 10 Chân sút bar chart hỗ trợ Drill-down và Cross-filtering.
- [x] Bộ lọc Slicers phản hồi tức thì với các biểu đồ còn lại.
