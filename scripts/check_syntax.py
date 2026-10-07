with open('resources/app/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_start = text.find('<script>') + 8
s_end = text.find('</script>')
code = text[s_start:s_end]
lines = code.split('\n')

stack = []
in_str = None
in_block_comment = False

for i, line in enumerate(lines):
    j = 0
    while j < len(line):
        if in_block_comment:
            if line[j:j+2] == '*/':
                in_block_comment = False
                j += 2
                continue
            j += 1
            continue
        if in_str:
            if line[j] == '\\':
                j += 2
                continue
            if line[j] == in_str:
                in_str = None
                j += 1
                continue
            j += 1
            continue
        if line[j:j+2] == '/*':
            in_block_comment = True
            j += 2
            continue
        if line[j:j+2] == '//':
            break
        if line[j] in ('"', "'", '`'):
            in_str = line[j]
            j += 1
            continue
        if line[j] in '({[':
            stack.append((line[j], i+1, j+1, line.strip()[:40]))
        elif line[j] in ')}]':
            if not stack:
                print(f'Extra closing {line[j]} at line {i+1}')
            else:
                op, op_line, op_col, op_text = stack.pop()
                expected = { '(': ')', '{': '}', '[': ']' }[op]
                if line[j] != expected:
                    print(f'Mismatch at line {i+1}: got {line[j]}, expected {expected} for {op} from line {op_line} ({op_text})')
        j += 1

print('Remaining unclosed items on stack:', len(stack))
for item in stack:
    print('  Unclosed:', item)
