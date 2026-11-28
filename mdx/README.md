# BỘ CÂU TRUY VẤN NGHIỆP VỤ ĐA CHIỀU MDX (MULTIDIMENSIONAL EXPRESSIONS)

Tài liệu này tổng hợp đầy đủ **15 câu truy vấn nghiệp vụ đa chiều (MDX Queries)** được chuẩn hóa đồng bộ với Chương 1 ([Bao_cao_OLAP.docx](../bao-cao-olap/Bao_cao_OLAP.docx)) và Chương 3 ([Chuong_3_SSAS.docx](../bao-cao-olap/Chuong_3_SSAS.docx)), triển khai trên **Cube `[DW Football Transfermarkt]`** thuộc SSAS Database **`SSAS_Football_Transfermarkt`** (nguồn SQL Server **`DW_Football_Transfermarkt`**).

Cả 15 câu truy vấn (gồm cả 5 câu trước đây từng nằm ở `archive/`) hiện được đặt tập trung trực tiếp trong thư mục `mdx/`, mỗi câu gồm đầy đủ tệp hướng dẫn `.md` (T-SQL đối chiếu, Cube Browser, Excel PivotTable, MDX, bảng kết quả thực tế từ `football/cleaned_data/new_version/`, độ phức tạp) và tệp thực thi `.mdx`.

---

## 📚 TÀI LIỆU LIÊN QUAN

- 👉 **[tutorial/README.md](./tutorial/README.md)**: Giáo trình Lý thuyết & Thực hành Truy vấn Đa chiều MDX.
- 👉 **[checklist.md](./checklist.md)**: Bảng đối chiếu, độ phủ hàm và kiểm định chất lượng 15 câu truy vấn MDX.
- 👉 **[../ssas/ssas_overview.md](../ssas/ssas_overview.md)**: Bộ hướng dẫn dựng SSAS Project `SSAS_Football_Transfermarkt` từ Data Source, DSV, Dimensions đến Cube & Deploy.
- 👉 **[../ssas/ke_hoach_chinh_sua_ssas_mdx.md](../ssas/ke_hoach_chinh_sua_ssas_mdx.md)**: Kế hoạch chỉnh sửa chi tiết SSAS & MDX từ bản cũ sang bản mới (10 câu cũ $\rightarrow$ 15 câu mới).

---

## 🌟 BẢNG TỔNG HỢP 15 CÂU TRUY VẤN MDX CHÍNH THỨC

| STT | Hướng dẫn chi tiết | Tệp `.mdx` | Measure Group (Grain) | Thao tác OLAP | Hàm / Kỹ thuật MDX cốt lõi |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **01** | [query_01.md](./query_01.md) | [query_01.mdx](./query_01.mdx) | `FACT Player Match Perf` | Slice & Top-N | `TOPCOUNT`, `NONEMPTY`, `Player ID` |
| **02** | [query_02.md](./query_02.md) | [query_02.mdx](./query_02.mdx) | `FACT Player Match Perf` | Slice & Top-N | `TOPCOUNT`, `NONEMPTY`, `.MEMBERS` |
| **03** | [query_03.md](./query_03.md) | [query_03.mdx](./query_03.mdx) | `FACT Player Match Perf` | Slice & Filter | `FILTER`, `ORDER (BDESC)`, `Goal Contributions` |
| **04** | [query_04.md](./query_04.md) | [query_04.mdx](./query_04.mdx) | `FACT Player Match Perf` + `Context` | Slice & Avg | `WITH SET`, `EXCEPT`, `ORDER (BASC)`, `Avg Minutes Played` |
| **05** | [query_05.md](./query_05.md) | [query_05.mdx](./query_05.mdx) | `FACT Player Match Perf` | Dice & Pivot | `EXCEPT`, `NON EMPTY`, `ORDER (BDESC)` |
| **06** | [query_06.md](./query_06.md) | [query_06.mdx](./query_06.mdx) | `FACT Player Match Perf` | Aggregate | `AVG`, `MAX`, `MIN`, `EXISTING`, `CrossJoin` |
| **07** | [query_07.md](./query_07.md) | [query_07.mdx](./query_07.mdx) | `FACT Player Match Perf` | Slice & Pareto | `EXCEPT`, `NONEMPTY`, `ORDER (BDESC)`, (`TOPPERCENT`) |
| **08** | [query_08.md](./query_08.md) | [query_08.mdx](./query_08.mdx) | `FACT Player Match Perf` | Threshold & Top-N | `TOPCOUNT`, `FILTER`, `Goals Per 90` |
| **09** | [query_09.md](./query_09.md) | [query_09.mdx](./query_09.mdx) | `FACT Player Match Perf` + `Context` | Slice & Pivot | `CrossJoin`, `NONEMPTY`, `Covered Match Count`, `Goals/Yellow Per Match` |
| **10** | [query_10.md](./query_10.md) | [query_10.mdx](./query_10.mdx) | `FACT Club Match Official` | Role-Playing & Slice | `CrossJoin`, `NONEMPTY`, `Year Quarter Key`, `DIM Opponent Club` |
| **11** | [query_11.md](./query_11.md) | [query_11.mdx](./query_11.mdx) | `DIM Game` + `DIM Home Club` | Match Aggregation | `FILTER`, `EXISTING`, `Stadium Seats Value` |
| **12** | [query_12.md](./query_12.md) | [query_12.mdx](./query_12.mdx) | `FACT Player Match Perf` + `Context` | Multi-Dim Slice | `WITH SET`, `CrossJoin`, `Covered Match Count`, `Year Month Key` |
| **13** | [query_13.md](./query_13.md) | [query_13.mdx](./query_13.mdx) | `FACT Player Match Perf` + `Distinct` | Distinct Count | `DistinctCount(Player_ID)`, `CrossJoin`, `NONEMPTY` |
| **14** | [query_14.md](./query_14.md) | [query_14.mdx](./query_14.mdx) | `DIM Game` + `Home/Away Club` | Match Filter | `FILTER`, `*`, `NONEMPTY`, `Total Match Goals` |
| **15** | [query_15.md](./query_15.md) | [query_15.mdx](./query_15.mdx) | `FACT Player Match Perf` | Date-Range Slice | `WITH SET`, `CDate`, `FILTER`, Subcube `SELECT` |

> **Lưu ý lược đồ DSV & Calculated Measures mới nhất:** Hai thuộc tính kỳ (`Year_Quarter_Key`, `Year_Month_Key`) trên `DIM_Time` được tạo bằng **Named Calculations trong SSAS DSV** (`[Year] * 10 + [Quarter]` và `[Year] * 100 + [Month]`) thay vì cột vật lý trong SQL Server; khi chạy T-SQL đối chiếu cho Câu 10 và Câu 12 cần tính inline trong `SELECT`/`GROUP BY`. Cube đồng thời định nghĩa sẵn `Covered Match Count`, `Goals Per Match`, `Yellow Cards Per Match` và `Red Cards Per Match` phục vụ Câu 09 và Câu 12.
>
> Các tài liệu nháp cũ của phiên bản lược đồ trước đã được chuyển vào [`archive/legacy_v1/`](./archive/legacy_v1/) để lưu vết lịch sử.

---

## HƯỚNG DẪN THỰC THI TRÊN SQL SERVER ANALYSIS SERVICES (SSAS)

1. **Khởi động SQL Server Management Studio (SSMS):**
   - Server Type: **Analysis Services**
   - Server Name: `localhost` (hoặc tên instance SSAS cục bộ)
   - Authentication: **Windows Authentication**
2. **Chọn Database & Cube:**
   - Mở rộng `Databases` $\rightarrow$ chọn **`SSAS_Football_Transfermarkt`**.
   - Mở rộng `Cubes` $\rightarrow$ bấm chuột phải vào **`DW Football Transfermarkt`** $\rightarrow$ **New Query** $\rightarrow$ **MDX**.
3. **Thực thi truy vấn:**
   - Mở trực tiếp tệp `query_01.mdx` đến `query_15.mdx` (hoặc sao chép từ `query_01.md` đến `query_15.md`).
   - Dán vào cửa sổ MDX Query Editor và nhấn **Execute (`F5`)**.
