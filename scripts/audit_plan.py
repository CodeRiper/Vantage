import re

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all data-action with plan-
actions_used = set(re.findall(r'data-action=["\'](plan-[^"\']+)["\']', text))
print("Plan actions used in HTML:", sorted(list(actions_used)))

# Find which are implemented in Actions
for a in sorted(list(actions_used)):
    has_fn = (f"'{a}'" in text or f'"{a}"' in text or f"Actions['{a}']" in text or f'Actions["{a}"]' in text)
    print(f"Action '{a}': {'FOUND' if has_fn else 'MISSING'}")
