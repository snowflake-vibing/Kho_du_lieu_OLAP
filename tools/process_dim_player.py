# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

xmla = """<Process xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Type>ProcessFull</Type>
  <Object>
    <DatabaseID>SSAS_Football_Transfermarkt</DatabaseID>
    <DimensionID>DIM Player</DimensionID>
  </Object>
</Process>"""

try:
    cmd = win32com.client.Dispatch("ADODB.Command")
    cmd.ActiveConnection = conn
    cmd.CommandText = xmla
    cmd.Execute()
    print("ProcessFull on DIM Player SUCCEEDED!")
except Exception as e:
    print("ProcessFull Error:", e)

conn.Close()
