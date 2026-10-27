# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

for q in ['06', '07', '09', '10', '11']:
    print(f'=== DETAILS QUERY {q} ===')
    with open(f'mdx/query_{q}.md', 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 2.1
    s21 = re.search(r'### 2\.1\.(.*?)(?=### 2\.2\.)', c, re.DOTALL).group(1)
    # Check if Calculations tab mentioned
    if 'Calculations' in s21:
        calc_m = re.findall(r'Name:\s*`([^`]+)`', s21)
        print('  2.1 Calculated Members:', calc_m)
    
    # 2.1 Grid measures
    grid_m = re.search(r'Kéo.*?(?:Thước đo|Measures).*?\n(.*?)(?=####? Bước|\Z)', s21, re.DOTALL)
    if grid_m:
        print('  2.1 Grid Measures lines:', [l.strip() for l in grid_m.group(1).split('\n') if l.strip().startswith(('*', '1.', '2.', '3.', '-'))])

    # 2.2 Pivot Values
    s22 = re.search(r'### 2\.2\.(.*?)(?=### 2\.3\.)', c, re.DOTALL).group(1)
    val_lines = [l.strip() for l in s22.split('\n') if 'Values' in l]
    print('  2.2 Pivot Values:', val_lines)

    # 2.3 MDX WITH MEMBER and ON COLUMNS
    s23 = re.search(r'### 2\.3\.(.*?)(?=### 2\.4\.)', c, re.DOTALL).group(1)
    with_members = re.findall(r'WITH\s+MEMBER\s+\[Measures\]\.\[([^\]]+)\]', s23, re.IGNORECASE)
    print('  2.3 MDX WITH MEMBERS:', with_members)
    col_m = re.search(r'\{([^}]+)\}\s+ON\s+COLUMNS', s23, re.IGNORECASE | re.DOTALL)
    if col_m:
        print('  2.3 MDX Columns:', [x.strip() for x in col_m.group(1).split(',') if x.strip()])
    print()
