# HƯỚNG DẪN SSAS - PHẦN 5: DEPLOY, ĐỐI SOÁT KHO & 15 CÂU TRUY VẤN MDX

---

## 1. MỤC TIÊU

Triển khai (**Deploy & Process**) dự án `SSAS_Football_Transfermarkt` lên SSAS Multidimensional Engine, đối soát tổng số liệu giữa SQL Server (`DW_Football_Transfermarkt`) và Cube `[DW Football Transfermarkt]`, và tổng hợp đủ **15 câu truy vấn nghiệp vụ** theo Mục 1.3 Chương 1.

---

## 2. BƯỚC 1: DEPLOY VÀ PROCESS SSAS CUBE

1. Trong Solution Explorer, bấm phải vào **`SSAS_Football_Transfermarkt`** $\rightarrow$ **Properties** $\rightarrow$ **Deployment**:
   - **Server**: `localhost` (hoặc tên instance SSAS cục bộ).
   - **Database**: `SSAS_Football_Transfermarkt`.
   - **Processing Option**: `Do Full`.
2. Nhấn **OK**.
3. Chọn **Build $\rightarrow$ Deploy Solution** (hoặc nhấn `F5`).
4. Kiểm tra cửa sổ **Deployment Progress** báo **`Deployment Completed Successfully`** (0 errors, 0 warnings).

---

## 3. BƯỚC 2: ĐỐI SOÁT TỔNG SỐ LIỆU GIỮA SQL SERVER VÀ SSAS CUBE

Mở **SQL Server Management Studio (SSMS)** $\rightarrow$ kết nối **Analysis Services** $\rightarrow$ bấm phải Cube **`DW Football Transfermarkt`** $\rightarrow$ **New Query $\rightarrow$ MDX** và chạy lệnh đối soát:

```mdx
SELECT
    {
        [Measures].[Official Match Count],
        [Measures].[Official Team Match Count],
        [Measures].[Appearance Count],
        [Measures].[Distinct Player Count],
        [Measures].[Minutes Played],
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,
    NON EMPTY [DIM Game].[Season].[Season].MEMBERS ON ROWS
FROM [DW Football Transfermarkt];
```

| Mùa giải | Số trận | Lượt ra sân | Cầu thủ | Số phút | Bàn thắng | Kiến tạo | Thẻ vàng | Thẻ đỏ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022/2023 | 3.691 | 106.281 | 5.296 | 6.848.543 | 9.563 | 7.340 | 14.478 | 455 |
| 2023/2024 | 3.589 | 104.466 | 5.239 | 6.714.184 | 9.610 | 7.399 | 14.216 | 372 |
| **Tổng toàn kho** | **7.280** | **210.747** | **7.069** | **13.562.727** | **19.173** | **14.739** | **28.694** | **827** |

> **Lưu ý về giải `UCOL`:** `DIM_Game` có 282 trận của giải `UCOL` (141 trận mùa 2022/2023 và 141 trận mùa 2023/2024), nhưng `FACT_Player_Match_Perf` có 0 lượt ra sân của giải này. Nhờ tách 4 Measure Groups riêng biệt, thống kê cấp trận giữ đủ 7.280 trận trong khi thống kê cầu thủ phản ánh đúng 210.747 lượt ra sân.

---

## 4. BƯỚC 3: TỔNG HỢP 15 CÂU TRUY VẤN NGHIỆP VỤ (THEO MỤC 1.3 CHƯƠNG 1)

Chi tiết đầy đủ T-SQL đối chiếu, hướng dẫn Cube Browser, Excel PivotTable, mã MDX chuẩn và bảng số liệu thực tế cho từng câu nằm trong thư mục [mdx/](../mdx/README.md):

| Câu | Tài liệu chi tiết | Tệp `.mdx` thực thi | Cấp độ (Measure Group) | Mốc kết quả kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [query_01.md](../mdx/query_01.md) | [query_01.mdx](../mdx/query_01.mdx) | `FACT Player Match Perf` | Top 10 ghi bàn GB1 2023/2024 (Haaland: 27 bàn) |
| **02** | [query_02.md](../mdx/query_02.md) | [query_02.mdx](../mdx/query_02.mdx) | `FACT Player Match Perf` | Top 10 tiền vệ kiến tạo `domestic_league` (De Bruyne: 28) |
| **03** | [query_03.md](../mdx/query_03.md) | [query_03.mdx](../mdx/query_03.mdx) | `FACT Player Match Perf` | 99 cầu thủ đạt `Goal Contributions > 20` mùa 2023/2024 |
| **04** | [query_04.md](../mdx/query_04.md) | [query_04.mdx](../mdx/query_04.mdx) | `FACT Player Match Perf` + `Context` | 28 độ tuổi hợp lệ (15–42) năm 2023 |
| **05** | [query_05.md](../mdx/query_05.md) | [query_05.mdx](../mdx/query_05.mdx) | `FACT Player Match Perf` | 13 `Sub_Position` × 3 `Foot` (`left`/`right`/`both`) |
| **06** | [query_06.md](../mdx/query_06.md) | [query_06.mdx](../mdx/query_06.mdx) | `FACT Player Match Perf` | 4 tuyến chính (chiều cao TB trên cầu thủ duy nhất) |
| **07** | [query_07.md](../mdx/query_07.md) | [query_07.mdx](../mdx/query_07.mdx) | `FACT Player Match Perf` | 75 quốc tịch ghi bàn tại Anh (Pareto 80% = 18 nước) |
| **08** | [query_08.md](../mdx/query_08.md) | [query_08.mdx](../mdx/query_08.mdx) | `FACT Player Match Perf` | Top 10 `Goals Per 90` (`≥ 900` phút, xếp theo tỷ lệ chưa làm tròn) |
| **09** | [query_09.md](../mdx/query_09.md) | [query_09.mdx](../mdx/query_09.mdx) | `FACT Player Match Perf` + `Context` | 207 CLB cuối tuần (Nhà vs Khách: tổng, số trận và TB/trận) |
| **10** | [query_10.md](../mdx/query_10.md) | [query_10.mdx](../mdx/query_10.mdx) | `FACT Club Match Official` | Real Madrid (`418`): 101 trận, 216 bàn chính thức, 92 cặp |
| **11** | [query_11.md](../mdx/query_11.md) | [query_11.mdx](../mdx/query_11.mdx) | `DIM Game` + `DIM Home Club` | 23 CLB sân > 60.000 chỗ, tổng 993 trận sân nhà |
| **12** | [query_12.md](../mdx/query_12.md) | [query_12.mdx](../mdx/query_12.mdx) | `FACT Player Match Perf` + `Context` | 3.967 bộ `Club × Manager × Year_Month_Key` (+ số trận & TB/trận) |
| **13** | [query_13.md](../mdx/query_13.md) | [query_13.mdx](../mdx/query_13.mdx) | `FACT Player Match Perf` + `Distinct` | 235 CLB ra sân theo `Squad_Size` (8 CLB bổ sung `Unknown`) |
| **14** | [query_14.md](../mdx/query_14.md) | [query_14.mdx](../mdx/query_14.mdx) | `DIM Game` + `Home/Away Club` | 1.196 trận đấu ≥ 5 bàn thắng (tối đa 10 bàn) |
| **15** | [query_15.md](../mdx/query_15.md) | [query_15.mdx](../mdx/query_15.mdx) | `FACT Player Match Perf` | 676 cầu thủ sinh từ 01/01/2004 trên 441 ngày (403 bàn) |

---

## 5. KẾT NỐI NHANH CUBE BROWSER & EXCEL PIVOTTABLE

1. **Cube Browser (Visual Studio / SSDT)**:
   - Mở `DW Football Transfermarkt.cube` $\rightarrow$ tab **Browser** $\rightarrow$ bật **Design Mode**.
   - Các bộ lọc số học hoặc tập hợp phức tạp sử dụng toán tử **`Custom`** với biểu thức MDX (chỉ dùng các toán tử thực sự có sẵn trong SSDT: `Equal`, `Not Equal`, `In`, `Not In`, `Contains`, `Begins With`, `Range`, `Custom`).
2. **Excel PivotTable**:
   - Vào **Data $\rightarrow$ Get Data $\rightarrow$ From Database $\rightarrow$ From Analysis Services**.
   - Server: `localhost` $\rightarrow$ Database: `SSAS_Football_Transfermarkt` $\rightarrow$ Cube: `DW Football Transfermarkt`.
   - Khi một trường hàng cần áp dụng đồng thời 2 điều kiện Value Filter (như Câu 8: `Minutes Played ≥ 900` và `Top 10 by Goals Per 90`), dùng **PivotTable Analyze $\rightarrow$ Fields, Items, & Sets $\rightarrow$ Create Set Using MDX...**.

---

## 6. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Deploy & Process toàn bộ Cube `DW Football Transfermarkt` thành công (0 errors, 0 warnings).
- [x] Khớp 100% số liệu tổng kho giữa SQL Server (Chương 2) và SSAS Cube (Chương 3).
- [x] Đồng bộ đủ 15 câu truy vấn từ `query_01` đến `query_15` với `Bao_cao_OLAP.docx` và `Chuong_3_SSAS.docx`.
