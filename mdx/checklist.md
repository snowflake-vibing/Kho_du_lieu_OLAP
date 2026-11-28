# BẢNG ĐỐI CHIẾU & KIỂM ĐỊNH CHẤT LƯỢNG 15 CÂU TRUY VẤN MDX
## (MDX Quality Audit, Function Coverage Matrix & Complexity Checklist)

> **Cơ sở dữ liệu SQL Server:** `DW_Football_Transfermarkt` (7.280 trận, 210.747 lượt ra sân, 7.069 cầu thủ, 272 CLB, 13 giải đấu, 488 ngày)  
> **SSAS Database / Cube:** `SSAS_Football_Transfermarkt` / `[DW Football Transfermarkt]` (4 Measure Groups, 9 Cube Dimensions)  
> **Mục tiêu:** Kiểm định toàn diện 15 câu truy vấn MDX chuẩn theo Mục 1.3 Chương 1 ([Bao_cao_OLAP.docx](../bao-cao-olap/Bao_cao_OLAP.docx)) và Chương 3 ([Chuong_3_SSAS.docx](../bao-cao-olap/Chuong_3_SSAS.docx)).

---

## 1. Khung tiêu chuẩn đánh giá 15 câu truy vấn MDX

1. **Đúng cấp độ dữ liệu (Grain Consistency):** Phân tách dứt khoát giữa cấp lượt ra sân (`FACT Player Match Perf`, 210.747 dòng), cấp cầu thủ duy nhất (`FACT Player Distinct`), cấp đội – trận (`FACT Club Match Official`, 14.560 dòng) và cấp trận đấu (`DIM Game`, 7.280 dòng).
2. **Định danh chính xác thực thể trùng tên:** Dùng thuộc tính khóa `[DIM Player].[Player ID]` (`KeyColumns = Player_ID`, `NameColumn = Player_Name`) để không gộp nhầm 51 tên cầu thủ bị trùng trên 108 hồ sơ trong `DIM_Player`.
3. **Xử lý dữ liệu thưa (Sparsity):** Luôn bọc `NONEMPTY()` quanh tập nguồn hoặc tích `CrossJoin` trước khi truyền vào `TOPCOUNT`, `FILTER` hoặc `ORDER` để đẩy bước lọc xuống Storage Engine.
4. **Xử lý NULL & Unknown an toàn:** Loại `[Unknown]` và `Missing` đúng ngữ cảnh (ví dụ `Player Age At Match`, `Club Manager Name`, `Height In Cm`, `Country Of Citizenship`), đồng thời giữ `Unknown` khi câu hỏi cần phản ánh đủ toàn kho (như 8 CLB bổ sung thiếu `Squad_Size` ở Câu 13).
5. **Đồng quy 3 công cụ:** Mọi câu truy vấn đều cho cùng kết quả trên **Cube Browser (SSDT)** (chỉ dùng toán tử có thật trong SSDT như `Equal`, `Not Equal`, `In`, `Custom`), **Excel PivotTable** và **SSMS MDX**.

---

## 2. Hệ thống 7 nhóm hàm & kỹ thuật MDX áp dụng

| Mã nhóm | Tên nhóm | Các hàm / Từ khóa sử dụng trong 15 câu | Vai trò |
| :---: | :--- | :--- | :--- |
| **G1** | **Tập hợp & Tích** | `TOPCOUNT`, `TOPPERCENT`, `CROSSJOIN` (`*`), `EXCEPT` | Cắt Top-N, Pareto 80%, kết hợp đa chiều, loại thành viên `Unknown`/`Missing`. |
| **G2** | **Lọc & Sắp xếp** | `FILTER`, `ORDER` (`BASC`, `BDESC`), `NONEMPTY`, `NON EMPTY` | Lọc ngưỡng số đo, sắp xếp phá vỡ phân cấp, loại bỏ ô thưa ở mức Storage Engine. |
| **G3** | **Điều hướng thành viên** | `.MEMBERS`, `.CURRENTMEMBER` | Duyệt tập lá của thuộc tính, truy cập ngữ cảnh dòng/cột hiện hành. |
| **G4** | **Tổng hợp & Đếm** | `SUM`, `AVG`, `MAX`, `MIN`, `DISTINCTCOUNT`, `COUNT` | Tổng hợp cộng dồn và đếm phân biệt trên từng Measure Group đúng grain. |
| **G5** | **Logic & Kiểu ngày** | `IIF`, `ISEMPTY`, `CDate` | Bảo vệ chia cho 0, loại giá trị rỗng, so sánh ngày sinh chuẩn ISO. |
| **G6** | **Thuộc tính & Giá trị** | `MEMBER_VALUE`, `.NAME` | Lấy giá trị số học (độ tuổi, chiều cao, sức chứa) và tên ngày sinh để so sánh. |
| **G7** | **Tính toán & Ngữ cảnh** | `WITH SET`, `CREATE MEMBER`, `EXISTING`, Subcube `SELECT` | Calculated Measures tự chủ, chuyển đổi ngữ cảnh theo cầu thủ duy nhất. |

---

## 3. Ma trận đối chiếu 15 câu truy vấn MDX

| Câu | Tên tệp | Nghiệp vụ trọng tâm | G1 | G2 | G3 | G4 | G5 | G6 | G7 |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | [query_01.md](query_01.md) | Top 10 ghi bàn GB1 mùa 2023/2024 | `TOPCOUNT` | `NONEMPTY` | `.MEMBERS` | `SUM` | - | - | `Player ID` |
| **02** | [query_02.md](query_02.md) | Top 10 tiền vệ kiến tạo giải VĐQG | `TOPCOUNT` | `NONEMPTY` | `.MEMBERS` | `SUM` | - | - | `Player ID` |
| **03** | [query_03.md](query_03.md) | Cầu thủ có `Goal Contributions > 20` (2023/2024) | - | `FILTER`, `ORDER (BDESC)`, `NONEMPTY` | `.MEMBERS` | `SUM` | - | - | `Goal Contributions` |
| **04** | [query_04.md](query_04.md) | Bàn thắng, kiến tạo, phút TB theo tuổi (2023) | `EXCEPT` | `FILTER`, `ORDER (BASC)`, `NONEMPTY` | `.MEMBERS`, `.CURRENTMEMBER` | `SUM`, `AVG` | `ISEMPTY`, `IIF` | `MEMBER_VALUE` | `WITH SET`, `Avg Minutes Played` |
| **05** | [query_05.md](query_05.md) | Bàn thắng theo `Foot × Sub_Position` | `EXCEPT` | `NON EMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM` | - | - | - |
| **06** | [query_06.md](query_06.md) | Chiều cao TB/Max/Min, bàn thắng, thẻ vàng theo tuyến | `EXCEPT`, `CrossJoin` | `ORDER (BDESC)`, `FILTER`, `NONEMPTY` | `.MEMBERS`, `.CURRENTMEMBER` | `AVG`, `MAX`, `MIN`, `SUM` | - | `MEMBER_VALUE` | `EXISTING`, Calculated Height |
| **07** | [query_07.md](query_07.md) | Bàn thắng theo quốc tịch tại Anh (+ Pareto 80%) | `EXCEPT` (`TOPPERCENT`) | `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM` | `IIF` | - | `Pct Of Country Goals` |
| **08** | [query_08.md](query_08.md) | Top 10 `Goals Per 90` (`Minutes_Played ≥ 900`, 2023/24) | `TOPCOUNT` | `FILTER`, `NONEMPTY` | `.MEMBERS` | `SUM` | `IIF`, `ISEMPTY` | - | `Goals Per 90` |
| **09** | [query_09.md](query_09.md) | Bàn, thẻ vàng & TB/trận Sân nhà vs Khách cuối tuần | `CrossJoin`, `EXCEPT` | `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM`, `COUNT` | `IIF`, `ISEMPTY` | - | `EXISTING`, `Covered Match Count`, `Goals/Yellow Per Match` |
| **10** | [query_10.md](query_10.md) | Bàn chính thức Real Madrid (`418`, 216 bàn) theo quý & đối thủ | `CrossJoin`, `EXCEPT` | `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM`, `COUNT` | - | - | `FACT Club Match Official`, Role-Play, `Year Quarter Key` |
| **11** | [query_11.md](query_11.md) | Đếm trận sân nhà của CLB sân `> 60.000` chỗ | `CrossJoin`, `EXCEPT` | `FILTER`, `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS`, `.CURRENTMEMBER` | `COUNT`, `MAX` | `ISEMPTY`, `IIF` | `MEMBER_VALUE` | `EXISTING`, `DIM Home Club` |
| **12** | [query_12.md](query_12.md) | Thẻ phạt & TB/trận theo `Club × Manager × Year_Month_Key` | `CrossJoin`, `EXCEPT` | `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM`, `COUNT` | `IIF`, `ISEMPTY` | - | `WITH SET`, `EXISTING`, `Covered Match Count`, `Year Month Key` |
| **13** | [query_13.md](query_13.md) | Lượt ra sân & số cầu thủ theo `Club × Squad_Size` | `CrossJoin`, `EXCEPT` | `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `COUNT`, `DISTINCTCOUNT` | - | - | `FACT Player Distinct` |
| **14** | [query_14.md](query_14.md) | Trận đấu có tổng bàn thắng `≥ 5` qua vòng & SVĐ | `*`, `EXCEPT` | `FILTER`, `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS` | `SUM`, `COUNT` | - | - | `DIM Game` MG, Role-Play 2 đội |
| **15** | [query_15.md](query_15.md) | Bàn thắng & thẻ phạt cầu thủ sinh từ `01/01/2004` theo ngày | `EXCEPT` | `FILTER`, `NONEMPTY`, `ORDER (BDESC)` | `.MEMBERS`, `.CURRENTMEMBER` | `SUM` | `CDate` | `.NAME` | `WITH SET`, Subcube `SELECT` |

---

## 4. Kiểm định độ phức tạp theo quy mô kho dữ liệu thực tế

Quy mô kho dữ liệu đã nạp từ Chương 2: `7.069` cầu thủ, `272` CLB, `13` giải đấu, `2` mùa (`2022`, `2023`), `488` ngày thi đấu, `7.280` trận đấu, `210.747` lượt ra sân.

| Query | Không gian lý thuyết (Cells) | Không gian thực tế sau lọc ($M$) | Bộ nhớ kết quả | Độ phức tạp thời gian | Động cơ SSAS tối ưu |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **Q01** | $7.069 \times 13 \times 2 \approx 1,84 \times 10^5$ | $M \approx 260$ cầu thủ ghi bàn ở GB1 2023 | $O(10)$ | $O(M \log 10)$ | SE Bitmap Slice + FE Min-Heap |
| **Q02** | $2.091 \times 3 = 6.273$ | Tiền vệ có kiến tạo ở VĐQG | $O(10)$ | $O(M \log 10)$ | SE Slice + FE Min-Heap |
| **Q03** | $7.069 \times 2 = 14.138$ | $M = 99$ cầu thủ đạt `G+A > 20` | $O(99)$ | $O(N_{2023} + M \log M)$ | SE Agg + FE Filter & IntroSort |
| **Q04** | $\sim 30 \times 3 = 90$ | $M = 28$ độ tuổi (15–42) năm 2023 | $O(28)$ | $O(M \log M)$ | SE Group-by + FE `Avg Minutes Played` |
| **Q05** | $13 \times 3 = 39$ | 13 vị trí chi tiết × 3 chân thuận | $O(39)$ | $O(13 \log 13)$ | SE Pre-aggregation |
| **Q06** | $4 \times 7.069 = 28.276$ | 4 tuyến chính (loại `Missing`) | $O(4)$ | $O(N_{\text{players}})$ | FE `EXISTING` Context Transition |
| **Q07** | $\sim 140 \times 13$ | $M = 75$ quốc tịch tại Anh (Pareto 80% = 18) | $O(75)$ | $O(M \log M)$ | SE Slice + FE `ORDER` / `TOPPERCENT` |
| **Q08** | $4.832$ cầu thủ mùa 2023 | $M = 2.960$ cầu thủ $\ge 900$ phút | $O(10)$ | $O(N_{2023} + M \log 10)$ | FE Filter + Min-Heap (`Goals Per 90`) |
| **Q09** | $272 \times 2 \times 5 = 2.720$ cells | $M = 207$ CLB ra sân cuối tuần | $O(10M)$ | $O(M \log M)$ | SE Slice (`Is_Weekend=1`) + `Covered Match Count` (`EXISTING`) |
| **Q10** | $8 \text{ quý} \times 272 \text{ đối thủ} = 2.176$ | $M = 92$ cặp quý – đối thủ (101 trận, 216 bàn) | $O(92)$ | $O(M \log M)$ | `FACT Club Match Official` + SE Slice |
| **Q11** | $272$ CLB sân nhà | $M = 23$ CLB sân $> 60.000$ chỗ (993 trận) | $O(23)$ | $O(N_{\text{clubs}} + M \log M)$ | `DIM Game` MG + Role-Play `DIM Home Club` |
| **Q12** | $272 \times 490 \times 23 \approx 3,07 \times 10^6$ | $M = 3.967$ tổ hợp (loại 2 trận thiếu HLV) | $O(M)$ | $O(M \log M)$ | `NONEMPTY` + `Covered Match Count` (`EXISTING`) |
| **Q13** | $272 \times 30 \approx 8.160$ | $M = 235$ CLB có lượt ra sân | $O(235)$ | $O(M \log M)$ | `FACT Player Distinct` Bitmap Scan |
| **Q14** | $7.280 \text{ trận} \times \text{các chiều}$ | $M = 1.196$ trận $\ge 5$ bàn (582/614 mùa) | $O(M)$ | $O(N_{\text{games}} + M \log M)$ | `FILTER` trước `*`, bọc `NONEMPTY` |
| **Q15** | $7.069 \times 488 \approx 3,45 \times 10^6$ | $M = 441$ ngày (676 cầu thủ trẻ) | $O(441)$ | $O(D_{\text{dob}} + M \log M)$ | Subcube Filter + `NONEMPTY` |

---

## 5. Câu hỏi phản biện trọng tâm theo thiết kế mới

1. **Tại sao phải tách 4 Measure Groups (`FACT Player Match Perf`, `FACT Player Distinct`, `FACT Club Match Official`, `DIM Game`)?**
   - Vì một trận đấu có ~29 lượt ra sân và có thể có bàn phản lưới nhà của đối phương. Nếu đếm số trận (`Official Match Count` — Câu 11, 14) hoặc cộng tỷ số chính thức của Real Madrid (`Official Team Goals` — Câu 10: 216 bàn vs 210 bàn cá nhân) trực tiếp trên `FACT_Player_Match_Perf` sẽ bị nhân bản hoặc thiếu bàn phản lưới. Riêng `Distinct Player Count` (Câu 13) bắt buộc tách Measure Group riêng theo quy tắc của SSAS Multidimensional.
2. **Tại sao dùng `[DIM Player].[Player ID]` làm trục truy vấn thay vì `[Player Name]`?**
   - Trong 7.069 cầu thủ có **51 tên bị trùng trên 108 hồ sơ**. Đặt `KeyColumns = Player_ID` và `NameColumn = Player_Name` trên thuộc tính `Player ID` giúp báo cáo hiển thị tên dễ đọc mà vẫn bảo toàn định danh duy nhất (ví dụ Câu 3 giữ đúng 99 cầu thủ thay vì bị gộp nhầm thành 101).
3. **Tại sao `Quarter`, `Month` trong `DIM_Time` và `Round` trong `DIM_Game` phải dùng khóa ghép?**
   - Dữ liệu trải từ 2022–2024 nên `Quarter = 1` hay `Month = 10` lặp qua nhiều năm, và có **55 tên vòng đấu** (`1. Matchday`, `Final`…) lặp ở cả 2 mùa 2022 và 2023. Tạo `Year_Quarter_Key` (`[Year] * 10 + [Quarter]`) và `Year_Month_Key` (`[Year] * 100 + [Month]`) qua **Named Calculations trong DSV trên bảng `DIM_Time`**, kết hợp `(Season, Round)` làm `KeyColumns`, giúp phân cấp `Calendar Hierarchy` và `Season Round Hierarchy` không bị gộp nhầm giữa các năm/mùa.
4. **Tại sao tính `Avg Height Cm` (Câu 6) phải dùng `EXISTING CrossJoin([Player ID], [Height In Cm])`?**
   - Để đảm bảo chiều cao trung bình được tính trên **mỗi cầu thủ duy nhất có chiều cao hợp lệ** trong ngữ cảnh vị trí hiện hành (tránh bị trọng số hóa theo số lần ra sân của từng cầu thủ) và tự động bỏ qua `Unknown`/NULL.
