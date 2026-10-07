import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for idx, line in enumerate(text.splitlines()):
    if 'npEditorBody' in line or 'npTitleInput' in line:
        print(f'{idx+1}: {line.strip()[:140]}')
