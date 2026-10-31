# -*- coding: utf-8 -*-
import sys
import win32com.client

sys.stdout.reconfigure(encoding='utf-8')

def run_query_09():
    conn = win32com.client.Dispatch("ADODB.Connection")
    conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")
    
    mdx_query = """
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
    
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query, conn)
    
    print("=" * 95)
    print("MDX QUERY 09 (STT 07 BÁO CÁO): GIAO TẬP HỢP INTERSECT TOP 30 CLB CUỐI TUẦN & NGÀY THƯỜNG")
    print("=" * 95)
    print(f"{'STT':<4} | {'Tên Câu Lạc Bộ (Club Name)':<24} | {'Cuối tuần Goals':>15} | {'Cuối tuần Cards':>15} | {'Ngày thường Goals':>17} | {'Ngày thường Cards':>17}")
    print("-" * 95)
    
    count = 0
    while not rs.EOF:
        count += 1
        club = str(rs.Fields(0).Value)
        we_goals = int(rs.Fields(1).Value)
        we_cards = int(rs.Fields(2).Value)
        wd_goals = int(rs.Fields(3).Value)
        wd_cards = int(rs.Fields(4).Value)
        
        print(f"{count:<4} | {club:<24} | {we_goals:>15} | {we_cards:>15} | {wd_goals:>17} | {wd_cards:>17}")
        rs.MoveNext()
        
    print("-" * 95)
    print(f"Tổng cộng {count} câu lạc bộ ưu tú duy trì sức tấn công đỉnh cao ở cả 2 khung thời gian.")
    rs.Close()
    conn.Close()

if __name__ == '__main__':
    run_query_09()
