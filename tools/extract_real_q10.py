# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')
mdx = """
WITH 
    MEMBER [Measures].[Prev Quarter Goals] AS
        (
            [Measures].[Goals],
            [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER
        ),
        FORMAT_STRING = "#,##0"

    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            ISEMPTY([Measures].[Prev Quarter Goals]) OR [Measures].[Prev Quarter Goals] = 0,
            NULL,
            ROUND(
                (([Measures].[Goals] - [Measures].[Prev Quarter Goals]) / [Measures].[Prev Quarter Goals]) * 100,
                2
            )
        ),
        FORMAT_STRING = "0.00%"

SELECT
    CrossJoin(
        DESCENDANTS(
            [DIM Time].[Hierarchy].[Year].[2023],
            [DIM Time].[Hierarchy].[Quarter]
        ),
        {
            [Measures].[Goals],
            [Measures].[QoQ Goals Growth]
        }
    ) ON COLUMNS,

    ORDER(
        NONEMPTY(
            EXCEPT([Opponent Club].[Club Name].[Club Name].MEMBERS, { [Opponent Club].[Club Name].[All] }),
            (
                [Measures].[Goals],
                [DIM Club].[Club Name].[Real Madrid]
            )
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]
WHERE (
    [DIM Club].[Club Name].[Real Madrid]
)
"""
rs = win32com.client.Dispatch('ADODB.Recordset')
rs.Open(mdx, conn)
rows = []
while not rs.EOF:
    row = [str(rs.Fields(i).Value) if rs.Fields(i).Value is not None else '-' for i in range(rs.Fields.Count)]
    rows.append(row)
    rs.MoveNext()
rs.Close()
conn.Close()

for r in rows[:12]:
    print(' | '.join(r))
