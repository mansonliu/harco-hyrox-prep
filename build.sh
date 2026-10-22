#!/bin/sh
# 依檔名順序串接 _notes/NN-*.html 成 body.html，再用 longform-research-html 的組裝器產出 index.html
# 兩個頁面：根目錄（HYROX 備賽讀本）與 running/（跑步訓練頁）
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
# 設定夾各台不同（Mini／Office 無點 ~/claude 並設 CLAUDE_CONFIG_DIR；Air 標準 ~/.claude）
# 先信環境變數，再依序退回兩種慣例；請勿依單一機器改動順序
for d in "${CLAUDE_CONFIG_DIR:-}" "$HOME/.claude" "$HOME/claude"; do
  [ -n "$d" ] && [ -d "$d/skills/longform-research-html" ] && SKILL="$d/skills/longform-research-html" && break
done
[ -n "${SKILL:-}" ] || { echo "找不到 longform-research-html skill（CLAUDE_CONFIG_DIR／~/.claude／~/claude 都沒有）" >&2; exit 1; }

build_one() {
  root="$1"
  cat "$root"/_notes/[0-9][0-9]-*.html > "$root/_notes/body.html"
  python3 "$SKILL/scripts/build_html.py" "$root"
  # 範本的 callout 標籤沿用自醫學影像讀本，改成符合本主題的用語
  python3 - "$root/index.html" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
s = s.replace('content:"判讀重點"', 'content:"重點"').replace('content:"陷阱"', 'content:"注意"')
open(p, 'w', encoding='utf-8').write(s)
print('callout 標籤已在地化')
PY
}

build_one "$DIR"
build_one "$DIR/running"
