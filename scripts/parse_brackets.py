with open('scripts/inner_code.js', 'r', encoding='utf-8') as f:
    code = f.read()

tokens = []
i = 0
n = len(code)
line = 1
col = 1
last_token = ''

stack = []

while i < n:
    c = code[i]
    if c == '\n':
        line += 1
        col = 1
        i += 1
        continue
    if c in ' \t\r':
        col += 1
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
        
    # regex vs division
    if c == '/':
        # if last_token indicates expression prefix:
        is_regex = False
        if not last_token or last_token in '({[,;:!?=&|+*-~^%<>' or last_token in ['return', 'typeof', 'case', 'delete', 'throw', 'in', 'instanceof', 'void']:
            is_regex = True
        
        if is_regex:
            i += 1
            col += 1
            in_bracket = False
            while i < n:
                if code[i] == '\\':
                    i += 2
                    col += 2
                    continue
                if code[i] == '[':
                    in_bracket = True
                elif code[i] == ']':
                    in_bracket = False
                elif code[i] == '/' and not in_bracket:
                    i += 1
                    col += 1
                    break
                if code[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
            # flags
            while i < n and code[i].isalnum():
                i += 1
                col += 1
            last_token = 'regex'
            continue
        else:
            last_token = '/'
            i += 1
            col += 1
            continue

    # single quote string
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
        last_token = 'str'
        continue

    # double quote string
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
        last_token = 'str'
        continue

    # template literal
    if c == '`':
        i += 1
        col += 1
        while i < n and code[i] != '`':
            if code[i] == '\\':
                i += 2
                col += 2
                continue
            # if ${...}, rough skip
            if code[i] == '$' and i + 1 < n and code[i+1] == '{':
                stack.append(('${', line, col))
                i += 2
                col += 2
                last_token = '${'
                break
            if code[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        if i < n and code[i] == '`':
            i += 1
            col += 1
            last_token = 'tpl'
        continue

    if c in '({[':
        stack.append((c, line, col))
        last_token = c
        i += 1
        col += 1
        continue
        
    if c in ')}]':
        if not stack:
            print(f'EXTRA closing {c} at line {line}:{col}')
        else:
            top, tl, tc = stack.pop()
            matches = {'(': ')', '{': '}', '[': ']', '${': '}'}
            if matches[top] != c:
                print(f'MISMATCH: {top} from line {tl}:{tc} closed by {c} at line {line}:{col}')
        last_token = c
        i += 1
        col += 1
        continue

    # identifier or number or symbol
    if c.isalnum() or c in '_$':
        start = i
        while i < n and (code[i].isalnum() or code[i] in '_$'):
            i += 1
            col += 1
        last_token = code[start:i]
        continue

    last_token = c
    i += 1
    col += 1

print(f'Final remaining stack items: {len(stack)}')
for item in stack:
    print('Unclosed:', item)
