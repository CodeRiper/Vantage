import json

log_path = r'C:\Users\Akash.J\.gemini\antigravity-ide\brain\fc547a50-a824-45d6-908c-8f22f3fcbffb\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)-1, max(0, len(lines)-150), -1):
    data = json.loads(lines[i])
    if 'tool_calls' in data:
        for tc in data['tool_calls']:
            name = tc.get('name', '')
            if 'replace' in name or 'write' in name:
                tf = tc.get('args', {}).get('TargetFile')
                desc = tc.get('args', {}).get('Description')
                print(f'Step {i}: {name} -> {tf}')
                print(f'   Desc: {desc}')
                if 'ReplacementChunks' in tc.get('args', {}):
                    for c in tc['args']['ReplacementChunks']:
                        print('   Chunk StartLine:', c.get('StartLine'), 'EndLine:', c.get('EndLine'))
                if 'StartLine' in tc.get('args', {}):
                    print('   StartLine:', tc['args'].get('StartLine'), 'EndLine:', tc['args'].get('EndLine'))
