import json

log_path = r'C:\Users\Akash.J\.gemini\antigravity-ide\brain\fc547a50-a824-45d6-908c-8f22f3fcbffb\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('scripts/step_details.txt', 'w', encoding='utf-8') as out:
    for idx in [5229, 5237, 5241, 5253, 5257, 5261, 5267, 5275, 5279]:
        data = json.loads(lines[idx])
        tc = data['tool_calls'][0]
        out.write(f'=== STEP {idx} ===\n')
        out.write('TargetContent:\n' + tc['args']['TargetContent'] + '\n')
        out.write('--- REPLACEMENT ---:\n' + tc['args']['ReplacementContent'] + '\n\n')

print('Wrote to scripts/step_details.txt')
