#!/usr/bin/env python3
"""Clean up Google Docs markdown export artifacts across all nightfall/ files."""

import os
import re
import glob

NIGHTFALL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nightfall")


def cleanup(text):
    # Remove broken image references like ![][image7]
    text = re.sub(r'!\[\]\[image\d+\]\s*\n?', '', text)

    # Remove bold wrapping from headers: # **Foo** -> # Foo
    text = re.sub(r'^(#+)\s*\*\*(.+?)\*\*\s*$', r'\1 \2', text, flags=re.MULTILINE)

    # Unescape special chars that Google Docs escapes unnecessarily
    # \= \. \- \[ \] \( \) \* \! \+ \> \~ \{ \} \# \_
    # But be careful not to break actual escape sequences
    text = re.sub(r'\\([=.\[\]()*!+>~{}#_`|<])', r'\1', text)
    # Handle \- but not in front of > (arrow)
    text = re.sub(r'\\-', '-', text)

    # Remove trailing backslash line continuations (Google Docs artifact)
    text = re.sub(r'\\\s*$', '', text, flags=re.MULTILINE)

    # Remove trailing whitespace on lines (including double-space forced breaks
    # that are artifacts, not intentional)
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

    # Collapse 3+ consecutive blank lines down to 2 (one blank line between content)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Ensure file ends with single newline
    text = text.strip() + '\n'

    return text


def process_file(filepath):
    with open(filepath, 'r') as f:
        original = f.read()

    cleaned = cleanup(original)

    if cleaned != original:
        with open(filepath, 'w') as f:
            f.write(cleaned)
        return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(NIGHTFALL_DIR, '**', '*.md'), recursive=True))
    changed = 0
    for filepath in files:
        relpath = os.path.relpath(filepath, NIGHTFALL_DIR)
        if process_file(filepath):
            print(f"  cleaned: {relpath}")
            changed += 1
        else:
            print(f"  unchanged: {relpath}")
    print(f"\n{changed}/{len(files)} files modified")


if __name__ == "__main__":
    main()