# -*- coding: utf-8 -*-
import sys, re, glob

sys.stdout.reconfigure(encoding='utf-8')

# True SSAS Schema from project files
VALID_SCHEMA = {
    'DIM Club': ['Club ID', 'Club Name', 'Stadium Name', 'Stadium Seats', 'Coach Name', 'Squad Size'],
    'DIM Competition': ['Competition ID', 'Competition Name', 'Country Name', 'Competition Type', 'Hierarchy'],
    'DIM Game': ['Game ID', 'Round', 'Home Club ID', 'Away Club ID', 'Home Club Goals', 'Away Club Goals', 'Stadium', 'Hierarchy'],
    'DIM Player': ['Player ID', 'Player Name', 'Date Of Birth', 'Age', 'Country Of Citizenship', 'Main Position', 'Sub Position', 'Foot', 'Height In Cm', 'Hierarchy'],
    'DIM Time': ['Time ID', 'Full Date', 'Day Of Week', 'Day', 'Month', 'Quarter', 'Year', 'Season', 'Is Weekend', 'Hierarchy'],
    'Opponent Club': ['Club ID', 'Club Name', 'Stadium Name', 'Stadium Seats', 'Coach Name', 'Squad Size'],
    'FACT Player Match Perf': ['Minutes Played', 'Goals', 'Assists', 'Goal Contributions', 'Yellow Cards', 'Red Cards', 'Is Starter', 'Is Home Game', 'FACT Player Match Perf Count']
}

queries = ['01', '03', '04', '05', '06', '07', '09', '10', '11', '12']

def audit_all():
    print('AUDITING ALL 10 QUERIES ACROSS 3 METHODS & METADATA...')
    issues = []

    for q in queries:
        file_path = f'mdx/query_{q}.md'
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for Coach Name with DIM Game anywhere in text
        if re.search(r'DIM Game.*?Coach Name', content, re.IGNORECASE):
            issues.append(f'Query {q}: DIM Game associated with Coach Name (Coach Name is in DIM Club!)')

        # Check for Stadium Name with DIM Game anywhere in text
        if re.search(r'DIM Game.*?Stadium Name', content, re.IGNORECASE):
            issues.append(f'Query {q}: DIM Game associated with Stadium Name (Stadium Name is in DIM Club!)')

        # Check 2.1 vs 2.2 vs 2.3 vs 3 consistency
        s21 = re.search(r'### 2\.1\.(.*?)(?=### 2\.2\.)', content, re.DOTALL)
        s22 = re.search(r'### 2\.2\.(.*?)(?=### 2\.3\.)', content, re.DOTALL)
        s23 = re.search(r'### 2\.3\.(.*?)(?=### 2\.4\.)', content, re.DOTALL)
        s3 = re.search(r'## 3\.(.*?)(?=## 4\.)', content, re.DOTALL)

        if not s21: issues.append(f'Query {q}: Missing 2.1')
        if not s22: issues.append(f'Query {q}: Missing 2.2')
        if not s23: issues.append(f'Query {q}: Missing 2.3')
        if not s3: issues.append(f'Query {q}: Missing Section 3')

        # Check if Calculated Member in 2.1 exists when WITH MEMBER is in 2.3
        if 'WITH MEMBER' in s23.group(1):
            if 'Calculations' not in s21.group(1):
                issues.append(f'Query {q}: 2.3 uses WITH MEMBER but 2.1 does NOT mention Calculations tab to create Calculated Member!')
            if 'Values' not in s22.group(1):
                issues.append(f'Query {q}: 2.3 uses WITH MEMBER but 2.2 does NOT pull Calculated Member into Values!')

    if issues:
        print(f'FOUND {len(issues)} ISSUES:')
        for iss in issues:
            print('  * ', iss)
    else:
        print('NO STRUCTURAL INCONSISTENCIES FOUND!')

if __name__ == '__main__':
    audit_all()
