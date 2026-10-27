# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')
mdx = """
WITH 
    MEMBER [Measures].[Avg Minutes Played] AS
        IIF(
            IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
            NULL,
            ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
        ),
        FORMAT_STRING = "#,##0.00"

    MEMBER [Measures].[Career Stage Group] AS
        CASE 
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 21 THEN "U21 Young Talent"
            WHEN [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE <= 29 THEN "Prime Age (22-29)"
            ELSE "Veteran (30+)"
        END

SELECT
    {
        [Measures].[Career Stage Group],
        [Measures].[Goals],
        [Measures].[Assists],
        [Measures].[Avg Minutes Played]
    } ON COLUMNS,

    ORDER(
        FILTER(
            [DIM Player].[Age].[Age].MEMBERS,
            NOT ISEMPTY([DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE) 
            AND [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE > 0
        ),
        [DIM Player].[Age].CURRENTMEMBER.MEMBERVALUE,
        BASC
    ) ON ROWS

FROM [DW Football Transfermarkt]
WHERE (
    [DIM Time].[Year].[2023]
)
"""
rs = win32com.client.Dispatch('ADODB.Recordset')
rs.Open(mdx, conn)
cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
print(' | '.join(cols))
while not rs.EOF:
    row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    print(' | '.join(row))
    rs.MoveNext()
rs.Close()
conn.Close()
