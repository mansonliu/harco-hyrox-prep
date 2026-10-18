# 用法：python3 scripts/hr_chart.py <harco_laps.py 輸出的 json>  > svg 片段，貼進 _notes/02-harco.html 的 .hrc-wrap

import sys, json
d=json.load(open(sys.argv[1]))
B=d['B']; starts=d['starts']; ends=d['ends']; L=d['L']
W,H=720,300; ml,mr,mt,mb=40,64,40,30
pw,ph=W-ml-mr,H-mt-mb
T=B[-1][2]  # official finish in watch time
y0,y1=120,190
X=lambda t: ml+t/T*pw
Y=lambda h: mt+(y1-h)/(y1-y0)*ph
short={"滑雪機":"滑雪","推雪橇":"推","拉雪橇":"拉","波比跳遠":"波比","划船機":"划船","農夫走路":"農夫","負重弓箭步":"弓步","藥球投擲":"藥球"}
def mmss(s):
    m=int(s//60); return f"{m}:{s-60*m:04.1f}"
o=[]
o.append(f'<svg class="hrc" viewBox="0 0 {W} {H}" role="img" aria-label="HARCO 全程心率時間軸，淺色底為站點">')
# grid + y labels
for h in range(120,191,10):
    o.append(f'<line class="g" x1="{ml}" x2="{W-mr}" y1="{Y(h):.1f}" y2="{Y(h):.1f}"/>')
    o.append(f'<text x="{ml-6}" y="{Y(h)+4:.1f}" text-anchor="end">{h}</text>')
o.append(f'<text x="{ml-6}" y="{mt-24}" text-anchor="end">bpm</text>')
# x ticks
for m in range(0,43,5):
    o.append(f'<text x="{X(m*60):.1f}" y="{H-mb+18}" text-anchor="middle">{m}</text>')
o.append(f'<text x="{W-mr+6}" y="{H-mb+18}">分鐘</text>')
# segment bands with tooltips
work={"滑雪機":1,"推雪橇":3,"波比跳遠":6,"划船機":8,"農夫走路":10,"負重弓箭步":12,"藥球投擲":14}
for name,a,b,t,ro,rg in B:
    a=max(a,0); x=X(a); w=X(b)-X(a)
    tip=f"{name}｜官方 {mmss(t)}｜總排名 {ro}/767｜分組 {rg}/121"
    if name in work:
        i=work[name]; tip+=f"｜手錶動作圈 {mmss(L[i]['dur'])}、平均心率 {L[i]['avg']}"
    if name.startswith("Run"):
        o.append(f'<rect class="hit" x="{x:.1f}" y="{mt}" width="{w:.1f}" height="{ph}"><title>{tip}</title></rect>')
    else:
        o.append(f'<rect class="band" x="{x:.1f}" y="{mt}" width="{w:.1f}" height="{ph}"><title>{tip}</title></rect>')
        o.append(f'<text class="bl" x="{x+w/2:.1f}" y="{mt-8}" text-anchor="middle">{short[name]}</text>')
# avg line
o.append(f'<line class="avg" x1="{ml}" x2="{W-mr}" y1="{Y(170):.1f}" y2="{Y(170):.1f}"/>')
o.append(f'<text class="al" x="{W-mr+6}" y="{Y(170)+4:.1f}">平均 170</text>')
# hr polyline (race portion only)
pts=[]
mx=(0,0)
for lap in L[:15]:
    for t,h in lap['pts']:
        if t<=T:
            pts.append(f"{X(t):.1f},{Y(max(min(h,y1),y0)):.1f}")
            if h>mx[1]: mx=(t,h)
o.append(f'<polyline class="hr" points="{" ".join(pts)}"/>')
o.append(f'<circle class="pk" cx="{X(mx[0]):.1f}" cy="{Y(mx[1]):.1f}" r="4"/>')
o.append(f'<text class="pl" x="{X(mx[0])-6:.1f}" y="{Y(mx[1])-2:.1f}" text-anchor="end">最高 {mx[1]}</text>')
o.append('</svg>')
print("\n".join(o))
