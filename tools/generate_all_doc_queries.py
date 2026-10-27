import re, glob, os

def generate_doc_query(query_file, doc_file, q_num):
    with open(query_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title
    title_m = re.search(r'^#\s+MDX Query \d+:\s*(.+)$', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else ''

    # Noi dung
    nd_m = re.search(r'\*\s+\*\*Nội dung truy vấn:\*\*\s*(.+?)(?=\n\s*\*|\n##|\Z)', content, re.DOTALL)
    noi_dung = nd_m.group(1).strip() if nd_m else ''
    noi_dung = ' '.join(noi_dung.split())

    # 2.1
    s21_m = re.search(r'### 2\.1\..+?\n(.*?)(?=### 2\.2\.)', content, re.DOTALL)
    s21_raw = s21_m.group(1).strip() if s21_m else ''
    b1_21 = re.search(r'(####?\s+Bước 1:.*)', s21_raw, re.DOTALL)
    s21_steps = b1_21.group(1).strip() if b1_21 else s21_raw
    s21_steps = re.sub(r'^####\s+', '### ', s21_steps, flags=re.MULTILINE)

    # 2.2
    s22_m = re.search(r'### 2\.2\..+?\n(.*?)(?=### 2\.3\.)', content, re.DOTALL)
    s22_raw = s22_m.group(1).strip() if s22_m else ''
    b1_22 = re.search(r'(####?\s+Bước 1:.*)', s22_raw, re.DOTALL)
    s22_steps = b1_22.group(1).strip() if b1_22 else s22_raw
    s22_steps = re.sub(r'^####\s+', '### ', s22_steps, flags=re.MULTILINE)

    # 2.3
    s23_m = re.search(r'### 2\.3\..+?\n(.*?)(?=### 2\.4\.)', content, re.DOTALL)
    s23_raw = s23_m.group(1).strip() if s23_m else ''
    b1_23 = re.search(r'(####?\s+Bước 1:.*)', s23_raw, re.DOTALL)
    s23_steps = b1_23.group(1).strip() if b1_23 else s23_raw
    s23_steps = re.sub(r'^####\s+', '### ', s23_steps, flags=re.MULTILINE)

    output = f'''# 3.10.{q_num} Câu truy vấn {q_num}: {title}

**Nội dung truy vấn:** {noi_dung}

## 3.10.{q_num}.1 Sử dụng Cube Browser

{s21_steps}

---

## 3.10.{q_num}.2 Sử dụng Pivot Excel

{s22_steps}

---

## 3.10.{q_num}.3 Sử dụng ngôn ngữ MDX

{s23_steps}

---

## 3.10.{q_num}.4 Nhận xét

Cả 3 cách (duyệt cube trong SSAS, dùng PivotTable trong Excel, và viết truy vấn MDX) đều trả về cùng một kết quả dữ liệu chính xác.
'''
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f'Generated {doc_file} successfully!')

if __name__ == '__main__':
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
        generate_doc_query(q, d, n)
