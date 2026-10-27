# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

mdx_query = """
WITH 
    -- 1. Tổng số bàn thắng của toàn bộ giải đấu tại Anh
    MEMBER [Measures].[England Total Goals] AS
        (
            [Measures].[Goals],
            [DIM Player].[Country Of Citizenship].[All],
            [DIM Competition].[Country Name].[England]
        )

    -- 2. Tỷ lệ phần trăm đóng góp bàn thắng của từng quốc gia
    MEMBER [Measures].[Pct Of England Goals] AS
        IIF(
            ISEMPTY([Measures].[England Total Goals]) OR [Measures].[England Total Goals] = 0,
            NULL,
            ROUND(([Measures].[Goals] / [Measures].[England Total Goals]) * 100, 2)
        ),
        FORMAT_STRING = "0.00%"

SELECT
    -- Trục Cột: Tổng số bàn thắng và Tỷ lệ phần trăm đóng góp
    {
        [Measures].[Goals],
        [Measures].[Pct Of England Goals]
    } ON COLUMNS,

    -- Trục Dòng: Các quốc gia chiếm 80% tổng số bàn thắng, xếp giảm dần
    ORDER(
        TOPPERCENT(
            NONEMPTY(
                EXCEPT(
                    [DIM Player].[Country Of Citizenship].[Country Of Citizenship].MEMBERS,
                    { [DIM Player].[Country Of Citizenship].[All] }
                ),
                (
                    [Measures].[Goals],
                    [DIM Competition].[Country Name].[England]
                )
            ),
            80,
            [Measures].[Goals]
        ),
        [Measures].[Goals],
        BDESC
    ) ON ROWS

FROM [DW Football Transfermarkt]

-- Lát cắt ngữ cảnh: Các giải đấu diễn ra tại Nước Anh
WHERE (
    [DIM Competition].[Country Name].[England]
)
"""

try:
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query, conn)
    fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
    print(' | '.join(fields))
    count = 0
    while not rs.EOF:
        count += 1
        row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
        print(f'{count}.', ' | '.join(row))
        rs.MoveNext()
    rs.Close()
except Exception as e:
    print("SSAS Error:", e)

conn.Close()
