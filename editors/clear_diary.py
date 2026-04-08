import re
import shutil
import sys

def clear_diary_entries(filepath):
    backup_path = filepath + ".bak"
    shutil.copy2(filepath, backup_path)
    print(f"Backup created: {backup_path}")

    # Detect encoding from BOM
    with open(filepath, 'rb') as f:
        raw = f.read(4)
    if raw[:2] == b'\xff\xfe':
        encoding = 'utf-16-le'
        bom = b'\xff\xfe'
    elif raw[:2] == b'\xfe\xff':
        encoding = 'utf-16-be'
        bom = b'\xfe\xff'
    elif raw[:3] == b'\xef\xbb\xbf':
        encoding = 'utf-8-sig'
        bom = b''
    else:
        encoding = 'utf-8'
        bom = b''
    print(f"Detected encoding: {encoding}")

    with open(filepath, 'r', encoding=encoding) as f:
        content = f.read()

    # Match "diary" => (const) [ ... ],
    # Use indentation of the "diary" line to find its own closing ],
    # (inner nested ], are at deeper indentation, so they won't match)
    pattern = r'(?m)^( +)"diary" => \(const\) \[\n([\s\S]*?)\n\1\],'

    matches = re.findall(pattern, content)
    count = sum(1 for _, body in matches if body.strip())
    print(f"Found {count} diary entries with content to clear")

    def replacer(m):
        indent = m.group(1)
        body = m.group(2)
        if body.strip():
            return f'{indent}"diary" => (const) [\n{indent}],'
        return m.group(0)

    result = re.sub(pattern, replacer, content)

    write_encoding = encoding if encoding != 'utf-8-sig' else 'utf-8-sig'
    with open(filepath, 'w', encoding=write_encoding) as f:
        f.write(result)

    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = r"d:\Music\temp\ダンジョン＆ブライドver1\savedata\data2.bmp.txt"
    clear_diary_entries(target)
