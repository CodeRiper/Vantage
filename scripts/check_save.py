with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if any(k in line for k in ['plan-save', 'plan-subtask-remove']):
            safe_line = line.strip()[:120].encode('ascii', errors='replace').decode()
            print(f'{idx}: {safe_line}')
