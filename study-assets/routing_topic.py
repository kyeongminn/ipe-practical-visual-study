"""Routing classifications, path examples, and the user's existing question 160."""
from pathlib import Path
from html import escape
import json
import re
from security_topic import box, text, edge, svg
from drm_topics import card, chapter, note

def router(x,y,label):
    return f'<circle cx="{x}" cy="{y}" r="17" class="node"/>'+text(x,y+5,label)

def path_example(method):
    xy={'A':(28,100),'B':(180,27),'D':(332,100),'C':(120,170),'E':(240,170)}
    links=[('A','B',9),('B','D',9),('A','C',1),('C','E',1),('E','D',1)]
    out=''
    for a,b,cost in links:
        x,y=xy[a];xx,yy=xy[b]
        active=(method=='RIP' and cost==9) or (method=='OSPF' and cost==1)
        out+=f'<path d="M{x} {y} L{xx} {yy}" class="edge {"strong" if active else ""}"/>'
    for x,y,v in [(101,51,'9'),(259,51,'9'),(60,150,'1'),(180,193,'1'),(300,150,'1')]:out+=text(x,y,v,'muted')
    for label,(x,y) in xy.items():out+=router(x,y,label)
    out+=text(180,230,'A → B → D : 2홉' if method=='RIP' else 'A → C → E → D : 비용 3','muted')
    return svg(out,method+'에서 선택하는 경로 예시. 위쪽은 2홉 비용18, 아래쪽은 3홉 비용3.',249)

def build_routing_chapter():
    scope='<rect x="5" y="10" width="145" height="160" rx="12" class="zone"/><rect x="210" y="10" width="145" height="160" rx="12" class="zone"/>'
    scope+=text(77,37,'AS A')+text(282,37,'AS B')
    for x in [42,112,248,318]:scope+=router(x,83,'R')
    scope+=edge(60,83,94,83)+edge(266,83,300,83)+edge(131,83,229,83)
    scope+=text(77,133,'IGP · AS 내부','muted')+text(282,133,'IGP · AS 내부','muted')+text(180,65,'eBGP','muted')+text(180,195,'AS = 하나의 관리 정책으로 운영하는 자율 시스템','muted')
    body=note('먼저 구분','<b>라우팅은 목적지까지의 경로를 정하는 일.</b> 정적 라우팅은 관리자가 경로를 설정하고, 동적 라우팅은 프로토콜로 정보를 교환하여 경로를 갱신한다.')
    body+='<h3 class="subhead">1. 사용 범위 · AS 안인가, AS 사이인가?</h3><div style="max-width:620px;margin:0 auto">'+svg(scope,'IGP는 AS 내부, eBGP는 서로 다른 AS의 경계를 연결',214)+'</div>'
    body+='<div class="branch-tree"><div class="family"><h3>IGP · 내부 라우팅</h3><ul class="tree-list"><li><b>거리 벡터</b><span>RIP · IGRP</span></li><li><b>개선된 거리 벡터</b><span>EIGRP · 수험서에서 하이브리드로도 분류</span></li><li><b>링크 상태</b><span>OSPF · IS-IS</span></li></ul></div><div class="family"><h3>EGP · 외부 라우팅 분류</h3><ul class="tree-list"><li><b>대표: BGP</b><span>경로 벡터 · AS 경로와 정책을 고려</span></li><li><b>eBGP</b><span>서로 다른 AS 사이에서 교환</span></li><li><b>iBGP</b><span>같은 AS 안에서 BGP 경로를 교환</span></li></ul></div></div>'
    body+=note('용어 주의','외부 라우팅을 뜻하는 <b>EGP라는 분류</b>와 예전에 쓰던 <b>EGP라는 개별 프로토콜</b>은 구분한다. BGP는 대표적인 외부 라우팅 프로토콜이지만 iBGP로 AS 내부에서도 경로 정보를 교환한다.')
    rows=[
      ('RIP','Routing Information Protocol','거리 벡터 · IGP','Bellman–Ford · 홉 수','목적지까지 거치는 홉 수를 기준으로 선택. 최대 유효 값은 <b>15</b>, <b>16은 도달 불가</b>.','RIP = 거리 벡터 + Bellman–Ford + 15홉'),
      ('OSPF','Open Shortest Path First','링크 상태 · IGP','Dijkstra · 비용(Cost)','링크 상태를 공유하고 최단 경로를 계산. 영역(Area) 단위로 나눠 구성할 수 있다.','OSPF = 링크 상태 + Dijkstra + 비용'),
      ('BGP','Border Gateway Protocol','경로 벡터 · 외부 라우팅','AS_PATH · 정책','AS 경로 등 속성과 정책으로 경로를 선택. TCP 179번 포트로 피어 간 정보를 교환한다.','BGP = AS 사이 + 경로 벡터 + 정책'),
      ('EIGRP','Enhanced Interior Gateway Routing Protocol','개선된 거리 벡터 · IGP','DUAL','거리 벡터 기반으로 빠른 수렴과 루프 없는 경로 계산을 제공. 수험서에서는 하이브리드라는 표현도 사용한다.','EIGRP = DUAL · 단순히 링크 상태로 외우지 않기'),
      ('IS-IS','Intermediate System to Intermediate System','링크 상태 · IGP','Dijkstra','OSPF처럼 링크 상태와 최단 경로 계산을 이용하는 내부 라우팅 프로토콜.','OSPF와 IS-IS = 링크 상태'),
      ('IGRP','Interior Gateway Routing Protocol','거리 벡터 · IGP','복합 메트릭','대역폭·지연 등을 고려하는 Cisco의 과거 프로토콜. EIGRP와 이름을 구분한다.','IGRP = 과거 방식 / EIGRP = 개선된 방식')]
    body+='<h3 class="subhead">2. 프로토콜별 핵심 특징</h3><div class="grid three">'
    for name,en,kind,algorithm,description,cue in rows:
        pic=svg(box(9,30,143,48,name)+edge(154,54,207,54)+box(210,30,142,48,'경로 결정','node accent')+text(180,119,algorithm,'muted'),name+'의 경로 결정 특징: '+algorithm,140)
        body+=card(name,en,pic,f'<b>{kind}</b><br>{description}',cue)
    body+='</div><div class="matrix-wrap" style="margin-top:20px"><table><thead><tr><th>프로토콜</th><th>분류</th><th>알고리즘·기준</th><th>암기 키워드</th></tr></thead><tbody><tr><td>RIP</td><td>거리 벡터 · IGP</td><td>Bellman–Ford / 홉 수</td><td>15 유효 · 16 도달 불가</td></tr><tr><td>OSPF</td><td>링크 상태 · IGP</td><td>Dijkstra / Cost</td><td>영역 · 최단 경로</td></tr><tr><td>BGP</td><td>경로 벡터</td><td>AS_PATH 등 속성 / 정책</td><td>AS 사이 · TCP 179</td></tr><tr><td>EIGRP</td><td>개선된 거리 벡터 · IGP</td><td>DUAL / 복합 메트릭</td><td>하이브리드라는 수험 표현</td></tr><tr><td>IS-IS</td><td>링크 상태 · IGP</td><td>Dijkstra / Cost</td><td>대규모 내부 라우팅</td></tr><tr><td>IGRP</td><td>거리 벡터 · IGP</td><td>복합 메트릭</td><td>과거 Cisco 방식</td></tr></tbody></table></div>'
    body+='<h3 class="subhead">3. 홉 수가 적은 길과 비용이 낮은 길</h3><div class="grid"><article class="concept"><h3>RIP · 적은 홉 수</h3>'+path_example('RIP')+'<p>위쪽 경로는 <b>2홉</b>, 아래쪽 경로는 3홉. RIP는 홉 수가 적은 위쪽을 선택한다.</p></article><article class="concept"><h3>OSPF · 낮은 비용 합</h3>'+path_example('OSPF')+'<p>숫자를 OSPF 링크 비용으로 놓으면 위쪽은 9+9=<b>18</b>, 아래쪽은 1+1+1=<b>3</b>. 아래쪽을 선택한다.</p></article></div><p class="caption">이해를 위한 단순한 비용 예시다. 파란 선은 선택 경로이며 RIP는 그림의 비용값 대신 홉 수를 센다.</p>'
    body+=note('BGP는 다르게','BGP는 단순히 홉 수가 가장 적거나 IGP 비용이 가장 낮은 길만 고르는 방식이 아니다. AS_PATH 등 여러 경로 속성과 운영 정책을 함께 고려한다.')
    body+='<h3 class="subhead">4. 시험 직전 기억할 세 연결</h3><div class="ribbon"><div><h3>Bellman–Ford · 15홉</h3><span class="big">RIP</span>거리 벡터 · 내부</div><div><h3>Dijkstra · 링크 상태</h3><span class="big">OSPF</span>비용 기반 · 내부</div><div><h3>AS 간 경로 교환</h3><span class="big">BGP</span>경로 벡터 · 외부</div></div>'
    sources=[('RFC 2453 · RIP','https://www.rfc-editor.org/rfc/rfc2453.html'),('RFC 2328 · OSPF','https://www.rfc-editor.org/rfc/rfc2328.html'),('RFC 4271 · BGP','https://www.rfc-editor.org/rfc/rfc4271.html'),('RFC 7868 · EIGRP / DUAL','https://www.rfc-editor.org/info/rfc7868/'),('Cisco · IS-IS','https://netascode.cisco.com/docs/data_models/iosxe/device/isis/')]
    return chapter('routing-protocols','11','라우팅 프로토콜 종류','AS 내부·외부와 거리 벡터·링크 상태·경로 벡터를 나눠 기억하기',body,sources)

def routing_questions(question,field):
    root=Path(__file__).resolve().parent.parent
    source_file=root/'정처기_실기_코드문제풀이.html'
    raw=source_file.read_text(encoding='utf-8')
    data=json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>',raw,re.S).group(1))
    source=next(q for q in data if q.get('id')==160)
    assert source['title']=='라우팅 프로토콜' and source['src']=='extra'
    imported=question('routing-local-160','160번 · '+source['title'],source['ask']+'\n\n'+source['body'],
      [field(f'{i+1}번',*blank['a']) for i,blank in enumerate(source['blanks'])],source['expl'],
      url=source_file.name,source='정처기_실기_코드문제풀이.html · 160번')
    imported['origin']='기존 문제은행 160번 · 직접 작성 예시'
    return {'routing-protocols':[
      imported,
      question('routing-scope','AS 내부와 외부','① 한 AS 내부에서 쓰는 라우팅 프로토콜의 분류, ② 서로 다른 AS 사이에 쓰는 라우팅 프로토콜의 분류를 영문 약어로 쓰세요.',[
        field('① AS 내부','IGP','Interior Gateway Protocol'),field('② AS 사이','EGP','Exterior Gateway Protocol')],
        'IGP / EGP입니다. RIP·OSPF 등은 IGP, BGP는 대표적인 외부 라우팅 프로토콜입니다. iBGP는 같은 AS 안에서 BGP 정보를 교환하는 방식입니다.'),
      question('routing-rip-hop','RIP의 15와 16','RIP의 홉 수 메트릭에서 ① 유효한 최대 값, ② 도달 불가능을 뜻하는 값을 쓰세요.',[
        field('① 유효 최대 값','15','15홉','15 Hop'),field('② 도달 불가 값','16','16홉','16 Hop')],
        '15 / 16입니다. 최대 유효 메트릭은 15이고 16은 무한대, 즉 도달 불가로 취급합니다.'),
      question('routing-algorithms','알고리즘 연결','OSPF와 EIGRP가 사용하는 대표적인 경로 계산 알고리즘을 쓰세요.',[
        field('① OSPF','다익스트라','Dijkstra'),field('② EIGRP','DUAL','Diffusing Update Algorithm')],
        'OSPF는 Dijkstra, EIGRP는 DUAL입니다. RIP는 Bellman–Ford 기반의 거리 벡터 방식입니다.'),
      question('routing-bgp','BGP의 정보 교환 위치','BGP에서 ① 서로 다른 AS의 피어 사이, ② 같은 AS의 피어 사이의 경로 정보 교환을 뜻하는 약어를 쓰세요.',[
        field('① 다른 AS','eBGP','External BGP'),field('② 같은 AS','iBGP','Internal BGP','Interior BGP')],
        'eBGP / iBGP입니다. BGP를 외부 라우팅 프로토콜로 분류한다고 해서 같은 AS 안에서는 사용할 수 없다는 뜻은 아닙니다.'),
      question('routing-cost','서로 다른 경로 선택 기준','경로 ①은 2홉·비용 합 18, 경로 ②는 3홉·비용 합 3입니다. 다른 조건이 같고 숫자를 OSPF 비용으로 사용할 때 각 프로토콜이 선택할 경로 번호를 쓰세요.',[
        field('RIP가 선택할 경로 번호','1','①','1번'),field('OSPF가 선택할 경로 번호','2','②','2번')],
        'RIP는 ①(2홉), OSPF는 ②(비용 합 3)입니다. “최단”의 기준이 홉 수인지 비용인지 먼저 확인하세요.')]
    }
