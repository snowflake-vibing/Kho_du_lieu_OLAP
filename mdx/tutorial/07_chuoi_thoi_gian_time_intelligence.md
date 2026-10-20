# CHƯƠNG 07: PHÂN TÍCH CHUỖI THỜI GIAN (TIME SERIES / TIME INTELLIGENCE)

---

## 1. TẦM QUAN TRỌNG CỦA TIME INTELLIGENCE TRONG OLAP

Trong phân tích dữ liệu thể thao và kinh doanh, dữ liệu chỉ thực sự có ý nghĩa khi được đặt vào **dòng chảy thời gian**. Các câu hỏi như:
- *"Phong độ ghi bàn của CLB ở Quý này tăng hay giảm so với Quý trước?"* (QoQ - Quarter-over-Quarter).
- *"Cùng kỳ năm ngoái (Tháng 5/2022 so với Tháng 5/2023), đội bóng ghi được bao nhiêu bàn?"* (YoY - Year-over-Year).
- *"Tính từ đầu năm đến nay (Year-to-Date), tổng số thẻ phạt đã chạm ngưỡng bao nhiêu?"*

Trong SQL truyền thống, các phép tính này đòi hỏi viết câu lệnh `Self-Join` hoặc các hàm cửa sổ rất nặng nề. Trong MDX, hệ thống cung cấp một bộ hàm **Time Intelligence** chuyên biệt hoạt động trực tiếp trên cây phân cấp thời gian.

---

## 2. BẢNG TỔNG HỢP CÁC HÀM TIME INTELLIGENCE CỐT LÕI

| Nhóm chức năng | Tên hàm / Cú pháp | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| **Kỳ liền kề** | `Member.PrevMember` | Lấy phần tử cùng cấp độ ngay liền trước (ví dụ: Tháng 2 $\to$ Tháng 1). |
| **Kỳ kế tiếp** | `Member.NextMember` | Lấy phần tử cùng cấp độ ngay liền sau (ví dụ: Quý 1 $\to$ Quý 2). |
| **Kỳ song song** | `ParallelPeriod(Level, Index, Member)` | Lấy phần tử ở vị trí tương đương tại một chu kỳ cấp cao hơn (ví dụ: cùng tháng này nhưng năm trước). |
| **Tích lũy năm** | `YTD([Member])` | Rút gọn của `PeriodsToDate([Year], Member)` - Tích lũy từ đầu năm đến ngày. |
| **Tích lũy quý** | `QTD([Member])` | Tích lũy từ đầu quý đến thời điểm hiện tại. |
| **Tích lũy tháng** | `MTD([Member])` | Tích lũy từ đầu tháng đến thời điểm hiện tại. |
| **Đầu kỳ / Cuối kỳ**| `OpeningPeriod(Level, Member)` / `ClosingPeriod(...)` | Trả về phần tử con đầu tiên hoặc cuối cùng ở cấp độ sâu chỉ định. |

---

## 3. CÔNG THỨC TOÁN HỌC & ĐỊNH NGHĨA BIẾN THIÊN THỜI GIAN

1. **Biến thiên tuyệt đối (Absolute Variance)**:
   $$\Delta = \text{Current Value} - \text{Previous Value}$$
2. **Tỷ lệ tăng trưởng phần trăm (Growth Rate %)**:
   $$\text{Growth \%} = \frac{\text{Current Value} - \text{Previous Value}}{\text{Previous Value}} \times 100\%$$
   *(Cần bọc hàm `IIF` hoặc cấu trúc kiểm tra mẫu số để phòng ngừa chia cho 0 khi kỳ trước không phát sinh dữ liệu).*
3. **Tổng tích lũy lũy kế (Running Cumulative Total)**:
   $$\text{YTD}(t) = \sum_{i = \text{Start of Year}}^{t} \text{Value}(i)$$

---

## 4. VÍ DỤ PHỨC TẠP: BẢNG THEO DÕI TOÀN DIỆN PHONG ĐỘ QOQ, YOY VÀ LŨY KẾ YTD CỦA REAL MADRID

> **Đề bài nghiệp vụ**: Ban lãnh đạo Real Madrid cần một báo cáo phân tích chuỗi thời gian hoàn chỉnh cho 2 mùa giải (2022 và 2023):
> 1. Số bàn thắng thực tế của từng Quý (`Quarter Goals`).
> 2. Số bàn thắng của Quý liền trước (`Prev Quarter Goals` bằng `.PrevMember`) và Tăng trưởng theo Quý (`QoQ Growth %`).
> 3. Số bàn thắng của cùng Quý này năm trước (`Same Quarter Last Year` bằng `ParallelPeriod`) và Tăng trưởng năm (`YoY Growth %`).
> 4. Tổng số bàn thắng lũy kế từ đầu năm đến hết quý tương ứng (`YTD Cumulative Goals`).

### Mã truy vấn MDX:
```mdx
WITH 
-- 1. Bàn thắng của Quý liền trước (QoQ Base)
MEMBER [Measures].[Prev Quarter Goals] AS
    ([DIM Time].[Hierarchy].CurrentMember.PrevMember, [Measures].[Goals]),
    FORMAT_STRING = '#,##0'

-- 2. Tỷ lệ tăng trưởng so với Quý trước (QoQ Growth %)
MEMBER [Measures].[QoQ Growth Pct] AS
    IIF(
        IsEmpty([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
        NULL,
        ([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]
    ),
    FORMAT_STRING = '+0.00%;-0.00%;0.00%'

-- 3. Bàn thắng cùng Quý năm ngoái (YoY Base bằng ParallelPeriod)
MEMBER [Measures].[Same Quarter Last Year Goals] AS
    (
        ParallelPeriod(
            [DIM Time].[Hierarchy].[Year],
            1,
            [DIM Time].[Hierarchy].CurrentMember
        ),
        [Measures].[Goals]
    ),
    FORMAT_STRING = '#,##0'

-- 4. Tỷ lệ tăng trưởng so với cùng kỳ năm trước (YoY Growth %)
MEMBER [Measures].[YoY Growth Pct] AS
    IIF(
        IsEmpty([Measures].[Same Quarter Last Year Goals]) OR [Measures].[Same Quarter Last Year Goals] = 0,
        NULL,
        ([Measures].[Goals] - [Measures].[Same Quarter Last Year Goals]) / [Measures].[Same Quarter Last Year Goals]
    ),
    FORMAT_STRING = '+0.00%;-0.00%;0.00%'

-- 5. Tổng bàn thắng tích lũy từ đầu năm đến hết Quý (YTD)
MEMBER [Measures].[YTD Goals] AS
    SUM(
        YTD([DIM Time].[Hierarchy].CurrentMember),
        [Measures].[Goals]
    ),
    FORMAT_STRING = '#,##0'

SELECT 
    -- TRỤC CỘT: Bộ 6 Thước đo Time Intelligence
    {
        [Measures].[Goals],
        [Measures].[Prev Quarter Goals],
        [Measures].[QoQ Growth Pct],
        [Measures].[Same Quarter Last Year Goals],
        [Measures].[YoY Growth Pct],
        [Measures].[YTD Goals]
    } ON AXIS(0),

    -- TRỤC DÒNG: Các Quý thuộc 2 năm 2022 và 2023
    NON EMPTY 
    Hierarchize(
        {
            [DIM Time].[Hierarchy].[Quarter].[Q1 2022],
            [DIM Time].[Hierarchy].[Quarter].[Q2 2022],
            [DIM Time].[Hierarchy].[Quarter].[Q3 2022],
            [DIM Time].[Hierarchy].[Quarter].[Q4 2022],
            [DIM Time].[Hierarchy].[Quarter].[Q1 2023],
            [DIM Time].[Hierarchy].[Quarter].[Q2 2023],
            [DIM Time].[Hierarchy].[Quarter].[Q3 2023],
            [DIM Time].[Hierarchy].[Quarter].[Q4 2023]
        }
    ) ON AXIS(1)

FROM [DW Football Transfermarkt]
-- SLICER: Cố định cho CLB Real Madrid
WHERE ([DIM Club].[Club Name].[Real Madrid])
```

---

## 5. BẢNG KẾT QUẢ DỰ KIẾN (EXPECTED OUTPUT TABLE)

Dưới đây là ma trận kết quả phản ánh đầy đủ mọi tình huống biến thiên chuỗi thời gian:

| Phân cấp Quý (`DIM Time`) | Bàn thắng (`Goals`) | Quý trước (`Prev Qtr`) | QoQ Growth % | Cùng kỳ năm trước | YoY Growth % | Bàn thắng lũy kế (`YTD`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q1 2022** | 28 | (null) | (null) | (null) | (null) | **28** |
| **Q2 2022** | 34 | 28 | +21.43% | (null) | (null) | **62** |
| **Q3 2022** | 22 | 34 | -35.29% | (null) | (null) | **84** |
| **Q4 2022** | 36 | 22 | +63.64% | (null) | (null) | **120** |
| **Q1 2023** | 31 | 36 | -13.89% | 28 | **+10.71%** | **31** |
| **Q2 2023** | 38 | 31 | +22.58% | 34 | **+11.76%** | **69** |
| **Q3 2023** | 26 | 38 | -31.58% | 22 | **+18.18%** | **95** |
| **Q4 2023** | 42 | 26 | +61.54% | 36 | **+16.67%** | **137** |

### Giải thích các trường hợp thể hiện trong bảng kết quả:
1. **Trường hợp khởi đầu biên giới dữ liệu (Edge Case - Boundary Nulls)**:
   - Tại `Q1 2022`, do là quý đầu tiên của dải khảo sát, không có quý trước đó nên `Prev Quarter Goals` và `QoQ Growth %` hiển thị `(null)`.
   - Toàn bộ năm 2022 không có dữ liệu năm 2021 nên cột `Same Quarter Last Year` hiển thị `(null)`. Hệ thống xử lý an toàn, không sinh lỗi.
2. **Trường hợp tự động reset chu kỳ tích lũy `YTD()`**:
   - Trong năm 2022, `YTD` tăng dần: $28 \to 62 \to 84 \to 120$.
   - Khi bước sang `Q1 2023`, hàm `YTD` tự động nhận diện ranh giới cây phân cấp cấp Năm và **reset lũy kế về lại 31 bàn**, sau đó tiếp tục cộng dồn cho đến cuối năm đạt **137 bàn**.
3. **Ý nghĩa phân tích thể thao chuyên sâu**:
   - Mặc dù quý 3 hàng năm thường có số bàn thấp nhất (do giai đoạn nghỉ hè tháng 6 - tháng 7 ít trận đấu), nhưng khi so sánh cùng kỳ năm trước (`YoY Growth`), Real Madrid năm 2023 vẫn duy trì mức tăng trưởng ấn tượng từ **+10.71% đến +18.18%** ở mọi quý, chứng minh sức mạnh tấn công gia tăng ổn định.
