import re

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== WINDOW/DOCUMENT EVENT LISTENERS ===')
pattern = r'(window|document)\.addEventListener\(\s*[\'"]([^\'"]+)[\'"]'
for m in re.finditer(pattern, text):
    line = text[:m.start()].count('\n') + 1
    snippet = text[m.start():m.start()+120].replace('\n', ' ')
    print(f'Line {line}: {m.group(1)}.{m.group(2)} -> {snippet[:80]}')
