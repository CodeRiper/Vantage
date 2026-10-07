import subprocess

with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_start = text.find('<script>') + 8
s_end = text.find('</script>')
code = text[s_start:s_end]
lines = code.split('\n')

node_code = """
const vm = require('vm');
const fs = require('fs');
const code = fs.readFileSync('scripts/temp_code.js', 'utf-8');
try {
  new vm.Script(code);
  console.log('VALID JS');
} catch (e) {
  console.log('ERROR:', e.message);
  console.log('STACK:', e.stack);
}
"""

with open('scripts/temp_code.js', 'w', encoding='utf-8') as f:
    f.write(code)

with open('scripts/temp_runner.js', 'w', encoding='utf-8') as f:
    f.write(node_code)

res = subprocess.run(['node', 'scripts/temp_runner.js'], capture_output=True, text=True)
print(res.stdout)
