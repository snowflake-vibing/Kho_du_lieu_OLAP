# 15 CÂU TRUY VẤN NGHIỆP VỤ OLAP (SQL QUERIES)

Dưới đây là danh sách **15 câu truy vấn nghiệp vụ đa chiều (OLAP Queries)** được thiết kế trên hệ cơ sở dữ liệu Kho dữ liệu bóng đá **`DW_Football_Analytics`**. Các câu truy vấn này khai thác tối đa mô hình hình sao (Star Schema) gồm 1 bảng Sự kiện (`FACT_Player_Match_Perf`) và 5 bảng Chiều (`DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`).

---

## DẠNG XEM TỔNG QUAN HỆ THỐNG CÂU TRUY VẤN

| STT | Tên / Mục tiêu truy vấn nghiệp vụ | Bảng DIM & FACT tham gia | Các thuộc tính cốt lõi |
| :---: | :--- | :--- | :--- |
| **1** | Top 10 cầu thủ ghi nhiều bàn thắng nhất tại Ngoại Hạng Anh (GB1) mùa 2023/2024 | `FACT`, `DIM_Player`, `DIM_Competition`, `DIM_Time` | `Player_Name`, `Goals`, `Competition_ID`, `Competition_Name`, `Season` |
| **2** | Top 10 tiền vệ kiến tạo nhiều nhất tại các giải VĐQG (`domestic_league`) | `FACT`, `DIM_Player`, `DIM_Competition` | `Player_Name`, `Assists`, `Main_Position`, `Competition_Type` |
| **3** | Tổng phút thi đấu & đóng góp bàn thắng cho cầu thủ > 20 G+A mùa 2023/2024 | `FACT`, `DIM_Player`, `DIM_Time` | `Player_Name`, `Minutes_Played`, `Goal_Contributions`, `Season` |
| **4** | Bàn thắng, kiến tạo & số phút thi đấu trung bình phân theo độ tuổi năm 2023 | `FACT`, `DIM_Player`, `DIM_Time` | `Age`, `Goals`, `Assists`, `Minutes_Played`, `Year` |
| **5** | So sánh tổng bàn thắng theo chân thuận (Trái, Phải, 2 Chân) & vị trí chi tiết | `FACT`, `DIM_Player` | `Foot`, `Sub_Position`, `Goals` |
| **6** | Chiều cao trung bình, tổng bàn thắng và thẻ vàng phân theo vị trí thi đấu chính | `FACT`, `DIM_Player` | `Height_In_Cm`, `Main_Position`, `Goals`, `Yellow_Cards` |
| **7** | Tổng bàn thắng theo quốc tịch cầu thủ khi thi đấu tại các giải đấu ở Nước Anh | `FACT`, `DIM_Player`, `DIM_Competition` | `Country_Of_Citizenship`, `Country_Name`, `Goals` |
| **8** | Cầu thủ ghi nhiều bàn thắng nhất từ ghế dự bị (`Is_Starter = 0`) & phút dự bị | `FACT`, `DIM_Player` | `Player_Name`, `Is_Starter`, `Goals`, `Minutes_Played` |
| **9** | So sánh bàn thắng & thẻ vàng CLB trên Sân nhà vs Sân khách vào Cuối tuần vs Ngày thường | `FACT`, `DIM_Club`, `DIM_Time` | `Club_Name`, `Is_Home_Game`, `Goals`, `Yellow_Cards`, `Is_Weekend`, `Day_Of_Week` |
| **10** | Tổng bàn thắng Real Madrid ghi vào lưới đối thủ phân theo Quý trong năm | `FACT`, `DIM_Club`, `DIM_Time` | `Club_ID`, `Club_Name`, `Opponent_Club_ID`, `Goals`, `Quarter` |
| **11** | Số trận đấu diễn ra tại sân vận động có sức chứa > 60.000 khán giả | `FACT`, `DIM_Club` | `Stadium_Name`, `Stadium_Seats`, `Club_Name`, `Game_ID` |
| **12** | Tổng thẻ vàng & thẻ đỏ của các đội bóng phân theo HLV trưởng & Tháng trong năm | `FACT`, `DIM_Club`, `DIM_Time` | `Coach_Name`, `Club_Name`, `Yellow_Cards`, `Red_Cards`, `Month` |
| **13** | Tổng lượt ra sân và số cầu thủ phân theo quy mô đội hình (`Squad_Size`) của CLB | `FACT`, `DIM_Club` | `Appearance_ID`, `Player_ID`, `Squad_Size`, `Club_Name` |
| **14** | Thống kê các trận đấu kịch tính (Tổng số bàn thắng $\ge$ 5 bàn) qua các vòng đấu | `DIM_Game`, `DIM_Club` | `Home_Club_ID`, `Away_Club_ID`, `Home_Club_Goals`, `Away_Club_Goals`, `Stadium`, `Round`, `Game_ID` |
| **15** | Thống kê hiệu suất & thẻ phạt của các cầu thủ trẻ sinh từ 01/01/2004 theo ngày thi đấu | `FACT`, `DIM_Player`, `DIM_Time` | `Date_Of_Birth`, `Time_ID`, `Full_Date`, `Day`, `Goals`, `Yellow_Cards`, `Red_Cards` |

---

## CHI TIẾT 15 CÂU TRUY VẤN VÀ CÂU LỆNH T-SQL

### Truy vấn 1: Top 10 Vua dội bom Ngoại Hạng Anh mùa giải 2023/2024
* **Mục tiêu nghiệp vụ:** Tìm ra 10 cầu thủ ghi được nhiều bàn thắng nhất tại giải Vô địch Quốc gia Anh (Premier League - Mã giải `GB1`) trong mùa giải 2023/2024.
* **Các thuộc tính:** `Player_Name`, `Goals`, `Competition_ID`, `Competition_Name`, `Season`.

```sql
USE DW_Football_Analytics;
GO

SELECT TOP 10
    p.Player_Name,
    c.Competition_ID,
    c.Competition_Name,
    t.Season,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE c.Competition_ID = 'GB1' 
  AND (t.Season = '2023/2024' OR t.Year = 2023 OR t.Year = 2024)
GROUP BY p.Player_Name, c.Competition_ID, c.Competition_Name, t.Season
ORDER BY Total_Goals DESC;
```

---

### Truy vấn 2: Top 10 Vua kiến tạo khu vực Tiền vệ ở các giải VĐQG
* **Mục tiêu nghiệp vụ:** Thống kê 10 cầu thủ thi đấu ở tuyến giữa (`Main_Position = 'Midfield'`) có số đường chuyền dọn cỗ (Assists) nhiều nhất tại các giải VĐQG hàng đầu (`Competition_Type = 'domestic_league'`).
* **Các thuộc tính:** `Player_Name`, `Assists`, `Main_Position`, `Competition_Type`.

```sql
SELECT TOP 10
    p.Player_Name,
    p.Main_Position,
    c.Competition_Type,
    SUM(f.Assists) AS Total_Assists
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
WHERE p.Main_Position LIKE '%Midfield%'
  AND c.Competition_Type = 'domestic_league'
GROUP BY p.Player_Name, p.Main_Position, c.Competition_Type
ORDER BY Total_Assists DESC;
```

---

### Truy vấn 3: Tổng số phút thi đấu và đóng góp bàn thắng cho cầu thủ xuất sắc (> 20 G+A)
* **Mục tiêu nghiệp vụ:** Đo lường khối lượng thời gian thi đấu (`Minutes_Played`) và hiệu quả ghi dấu ấn vào bàn thắng (`Goal_Contributions = Goals + Assists`) đối với những chân sút/chân kiến tạo đẳng cấp có trên 20 đóng góp bàn thắng trong mùa 2023/2024.
* **Các thuộc tính:** `Player_Name`, `Minutes_Played`, `Goal_Contributions`, `Season`.

```sql
SELECT 
    p.Player_Name,
    t.Season,
    SUM(f.Minutes_Played) AS Total_Minutes_Played,
    SUM(f.Goal_Contributions) AS Total_Goal_Contributions
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Season = '2023/2024' OR t.Year = 2023
GROUP BY p.Player_Name, t.Season
HAVING SUM(f.Goal_Contributions) > 20
ORDER BY Total_Goal_Contributions DESC;
```

---

### Truy vấn 4: Phân tích hiệu suất thi đấu và số phút trung bình theo từng độ tuổi
* **Mục tiêu nghiệp vụ:** Đánh giá sự ảnh hưởng của yếu tố tuổi tác (`Age`) đến tổng bàn thắng, kiến tạo và độ bền thể lực (số phút thi đấu trung bình mỗi trận) trong năm 2023.
* **Các thuộc tính:** `Age`, `Goals`, `Assists`, `Minutes_Played`, `Year`.

```sql
SELECT 
    p.Age,
    t.Year,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Assists) AS Total_Assists,
    AVG(CAST(f.Minutes_Played AS FLOAT)) AS Avg_Minutes_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE t.Year = 2023 AND p.Age IS NOT NULL
GROUP BY p.Age, t.Year
ORDER BY p.Age ASC;
```

---

### Truy vấn 5: So sánh sức mạnh bàn thắng giữa chân Trái, chân Phải & 2 Chân theo vị trí chi tiết
* **Mục tiêu nghiệp vụ:** Khảo sát xem yếu tố chân thuận (`Foot`: Left, Right, Both) ảnh hưởng như thế nào tới năng suất ghi bàn ở từng vai trò cụ thể trên sân (`Sub_Position` như Striker, Winger, Attacking Midfield...).
* **Các thuộc tính:** `Foot`, `Sub_Position`, `Goals`.

```sql
SELECT 
    p.Sub_Position,
    p.Foot,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE p.Foot IS NOT NULL AND p.Sub_Position IS NOT NULL
GROUP BY p.Sub_Position, p.Foot
ORDER BY p.Sub_Position, Total_Goals DESC;
```

---

### Truy vấn 6: Tương quan chiều cao, khả năng ghi bàn và tính kỷ luật theo vị trí thi đấu chính
* **Mục tiêu nghiệp vụ:** Phân tích chiều cao trung bình (`Height_In_Cm`), tổng bàn thắng (`Goals`) và tổng số thẻ vàng (`Yellow_Cards`) giữa các tuyến thi đấu (`Main_Position`: Goalkeeper, Defender, Midfield, Attack).
* **Các thuộc tính:** `Height_In_Cm`, `Main_Position`, `Goals`, `Yellow_Cards`.

```sql
SELECT 
    p.Main_Position,
    AVG(CAST(p.Height_In_Cm AS FLOAT)) AS Avg_Height_Cm,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Yellow_Cards) AS Total_Yellow_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE p.Main_Position IS NOT NULL
GROUP BY p.Main_Position
ORDER BY Total_Goals DESC;
```

---

### Truy vấn 7: Thống kê bàn thắng theo quốc tịch cầu thủ tại các giải đấu thuộc Nước Anh
* **Mục tiêu nghiệp vụ:** Đo lường sự đóng góp chuyên môn của lực lượng cầu thủ nội địa Anh so với các cầu thủ ngoại binh (phân theo `Country_Of_Citizenship`) tại các giải đấu diễn ra ở Anh (`Country_Name = 'England'`).
* **Các thuộc tính:** `Country_Of_Citizenship`, `Country_Name`, `Goals`.

```sql
SELECT 
    p.Country_Of_Citizenship,
    c.Country_Name,
    SUM(f.Goals) AS Total_Goals
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Competition c ON f.Competition_SK = c.Competition_SK
WHERE c.Country_Name = 'England' AND p.Country_Of_Citizenship IS NOT NULL
GROUP BY p.Country_Of_Citizenship, c.Country_Name
ORDER BY Total_Goals DESC;
```

---

### Truy vấn 8: Danh sách các "Siêu dự bị" ghi nhiều bàn thắng nhất khi vào sân từ ghế dự bị
* **Mục tiêu nghiệp vụ:** Phát hiện những cầu thủ thi đấu bùng nổ, có duyên ghi bàn khi không có tên trong đội hình xuất phát (`Is_Starter = 0`) và thống kê tổng phút thi đấu dự bị của họ.
* **Các thuộc tính:** `Player_Name`, `Is_Starter`, `Goals`, `Minutes_Played`.

```sql
SELECT TOP 15
    p.Player_Name,
    f.Is_Starter,
    SUM(f.Goals) AS Goals_As_Sub,
    SUM(f.Minutes_Played) AS Sub_Minutes_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
WHERE f.Is_Starter = 0
GROUP BY p.Player_Name, f.Is_Starter
HAVING SUM(f.Goals) > 0
ORDER BY Goals_As_Sub DESC, Sub_Minutes_Played ASC;
```

---

### Truy vấn 9: So sánh hiệu năng & thẻ phạt Sân nhà vs Sân khách giữa Cuối tuần & Ngày thường
* **Mục tiêu nghiệp vụ:** Phân tích ảnh hưởng của yếu tố địa lợi sân bãi (`Is_Home_Game`) và thời điểm diễn ra trận đấu (`Is_Weekend`: Thứ 7/Chủ Nhật vs Ngày thường `Day_Of_Week`) đến tổng bàn thắng ghi được và mức độ phạm lỗi (thẻ vàng).
* **Các thuộc tính:** `Club_Name`, `Is_Home_Game`, `Goals`, `Yellow_Cards`, `Is_Weekend`, `Day_Of_Week`.

```sql
SELECT 
    cb.Club_Name,
    f.Is_Home_Game,
    t.Is_Weekend,
    SUM(f.Goals) AS Total_Goals,
    SUM(f.Yellow_Cards) AS Total_Yellow_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
GROUP BY cb.Club_Name, f.Is_Home_Game, t.Is_Weekend
ORDER BY cb.Club_Name, f.Is_Home_Game, t.Is_Weekend;
```

---

### Truy vấn 10: Thống kê bàn thắng của Real Madrid vào lưới các đối thủ theo từng Quý trong năm
* **Mục tiêu nghiệp vụ:** Khảo sát chi tiết số bàn thắng của câu lạc bộ Real Madrid (`Club_ID = 418` hoặc `Club_Name = 'Real Madrid'`) ghi vào lưới từng câu lạc bộ đối thủ (`Opponent_Club_SK`) phân bổ qua 4 Quý thời gian (`Quarter` 1, 2, 3, 4).
* **Các thuộc tính:** `Club_ID`, `Club_Name`, `Opponent_Club_ID`, `Goals`, `Quarter`.

```sql
SELECT 
    cb.Club_ID,
    cb.Club_Name AS Real_Madrid,
    opp.Club_Name AS Opponent_Club_Name,
    t.Quarter,
    SUM(f.Goals) AS Goals_Scored
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
JOIN dbo.DIM_Club opp ON f.Opponent_Club_SK = opp.Club_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE cb.Club_ID = 418 OR cb.Club_Name LIKE '%Real Madrid%'
GROUP BY cb.Club_ID, cb.Club_Name, opp.Club_Name, t.Quarter
ORDER BY t.Quarter, Goals_Scored DESC;
```

---

### Truy vấn 11: Số lượng trận đấu tại các "Thánh địa" có sức chứa > 60.000 khán giả
* **Mục tiêu nghiệp vụ:** Thống kê số lượng trận đấu (`Game_ID`) đã tổ chức tại các sân vận động quy mô lớn (`Stadium_Seats > 60000`) của các câu lạc bộ hàng đầu Châu Âu.
* **Các thuộc tính:** `Stadium_Name`, `Stadium_Seats`, `Club_Name`, `Game_ID`.

```sql
SELECT 
    cb.Club_Name,
    cb.Stadium_Name,
    cb.Stadium_Seats,
    COUNT(DISTINCT f.Game_ID) AS Total_Matches_Played
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
WHERE cb.Stadium_Seats > 60000
GROUP BY cb.Club_Name, cb.Stadium_Name, cb.Stadium_Seats
ORDER BY cb.Stadium_Seats DESC;
```

---

### Truy vấn 12: Thẻ phạt của các đội bóng phân theo Huấn luyện viên trưởng & Tháng trong năm
* **Mục tiêu nghiệp vụ:** Đo lường lối chơi và phong cách kỷ luật của các chiến lược gia (`Coach_Name`) thông qua tổng số thẻ vàng (`Yellow_Cards`) và thẻ đỏ (`Red_Cards`) mà các học trò nhận phải theo từng tháng (`Month`).
* **Các thuộc tính:** `Coach_Name`, `Club_Name`, `Yellow_Cards`, `Red_Cards`, `Month`.

```sql
SELECT 
    cb.Coach_Name,
    cb.Club_Name,
    t.Month,
    SUM(f.Yellow_Cards) AS Total_Yellow_Cards,
    SUM(f.Red_Cards) AS Total_Red_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE cb.Coach_Name IS NOT NULL
GROUP BY cb.Coach_Name, cb.Club_Name, t.Month
ORDER BY Total_Yellow_Cards DESC, Total_Red_Cards DESC;
```

---

### Truy vấn 13: Thống kê số lượt ra sân và lực lượng cầu thủ theo quy mô đội hình (`Squad_Size`)
* **Mục tiêu nghiệp vụ:** Đánh giá mối quan hệ giữa độ dày đội hình đăng ký (`Squad_Size`) với tần suất xoay tua cầu thủ (`Total_Appearances` & `Active_Players_Count`).
* **Các thuộc tính:** `Appearance_ID`, `Player_ID`, `Squad_Size`, `Club_Name`.

```sql
SELECT 
    cb.Club_Name,
    cb.Squad_Size,
    COUNT(f.Appearance_ID) AS Total_Appearances,
    COUNT(DISTINCT f.Player_SK) AS Active_Players_Count
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Club cb ON f.Club_SK = cb.Club_SK
GROUP BY cb.Club_Name, cb.Squad_Size
ORDER BY cb.Squad_Size DESC;
```

---

### Truy vấn 14: Thống kê các trận cầu mưa bàn thắng ($\ge$ 5 bàn) qua các vòng đấu
* **Mục tiêu nghiệp vụ:** Lọc ra các trận đấu bùng nổ bàn thắng kịch tính (Tổng số bàn thắng của Đội nhà + Đội khách từ 5 bàn trở lên) để phục vụ phân tích trải nghiệm khán giả và diễn biến chuyên môn.
* **Các thuộc tính:** `Home_Club_ID`, `Away_Club_ID`, `Home_Club_Goals`, `Away_Club_Goals`, `Stadium`, `Round`, `Game_ID`.

```sql
SELECT 
    g.Game_ID,
    g.Round,
    hc.Club_Name AS Home_Club,
    ac.Club_Name AS Away_Club,
    g.Home_Club_Goals,
    g.Away_Club_Goals,
    (g.Home_Club_Goals + g.Away_Club_Goals) AS Total_Match_Goals,
    g.Stadium
FROM dbo.DIM_Game g
JOIN dbo.DIM_Club hc ON g.Home_Club_ID = hc.Club_ID
JOIN dbo.DIM_Club ac ON g.Away_Club_ID = ac.Club_ID
WHERE (g.Home_Club_Goals + g.Away_Club_Goals) >= 5
ORDER BY Total_Match_Goals DESC, g.Season DESC;
```

---

### Truy vấn 15: Theo dõi phong độ & thẻ phạt của lứa cầu thủ trẻ (Sinh từ 01/01/2004) theo ngày
* **Mục tiêu nghiệp vụ:** Theo dõi tiến trình phát triển, năng suất ghi bàn và mức độ va chạm (thẻ phạt) của thế hệ tài năng trẻ (Gen Z sinh từ năm 2004 trở lại đây) qua từng ngày thi đấu cụ thể (`Full_Date`, `Day`, `Time_ID`).
* **Các thuộc tính:** `Date_Of_Birth`, `Time_ID`, `Full_Date`, `Day`, `Goals`, `Yellow_Cards`, `Red_Cards`.

```sql
SELECT 
    p.Player_Name,
    p.Date_Of_Birth,
    t.Time_ID,
    t.Full_Date,
    t.Day,
    SUM(f.Goals) AS Goals,
    SUM(f.Yellow_Cards) AS Yellow_Cards,
    SUM(f.Red_Cards) AS Red_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.Player_SK = p.Player_SK
JOIN dbo.DIM_Time t ON f.Time_SK = t.Time_SK
WHERE p.Date_Of_Birth >= '2004-01-01'
GROUP BY p.Player_Name, p.Date_Of_Birth, t.Time_ID, t.Full_Date, t.Day
ORDER BY t.Time_ID ASC, Goals DESC;
```
