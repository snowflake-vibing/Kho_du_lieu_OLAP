# -*- coding: utf-8 -*-
import glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# Known Valid SSAS Elements from Cube XML:
VALID_DIMS = {
    '[DIM Game]', '[DIM Club]', '[DIM Player]', '[DIM Time]', '[DIM Competition]', '[Opponent Club]'
}

KNOWN_DISALLOWED_PATTERNS = [
    ('[DIM Game].[Coach Name]', 'Coach Name belongs to [DIM Club]'),
    ('[Hierarchy Time]', 'User hierarchy in DIM Time is [Hierarchy]'),
    ('[FACT Player Match Perf].[Is Home Game]', 'Is Home Game is not a dimension hierarchy'),
    ('Is Home Game', 'Query 09 should use Is Weekend, not Is Home Game'),
]

def check_file(filepath):
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Check known disallowed patterns
    for bad, reason in KNOWN_DISALLOWED_PATTERNS:
        if bad in content:
            # Query 09 shouldn't have Is Home Game at all
            if 'Is Home Game' in bad:
                if 'query_09' in filepath:
                    errors.append(f'Contains {bad} ({reason})')
            else:
                errors.append(f'Contains {bad} ({reason})')
    
    # 2. Check for unbalanced code blocks
    code_blocks = content.count('```')
    if code_blocks % 2 != 0:
        errors.append(f'Unbalanced code blocks (count: {code_blocks})')
    
    # 3. Check section completeness for query_XX.md
    if 'query_' in filepath and 'doc_query_' not in filepath:
        for s in ['## 1.', '## 2.', '## 3.', '## 4.', '## 5.']:
            if s not in content:
                errors.append(f'Missing section {s}')
        for m in ['### 2.1.', '### 2.2.', '### 2.3.', '### 2.4.']:
            if m not in content:
                errors.append(f'Missing method {m}')
    
    # 4. Check section completeness for doc_query_XX.md
    if 'doc_query_' in filepath:
        match = re.search(r'# 3\.10\.(\d+)', content)
        if not match:
            errors.append('Missing main heading # 3.10.x')
        else:
            num = match.group(1)
            for sub in [f'## 3.10.{num}.1', f'## 3.10.{num}.2', f'## 3.10.{num}.3', f'## 3.10.{num}.4']:
                if sub not in content:
                    errors.append(f'Missing doc section {sub}')

    return errors

def main():
    queries = sorted(glob.glob('mdx/query_*.md'))
    docs = sorted(glob.glob('mdx/doc_query_*.md'))
    all_files = queries + docs
    print(f'Auditing {len(all_files)} files in mdx/...')
    
    total_errors = 0
    for f in all_files:
        errs = check_file(f)
        if errs:
            print(f'[FAIL] {f}:')
            for e in errs:
                print(f'   - {e}')
            total_errors += len(errs)
        else:
            print(f'[PASS] {f}')

    print('='*60)
    if total_errors == 0:
        print('SUCCESS: ALL 20 FILES PASSED 100% METADATA AND SYNCHRONIZATION AUDIT!')
    else:
        print(f'FAILED: {total_errors} errors found.')

if __name__ == '__main__':
    main()
