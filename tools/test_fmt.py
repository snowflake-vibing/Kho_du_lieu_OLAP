# -*- coding: utf-8 -*-
import win32com.client

conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')

mdx = """
WITH 
    MEMBER [Measures].[England Total Goals] AS
        (
            [Measures].[Goals],
            [DIM Player].[Country Of Citizenship].[All],
            [DIM Competition].[Country Name].[England]
        )
    MEMBER [Measures].[Pct Of England Goals] AS
        IIF(
            ISEMPTY([Measures].[England Total Goals]) OR [Measures].[England Total Goals] = 0,
            NULL,
            [Measures].[Goals] / [Measures].[England Total Goals]
        ),
        FORMAT_STRING = "0.00%"
SELECT
    {[Measures].[Goals], [Measures].[Pct Of England Goals]} ON COLUMNS,
    HEAD(ORDER(TOPPERCENT(NONEMPTY(EXCEPT([DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS, {[DIM Player].[Country Of Citizenship].[All]}), ([Measures].[Goals], [DIM Competition].[Country Name].[England])), 80, [Measures].[Goals]), [Measures].[Goals], BDESC), 3) ON ROWS
FROM [DW Football Transfermarkt]
WHERE ([DIM Competition].[Country Name].[England])
"""

rs = win32com.client.Dispatch('ADODB.Recordset')
rs.Open(mdx, conn)
while not rs.EOF:
    print(rs.Fields(0).Value, '|', rs.Fields(1).Value, '|', rs.Fields(2).Value)
    rs.MoveNext()
rs.Close()
conn.Close()
