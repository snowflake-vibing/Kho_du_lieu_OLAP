# HƯỚNG DẪN SSAS - PHẦN 5: DEPLOY PROJECT & 15 CÂU TRUY VẤN OLAP / MDX

---

## 1. MỤC TIÊU HUẤN LUYỆN
Hướng dẫn thực hiện **Deploy & Process** dự án SSAS lên server SQL Server Analysis Services Engine, sau đó thực thi và đánh giá **15 câu truy vấn nghiệp vụ bóng đá** bằng **Cube Browser**, **Excel PivotTable** và **ngôn ngữ MDX**.

---

## 2. BƯỚC 1: DEPLOY VÀ PROCESS SSAS CUBE

1. Trong Solution Explorer, chuột phải vào tên Project **`DW_Football_SSAS`** $\rightarrow$ chọn **Properties**.
2. Chọn mục **Deployment**:
   - **Server**: Nhập tên SSAS Instance (ví dụ `localhost` hoặc `localhost\MSOLAP`).
   - **Database**: `DW_Football_SSAS`.
   - **Processing Option**: `Do Full`.
3. Nhấn **OK**.
4. Chuột phải vào Project `DW_Football_SSAS` $\rightarrow$ chọn **Deploy**.
5. Cửa sổ **Deployment Progress** hiển thị log tính toán.
6. Đảm bảo trạng thái báo **`Deployment Completed Successfully`**.

---

## 3. BƯỚC 2: THỰC THI 15 CÂU TRUY VẤN MDX VÀ PHÂN TÍCH

Dưới đây là cú pháp 15 câu truy vấn MDX mẫu đại diện phục vụ phân tích đa chiều:

### Câu 1: Top 10 Chân sút ghi bàn nhiều nhất mùa giải 2023/2024
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Assists]} ON COLUMNS,
    TOPCOUNT(
        [DIM Player].[Player Name].[Player Name].Members,
        10,
        [Measures].[Total Goals]
    ) ON ROWS
FROM [DW_Football_Cube]
WHERE ([DIM Time].[Season].&[2023]);
```

### Câu 2: Hiệu suất bàn thắng & kiến tạo theo Vị trí thi đấu chính
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Assists], [Measures].[Contributions Per 90 Mins]} ON COLUMNS,
    [DIM Player].[Main Position].[Main Position].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 3: Thống kê số phút thi đấu và số trận đá chính (Starter) theo Câu lạc bộ
```mdx
SELECT 
    {[Measures].[Total Minutes Played], [Measures].[Total Starter Appearances], [Measures].[Starter Rate Percent]} ON COLUMNS,
    ORDER(
        [DIM Club].[Club Name].[Club Name].Members,
        [Measures].[Total Minutes Played],
        BDESC
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 4: Thống kê kỉ luật thẻ phạt (Yellow & Red Cards) theo Giải đấu
```mdx
SELECT 
    {[Measures].[Total Yellow Cards], [Measures].[Total Red Cards]} ON COLUMNS,
    [DIM Competition].[Competition Name].[Competition Name].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 5: So sánh hiệu suất bàn thắng Sân nhà vs Sân khách của các CLB
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Appearances]} ON COLUMNS,
    CROSSJOIN(
        [DIM Club].[Club Name].[Club Name].Members,
        {[DIM Game].[Is Home Game].&[1], [DIM Game].[Is Home Game].&[0]}
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 6: Tổng số phút thi đấu theo Quý trong năm
```mdx
SELECT 
    {[Measures].[Total Minutes Played]} ON COLUMNS,
    [DIM Time].[Calendar Hierarchy].[Quarter].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 7: Phân tích đóng góp bàn thắng của Cầu thủ Trẻ (< 21 tuổi)
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Assists]} ON COLUMNS,
    FILTER(
        [DIM Player].[Player Name].[Player Name].Members,
        [DIM Player].[Age].CurrentMember.Properties("Key") < 21
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 8: Top 5 Cầu thủ dính thẻ đỏ nhiều nhất
```mdx
SELECT 
    {[Measures].[Total Red Cards], [Measures].[Total Yellow Cards]} ON COLUMNS,
    TOPCOUNT(
        [DIM Player].[Player Name].[Player Name].Members,
        5,
        [Measures].[Total Red Cards]
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 9: Tỷ lệ đá chính theo từng mùa giải bóng đá
```mdx
SELECT 
    {[Measures].[Total Appearances], [Measures].[Total Starter Appearances], [Measures].[Starter Rate Percent]} ON COLUMNS,
    [DIM Time].[Season].[Season].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 10: Thống kê hiệu suất bàn thắng theo Chân thuận (Left vs Right Foot)
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Appearances]} ON COLUMNS,
    [DIM Player].[Foot].[Foot].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 11: Phân tích số trận thi đấu theo từng Quốc tịch Cầu thủ
```mdx
SELECT 
    {[Measures].[Total Appearances], [Measures].[Total Goals]} ON COLUMNS,
    TOPCOUNT(
        [DIM Player].[Country Of Citizenship].[Country Of Citizenship].Members,
        10,
        [Measures].[Total Appearances]
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 12: Thống kê tổng bàn thắng theo HLV Trưởng (Coach Name)
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Appearances]} ON COLUMNS,
    ORDER(
        [DIM Club].[Coach Name].[Coach Name].Members,
        [Measures].[Total Goals],
        BDESC
    ) ON ROWS
FROM [DW_Football_Cube];
```

### Câu 13: Trung bình số phút thi đấu mỗi trận theo Vị trí
```mdx
SELECT 
    {[Measures].[Avg Minutes Per Match]} ON COLUMNS,
    [DIM Player].[Main Position].[Main Position].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 14: Thống kê tổng thẻ phạt theo Nhóm tuổi Cầu thủ
```mdx
SELECT 
    {[Measures].[Total Yellow Cards], [Measures].[Total Red Cards]} ON COLUMNS,
    [DIM Player].[Age].[Age].Members ON ROWS
FROM [DW_Football_Cube];
```

### Câu 15: Thống kê tổng hợp Toàn diện Hiệu suất CLB theo Giải đấu
```mdx
SELECT 
    {[Measures].[Total Goals], [Measures].[Total Assists], [Measures].[Total Yellow Cards], [Measures].[Total Red Cards]} ON COLUMNS,
    CROSSJOIN(
        [DIM Competition].[Competition Name].[Competition Name].Members,
        [DIM Club].[Club Name].[Club Name].Members
    ) ON ROWS
FROM [DW_Football_Cube];
```

---

## 4. BƯỚC 3: PHÂN TÍCH QUA EXCEL PIVOT TABLE & CUBE BROWSER

1. **Sử dụng Cube Browser trong Visual Studio**:
   - Mở Cube `DW_Football_Cube.cube` $\rightarrow$ Chuyển sang tab **Browser**.
   - Kéo các Measure (`Total Goals`, `Total Assists`) vào vùng **Values**.
   - Kéo `Player_Name` hoặc `Club_Name` vào vùng **Rows**.
   - Nhấn **Execute Query** để xem kết quả tức thì.

2. **Sử dụng Excel PivotTable kết nối SSAS**:
   - Mở Excel $\rightarrow$ Vào thẻ **Data** $\rightarrow$ **Get Data** $\rightarrow$ **From Database** $\rightarrow$ **From Analysis Services**.
   - Server name: `localhost` $\rightarrow$ Select Database: `DW_Football_SSAS` $\rightarrow$ Select Cube: `DW_Football_Cube`.
   - Nhấn **Finish** để chèn PivotTable.
   - Kéo thả các thuộc tính đa chiều và dựng biểu đồ trực quan OLAP.

---

## 5. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Deploy SSAS thành công không báo lỗi.
- [x] 15 câu truy vấn MDX chạy thành công và trả về kết quả chính xác.
- [x] Excel PivotTable kết nối mượt mà tới SSAS OLAP Engine.
