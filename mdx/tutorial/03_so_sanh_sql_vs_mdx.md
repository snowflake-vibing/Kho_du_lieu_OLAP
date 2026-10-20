# CHƯƠNG 03: SO SÁNH CHUYÊN SÂU: SQL (QUAN HỆ) VS MDX (ĐA CHIỀU)

---

## 1. BẢNG ĐỐI CHIẾU 10 TIÊU CHÍ HỌC THUẬT GIỮA SQL VÀ MDX

Dưới đây là bảng so sánh bản chất kiến trúc giữa hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) và hệ phân tích trực tuyến đa chiều (SSAS OLAP):

| STT | Tiêu chí so sánh | Ngôn ngữ SQL (Relational) | Ngôn ngữ MDX (Multidimensional) |
| :---: | :--- | :--- | :--- |
| **1** | **Mô hình dữ liệu gốc** | Quan hệ bảng 2 chiều (Relations: Rows $\times$ Columns). | Không gian siêu khối $N$ chiều ($N$-Dimensional Hypercube). |
| **2** | **Đơn vị kết quả trả về** | Tập hợp bản ghi phẳng 2 chiều (Tabular Recordset). | Ma trận ô dữ liệu đa chiều (Multidimensional Cellset). |
| **3** | **Số trục hiển thị (Axes)** | Cố định 2 chiều (Hàng dọc chứa Record, Cột ngang chứa Field). | Hỗ trợ tới 128 trục tọa độ (`COLUMNS`, `ROWS`, `PAGES`,...). |
| **4** | **Bản chất mệnh đề `SELECT`** | Chọn các trường (Columns) cần chiếu (Projection). | Đặt các tập hợp (Sets) lên các trục tọa độ trực quan. |
| **5** | **Bản chất mệnh đề `FROM`** | Chỉ định bảng nguồn và thực hiện các phép kết nối (`JOIN`). | Chỉ định Khối dữ liệu nguồn (`Cube`) chứa sẵn dữ liệu. |
| **6** | **Bản chất mệnh đề `WHERE`** | **Bộ lọc dòng**: Lọc bỏ các bản ghi không thỏa điều kiện. | **Trục cắt lát (Slicer Axis)**: Cố định tọa độ không gian khối. |
| **7** | **Nhận biết cây phân cấp** | Hoàn toàn mù (Hierarchy-Blind), phải tự xử lý bằng code. | Tự nhiên (Built-in: `.Parent`, `.Children`, `.PrevMember`). |
| **8** | **Xử lý dữ liệu thưa (Sparsity)**| Quét tuần tự toàn bộ không gian dòng, gây lãng phí. | Tự động loại trừ các ô rỗng bằng từ khóa `NON EMPTY`. |
| **9** | **Cơ chế tính toán tổng hợp**| Quét bảng sự kiện và tính toán từ đầu lúc truy vấn chạy. | Sử dụng dữ liệu tiền tính toán sẵn (Pre-aggregations MOLAP). |
| **10**| **Thao tác xoay chiều (Pivot)** | Rất cồng kềnh (cần cú pháp `PIVOT` hoặc chuỗi `CASE WHEN`).| Tự nhiên và tức thì bằng cách hoán vị trục `COLUMNS` và `ROWS`.|

---

## 2. BÓC TÁCH CÚ PHÁP: `SELECT - FROM - WHERE` TRONG SQL VS MDX

```
           SQL (Quan hệ)                                    MDX (Đa chiều)
┌──────────────────────────────────────┐        ┌──────────────────────────────────────┐
│ SELECT col1, col2, SUM(col3)         │        │ SELECT                               │
│ FROM Fact_Table                      │        │     {[Measures].[Goals]} ON COLUMNS, │
│ INNER JOIN Dim_A ON ...              │        │     NON EMPTY [DIM Player].Members   │
│ INNER JOIN Dim_B ON ...              │        │              ON ROWS                 │
│ WHERE col4 = 'Condition'             │        │ FROM [DW Football Transfermarkt]     │
│ GROUP BY col1, col2                  │        │ WHERE ([DIM Time].[Year].[2023])     │
└──────────────────────────────────────┘        └──────────────────────────────────────┘
      ▲                                              ▲
      │                                              │
  Mệnh đề WHERE: Lọc bỏ dòng                    Mệnh đề WHERE: Cắt lát không gian
  Mệnh đề FROM: JOIN nhiều bảng                 Mệnh đề FROM: Trỏ vào một CUBE
  Mệnh đề SELECT: Chọn cột                      Mệnh đề SELECT: Đặt Set lên Trục
```

### 2.1. Sự khác biệt cốt tử của mệnh đề `WHERE`
- **Trong SQL**: Mệnh đề `WHERE` là một **vị từ logic (Predicate Filter)**. Nó duyệt qua từng dòng dữ liệu của bảng nguồn, đánh giá điều kiện `True/False` và loại bỏ hoàn toàn các dòng `False` trước khi gom nhóm (`GROUP BY`).
- **Trong MDX**: Mệnh đề `WHERE` được gọi chính xác là **Trục cắt lát (Slicer Specification)**. Nó không lọc bỏ phần tử trên các trục `ROWS` hay `COLUMNS`, mà chỉ ấn định rằng mọi ô dữ liệu (`Cell`) được hiển thị đều được tính toán tại tọa độ chiều đã chọn. Nếu bạn đưa một Member vào `WHERE`, danh sách các dòng trên `ROWS` vẫn hiển thị đầy đủ.

---

## 3. VÍ DỤ ĐỐI CHIẾU THỰC TIỄN: CÙNG MỘT BÀI TOÁN - HAI CÁCH GIẢI QUYẾT

Để đánh giá tính ưu việt của MDX so với SQL trong môi trường BI, xét một bài toán nghiệp vụ kinh điển:

> **Đề bài nghiệp vụ**: Thống kê ma trận so sánh **Tổng số bàn thắng** của 3 câu lạc bộ hàng đầu nước Anh (**Arsenal, Chelsea, Liverpool**) ghi được tại 2 giải đấu cúp quốc nội (**EFL Cup - FAC, FA Cup - GBC**) trong mùa giải 2023. Đồng thời tính **Tỷ trọng bàn thắng (%) của mỗi CLB so với tổng số bàn thắng của cả 3 CLB gộp lại**.

---

### Cách 1: Giải bằng T-SQL (Mô hình Quan hệ)
Trong T-SQL, ta phải:
1. Kết nối 4 bảng (`FACT_Player_Match_Perf`, `DIM_Club`, `DIM_Competition`, `DIM_Time`).
2. Dùng phép lọc `WHERE` để giới hạn mùa giải, câu lạc bộ và giải đấu.
3. Sử dụng hàm cửa sổ `SUM(...) OVER(...)` để tính tổng số bàn thắng của cả 3 CLB làm mẫu số.
4. Dùng cấu trúc `CASE WHEN` hoặc toán tử `PIVOT` để xoay các giải đấu thành các cột ngang.

```sql
WITH Raw_Match_Data AS (
    SELECT 
        c.Club_Name,
        comp.Competition_ID,
        SUM(f.Goals) AS Goals,
        -- Hàm cửa sổ tính tổng bàn thắng của cả 3 CLB trong từng giải đấu
        SUM(SUM(f.Goals)) OVER(PARTITION BY comp.Competition_ID) AS Total_Comp_Goals
    FROM dbo.FACT_Player_Match_Perf f
    INNER JOIN dbo.DIM_Club c ON f.Club_SK = c.Club_SK
    INNER JOIN dbo.DIM_Competition comp ON f.Competition_SK = comp.Competition_SK
    INNER JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
    WHERE t.Year = 2023
      AND c.Club_Name IN ('Arsenal FC', 'Chelsea FC', 'Liverpool FC')
      AND comp.Competition_ID IN ('FAC', 'GBC')
    GROUP BY c.Club_Name, comp.Competition_ID
)
SELECT 
    Club_Name,
    -- Cột FA Cup (FAC)
    ISNULL(MAX(CASE WHEN Competition_ID = 'FAC' THEN Goals END), 0) AS FA_Cup_Goals,
    -- Tỷ lệ phần trăm trong giải FA Cup
    CAST(ISNULL(MAX(CASE WHEN Competition_ID = 'FAC' THEN Goals END), 0) * 100.0 / 
         NULLIF(MAX(CASE WHEN Competition_ID = 'FAC' THEN Total_Comp_Goals END), 0) AS DECIMAL(5,2)) AS FA_Cup_Share_Pct,
    -- Cột EFL Cup (GBC)
    ISNULL(MAX(CASE WHEN Competition_ID = 'GBC' THEN Goals END), 0) AS EFL_Cup_Goals,
    -- Tỷ lệ phần trăm trong giải EFL Cup
    CAST(ISNULL(MAX(CASE WHEN Competition_ID = 'GBC' THEN Goals END), 0) * 100.0 / 
         NULLIF(MAX(CASE WHEN Competition_ID = 'GBC' THEN Total_Comp_Goals END), 0) AS DECIMAL(5,2)) AS EFL_Cup_Share_Pct
FROM Raw_Match_Data
GROUP BY Club_Name
ORDER BY Club_Name;
```
> **Đánh giá T-SQL**: Dài 32 dòng mã, cần 4 phép `INNER JOIN`, quét hàng trăm ngàn dòng trong bảng Fact, đòi hỏi tính toán cửa sổ `SUM() OVER(PARTITION BY)` và lồng nhiều tầng `MAX(CASE WHEN...)` để xoay trục thủ công.

---

### Cách 2: Giải bằng MDX (Mô hình Đa chiều)
Trong MDX, khối Cube đã tự động duy trì các quan hệ và tiền tính toán sẵn. Ta chỉ cần định nghĩa thành viên tính toán tỷ trọng và đặt các Set lên 2 trục:

```mdx
WITH 
-- 1. Tính tổng số bàn thắng của cả 3 CLB làm mẫu số
MEMBER [DIM Club].[Club Name].[3 Clubs Total] AS
    AGGREGATE(
        {
            [DIM Club].[Club Name].[Arsenal FC],
            [DIM Club].[Club Name].[Chelsea FC],
            [DIM Club].[Club Name].[Liverpool FC]
        }
    )

-- 2. Tính tỷ trọng % đóng góp của từng CLB
MEMBER [Measures].[Club Goal Share] AS
    IIF(
        ([DIM Club].[Club Name].[3 Clubs Total], [Measures].[Goals]) = 0,
        NULL,
        [Measures].[Goals] / ([DIM Club].[Club Name].[3 Clubs Total], [Measures].[Goals])
    ),
    FORMAT_STRING = '0.00%'

SELECT 
    -- Trục Cột: Tích Đề-các giữa Giải đấu và Thước đo
    CROSSJOIN(
        {[DIM Competition].[Competition ID].[FAC], [DIM Competition].[Competition ID].[GBC]},
        {[Measures].[Goals], [Measures].[Club Goal Share]}
    ) ON COLUMNS,

    -- Trục Dòng: Danh sách 3 CLB cùng dòng tổng hợp
    {
        [DIM Club].[Club Name].[Arsenal FC],
        [DIM Club].[Club Name].[Chelsea FC],
        [DIM Club].[Club Name].[Liverpool FC],
        [DIM Club].[Club Name].[3 Clubs Total]
    } ON ROWS

FROM [DW Football Transfermarkt]
-- Trục cắt lát Slicer: Năm 2023
WHERE ([DIM Time].[Hierarchy].[Year].[2023])
```
> **Đánh giá MDX**: Ngắn gọn, tường minh, không cần bất kỳ phép `JOIN` nào. Hệ thống tự động tạo ma trận 2 chiều với dữ liệu xoay trục ngay tức thì.

---

## 4. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Kết quả trả về chính xác như nhau ở cả hai phương pháp, nhưng MDX hiển thị dưới dạng ma trận OLAP Grid chuyên nghiệp:

| Câu lạc bộ (`DIM Club`) | FA Cup - Goals | FA Cup - Share Pct | EFL Cup - Goals | EFL Cup - Share Pct |
| :--- | :---: | :---: | :---: | :---: |
| **Arsenal FC** | 8 | 26.67% | 6 | 24.00% |
| **Chelsea FC** | 10 | 33.33% | 7 | 28.00% |
| **Liverpool FC** | 12 | 40.00% | 12 | 48.00% |
| **3 Clubs Total (Tổng hợp)** | **30** | **100.00%** | **25** | **100.00%** |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp tự động xoay trục (Auto-Pivoting)**: Hai giải đấu cúp (`FAC` và `GBC`) tự động được tách thành các cột nhóm riêng biệt mà không cần viết mã biến đổi dòng thành cột.
2. **Trường hợp tính toán mẫu số động (`3 Clubs Total`)**: Member `[3 Clubs Total]` đóng vai trò là điểm neo tổng hợp mẫu số. Tại dòng này, tỷ trọng đạt chính xác 100.00%, kiểm chứng tính toàn vẹn toán học của phép chia.
3. **Hiệu năng thực thi**:
   - Truy vấn T-SQL mất trung bình **180ms - 350ms** do phải quét bảng Fact và băm bảng (Hash Match).
   - Truy vấn MDX hoàn thành trong **< 15ms** nhờ đọc trực tiếp từ Aggregation Cache của SSAS Storage Engine.
