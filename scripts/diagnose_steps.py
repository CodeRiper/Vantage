import json
import subprocess

log_path = r'C:\Users\Akash.J\.gemini\antigravity-ide\brain\fc547a50-a824-45d6-908c-8f22f3fcbffb\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

step_indices = [5279, 5275, 5267, 5261, 5257, 5253, 5241, 5237, 5229, 5223, 5217, 5211, 5207, 5203]

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    current_content = f.read()

def test_syntax(html_text):
    s_start = html_text.find('<script>') + 8
    s_end = html_text.find('</script>')
    code = html_text[s_start:s_end]
    with open('scripts/test_candidate.js', 'w', encoding='utf-8') as tf:
        tf.write(code)
    res = subprocess.run(['node', '--check', 'scripts/test_candidate.js'], capture_output=True, text=True)
    return res.returncode == 0, res.stderr

valid, err = test_syntax(current_content)
print(f'Current content valid: {valid}')

# Now revert each step one by one
sim_content = current_content.replace('\r\n', '\n')
for idx in step_indices:
    data = json.loads(lines[idx])
    tc = data['tool_calls'][0]
    target = tc['args']['TargetContent']
    replacement = tc['args']['ReplacementContent']
    if isinstance(target, str) and target.startswith('"') and target.endswith('"'):
        try:
            target = json.loads(target)
        except Exception:
            pass
    if isinstance(replacement, str) and replacement.startswith('"') and replacement.endswith('"'):
        try:
            replacement = json.loads(replacement)
        except Exception:
            pass
    target = target.replace('\r\n', '\n')
    replacement = replacement.replace('\r\n', '\n')
    
    if replacement in sim_content:
        sim_content = sim_content.replace(replacement, target, 1)
        valid, err = test_syntax(sim_content)
        desc = tc["args"].get("Description", "")[:40]
        print(f'After reverting step {idx} ({desc}): valid={valid}')
        if valid:
            print(f'>>> Step {idx} caused the syntax error! <<<')
            break
    else:
        print(f'Could not find replacement for step {idx}')
