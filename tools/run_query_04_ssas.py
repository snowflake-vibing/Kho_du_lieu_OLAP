# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx_query_04 = """
WITH 
    MEMBER [Measures].[Avg Minutes Played] AS
        IIF(
            IsEmpty([Measures].[FACT Player Match Perf Count]) OR [Measures].[FACT Player Match Perf Count] = 0,
            NULL,
            ROUND([Measures].[Minutes Played] / [Measures].[FACT Player Match Perf Count], 2)
        ),
        FORMAT_STRING = "#,##0.00"

SELECT
    {
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
);
"""

print("==============================================================================================================")
print("MDX QUERY 04: BÀN THẮNG, KIẾN TẠO & SỐ PHÚT THI ĐẤU TRUNG BÌNH THEO ĐỘ TUỔI NĂM 2023")
print("==============================================================================================================")

try:
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query_04, conn)
    header = f"{'STT':<4} | {'Độ Tuổi (Age)':<14} | {'Tổng Bàn Thắng':>16} | {'Tổng Kiến Tạo':>16} | {'Số Phút TB/Trận':>18}"
    print(header)
    print("-" * len(header))
    stt = 0
    while not rs.EOF:
        stt += 1
        age = str(rs.Fields(0).Value)
        goals = f"{int(rs.Fields(1).Value):,}" if rs.Fields(1).Value is not None else "-"
        assists = f"{int(rs.Fields(2).Value):,}" if rs.Fields(2).Value is not None else "-"
        avg_min = f"{float(rs.Fields(3).Value):.2f}" if rs.Fields(3).Value is not None else "-"
        
        print(f"{stt:<4} | {age:<14} | {goals:>16} | {assists:>16} | {avg_min:>18}")
        rs.MoveNext()
    rs.Close()
except Exception as e:
    print("Error Query 04:", e)

conn.Close()
