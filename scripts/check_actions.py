import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    'data-action="nav"',
    'np-download-att',
    'np-font-size',
    'np-heading',
    'np-img-del',
    'np-img-size',
    'np-remove-att',
    'sticky-edit'
]

for i, line in enumerate(lines):
    for t in targets:
        if t in line:
            print(f"Line {i+1}: [{t}] {line.strip()[:140]}")
