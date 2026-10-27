# -*- coding: utf-8 -*-
import sys, re, glob

sys.stdout.reconfigure(encoding='utf-8')

for q_num in ['01', '03', '04', '05', '06', '07', '09', '10', '11', '12']:
    filepath = f'mdx/query_{q_num}.md'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'============================== QUERY {q_num} ==============================')
    
    # 1. Title
    title_m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    print('TITLE:', title_m.group(1) if title_m else '')

    # 2. Section 3 Table header
    s3_idx = content.find('## 3.')
    if s3_idx != -1:
        s3_part = content[s3_idx:s3_idx+500]
        tbl_lines = [l for l in s3_part.split('\n') if l.strip().startswith('|')]
        if tbl_lines:
            print('S3 COLUMNS:', tbl_lines[0].strip())
    
    # 3. MDX query SELECT
    mdx_blocks = re.findall(r'```mdx\s*(SELECT.*?)```', content, re.DOTALL | re.IGNORECASE)
    if not mdx_blocks:
        mdx_blocks = re.findall(r'```mdx\s*(WITH.*?)```', content, re.DOTALL | re.IGNORECASE)
    if mdx_blocks:
        code = mdx_blocks[0]
        # find ON COLUMNS
        cols = re.findall(r'\{([^}]+)\}\s+ON\s+COLUMNS', code, re.IGNORECASE | re.DOTALL)
        if cols:
            print('MDX COLUMNS:', ' '.join(cols[0].split()))
        else:
            print('MDX COLUMNS: (complex or crossjoin in code)')
    
    # 4. Check 2.1 Drag Steps
    s21_m = re.search(r'### 2\.1\..*?(?=### 2\.2\.)', content, re.DOTALL)
    if s21_m:
        step4_m = re.search(r'Bước \d+: Kéo thả.*?\n(.*?)(?=####? Bước|\Z)', s21_m.group(0), re.DOTALL)
        if step4_m:
            lines = [l.strip() for l in step4_m.group(1).split('\n') if l.strip().startswith(('*', '1.', '2.', '3.', '-'))]
            print('2.1 DRAG STEPS:')
            for l in lines[:6]:
                print('   ', l)
    
    # 5. Check 2.2 Fields Table
    s22_m = re.search(r'### 2\.2\..*?(?=### 2\.3\.)', content, re.DOTALL)
    if s22_m:
        step3_m = re.search(r'Bước \d+: Thao tác kéo thả.*?\n(.*?)(?=####? Bước|\Z)', s22_m.group(0), re.DOTALL)
        if step3_m:
            lines = [l.strip() for l in step3_m.group(1).split('\n') if l.strip().startswith('|')]
            print('2.2 PIVOT FIELDS TABLE:')
            for l in lines[:6]:
                print('   ', l)
    print()
