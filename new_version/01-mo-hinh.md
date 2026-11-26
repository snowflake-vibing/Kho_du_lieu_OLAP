# Mô hình và kiểu dữ liệu

| Bảng | Thiết kế đề xuất |
| --- | --- |
| `FACT_Player_Match_Perf` | Một dòng mỗi lượt ra sân. Giữ các khóa cầu thủ, CLB, đối thủ, giải, trận và ngày. Các độ đo gốc gồm phút, bàn thắng, kiến tạo, thẻ vàng và thẻ đỏ. |
| `DIM_Player` | Một dòng mỗi cầu thủ. Giữ tên, vị trí và quốc tịch. Giữ ngày sinh, chiều cao hoặc chân thuận nếu có câu hỏi sử dụng. Khai báo ngày sinh kiểu `DATE`. |
| `DIM_Club` | Một dòng mỗi CLB. Hai khóa `Club_ID` và `Opponent_Club_ID` của fact dùng chung bảng chiều với hai vai trò. Tên CLB là đủ cho phạm vi rút gọn. |
| `DIM_Competition` | Một dòng mỗi giải. Dùng cùng kiểu và độ dài của `Competition_ID` trong fact và chiều. |
| `DIM_Game` | Một dòng mỗi trận. Giữ mã trận, hai đội, vòng đấu và `Season` lấy từ `games.season`. Giữ tỷ số nếu báo cáo có câu hỏi cấp trận. |
| `DIM_Time` | Một dòng mỗi ngày, khóa `Time_ID` dạng `YYYYMMDD` và `Full_Date` kiểu `DATE`. Phân cấp năm → quý → tháng → ngày. |

## Khóa lượt ra sân

[DDL hiện tại](../setup_schema_dw_football.sql) tạo `Appearance_ID INT IDENTITY`. Đây là khóa tự sinh của kho. Mã trong [CSV đã làm sạch](../data/cleaned_appearances.csv) là chuỗi có dấu gạch dưới, ví dụ `2872326_110858`. Giữ khóa hiện tại và thêm `Source_Appearance_ID VARCHAR(100) NOT NULL UNIQUE` để truy vết và ngăn nạp trùng. Với kho đồ án có thể nạp lại toàn bộ fact từ CSV sạch để bổ sung mã nguồn.

## Ngày và mùa giải

Chuyển `Season` từ `DIM_Time` sang `DIM_Game`. Mùa `2023/24` có thể trải qua hai năm dương lịch, còn khóa của `DIM_Time` chỉ đại diện cho một ngày. Chốt `Time_ID` là khóa theo DDL và cập nhật [tài liệu DIM Time](../docs/dim_time.md), nơi còn mô tả `Time_SK`. Đồng bộ [sơ đồ DBML](../docs/schema_dbdiagram.dbml), DDL, SSIS, SSAS và bảng mô tả trong Chương 1.
