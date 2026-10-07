import re

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_start = text.find('<script>')
s_end = text.find('</script>')
script_text = text[s_start:s_end]

actions_in_html = set(re.findall(r'data-action=["\']([a-zA-Z0-9_-]+)["\']', text))
missing = []
for a in sorted(actions_in_html):
    # Check if a has a handler in Actions or a listener
    p_call1 = f"'{a}'("
    p_call2 = f'"{a}"('
    p_col1 = f"'{a}':"
    p_col2 = f'"{a}":'
    p_act1 = f"Actions['{a}']"
    p_act2 = f'Actions["{a}"]'
    p_ev1 = f"action === '{a}'"
    p_ev2 = f'action === "{a}"'
    if not (p_call1 in script_text or p_call2 in script_text or p_col1 in script_text or p_col2 in script_text or p_act1 in script_text or p_act2 in script_text or p_ev1 in script_text or p_ev2 in script_text):
        missing.append(a)

print(f"Total data-actions found: {len(actions_in_html)}")
print("Actions with NO handler:", missing)
