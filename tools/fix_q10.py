# -*- coding: utf-8 -*-
import re

with open('mdx/query_10.md', 'r', encoding='utf-8') as f:
    text = f.read()

s3_10 = """| Câu Lạc Bộ Đối Thủ (`Opponent Club`) | Q1 Bàn Thắng | Q1 QoQ % | Q2 Bàn Thắng | Q2 QoQ % | Q3 Bàn Thắng | Q3 QoQ % | Q4 Bàn Thắng | Q4 QoQ % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **UD Almería** | - | - | 4 | - | 3 | -25.00% | - | -100.00% |
| **CA Osasuna** | 2 | +100.00% | - | -100.00% | - | - | 4 | - |
| **Cádiz CF** | - | -100.00% | 2 | - | - | -100.00% | 3 | - |
| **Girona FC** | - | -100.00% | 2 | - | 3 | +50.00% | - | -100.00% |
| **Villarreal CF** | 1 | - | 1 | 0.00% | - | -100.00% | 4 | - |
| **Celta de Vigo** | - | - | 2 | - | 1 | -50.00% | - | -100.00% |
| **Valencia CF** | 2 | - | 0 | -100.00% | - | - | 5 | - |
| **Real Valladolid CF** | - | -100.00% | 6 | - | - | -100.00% | - | - |
| **Athletic Bilbao** | 2 | - | 1 | -50.00% | 2 | +100.00% | - | -100.00% |
| **FC Barcelona** | 0 | -100.00% | - | - | - | - | 2 | - |"""

text = re.sub(r'\| Câu Lạc Bộ Đối Thủ.*?\n(?=\n> \*Ghi chú|\n---|\n## 4|\Z)', s3_10 + '\n', text, flags=re.DOTALL)

with open('mdx/query_10.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated query_10.md Section 3 successfully!")
