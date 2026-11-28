# HƯỚNG DẪN SSAS - PHẦN 3: XÂY DỰNG CUBE & CALCULATED MEASURES

---

## 1. MỤC TIÊU

Khởi tạo OLAP Cube **`DW Football Transfermarkt`** tách bạch **4 Measure Groups** theo đúng cấp độ dữ liệu (Grain) của Chương 1, định nghĩa **13 Base Measures** và khai báo bộ **Calculated Measures** tự chủ bằng MDX trong tab **Calculations**.

---

## 2. BƯỚC 1: KHỞI TẠO CUBE `DW Football Transfermarkt`

1. Trong Solution Explorer, bấm chuột phải vào **Cubes** $\rightarrow$ chọn **New Cube...** $\rightarrow$ **Next >**.
2. Chọn **Use existing tables** $\rightarrow$ **Next >**.
3. Tại màn hình **Select Measure Group Tables**, tích chọn đồng thời 3 bảng chứa độ đo:
   - `FACT_Player_Match_Perf` (cấp lượt ra sân — 210.747 dòng)
   - `FACT_Club_Match_Official` (cấp đội – trận — 14.560 dòng)
   - `DIM_Game` (cấp trận đấu — 7.280 dòng)
4. Tại màn hình **Select Measures**: chỉ tích giữ các độ đo nghiệp vụ hợp lệ (bỏ các cột khóa ngoại, cờ `Is_Home_Game`, `Player_Age_At_Match`, `Season`).
5. Tại màn hình **Select Existing Dimensions**: tích chọn đầy đủ 6 Dimensions đã tạo (`DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Player`, `DIM_Time`, `DIM_Appearance_Context`).
6. Đặt tên Cube là **`DW Football Transfermarkt`** $\rightarrow$ nhấn **Finish**.

### Tạo Measure Group thứ 4 cho Distinct Count (`FACT Player Distinct`)
Theo quy chuẩn SSAS Multidimensional, phép đếm phân biệt (`DistinctCount`) bắt buộc nằm trên một Measure Group riêng biệt để phục vụ Câu 13 (đếm số cầu thủ duy nhất ra sân theo CLB):
1. Trong tab **Cube Structure**, bấm chuột phải vào vùng Measures $\rightarrow$ chọn **New Measure...**.
2. Chọn **Usage** = `Distinct count`, **Source table** = `FACT_Player_Match_Perf`, **Source column** = `Player_ID`.
3. SSAS tự sinh Measure Group **`FACT Player Distinct`**; đặt tên độ đo là **`Distinct Player Count`**, `FormatString = #,##0`.

---

## 3. BƯỚC 2: DANH MỤC 13 BASE MEASURES THUỘC 4 MEASURE GROUPS

| Measure Group | Bảng nguồn (DSV) | Tên độ đo (Measure) | Hàm tổng hợp | Format String | Cấp độ (Grain) |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Minutes Played` | `Sum` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Goals` | `Sum` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Assists` | `Sum` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Yellow Cards` | `Sum` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Red Cards` | `Sum` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Match Perf` | `FACT_Player_Match_Perf` | `Appearance Count` | `Count` | `#,##0` | Lượt ra sân (210.747) |
| `FACT Player Distinct` | `FACT_Player_Match_Perf` | `Distinct Player Count` | `DistinctCount` | `#,##0` | Cầu thủ duy nhất |
| `FACT Club Match Official` | `FACT_Club_Match_Official` | `Official Team Goals` | `Sum` | `#,##0` | Đội – Trận (14.560) |
| `FACT Club Match Official` | `FACT_Club_Match_Official` | `Official Team Match Count` | `Count` | `#,##0` | Đội – Trận (14.560) |
| `DIM Game` | `DIM_Game` | `Official Match Count` | `Count` | `#,##0` | Trận đấu (7.280) |
| `DIM Game` | `DIM_Game` | `Home Club Goals` | `Sum` | `#,##0` | Trận đấu (7.280) |
| `DIM Game` | `DIM_Game` | `Away Club Goals` | `Sum` | `#,##0` | Trận đấu (7.280) |
| `DIM Game` | `DIM_Game` | `Total Match Goals` | `Sum` | `#,##0` | Trận đấu (7.280) |

Đặt `NullProcessing = Preserve` cho các độ đo gốc kiểu `Sum` để không nhầm giá trị thiếu với số 0.

---

## 4. BƯỚC 3: ĐỊNH NGHĨA CALCULATED MEASURES TRONG TAB `Calculations`

Mọi Calculated Measure đều viết độc lập từ Base Measures gốc (không tạo dây chuyền phụ thuộc chéo dễ gãy) và bảo vệ phép chia cho 0 bằng `IIF`:

```mdx
// 1. Tổng đóng góp bàn thắng (Câu 3)
CREATE MEMBER CURRENTCUBE.[Measures].[Goal Contributions] AS
    [Measures].[Goals] + [Measures].[Assists],
    FORMAT_STRING = "#,##0",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 2. Thời lượng thi đấu trung bình mỗi lượt ra sân (Câu 4)
CREATE MEMBER CURRENTCUBE.[Measures].[Avg Minutes Played] AS
    IIF(
        ISEMPTY([Measures].[Appearance Count])
        OR [Measures].[Appearance Count] = 0,
        NULL,
        [Measures].[Minutes Played] / [Measures].[Appearance Count]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 3. Số bàn thắng trên 90 phút (Câu 8 mới)
CREATE MEMBER CURRENTCUBE.[Measures].[Goals Per 90] AS
    IIF(
        ISEMPTY([Measures].[Minutes Played])
        OR [Measures].[Minutes Played] = 0,
        NULL,
        ([Measures].[Goals] * 90.0) / [Measures].[Minutes Played]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 4. Đóng góp bàn thắng trên 90 phút (phân tích bổ trợ)
CREATE MEMBER CURRENTCUBE.[Measures].[Goal Contributions Per 90] AS
    IIF(
        ISEMPTY([Measures].[Minutes Played])
        OR [Measures].[Minutes Played] = 0,
        NULL,
        (([Measures].[Goals] + [Measures].[Assists]) * 90.0)
            / [Measures].[Minutes Played]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 5. Thống kê chiều cao trên tập cầu thủ duy nhất hợp lệ (Câu 6)
CREATE MEMBER CURRENTCUBE.[Measures].[Avg Height Cm] AS
    AVG(
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player ID].[Player ID].MEMBERS,
                FILTER(
                    EXCEPT(
                        [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                        { [DIM Player].[Height In Cm].[Unknown] }
                    ),
                    [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE > 0
                )
            ),
            [Measures].[Appearance Count]
        ),
        [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

CREATE MEMBER CURRENTCUBE.[Measures].[Max Height Cm] AS
    MAX(
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player ID].[Player ID].MEMBERS,
                FILTER(
                    EXCEPT(
                        [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                        { [DIM Player].[Height In Cm].[Unknown] }
                    ),
                    [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE > 0
                )
            ),
            [Measures].[Appearance Count]
        ),
        [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
    ),
    FORMAT_STRING = "#,##0",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

CREATE MEMBER CURRENTCUBE.[Measures].[Min Height Cm] AS
    MIN(
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player ID].[Player ID].MEMBERS,
                FILTER(
                    EXCEPT(
                        [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                        { [DIM Player].[Height In Cm].[Unknown] }
                    ),
                    [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE > 0
                )
            ),
            [Measures].[Appearance Count]
        ),
        [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
    ),
    FORMAT_STRING = "#,##0",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 6. Tỷ lệ phần trăm bàn thắng theo quốc tịch (Câu 7 - Pareto)
CREATE MEMBER CURRENTCUBE.[Measures].[Pct Of Country Goals] AS
    IIF(
        ([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All]) = 0,
        NULL,
        [Measures].[Goals]
            / ([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All])
    ),
    FORMAT_STRING = "0.00%",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

// 7. Sức chứa sân nhà dạng số học cho bảng CLB chủ nhà (Câu 11)
CREATE MEMBER CURRENTCUBE.[Measures].[Stadium Seats Value] AS
    IIF(
        ISEMPTY([Measures].[Official Match Count]),
        NULL,
        MAX(
            EXISTING EXCEPT(
                [DIM Home Club].[Stadium Seats].[Stadium Seats].MEMBERS,
                { [DIM Home Club].[Stadium Seats].[Unknown] }
            ),
            [DIM Home Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE
        )
    ),
    FORMAT_STRING = "#,##0",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'DIM Game';

// Trận có lượt ra sân trong ngữ cảnh CLB, sân và HLV hiện hành.
CREATE MEMBER CURRENTCUBE.[Measures].[Covered Match Count] AS
    COUNT(
        NONEMPTY(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS,
            [Measures].[Appearance Count]
        )
    ),
    FORMAT_STRING = "#,##0",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

CREATE MEMBER CURRENTCUBE.[Measures].[Goals Per Match] AS
    IIF(
        [Measures].[Covered Match Count] = 0,
        NULL,
        [Measures].[Goals] / [Measures].[Covered Match Count]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

CREATE MEMBER CURRENTCUBE.[Measures].[Yellow Cards Per Match] AS
    IIF(
        [Measures].[Covered Match Count] = 0,
        NULL,
        [Measures].[Yellow Cards] / [Measures].[Covered Match Count]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';

CREATE MEMBER CURRENTCUBE.[Measures].[Red Cards Per Match] AS
    IIF(
        [Measures].[Covered Match Count] = 0,
        NULL,
        [Measures].[Red Cards] / [Measures].[Covered Match Count]
    ),
    FORMAT_STRING = "#,##0.00",
    VISIBLE = 1,
    ASSOCIATED_MEASURE_GROUP = 'FACT Player Match Perf';
```

---

## 5. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Cube `DW Football Transfermarkt` có đủ 4 Measure Groups và 13 Base Measures khớp hoàn toàn Chương 1 & Chương 3.
- [x] Toàn bộ Calculated Measures bám sát 15 câu truy vấn mới của Chương 1 (bao gồm `Goals Per 90`, `Goal Contributions`, `Avg Minutes Played`, chiều cao trên cầu thủ duy nhất, tỷ trọng quốc tịch và sức chứa sân).
- [x] Tất cả Calculated Measures viết tự chủ, xử lý đúng `NULL`, `Unknown` và chia cho 0.
