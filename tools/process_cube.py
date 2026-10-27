# -*- coding: utf-8 -*-
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

xmla = """<Process xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Type>ProcessDefault</Type>
  <Object>
    <DatabaseID>SSAS_Football_Transfermarkt</DatabaseID>
    <CubeID>DW Football Transfermarkt</CubeID>
  </Object>
</Process>"""

try:
    cmd = win32com.client.Dispatch("ADODB.Command")
    cmd.ActiveConnection = conn
    cmd.CommandText = xmla
    cmd.Execute()
    print("ProcessDefault on Cube SUCCEEDED!")
except Exception as e:
    print("ProcessDefault Error:", e)

conn.Close()
