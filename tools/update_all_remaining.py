# -*- coding: utf-8 -*-
import sys, re

# ==============================================================================
# 1. UPDATE QUERY 01
# ==============================================================================
with open('mdx/query_01.md', 'r', encoding='utf-8') as f:
    q01 = f.read()

# Replace [2023/2024] with [2023] in MDX and text
q01 = q01.replace('[DIM Time].[Season].[2023/2024]', '[DIM Time].[Season].[2023]')
q01 = q01.replace("WHERE t.Season = '2023/2024'", "WHERE t.Season = '2023'")
q01 = q01.replace("mùa giải 2023/2024", "mùa giải 2023/2024 (Season = '2023')")

# Update Section 3 Table in query_01
s3_01 = """| Xếp hạng | Tên Cầu Thủ (`Player Name`) | Câu Lạc Bộ Thi Đấu | Tổng Số Bàn Thắng (`Goals`) |
| :---: | :--- | :--- | :---: |
| **1** | **Erling Haaland** | Manchester City | **27** |
| **2** | **Cole Palmer** | Chelsea FC | **22** |
| **3** | **Alexander Isak** | Newcastle United | **21** |
| **4** | **Dominic Solanke** | AFC Bournemouth | **19** |
| **5** | **Ollie Watkins** | Aston Villa | **19** |
| **6** | **Phil Foden** | Manchester City | **19** |
| **7** | **Mohamed Salah** | Liverpool FC | **18** |
| **8** | **Heung-min Son** | Tottenham Hotspur | **17** |
| **9** | **Bukayo Saka** | Arsenal FC | **16** |
| **10** | **Jarrod Bowen** | West Ham United | **16** |"""

q01 = re.sub(r'\| Xếp hạng \| Tên Cầu Thủ.*?\n(?=\n---|\n## 4|\Z)', s3_01 + '\n', q01, flags=re.DOTALL)

with open('mdx/query_01.md', 'w', encoding='utf-8') as f:
    f.write(q01)
print("query_01.md updated successfully!")

# ==============================================================================
# 2. UPDATE QUERY 03
# ==============================================================================
with open('mdx/query_03.md', 'r', encoding='utf-8') as f:
    q03 = f.read()

q03 = q03.replace('[DIM Time].[Season].[2023/2024]', '[DIM Time].[Season].[2023]')
q03 = q03.replace("WHERE t.Season = '2023/2024'", "WHERE t.Season = '2023'")

s3_03 = """| Xếp hạng | Tên Cầu Thủ (`Player Name`) | Câu Lạc Bộ Đại Diện | Số Phút Thi Đấu (`Minutes Played`) | Đóng Góp Bàn Thắng (`Goal Contributions`) |
| :---: | :--- | :--- | :---: | :---: |
| **1** | **Harry Kane** | FC Bayern Munich | 3.818 | **56** |
| **2** | **Luuk de Jong** | PSV Eindhoven | 3.406 | **47** |
| **3** | **Viktor Gyökeres** | Sporting CP | 3.447 | **43** |
| **4** | **Kylian Mbappé** | Paris Saint-Germain | 3.149 | **40** |
| **5** | **Erling Haaland** | Manchester City | 3.337 | **38** |
| **6** | **Mauro Icardi** | Galatasaray | 3.465 | **38** |
| **7** | **Pierre-Emerick Aubameyang** | Olympique Marseille | 3.659 | **38** |
| **8** | **Mohamed Salah** | Liverpool FC | 2.935 | **37** |
| **9** | **Loïs Openda** | RB Leipzig | 3.274 | **35** |
| **10** | **Phil Foden** | Manchester City | 3.555 | **35** |
| **11** | **Jude Bellingham** | Real Madrid | 3.318 | **34** |
| **12** | **Cole Palmer** | Chelsea FC | 2.628 | **33** |
| **13** | **Bukayo Saka** | Arsenal FC | 3.661 | **33** |"""

q03 = re.sub(r'\| Xếp hạng \| Tên Cầu Thủ.*?\n(?=\n---|\n## 4|\Z)', s3_03 + '\n', q03, flags=re.DOTALL)

with open('mdx/query_03.md', 'w', encoding='utf-8') as f:
    f.write(q03)
print("query_03.md updated successfully!")

# ==============================================================================
# 3. UPDATE QUERY 04
# ==============================================================================
with open('mdx/query_04.md', 'r', encoding='utf-8') as f:
    q04 = f.read()

s3_04 = """| Độ Tuổi (`Age`) | Phân Khúc Sự Nghiệp (`Career Stage`) | Tổng Bàn Thắng (`Goals`) | Tổng Kiến Tạo (`Assists`) | Số Phút TB/Trận (`Avg Minutes`) |
| :---: | :--- | :---: | :---: | :---: |
| **19** | U21 Young Talent | 1 | 3 | 40.31 |
| **20** | U21 Young Talent | 24 | 16 | 47.78 |
| **21** | U21 Young Talent | 46 | 54 | 42.69 |
| **22** | Prime Age (22-29) | 127 | 115 | 44.89 |
| **23** | Prime Age (22-29) | 298 | 266 | 51.30 |
| **24** | Prime Age (22-29) | 447 | 391 | 57.07 |
| **25** | Prime Age (22-29) | 672 | 536 | 59.74 |
| **26** | Prime Age (22-29) | 865 | 694 | 62.56 |
| **27** | Prime Age (22-29) | 838 | 641 | 63.33 |
| **28** | Prime Age (22-29) | 948 | 718 | 66.09 |
| **29** | Prime Age (22-29) | 1.008 | 776 | 67.72 |
| **30** | Veteran (30+) | 816 | 582 | 65.17 |
| **31** | Veteran (30+) | 632 | 471 | 65.28 |
| **32** | Veteran (30+) | 720 | 561 | 69.87 |
| **33** | Veteran (30+) | 660 | 484 | 69.45 |
| **34** | Veteran (30+) | 543 | 403 | 68.92 |
| **35** | Veteran (30+) | 507 | 316 | 66.56 |
| **36** | Veteran (30+) | 222 | 198 | 68.58 |
| **37** | Veteran (30+) | 199 | 139 | 66.51 |
| **38** | Veteran (30+) | 165 | 126 | 70.28 |"""

q04 = re.sub(r'\| Độ Tuổi.*?\n(?=\n---|\n## 4|\Z)', s3_04 + '\n', q04, flags=re.DOTALL)

with open('mdx/query_04.md', 'w', encoding='utf-8') as f:
    f.write(q04)
print("query_04.md updated successfully!")

# ==============================================================================
# 4. UPDATE QUERY 05
# ==============================================================================
with open('mdx/query_05.md', 'r', encoding='utf-8') as f:
    q05 = f.read()

# Fix MDX query in query_05 (put Goals on COLUMNS, CrossJoin on ROWS)
old_mdx_05 = """SELECT
    -- Trục Cột: Chân thuận của cầu thủ
    {
        [DIM Player].[Foot].[Foot].MEMBERS
    } ON COLUMNS,

    -- Trục Dòng: Các vị trí tấn công và tiền vệ chủ chốt
    ORDER(
        CrossJoin(
            UNION(
                { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
                { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
            ),
            EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All], [DIM Player].[Foot].[Unknown] })
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Lấy thước đo tổng số bàn thắng
WHERE ([Measures].[Goals]);"""

new_mdx_05 = """SELECT
    -- Trục Cột: Thước đo tổng số bàn thắng
    { [Measures].[Goals] } ON COLUMNS,

    -- Trục Dòng: Tích Đề-các giữa 5 vị trí tấn công và chân thuận, xếp giảm dần
    ORDER(
        CrossJoin(
            UNION(
                { [DIM Player].[Sub Position].[Centre-Forward], [DIM Player].[Sub Position].[Second Striker] },
                { [DIM Player].[Sub Position].[Left Winger], [DIM Player].[Sub Position].[Right Winger], [DIM Player].[Sub Position].[Attacking Midfield] }
            ),
            EXCEPT([DIM Player].[Foot].[Foot].MEMBERS, { [DIM Player].[Foot].[All], [DIM Player].[Foot].[Unknown] })
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];"""

if old_mdx_05 in q05:
    q05 = q05.replace(old_mdx_05, new_mdx_05)
else:
    # replace regex
    q05 = re.sub(r'SELECT\s+\{\s+\[DIM Player\]\.\[Foot\]\.\[Foot\]\.MEMBERS\s+\}\s+ON\s+COLUMNS.*?WHERE\s+\(\[Measures\]\.\[Goals\]\);', new_mdx_05, q05, flags=re.DOTALL)

s3_05 = """| Vị Trí Chi Tiết (`Sub Position`) | Chân Thuận (`Foot`) | Tổng Bàn Thắng (`Goals`) | Đánh Giá Chiến Thuật & Đặc Điểm |
| :--- | :---: | :---: | :--- |
| **Centre-Forward** | **right** | **5.457** | Trung phong chân phải truyền thống, chiếm khối lượng bàn thắng áp đảo |
| **Left Winger** | **right** | **2.015** | Tiền đạo cánh trái nghịch chân (Inverted Winger) cắt vào trong dứt điểm |
| **Attacking Midfield** | **right** | **1.308** | Nhạc trưởng làm bóng và sút xa từ tuyến hai bằng chân thuận |
| **Right Winger** | **left** | **1.207** | Tiền đạo cánh phải nghịch chân (kèo trái) tạo đột biến |
| **Centre-Forward** | **left** | **1.114** | Trung phong chân trái hiếm có, góc sút độc hiểm |
| **Right Winger** | **right** | **783** | Tiền đạo cánh phải bám biên tạt bóng cổ điển |
| **Attacking Midfield** | **left** | **667** | Tiền vệ công chân trái điều tiết nhịp độ và sút phạt |
| **Centre-Forward** | **both** | **273** | Tiền đạo toàn năng hai chân, cực kỳ nguy hiểm trong vòng cấm |
| **Second Striker** | **right** | **242** | Hộ công cơ động hỗ trợ trung phong |
| **Left Winger** | **left** | **186** | Tiền đạo cánh trái thuần tạt bóng biên |
| **Left Winger** | **both** | **79** | Chạy cánh trái dứt điểm linh hoạt hai chân |
| **Right Winger** | **both** | **76** | Chạy cánh phải dứt điểm linh hoạt hai chân |
| **Attacking Midfield** | **both** | **59** | Tiền vệ công xử lý bóng hai chân |
| **Second Striker** | **left** | **40** | Hộ công chân trái |
| **Second Striker** | **both** | **13** | Hộ công xử lý hai chân |"""

q05 = re.sub(r'\| Vị Trí Chi Tiết.*?\n(?=\n---|\n## 4|\Z)', s3_05 + '\n', q05, flags=re.DOTALL)

with open('mdx/query_05.md', 'w', encoding='utf-8') as f:
    f.write(q05)
print("query_05.md updated successfully!")

# ==============================================================================
# 5. UPDATE QUERY 09
# ==============================================================================
with open('mdx/query_09.md', 'r', encoding='utf-8') as f:
    q09 = f.read()

s3_09 = """| Tên Câu Lạc Bộ (`Club Name`) | Cuối tuần - Bàn thắng | Cuối tuần - Thẻ vàng | Ngày thường - Bàn thắng | Ngày thường - Thẻ vàng |
| :--- | :---: | :---: | :---: | :---: |
| **FC Bayern Munich** | 150 | 83 | 75 | 46 |
| **Manchester City** | 139 | 76 | 106 | 53 |
| **Arsenal FC** | 134 | 93 | 65 | 52 |
| **Bayer 04 Leverkusen** | 131 | 122 | 60 | 72 |
| **Borussia Dortmund** | 128 | 101 | 49 | 64 |
| **Paris Saint-Germain** | 128 | 93 | 70 | 59 |
| **Real Madrid** | 128 | 108 | 82 | 67 |
| **FC Barcelona** | 118 | 147 | 61 | 65 |
| **SL Benfica** | 115 | 81 | 77 | 89 |
| **Fenerbahce** | 113 | 111 | 75 | 76 |"""

q09 = re.sub(r'\| Tên Câu Lạc Bộ.*?\n(?=\n---|\n## 4|\Z)', s3_09 + '\n', q09, flags=re.DOTALL)

with open('mdx/query_09.md', 'w', encoding='utf-8') as f:
    f.write(q09)
print("query_09.md updated successfully!")

# ==============================================================================
# 6. UPDATE QUERY 10
# ==============================================================================
with open('mdx/query_10.md', 'r', encoding='utf-8') as f:
    q10 = f.read()

# Fix MDX where clause in query_10 (remove [DIM Time].[Hierarchy].[Year].[2023] from WHERE)
q10 = q10.replace("""WHERE (
    [DIM Club].[Club Name].[Real Madrid],
    [DIM Time].[Hierarchy].[Year].[2023]
);""", """WHERE (
    [DIM Club].[Club Name].[Real Madrid]
);""")

s3_10 = """| Đối Thủ (`Opponent Club`) | Q1 Bàn Thắng | Q1 QoQ % | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **UD Almería** | - | - | 4 | - | 3 | -25.00% | - | -100.00% |
| **CA Osasuna** | 2 | +100.00% | - | -100.00% | - | - | 4 | - |
| **Cádiz CF** | - | -100.00% | 2 | - | - | -100.00% | 3 | - |
| **Girona FC** | - | -100.00% | 2 | - | 3 | +50.00% | - | -100.00% |
| **Villarreal CF** | 1 | - | 1 | 0.00% | - | -100.00% | 4 | - |
| **Celta de Vigo** | - | - | 2 | - | 1 | -50.00% | - | -100.00% |
| **Valencia CF** | 2 | - | 0 | -100.00% | - | - | 5 | - |
| **FC Barcelona** | 0 | -100.00% | - | - | - | - | 2 | - |"""

q10 = re.sub(r'\| Đối Thủ.*?\n(?=\n---|\n## 4|\Z)', s3_10 + '\n', q10, flags=re.DOTALL)

with open('mdx/query_10.md', 'w', encoding='utf-8') as f:
    f.write(q10)
print("query_10.md updated successfully!")

# ==============================================================================
# 7. UPDATE QUERY 11
# ==============================================================================
with open('mdx/query_11.md', 'r', encoding='utf-8') as f:
    q11 = f.read()

# Fix MDX query in query_11: include Stadium Seats in the set
old_mdx_11 = """WITH 
    -- 1. Sức chứa sân vận động xử lý NULL bằng COALESCEEMPTY
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        COALESCEEMPTY(
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE,
            0
        ),
        FORMAT_STRING = "#,##0 Chỗ"

    -- 2. Đếm số trận đấu duy nhất diễn ra tại sân vận động
    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Sức chứa sân đã làm sạch, số trận duy nhất và tổng bàn thắng
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các sân vận động có sức chứa >= 60.000 chỗ, xếp giảm dần
    ORDER(
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] }),
                    EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] })
                ),
                [Measures].[FACT Player Match Perf Count]
            ),
            [Measures].[Stadium Capacity Cleaned] >= 60000
        ),
        [Measures].[Stadium Capacity Cleaned],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];"""

new_mdx_11 = """WITH 
    -- 1. Tập hợp các sân vận động quy mô lớn (sức chứa >= 60.000 chỗ)
    SET [ValidStadiums] AS
        FILTER(
            NONEMPTY(
                CrossJoin(
                    EXCEPT([DIM Club].[Stadium Name].[Stadium Name].MEMBERS, { [DIM Club].[Stadium Name].[All] }),
                    EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                    EXCEPT([DIM Club].[Stadium Seats].[Stadium Seats].MEMBERS, { [DIM Club].[Stadium Seats].[0], [DIM Club].[Stadium Seats].[All] })
                ),
                [Measures].[FACT Player Match Perf Count]
            ),
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE >= 60000
        )

    -- 2. Sức chứa sân vận động định dạng chuẩn
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
        FORMAT_STRING = "#,##0 Chỗ"

    -- 3. Đếm số trận đấu duy nhất diễn ra tại sân vận động
    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Sức chứa sân đã làm sạch, số trận duy nhất và tổng bàn thắng
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các sân vận động có sức chứa >= 60.000 chỗ, xếp giảm dần
    ORDER(
        [ValidStadiums],
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];"""

if old_mdx_11 in q11:
    q11 = q11.replace(old_mdx_11, new_mdx_11)
else:
    q11 = re.sub(r'WITH\s+-- 1\. Sức chứa sân vận động.*?FROM \[DW Football Transfermarkt\];', new_mdx_11, q11, flags=re.DOTALL)

s3_11 = """| Sân Vận Động (`Stadium Name`) | Câu Lạc Bộ Chủ Quản (`Club Name`) | Sức Chứa Chuẩn Hóa (`Stadium Capacity`) | Số Trận Đã Diễn Ra (`Distinct Matches`) | Tổng Bàn Thắng (`Goals`) |
| :--- | :--- | :---: | :---: | :---: |
| **Santiago Bernabéu** | Real Madrid | 83.186 Chỗ | 101 | 210 |
| **SIGNAL IDUNA PARK** | Borussia Dortmund | 81.365 Chỗ | 89 | 177 |
| **Atatürk Olimpiyat** | Fatih Karagümrük | 77.563 Chỗ | 72 | 118 |
| **Giuseppe Meazza** | AC Milan | 75.923 Chỗ | 100 | 169 |
| **Giuseppe Meazza** | Inter Milan | 75.923 Chỗ | 97 | 184 |
| **Allianz Arena** | Bayern Munich | 75.000 Chỗ | 90 | 225 |
| **Old Trafford** | Manchester United | 74.879 Chỗ | 94 | 145 |
| **Olympiastadion Berlin** | Hertha BSC | 74.667 Chỗ | 34 | 40 |
| **La Cartuja** | Real Betis Balompié | 71.374 Chỗ | 90 | 111 |
| **Olimpico di Roma** | AS Roma | 70.634 Chỗ | 105 | 156 |"""

q11 = re.sub(r'\| Sân Vận Động.*?\n(?=\n---|\n## 4|\Z)', s3_11 + '\n', q11, flags=re.DOTALL)

with open('mdx/query_11.md', 'w', encoding='utf-8') as f:
    f.write(q11)
print("query_11.md updated successfully!")

# ==============================================================================
# 8. UPDATE QUERY 12
# ==============================================================================
with open('mdx/query_12.md', 'r', encoding='utf-8') as f:
    q12 = f.read()

# In MDX, filter out Unknown Coach
q12 = q12.replace('[DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown"', '[DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown" AND [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown Coach"')

s3_12 = """| Huấn Luyện Viên (`Coach Name`) | Tháng Kỷ Lục Thẻ Phạt (`Month`) | Thẻ Vàng (`Yellow Cards`) | Thẻ Đỏ (`Red Cards`) | Nhận Định Chuyên Môn |
| :--- | :---: | :---: | :---: | :--- |
| **Matías Almeyda** | Tháng 10 | **32** | **1** | Tháng đỉnh điểm căng thẳng tại giải VĐQG Hy Lạp |
| **Diego Simeone** | Tháng 10 | **27** | **0** | Phong cách phòng ngự áp sát rát, thẻ vàng đạt đỉnh |
| **João Pereira** | Tháng 10 | **27** | **0** | Đội bóng nhận nhiều thẻ trong các trận derby căng thẳng |
| **Rúben Amorim** | Tháng 12 | **25** | **0** | Giai đoạn tourmalet mùa đông tại Bồ Đào Nha |
| **Sergio Francisco** | Tháng 10 | **25** | **0** | Đội hình trẻ tranh chấp quyết liệt |
| **Sven Vandenbroeck** | Tháng 10 | **25** | **1** | Đạt đỉnh thẻ phạt và có 1 thẻ đỏ trực tiếp |
| **Russell Martin** | Tháng 10 | **24** | **0** | Lối chơi kiểm soát bóng chịu nhiều pha phản công |
| **Sandro Wagner** | Tháng 10 | **24** | **0** | Tranh chấp va chạm rát ở khu vực giữa sân |
| **Carlos Corberán** | Tháng 10 | **23** | **1** | Lối đá thể lực áp sát cao độ |
| **José Bordalás** | Tháng 5 | **23** | **0** | Giai đoạn nước rút cuối mùa giải khốc liệt |"""

q12 = re.sub(r'\| Huấn Luyện Viên.*?\n(?=\n---|\n## 4|\Z)', s3_12 + '\n', q12, flags=re.DOTALL)

with open('mdx/query_12.md', 'w', encoding='utf-8') as f:
    f.write(q12)
print("query_12.md updated successfully!")
