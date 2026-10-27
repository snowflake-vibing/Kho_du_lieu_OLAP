# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

print("=== CHECKING SEASONS AND COMPETITIONS IN SSAS ===")
rs = win32com.client.Dispatch("ADODB.Recordset")
rs.Open("SELECT [DIM Time].[Season].[Season].MEMBERS ON ROWS, [Measures].[Goals] ON COLUMNS FROM [DW Football Transfermarkt]", conn)
while not rs.EOF:
    print("Season:", repr(rs.Fields(0).Value), rs.Fields(1).Value)
    rs.MoveNext()
rs.Close()

rs.Open("SELECT [DIM Competition].[Competition ID].[Competition ID].MEMBERS ON ROWS, [Measures].[Goals] ON COLUMNS FROM [DW Football Transfermarkt]", conn)
while not rs.EOF:
    print("Comp ID:", repr(rs.Fields(0).Value), rs.Fields(1).Value)
    rs.MoveNext()
rs.Close()

conn.Close()
