#!/usr/bin/env python3
"""Garmin 月檢：從 Garmin Connect Personal API 拉跑步／騎車／肌力量、同心率配速、心率區間、HRV、安靜心率、睡眠，輸出 Markdown。

需求：Garmin 官方 Personal API Python 套件（PyPI 名稱見 github.com/garmin 的 personal api 範例 repo），
預設裝在 ~/garmin-env；API key 放在 ~/.config/garmin/ 的 key 檔（gc-personal 預設路徑；key 不進 repo）。

用法：
  python3 scripts/garmin_pull.py                 # 近 365 天，輸出到 stdout
  python3 scripts/garmin_pull.py --since 2026-01-01 --public > research/garmin-monthly/2026-11.md
  --public  睡眠只給定性描述（不含時數），給公開 repo 用
  --gc PATH 指定 gc-personal 執行檔（預設 $GC_PERSONAL、~/garmin-env/bin/gc-personal、PATH）
"""
import argparse, datetime as dt, json, os, shutil, statistics as st, subprocess, sys
from collections import Counter, defaultdict

RUN = {"running", "treadmill_running", "virtual_run"}
BIKE = {"road_biking", "indoor_cycling", "virtual_ride", "cycling"}
STR = {"strength_training", "hiit", "indoor_cardio", "jump_rope", "indoor_rowing"}
GC = None


def find_gc(explicit):
    for c in [explicit, os.environ.get("GC_PERSONAL"), os.path.expanduser("~/garmin-env/bin/gc-personal"), shutil.which("gc-personal")]:
        if c and os.path.exists(c):
            return c
    sys.exit("找不到 gc-personal；用 --gc 指定或設 GC_PERSONAL")


def gc(args):
    r = subprocess.run([GC, "--no-color", "--quiet", *args], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return json.loads(r.stdout)


def activities(since):
    out, start = [], 0
    while True:
        page = gc(["activities", "--start", str(start), "--limit", "20"])  # limit > 20 會 HTTP 500
        if not page:
            break
        out += page
        if len(page) < 20 or page[-1]["startTimeLocal"][:10] < since:
            break
        start += 20
    seen, uniq = set(), []
    for a in out:
        if a["activityId"] not in seen and a["startTimeLocal"][:10] >= since:
            seen.add(a["activityId"]); uniq.append(a)
    return uniq


def chunks(start, end, days):
    d = start
    while d <= end:
        e = min(d + dt.timedelta(days=days - 1), end)
        yield d.isoformat(), e.isoformat()
        d = e + dt.timedelta(days=1)


def pace(a):
    return (a["duration"] / 60) / (a["distance"] / 1000)


def fmt(p):
    return f"{int(p)}:{int(round((p % 1) * 60)):02d}"


def main():
    global GC
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=(dt.date.today() - dt.timedelta(days=365)).isoformat())
    ap.add_argument("--recovery-days", type=int, default=56)
    ap.add_argument("--public", action="store_true")
    ap.add_argument("--gc")
    o = ap.parse_args()
    GC = find_gc(o.gc)
    today = dt.date.today()
    A = activities(o.since)
    R = [a for a in A if a["activityType"]["typeKey"] in RUN and a.get("distance", 0) > 1000]
    L = [f"# Garmin 月檢 {today.isoformat()}", "", f"區間 {o.since} → {today}，活動 {len(A)} 筆，跑步 {len(R)} 次。", ""]

    M = defaultdict(lambda: defaultdict(float))
    for a in A:
        t = a["activityType"]["typeKey"]; g = "run" if t in RUN else "bike" if t in BIKE else "str" if t in STR else "other"
        m = M[a["startTimeLocal"][:7]]
        m[g + "_n"] += 1; m[g + "_km"] += a.get("distance", 0) / 1000; m[g + "_h"] += a.get("duration", 0) / 3600
    L += ["## 每月訓練量", "", "| 月 | 跑次 | 跑 km | 騎次 | 騎 km | 肌力次 | 肌力 h |", "|---|---|---|---|---|---|---|"]
    for m in sorted(M):
        x = M[m]; L.append(f"| {m} | {int(x['run_n'])} | {x['run_km']:.0f} | {int(x['bike_n'])} | {x['bike_km']:.0f} | {int(x['str_n'])} | {x['str_h']:.1f} |")

    W = defaultdict(float); Wn = Counter(); Wmax = defaultdict(float)
    for a in R:
        k = dt.date.fromisoformat(a["startTimeLocal"][:10]).isocalendar()[:2]
        W[k] += a["distance"] / 1000; Wn[k] += 1; Wmax[k] = max(Wmax[k], a["distance"] / 1000)
    L += ["", "## 近 12 週週跑量", "", "| 週 | km | 次 | 最長 |", "|---|---|---|---|"]
    for k in sorted(W)[-12:]:
        L.append(f"| {k[0]}-W{k[1]:02d} | {W[k]:.1f} | {Wn[k]} | {Wmax[k]:.1f} |")

    Q = defaultdict(list)
    for a in R:
        hr = a.get("averageHR") or 0
        if 140 <= hr <= 152 and a["distance"] >= 5000:
            d = dt.date.fromisoformat(a["startTimeLocal"][:10]); Q[f"{d.year}Q{(d.month - 1) // 3 + 1}"].append(a)
    L += ["", "## 同心率配速（心率 140–152、≥ 5 km）", "", "| 季 | 次 | 配速 | 心率 | 步頻 |", "|---|---|---|---|---|"]
    for q in sorted(Q):
        x = Q[q]; L.append(f"| {q} | {len(x)} | {fmt(st.mean(pace(a) for a in x))} | {st.mean(a['averageHR'] for a in x):.0f} | {st.mean(a.get('averageRunningCadenceInStepsPerMinute', 0) for a in x):.0f} |")

    z = [0.0] * 5; cut = (today - dt.timedelta(days=90)).isoformat()
    for a in R:
        if a["startTimeLocal"][:10] >= cut:
            for i in range(5):
                z[i] += a.get(f"hrTimeInZone_{i + 1}", 0)
    tot = sum(z) or 1
    L += ["", "## 近 90 天跑步心率區間時間", "", " / ".join(f"Z{i + 1} {z[i] / tot * 100:.0f}%" for i in range(5)), "", f"Z1–2 合計 {(z[0] + z[1]) / tot * 100:.0f}%（目標 70%）。"]
    easy = sum(1 for a in R if a["startTimeLocal"][:10] >= cut and 0 < (a.get("averageHR") or 0) <= 140)
    n90 = sum(1 for a in R if a["startTimeLocal"][:10] >= cut)
    L.append(f"近 90 天 {n90} 次跑步中平均心率 ≤ 140 的有 {easy} 次。")

    L += ["", "## 最長的 5 次跑", ""]
    for a in sorted(R, key=lambda a: -a["distance"])[:5]:
        L.append(f"- {a['startTimeLocal'][:10]} {a['distance'] / 1000:.1f} km，{fmt(pace(a))}/km，心率 {a.get('averageHR') or 0:.0f}")
    best = {}
    for k, lab in [("fastestSplit_1000", "1 km"), ("fastestSplit_5000", "5 km"), ("fastestSplit_10000", "10 km")]:
        v = [(a[k], a["startTimeLocal"][:10]) for a in R if a.get(k)]
        if v:
            s, d = min(v); best[lab] = f"{int(s // 60)}:{int(s % 60):02d}（{d}）"
    L += ["", "最佳分段：" + "、".join(f"{k} {v}" for k, v in best.items())]

    rs = today - dt.timedelta(days=o.recovery_days)
    hrv = []
    for s, e in chunks(rs, today, 28):
        r = gc(["hrv-summaries", "--start-date", s, "--end-date", e]) or {}
        hrv += r.get("hrvSummaries", [])
    L += ["", f"## 恢復（近 {o.recovery_days} 天）", ""]
    if hrv:
        wk = [x["weeklyAvg"] for x in hrv if x.get("weeklyAvg")]; b = hrv[-1].get("baseline", {})
        L.append(f"- HRV 週平均 {min(wk)}–{max(wk)}，最近 {wk[-1]}；平衡區 {b.get('balancedLow')}–{b.get('balancedUpper')}；狀態 {dict(Counter(x['status'] for x in hrv))}")
    dd = []
    for s, e in chunks(rs, today, 28):
        r = gc(["daily-summaries", "--start-date", s, "--end-date", e]) or {}
        dd += r.get("data", [])
    rhr = [(d.get("heartRate") or {}).get("restingValue") for d in dd]; rhr = [v for v in rhr if v]
    if rhr:
        L.append(f"- 安靜心率 {min(rhr)}–{max(rhr)}，平均 {st.mean(rhr):.0f}")
    sl = []
    for s, e in chunks(rs, today, 21):
        r = gc(["sleep-summaries", "--start-date", s, "--end-date", e])
        if isinstance(r, list):
            sl += r
        elif isinstance(r, dict):
            sl += next((v for v in r.values() if isinstance(v, list)), [])
    dur = [x["sleepTimeSeconds"] for x in sl if x.get("sleepTimeSeconds")]
    if dur:
        short = sum(1 for v in dur if v < 6 * 3600)
        if o.public:
            L.append(f"- 睡眠：{len(dur)} 晚中 {short} 晚不足 6 小時" + ("，恢復仍是主要限制" if short > len(dur) / 2 else ""))
        else:
            L.append(f"- 睡眠：{len(dur)} 晚，平均 {st.mean(dur) / 3600:.1f} 小時，不足 6 小時 {short} 晚，最長 {max(dur) / 3600:.1f}")
    print("\n".join(L))


if __name__ == "__main__":
    main()
