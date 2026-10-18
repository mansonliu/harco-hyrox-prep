# HYROX Taipei 2027 備賽讀本（原 HARCO 2026 備賽讀本）

個人混合體能賽事備賽整理。2026-10-18 完成 HARCO 八項混合運動挑戰賽（官方 41:58.5），
下一場是 **2027-03-13（六）HYROX Taipei 男子公開組**（南港展覽館一館）。
讀本已從 HARCO 版改寫為 HYROX 版，HARCO 的實際成績與手錶紀錄當作訓練基準。

**成品：`index.html`** — 左側頁籤式讀本，響應式、暗色模式相容。用瀏覽器開啟即可，
或看 GitHub Pages：https://mansonliu.github.io/harco-hyrox-prep/

## 內容

| 章節 | 內容 |
|---|---|
| 1. HYROX 賽制與目標 | HYROX Taipei 賽事資訊、Men Open 規格、與 HARCO 不同的規則、判罰總表、以 HARCO 實測放大的目標時間 |
| 2. HARCO 2026 成績檢討 | 官方分段與排名、Garmin 圈數對齊、各站動作時間與站內走動、心率時間軸、帶到 HYROX 的五個結論 |
| 3. Wall Ball 專章 | HARCO 最困難的一站：No Rep 全是高度不夠的問題鏈、高度修正、瞄準點、「高度一掉就停」分組、用自己的 6 kg 球自主訓練、比賽腳本 |
| 4. 雪橇兩站 | 推 152 kg、拉 103 kg，各 4 × 12.5 m；精簡版技術、卡住重啟、繩索管理、替代訓練 |
| 5. 其他五站 | SkiErg、Burpee、Row、Farmers、Sandbag Lunges：規則、HARCO 實測、HYROX 推估 |
| 6. 跑步與轉換區 | 8 × 1 km 心率配速、跑圈自己數、RoxZone 流程 |
| 7. 訓練計畫 | 21 週（2026-10-19 → 2027-03-13），以每週六中午 1 小時教練課為核心＋自主訓練；W9／W13／W18 三次測驗；連假安排 |
| 8. 比賽週與比賽日 | 報到、裝備（§10 允許清單）、補給、以出發時間往回推的時間表、配速卡 |
| 9. 來源與待確認 | 規則書與賽事頁、HARCO 成績來源、技術資料、HYROX Taipei 待公布事項 |

## 重要提醒

- **規格與判罰以 HYROX 26/27 Singles Rulebook 為準**（2026-10-18 核對），重點在 `research/hyrox-rulebook-2627.md`。
- **Men Open 器材是灰色**：壺鈴 2 × 24 kg、沙包 20 kg、藥球 6 kg；雪橇 152／103 kg 含雪橇，各 4 × 12.5 m。
- HYROX 與 HARCO 的關鍵差異：**沙包要扛雙肩**、**任何一站沒做完 DQ**、**跑圈自己數**、止滑粉只能用大會提供的。
- 目標時間「約 1:32–1:44」是用 HARCO 動作時間乘假設係數、加上 HARCO 跑段（每圈 380 m）換算的配速推來的量級，不是預測；以 W3、W9、W13、W18 測驗修正。
- HARCO 當天推雪橇臨時下修為 126 kg（新草皮摩擦大），HYROX 的 152 kg 還沒在比賽中推過。
- HYROX Taipei 的跑圈數、場地圖、報到時間仍是 TBC；個人出發時間賽前約 3 天公布。
- 鞋確定沿用 HARCO 穿的 adidas Dropset Pro；硬地板與新地毯抓地較差，比賽當天熱身先試地面。
- 公開 repo：不寫姓名、選手編號；HARCO 原始成績 PDF 與 TCX 不進 repo。

## 目錄結構

```
index.html          成品讀本
_notes/             讀本原始碼（NN-*.html 分段 + meta.json），改內容改這裡
research/           研究筆記（含出處），讀本的憑據
  hyrox-rulebook-2627.md      HYROX 26/27 單人規則書重點＋HYROX Taipei 賽事資訊
  harco-2026-results.md       HARCO 官方分段、Garmin 圈數、對齊方法、心率、HYROX 推估
  harco-handbook-2026.md      HARCO 官方大會手冊重點（對照 HARCO 成績時查規則用）
  harco-official-spec.md      HARCO 官網逐字規格（2026-08-20）
  codex-hyrox-stations.md     HYROX 八站技術（Codex 產出）
  codex-sled-deep-dive.md     雪橇兩站專題（Codex 產出）
  archive/                    已結束的 HARCO 備賽資料（配速模型、八週計畫、選鞋）
scripts/            HARCO 圈數對齊與心率圖產生腳本（輸入 TCX，不在 repo）
build.sh            重新產生 index.html
```

## 重新產生 index.html

```sh
./build.sh
```

改內容只需編輯 `_notes/` 下的 html 分段，再跑 build。
章節（頁籤）由 `<h2 id="...">` 自動切分。
