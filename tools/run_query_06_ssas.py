# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx_query = """
WITH 
    -- 1. Chiều cao trung bình theo ngữ cảnh vị trí hiện tại
    MEMBER [Measures].[Avg Height Cm] AS
        ROUND(
            AVG(
                FILTER(
                    EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                    NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
                    AND [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE > 0
                ),
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
            ),
            1
        ),
        FORMAT_STRING = "#,##0.0"

    -- 2. Chiều cao lớn nhất (Max Height) theo vị trí
    MEMBER [Measures].[Max Height Cm] AS
        MAX(
            FILTER(
                EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
            ),
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
        ),
        FORMAT_STRING = "#,##0"

    -- 3. Chiều cao nhỏ nhất (Min Height) theo vị trí
    MEMBER [Measures].[Min Height Cm] AS
        MIN(
            FILTER(
                EXISTING [DIM Player].[Player Name].[Player Name].MEMBERS,
                NOT ISEMPTY([DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE)
                AND [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE > 0
            ),
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBERVALUE
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

    -- Trục Dòng: Các vị trí chính, sắp xếp theo số bàn thắng giảm dần
    ORDER(
        EXCEPT(
            [DIM Player].[Main Position].[Main Position].MEMBERS,
            { [DIM Player].[Main Position].[All] }
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]
"""

try:
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query, conn)
    print("Recordset opened!")
    fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
    print('Columns:', fields)
    while not rs.EOF:
        row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
        print('Row:', ' | '.join(row))
        rs.MoveNext()
    rs.Close()
except Exception as e:
    print("SSAS Error:", e)
conn.Close()
