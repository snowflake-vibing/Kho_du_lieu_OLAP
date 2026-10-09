# HƯỚNG DẪN POWER BI - PHẦN 1: KHỞI TẠO PROJECT, KẾT NỐI DỮ LIỆU & DAX MODELING

---

## 1. MỤC TIÊU HUẤN LUYỆN
Tạo file báo cáo **Power BI Desktop (`.pbix`)**, nạp cơ sở dữ liệu `DW_Football_Analytics` từ SQL Server (hoặc kết nối SSAS Live Connection), thiết lập mô hình mối quan hệ Star Schema và viết danh sách **DAX Measures** tiêu chuẩn.

---

## 2. BƯỚC 1: KẾT NỐI DỮ LIỆU VÀO POWER BI DESKTOP

1. Mở ứng dụng **Power BI Desktop**.
2. Chọn **Get Data** $\rightarrow$ chọn **SQL Server Database** (hoặc **SQL Server Analysis Services database**).
3. Nhập thông tin kết nối:
   - **Server**: `localhost` (hoặc tên server SQL Server).
   - **Database**: `DW_Football_Analytics`.
   - **Data Connectivity mode**: Chọn **Import** (để nạp dữ liệu vào bộ nhớ RAM Power BI tối ưu tốc độ) hoặc **DirectQuery**.
4. Chọn các bảng dữ liệu:
   - `FACT_Player_Match_Perf`
   - `DIM_Player`
   - `DIM_Club`
   - `DIM_Competition`
   - `DIM_Game`
   - `DIM_Time`
5. Nhấn **Load**.

---

## 2. BƯỚC 2: KIỂM TRA MÔ HÌNH DỮ LIỆU (MODEL VIEW)

1. Chuyển sang thẻ **Model View** trong Power BI Desktop.
2. Kiểm tra các mối liên kết (1 - Many Relationships):
   - `DIM_Player [Player_ID]` (1) $\rightarrow$ `FACT_Player_Match_Perf [Player_ID]` (*)
   - `DIM_Club [Club_ID]` (1) $\rightarrow$ `FACT_Player_Match_Perf [Club_ID]` (*)
   - `DIM_Competition [Competition_ID]` (1) $\rightarrow$ `FACT_Player_Match_Perf [Competition_ID]` (*)
   - `DIM_Game [Game_ID]` (1) $\rightarrow$ `FACT_Player_Match_Perf [Game_ID]` (*)
   - `DIM_Time [Time_ID]` (1) $\rightarrow$ `FACT_Player_Match_Perf [Time_ID]` (*)
3. Đảm bảo tất cả các đường liên kết có hướng lọc **Single** (Dimension filters Fact).

---

## 3. BƯỚC 3: XÂY DỰNG THƯ VIỆN DAX MEASURES

Tạo một bối cảnh tính toán (Measure Table) đặt tên là `_Measures` và tạo các câu lệnh DAX sau:

```dax
// 1. Tổng số bàn thắng
Total Goals = SUM(FACT_Player_Match_Perf[Goals])

// 2. Tổng số đường kiến tạo
Total Assists = SUM(FACT_Player_Match_Perf[Assists])

// 3. Tổng đóng góp bàn thắng + kiến tạo
Total Goal Contributions = [Total Goals] + [Total Assists]

// 4. Tổng số phút thi đấu
Total Minutes Played = SUM(FACT_Player_Match_Perf[Minutes_Played])

// 5. Số phút thi đấu trung bình mỗi trận
Avg Minutes Per Match = DIVIDE([Total Minutes Played], COUNTROWS(FACT_Player_Match_Perf), 0)

// 6. Tổng số thẻ vàng
Total Yellow Cards = SUM(FACT_Player_Match_Perf[Yellow_Cards])

// 7. Tổng số thẻ đỏ
Total Red Cards = SUM(FACT_Player_Match_Perf[Red_Cards])

// 8. Số trận đá chính (Starter)
Total Starter Games = CALCULATE(COUNTROWS(FACT_Player_Match_Perf), FACT_Player_Match_Perf[Is_Starter] = 1)

// 9. Tỷ lệ trận đá chính (%)
Starter Rate % = DIVIDE([Total Starter Games], COUNTROWS(FACT_Player_Match_Perf), 0)

// 10. Số phút trung bình cho mỗi bàn thắng (Mins Per Goal)
Mins Per Goal = DIVIDE([Total Minutes Played], [Total Goals], 0)
```

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Nạp đủ 6 bảng từ SQL Server vào Power BI Model.
- [x] Star Schema Relationship hoàn chỉnh và hoạt động đúng.
- [x] 10 DAX Measures được tạo và format đúng định dạng hiển thị.
