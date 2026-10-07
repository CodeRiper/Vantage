import re

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
current_fn = None
for i, line in enumerate(lines):
    fn_match = re.search(r'function\s+([a-zA-Z0-9_$]+)\s*\(', line)
    if fn_match:
        current_fn = fn_match.group(1)
    if 'addEventListener' in line:
        print(f"Line {i+1} in [{current_fn}]: {line.strip()[:100]}")
