# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')

def run(name, mdx):
    print(f"\n==================== {name} ====================")
    try:
        rs = win32com.client.Dispatch('ADODB.Recordset')
        rs.Open(mdx, conn)
        cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
        print(' | '.join(cols))
        rows = 0
        while not rs.EOF and rows < 10:
            row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
            print(' | '.join(row))
            rs.MoveNext()
            rows += 1
        rs.Close()
        print(f"Total rows previewed: {rows}")
    except Exception as e:
        print("ERROR:", e)

# Query 05
run("QUERY 05", """
SELECT
    {
        [DIM Player].[Foot].[Foot].MEMBERS
    } ON COLUMNS,
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
WHERE ([Measures].[Goals])
""")

# Query 09
run("QUERY 09", """
SELECT
    CrossJoin(
        { [DIM Time].[Is Weekend].[1], [DIM Time].[Is Weekend].[0] },
        { [Measures].[Goals], [Measures].[Yellow Cards] }
    ) ON COLUMNS,

    INTERSECT(
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ( [Measures].[Goals], [DIM Time].[Is Weekend].[1] )
            ),
            30,
            ( [Measures].[Goals], [DIM Time].[Is Weekend].[1] )
        ),
        TOPCOUNT(
            NONEMPTY(
                EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
                ( [Measures].[Goals], [DIM Time].[Is Weekend].[0] )
            ),
            30,
            ( [Measures].[Goals], [DIM Time].[Is Weekend].[0] )
        )
    ) ON ROWS

FROM [DW Football Transfermarkt]
""")

# Query 10
run("QUERY 10", """
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
    [DIM Club].[Club Name].[Real Madrid],
    [DIM Time].[Hierarchy].[Year].[2023]
)
""")

# Query 11
run("QUERY 11", """
WITH 
    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        COALESCEEMPTY(
            [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBERVALUE,
            0
        ),
        FORMAT_STRING = "#,##0 Chỗ"

    MEMBER [Measures].[Distinct Matches Played] AS
        DISTINCTCOUNT(
            EXISTING [DIM Game].[Game ID].[Game ID].MEMBERS
        ),
        FORMAT_STRING = "#,##0"

SELECT
    {
        [Measures].[Stadium Capacity Cleaned],
        [Measures].[Distinct Matches Played],
        [Measures].[Goals]
    } ON COLUMNS,

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

FROM [DW Football Transfermarkt]
""")

# Query 12
run("QUERY 12", """
SELECT
    {
        [Measures].[Yellow Cards],
        [Measures].[Red Cards]
    } ON COLUMNS,

    ORDER(
        GENERATE(
            FILTER(
                NONEMPTY(
                    EXCEPT([DIM Club].[Coach Name].[Coach Name].MEMBERS, { [DIM Club].[Coach Name].[All] }),
                    [Measures].[Yellow Cards]
                ),
                [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown"
            ),
            TOPCOUNT(
                NONEMPTY(
                    CrossJoin(
                        { [DIM Club].[Coach Name].CURRENTMEMBER },
                        EXCEPT([DIM Time].[Month].[Month].MEMBERS, { [DIM Time].[Month].[All] })
                    ),
                    [Measures].[Yellow Cards]
                ),
                1,
                [Measures].[Yellow Cards]
            )
        ),
        [Measures].[Yellow Cards],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]
""")

conn.Close()
