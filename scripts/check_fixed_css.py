with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

style_start = text.find('<style>')
style_end = text.find('</style>')
style = text[style_start:style_end]

lines = style.split('\n')
for i, line in enumerate(lines):
    if 'position: fixed' in line or 'position:fixed' in line:
        context = '\n'.join(lines[max(0, i-2):min(len(lines), i+4)])
        print(f"Line {i+1}:\n{context}\n---")
