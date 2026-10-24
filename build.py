#!/usr/bin/env python3
"""Build the page: put the prose from text.md into src/page.html.

Writes audible-sdr.html (the page body, also used for the claude.ai artifact)
and index.html (the standalone page served on g3ali.com and GitHub Pages).
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = r'[\w.\-]+'


def read_text(path):
    """Parse text.md into {key: [paragraph, ...]}."""
    src = re.sub(r'<!--.*?-->', '', path.read_text(encoding='utf-8'), flags=re.S)
    blocks, key, lines = {}, None, []

    def flush():
        if key is not None:
            paras = [' '.join(l.strip() for l in p.splitlines()) for p in re.split(r'\n\s*\n', '\n'.join(lines))]
            blocks[key] = [p for p in paras if p]

    for line in src.splitlines():
        m = re.match(rf'^##\s+({KEY})\s*$', line)
        if m:
            flush()
            key, lines = m.group(1), []
            if key in blocks:
                sys.exit(f'text.md: key "{key}" appears twice')
        elif line.startswith('#'):
            continue  # signpost heading
        elif key is not None:
            lines.append(line)
    flush()
    return blocks


def inline(text):
    """Light markdown to HTML: `code`, **bold**, *italic*, [text](url). Raw HTML passes through."""
    parts = re.split(r'(`[^`]*`)', text)
    out = []
    for part in parts:
        if part.startswith('`') and part.endswith('`') and len(part) > 1:
            out.append('<code>' + part[1:-1] + '</code>')
            continue
        part = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', part)
        part = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', part)
        part = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', part)
        out.append(part)
    return ''.join(out)


def build():
    template = (ROOT / 'src' / 'page.html').read_text(encoding='utf-8')
    text = read_text(ROOT / 'text.md')
    used, missing = set(), []

    def get(key):
        used.add(key)
        if key not in text:
            missing.append(key)
            return ['']
        return text[key]

    # A paragraph tag holding one key becomes one tag per paragraph in text.md.
    page = re.sub(rf'<p([^>]*)>\{{\{{({KEY})\}}\}}</p>',
                  lambda m: '\n'.join(f'<p{m.group(1)}>{inline(p)}</p>' for p in get(m.group(2))), template)
    # Strings inside the script.
    page = re.sub(rf'\{{\{{js:({KEY})\}}\}}', lambda m: json.dumps(inline(' '.join(get(m.group(1)))), ensure_ascii=False), page)
    # Everything else is inline text.
    page = re.sub(rf'\{{\{{({KEY})\}}\}}', lambda m: inline(' '.join(get(m.group(1)))), page)

    if missing:
        sys.exit('text.md is missing these keys:\n  ' + '\n  '.join(missing))
    for key in sorted(set(text) - used):
        print(f'warning: text.md key "{key}" is not used by the page', file=sys.stderr)

    (ROOT / 'audible-sdr.html').write_text(page, encoding='utf-8')
    (ROOT / 'index.html').write_text(
        '<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
        + page + '\n</body></html>\n', encoding='utf-8')
    print(f'built audible-sdr.html and index.html ({len(used)} text blocks)')


if __name__ == '__main__':
    build()
