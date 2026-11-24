# 4.1 Chuẩn bị nguồn dữ liệu

## Kết nối Power BI với kho dữ liệu đa chiều

1. Deploy và process cube **DW Football Transfermarkt** trên máy chủ SSAS Multidimensional.
2. Trong Power BI Desktop, chọn **Get data → SQL Server Analysis Services database**, nhập máy chủ SSAS, rồi chọn **Connect live**.
3. Chọn cube **DW Football Transfermarkt** trong Navigator. Kiểm tra nhóm độ đo và các chiều Cầu thủ, Câu lạc bộ, Giải đấu, Trận đấu và Thời gian.
4. Thêm hai thẻ kiểm tra với `Distinct Matches Played` và `FACT Player Match Perf Count`. Với một trận có nhiều cầu thủ ra sân, thẻ thứ nhất đếm một trận, thẻ thứ hai đếm các lượt ra sân hiện có trong ngữ cảnh lọc.

Xem [triển khai cube và truy vấn MDX](../ssas/ssas_deploy_mdx.md) và [định nghĩa bảng sự kiện](../docs/fact_player_match_perf.md).

## Xuất dữ liệu cho Looker Studio

Mở cơ sở dữ liệu kho bóng đá đã nạp trong SSMS và chạy truy vấn đọc dưới đây. Xuất kết quả dạng CSV UTF-8 có dòng tiêu đề. Mỗi dòng tương ứng một lượt ra sân. Cột `Full_Date` xuất dưới dạng ISO để dùng bộ lọc khoảng ngày. Phạm vi 2022–2024 được xác định theo năm dương lịch, còn `Season` giữ nguyên nhãn mùa giải.

```sql
SELECT
    F.Appearance_ID, F.Game_ID, F.Player_ID, F.Club_ID, F.Competition_ID,
    P.Player_Name, P.Age, P.Sub_Position, P.Foot,
    P.Country_Of_Citizenship,
    C.Club_Name, C.Coach_Name,
    Comp.Competition_Name, Comp.Country_Name AS Competition_Country,
    Comp.Competition_Type,
    G.[Round] AS Match_Round, G.Stadium,
    CONVERT(char(10), D.Match_Date, 23) AS Full_Date,
    T.[Year], T.[Quarter], T.[Month], T.Season,
    F.Goals, F.Assists, F.Goal_Contributions, F.Minutes_Played,
    F.Yellow_Cards, F.Red_Cards
FROM dbo.FACT_Player_Match_Perf AS F
JOIN dbo.DIM_Player AS P ON P.Player_ID = F.Player_ID
JOIN dbo.DIM_Club AS C ON C.Club_ID = F.Club_ID
JOIN dbo.DIM_Competition AS Comp ON Comp.Competition_ID = F.Competition_ID
JOIN dbo.DIM_Game AS G ON G.Game_ID = F.Game_ID
JOIN dbo.DIM_Time AS T ON T.Time_ID = F.Time_ID
CROSS APPLY (VALUES (TRY_CONVERT(date, CONVERT(char(8), F.Time_ID), 112))) AS D(Match_Date)
WHERE D.Match_Date >= '20220101' AND D.Match_Date < '20250101';
```

## Quy ước tổng hợp

| Chỉ số | Định nghĩa trên dữ liệu lượt ra sân |
| --- | --- |
| Số trận | Đếm phân biệt `Game_ID` |
| Lượt ra sân | Đếm phân biệt `Appearance_ID` |
| Bàn thắng, kiến tạo, phút thi đấu, thẻ | Tổng từng cột tương ứng trong bộ lọc |
| Đóng góp bàn thắng | Tổng `Goal_Contributions`, đối chiếu với tổng bàn thắng cộng tổng kiến tạo |
| Phút trung bình mỗi lượt | Tổng số phút chia số lượt ra sân |
| Số HLV | Đối chiếu định nghĩa độ đo `Total Coaches` trong cube. Nếu đếm tên trên CSV, ghi rõ cách xử lý tên trống và giá trị đại diện cho HLV chưa xác định. |

Một trận có thể xuất hiện ở nhiều dòng hoặc nhiều nhóm CLB. Tính lại số trận phân biệt ở cấp tổng thay vì cộng số trận từ các nhóm. Với báo biểu sân vận động, dùng `Stadium` của trận đấu. Tên sân mặc định của CLB có thể khác địa điểm trận.
