with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
actions = re.findall(r'data-action="([^"]+)"', text)
np_actions = [a for a in set(actions) if 'np' in a or 'note' in a]
print('Actions:', sorted(np_actions))
