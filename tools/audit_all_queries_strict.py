# -*- coding: utf-8 -*-
"""
STRICT AUTOMATED 3-WAY AUDIT SUITE
Chế tài kiểm định tự động bắt buộc nhằm ngăn chặn AI Assistant vi phạm các quy tắc trong GEMINI.md.
"""
import sys, win32com.client

sys.stdout.reconfigure(encoding='utf-8')

conn = win32com.client.Dispatch("ADODB.Connection")
conn.Open("Provider=MSOLAP;Data Source=localhost;Initial Catalog=SSAS_Football_Transfermarkt;")

print("===================================================================================")
print("KHUNG KIỂM ĐỊNH KỶ LUẬT TỰ ĐỘNG (STRICT DISCIPLINARY AUDIT) - SSAS LIVE CUBE")
print("===================================================================================")

total_checks = 0
passed_checks = 0

def check(name, condition, details=""):
    global total_checks, passed_checks
    total_checks += 1
    if condition:
        passed_checks += 1
        print(f"  [PASS] {name} {details}")
    else:
        print(f"  [FAIL] {name} {details}")

# 1. AUDIT QUERY 10
print("\n--- 1. AUDIT QUERY 10: Top 10 CLB Châu Âu theo 4 Quý năm 2023 ---")
with open("mdx/query_10.mdx", "r", encoding="utf-8") as f:
    mdx_10 = f.read()

rs10 = win32com.client.Dispatch("ADODB.Recordset")
rs10.Open(mdx_10, conn)
rows10 = []
while not rs10.EOF:
    rows10.append([rs10.Fields(i).Value for i in range(rs10.Fields.Count)])
    rs10.MoveNext()
rs10.Close()

check("Q10 - MDX Row Count == 10", len(rows10) == 10, f"(Actual: {len(rows10)})")
check("Q10 - MDX Column Count == 7", len(rows10[0]) - 1 == 7, f"(Actual: {len(rows10[0]) - 1})")

# Check no nulls
has_null = any(any(val is None for val in r[1:]) for r in rows10)
check("Q10 - Zero Null / Dense Data", not has_null, "(No nulls or missing cells)")

# Check Browser simulation via Named Set
rs10_set = win32com.client.Dispatch("ADODB.Recordset")
rs10_set.Open("SELECT {[Measures].[Goals], [Measures].[QoQ Goals Growth]} ON 0, NONEMPTY([Top 10 Clubs 2023] * [DIM Time].[Hierarchy].[Year].[2023].CHILDREN, [Measures].[Goals]) ON 1 FROM [DW Football Transfermarkt];", conn)
set_clubs = set()
set_rows = 0
while not rs10_set.EOF:
    set_rows += 1
    set_clubs.add(rs10_set.Fields(0).Value)
    rs10_set.MoveNext()
rs10_set.Close()

check("Q10 - Named Set in Cube Browser has exactly 10 clubs", len(set_clubs) == 10, f"(Actual: {len(set_clubs)} clubs)")
check("Q10 - Named Set row count == 40 (10 clubs x 4 quarters)", set_rows == 40, f"(Actual: {set_rows} rows)")

# 2. AUDIT QUERY 11
print("\n--- 2. AUDIT QUERY 11: Siêu sân vận động sức chứa >= 60.000 chỗ ---")
with open("mdx/query_11.mdx", "r", encoding="utf-8") as f:
    mdx_11 = f.read()

rs11 = win32com.client.Dispatch("ADODB.Recordset")
rs11.Open(mdx_11, conn)
rows11 = []
while not rs11.EOF:
    rows11.append([rs11.Fields(i).Value for i in range(rs11.Fields.Count)])
    rs11.MoveNext()
rs11.Close()

check("Q11 - MDX Row Count == 23", len(rows11) == 23, f"(Actual: {len(rows11)})")

# Check capacity is integer, not "All" string
all_caps_numeric = all(isinstance(r[3], (int, float)) and r[3] >= 60000 for r in rows11)
check("Q11 - Capacity is numeric and >= 60000 (No 'All' text bug)", all_caps_numeric, f"(Min cap: {min(r[3] for r in rows11)})")

# Check Browser simulation with Custom operator
rs11_browser = win32com.client.Dispatch("ADODB.Recordset")
rs11_browser.Open("""
SELECT
    {[Measures].[Stadium Capacity Cleaned], [Measures].[Distinct Matches Played], [Measures].[Goals]} ON 0,
    FILTER(NONEMPTY([DIM Club].[Stadium Name].[Stadium Name].MEMBERS * [DIM Club].[Club Name].[Club Name].MEMBERS, [Measures].[Goals]), [Measures].[Stadium Capacity Cleaned] >= 60000) ON 1
FROM [DW Football Transfermarkt];
""", conn)
browser11_rows = 0
while not rs11_browser.EOF:
    browser11_rows += 1
    rs11_browser.MoveNext()
rs11_browser.Close()

check("Q11 - Browser Custom Filter Row Count == 23", browser11_rows == 23, f"(Actual: {browser11_rows} rows)")

# 3. AUDIT EXCEL FILE
print("\n--- 3. AUDIT EXCEL DOUBLE-CHECK WORKBOOK ---")
import openpyxl
wb = openpyxl.load_workbook("mdx/Bao_Cao_Double_Check_Query_10_11.xlsx")
ws10 = wb["Query 10 - QoQ Top 10 CLB"]
ws11 = wb["Query 11 - Sân trên 60k Chỗ"]
check("Excel - Q10 Sheet has 10 data rows", ws10.max_row - 4 == 10, f"(Actual: {ws10.max_row - 4})")
check("Excel - Q11 Sheet has 23 data rows", ws11.max_row - 4 == 23, f"(Actual: {ws11.max_row - 4})")

conn.Close()

print("\n===================================================================================")
print(f"KẾT QUẢ TỔNG THỂ: {passed_checks}/{total_checks} KIỂM TRA ĐẠT CHUẨN")
if passed_checks == total_checks:
    print("TRẠNG THÁI: TẤT CẢ CÁC RÀO CẢN KỶ LUẬT ĐÃ ĐƯỢC THỎA MÃN 100%!")
else:
    print("TRẠNG THÁI: PHÁT HIỆN SAI PHẠM! YÊU CẦU SỬA ĐỔI NGAY LẬP TỨC!")
print("===================================================================================")
