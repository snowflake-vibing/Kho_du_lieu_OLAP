# GIÁO TRÌNH LÝ THUYẾT & THỰC HÀNH TRUY VẤN ĐA CHIỀU MDX (MULTIDIMENSIONAL EXPRESSIONS)

> **Môn học**: Kho Dữ Liệu & Phân Tích Dữ Liệu Lớn (Data Warehouse & OLAP)  
> **Hệ quản trị áp dụng**: Microsoft SQL Server Analysis Services (SSAS Multidimensional)  
> **Cube thực hành**: `[DW Football Transfermarkt]`  
> **Tài liệu tham khảo chính**: Microsoft OLE DB for OLAP Specification, Fast Track to MDX, The Definitive Guide to DAX/MDX.

---

## MỤC LỤC TỔNG QUAN

1. [Tổng quan về Ngôn ngữ MDX & Bối cảnh Lịch sử](#1-tổng-quan-về-ngôn-ngữ-mdx--bối-cảnh-lịch-sử)
2. [Các khái niệm Cốt lõi trong Mô hình Đa chiều (Core Concepts)](#2-các-khái-niệm-cốt-lõi-trong-mô-hình-đa-chiều-core-concepts)
3. [So sánh Chuyên sâu: SQL (Quan hệ) vs MDX (Đa chiều)](#3-so-sánh-chuyên-sâu-sql-quan-hệ-vs-mdx-đa-chiều)
4. [Cấu trúc Cú pháp Cơ bản của một Truy vấn MDX](#4-cấu-trúc-cú-pháp-cơ-bản-của-một-truy-vấn-mdx)
5. [Khai báo Thành viên Tính toán & Tập hợp Đặt tên (`WITH` Clause)](#5-khai-báo-thành-viên-tính-toán--tập-hợp-đặt-tên-with-clause)
6. [Điều hướng Phân cấp & Quan hệ Cây (Hierarchical Navigation)](#6-điều-hướng-phân-cấp--quan-hệ-cây-hierarchical-navigation)
7. [Phân tích Chuỗi Thời gian (Time Series / Time Intelligence)](#7-phân-tích-chuỗi-thời-gian-time-series--time-intelligence)
8. [Đại số Tập hợp & Xử lý Không gian Đa chiều (Set Algebra)](#8-đại-số-tập-hợp--xử-lý-không-gian-đa-chiều-set-algebra)
9. [Lọc Dữ liệu & Sắp xếp (Filtering & Sorting)](#9-lọc-dữ-liệu--sắp-xếp-filtering--sorting)
10. [Phân tích Hiệu năng Đầu - Cuối & Quy tắc Pareto (Ranking Functions)](#10-phân-tích-hiệu-năng-đầu---cuối--quy-tắc-pareto-ranking-functions)
11. [Các Hàm Thống kê & Biểu thức Logic Nghiệp vụ](#11-các-hàm-thống-kê--biểu-thức-logic-nghiệp-vụ)
12. [Bóc tách Kiến trúc Thực thi & Tối ưu hóa SSAS (Engine Internals)](#12-bóc-tách-kiến-trúc-thực-thi--tối-ưu-hóa-ssas-engine-internals)
13. [Bộ Câu hỏi Phản biện & Ôn tập Lý thuyết Thường gặp](#13-bộ-câu-hỏi-phản-biện--ôn-tập-lý-thuyết-thường-gặp)

---

## 1. TỔNG QUAN VỀ NGÔN NGỮ MDX & BỐI CẢNH LỊCH SỬ

### 1.1. MDX là gì?
**MDX (Multidimensional Expressions)** là ngôn ngữ truy vấn mạnh mẽ được Microsoft giới thiệu lần đầu tiên vào năm 1997 như một phần của chuẩn **OLE DB for OLAP** (sau này được chuẩn hóa rộng rãi trên toàn ngành thông qua giao diện XMLA - XML for Analysis).

Khác với SQL (Structured Query Language) được thiết kế để thao tác trên **mô hình dữ liệu quan hệ 2 chiều (Relational Tables - Dòng và Cột)**, MDX được xây dựng chuyên biệt để truy vấn và tính toán trên **khối dữ liệu đa chiều (Multidimensional Cubes / Hypercubes)**.

```
       Mô hình Quan hệ (SQL)                      Mô hình Siêu khối (MDX)
       ┌────────────────────────┐                 ┌────────────────────────┐
       │ Dòng (Rows)            │                 │ Chiều 1: Player        │
       │ x                      │       VS        │ Chiều 2: Club          │
       │ Cột (Columns)          │                 │ Chiều 3: Time          │
       │                        │                 │ Chiều N: Measures,...  │
       └────────────────────────┘                 └────────────────────────┘
```

### 1.2. Vì sao SQL truyền thống thất bại trước bài toán OLAP phức tạp?
Khi phân tích nghiệp vụ quản trị và hỗ trợ ra quyết định (Business Intelligence - BI), các chuyên gia dữ liệu thường xuyên gặp phải các rào cản nghiêm trọng với SQL:
1. **Bùng nổ phép nối (Join Explosion)**: Mỗi góc nhìn phân tích đòi hỏi phải `JOIN` từ 5 đến 10 bảng Fact và Dimension, gây quá tải bộ nhớ và nghẽn I/O đĩa.
2. **Không nhận biết cấu trúc phân cấp (Hierarchy-Blind)**: SQL không có khái niệm gốc về quan hệ cha-con (Year -> Quarter -> Month -> Day). Để tính tăng trưởng so với cùng kỳ năm trước (YoY), SQL buộc phải dùng `LEFT JOIN` chính bảng đó (Self-Join) hoặc hàm cửa sổ `LAG()` phức tạp và chậm chạp.
3. **Thao tác tính toán trên dữ liệu thưa (Data Sparsity)**: Trong khối OLAP thực tế, hơn 95% các tọa độ giao điểm giữa các chiều không có dữ liệu phát sinh (Ví dụ: Một cầu thủ không thể thi đấu cho tất cả CLB trong cùng một ngày). SQL quét toàn bộ không gian bảng, trong khi MDX tự động bỏ qua các ô rỗng (`NON EMPTY`) thông qua chỉ mục Bitmap.

---

## 2. CÁC KHÁI NIỆM CỐT LÕI TRONG MÔ HÌNH ĐA CHIỀU (CORE CONCEPTS)

Để làm chủ MDX, ta cần phân biệt rạch ròi 8 thực thể nền tảng tạo nên cấu trúc siêu khối:

```
[Cube]
  │
  ├── [Dimensions] (Player, Club, Time, Competition, Game)
  │     └── [Hierarchies] (e.g. Time Hierarchy: Year -> Quarter -> Month -> Day)
  │           └── [Levels] (Cấp độ trong cây)
  │                 └── [Members] (Phần tử cụ thể, e.g. [2023], [Erling Haaland])
  │
  ├── [Measures] (Goals, Assists, Minutes Played, Yellow Cards)
  │
  └── [Tuples] & [Sets] ──> Xác định giá trị tại [Cell]
```

### 2.1. Cube (Khối dữ liệu)
Là vùng chứa trung tâm gom nhóm các **Bảng chiều (Dimensions)** và **Độ đo (Measures)** có quan hệ mật thiết với nhau. Trong dự án này, Cube trung tâm là `[DW Football Transfermarkt]`.

### 2.2. Dimension (Chiều dữ liệu)
Đại diện cho góc nhìn phân tích dữ liệu nghiệp vụ (trả lời cho các câu hỏi: Ai? Ở đâu? Khi nào? Cái gì?).
*Ví dụ*:
- `[DIM Player]`: Góc nhìn cầu thủ (Họ tên, Vị trí, Chân thuận, Quốc tịch).
- `[DIM Club]`: Góc nhìn câu lạc bộ (Tên CLB, Huấn luyện viên, Sân vận động, Sức chứa).
- `[DIM Time]`: Góc nhìn thời gian diễn ra trận đấu.

### 2.3. Hierarchy (Cây phân cấp) & Level (Cấp độ)
Một chiều có thể chứa một hoặc nhiều cây phân cấp. Mỗi cây phân cấp bao gồm các **Level** có mối quan hệ phụ thuộc cha - con xác định:
- Cây phân cấp thời gian: `[DIM Time].[Hierarchy].[Year]` $\to$ `[Quarter]` $\to$ `[Month]` $\to$ `[Full Date]`.
- Level cao nhất là `[All]` (chứa giá trị tổng hợp toàn bộ).

### 2.4. Member (Phần tử)
Là một thực thể dữ liệu cụ thể tại một Level trong Hierarchy.
*Ví dụ*:
- `[DIM Time].[Year].[2023]` là một Member của Level `[Year]`.
- `[DIM Player].[Player Name].[Erling Haaland]` là một Member của chiều Cầu thủ.
- `[Measures].[Goals]` cũng là một Member đặc biệt thuộc chiều `[Measures]`.

### 2.5. Measure (Độ đo) & Measure Group
Là các giá trị số học định lượng nằm trong bảng sự kiện (Fact Table) được tổng hợp (Aggregated) qua các hàm như `SUM`, `COUNT`, `DISTINCTCOUNT`, `MIN`, `MAX`.
*Ví dụ*: `[Measures].[Goals]`, `[Measures].[Assists]`, `[Measures].[Minutes Played]`.

### 2.6. Tuple (Bộ tọa độ ô)
Một **Tuple** là một bộ tọa độ xác định duy nhất một lát cắt hoặc một ô dữ liệu trong không gian đa chiều. Một Tuple được đặt trong dấu ngoặc đơn `(...)` và gồm các Member đến từ các chiều **khác nhau** (không bao giờ chứa 2 Member trong cùng một chiều).
*Ví dụ*:
```mdx
([DIM Player].[Player Name].[Erling Haaland], [DIM Time].[Year].[2023], [Measures].[Goals])
```
> *Lưu ý*: Nếu một Tuple chỉ gồm 1 Member duy nhất, ta có thể viết tắt bỏ dấu ngoặc đơn: `[Measures].[Goals]`.

### 2.7. Set (Tập hợp)
Một **Set** là một tập hợp có thứ tự gồm **không, một hoặc nhiều Tuple có cùng cấu trúc không gian** (cùng thứ tự các chiều). Set được đặt trong dấu ngoặc nhọn `{...}`.
*Ví dụ*:
```mdx
{
    ([DIM Player].[Player Name].[Erling Haaland], [Measures].[Goals]),
    ([DIM Player].[Player Name].[Bukayo Saka],    [Measures].[Goals]),
    ([DIM Player].[Player Name].[Mohamed Salah],  [Measures].[Goals])
}
```

### 2.8. Cell (Ô dữ liệu)
Là giao điểm hình học chính xác giữa tất cả các chiều trong Cube (ứng với một Tuple hoàn chỉnh chứa một Measure). Mỗi Cell lưu trữ một giá trị số học tổng hợp.

---

## 3. SO SÁNH CHUYÊN SÂU: SQL (QUAN HỆ) VS MDX (ĐA CHIỀU)

| Tiêu chí so sánh | Ngôn ngữ SQL (Relational) | Ngôn ngữ MDX (Multidimensional) |
| :--- | :--- | :--- |
| **Mô hình dữ liệu cơ sở** | Bảng 2 chiều (Dòng x Cột) | Không gian siêu khối $N$ chiều ($N$-Dimensional Hypercube) |
| **Đơn vị kết quả** | Bảng tập hợp bản ghi (Recordset) | Ma trận đa chiều (Cellset: Columns, Rows, Pages,...) |
| **Số trục hiển thị** | 2 chiều cố định (Hàng dọc và Cột ngang) | Tối đa 128 trục truy vấn (`AXIS(0)`, `AXIS(1)`, `AXIS(2)`,...) |
| **Mệnh đề `WHERE`** | Bộ lọc điều kiện dòng dữ liệu (Row Filter) | **Slicer Axis**: Cắt lát không gian tại một tọa độ xác định |
| **Khả năng hiểu phân cấp** | Không (phải dùng đệ quy CTE hoặc Self-Join) | Tự nhiên (Built-in Navigation: `.Parent`, `.Children`, `.PrevMember`) |
| **Tính toán ô thưa (Sparsity)** | Quét tuần tự toàn bộ dòng dữ liệu | Bỏ qua hoàn toàn các ô rỗng bằng từ khóa `NON EMPTY` |
| **Tiền tính toán (Pre-aggregation)** | Không có sẵn (phải tạo Index/Indexed View) | Tích hợp sẵn trong Storage Engine (MOLAP Cache & Aggregations) |
| **Thao tác xoay chiều (Pivot)** | Rất phức tạp (cần hàm `PIVOT` hoặc `CASE WHEN`) | Tự nhiên bằng cách đặt Set lên các trục `COLUMNS` và `ROWS` |
| **Tốc độ phản hồi phân tích** | Chậm dần theo cấp số nhân khi dữ liệu tăng | Tức thì (thường dưới 1 giây) nhờ cấu trúc khối nén |

### ⚠️ Sai lầm phổ biến nhất của người mới học MDX: Mệnh đề `WHERE`!
- Trong **SQL**: `WHERE Country = 'England'` lọc bỏ các dòng không thỏa mãn trước khi `GROUP BY`.
- Trong **MDX**: Mệnh đề `WHERE` đóng vai trò là **Bộ cắt lát (Slicer Axis)**. Nó ấn định một tọa độ cố định ngầm định cho toàn bộ các ô trong khối mà không làm thay đổi cấu trúc danh sách phần tử hiển thị trên trục `ROWS` hay `COLUMNS`.

---

## 4. CẤU TRÚC CÚ PHÁP CƠ BẢN CỦA MỘT TRUY VẤN MDX

### 4.1. Cú pháp chuẩn tổng quát
```mdx
[WITH 
    MEMBER [Cube_Name].[Dimension].[Member_Name] AS 'Expression' [, FORMAT_STRING = '...']
    SET [Set_Name] AS '{...}'
]
SELECT 
    [NON EMPTY] <Set_Expression_1> ON COLUMNS,  -- hoặc ON AXIS(0)
    [NON EMPTY] <Set_Expression_2> ON ROWS      -- hoặc ON AXIS(1)
FROM [<Cube_Name>]
[WHERE (<Tuple_Slicer_Specification>)]
```

### 4.2. Các trục truy vấn (Axes)
MDX hỗ trợ chuẩn đến 128 trục, tuy nhiên các công cụ hiển thị (như SSMS Grid, Excel PivotTable) thường sử dụng 2 trục trực quan:
- **`COLUMNS`** (hoặc `AXIS(0)`): Xác định các thước đo hoặc thuộc tính xuất hiện trên thanh tiêu đề cột ngang.
- **`ROWS`** (hoặc `AXIS(1)`): Xác định danh sách phần tử xuất hiện ở từng dòng dọc.
- **`PAGES`** (hoặc `AXIS(2)`): Xác định trang báo cáo lật trang.

*Ví dụ cơ bản*:
```mdx
SELECT 
    {[Measures].[Goals], [Measures].[Assists]} ON COLUMNS,
    [DIM Player].[Player Name].Members ON ROWS
FROM [DW Football Transfermarkt]
```

### 4.3. Tối ưu ô thưa với `NON EMPTY`
Trong bóng đá, số lượng cầu thủ đăng ký là hàng chục ngàn người, nhưng trong một giải đấu cụ thể chỉ có một nhóm cầu thủ ghi bàn. Nếu không có `NON EMPTY`, câu truy vấn sẽ trả về hàng chục ngàn dòng với giá trị rỗng (`(null)`), làm tràn bộ nhớ client.
- **Từ khóa `NON EMPTY`**: Đặt trước biểu thức Set trên mỗi trục để loại bỏ toàn bộ hàng hoặc cột hoàn toàn không có dữ liệu.

```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    NON EMPTY [DIM Player].[Player Name].Members ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 5. KHAI BÁO THÀNH VIÊN TÍNH TOÁN & TẬP HỢP ĐẶT TÊN (`WITH` CLAUSE)

Mệnh đề `WITH` cho phép mở rộng khối dữ liệu động trong thời gian chạy (Runtime) mà không cần can thiệp tái cấu trúc Cube trên Visual Studio SSDT.

### 5.1. Thành viên tính toán (`WITH MEMBER`)
Được sử dụng khi cần định nghĩa một chỉ số đo lường mới từ các độ đo có sẵn (Ví dụ: Hiệu suất bàn thắng/kiến tạo, tỷ lệ phần trăm, quy đổi thẻ phạt).

```mdx
WITH 
MEMBER [Measures].[Goal Contributions] AS
    [Measures].[Goals] + [Measures].[Assists],
    FORMAT_STRING = '#,##0'

MEMBER [Measures].[Goals Per Appearance] AS
    IIF([Measures].[FACT Player Match Perf Count] = 0, NULL,
        [Measures].[Goals] / [Measures].[FACT Player Match Perf Count]),
    FORMAT_STRING = '0.00'

SELECT 
    {[Measures].[Goals], [Measures].[Assists], [Measures].[Goal Contributions], [Measures].[Goals Per Appearance]} ON COLUMNS,
    NON EMPTY [DIM Player].[Player Name].Members ON ROWS
FROM [DW Football Transfermarkt]
```

### 5.2. Tập hợp đặt tên (`WITH SET`)
Định nghĩa trước một danh sách tập hợp phức tạp để tái sử dụng nhiều lần trong các trục hoặc trong các phép tính toán con, giúp câu truy vấn ngắn gọn và tối ưu hóa bộ nhớ tạm (Cache).

```mdx
WITH 
SET [Top_Strikers] AS
    TOPCOUNT([DIM Player].[Player Name].Members, 5, [Measures].[Goals])

SELECT 
    {[Measures].[Goals], [Measures].[Assists]} ON COLUMNS,
    [Top_Strikers] ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 6. ĐIỀU HƯỚNG PHÂN CẤP & QUAN HỆ CÂY (HIERARCHICAL NAVIGATION)

Sức mạnh vượt trội nhất của MDX là khả năng "leo trèo" tự do trên cây phân cấp dữ liệu thông qua các hàm điều hướng:

```
                  [All Time]
                      │
                   [2023]  <--- .Parent của Q1
                 /        \
              [Q1]        [Q2]  <--- .Siblings
             /    \
        [Tháng 1]  [Tháng 2]  <--- .Children của Q1
```

### Bảng tra cứu các hàm điều hướng cây phân cấp

| Hàm / Thuộc tính | Cú pháp | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| **`.Members`** | `Level.Members` | Trả về tất cả các phần tử thuộc một cấp độ hoặc chiều. |
| **`.Children`** | `Member.Children` | Lấy tập hợp con trực tiếp cấp dưới của Member hiện tại. |
| **`.Parent`** | `Member.Parent` | Trả về phần tử cha trực tiếp cấp trên. |
| **`.FirstChild` / `.LastChild`** | `Member.FirstChild` | Lấy phần tử con đầu tiên hoặc cuối cùng. |
| **`.Siblings`** | `Member.Siblings` | Lấy danh sách các anh chị em cùng cha (cùng cấp độ). |
| **`Descendants()`** | `Descendants(Member, Level, Flags)` | Lấy toàn bộ con cháu ở các cấp độ sâu bên dưới. |
| **`Ancestors()`** | `Ancestors(Member, Level)` | Lấy danh sách tổ tiên ngược lên cấp trên. |

*Ví dụ: Thống kê bàn thắng của toàn bộ các tháng thuộc năm 2023*:
```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    [DIM Time].[Hierarchy].[Year].[2023].Children ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 7. PHÂN TÍCH CHUỖI THỜI GIAN (TIME SERIES / TIME INTELLIGENCE)

Phân tích xu hướng qua thời gian là "linh hồn" của hệ thống Kho dữ liệu. MDX cung cấp các hàm chuyên biệt để tính toán so sánh kỳ trước (Period-over-Period) và lũy kế đầu kỳ đến ngày (To-Date).

### 7.1. So sánh kỳ trước với `.PrevMember`
Trả về phần tử liền trước cùng cấp độ. Rất hữu ích để tính tăng trưởng theo Quý (Quarter-over-Quarter - QoQ) hoặc theo Tháng (Month-over-Month - MoM).

```mdx
WITH 
MEMBER [Measures].[Prev Quarter Goals] AS
    ([DIM Time].[Hierarchy].CurrentMember.PrevMember, [Measures].[Goals])

MEMBER [Measures].[QoQ Goals Growth] AS
    [Measures].[Goals] - [Measures].[Prev Quarter Goals],
    FORMAT_STRING = '+#,##0;-#,##0;0'

SELECT 
    {[Measures].[Goals], [Measures].[Prev Quarter Goals], [Measures].[QoQ Goals Growth]} ON COLUMNS,
    [DIM Time].[Hierarchy].[Quarter].Members ON ROWS
FROM [DW Football Transfermarkt]
```

### 7.2. So sánh cùng kỳ năm trước với `ParallelPeriod()`
Hàm `ParallelPeriod(Level, Index, Member)` tìm phần tử ở vị trí song song trong kỳ trước (Ví dụ: Tháng 5 năm nay so với Tháng 5 năm ngoái).

```mdx
WITH 
MEMBER [Measures].[Same Month Last Year Goals] AS
    (ParallelPeriod([DIM Time].[Hierarchy].[Year], 1, [DIM Time].[Hierarchy].CurrentMember), [Measures].[Goals])

SELECT 
    {[Measures].[Goals], [Measures].[Same Month Last Year Goals]} ON COLUMNS,
    [DIM Time].[Hierarchy].[Month].Members ON ROWS
FROM [DW Football Transfermarkt]
```

### 7.3. Tính toán lũy kế: `YTD()`, `QTD()`, `MTD()`
- **`YTD()`**: Year-to-Date (Tích lũy từ đầu năm đến thời điểm hiện tại).
- **`QTD()`**: Quarter-to-Date (Tích lũy từ đầu quý).
- **`MTD()`**: Month-to-Date (Tích lũy từ đầu tháng).

```mdx
WITH 
MEMBER [Measures].[YTD Goals] AS
    SUM(YTD([DIM Time].[Hierarchy].CurrentMember), [Measures].[Goals])

SELECT 
    {[Measures].[Goals], [Measures].[YTD Goals]} ON COLUMNS,
    [DIM Time].[Hierarchy].[Month].Members ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 8. ĐẠI SỐ TẬP HỢP & XỬ LÝ KHÔNG GIAN ĐA CHIỀU (SET ALGEBRA)

MDX áp dụng đầy đủ các quy tắc của đại số quan hệ và lý thuyết tập hợp để tạo ra các tổ hợp phân tích đa chiều:

```
   CROSSJOIN (A * B)           UNION (A + B)           INTERSECT (A ∩ B)        EXCEPT (A - B)
   ┌───┬───┐                   ┌───────┐               ┌───────┐                ┌───────┐
   │A1 │B1 │                   │   A   │               │   A   │ ∩ │ B │        │   A   │ \ B
   ├───┼───┤                   ├───────┤               └───────┘                └───────┘
   │A1 │B2 │                   │   B   │
   └───┴───┘                   └───────┘
```

### 8.1. Tích Đề-các: `CROSSJOIN` hoặc toán tử `*`
Kết hợp từng phần tử của tập hợp 1 với mọi phần tử của tập hợp 2 để tạo thành ma trận 2 chiều lồng nhau.
*Ví dụ*: Phân tích bàn thắng theo từng Vị trí thi đấu và Chân thuận:
```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    NON EMPTY [DIM Player].[Main Position].Members * [DIM Player].[Foot].Members ON ROWS
FROM [DW Football Transfermarkt]
```

### 8.2. Phép hợp: `UNION` hoặc toán tử `+`
Gộp hai tập hợp có cùng cấu trúc chiều thành một tập hợp duy nhất.
```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    UNION(
        [DIM Player].[Sub Position].[Left Winger].Members,
        [DIM Player].[Sub Position].[Right Winger].Members
    ) ON ROWS
FROM [DW Football Transfermarkt]
```

### 8.3. Phép giao: `INTERSECT`
Tìm các phần tử xuất hiện đồng thời trong cả hai tập hợp (Ví dụ: Các CLB vừa nằm trong Top ghi bàn Sân nhà, vừa nằm trong Top ghi bàn Sân khách).

### 8.4. Phép trừ: `EXCEPT` hoặc toán tử `-`
Loại bỏ các phần tử của tập hợp 2 ra khỏi tập hợp 1 (Ví dụ: Lấy toàn bộ các giải đấu nhưng loại trừ các giải đấu giao hữu).

---

## 9. LỌC DỮ LIỆU & SẮP XẾP (FILTERING & SORTING)

### 9.1. Lọc điều kiện với `FILTER()`
Hàm `FILTER(Set, Boolean_Expression)` quét từng phần tử trong Set và chỉ giữ lại những phần tử thỏa mãn điều kiện logic.

```mdx
SELECT 
    {[Measures].[Goals], [Measures].[Minutes Played]} ON COLUMNS,
    NON EMPTY FILTER(
        [DIM Player].[Player Name].Members,
        [Measures].[Goals] >= 15 AND [Measures].[Minutes Played] > 1000
    ) ON ROWS
FROM [DW Football Transfermarkt]
```

### 9.2. Sắp xếp với `ORDER()`
Cú pháp: `ORDER(Set, Expression, [ASC | DESC | BASC | BDESC])`.
- **`ASC / DESC` (Hierarchical)**: Sắp xếp dữ liệu nhưng **bảo tồn quan hệ cấp bậc** cha - con (các con chỉ được sắp xếp trong phạm vi cha của nó).
- **`BASC / BDESC` (Break Hierarchy)**: **Phá vỡ hoàn toàn quan hệ thứ bậc**, sắp xếp phẳng toàn bộ tập hợp trên toàn không gian.

```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    ORDER([DIM Player].[Player Name].Members, [Measures].[Goals], BDESC) ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 10. PHÂN TÍCH HIỆU NĂNG ĐẦU - CUỐI & QUY TẮC PARETO (RANKING FUNCTIONS)

### 10.1. `TOPCOUNT()` & `BOTTOMCOUNT()`
Lọc lấy $N$ phần tử có giá trị cao nhất hoặc thấp nhất dựa trên một thước đo.
- **Thuật toán nội tại của SSAS**: SSAS triển khai cấu trúc dữ liệu **Min-Heap (hoặc Max-Heap)** với độ phức tạp thời gian tối ưu $O(N \log k)$, giúp truy vấn hàng triệu dòng cực nhanh mà không cần sắp xếp toàn bộ dữ liệu.

```mdx
-- Lấy Top 10 cầu thủ ghi bàn nhiều nhất
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    TOPCOUNT([DIM Player].[Player Name].Members, 10, [Measures].[Goals]) ON ROWS
FROM [DW Football Transfermarkt]
```

### 10.2. Quy tắc Pareto 80/20 với `TOPPERCENT()` & `BOTTOMPERCENT()`
Lấy danh sách các phần tử có tổng lũy kế đóng góp đạt ngưỡng $P\%$ tổng số toàn thể.
*Ví dụ*: Tìm nhóm các quốc gia đóng góp vào **80% tổng số bàn thắng** của giải đấu:

```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    TOPPERCENT([DIM Player].[Country Name].Members, 80, [Measures].[Goals]) ON ROWS
FROM [DW Football Transfermarkt]
```

### 10.3. Hàm đại số lặp nâng cao: `GENERATE()`
`GENERATE(Set1, Set2_Expression)` tương đương với phép lặp `FOR EACH` hoặc `CROSS APPLY` trong SQL. Nó duyệt qua từng phần tử của `Set1`, áp dụng biểu thức tính toán `Set2` và gom kết quả lại.
*Ứng dụng kinh điển*: **Bài toán Group By Top 1 per Category** (Ví dụ: Tìm cầu thủ ghi nhiều bàn nhất của TỪNG câu lạc bộ):

```mdx
SELECT 
    {[Measures].[Goals]} ON COLUMNS,
    GENERATE(
        [DIM Club].[Club Name].Members,
        TOPCOUNT([DIM Club].[Club Name].CurrentMember * [DIM Player].[Player Name].Members, 1, [Measures].[Goals])
    ) ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 11. CÁC HÀM THỐNG KÊ & BIỂU THỨC LOGIC NGHIỆP VỤ

### 11.1. Các hàm tổng hợp thống kê
- `SUM(Set, [Numeric_Expression])`: Tính tổng.
- `AVG(Set, [Numeric_Expression])`: Tính giá trị trung bình (tự động bỏ qua các ô rỗng).
- `MIN(Set, [Numeric_Expression])` / `MAX(Set, [Numeric_Expression])`: Tìm giá trị cực trị.
- `COUNT(Set, [EXCLUDEEMPTY | INCLUDEEMPTY])`: Đếm số phần tử trong tập hợp.
- `DISTINCTCOUNT(Set)`: Đếm số giá trị phân biệt (loại trừ đếm trùng lặp).

### 11.2. Từ khóa chuyển ngữ cảnh `EXISTING`
Khi viết Calculated Member sử dụng hàm thống kê, từ khóa `EXISTING` ép buộc tập hợp phải được lọc theo ngữ cảnh tọa độ hiện tại của dòng/cột hiển thị thay vì tính trên toàn bộ khối.
```mdx
MEMBER [Measures].[Club Avg Player Goals] AS
    AVG(EXISTING [DIM Player].[Player Name].Members, [Measures].[Goals])
```

### 11.3. Xử lý giá trị NULL với `COALESCEEMPTY()`
Trong bóng đá, có những sân vận động không công bố sức chứa hoặc cầu thủ chưa từng ra sân. Hàm `COALESCEEMPTY(Exp1, Exp2, ...)` sẽ trả về giá trị đầu tiên khác rỗng (tương tự hàm `COALESCE` trong SQL).

### 11.4. Cấu trúc rẽ nhánh: `IIF()` và `CASE WHEN`
Cho phép phân loại phân khúc nghiệp vụ ngay trên trục hiển thị:

```mdx
WITH 
MEMBER [Measures].[Age Category] AS
    CASE 
        WHEN [DIM Player].[Age].CurrentMember.Member_Value < 21 THEN 'U21 - Tiềm năng trẻ'
        WHEN [DIM Player].[Age].CurrentMember.Member_Value <= 29 THEN '22-29 - Đỉnh cao phong độ'
        ELSE '30+ - Lão tướng'
    END

SELECT 
    {[Measures].[Goals], [Measures].[Age Category]} ON COLUMNS,
    NON EMPTY [DIM Player].[Player Name].Members ON ROWS
FROM [DW Football Transfermarkt]
```

---

## 12. BÓC TÁCH KIẾN TRÚC THỰC THI & TỐI ƯU HÓA SSAS (ENGINE INTERNALS)

Hiểu rõ cơ chế hoạt động bên dưới của SSAS sẽ giúp bạn giải trình xuất sắc trước hội đồng về tính tối ưu của các câu truy vấn MDX:

```
┌────────────────────────────────────────────────────────┐
│                   CLIENT (SSMS / Excel)                │
└───────────────────────────┬────────────────────────────┘
                            │ Gửi câu truy vấn MDX
                            ▼
┌────────────────────────────────────────────────────────┐
│             FORMULA ENGINE (FE - Đơn luồng)            │
│  - Phân tích cú pháp (Parser) & Lập cây kế hoạch       │
│  - Tính toán các hàm phức tạp: IIF, CASE, GENERATE     │
│  - Quản lý ngữ cảnh và điều phối kết quả               │
└───────────────────────────┬────────────────────────────┘
                            │ Yêu cầu dữ liệu thô (Subcube Request)
                            ▼
┌────────────────────────────────────────────────────────┐
│            STORAGE ENGINE (SE - Đa luồng)              │
│  - Quét dữ liệu từ MOLAP Cache / Bitmap Index          │
│  - Tổng hợp cực nhanh: SUM, MIN, MAX                   │
│  - Trả về khối con (Subcube) nén cho FE                │
└────────────────────────────────────────────────────────┘
```

### 12.1. Phân định vai trò: Formula Engine (FE) vs Storage Engine (SE)
1. **Formula Engine (FE)**:
   - Chịu trách nhiệm biên dịch cú pháp MDX, đánh giá các biểu thức điều kiện logic phức tạp (`CASE WHEN`, `FILTER`), xử lý chuỗi và định dạng.
   - **Đặc điểm**: Hoạt động **đơn luồng (Single-threaded)**. Nếu một truy vấn đẩy quá nhiều logic tính toán cho FE, hiệu năng sẽ bị thắt nút cổ chai (Bottleneck).
2. **Storage Engine (SE)**:
   - Chịu trách nhiệm truy xuất các ô dữ liệu vật lý từ các phân vùng (Partitions) và Aggregation Cache trên đĩa.
   - **Đặc điểm**: Hoạt động **đa luồng song song (Multi-threaded)**, tốc độ cực cao nhờ giải thuật nén dữ liệu theo cột và Bitmap Indexing.

### 12.2. Chiến lược Tối ưu hóa Truy vấn MDX trong Thực tế
1. **Hạn chế phép lặp từng ô (Cell-by-cell Evaluation)**: Tránh lồng các hàm điều kiện phức tạp bên trong các tập hợp lớn. Hãy tận dụng **Block Computation** (Tính toán theo khối) của SSAS.
2. **Sử dụng `NON EMPTY` đúng chỗ**: Luôn đặt `NON EMPTY` trên trục `ROWS` khi làm việc với các Dimension có độ phân mảnh cao (như Cầu thủ với hàng chục ngàn Member) để loại bỏ sớm các ô rỗng ngay tại tầng Storage Engine.
3. **Ưu tiên `TOPCOUNT` hơn `ORDER` + `FILTER`**: Khi chỉ cần lấy Top phần tử, hàm `TOPCOUNT` sử dụng giải thuật Min-Heap tại tầng SE nhanh hơn hàng chục lần so với việc dùng `ORDER` toàn bộ tập dữ liệu rồi mới cắt bớt.

---

## 13. BỘ CÂU HỎI PHẢN BIỆN & ÔN TẬP LÝ THUYẾT THƯỜNG GẶP

Dưới đây là 10 câu hỏi lý thuyết điển hình mà Giảng viên thường đặt ra khi phản biện đồ án Kho dữ liệu & OLAP:

### Câu 1: Sự khác biệt cơ bản nhất giữa mệnh đề `WHERE` trong SQL và mệnh đề `WHERE` trong MDX là gì?
- **Trả lời**: Trong SQL, `WHERE` là bộ lọc điều kiện trên từng bản ghi (dòng) của bảng trước khi thực hiện nhóm (`GROUP BY`). Trong MDX, `WHERE` đóng vai trò là **Trục cắt lát (Slicer Axis)**; nó không lọc bỏ dòng mà ấn định tọa độ chiều cố định ngầm định cho toàn bộ không gian của khối Cube mà không làm thay đổi danh sách các Member hiển thị trên trục `ROWS` hoặc `COLUMNS`.

### Câu 2: Phân biệt `Tuple` và `Set` trong MDX? Cho ví dụ minh họa trong Cube bóng đá?
- **Trả lời**: 
  - `Tuple` là tọa độ xác định một lát cắt, chứa các Member thuộc các chiều **khác nhau**, đặt trong ngoặc đơn. *Ví dụ*: `([DIM Time].[Year].[2023], [Measures].[Goals])`.
  - `Set` là tập hợp gồm các Tuple có **cùng cấu trúc chiều**, đặt trong ngoặc nhọn. *Ví dụ*: `{([DIM Time].[Year].[2023], [Measures].[Goals]), ([DIM Time].[Year].[2024], [Measures].[Goals])}`.

### Câu 3: Khi nào nên sử dụng `ORDER(..., BDESC)` thay vì `ORDER(..., DESC)`?
- **Trả lời**: `DESC` là sắp xếp bảo toàn phân cấp (Hierarchical Sorting); nó chỉ sắp xếp các phần tử con trong phạm vi từng phần tử cha tương ứng. `BDESC` (Break Hierarchy) là sắp xếp phá vỡ phân cấp; nó bỏ qua hoàn toàn ranh giới cha-con và sắp xếp phẳng toàn bộ các phần tử trên toàn khối dữ liệu từ cao xuống thấp.

### Câu 4: Từ khóa `NON EMPTY` hoạt động như thế nào và tại sao nó lại tối quan trọng trong các hệ thống OLAP?
- **Trả lời**: Trong không gian khối đa chiều, phần lớn các ô dữ liệu là ô rỗng (Sparsity > 95%). `NON EMPTY` hướng dẫn Storage Engine loại bỏ các hàng/cột không chứa bất kỳ dữ liệu sự kiện nào trước khi trả kết quả về cho client, giúp giảm thời gian truyền tải mạng, tiết kiệm dung lượng RAM và tránh treo ứng dụng báo cáo.

### Câu 5: Thành viên tính toán (`WITH MEMBER`) được lưu trữ ở đâu? Trên ổ đĩa hay trong bộ nhớ RAM?
- **Trả lời**: `WITH MEMBER` khai báo trong câu truy vấn MDX chỉ có phạm vi trong phiên truy vấn đó (Query-scoped) và được tính toán động (Calculated on-the-fly) trong bộ nhớ RAM của Formula Engine khi câu truy vấn thực thi; nó hoàn toàn không được lưu trữ vật lý trên ổ cứng của Cube.

### Câu 6: Làm thế nào để giải quyết bài toán "Top 1 phần tử của từng nhóm" (Group-by Top 1) trong MDX?
- **Trả lời**: Sử dụng hàm đại số lặp `GENERATE()`. Hàm này duyệt qua từng Member của chiều nhóm (ví dụ từng CLB), sau đó áp dụng hàm `TOPCOUNT(..., 1, ...)` cho từng Member đó và gộp kết quả lại thành một tập hợp duy nhất.

### Câu 7: Điểm khác biệt giữa hai hàm đo lường `COUNT()` và `DISTINCTCOUNT()` là gì?
- **Trả lời**: `COUNT()` đếm tổng số phần tử (hoặc số lần xuất hiện bản ghi Fact). `DISTINCTCOUNT()` đếm số lượng thực thể phân biệt (ví dụ đếm số lượng cầu thủ duy nhất ra sân, loại bỏ việc một cầu thủ được đếm nhiều lần khi thi đấu nhiều trận).

### Câu 8: Tại sao hàm `TOPPERCENT()` lại được coi là công cụ đắc lực cho phân tích quản trị kinh doanh và thể thao?
- **Trả lời**: `TOPPERCENT` cho phép hiện thực hóa nguyên lý Pareto 80/20. Thay vì ấn định một con số cố định như Top 5 hay Top 10, `TOPPERCENT` tự động co giãn danh sách để tìm nhóm hạt nhân nòng cốt đóng góp phần lớn giá trị (ví dụ: nhóm quốc gia đóng góp 80% số bàn thắng).

### Câu 9: Từ khóa `EXISTING` có vai trò gì trong các biểu thức tính toán thống kê của MDX?
- **Trả lời**: `EXISTING` thực hiện chuyển đổi ngữ cảnh (Context Transition), buộc một tập hợp phải được lọc theo ngữ cảnh tọa độ hiện tại của cell đang được tính toán, thay vì áp dụng trên toàn bộ tập hợp tĩnh của toàn Cube.

### Câu 10: Hai thành phần Formula Engine (FE) và Storage Engine (SE) phối hợp với nhau như thế nào khi người dùng chạy một truy vấn MDX?
- **Trả lời**: Khi nhận truy vấn, FE phân tích cú pháp và xác định các khối con dữ liệu cần thiết. FE gửi yêu cầu (Subcube Request) tới SE. SE quét dữ liệu đa luồng từ bộ nhớ đệm cache hoặc đĩa, thực hiện các phép cộng tổng hợp thô và trả lại khối con cho FE. FE tiếp tục xử lý các phép toán phức tạp (như tính tỷ lệ, hàm điều kiện `CASE WHEN`) rồi định dạng và trả kết quả về cho Client.

---

## TỔNG KẾT

Tài liệu này cung cấp toàn bộ nền tảng lý thuyết vững chắc giúp bạn hiểu sâu sắc bản chất của ngôn ngữ truy vấn đa chiều MDX. Khi kết hợp tài liệu này cùng **[10 câu truy vấn MDX chính thức](../README.md)** và **[Báo cáo kiểm định chất lượng](../checklist.md)**, bạn đã sở hữu trọn bộ tư liệu hoàn chỉnh, chuẩn mực và chuyên nghiệp nhất phục vụ cho bài báo cáo và bảo vệ đồ án Kho dữ liệu & OLAP.
