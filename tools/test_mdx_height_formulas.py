# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

def test_formula(desc, mdx):
    print(f"\n=== TESTING: {desc} ===")
    try:
        rs = win32com.client.Dispatch("ADODB.Recordset")
        rs.Open(mdx, conn)
        fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
        print(' | '.join(fields))
        while not rs.EOF:
            row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
            print(' | '.join(row))
            rs.MoveNext()
        rs.Close()
    except Exception as e:
        print("Error:", e)

# Test 1: CrossJoin with MEMBER_VALUE
test_formula("CrossJoin Player Name and Height with MEMBER_VALUE", """
WITH 
    SET [ValidPlayers] AS
        NONEMPTY(
            EXISTING CrossJoin(
                [DIM Player].[Player Name].[Player Name].MEMBERS,
                EXCEPT([DIM Player].[Height In Cm].[Height In Cm].MEMBERS, {[DIM Player].[Height In Cm].[0], [DIM Player].[Height In Cm].[All]})
            ),
            [Measures].[FACT Player Match Perf Count]
        )
    MEMBER [Measures].[AvgH] AS
        ROUND(
            AVG(
                [ValidPlayers],
                [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
            ),
            1
        )
    MEMBER [Measures].[MaxH] AS
        MAX(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        )
    MEMBER [Measures].[MinH] AS
        MIN(
            [ValidPlayers],
            [DIM Player].[Height In Cm].CURRENTMEMBER.MEMBER_VALUE
        )
SELECT 
    {[Measures].[AvgH], [Measures].[MaxH], [Measures].[MinH], [Measures].[Goals], [Measures].[Yellow Cards]} ON COLUMNS,
    EXCEPT([DIM Player].[Main Position].[Main Position].MEMBERS, {[DIM Player].[Main Position].[Missing], [DIM Player].[Main Position].[All]}) ON ROWS
FROM [DW Football Transfermarkt]
""")

conn.Close()
