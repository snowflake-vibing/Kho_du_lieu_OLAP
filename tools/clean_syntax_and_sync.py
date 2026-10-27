# -*- coding: utf-8 -*-
import glob, re, os

def fix_mangled_arrows(text):
    # Fix $\n\rightarrow$, $\rightarrow$, $\r\rightarrow$, etc.
    # Replace any variant of arrow with unicode '→'
    text = re.sub(r'\$\s*\\?r?ightarrow\s*\$', '→', text)
    text = re.sub(r'\$\s*\n\s*\\?r?ightarrow\s*\$', '→', text)
    text = re.sub(r'\\rightarrow', '→', text)
    text = re.sub(r'\$\s*→\s*\$', '→', text)
    return text

def run():
    md_files = glob.glob('mdx/*.md')
    for f in md_files:
        with open(f, 'r', encoding='utf-8') as fp:
            orig = fp.read()
        cleaned = fix_mangled_arrows(orig)
        if cleaned != orig:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(cleaned)
            print(f'Cleaned arrows in {f}')

    # Now re-generate all doc_query_*.md files to ensure 100% exact alignment
    import generate_all_doc_queries
    mapping = [
        ('mdx/query_01.md', 'mdx/doc_query_01.md', 1),
        ('mdx/query_03.md', 'mdx/doc_query_03.md', 3),
        ('mdx/query_04.md', 'mdx/doc_query_04.md', 4),
        ('mdx/query_05.md', 'mdx/doc_query_05.md', 5),
        ('mdx/query_06.md', 'mdx/doc_query_06.md', 6),
        ('mdx/query_07.md', 'mdx/doc_query_07.md', 7),
        ('mdx/query_09.md', 'mdx/doc_query_09.md', 9),
        ('mdx/query_10.md', 'mdx/doc_query_10.md', 10),
        ('mdx/query_11.md', 'mdx/doc_query_11.md', 11),
        ('mdx/query_12.md', 'mdx/doc_query_12.md', 12),
    ]
    for q, d, n in mapping:
        generate_all_doc_queries.generate_doc_query(q, d, n)
    print('All doc queries regenerated successfully.')

if __name__ == '__main__':
    run()
