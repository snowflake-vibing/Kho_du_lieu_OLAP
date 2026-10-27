# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')
with open('do_an/SSAS_Football_Transfermarkt/DW Football Transfermarkt.dsv', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<xs:element name="dbo_DIM_Player".*?</xs:element>', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
