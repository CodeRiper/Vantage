import re
import os

with open(r'resources/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check all data-action attributes
actions_in_html = set(re.findall(r'data-action="([^"]+)"', content))
actions_in_html.update(re.findall(r"data-action='([^']+)'", content))

# Check for Actions definitions
actions_keys = set()
for match in re.finditer(r"['\"]([a-zA-Z0-9_\-]+)['\"]\s*(\([^\)]*\)|\:)\s*\{", content):
    actions_keys.add(match.group(1))

# Also search for direct assignments: Actions['foo'] or Actions.foo
for match in re.finditer(r"Actions\[['\"]([^'\"]+)['\"]\]", content):
    actions_keys.add(match.group(1))

# Check which HTML actions are not in actions_keys
missing = []
for a in sorted(actions_in_html):
    # Some actions might be handled dynamically or in switch/case
    if a not in actions_keys and f"case '{a}'" not in content and f'case "{a}"' not in content:
        missing.append(a)

print(f"Total unique data-actions found: {len(actions_in_html)}")
print(f"Unmatched actions count: {len(missing)}")
if missing:
    print("Unmatched actions list:")
    for m in missing:
        print(f" - {m}")
