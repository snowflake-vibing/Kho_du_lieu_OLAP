# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')

mdx = """
WITH 
    SET [Top_Weekend_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[1])
        )

    SET [Top_Weekday_Clubs] AS
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
            ),
            30,
            ([Measures].[Goals], [DIM Time].[Is Weekend].[0])
        )

    SET [Elite_Clubs_All_Days] AS
        INTERSECT([Top_Weekend_Clubs], [Top_Weekday_Clubs])

SELECT
    CrossJoin(
        { [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] },
        { [Measures].[Goals], [Measures].[Yellow Cards] }
    ) ON COLUMNS,

    ORDER(
        [Elite_Clubs_All_Days],
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
"""

rs = win32com.client.Dispatch('ADODB.Recordset')
rs.Open(mdx, conn)
cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
print(' | '.join(cols))
rows = []
while not rs.EOF:
    row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    rows.append(row)
    rs.MoveNext()
rs.Close()
conn.Close()

print(f"Total clubs returned by INTERSECT: {len(rows)}")
for r in rows:
    print(' | '.join(r))
