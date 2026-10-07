import json

log_path = r'C:\Users\Akash.J\.gemini\antigravity-ide\brain\fc547a50-a824-45d6-908c-8f22f3fcbffb\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

user_step = -1
for i, l in enumerate(lines):
    data = json.loads(l)
    if data.get('type') == 'USER_INPUT':
        content = data.get('content', '')
        if 'Here still have an issues' in content or 'i will write a notes' in content:
            user_step = i
            print(f'Found user message at step {i}')

if user_step != -1:
    print(f'Scanning steps from {user_step} to {len(lines)}...')
    with open('scripts/user_turn_edits.txt', 'w', encoding='utf-8') as out:
        for i in range(user_step, len(lines)):
            data = json.loads(lines[i])
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    name = tc.get('name', '')
                    if 'replace' in name or 'write' in name:
                        tf = tc.get('args', {}).get('TargetFile')
                        desc = tc.get('args', {}).get('Description')
                        out.write(f'Step {i}: {name} -> {tf}\n')
                        out.write(f'  Desc: {desc}\n')
                        if 'TargetContent' in tc.get('args', {}):
                            out.write('  Target:\n' + tc['args']['TargetContent'] + '\n')
                            out.write('  Replacement:\n' + tc['args']['ReplacementContent'] + '\n')
                        out.write('='*50 + '\n')

print('Done writing user_turn_edits.txt')
