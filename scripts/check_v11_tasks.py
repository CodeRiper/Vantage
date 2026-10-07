import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

v11_start = text.find('VANTAGE v1.1')
lines = text[v11_start:].splitlines()
for idx, line in enumerate(lines):
    if 'task' in line.lower() and ('function ' in line or 'action' in line or 'render' in line or 'store' in line):
        print(f'{idx+1}: {line.strip()[:140]}')
