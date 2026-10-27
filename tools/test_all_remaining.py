# -*- coding: utf-8 -*-
import sys, win32com.client, re

sys.stdout.reconfigure(encoding='utf-8')

conn_ssas = win32com.client.Dispatch("ADODB.Connection")
conn_ssas.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

conn_sql = win32com.client.Dispatch("ADODB.Connection")
conn_sql.Open("Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=DW_Football_Transfermarkt;Integrated Security=SSPI;TrustServerCertificate=True;")

def test_query(q_num):
    print(f"\n=================================================================")
    print(f"                       QUERY {q_num}                             ")
    print(f"=================================================================")
    filepath = f"mdx/query_{q_num}.md"
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract MDX
    m_mdx = re.search(r'```mdx\s*(?:/\*.*?\*/\s*)?(WITH.*?|SELECT.*?FROM\s+\[DW Football Transfermarkt\].*?;)', text, re.DOTALL | re.IGNORECASE)
    if not m_mdx:
        # try without semicolon
        m_mdx = re.search(r'```mdx\s*(?:/\*.*?\*/\s*)?(WITH.*?|SELECT.*?FROM\s+\[DW Football Transfermarkt\].*?)(?=```)', text, re.DOTALL | re.IGNORECASE)
    
    if m_mdx:
        mdx_code = m_mdx.group(1).strip()
        print("--- MDX QUERY ---")
        try:
            rs = win32com.client.Dispatch("ADODB.Recordset")
            rs.Open(mdx_code, conn_ssas)
            cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
            print("SSAS Columns:", cols)
            rows = []
            while not rs.EOF and len(rows) < 15:
                row = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
                rows.append(row)
                rs.MoveNext()
            rs.Close()
            print(f"SSAS Rows returned (showing first {len(rows)}):")
            for r in rows:
                print("  ", " | ".join(r))
        except Exception as e:
            print("SSAS ERROR:", e)
    else:
        print("Could not extract MDX code!")

    # Extract T-SQL
    m_sql = re.search(r'```sql\s*(USE.*?;)?\s*(WITH.*?|SELECT.*?)(?=```)', text, re.DOTALL | re.IGNORECASE)
    if m_sql:
        sql_code = m_sql.group(2).strip()
        # adjust database name or schema if needed
        print("--- T-SQL QUERY ---")
        try:
            rs_sql = win32com.client.Dispatch("ADODB.Recordset")
            rs_sql.Open(sql_code, conn_sql)
            cols_sql = [rs_sql.Fields(i).Name for i in range(rs_sql.Fields.Count)]
            print("SQL Columns:", cols_sql)
            rows_sql = []
            while not rs_sql.EOF and len(rows_sql) < 15:
                row = [str(rs_sql.Fields(i).Value) for i in range(rs_sql.Fields.Count)]
                rows_sql.append(row)
                rs_sql.MoveNext()
            rs_sql.Close()
            print(f"SQL Rows returned (showing first {len(rows_sql)}):")
            for r in rows_sql:
                print("  ", " | ".join(r))
        except Exception as e:
            print("SQL ERROR:", e)

for q in ['01', '03', '04', '05', '09', '10', '11', '12']:
    test_query(q)

conn_ssas.Close()
conn_sql.Close()
