# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')

def test(name, mdx):
    print(f"\n==================== {name} ====================")
    try:
        rs = win32com.client.Dispatch('ADODB.Recordset')
        rs.Open(mdx, conn)
        cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
        print(' | '.join(cols))
        count = 0
        while not rs.EOF and count < 10:
            row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
            print(' | '.join(row))
            rs.MoveNext()
            count += 1
        rs.Close()
        print(f"Success! Previewed {count} rows.")
    except Exception as e:
        print("ERROR:", e)

# 1. Test Query 05 Fixed
test("QUERY 05 FIXED", """
SELECT
    { [Measures].[Goals] } ON COLUMNS,

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

FROM [DW Football Transfermarkt];
""")

# 2. Test Query 10 Fixed
test("QUERY 10 FIXED", """
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
);
""")

# 3. Test Query 11 Fixed
test("QUERY 11 FIXED", """
WITH 
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

    MEMBER [Measures].[Stadium Capacity Cleaned] AS
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
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
        [ValidStadiums],
        [DIM Club].[Stadium Seats].CURRENTMEMBER.MEMBER_VALUE,
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt];
""")

# 4. Test Query 12 Fixed (filter out Unknown Coach)
test("QUERY 12 FIXED", """
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
                AND [DIM Club].[Coach Name].CURRENTMEMBER.NAME <> "Unknown Coach"
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

FROM [DW Football Transfermarkt];
""")

conn.Close()
