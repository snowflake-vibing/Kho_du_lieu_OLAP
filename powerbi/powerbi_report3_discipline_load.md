# HƯỚNG DẪN POWER BI - PHẦN 4: THIẾT KẾ REPORT 3 - PHÂN TÍCH KỶ LUẬT & TẢI TRỌNG THI ĐẤU

---

## 1. MỤC TIÊU BÁO CÁO
Báo cáo **Report 3** cung cấp góc nhìn về **Tính Kỷ luật (Thẻ phạt)** và **Tải trọng Thi đấu (Số phút thi đấu thực tế)** của cầu thủ theo nhóm tuổi và vị trí thi đấu.

---

## 2. BƯỚC 1: TẠO CÁC BIỂU ĐỒ NỘI DUNG

### Visual 1: Thống kê Thẻ vàng & Thẻ đỏ theo Vị trí Thi đấu (Clustered Bar Chart)
- **Visual Type**: `Clustered Bar Chart`.
- **Y-Axis**: `DIM_Player [Main_Position]`.
- **X-Axis**: `[Total Yellow Cards]`, `[Total Red Cards]`.
- **Data Labels**: On.

### Visual 2: Phân bố Số phút thi đấu theo Nhóm tuổi (Area / Line Chart)
- **Visual Type**: `Area Chart`.
- **X-Axis**: `DIM_Player [Age]`.
- **Y-Axis**: `[Total Minutes Played]`.
- **Legend**: `DIM_Player [Main_Position]`.

### Visual 3: Tỷ lệ Đá chính vs Dự bị theo Vòng đấu (Donut Chart)
- **Visual Type**: `Donut Chart`.
- **Legend**: `[Total Starter Games]` vs `[Dự bị]`.
- **Values**: `COUNTROWS(FACT_Player_Match_Perf)`.

---

## 3. BƯỚC 2: TỰ ĐỘNG HÓA VÀ ĐÁNH GIÁ TƯƠNG TÁC
1. Thêm bộ lọc Slicer theo `DIM_Player [Age Group]` (Cầu thủ Trẻ < 21, Đỉnh cao 21-29, Lão tướng > 30).
2. Định dạng màu sắc cảnh báo: Thẻ vàng (Màu Vàng), Thẻ đỏ (Màu Đỏ thẫm).

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Biểu đồ kỉ luật phân định rõ ràng lỗi thẻ vàng và thẻ đỏ.
- [x] Area chart phản ánh chính xác xu hướng tải trọng thi đấu giảm dần ở độ tuổi trên 32.
- [x] Đã thiết lập xong trọn bộ 3 Report Dashboards trên Power BI.
