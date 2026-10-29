# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx_query_11 = """
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
"""

print("==============================================================================================================")
print("MDX QUERY 11: THỐNG KÊ SÂN VẬN ĐỘNG CÓ SỨC CHỨA TRÊN 60.000 CHỖ NGỒI (SỨC CHỨA, SỐ TRẬN, BÀN THẮNG)")
print("==============================================================================================================")

try:
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query_11, conn)
    header = f"{'STT':<4} | {'Sân Vận Động':<28} | {'CLB Chủ Quản':<30} | {'Sức Chứa':>14} | {'Số Trận':>8} | {'Bàn Thắng':>10}"
    print(header)
    print("-" * len(header))
    stt = 0
    while not rs.EOF:
        stt += 1
        stadium = str(rs.Fields(0).Value)
        club = str(rs.Fields(1).Value)
        # In CrossJoin order: fields might be stadium, club, seats or measures
        # Let's inspect fields
        capacity = f"{int(rs.Fields(3).Value):,} Chỗ" if rs.Fields(3).Value is not None else "0 Chỗ"
        matches = int(rs.Fields(4).Value) if rs.Fields(4).Value is not None else 0
        goals = int(rs.Fields(5).Value) if rs.Fields(5).Value is not None else 0
        
        print(f"{stt:<4} | {stadium:<28} | {club:<30} | {capacity:>14} | {matches:>8} | {goals:>10}")
        rs.MoveNext()
    rs.Close()
except Exception as e:
    print("Error Query 11:", e)

conn.Close()
