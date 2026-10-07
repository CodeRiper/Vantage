with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ["'open-entry'", "'new-entry'", 'openEntry', 'function openEntryModal', 'renderEntryModal', 'saveJournal']):
        print(f'{i+1}: {l.strip()[:80]}')
