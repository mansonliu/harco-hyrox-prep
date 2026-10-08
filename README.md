# HARCO 2026 備賽讀本

2026 HARCO 八項混合運動挑戰賽（2026.10.17–10.18，台北世貿一館）的個人備賽整理。

**成品：`index.html`** — 左側頁籤式讀本，響應式、暗色模式相容。用瀏覽器開啟即可。
GitHub 的 markdown 渲染看不到排版，請直接下載 `index.html` 開啟。

## 內容

| 章節 | 內容 |
|---|---|
| 1. 賽制與目標 | 大會手冊規格與時段、判罰總表、HARCO ≒ 半場 Hyrox 的對照、推估目標時間 |
| 2. 推雪橇 Sled Push | 技術、卡住的破解、無器材替代訓練 |
| 3. 拉雪橇 Sled Pull | 三種拉法比較、繩索管理、選擇依據 |
| 4. 其他六站 | SkiErg、Burpee、Row、Farmer、Lunge、Wall Ball |
| 5. 跑步與轉換區 | 八段配速計畫、RoxZone 策略、場地配置與動線 |
| 6. 八週訓練計畫 | 2026-08-24 → 2026-10-18 |
| 7. 賽前一週與比賽日 | 報到與晶片、鞋（已定案 adidas Dropset Pro）、裝備、時間表、完賽與申訴 |
| 8. 來源與待確認 | 全部出處、大會手冊核對結果、仍待現場確認的事 |

## 重要提醒

- **跑步是每站間 400 m（全程 3.2 km）**，不是媒體稿寫的 800 m。以官網為準。
- **重量與 Hyrox 完全相同**，只有距離與次數減半。肌力門檻沒有變低。
- 讀本以**男子組 SOLO** 為對象。
- 讀本中的時間是**由 Hyrox 公開資料推估的區間**（約 37–41 分），不是 HARCO 官方預測，也不是統計上的中位完賽時間。HARCO 是首屆賽事，無歷史成績。
- **2026-10-08 官方大會手冊發佈後，賽制、動作標準與判罰一律以手冊為準**（本 repo 不附原檔），
  重點整理在 `research/harco-handbook-2026.md`。第 2、3、4 章的規則敘述已改為手冊條文。
- 手冊沒寫的仍待現場確認：雪橇每趟長度與趟數、地面材質、個人出發梯次（見第 8 章）。
- **鞋已定案：adidas Dropset Pro**（2026-09-14）。定案前的候選比較與四項門檻討論
  歸檔在 `research/archive/shoe-selection.md`，不再更新；第 7 章只留磨合安排。

## 目錄結構

```
index.html          成品讀本
_notes/             讀本原始碼（body.html 分段 + meta.json），改內容改這裡
research/           研究筆記（含出處），讀本的憑據
  harco-handbook-2026.md      官方大會手冊重點（規格、流程、八站規則與判罰）
  harco-official-spec.md      官網逐字規格（2026-08-20）
  pacing-model.md             配速換算模型與推算過程
  training-plan.md            八週計畫草稿
  codex-hyrox-stations.md     Hyrox 八站技術（Codex 產出）
  codex-sled-deep-dive.md     雪橇兩站專題（Codex 產出）
  archive/shoe-selection.md   選鞋候選比較與決策門檻（已歸檔，鞋已定案 adidas Dropset Pro）
build.sh            重新產生 index.html
```

## 重新產生 index.html

```sh
./build.sh
```

改內容只需編輯 `_notes/` 下的 html 分段，再跑 build。
章節（頁籤）由 `<h2 id="...">` 自動切分。
