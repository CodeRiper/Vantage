import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [i for i in range(len(text)) if text.startswith('setInterval', i)]
print(f'Total setInterval calls: {len(matches)}')
for pos in matches:
    line_no = text[:pos].count('\n') + 1
    print(f'Line {line_no}: {text[pos:pos+100]}')
