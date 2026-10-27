# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx = """
/* ==============================================================================
   Truy vấn MDX 06: Thể hình (AVG, MAX, MIN) và hiệu suất theo vị trí chính
   Khai thác: WITH SET, WITH MEMBER, AVG, MAX, MIN, CrossJoin, NONEMPTY, ORDER
   Cube: [DW Football Transfermarkt]
   ============================================================================== */

WITH 
    -- 1. Tập hợp các cầu thủ hợp lệ (có chiều cao > 0) theo ngữ cảnh vị trí đang xét
    SET [ValidPlayers] AS
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                EXCEPT(
                    [DIM Player].[Height In Cm].[Height In Cm].MEMBERS,
                    { [DIM Player].[Height In Cm].[0], [DIM Player].[Height In Cm].[All] }
                )
            ),
            [Measures].[FACT Player Match Perf Count]
        )

    -- 2. Chiều cao trung bình theo vị trí
    MEMBER [Measures].[Avg Height Cm] AS
        ROUND(
            AVG(
                [ValidPlayers],
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
            ),
            1
        ),
        FORMAT_STRING = "#,##0.0"

    -- 3. Chiều cao lớn nhất (Max Height) theo vị trí
    MEMBER [Measures].[Max Height Cm] AS
        MAX(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

    -- 4. Chiều cao nhỏ nhất (Min Height) theo vị trí
    MEMBER [Measures].[Min Height Cm] AS
        MIN(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        ),
        FORMAT_STRING = "#,##0"

SELECT
    -- Trục Cột: Các chỉ số thống kê thể hình và kết quả thi đấu
    {
        [Measures].[Avg Height Cm],
        [Measures].[Max Height Cm],
        [Measures].[Min Height Cm],
        [Measures].[Goals],
        [Measures].[Yellow Cards]
    } ON COLUMNS,

    -- Trục Dòng: Các vị trí chính hợp lệ, sắp xếp theo số bàn thắng giảm dần
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].[Missing], [DIM Player].[Main Position].[All] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
"""

rs = win32com.client.Dispatch("ADODB.Recordset")
rs.Open(mdx, conn)
fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
print(' | '.join(fields))
while not rs.EOF:
    row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    print(' | '.join(row))
    rs.MoveNext()
rs.Close()
conn.Close()
