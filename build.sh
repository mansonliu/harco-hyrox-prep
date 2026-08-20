#!/bin/sh
# 依檔名順序串接 _notes/NN-*.html 成 body.html，再用 longform-research-html 的組裝器產出 index.html
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL="$HOME/claude/skills/longform-research-html"
cat "$DIR"/_notes/[0-9][0-9]-*.html > "$DIR/_notes/body.html"
python3 "$SKILL/scripts/build_html.py" "$DIR"
