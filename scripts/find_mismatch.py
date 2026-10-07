with open('scripts/temp_code.js', 'r', encoding='utf-8') as f:
    code = f.read()

stack = []
i = 0
n = len(code)
line = 1
col = 1

while i < n:
    c = code[i]
    if c == '\n':
        line += 1
        col = 1
        i += 1
        continue
    
    # line comment
    if c == '/' and i + 1 < n and code[i+1] == '/':
        i += 2
        col += 2
        while i < n and code[i] != '\n':
            i += 1
            col += 1
        continue
        
    # block comment
    if c == '/' and i + 1 < n and code[i+1] == '*':
        i += 2
        col += 2
        while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
            if code[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        i += 2
        col += 2
        continue
        
    # string single quote
    if c == "'":
        i += 1
        col += 1
        while i < n and code[i] != "'":
            if code[i] == '\\':
                i += 2
                col += 2
                continue
            if code[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        i += 1
        col += 1
        continue
        
    # string double quote
    if c == '"':
        i += 1
        col += 1
        while i < n and code[i] != '"':
            if code[i] == '\\':
                i += 2
                col += 2
                continue
            if code[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        i += 1
        col += 1
        continue
        
    # template literal (rough)
    if c == '`':
        i += 1
        col += 1
        while i < n and code[i] != '`':
            if code[i] == '\\':
                i += 2
                col += 2
                continue
            if code[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        i += 1
        col += 1
        continue

    if c in '({[':
        stack.append((c, line, col))
    elif c in ')}]':
        if not stack:
            print(f'Extra closing {c} at line {line}:{col}')
        else:
            top, tl, tc = stack.pop()
            matches = {'(': ')', '{': '}', '[': ']'}
            if matches[top] != c:
                print(f'Mismatched {top} from line {tl}:{tc} closed by {c} at line {line}:{col}')
                break
    i += 1
    col += 1

print(f'Finished. Remaining stack size: {len(stack)}')
for item in stack[-15:]:
    print('Unclosed:', item)
