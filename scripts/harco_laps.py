# 用法：python3 scripts/harco_laps.py <activity.tcx> <out.json>
# 對齊 Garmin 手動圈數與 HARCO 官方分段（OFF＝官方起跑 13:45:05.148 減手錶起點 13:45:03），印出站內拆解與 HYROX 推估

import sys, json, itertools, xml.etree.ElementTree as ET
from datetime import datetime
ns={'t':'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
r=ET.parse(sys.argv[1]).getroot()
def ts(s): return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
laps=r.findall('.//t:Lap',ns)
t0=ts(laps[0].get('StartTime'))
L=[]
for l in laps:
    hrs=[]
    for tp in l.iter('{%s}Trackpoint'%ns['t']):
        h=tp.find('t:HeartRateBpm/t:Value',ns)
        if h is not None: hrs.append((ts(tp.find('t:Time',ns).text)-t0,int(h.text)))
    L.append(dict(dur=float(l.find('t:TotalTimeSeconds',ns).text),avg=int(l.find('t:AverageHeartRateBpm/t:Value',ns).text),mx=int(l.find('t:MaximumHeartRateBpm/t:Value',ns).text),pts=hrs))
ends=list(itertools.accumulate(x['dur'] for x in L))
starts=[0]+ends[:-1]
OFF=2.148  # official start 13:45:05.148 vs watch start 13:45:03
seg=[("Run 1",133.954,647,86),("滑雪機",220.126,662,94),("Run 2",102.690,609,80),("推雪橇",101.545,434,52),
("Run 3",105.393,469,68),("拉雪橇",182.255,500,65),("Run 4",101.117,401,58),("波比跳遠",214.425,331,42),
("Run 5",109.449,288,44),("划船機",201.914,340,42),("Run 6",104.114,351,45),("農夫走路",111.803,410,54),
("Run 7",105.686,208,25),("負重弓箭步",257.295,494,66),("Run 8",111.325,287,34),("藥球投擲",355.450,517,70)]
cum=0;B=[]
for name,t,ro,rg in seg:
    B.append((name,cum+OFF,cum+t+OFF,t,ro,rg)); cum+=t
print("official total %.3f"%cum)
def mmss(s,dec=1):
    s=round(s,dec); m=int(s//60); r=s-60*m
    return f"{m}:{r:0{3+dec if dec else 2}.{dec}f}" if dec else f"{m}:{int(round(r)):02d}"
# station work laps (garmin lap index 0-based) and station index in B
work={"滑雪機":1,"推雪橇":3,"波比跳遠":6,"划船機":8,"農夫走路":10,"負重弓箭步":12,"藥球投擲":14}
rows=[]
for name,a,b,t,ro,rg in B:
    if name.startswith("Run"): continue
    if name in work:
        i=work[name]; ws,we=starts[i],ends[i]
        ent=ws-a; ex=b-we
        rows.append((name,t,L[i]['dur'],ent,ex,ent+ex,L[i]['avg'],L[i]['mx'],ro,rg))
    else: # pull: start missed
        we=ends[4]; ex=b-we
        rows.append((name,t,None,None,ex,None,None,None,ro,rg))
for r_ in rows: print(r_)
tot_nonwork=sum(x[5] for x in rows if x[5] is not None)+rows[2][4]
print("nonwork excl pull entry: %.1f s = %s"%(tot_nonwork,mmss(tot_nonwork)))
runs=[x for x in B if x[0].startswith("Run")]
print("runs total",mmss(sum(x[3] for x in runs)),"run2-8 avg",mmss(sum(x[3] for x in runs[1:])/7))
st=[x for x in B if not x[0].startswith("Run")]
print("stations total",mmss(sum(x[3] for x in st)))
print("Run7/Run2 %.3f Run8/Run2 %.3f"%(runs[6][3]/runs[1][3],runs[7][3]/runs[1][3]))
# projection
fac={"滑雪機":(2.0,2.1),"推雪橇":(2.0,2.2),"拉雪橇":(2.0,2.2),"波比跳遠":(2.1,2.3),"划船機":(2.0,2.1),"農夫走路":(2.0,2.3),"負重弓箭步":(2.1,2.3),"藥球投擲":(2.1,2.4)}
lo=hi=0;proj=[]
for x in rows:
    base=x[2] if x[2] is not None else (x[1]-x[4])  # pull: entry+work
    a,b=fac[x[0]]
    proj.append((x[0],base,a,b,base*a,base*b)); lo+=base*a; hi+=base*b
for p in proj: print(p[0],mmss(p[1]),p[2],p[3],mmss(p[4],0),mmss(p[5],0))
print("stations proj",mmss(lo,0),mmss(hi,0))
for runpace in (300,320):
    for rox in (360,540):
        pass
print("total low",mmss(lo+8*300+360,0),"high",mmss(hi+8*320+540,0))
json.dump(dict(B=B,starts=starts,ends=ends,L=[{k:v for k,v in x.items()} for x in L]),open(sys.argv[2],'w'),ensure_ascii=False)
