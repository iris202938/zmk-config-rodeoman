from pathlib import Path
import re
path = Path(r'c:\Users\iris2\github\zmk-config-rodeoman\config\rodeoman.keymap')
text = path.read_text(encoding='utf-8')
lines = text.splitlines()
start, end = 716, 2336
changed = 0
for i in range(start, min(end+1, len(lines))):
    line = lines[i]
    m = re.search(r'^(?P<prefix>\s*//\s*)?(?P<body>key-positions\s*=\s*<(?P<first>\d+)\s+(?P<second>31|34)>;)(?P<comment>.*)$', line)
    if not m:
        continue
    prefix = m.group('prefix') or ''
    body = m.group('body')
    first = m.group('first')
    second = m.group('second')
    comment = m.group('comment') or ''
    new_second = '33' if second == '31' else '36'
    new_body = re.sub(r'<'+first+r'\s+'+second+r'>;', f'<{first} {new_second}>;', body)
    extra = ''
    comment_text = comment.strip()
    if comment_text.startswith('//'):
        tail = re.sub(r'^//\s*旧\s+\d+\s+\d+', '', comment_text).strip()
        if tail:
            extra = ' ' + tail
    elif comment_text:
        extra = ' ' + comment_text
    new_comment = f' // before: <{first} {second}>' + extra if comment_text else ''
    if new_comment == comment and new_body == body:
        continue
    lines[i] = f'{prefix}{new_body}{new_comment}'
    changed += 1
path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''), encoding='utf-8')
print(f'changed {changed} lines')
