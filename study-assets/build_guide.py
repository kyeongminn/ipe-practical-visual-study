from pathlib import Path
from html import escape as esc
import math

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '정보처리기사_핵심이론_그림정리.html'

def txt(x,y,t,cls='',anchor='middle'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(t)}</text>'

def rect(x,y,w,h,t='',cls='node',rx=9):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>' + (txt(x+w/2,y+h/2+5,t) if t else '')

def line(x1,y1,x2,y2,cls='',arrow=False):
    end=' marker-end="url(#arrow)"' if arrow else ''
    return f'<path d="M{x1},{y1} L{x2},{y2}" class="edge {cls}"{end}/>'

def path(d,cls='',arrow=False):
    end=' marker-end="url(#arrow)"' if arrow else ''
    return f'<path d="{d}" class="edge {cls}"{end}/>'

def circle(x,y,t='',r=17,cls='node'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>'+(txt(x,y+5,t) if t else '')

def svg(content,label,w=360,h=160,cls=''):
    return f'<svg class="diagram {cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label,quote=True)}"><title>{esc(label)}</title>{content}</svg>'

def flow(labels,kind=''):
    # Conceptual sketches; these are deliberately not labeled as formal UML.
    n=len(labels); w=360; cell=92 if n==3 else 134; gap=(w-24-n*cell)/(n-1) if n>1 else 0
    out=''
    for i,label in enumerate(labels):
        x=12+i*(cell+gap)
        out+=rect(x,33,cell,42,label,'node '+('accent' if i==n-1 else ''))
        if i<n-1: out+=line(x+cell,54,x+cell+gap-5,54,arrow=True)
    if kind: out+=txt(180,108,kind,'muted')
    return svg(out,' → '.join(labels)+((': '+kind) if kind else ''),h=125)

def card(title,en,visual,body,tag='',cls=''):
    if '<div' in body:
        description, extra = body.split('<div', 1)
        content = f'<p>{description}</p><div{extra}'
    else:
        content = f'<p>{body}</p>'
    return f'<article class="concept {cls}"><div class="card-top"><h3>{title}</h3>{f"<span class=tag>{tag}</span>" if tag else ""}</div><div class="en">{en}</div>{visual}{content}</article>'

def note(text): return f'<div class="note"><b>구분 포인트</b><span>{text}</span></div>'
def source(text,url): return f'<a class="source" href="{url}" target="_blank" rel="noopener noreferrer">↗ {text}</a>'
def section(id,no,title,sub,body,src=''):
    return f'<section id="{id}" class="chapter"><header class="chapter-head"><span class="chapter-no">{no}</span><div><p class="eyebrow">CONCEPT MAP / {no}</p><h2>{title}</h2><p>{sub}</p></div></header>{body}<div class="source-row">{src}</div></section>'

CSS = '''
:root{--bg:#f3f5f9;--paper:#fff;--ink:#1b2541;--muted:#56617a;--line:#dbe1ec;--blue:#345ce0;--purple:#7751cd;--teal:#087f84;--amber:#9c650c;--soft:#edf1ff;--nav:#14213c;--red:#b8434c;--radius:18px;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif}a{color:var(--blue)}button,input,select{font:inherit}button,a,input,select,summary{-webkit-tap-highlight-color:transparent}button{cursor:pointer}button:focus-visible,a:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #b27600;outline-offset:4px}button{border:1px solid var(--line);border-radius:10px;padding:9px 15px;background:var(--paper);color:var(--ink);min-height:44px}button:hover{background:var(--soft)}button.primary{background:var(--blue);border-color:var(--blue);color:white}p{margin:8px 0 0}h1,h2,h3,h4{margin:0;line-height:1.35}h3{font-size:19px}h4{font-size:17px}small,.small{font-size:13px;color:var(--muted)}b,strong{font-weight:700}code{font:14px/1.6 Consolas,monospace;background:#edf0f7;padding:2px 5px;border-radius:4px}pre{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.8 Consolas,'Malgun Gothic',monospace}pre code{background:none;padding:0}.layout{display:grid;grid-template-columns:248px minmax(0,1fr);max-width:1680px;margin:auto}.sidebar{background:var(--nav);color:#fff;padding:32px 20px;position:sticky;top:0;height:100vh;overflow:auto}.brand{font-size:12px;letter-spacing:2px;color:#a9b9df}.sidebar h2{font-size:25px;margin:13px 0 26px}.sidebar nav{display:flex;flex-direction:column;gap:5px}.sidebar a{display:flex;align-items:center;gap:12px;text-decoration:none;color:#cbd5ee;padding:11px 10px;border-radius:10px;font-size:14px}.sidebar a span{font-size:12px;color:#9bafdf}.sidebar a:hover,.sidebar a.active{background:#2b3d60;color:white}.sidebar .nav-footer{font-size:12px;color:#adbad6;margin-top:30px;line-height:1.8}.sidebar .nav-footer b{color:#dce7ff}main{min-width:0;padding:38px clamp(20px,4vw,66px) 70px}.topline{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}.eyebrow{font:700 11px/1.6 system-ui,sans-serif;letter-spacing:1.6px;color:var(--blue);margin:0 0 9px}.topline .eyebrow{margin:0}.hero{padding:38px 0 32px}.hero h1{font-size:clamp(30px,3.6vw,48px);letter-spacing:-1.8px}.hero h1 em{font-style:normal;color:var(--blue)}.hero>p{font-size:17px;max-width:720px;color:var(--muted);margin-top:17px}.hero-bottom{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}.pill,.tag{display:inline-block;border-radius:20px;background:var(--soft);color:var(--blue);font-size:12px;font-weight:700;padding:4px 10px}.pill{color:var(--muted);background:#e8ecf4}.overview{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:58px}.overview a{background:var(--paper);border:1px solid var(--line);text-decoration:none;padding:16px;border-radius:13px;color:var(--ink)}.overview a:hover{border-color:var(--blue);transform:translateY(-2px)}.overview b{font-size:23px;display:block;color:var(--blue);margin-bottom:5px}.overview span{font-size:13px}.chapter{margin-bottom:70px}.chapter-head{display:flex;align-items:flex-start;gap:18px;margin-bottom:25px;border-top:1px solid var(--line);padding-top:30px}.chapter-head h2{font-size:28px;letter-spacing:-.8px}.chapter-head p:last-child{font-size:15px;color:var(--muted);margin-top:7px}.chapter-no{font:700 21px/1 system-ui,sans-serif;background:var(--ink);color:white;display:grid;place-items:center;flex:0 0 52px;height:52px;border-radius:16px}.grid{display:grid;gap:17px;grid-template-columns:repeat(2,minmax(0,1fr))}.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}.concept{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:21px;min-width:0;break-inside:avoid}.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.en{font:12px/1.5 system-ui,sans-serif;color:var(--muted);margin:3px 0 6px;overflow-wrap:anywhere}.concept p{font-size:14px}.concept p b{color:var(--blue)}.diagram{width:100%;height:auto;display:block;overflow:visible;margin:10px 0;max-height:290px}.diagram text{fill:var(--ink);font:14px 'Malgun Gothic',system-ui,sans-serif}.diagram text.muted{fill:var(--muted);font-size:12px}.diagram text.large{font-size:23px;font-weight:700}.diagram .node{fill:#fff;stroke:#9caac5;stroke-width:1.6}.diagram .accent{fill:#edf1ff;stroke:var(--blue)}.diagram .warm{fill:#fff1d9;stroke:#ba861e}.diagram .filled{fill:var(--ink);stroke:var(--ink)}.diagram .edge{fill:none;stroke:#637492;stroke-width:1.8}.diagram .dash{stroke-dasharray:6 5}.diagram .strong{stroke:var(--blue);stroke-width:3}.diagram .dotted{stroke-dasharray:2 4}.diagram .off{opacity:.24}.diagram .hit{fill:var(--blue);stroke:var(--blue)}.diagram .hittext{fill:white}.diagram .zone{fill:#f0f4ff;stroke:#bfcae1;stroke-width:1.3}.diagram .diamond{fill:white;stroke:var(--ink);stroke-width:1.8}.note{display:flex;gap:14px;margin:19px 0;padding:15px 18px;border-left:4px solid var(--blue);border-radius:0 10px 10px 0;background:#e9eefc;font-size:14px}.note>b{white-space:nowrap;color:var(--blue)}.source-row{display:flex;flex-wrap:wrap;gap:16px;margin-top:17px}.source{font-size:12px;color:var(--muted)}.subhead{margin:30px 0 17px;display:flex;gap:12px;align-items:center;font-size:20px}.subhead small{font-size:13px;font-weight:400}.branch-tree{display:grid;grid-template-columns:1fr 1fr;gap:18px}.family{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:20px}.family h3{display:flex;justify-content:space-between;padding-bottom:12px;border-bottom:2px solid var(--blue)}.family.behavior h3{border-color:var(--purple)}.tree-list{display:grid;gap:9px;margin-top:15px;padding:0;list-style:none}.tree-list li{border-left:2px solid #c8d3ee;padding:4px 0 4px 14px;display:flex;justify-content:space-between;gap:10px;font-size:14px}.tree-list li span{color:var(--muted);font-size:12px}.interaction-group{background:#f3effc;padding:12px;border-radius:10px;margin-top:12px}.interaction-group strong{font-size:14px;color:var(--purple)}.interaction-group .tree-list{margin:8px 0 0}.tiny-grid .concept{padding:17px}.tiny-grid h3{font-size:17px}.tiny-grid .diagram{max-height:180px}.caption{font-size:13px;color:var(--muted)}.legendline{display:flex;flex-wrap:wrap;gap:18px;font-size:13px;padding:13px 0}.legendline strong{font-family:Consolas,monospace}.ribbon{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:18px 0;gap:10px}.ribbon>div{padding:18px;border-radius:13px;background:var(--soft);border-top:3px solid var(--blue);font-size:14px}.ribbon h3{font-size:18px}.ribbon .big{font-size:26px;color:var(--blue);font-weight:700;display:block;margin:8px 0}.ribbon .mid{background:#f1edfb;border-color:var(--purple)}.ribbon .high{background:#e7f4f2;border-color:var(--teal)}.ribbon .mid .big{color:var(--purple)}.ribbon .high .big{color:var(--teal)}.steps{display:flex;gap:9px;align-items:center;margin-top:16px;flex-wrap:wrap}.steps>div{flex:1;min-width:140px;border:1px solid var(--line);background:var(--paper);border-radius:12px;padding:18px}.steps .arrow{color:var(--blue);font-size:24px}.calc{background:var(--ink);color:white;border-radius:18px;padding:24px;margin-top:25px}.calc h3{font-size:20px}.calc .caption{color:#c4d0e8}.calc-controls{display:flex;gap:16px;flex-wrap:wrap;margin:18px 0}.calc label{font-size:13px;display:flex;flex-direction:column;gap:6px}.calc input,.calc select{padding:9px 10px;border-radius:8px;border:1px solid #677a9c;min-height:44px;max-width:100%;background:#fff;color:var(--ink)}.calc .results{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-top:18px;border-top:1px solid #50607e}.results span{font-size:13px;color:#bdcbe6}.results output{font:700 28px/1.4 system-ui,sans-serif;display:block}.results small{color:#bdcbe6}.formula{font:16px/1.8 Consolas,monospace;margin-top:13px}.formula.error{color:#ffd098}.patterns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.patterns .concept{padding:18px}.patterns h3{font-size:18px}.patterns .diagram{max-height:160px}.category-title{display:flex;align-items:center;gap:12px;padding:12px 0;margin-top:20px}.category-title .num{font-size:32px;color:var(--blue);font-weight:700}.category-title h3{font-size:21px}.category-title .en{margin:0}.structural .num{color:var(--teal)}.behavioral .num{color:var(--purple)}.pattern-cue{font-size:12px;background:#f0f3fa;padding:7px 10px;border-radius:7px;margin-top:10px}.matrix-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px;background:var(--paper)}th,td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top}th{background:#eaf0fa;font-weight:700}td .tag{padding:2px 7px}.matrix-table th,.matrix-table td{text-align:center}.matrix-table input{width:19px;height:19px;accent-color:var(--blue);cursor:pointer}.matrix-table label{display:flex;align-items:center;justify-content:center;gap:7px;min-height:30px}.matrix-table tr.chosen{background:#eff3ff}.preset-row{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}.preset-row button{font-size:13px}.coverage{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.meter{padding:13px;border:1px solid var(--line);border-radius:10px;background:var(--paper)}.meter strong{font:700 25px system-ui,sans-serif;display:block;margin-top:4px;color:var(--blue)}.track{height:6px;background:#e5eaf4;border-radius:5px;margin-top:10px;overflow:hidden}.track i{display:block;height:100%;background:var(--blue);width:0;transition:width .2s}.coverage-note{font-size:13px;min-height:42px;color:var(--muted);margin-top:13px}.code-panel{background:#18243c;color:#dce7ff;padding:23px;border-radius:15px}.code-panel code{color:inherit}.code-panel .ln{color:#8da7d4}.technique{display:flex;align-items:flex-start;gap:12px;margin:14px 0}.technique .symbol{font-size:20px;font-weight:700;background:var(--soft);color:var(--blue);border-radius:10px;width:42px;height:42px;display:grid;place-items:center;flex:0 0 42px}.technique p{margin-top:2px}.principles .concept{position:relative}.principles .n{font:700 12px system-ui,sans-serif;letter-spacing:1px;color:var(--blue);margin-bottom:10px}.principles .concept.wide{grid-column:1/-1}.recall-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}details.recall{border:1px solid var(--line);border-radius:12px;background:var(--paper);padding:15px;break-inside:avoid}details.recall summary{cursor:pointer;font-size:14px;font-weight:700;min-height:44px;list-style-position:inside}details.recall p{font-size:14px;color:var(--blue);border-top:1px solid var(--line);padding-top:10px}details.recall .q-no{color:var(--muted);font-size:11px;display:block;margin-bottom:4px}.recall-actions{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap}.closing{border-top:1px solid var(--line);padding-top:25px;color:var(--muted);font-size:13px}.bottom-link{display:inline-block;margin-top:15px}.utility{display:flex;gap:9px}.counter{font:12px/1.6 system-ui,sans-serif;color:var(--muted)}
@media(min-width:1550px){.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:1180px){.layout{grid-template-columns:210px minmax(0,1fr)}.sidebar{padding:28px 13px}main{padding:28px 26px}.patterns,.grid.three,.recall-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.overview{grid-template-columns:repeat(4,minmax(0,1fr))}.overview a{padding:12px}}
@media(max-width:850px){.layout{display:block}.sidebar{position:static;height:auto;padding:18px 22px}.sidebar .brand{display:none}.sidebar h2{font-size:19px;margin:0 0 13px}.sidebar nav{flex-direction:row;flex-wrap:wrap;gap:4px}.sidebar nav a{padding:7px 10px;font-size:12px;gap:5px}.sidebar .nav-footer{display:none}main{padding:25px 22px}.hero{padding-top:24px}.hero h1{letter-spacing:-1px}.chapter-head h2{font-size:26px}.chapter{margin-bottom:48px}}
@media(max-width:560px){body{font-size:15px}main{padding:22px 15px}.hero h1{font-size:31px}.hero>p{font-size:15px}.overview{grid-template-columns:repeat(2,minmax(0,1fr));margin-bottom:32px}.grid,.grid.three,.patterns,.branch-tree,.recall-grid{grid-template-columns:1fr}.concept{padding:18px}.chapter-head{gap:11px;padding-top:22px}.chapter-head h2{font-size:23px}.chapter-no{flex-basis:42px;height:42px;border-radius:12px;font-size:17px}.note{display:block;padding:13px}.note>b{display:block;margin-bottom:5px}.ribbon{grid-template-columns:1fr}.ribbon .big{font-size:22px}.steps{display:grid;grid-template-columns:1fr}.steps .arrow{text-align:center;transform:rotate(90deg)}.coverage{gap:6px}.meter{padding:9px;font-size:12px}.meter strong{font-size:21px}.calc{padding:19px}.calc-controls{display:grid;grid-template-columns:1fr}.calc .results{gap:10px}.results output{font-size:23px}.results small{font-size:11px}.formula{font-size:13px}.topline{align-items:flex-start}.topline .eyebrow{font-size:10px;letter-spacing:1px}.utility button{padding:7px 11px;font-size:12px}.tree-list li{display:block}.tree-list li span{display:block}.matrix-table th,.matrix-table td{padding:10px 7px}.principles .concept.wide{grid-column:auto}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{transition:none!important;animation:none!important}}
@media print{@page{size:A4;margin:13mm}html{scroll-behavior:auto}body{background:white;font-size:11px;line-height:1.5}.layout{display:block;max-width:none}.sidebar,.utility,.overview,.calc,.preset-row,.recall-actions,.source-row,.bottom-link,.interactive-only{display:none!important}main{padding:0}.hero{padding:0 0 18px}.hero h1{font-size:29px}.hero>p{font-size:12px}.hero-bottom{margin-top:10px}.pill{font-size:10px}.chapter{margin-bottom:22px}.chapter-head{padding-top:15px;margin-bottom:13px;break-after:avoid}.chapter-head h2{font-size:23px}.chapter-head p:last-child{font-size:11px}.chapter-no{flex-basis:36px;height:36px;font-size:16px}.chapter-head .eyebrow{font-size:9px;margin-bottom:3px}.grid,.grid.three,.patterns{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.concept,.patterns .concept{padding:12px;border-radius:10px;box-shadow:none}.concept h3,.patterns h3{font-size:15px}.concept p{font-size:11px}.en{font-size:10px}.diagram{max-height:145px;margin:5px 0}.note{font-size:11px;margin:12px 0;padding:10px}.source{font-size:10px}.tag{font-size:9px}.subhead{font-size:17px;margin:17px 0 10px;break-after:avoid}.caption{font-size:10px}.family{padding:12px}.family h3{font-size:16px}.tree-list li{font-size:11px}.tree-list li span{font-size:10px}.ribbon>div{font-size:10px;padding:12px}.ribbon .big{font-size:20px}.steps>div{padding:10px;font-size:11px}.steps .arrow{font-size:18px}.pattern-cue{font-size:10px}.category-title{break-after:avoid}.category-title h3{font-size:18px}table{font-size:11px}th,td{padding:6px 8px}.code-panel{padding:13px}pre{font-size:11px}.coverage{font-size:11px}.meter strong{font-size:21px}.recall-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}details.recall{padding:10px}details.recall summary,details.recall p{font-size:11px;min-height:0}.closing{font-size:10px}.chapter-head,.concept,.family,.note,.ribbon,.steps,.coverage,.matrix-wrap,.code-panel{break-inside:avoid}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''

defs='''<svg width="0" height="0" aria-hidden="true" style="position:absolute"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#637492" stroke-width="1.5"/></marker></defs></svg>'''

# 01. UML relationship notation: hand-positioned endpoints avoid ambiguous diamonds.
rel=[]
for title,en,left,right,kind,desc,tag in [
 ('연관 관계','Association','학생','강의','association','객체 사이의 <b>구조적인 연결</b>. 학생이 강의를 수강한다.','알고 있다'),
 ('집합 / 집약 관계','Aggregation','팀','선수','aggregation','느슨한 전체–부분. 팀이 없어져도 선수는 <b>독립적으로 존재</b>할 수 있다.','빈 마름모'),
 ('합성 / 포함 관계','Composition','주문','주문항목','composition','강한 전체–부분. 주문에 속한 항목의 <b>생명주기를 전체가 관리</b>한다.','채운 마름모'),
 ('일반화 관계','Generalization','고양이','동물','generalization','구체적인 자식은 일반적인 부모의 한 종류. <b>is-a · 상속</b>.','실선 + 삼각형'),
 ('의존 관계','Dependency','보고서생성기','프린터','dependency','인자·지역 변수·메서드 호출 등으로 다른 요소를 <b>사용</b>한다.','점선 + 열린 화살촉'),
 ('실체화 관계','Realization','카드결제','결제 명세','realization','인터페이스 등 명세의 계약을 실제로 <b>구현</b>한다.','점선 + 삼각형')]:
    s=rect(8,35,112,49,left)+rect(240,35,112,49,right)
    if kind=='association':s+=line(120,59,240,59)+txt(131,49,'*','muted')+txt(228,49,'*','muted')
    if kind in ('aggregation','composition'):
        s+=line(145,59,240,59)+f'<polygon points="120,59 133,51 146,59 133,67" class="{"filled" if kind=="composition" else "diamond"}"/>'
    if kind in ('generalization','realization'):
        s+=line(120,59,223,59,'dash' if kind=='realization' else '')+'<polygon points="240,59 223,49 223,69" class="diamond"/>'
    if kind=='dependency':s+=line(120,59,238,59,'dash',True)
    caption={'association':'선만으로도 연관을 표현','aggregation':'◇는 전체 쪽','composition':'◆는 전체 쪽','generalization':'삼각형은 부모 쪽 →','dependency':'사용하는 쪽 → 사용되는 쪽','realization':'삼각형은 명세 쪽 →'}[kind]
    s+=txt(180,115,caption,'muted')
    rel.append(card(title,en,svg(s,f'{title}: {left}에서 {right}, {caption}',h=137),desc,tag))
use=''
for en,left,right,desc in [('include','주문하기','결제하기','<b>포함</b>: 기본 유스케이스가 공통 기능을 반드시 포함. 기본 → 포함되는 기능.'),('extend','쿠폰 적용','주문하기','<b>확장</b>: 조건에 따라 기본 기능에 행동을 추가. 확장 기능 → 기본 기능.')]:
    s=f'<ellipse cx="69" cy="59" rx="62" ry="29" class="node"/>'+txt(69,64,left)+f'<ellipse cx="291" cy="59" rx="62" ry="29" class="node"/>'+txt(291,64,right)+line(132,59,227,59,'dash',True)+txt(180,43,'«'+en+'»','muted')
    use+=card('«'+en+'»','Use case relationship',svg(s,left+' → '+right+' '+en,h=108),desc)
body='<div class="grid">'+''.join(rel)+'</div>'+note('마름모는 <b>전체</b>에 붙이고, 빈 삼각형은 <b>부모·인터페이스</b>를 향한다. 화살표가 없는 연관선은 양방향 탐색을 확정한다는 뜻이 아니라, 탐색 방향을 생략한 표기일 수 있다.')+'<h3 class="subhead">유스케이스에서 추가로 구분할 관계</h3><div class="grid">'+use+'</div>'
chapters=[section('uml-rel','01','UML 관계 종류','선의 종류 → 끝 모양 → 방향 순서로 읽으면 구분이 쉬워집니다.',body,source('Sparx · Class diagram','https://sparxsystems.com/resources/tutorials/uml2/class-diagram.html'))]

# 02. Fourteen diagram types with a tiny recognizable example each.
struct=[('클래스','Class','속성·연산·클래스 관계'),('객체','Object','특정 시점의 인스턴스'),('패키지','Package','모델의 논리적 묶음'),('컴포넌트','Component','소프트웨어 구성 단위'),('배치','Deployment','장치·실행 환경에 배포'),('복합 구조','Composite structure','내부 부품·포트·연결'),('프로파일','Profile','스테레오타입으로 UML 확장')]
behavior=[('유스케이스','Use case','사용자 관점의 기능'),('활동','Activity','작업·분기·병렬 흐름'),('상태 머신','State machine','이벤트에 따른 상태 변화')]
inter=[('시퀀스 / 순차','Sequence','시간 순서의 메시지'),('커뮤니케이션','Communication','객체 연결 + 메시지 번호'),('상호작용 개요','Interaction overview','상호작용 간 제어 흐름'),('타이밍','Timing','시간에 따른 상태·값')]
tree=lambda items:'<ul class="tree-list">'+''.join(f'<li><b>{a}</b><span>{c}</span></li>' for a,b,c in items)+'</ul>'
body='<div class="branch-tree"><div class="family"><h3>구조 · 정적 <span class="tag">7종</span></h3>'+tree(struct)+'</div><div class="family behavior"><h3>행위 · 동적 <span class="tag">7종</span></h3>'+tree(behavior)+'<div class="interaction-group"><strong>↳ 상호작용 다이어그램 4종 포함</strong>'+tree(inter)+'</div></div></div>'
body+=note('이 정리는 프로파일을 포함한 <b>14종 분류</b>를 사용한다. 일부 국내 수험서의 <b>13종 분류는 프로파일을 제외</b>한다. 13종이면 구조 6 + 행위 7이며, 상호작용 4종은 행위에 포함된다.')
def umlmini(key):
    if key=='Class':
        s=rect(81,10,198,130,rx=2)+txt(180,36,'회원')+line(81,48,279,48)+txt(94,72,'− name : String',anchor='start')+line(81,87,279,87)+txt(94,112,'+ login() : boolean',anchor='start')
    elif key=='Object':s=rect(76,27,208,94,rx=2)+txt(180,51,'minsu : 회원')+line(122,56,238,56)+line(76,64,284,64)+txt(180,95,'name = "민수"')
    elif key=='Package':s=rect(25,30,125,80,'',rx=1)+rect(25,14,55,20,'',rx=1)+txt(87,77,'주문')+rect(215,30,120,80,'',rx=1)+rect(215,14,55,20,'',rx=1)+txt(275,77,'결제')+line(150,70,213,70,'dash',True)
    elif key=='Component':s=rect(25,38,125,65,'주문 서비스',rx=2)+rect(215,38,120,65,'결제 서비스',rx=2)+rect(131,45,12,15,rx=0)+rect(127,47,7,4,rx=0)+rect(127,54,7,4,rx=0)+rect(316,45,12,15,rx=0)+rect(312,47,7,4,rx=0)+rect(312,54,7,4,rx=0)+line(150,70,215,70)+circle(183,70,r=7)
    elif key=='Deployment':s=path('M30 36 L46 22 H150 V96 L134 111 H30 Z')+line(30,36,134,36)+line(134,36,150,22)+line(134,36,134,111)+txt(82,61,'«device»','muted')+txt(82,84,'서버')+rect(209,36,125,75,'DB 노드',rx=2)+line(150,69,209,69)
    elif key=='Composite structure':s=rect(24,12,312,127,rx=1)+txt(180,36,'주문 처리기')+rect(48,57,101,58,'검증 부품',rx=2)+rect(211,57,101,58,'저장 부품',rx=2)+line(149,86,211,86)+rect(18,75,12,22,rx=0)+rect(330,75,12,22,rx=0)
    elif key=='Profile':s=rect(29,27,137,91,rx=2)+txt(98,56,'«stereotype»','muted')+txt(98,85,'Entity')+rect(221,27,111,91,rx=2)+txt(276,56,'«metaclass»','muted')+txt(276,85,'Class')+line(166,76,209,76)+'<polygon points="221,76 209,70 209,82" class="filled"/>'
    elif key=='Use case':s=circle(34,42,r=10)+line(34,52,34,88)+line(16,68,52,68)+line(34,88,17,111)+line(34,88,51,111)+txt(34,136,'사용자','muted')+rect(102,15,222,126,rx=0)+txt(213,37,'쇼핑 시스템','muted')+'<ellipse cx="213" cy="83" rx="75" ry="29" class="node"/>'+txt(213,88,'상품 주문')+line(52,68,138,83)
    elif key=='Activity':s=circle(44,77,r=9,cls='filled')+line(53,77,76,77,arrow=True)+rect(78,55,90,44,'검증')+line(168,77,198,77,arrow=True)+'<polygon points="220,55 242,77 220,99 198,77" class="diamond"/>'+line(242,77,265,77,arrow=True)+rect(266,55,82,44,'저장')+txt(260,49,'정상','muted')+path('M220 99 V126 H122',arrow=True)+txt(163,119,'오류 처리','muted')
    elif key=='State machine':s=rect(14,52,86,48,'대기')+rect(135,52,86,48,'진행')+rect(256,52,90,48,'완료')+line(100,76,133,76,arrow=True)+line(221,76,254,76,arrow=True)+txt(117,40,'시작','muted')+txt(239,40,'종료','muted')
    elif key=='Sequence':s=rect(31,10,103,31,'클라이언트')+rect(225,10,103,31,'서버')+line(82,41,82,146,'dash')+line(276,41,276,146,'dash')+rect(270,58,12,72,rx=0)+line(82,70,268,70,arrow=True)+txt(175,61,'1: 요청','muted')+line(270,116,84,116,'dash',True)+txt(175,109,'2: 응답','muted')+txt(18,131,'시간 ↓','muted',anchor='start')
    elif key=='Communication':s=rect(14,61,110,45,'클라이언트')+rect(236,61,110,45,'서비스')+line(124,84,236,84)+line(139,54,220,54,arrow=True)+txt(180,40,'1: 요청','muted')+line(220,122,139,122,arrow=True)+txt(180,145,'2: 응답','muted')
    elif key=='Interaction overview':s=circle(36,77,r=8,cls='filled')+line(44,77,65,77,arrow=True)+rect(67,45,96,64,rx=1)+txt(115,65,'ref','muted')+txt(115,89,'인증 상호작용')+line(163,77,198,77,arrow=True)+rect(200,45,123,64,rx=1)+txt(261,65,'ref','muted')+txt(261,89,'주문 상호작용')
    else:s=line(60,23,60,124)+line(60,124,336,124,arrow=True)+txt(48,43,'ON','muted',anchor='end')+txt(48,97,'OFF','muted',anchor='end')+path('M60 91 H121 V42 H232 V91 H320','strong')+txt(180,148,'시간 →','muted')
    return svg(s,key+' 개념 예시',h=160)
body+='<h3 class="subhead">그림으로 알아보는 14가지 <small>이해용 축약 예시</small></h3><div class="grid three tiny-grid">'
for a,b,c in struct+behavior+inter: body+=card(a,b,umlmini(b),c, '구조' if (a,b,c) in struct else ('상호작용' if (a,b,c) in inter else '행위'))
body+='</div>'+note('<b>시퀀스</b>는 시간 순서, <b>커뮤니케이션</b>은 연결 구조와 메시지 번호가 중심이다. <b>상태 머신</b>은 객체의 상태, <b>활동</b>은 작업 흐름이 중심이다.')
chapters.append(section('uml-types','02','UML 다이어그램 종류','무엇으로 구성되는가 = 구조 / 어떻게 움직이는가 = 행위',body,source('Sparx · UML 2, 14 diagram types','https://sparxsystems.com/resources/tutorials/uml2//')))

# 03. COCOMO modes and model detail are separate dimensions.
body='<div class="note"><b>COCOMO 81</b><span>Barry Boehm의 <b>Constructive Cost Model</b>. 소프트웨어 규모(LOC)와 개발 특성으로 <b>노력·기간·비용</b>을 추정하는 알고리즘 모형.</span></div><h3 class="subhead">A. 프로젝트 개발 유형 <small>어떤 성격의 개발인가?</small></h3><div class="ribbon">'
for title,en,size,desc,cls in [
 ('조직형','Organic','약 5만 라인 이하','비교적 작고 익숙한 업무 · 경험 있는 소규모 팀<br><b>기억: 사무 처리·업무용 SW</b>',''),
 ('반분리형','Semi-detached','약 5만~30만 라인','중간 규모·복잡도 · 경험 수준이 섞인 팀<br><b>수험 예시: OS·DBMS·트랜잭션 처리</b>','mid'),
 ('내장형','Embedded','약 30만 라인 이상','하드웨어·소프트웨어·운영 조건의 강한 제약<br><b>기억: 실시간 제어·항공·유도 시스템</b>','high')]:
    body+=f'<div class="{cls}"><h3>{title}</h3><div class="en">{en}</div><span class="big">{size}</span>{desc}</div>'
body+='</div><p class="caption">라인 수는 국내 수험서에서 쓰는 대략적인 암기 기준이다. 실제 COCOMO 유형은 규모만으로 결정하지 않으며, 경험·복잡도·제약 조건도 고려한다. 같은 OS라도 개발 조건에 따라 유형이 달라질 수 있다.</p>'
body+='<h3 class="subhead">B. 추정 모형의 상세 수준 <small>얼마나 자세히 보정하는가?</small></h3><div class="steps"><div><span class="tag">Basic</span><h3>기본형</h3><p>코드 규모 + 개발 유형<br><b>빠른 개략 추정</b></p></div><span class="arrow">→</span><div><span class="tag">Intermediate</span><h3>중간형</h3><p>기본 추정 × 비용 동인<br><b>인력·제품·환경 등 보정</b></p></div><span class="arrow">→</span><div><span class="tag">Detailed</span><h3>발전형 / 상세형</h3><p>중간형 + 개발 단계별 특성<br><b>단계별로 더 세밀하게</b></p></div></div>'
body+=note('시험에서 “조직형·반분리형·내장형”은 <b>개발 유형</b>, “기본형·중간형·발전형”은 <b>상세 수준</b>이다. 아래 계수는 <b>Basic COCOMO 81</b>에만 적용한다. COCOMO II와 혼동하지 말 것.')
body+='''<div class="matrix-wrap"><table><caption class="caption">Basic COCOMO 81 계수</caption><thead><tr><th>개발 유형</th><th>노력 E = a × KLOCᵇ</th><th>기간 D = 2.5 × Eᵈ</th></tr></thead><tbody><tr><td>조직형</td><td>a = 2.4 / b = 1.05</td><td>d = 0.38</td></tr><tr><td>반분리형</td><td>a = 3.0 / b = 1.12</td><td>d = 0.35</td></tr><tr><td>내장형</td><td>a = 3.6 / b = 1.20</td><td>d = 0.32</td></tr></tbody></table></div><div class="calc"><h3>직접 비교하는 Basic COCOMO</h3><p class="caption">1 KLOC = 소스 코드 1,000줄 · E의 단위는 인월(Person-Month)</p><div class="calc-controls"><label>개발 유형<select id="cocomo-mode"><option value="0">조직형 · Organic</option><option value="1">반분리형 · Semi-detached</option><option value="2">내장형 · Embedded</option></select></label><label>규모 (KLOC)<input id="cocomo-size" type="number" min="0.1" max="10000" step="0.1" value="10" inputmode="decimal"></label></div><div class="results" aria-live="polite"><div><span>총 개발 노력</span><output id="effort">26.93</output><small>인월</small></div><div><span>개발 기간</span><output id="duration">8.74</output><small>개월</small></div><div><span>평균 투입 인원 ≈ E ÷ D</span><output id="people">3.08</output><small>명 · 단순 평균</small></div></div><p id="cocomo-formula" class="formula"></p></div>'''
chapters.append(section('cocomo','03','COCOMO 모형','개발 유형 3가지와 추정 상세 수준 3가지를 서로 다른 축으로 기억합니다.',body,source('IIT Kharagpur · Estimation of project metrics','https://vlabs.iitkgp.ac.in/sevl/Exp2/theory.html')+source('IPA · COCOMO 81 / II 비교','https://www.ipa.go.jp/archive/files/000024479.pdf')))

# 04. The seven design patterns selected for review.
patterns=[
 ('생성','팩토리 메서드','Factory Method',['부모 생성 규약','자식의 생성'],'생성 인터페이스를 정의하고, <b>하위 클래스가 생성할 클래스</b>를 결정.','팩토리 = 생성 결정을 자식에게'),
 ('구조','퍼사드 / 파사드','Facade',['사용자','단일 창구','서브시스템'],'복잡한 서브시스템에 <b>단순한 통합 인터페이스</b> 제공.','여러 기능의 앞문 하나'),
 ('구조','프록시','Proxy',['사용자','대리 객체','실제 객체'],'실제 객체 대신 접근하여 <b>접근·생성·원격 호출 등을 제어</b>.','대리인이 접근 관리'),
 ('구조','데코레이터','Decorator',['원래 객체','기능 감싸기'],'객체를 감싸서 <b>책임·기능을 동적으로 추가</b>.','장식은 중첩 가능'),
 ('구조','브리지 / 브릿지','Bridge',['추상 계층','구현 계층'],'추상과 구현을 분리하여 <b>각각 독립적으로 확장</b>.','추상 × 구현의 두 변화 축'),
 ('구조','플라이웨이트','Flyweight',['객체 A·B·C','공유 핵심 상태'],'공유 가능한 상태를 나눠 써서 <b>다수 객체의 메모리 절약</b>.','공통 상태 공유 / 외부 상태 분리'),
 ('행위','옵저버 / 관찰자','Observer',['대상 변경','관찰자 A·B'],'대상의 상태 변화 시 등록된 객체들에 <b>변경을 통지</b>.','일대다 알림')]
def pattern_visual(en,labels):
    if en in ['Observer','Flyweight']:
        mid={'Observer':'대상','Flyweight':'공유 상태'}[en]
        s=rect(123,6,114,38,mid,'node accent')
        for i,l in enumerate(['A','B','C']):
            x=60+120*i
            s+=circle(x,99,l,20)+line(180,44,x,77,arrow=True) if en=='Observer' else circle(x,99,l,20)+line(x,77,180,46,arrow=True)
        return svg(s,labels[0]+'와 '+labels[-1]+'의 관계',h=131)
    if en=='Decorator':return svg(rect(34,8,292,112,'','zone')+txt(180,32,'장식 B')+rect(65,41,230,63,'','node accent')+txt(180,61,'장식 A')+rect(102,71,156,29,'원래 객체'),'원래 객체를 장식 A와 B가 겹쳐 감싼 구조',h=131)
    return flow(labels)
body='<div class="ribbon"><div><h3>선택한 생성 패턴</h3><span class="big">1개</span>팩토리 메서드</div><div class="high"><h3>선택한 구조 패턴</h3><span class="big">5개</span>퍼사드 · 프록시 · 데코레이터<br>브리지 · 플라이웨이트</div><div class="mid"><h3>선택한 행위 패턴</h3><span class="big">1개</span>옵저버</div></div><p class="caption">선택한 7개만 정리했다. 팩토리는 Factory Method 기준이다. 아래 화살표는 설명 그림이며, 정식 UML 관계 기호를 뜻하지 않는다.</p>'
for category,cls,memo in [('생성','','팩토리'),('구조','structural','퍼 · 프 · 데 · 브 · 플'),('행위','behavioral','옵저버')]:
    count=sum(1 for x in patterns if x[0]==category)
    body+=f'<div class="category-title {cls}"><span class="num">{count:02}</span><div><h3>{category} 패턴</h3><div class="en">암기 순서 · {memo}</div></div></div><div class="patterns">'
    for cat,title,en,labels,desc,cue in patterns:
        if cat==category: body+=card(title,en,pattern_visual(en,labels),desc+f'<div class="pattern-cue">↳ {cue}</div>')
    body+='</div>'
body+=note('<b>퍼사드</b>는 창구 단순화, <b>프록시</b>는 접근 제어, <b>데코레이터</b>는 기능 추가, <b>브리지</b>는 추상·구현 분리, <b>플라이웨이트</b>는 공통 상태 공유. <b>팩토리 메서드</b>는 생성 결정, <b>옵저버</b>는 변경 통지.')
chapters.append(section('patterns','04','디자인 패턴 7종','팩토리 메서드 · 퍼사드 · 프록시 · 데코레이터 · 브리지 · 플라이웨이트 · 옵저버',body,source('GoF 원저 출판사 · 패턴 목차','https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780321770462')+source('Pearson · 패턴 의도와 예시','https://www.informit.com/store/design-patterns-in-java-9780321947925')))

# 05. Networks: extent and topology use independent classification axes.
body='<h3 class="subhead">A. 범위로 나누기 <small>얼마나 넓게 연결하는가?</small></h3>'
extent=[('PAN','Personal Area Network','개인 주변','휴대폰 ↔ 이어폰'),('LAN','Local Area Network','건물·사무실','교실 PC ↔ 스위치'),('MAN','Metropolitan Area Network','도시·도시권','도시 내 여러 거점'),('WAN','Wide Area Network','지역·국가·대륙','멀리 떨어진 LAN 연결')]
body+='<div class="ribbon" style="grid-template-columns:repeat(2,minmax(0,1fr))">'+''.join(f'<div><h3>{a} · {c}</h3><div class="en">{b}</div><p>{d}</p></div>' for a,b,c,d in extent)+'</div>'
s=''
for i,(a,b,c,d) in enumerate(extent):
    s+=rect(8+i*87,27,81,52,a,'node accent')
    if i<3:s+=line(89+i*87,53,94+i*87,53,arrow=True)
s+=txt(180,112,'개인 주변 → 건물 → 도시 → 광역','muted')
body+=svg(s,'PAN, LAN, MAN, WAN 순으로 범위가 넓어짐',h=130)+ '<p class="caption">범위는 상대적인 개념이다. 고정된 거리 수치만으로 구분하지 않는다. WLAN은 무선 LAN이며, WAN의 약어가 아니다.</p>'
body+='<h3 class="subhead">B. 연결 형태로 나누기 <small>노드와 링크를 어떻게 배치하는가?</small></h3><div class="grid three">'
def topo(kind):
    s=''; coords=[(180+98*math.cos(i*math.pi/3),83+57*math.sin(i*math.pi/3)) for i in range(6)]
    if kind=='Star':
        for x,y in coords:s+=line(180,83,x,y)
        s+=circle(180,83,'중앙',26,'node accent')
        for x,y in coords:s+=circle(round(x,1),round(y,1),r=10)
    elif kind=='Ring':
        for i,(x,y) in enumerate(coords):s+=line(x,y,*coords[(i+1)%6])
        for x,y in coords:s+=circle(round(x,1),round(y,1),r=12)
        s+=txt(180,88,'고리','muted')
    elif kind=='Bus':
        s+=line(27,90,333,90,'strong')+line(27,79,27,101)+line(333,79,333,101)
        for x in [62,139,216,293]:s+=line(x,90,x,49)+circle(x,34,r=14)
        s+=txt(180,129,'공유 백본 케이블','muted')
    elif kind=='Tree':
        s+=line(180,27,94,76)+line(180,27,266,76)
        for p,kids in [(94,[45,140]),(266,[220,315])]:
            for x in kids:s+=line(p,76,x,131)+circle(x,131,r=12)
            s+=circle(p,76,r=15)
        s+=circle(180,27,r=15,cls='node accent')
    elif kind=='Mesh':
        xy=[(74,41),(286,41),(286,131),(74,131)]
        for i,(x,y) in enumerate(xy):
            for x2,y2 in xy[i+1:]:s+=line(x,y,x2,y2)
        for x,y in xy:s+=circle(x,y,r=15)
        s+=txt(180,151,'완전 연결 예시: 4노드 · 6링크','muted')
    elif kind=='Hybrid':
        s+=line(103,82,255,82,'strong')
        for rootx in [103,255]:
            for x,y in [(rootx-48,30),(rootx+48,30),(rootx,136)]:s+=line(rootx,82,x,y)+circle(x,y,r=11)
            s+=circle(rootx,82,r=18,cls='node accent')
    return svg(s,kind+' 네트워크 토폴로지',h=165)
for title,en,desc in [('성형 / 스타형','Star','중앙 허브·스위치에 연결. 개별 링크 장애는 국소적이지만 <b>중앙 장비 장애의 영향이 큼</b>.'),('링형','Ring','이웃 노드끼리 <b>고리</b>로 연결. 단일 링은 단절에 취약하며 이중 링 등으로 보완.'),('버스형','Bus','하나의 <b>공유 회선</b>에 연결. 백본 단절의 영향이 크며 전통적 공유 매체에서 충돌 가능.'),('트리형 / 계층형','Tree','상위–하위의 <b>계층 구조</b>. 확장과 관리가 쉽지만 상위 연결 장애가 하위에 영향.'),('망형 / 메시형','Mesh','여러 경로로 연결하여 <b>우회·중복성</b> 확보. 완전 망형의 링크 수 = <b>n(n−1)/2</b>.'),('혼합형','Hybrid','성형·링형·버스형 등 <b>서로 다른 형태를 결합</b>. 요구에 맞게 구성하되 설계가 복잡해짐.')]:body+=card(title,en,topo(en),desc)
body+='</div>'+note('“LAN”과 “성형”은 동시에 성립할 수 있다. <b>LAN은 범위</b>, <b>성형은 연결 형태</b>다. 실제 네트워크는 물리적 배치와 논리적 데이터 흐름이 다를 수 있다.')
body+='<h3 class="subhead">C. 전송 대상에 따른 구분</h3><div class="grid">'
for title,en,targets,desc in [('유니캐스트','Unicast',[0],'하나의 송신자가 <b>특정 수신자 하나</b>에게 전달.'),('브로드캐스트','Broadcast',[0,1,2],'브로드캐스트 도메인 안의 <b>모든 대상</b>에게 전달.'),('멀티캐스트','Multicast',[0,2],'해당 그룹에 가입한 <b>여러 수신자</b>에게 전달.'),('애니캐스트','Anycast',[1],'같은 주소를 제공하는 노드 중 라우팅상 선택된 <b>하나</b>에게 전달.')]:
    s=rect(12,50,90,43,'송신자','node accent')
    for i in range(3):
        y=25+48*i;s+=line(102,71,246,y,'strong' if i in targets else 'off',i in targets)+circle(269,y,chr(65+i),18,'node accent' if i in targets else 'node')
    body+=card(title,en,svg(s,en+' 수신 대상 개념도',h=150),desc)
body+='</div><p class="caption">애니캐스트의 “가까움”은 물리적 거리보다 라우팅 정책·비용에 따른 최적 경로를 뜻한다. IPv6는 브로드캐스트 대신 멀티캐스트 등을 사용한다.</p>'
chapters.append(section('network','05','네트워크 종류','범위 · 연결 형태 · 전송 대상, 세 가지 분류 축을 따로 봅니다.',body,source('IBM · Networking','https://www.ibm.com/think/topics/networking')+source('IBM · Network topology','https://www.ibm.com/think/topics/network-topology')+source('RFC 4291 · Unicast / Anycast / Multicast','https://www.rfc-editor.org/rfc/rfc4291#section-2')))

# 06. White-box methods, basis-path CFG, truth-table coverage comparison.
body='<div class="preset-row"><button type="button" data-concept-jump="whitebox-techniques">화이트박스 기법 ↓</button><button type="button" data-concept-jump="blackbox-techniques">블랙박스 기법 ↓</button></div><div class="grid"><article class="concept"><h3>화이트박스 테스트</h3><div class="en">White-box · Structural testing</div>'+flow(['코드 내부','논리·흐름','테스트 설계'])+'<p>프로그램의 <b>내부 구조·제어 흐름·데이터 흐름</b>을 기준으로 테스트한다.</p></article><article class="concept"><h3>블랙박스와 비교</h3><div class="en">Black-box · Specification-based testing</div>'+flow(['입력','기능 상자','기대 출력'])+'<p>명세와 입출력 동작을 기준으로 테스트. <b>동등 분할·경계값·결정 테이블</b>은 블랙박스 기법이다.</p></article></div>'
body+='<h3 class="subhead" id="whitebox-techniques" tabindex="-1">A. 대표적인 화이트박스 기법</h3><div class="grid">'
for title,en,labels,desc in [
 ('기초 경로 검사','Basis path testing',['흐름 그래프','복잡도 V(G)','독립 경로'],'제어 흐름 그래프에서 <b>독립 경로 집합</b>을 선정하여 실행.'),
 ('조건 검사','Condition testing',['복합 조건','개별 조건','참·거짓'],'논리식의 각 조건과 결정 결과를 살펴 <b>조건·분기 오류</b>를 검출.'),
 ('루프 검사','Loop testing',['0회·1회','정상 반복','경계 반복'],'반복 횟수와 종료 조건 검사. <b>0·1·2회, 보통 횟수, 최대 부근</b>을 살핌.'),
 ('데이터 흐름 검사','Data-flow testing',['정의 d','경로','사용 u'],'변수의 <b>정의(def)–사용(use)</b> 연결을 기준으로 경로를 선정.')]:body+=card(title,en,flow(labels),desc)
body+='</div><p class="caption">루프가 0회를 허용하는지, 반복 상한이 있는지에 따라 입력을 설계한다. 최대 반복 수가 n이면 n−1·n·n+1 등의 경계를 살피되 유효·오류 입력을 구분한다.</p>'
body+='<h3 class="subhead">B. 기초 경로와 순환 복잡도</h3><div class="grid"><article class="concept"><h3>제어 흐름 그래프</h3>'
s=line(180,28,180,60)+line(180,85,83,125)+line(180,85,277,125)+line(83,151,180,196)+line(277,151,180,196)+circle(180,17,'1',16)+circle(180,76,'2',18,'node accent')+circle(83,138,'3',18)+circle(277,138,'4',18)+circle(180,208,'5',18)+txt(104,98,'T','muted')+txt(255,98,'F','muted')+txt(32,238,'1 시작 · 2 조건 · 3/4 처리 · 5 종료','muted',anchor='start')
body+=svg(s,'노드 5개, 간선 5개, 분기 노드 1개인 제어 흐름 그래프',h=255)+'</article><article class="concept"><h3>V(G) = E − N + 2</h3><p>E: 간선 수 / N: 노드 수<br>연결된 하나의 흐름 그래프 기준</p><div class="formula">5 − 5 + 2 = <b>2</b></div><p>이진 분기만 있는 경우<br><b>분기 노드 수 + 1 = 1 + 1 = 2</b></p><div class="pattern-cue">독립 경로 ① · 1 → 2 → 3 → 5</div><div class="pattern-cue">독립 경로 ② · 1 → 2 → 4 → 5</div><p>V(G)는 <b>선형 독립 경로 수</b>다. 전체 가능한 경로 수와 같다고 외우지 않는다.</p></article></div>'
body+='<h3 class="subhead">C. 커버리지 기준 비교 <small>기법과 측정 기준을 구분</small></h3><div class="matrix-wrap"><table><thead><tr><th>기준</th><th>100%가 되려면?</th><th>기억할 차이</th></tr></thead><tbody><tr><td><b>문장 / 구문</b><br>Statement</td><td>모든 실행 가능 문장을 한 번 이상 실행</td><td>문장 실행 ≠ 모든 분기 결과</td></tr><tr><td><b>결정 / 분기</b><br>Decision / Branch</td><td>각 결정의 T·F / 각 분기를 한 번 이상 실행</td><td>이진 if에서는 결정과 분기를 같은 기준으로 비교</td></tr><tr><td><b>조건</b><br>Condition</td><td>각 원자 조건이 T·F를 모두 가짐</td><td>결정 전체가 T·F가 되는지는 별개</td></tr><tr><td><b>조건·결정</b><br>Condition/Decision</td><td>조건 커버리지와 결정 커버리지를 모두 만족</td><td>각 조건 + 전체 결정</td></tr><tr><td><b>변경 조건·결정</b><br>MC/DC</td><td>각 조건이 독립적으로 결정 결과에 영향을 줌을 확인</td><td>다른 조건 고정 후 해당 조건 변경</td></tr><tr><td><b>다중 조건</b><br>Multiple condition</td><td>결정식의 가능한 조건 조합을 모두 수행</td><td>독립 조건 n개이면 최대 2ⁿ개 조합</td></tr><tr><td><b>경로</b><br>Path</td><td>정의한 범위의 실행 경로를 수행</td><td>모든 경로는 반복문 등으로 불가능할 수 있음</td></tr></tbody></table></div>'
body+=note('<b>분기 100% → 문장 100%</b>. 역은 성립하지 않는다. <b>조건 100%와 결정 100%는 서로 보장하지 않는다.</b> 커버리지 100%도 결함이 없다는 증거가 아니다.')
body+='''<h3 class="subhead">D. 직접 선택해서 이해하는 조건 vs 결정</h3><div class="grid"><article class="concept"><h3>예제: D = A AND B</h3><p class="caption">A·B를 모두 평가하는 논리 모델. 실제 언어의 단락 평가로 생략된 조건은 실행 기반 커버리지에서 별도로 취급한다.</p><div class="matrix-wrap"><table class="matrix-table"><thead><tr><th>선택</th><th>A</th><th>B</th><th>D</th></tr></thead><tbody><tr><td><label><input class="case-check" type="checkbox" value="0" checked aria-label="TT 사례 선택">TT</label></td><td>T</td><td>T</td><td>T</td></tr><tr><td><label><input class="case-check" type="checkbox" value="1" checked aria-label="TF 사례 선택">TF</label></td><td>T</td><td>F</td><td>F</td></tr><tr><td><label><input class="case-check" type="checkbox" value="2" aria-label="FT 사례 선택">FT</label></td><td>F</td><td>T</td><td>F</td></tr><tr><td><label><input class="case-check" type="checkbox" value="3" aria-label="FF 사례 선택">FF</label></td><td>F</td><td>F</td><td>F</td></tr></tbody></table></div><div class="preset-row"><button type="button" data-cases="1,2">조건만 100%</button><button type="button" data-cases="0,1">결정만 100%</button><button type="button" data-cases="0,1,2">MC/DC 예시</button><button type="button" data-cases="0,1,2,3">전체 조합</button></div></article><article class="concept"><h3>선택한 사례의 커버리지</h3><div class="coverage" aria-live="polite"><div class="meter">조건<strong id="condition-pct">75%</strong><div class="track"><i id="condition-bar"></i></div></div><div class="meter">결정<strong id="decision-pct">100%</strong><div class="track"><i id="decision-bar"></i></div></div><div class="meter">다중 조건<strong id="multiple-pct">50%</strong><div class="track"><i id="multiple-bar"></i></div></div></div><p id="coverage-note" class="coverage-note" aria-live="polite"></p><div class="pattern-cue">조건 = 관측한 A·B의 T/F 항목 수 ÷ 4</div><div class="pattern-cue">결정 = 관측한 D의 T/F 항목 수 ÷ 2</div><div class="pattern-cue">다중 조건 = 선택한 조합 수 ÷ 4</div><p><b>MC/DC 예시: TT·TF·FT</b><br>TT↔FT는 B=T 고정, A만 바꿔 D 변화.<br>TT↔TF는 A=T 고정, B만 바꿔 D 변화.</p></article></div>'''
body+='<h3 class="subhead">E. 문장 100%여도 분기 100%가 아닌 이유</h3><div class="grid"><div class="code-panel"><pre><code><span class="ln">1</span> x = 0;\n<span class="ln">2</span> if (A) {\n<span class="ln">3</span>     x = 1;\n<span class="ln">4</span> }\n<span class="ln">5</span> print(x);</code></pre></div><article class="concept"><h3>A = T 한 번만 실행하면?</h3><p><b>실행문 x=0, x=1, print(x)는 전부 실행</b>한다.<br>하지만 if의 <b>F 분기</b>는 아직 지나가지 않았다.</p><div class="pattern-cue">문장 100% / 결정 50%</div><p>A=F 테스트를 추가해야 결정의 T·F가 모두 충족된다. 중괄호·주석은 실행문 수에 포함하지 않는다.</p></article></div>'
from whitebox_cases import whitebox_cases_content
body+=whitebox_cases_content()
from blackbox_topic import blackbox_content
body+=blackbox_content()
chapters.append(section('whitebox','06','화이트박스 테스트 기법','화이트박스는 내부 구조로, 블랙박스는 명세·입출력으로 테스트를 설계합니다.',body,source('ISTQB CTFL 4.0.1 · §4.3','https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf')+source('NASA · Basis path & cyclomatic complexity','https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709643/SWE-220%2B-%2BCyclomatic%2BComplexity%2Bfor%2BSafety-Critical%2BSoftware')+source('NASA · MC/DC coverage','https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709626/SWE-219%2B-%2BCode%2BCoverage%2Bfor%2BSafety%2BCritical%2BSoftware')))

# 07. Seven testing principles, each paired with a mnemonic picture.
principles=[
 ('결함의 존재를 보여준다','Testing shows the presence of defects','결함은 발견할 수 있지만 <b>결함이 전혀 없음을 증명할 수는 없다</b>.','발견 0건 ≠ 결함 0개'),
 ('완벽한 테스팅은 불가능하다','Exhaustive testing is impossible','모든 입력·경로·환경의 조합을 검사하기는 어렵다. <b>위험·우선순위</b>로 집중한다.','전수 검사 대신 우선순위'),
 ('테스팅은 초기에 시작한다','Early testing saves time and money','요구사항·설계부터 검토하여 <b>뒤늦은 수정과 재작업</b>을 줄인다.','일찍 발견 → 재작업 감소'),
 ('결함은 집중된다','Defects cluster together','적은 수의 모듈에 많은 결함이 모이는 경향. <b>결함 이력·위험</b>을 참고한다.','파레토: 소수 영역에 다수 결함'),
 ('살충제 패러독스','Tests wear out','같은 테스트만 반복하면 새 결함 발견 효과가 줄어든다. <b>사례·데이터를 갱신</b>한다.','회귀 테스트는 유지 + 새 사례 보강'),
 ('테스팅은 정황에 의존한다','Testing is context dependent','안전 제어·쇼핑몰 등 <b>제품과 위험에 따라</b> 테스트 전략이 달라진다.','목적·환경에 맞는 테스트'),
 ('오류 부재의 궤변','Absence-of-defects fallacy','명세상 결함을 고쳐도 <b>사용자에게 쓸모없는 제품</b>이면 성공이라 할 수 없다.','결함 제거 + 사용자 요구 충족')]
def principle_visual(i):
    if i==0:s=rect(18,31,135,58,'발견: 0건')+txt(182,70,'≠','large')+rect(211,31,132,58,'잔여: 0개','node accent')
    elif i==1:
        s=''
        for y in range(4):
            for x in range(10):s+=rect(22+x*32,15+y*24,23,16,'','node accent' if (x+y)%4==0 else 'node',rx=3)
        s+=txt(180,130,'입력 × 경로 × 환경 → 조합 폭발','muted')
    elif i==2:s=rect(9,40,88,46,'요구사항','node accent')+rect(132,40,88,46,'구현')+rect(255,40,94,46,'운영')+line(97,63,130,63,arrow=True)+line(220,63,253,63,arrow=True)+txt(53,111,'초기 검토 ↑','muted')+txt(301,111,'재작업 부담 ↑','muted')
    elif i==3:
        s=''
        for j,n in enumerate([2,3,18,1,2]):
            x=24+j*66;s+=rect(x,19,49,82,'','node accent' if j==2 else 'node',rx=5)
            for k in range(n):s+=circle(x+10+(k%3)*14,32+(k//3)*11,r=3,cls='filled')
            s+=txt(x+24,124,chr(65+j),'muted')
    elif i==4:s=rect(9,37,100,48,'반복 사례')+path('M30 30 C20 3 100 3 92 31',arrow=True)+line(111,60,159,60,arrow=True)+rect(162,37,80,48,'갱신','node accent')+line(242,60,265,60,arrow=True)+rect(268,37,84,48,'새 결함')+txt(180,120,'기존 회귀 테스트의 가치는 유지','muted')
    elif i==5:s=rect(12,28,152,65,'의료·안전','node accent')+rect(196,28,152,65,'쇼핑 서비스')+txt(88,119,'안전성·신뢰성','muted')+txt(272,119,'구매 흐름·부하','muted')
    else:s=rect(15,29,139,59,'명세대로 동작')+txt(181,69,'+','large')+rect(209,29,139,59,'사용자 요구 충족','node accent')+txt(180,125,'검증 Verification + 확인 Validation','muted')
    return svg(s,principles[i][0]+': '+principles[i][3],h=145)
body='<div class="grid principles">'
for i,(title,en,desc,cue) in enumerate(principles):body+=f'<article class="concept {"wide" if i==6 else ""}"><div class="n">PRINCIPLE 0{i+1}</div><h3>{title}</h3><div class="en">{en}</div>{principle_visual(i)}<p>{desc}</p><div class="pattern-cue">{cue}</div></article>'
body+='</div>'+note('<b>한 줄로 연결:</b> 결함을 찾되 → 전부 검사할 수 없으니 → 일찍 시작하고 → 결함이 모인 곳에 집중하며 → 테스트를 갱신하고 → 상황에 맞게 검사하여 → 사용자에게 필요한 제품인지 확인한다.')+'<p class="caption">수험서의 “살충제 패러독스”는 ISTQB CTFL 4.0.1에서 “Tests wear out”으로 설명한다. 파레토의 80/20은 경향을 기억하는 표현이며 모든 프로젝트에 정확히 적용되는 법칙은 아니다.</p>'
chapters.append(section('principles','07','소프트웨어 테스트의 7가지 원리','테스트를 많이 하는 것과 올바르게 하는 것은 다릅니다.',body,source('ISTQB CTFL 4.0.1 · §1.3 Testing principles','https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf')))

questions=[
 ('빈 마름모 ◇가 전체 쪽에 있다면?','집합 / 집약(Aggregation). 부분이 독립적으로 존재할 수 있다.'),('실선 + 빈 삼각형, 자식에서 부모로 향한다면?','일반화(Generalization). 상속·is-a 관계.'),('점선 + 빈 삼각형, 구현체에서 명세로 향한다면?','실체화(Realization). 인터페이스 등의 명세 구현.'),('«extend» 화살표는 어디로 향하는가?','확장 유스케이스 → 기본 유스케이스.'),('14종 분류에서 구조·행위·상호작용 수는?','구조 7 + 행위 7. 상호작용 4는 행위 7 안에 포함. 프로파일 제외 시 총 13종.'),('메시지의 시간 순서와 생명선이 보이면?','시퀀스(Sequence) 다이어그램.'),('COCOMO 개발 유형 세 가지는?','조직형(Organic) / 반분리형(Semi-detached) / 내장형(Embedded).'),('COCOMO 기본형·중간형·발전형은 무엇의 분류?','추정 모형의 상세 수준. 개발 유형 3가지와 서로 다른 분류 축.'),('GoF 패턴은 분류별로 몇 개?','생성 5 / 구조 7 / 행위 11 = 총 23개.'),('규격 변환·단일 창구·접근 제어 패턴은?','Adapter / Facade / Proxy.'),('알고리즘을 교체하는 패턴 vs 절차 골격을 유지하는 패턴?','Strategy(전략) vs Template Method(템플릿 메서드).'),('LAN과 성형은 어떤 분류가 다른가?','LAN은 범위, 성형(Star)은 연결 형태(토폴로지).'),('완전 망형의 노드가 5개이면 링크는 몇 개?','5 × 4 ÷ 2 = 10개. n(n−1)/2.'),('V(G)=E−N+2가 나타내는 것은?','연결된 흐름 그래프의 순환 복잡도, 선형 독립 경로 수. 전체 경로 수가 아니다.'),('분기 100%이면 문장 100%인가? 역도 가능한가?','분기 100%이면 문장 100%. 문장 100%여도 분기 100%를 보장하지 않는다.'),('A AND B에서 TF·FT만 검사하면?','A와 B는 각각 T/F를 모두 가짐 → 조건 100%. D는 F만 관측 → 결정 50%.'),('같은 테스트만 반복하면 새 결함이 덜 발견되는 현상은?','살충제 패러독스 / Tests wear out. 테스트와 데이터를 갱신하되 회귀 테스트는 유지.'),('결함은 없지만 사용자에게 쓸모가 없다면?','오류 부재의 궤변(Absence-of-defects fallacy). 사용자 요구를 충족하는지도 확인해야 한다.')]
body='<div class="recall-actions"><button type="button" class="primary" id="open-answers">정답 모두 펼치기</button><button type="button" id="close-answers">정답 모두 접기</button><span id="recall-status" class="small" aria-live="polite">문항을 누르면 정답이 펼쳐집니다.</span></div><div class="recall-grid">'
for i,(q,a) in enumerate(questions):body+=f'<details class="recall"><summary><span class="q-no">RECALL {i+1:02}</span>{q}</summary><p>{a}</p></details>'
body+='</div>'
chapters.append(section('recall','08','그림을 떠올리며 셀프 체크','읽기를 마쳤다면 답을 가리고 핵심을 떠올려 보세요.',body))

CSS+='''
.sidebar h2{font-size:22px}
@media(max-width:1350px) and (min-width:851px){.patterns,.grid.three{grid-template-columns:repeat(2,minmax(0,1fr))}.sidebar h2{font-size:20px}}
@media(max-width:850px){.sidebar h2{font-size:19px}}
@media(max-width:560px){.diagram text{font-size:16px}.diagram text.muted{font-size:14px}.diagram text.large{font-size:24px}}
'''

JS='''
(()=>{'use strict';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const modes=[[2.4,1.05,.38],[3,1.12,.35],[3.6,1.20,.32]];
function calc(){const size=Number($('#cocomo-size').value),m=modes[Number($('#cocomo-mode').value)],f=$('#cocomo-formula');
if(!Number.isFinite(size)||size<=0||size>10000){['effort','duration','people'].forEach(id=>$('#'+id).textContent='—');f.textContent='0보다 크고 10,000 이하인 KLOC 값을 입력하세요.';f.classList.add('error');return;}
f.classList.remove('error');const e=m[0]*Math.pow(size,m[1]),d=2.5*Math.pow(e,m[2]);$('#effort').textContent=e.toFixed(2);$('#duration').textContent=d.toFixed(2);$('#people').textContent=(e/d).toFixed(2);f.textContent=`E = ${m[0].toFixed(1)} × ${size}^${m[1].toFixed(2)}  /  D = 2.5 × E^${m[2].toFixed(2)}`;}
$('#cocomo-mode').addEventListener('change',calc);$('#cocomo-size').addEventListener('input',calc);calc();
const cases=[[true,true,true],[true,false,false],[false,true,false],[false,false,false]];
function cover(){const selected=$$('.case-check').filter(x=>x.checked).map(x=>Number(x.value)),av=new Set(),bv=new Set(),dv=new Set();selected.forEach(i=>{av.add(cases[i][0]);bv.add(cases[i][1]);dv.add(cases[i][2]);});const a=(av.size+bv.size)*25,b=dv.size*50,c=selected.length*25;
[['condition',a],['decision',b],['multiple',c]].forEach(([id,v])=>{$('#'+id+'-pct').textContent=v+'%';$('#'+id+'-bar').style.width=v+'%';});
$$('.case-check').forEach(x=>x.closest('tr').classList.toggle('chosen',x.checked));
$('#coverage-note').textContent=!selected.length?'테스트 사례를 선택해 보세요.':a===100&&b<100?'각 조건의 T/F는 모두 검사했지만, 결정 전체는 F만 관측했습니다.':b===100&&a<100?'결정은 T/F 모두 검사했지만, A의 F는 검사하지 않았습니다.':a===100&&b===100?'조건·결정 모두 100%입니다. 다중 조건은 네 조합 전체를 선택해야 100%입니다.':'아직 관측하지 못한 조건값·결정 결과가 남아 있습니다.';
}
$$('.case-check').forEach(x=>x.addEventListener('change',cover));$$('[data-cases]').forEach(b=>b.addEventListener('click',()=>{const a=b.dataset.cases.split(',');$$('.case-check').forEach(x=>x.checked=a.includes(x.value));cover();}));cover();
const answers=$$('details.recall');function status(){const n=answers.filter(x=>x.open).length;$('#recall-status').textContent=`정답 ${n} / ${answers.length}개 펼침`;}
$('#open-answers').addEventListener('click',()=>{answers.forEach(x=>x.open=true);status();});$('#close-answers').addEventListener('click',()=>{answers.forEach(x=>x.open=false);status();});answers.forEach(x=>x.addEventListener('toggle',status));
let previous=[];window.addEventListener('beforeprint',()=>{previous=answers.map(x=>x.open);answers.forEach(x=>x.open=true);});window.addEventListener('afterprint',()=>{answers.forEach((x,i)=>x.open=previous[i]||false);status();});$('#print').addEventListener('click',()=>window.print());
const links=$$('.sidebar nav a');if('IntersectionObserver' in window){const io=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){links.forEach(l=>{const on=l.hash==='#'+e.target.id;l.classList.toggle('active',on);if(on)l.setAttribute('aria-current','location');else l.removeAttribute('aria-current');});}});},{rootMargin:'-8% 0px -73% 0px',threshold:0});$$('.chapter').forEach(s=>io.observe(s));}
})();
'''
nav=[('uml-rel','UML 관계'),('uml-types','UML 다이어그램'),('cocomo','COCOMO 모형'),('patterns','디자인 패턴'),('network','네트워크'),('whitebox','화이트박스 테스트'),('principles','테스트의 7원리'),('recall','셀프 체크')]
navigation=''.join(f'<a href="#{id}"><span>{i+1:02}</span>{label}</a>' for i,(id,label) in enumerate(nav))
overview=''.join(f'<a href="#{id}"><b>{num}</b><span>{label}</span></a>' for id,label,num in [('uml-rel','UML 기본 관계','6'),('uml-types','UML 다이어그램','14'),('patterns','GoF 디자인 패턴','23'),('principles','테스트의 원리','7')])
html=f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="정보처리기사 실기 핵심 이론 7개 주제를 도형과 그림으로 정리한 오프라인 학습 노트"><title>정보처리기사 · 핵심이론 그림 정리</title><style>{CSS}</style></head><body id="top">{defs}<div class="layout"><aside class="sidebar"><div class="brand">VISUAL STUDY NOTES</div><h2>정보처리기사<br>핵심이론 그림 정리</h2><nav aria-label="학습 목차">{navigation}</nav><div class="nav-footer"><b>그림 → 구분 → 회상</b><br>관계는 화살표로,<br>종류는 가지로,<br>원리는 장면으로 기억하세요.<br><br>오프라인 단일 파일<br>정리 기준: 2026.10.21</div></aside><main><div class="topline"><p class="eyebrow">INFORMATION PROCESSING ENGINEER / PRACTICAL</p><div class="utility"><button type="button" id="print">인쇄 / PDF 저장</button></div></div><header class="hero"><h1>복잡한 이론을<br><em>한 장면씩</em> 기억하기.</h1><p>UML부터 테스트 원리까지, 7개 주제를 도형·흐름·비교 그림으로 정리했습니다. 이름을 외우기 전에 모양과 차이를 먼저 보세요.</p><div class="hero-bottom"><span class="pill">UML 관계·다이어그램</span><span class="pill">COCOMO·GoF</span><span class="pill">네트워크</span><span class="pill">화이트박스·테스트 원리</span></div></header><div class="overview">{overview}</div>{''.join(chapters)}<footer class="closing"><b>사용 안내</b><p>외부 라이브러리·폰트 없이 동작하는 단일 HTML입니다. 왼쪽 목차로 이동하고, 계산기·진리표·셀프 체크로 복습하세요. 인쇄하면 정답을 펼친 학습용 레이아웃으로 출력됩니다.</p><p>공식 표준·출판사·기술 문서를 참고하여 학습용으로 재구성했습니다. 그림은 개념 이해를 위한 축약 표현을 포함합니다. COCOMO 규모 및 UML 13/14종은 교재별 표현 차이를 함께 적었습니다.</p><a class="bottom-link" href="#top">↑ 맨 위로</a></footer></main></div><script>{JS}</script></body></html>'''
from study_app import build_app, BANK, TOPICS
html = build_app(CSS, defs, chapters[:7], JS)
OUT.write_text(html, encoding='utf-8', newline='\n')
# GitHub Pages entry point, kept identical to the offline study document.
(ROOT / 'index.html').write_text(html, encoding='utf-8', newline='\n')
code_source = ROOT / '정처기_실기_코드문제풀이.html'
(ROOT / 'code-practice.html').write_text(code_source.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
print(f'Created: {OUT}\nSize: {OUT.stat().st_size:,} bytes\nSVG diagrams: {html.count("<svg")}\nConcepts: {len(TOPICS)}\nPractice questions: {sum(len(qs) for qs in BANK.values())}')
