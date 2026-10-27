# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=DW_Football_Transfermarkt;Integrated Security=SSPI;TrustServerCertificate=True;")

rs = win32com.client.Dispatch("ADODB.Recordset")
rs.Open("""
SELECT 
    p.main_position,
    ROUND(AVG(CAST(p.height_in_cm AS FLOAT)), 1) AS Avg_Height_Cm,
    MAX(p.height_in_cm) AS Max_Height_Cm,
    MIN(p.height_in_cm) AS Min_Height_Cm,
    SUM(f.goals) AS Total_Goals,
    SUM(f.yellow_cards) AS Total_Yellow_Cards
FROM dbo.FACT_Player_Match_Perf f
JOIN dbo.DIM_Player p ON f.player_sk = p.player_sk
WHERE p.main_position IS NOT NULL AND p.height_in_cm > 0
GROUP BY p.main_position
ORDER BY Total_Goals DESC;
""", conn)

print("SQL Query Result:")
fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
print(' | '.join(fields))
while not rs.EOF:
    row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    print(' | '.join(row))
    rs.MoveNext()
rs.Close()
conn.Close()
