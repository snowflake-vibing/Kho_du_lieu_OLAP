# -*- coding: utf-8 -*-
import sys
import win32com.client

sys.stdout.reconfigure(encoding='utf-8')

def run_query_07():
    conn = win32com.client.Dispatch("ADODB.Connection")
    conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")
    
    mdx_query = """
    WITH 
        MEMBER [Measures].[Pct Of England Goals] AS
            IIF(
                IsEmpty(([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All])) 
                OR ([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All]) = 0,
                NULL,
                [Measures].[Goals] / ([Measures].[Goals], [DIM Player].[Country Of Citizenship].[All])
            ),
            FORMAT_STRING = "0.00%"

    SELECT
        {
            [Measures].[Goals],
            [Measures].[Pct Of England Goals]
        } ON COLUMNS,

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
    WHERE (
        [DIM Competition].[Country Name].[England]
    );
    """
    
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(mdx_query, conn)
    
    print("=" * 80)
    print("MDX QUERY 07: THỐNG KÊ BÀN THẮNG THEO QUỐC TỊCH (PARETO 80% GIẢI ĐẤU Ở ANH)")
    print("=" * 80)
    print(f"{'STT':<4} | {'Quốc Tịch (Country Of Citizenship)':<25} | {'Tổng Bàn Thắng (Goals)':>22} | {'Tỷ Lệ Đóng Góp (%)':>20}")
    print("-" * 80)
    
    count = 0
    total_goals = 0
    while not rs.EOF:
        count += 1
        country = str(rs.Fields(0).Value)
        goals_val = rs.Fields(1).Value
        pct_val = rs.Fields(2).Value
        
        goals_str = f"{int(goals_val):,}" if goals_val is not None else "-"
        pct_str = f"{float(pct_val)*100:.2f}%" if pct_val is not None else "-"
        
        if goals_val is not None:
            total_goals += int(goals_val)
            
        print(f"{count:<4} | {country:<25} | {goals_str:>22} | {pct_str:>20}")
        rs.MoveNext()
        
    print("-" * 80)
    print(f"Tổng cộng {count} quốc gia chiếm {total_goals} bàn thắng (trên tổng số 2.236 bàn).")
    rs.Close()
    conn.Close()

if __name__ == '__main__':
    run_query_07()
