import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_start = text.find('id="view-tasks"')
if s_start == -1:
    s_start = text.find('view-tasks')
print(text[s_start:s_start+1500])
