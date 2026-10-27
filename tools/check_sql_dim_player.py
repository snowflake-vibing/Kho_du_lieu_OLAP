# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
# Try connecting to SQL Server
try:
    conn.Open("Provider=SQLOLEDB;Data Source=localhost;Initial Catalog=DW_Football_Transfermarkt;Integrated Security=SSPI;")
    print("Connected to SQL Server DW_Football_Transfermarkt!")
except Exception as e:
    print("Failed to connect to DW_Football_Transfermarkt:", e)
    try:
        conn.Open("Provider=SQLOLEDB;Data Source=localhost;Initial Catalog=DW_Football_Analytics;Integrated Security=SSPI;")
        print("Connected to SQL Server DW_Football_Analytics!")
    except Exception as e2:
        print("Failed to connect to DW_Football_Analytics:", e2)

rs = win32com.client.Dispatch("ADODB.Recordset")
rs.Open("SELECT DISTINCT main_position FROM dbo.DIM_Player", conn)
while not rs.EOF:
    print('main_position:', repr(rs.Fields(0).Value))
    rs.MoveNext()
rs.Close()

rs.Open("SELECT TOP 5 player_name, main_position, sub_position, height_in_cm FROM dbo.DIM_Player", conn)
while not rs.EOF:
    print('Sample:', [rs.Fields(i).Value for i in range(rs.Fields.Count)])
    rs.MoveNext()
rs.Close()
conn.Close()
