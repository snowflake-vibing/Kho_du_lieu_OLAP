# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

def run_mdx(query):
    print("--- MDX ---")
    print(query)
    rs = win32com.client.Dispatch("ADODB.Recordset")
    rs.Open(query, conn)
    fields = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
    print('Columns:', fields)
    while not rs.EOF:
        row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
        print('Row:', ' | '.join(row))
        rs.MoveNext()
    rs.Close()

run_mdx("SELECT [DIM Player].[Main Position].[Main Position].MEMBERS ON ROWS, [Measures].[Goals] ON COLUMNS FROM [DW Football Transfermarkt]")
conn.Close()
