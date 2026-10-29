# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx_query_10 = """
WITH 
    MEMBER [Measures].[QoQ Goals Growth] AS
        IIF(
            [DIM Time].[Hierarchy].CURRENTMEMBER.LEVEL IS [DIM Time].[Hierarchy].[Quarter]
            AND [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER.PARENT IS [DIM Time].[Hierarchy].CURRENTMEMBER.PARENT
            AND NOT ISEMPTY(([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
            AND ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER) <> 0,
            ([Measures].[Goals] - ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER))
                / ([Measures].[Goals], [DIM Time].[Hierarchy].CURRENTMEMBER.PREVMEMBER),
            NULL
        ),
        FORMAT_STRING = "0.00%"

SELECT
    {
        ([DIM Time].[Hierarchy].[Year].[2023].[1], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[2], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[3], [Measures].[QoQ Goals Growth]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[Goals]),
        ([DIM Time].[Hierarchy].[Year].[2023].[4], [Measures].[QoQ Goals Growth])
    } ON COLUMNS,

    TOPCOUNT(
        NONEMPTY(
            EXCEPT([DIM Club].[Club Name].[Club Name].MEMBERS, { [DIM Club].[Club Name].[All] }),
            ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
        ),
        10,
        ([Measures].[Goals], [DIM Time].[Hierarchy].[Year].[2023])
    ) ON ROWS

FROM [DW Football Transfermarkt];
"""

print("==============================================================================================================")
print("MDX QUERY 10: TĂNG TRƯỞNG BÀN THẮNG THEO QUÝ (QOQ) CỦA TOP 10 CLB HÀNG ĐẦU CHÂU ÂU NĂM 2023")
print("==============================================================================================================")

try:
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query_10, conn)
    header = f"{'STT':<4} | {'Câu Lạc Bộ':<24} | {'Q1 Goals':>8} | {'Q2 Goals':>8} | {'Q2 QoQ':>9} | {'Q3 Goals':>8} | {'Q3 QoQ':>9} | {'Q4 Goals':>8} | {'Q4 QoQ':>9}"
    print(header)
    print("-" * len(header))
    stt = 0
    while not rs.EOF:
        stt += 1
        club = str(rs.Fields(0).Value)
        q1_g = int(rs.Fields(1).Value) if rs.Fields(1).Value is not None else 0
        q2_g = int(rs.Fields(2).Value) if rs.Fields(2).Value is not None else 0
        q2_q = f"{rs.Fields(3).Value*100:+.2f}%" if rs.Fields(3).Value is not None else "NULL"
        q3_g = int(rs.Fields(4).Value) if rs.Fields(4).Value is not None else 0
        q3_q = f"{rs.Fields(5).Value*100:+.2f}%" if rs.Fields(5).Value is not None else "NULL"
        q4_g = int(rs.Fields(6).Value) if rs.Fields(6).Value is not None else 0
        q4_q = f"{rs.Fields(7).Value*100:+.2f}%" if rs.Fields(7).Value is not None else "NULL"
        
        print(f"{stt:<4} | {club:<24} | {q1_g:>8} | {q2_g:>8} | {q2_q:>9} | {q3_g:>8} | {q3_q:>9} | {q4_g:>8} | {q4_q:>9}")
        rs.MoveNext()
    rs.Close()
except Exception as e:
    print("Error Query 10:", e)

conn.Close()
