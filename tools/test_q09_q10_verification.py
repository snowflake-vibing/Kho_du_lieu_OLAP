# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. CHECK SQL TABLES & COLUMNS ===")
sql_conn = win32com.client.Dispatch('ADODB.Connection')
sql_conn.Open('Provider=SQLOLEDB.1;Data Source=DESKTOP-9B88R8P;Integrated Security=SSPI;Initial Catalog=DW_Football_Transfermarkt')

for tname in ['DIM_Time', 'DIM_Club', 'FACT_Player_Match_Perf']:
    rs, _ = sql_conn.Execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}'")
    cols = []
    while not rs.EOF:
        cols.append(f"{rs.Fields(0).Value} ({rs.Fields(1).Value})")
        rs.MoveNext()
    rs.Close()
    print(f"Table {tname}: {', '.join(cols)}")

print("\n=== 2. RUN T-SQL FOR QUERY 09 ===")
q9_sql = """
WITH WeekendTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekend_Goals,
        SUM(f.Yellow_Cards) AS Weekend_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 1
    GROUP BY c.Club_Name
    ORDER BY Weekend_Goals DESC
),
WeekdayTop AS (
    SELECT TOP 30 
        c.Club_Name, 
        SUM(f.Goals) AS Weekday_Goals,
        SUM(f.Yellow_Cards) AS Weekday_Yellow_Cards
    FROM dbo.FACT_Player_Match_Perf f
    JOIN dbo.DIM_Club c ON f.Club_ID = c.Club_ID
    JOIN dbo.DIM_Time t ON f.Time_ID = t.Time_ID
    WHERE t.Is_Weekend = 0
    GROUP BY c.Club_Name
    ORDER BY Weekday_Goals DESC
)
SELECT 
    w.Club_Name,
    w.Weekend_Goals,
    w.Weekend_Yellow_Cards,
    d.Weekday_Goals,
    d.Weekday_Yellow_Cards,
    (w.Weekend_Goals + d.Weekday_Goals) AS Total_Goals
FROM WeekendTop w
INNER JOIN WeekdayTop d ON w.Club_Name = d.Club_Name
ORDER BY Total_Goals DESC;
"""

try:
    rs, _ = sql_conn.Execute(q9_sql)
    print("T-SQL Q09 Results:")
    cnt = 0
    while not rs.EOF:
        cnt += 1
        row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
        print(f"  {cnt}. " + " | ".join(row))
        rs.MoveNext()
    rs.Close()
    print(f"Total T-SQL clubs: {cnt}")
except Exception as e:
    print("SQL Error:", e)

sql_conn.Close()

print("\n=== 3. RUN SSAS MDX FOR QUERY 09 ===")
as_conn = win32com.client.Dispatch('ADODB.Connection')
as_conn.Open('Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;')

q9_mdx = """
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

rs, _ = as_conn.Execute(q9_mdx)
print("MDX Q09 Results:")
cnt = 0
while not rs.EOF:
    cnt += 1
    row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    print(f"  {cnt}. " + " | ".join(row))
    rs.MoveNext()
rs.Close()
print(f"Total MDX clubs: {cnt}")

as_conn.Close()
