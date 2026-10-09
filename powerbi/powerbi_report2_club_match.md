# HƯỚNG DẪN POWER BI - PHẦN 3: THIẾT KẾ REPORT 2 - PHÂN TÍCH TRẬN ĐẤU & VẬN HÀNH CÂU LẠC BỘ

---

## 1. MỤC TIÊU BÁO CÁO
Báo cáo **Report 2** đánh giá **Sức mạnh Vận hành của các Câu lạc bộ**, so sánh phong độ Sân nhà vs Sân khách và phân tích quy mô khán giả tham dự trên các Sân vận động.

---

## 2. BƯỚC 1: TẠO CÁC BIỂU ĐỒ CHÍNH

### Visual 1: Tổng số Bàn thắng của CLB trên Sân nhà vs Sân khách (Grouped Column Chart)
- **Visual Type**: `Clustered Column Chart`.
- **X-Axis**: `DIM_Club [Club_Name]`.
- **Y-Axis**: `[Total Goals]`.
- **Legend**: `FACT_Player_Match_Perf [Is_Home_Game]` (1: Home, 0: Away).
- **Sort**: Bàn thắng giảm dần.

### Visual 2: Phân bố Bàn thắng theo Cấp độ Giải đấu (Treemap Visual)
- **Visual Type**: `Treemap`.
- **Category**: `DIM_Competition [Competition_Type]`, `DIM_Competition [Country_Name]`.
- **Details**: `DIM_Competition [Competition_Name]`.
- **Values**: `[Total Goals]`.

### Visual 3: Sức chứa Sân vận động vs Lượt thi đấu (Scatter Chart)
- **Visual Type**: `Scatter Chart`.
- **X-Axis**: `DIM_Club [Stadium_Seats]`.
- **Y-Axis**: `[Total Goals]`.
- **Size**: `DIM_Club [Squad_Size]`.
- **Legend**: `DIM_Competition [Country_Name]`.
- **Values**: `DIM_Club [Club_Name]`.

---

## 3. BƯỚC 2: CẤU HÌNH CONTROL VÀ NHẬN XÉT DỮ LIỆU

1. **Thêm Slicers**:
   - Slicer 1: `DIM_Club [Coach_Name]` (HLV trưởng).
   - Slicer 2: `DIM_Competition [Country_Name]` (Quốc gia đăng cai).
2. **Bật thuộc tính Cross-highlighting**: Nhấp chọn một CLB trên Treemap để highlight số liệu bàn thắng tương ứng ở các biểu đồ cột.

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Biểu đồ Clustered Column phân tách rõ ràng phong độ Sân nhà và Sân khách.
- [x] Treemap thể hiện tương quan đóng góp giữa Giải quốc nội và Cúp Châu Âu.
- [x] Scatter chart hỗ trợ phân tích quy mô sân vận động và quy mô đội hình.
