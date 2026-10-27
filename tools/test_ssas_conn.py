# -*- coding: utf-8 -*-
import sys

try:
    import win32com.client
    conn = win32com.client.Dispatch("ADODB.Connection")
    # Try different catalog names if DW_Football_SSAS doesn't exist
    conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")
    print("Connected to SSAS SSAS_Football_Transfermarkt successfully!")
except Exception as e:
    print("Error connecting to SSAS_Football_Transfermarkt:", e)
    try:
        conn = win32com.client.Dispatch("ADODB.Connection")
        conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=DW_Football_SSAS;")
        print("Connected to DW_Football_SSAS successfully!")
    except Exception as e2:
        print("Error connecting to DW_Football_SSAS:", e2)
