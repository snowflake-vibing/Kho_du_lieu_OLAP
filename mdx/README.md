# BỘ 15 CÂU TRUY VẤN NGHIỆP VỤ ĐA CHIỀU MDX (MULTIDIMENSIONAL EXPRESSIONS)

Tài liệu này tổng hợp **15 câu truy vấn nghiệp vụ đa chiều (MDX Queries)** được thiết kế và tối ưu riêng cho **Cube `[DW Football Transfermarkt]`** (thuộc hệ thống Kho dữ liệu bóng đá Châu Âu `DW_Football_Analytics`).

Các truy vấn được chuyển đổi tương đương và nâng cao từ 15 câu truy vấn T-SQL tại [docs/15_queries.md](file:///d:/Kho_du_lieu_OLAP/docs/15_queries.md), tận dụng triệt để kiến trúc OLAP phân cấp đa chiều, tiền tính toán (Pre-aggregations), Bitmap Indexing và Block Computation của Microsoft SQL Server Analysis Services (SSAS).

---

## BẢNG TỔNG HỢP 15 CÂU TRUY VẤN MDX

| STT | File Tài Liệu | Mục tiêu nghiệp vụ MDX | Chiều & Thước đo chính | Các hàm MDX cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [query_01.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_01.md) | Top 10 Vua dội bom Ngoại Hạng Anh mùa 2023/2024 | `DIM Player`, `DIM Competition`, `DIM Time`, `Goals` | `TOPCOUNT`, `NONEMPTY`, `MEMBERS` |
| **02** | [query_02.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_02.md) | Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG | `DIM Player`, `DIM Competition`, `Assists` | `TOPCOUNT`, `CROSSJOIN`, `NONEMPTY` |
| **03** | [query_03.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_03.md) | Cầu thủ xuất sắc có trên 20 đóng góp bàn thắng (G+A) | `DIM Player`, `DIM Time`, `Goal Contributions`, `Minutes Played` | `FILTER`, `ORDER (BDESC)`, `NONEMPTY` |
| **04** | [query_04.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_04.md) | Hiệu suất bàn thắng & số phút TB theo độ tuổi năm 2023 | `DIM Player`, `DIM Time`, `Avg Minutes Played`, `Goals` | `WITH MEMBER`, `IIF`, `ORDER (BASC)` |
| **05** | [query_05.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_05.md) | So sánh bàn thắng theo chân thuận & vị trí chi tiết | `DIM Player` (`Sub Position`, `Foot`), `Goals` | `CROSSJOIN`, `EXCEPT`, `ORDER (DESC)` |
| **06** | [query_06.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_06.md) | Chiều cao trung bình, bàn thắng và thẻ phạt theo vị trí chính | `DIM Player` (`Main Position`), `Avg Height Cm`, `Goals`, `Cards` | `WITH MEMBER`, `AVG`, `EXISTING`, `ORDER` |
| **07** | [query_07.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_07.md) | Bàn thắng theo quốc tịch cầu thủ tại các giải ở Anh | `DIM Player`, `DIM Competition`, `Goals` | `NONEMPTY`, `EXCEPT`, `ORDER (BDESC)` |
| **08** | [query_08.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_08.md) | Top 15 "Siêu dự bị" ghi nhiều bàn nhất khi vào sân thay người | `DIM Player`, `FACT Player Match Perf`, `Goals`, `Minutes Played` | `TOPCOUNT`, `FILTER`, `NONEMPTY` |
| **09** | [query_09.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_09.md) | Hiệu năng Sân nhà vs Sân khách x Cuối tuần vs Ngày thường | `DIM Club`, `DIM Time`, `Goals`, `Yellow Cards` | `CROSSJOIN`, `NON EMPTY`, `EXCEPT` |
| **10** | [query_10.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_10.md) | Bàn thắng Real Madrid ghi vào lưới đối thủ theo từng Quý | `DIM Club`, `Opponent Club`, `DIM Time`, `Goals` | Role-Playing Dim, `NONEMPTY`, `ORDER` |
| **11** | [query_11.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_11.md) | Số trận đấu tại các SVĐ có sức chứa > 60.000 khán giả | `DIM Club`, `DIM Game`, `Total Matches Played` | `WITH MEMBER`, `DISTINCTCOUNT`, `FILTER` |
| **12** | [query_12.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_12.md) | Thẻ phạt phân theo Huấn luyện viên trưởng & Tháng trong năm | `DIM Club`, `DIM Time`, `Yellow Cards`, `Red Cards` | `CROSSJOIN`, `FILTER`, `NONEMPTY`, `ORDER` |
| **13** | [query_13.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_13.md) | Lực lượng cầu thủ thực tế ra sân theo quy mô đội hình | `DIM Club`, `DIM Player`, `Active Players Count`, `Count` | `WITH MEMBER`, `DISTINCTCOUNT`, `EXISTING` |
| **14** | [query_14.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_14.md) | Thống kê các trận cầu mưa bàn thắng ($\ge 5$ bàn) qua các vòng | `DIM Game`, `Measures.[Goals]` | `FILTER`, `NONEMPTY`, `ORDER (BDESC)` |
| **15** | [query_15.md](file:///d:/Kho_du_lieu_OLAP/mdx/query_15.md) | Hiệu suất & thẻ phạt của lứa cầu thủ trẻ (sinh từ 2004) theo ngày | `DIM Player`, `DIM Time`, `Goals`, `Cards` | `WITH SET`, `PROPERTIES`, `NONEMPTY`, `ORDER` |

---

## HƯỚNG DẪN THỰC THI TRÊN SQL SERVER ANALYSIS SERVICES (SSAS)

1. **Khởi động SQL Server Management Studio (SSMS):**
   * Server Type: Chọn **Analysis Services**.
   * Server Name: Nhập địa chỉ máy chủ SSAS của bạn (ví dụ: `localhost` hoặc `DESKTOP-XXX\SSAS`).
   * Authentication: Windows Authentication.
2. **Chọn Database & Cube:**
   * Trong cửa sổ **Object Explorer**, mở rộng nhánh `Databases` $\to$ Chọn database triển khai Cube (ví dụ: `SSAS_Football_Transfermarkt`).
   * Mở rộng nhánh `Cubes` $\to$ Chuột phải vào Cube **`DW Football Transfermarkt`** $\to$ Chọn **New Query** $\to$ **MDX**.
3. **Thực thi truy vấn:**
   * Mở từng file trong thư mục `mdx/` (từ `query_01.md` đến `query_15.md`), sao chép đoạn mã trong mục **Mã truy vấn MDX chuẩn**.
   * Dán vào cửa sổ Editor của SSMS và nhấn **Execute (F5)**.
   * Kết quả sẽ được hiển thị ngay lập tức dưới dạng lưới ma trận ô dữ liệu (OLAP Grid).

---

## 📑 BÁO CÁO KIỂM ĐỊNH HỌC THUẬT & ĐỐI CHIẾU HÀM MDX (QUALITY CHECKLIST)

Nhằm phục vụ công tác nghiệm thu, chấm điểm đồ án và bảo vệ chuyên sâu trước Giảng viên / Hội đồng, toàn bộ 15 câu truy vấn đã được kiểm định khắt khe tại tài liệu:
👉 **[checklist.md](checklist.md)**: **Bảng đối chiếu & Kiểm định chất lượng 15 câu truy vấn MDX**

Nội dung thẩm định bao gồm:
- **Ma trận đối chiếu độ phủ 7 nhóm hàm MDX** (Tập hợp, Lọc/Sắp xếp, Phân cấp, Thống kê, Logic, Thuộc tính, Tính toán) - Đạt tỷ lệ bao phủ 100%.
- **Bảng phân tích định lượng độ phức tạp tính toán (Time & Space Complexity)** cho cả 15 câu.
- **Bóc tách kiến trúc thực thi SSAS**: Cơ chế tối ưu giữa **Storage Engine (SE)** và **Formula Engine (FE)**, giải thuật Min-Heap $O(N \log k)$, Block Computation.
- **Bộ 5 câu hỏi phản biện chuyên sâu** thường gặp khi bảo vệ đồ án cùng đáp án chuẩn mực.

