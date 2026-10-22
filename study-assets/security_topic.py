"""CIA triad: definitions, visual comparisons, examples, and source links."""
from html import escape

def text(x,y,label,cls='',anchor='middle'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(label)}</text>'

def box(x,y,w,h,label,cls='node'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" class="{cls}"/>'+text(x+w/2,y+h/2+5,label)

def edge(x,y,xx,yy):
    return f'<path d="M{x} {y} L{xx} {yy}" class="edge" marker-end="url(#arrow)"/>'

def svg(content,label,height=145):
    return f'<svg class="diagram" viewBox="0 0 360 {height}" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>{content}</svg>'

def build_security_chapter():
    triangle='<path d="M180 62 L82 180 H278 Z" class="edge"/>'
    triangle+=box(105,8,150,49,'C · 기밀성','node accent')
    triangle+=box(8,185,143,49,'I · 무결성')+box(209,185,143,49,'A · 가용성')
    triangle+=text(180,130,'정보 · 시스템')+text(180,152,'보호의 세 가지 목표','muted')
    triangle+=text(180,257,'몰래 보기 방지 · 무단 변경 방지 · 사용 보장','muted')
    overview=svg(triangle,'CIA 삼각형: 기밀성, 무결성, 가용성은 정보와 시스템을 보호하는 세 가지 목표',275)
    confidential=box(8,35,105,44,'개인정보')+edge(114,57,128,57)+box(131,35,105,44,'접근 통제','node accent')+edge(237,57,250,57)+box(253,35,101,44,'인가 사용자')+text(180,119,'권한 없는 열람·유출을 막는다','muted')
    integrity=box(10,25,145,48,'원본 금액 100')+box(205,25,145,48,'전달 금액 100')+edge(156,49,203,49)+text(180,115,'허가 없이 100 → 900 변경 금지','muted')
    available=box(8,25,145,48,'주 서버 장애')+edge(154,49,202,49)+box(205,25,145,48,'대체 서버 운영','node accent')+text(180,115,'필요한 때 서비스를 계속 이용','muted')
    card_data=[
      ('기밀성','Confidentiality',confidential,'누가 볼 수 있는가?','인가된 대상만 정보를 열람하도록 하고, 허가되지 않은 접근·공개를 막는다.','고객의 개인정보가 외부로 새어나감','암호화 · 인증과 접근 통제 · 최소 권한'),
      ('무결성','Integrity',integrity,'내용을 믿을 수 있는가?','정보의 부적절한 변경·파괴를 막고 정확성과 완전성을 지킨다. 정당한 권한에 따른 수정까지 금지하는 뜻은 아니다.','송금액이나 성적이 허가 없이 변경됨','MAC · 전자서명 · 변경 권한 통제 · 신뢰된 기준 해시 비교'),
      ('가용성','Availability',available,'필요할 때 쓸 수 있는가?','인가된 사용자가 필요한 때 정보와 시스템에 적시에 안정적으로 접근하고 사용할 수 있게 한다.','DDoS·장애·정전으로 정상 이용이 막힘','이중화 · 장애 전환 · 백업·복구 · DDoS 대응')]
    cards=''
    for ko,en,drawing,cue,definition,incident,control in card_data:
        cards+=f'<article class="concept"><div class="card-top"><h3>{ko}</h3><span class="tag">{en[0]}</span></div><div class="en">{en}</div>{svg(drawing,ko+": "+cue)}<div class="pattern-cue"><b>{cue}</b></div><p>{definition}</p><p><b>침해 예시</b><br>{incident}</p><p><b>보호 수단</b><br>{control}</p></article>'
    scenarios=[
      ('비밀번호·개인정보를 몰래 읽고 유출','기밀성 C','볼 권한이 없는 대상에게 정보가 공개됨'),
      ('계좌번호·송금액을 허가 없이 바꿈','무결성 I','정보 내용이 부적절하게 변경됨'),
      ('과도한 요청으로 서버를 마비시킴','가용성 A','정상 사용자가 서비스에 접근하지 못함'),
      ('랜섬웨어가 파일을 변조·암호화하여 사용을 막음','무결성 I + 가용성 A','내용 훼손과 사용 불가가 함께 발생할 수 있음'),
      ('랜섬웨어 공격자가 원본을 외부로 유출하기도 함','기밀성 C도 침해 가능','하나의 사고가 여러 보안 목표를 동시에 해칠 수 있음')]
    table='<div class="matrix-wrap"><table><thead><tr><th>상황</th><th>주요 침해 요소</th><th>구분 이유</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>' for a,b,c in scenarios)+'</tbody></table></div>'
    return f'''<section id="security-cia" class="chapter"><header class="chapter-head"><span class="chapter-no">08</span><div><p class="eyebrow">CONCEPT MAP / 08</p><h2>보안의 3요소 · CIA</h2><p>몰래 보지 못하게 · 함부로 바꾸지 못하게 · 필요할 때 쓸 수 있게</p></div></header><div style="max-width:540px;margin:0 auto 24px">{overview}</div><div class="grid three">{cards}</div><div class="note"><b>한 줄 암기</b><span><b>C</b> = 비밀을 지킨다 / <b>I</b> = 내용을 지킨다 / <b>A</b> = 이용을 지킨다.</span></div><h3 class="subhead">사건을 보고 어떤 요소인지 구분하기</h3>{table}<h3 class="subhead">헷갈리기 쉬운 두 가지</h3><div class="grid"><article class="concept"><h3>기밀성 ≠ 무결성</h3><p>읽지 못하게 막는 것과, 내용이 바뀌지 않았는지 확인하는 것은 별개다. <b>암호화만으로 무결성이 자동 보장되지는 않는다.</b></p><div class="pattern-cue">암호화: 내용 보호 / MAC·전자서명: 변경 검증 등에 활용</div></article><article class="concept"><h3>해시 비교에도 기준이 필요</h3><p>파일과 비교용 해시를 공격자가 함께 바꾸면 단순 비교로는 속을 수 있다. <b>해시 기준값을 신뢰할 수 있게 보호</b>하거나 MAC·전자서명 등 인증된 검증을 사용한다.</p><div class="pattern-cue">무결성은 “변경 금지”가 아니라 “부적절한 변경 방지”</div></article></div><div class="source-row"><a class="source" href="https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.199.pdf" target="_blank" rel="noopener noreferrer">↗ NIST FIPS 199 · CIA 정의</a><a class="source" href="https://www.nccoe.nist.gov/data-security" target="_blank" rel="noopener noreferrer">↗ NIST NCCoE · Data security</a><a class="source" href="https://informationsecurity.wustl.edu/guidance/confidentiality-integrity-and-availability-the-cia-triad/" target="_blank" rel="noopener noreferrer">↗ Washington University · CIA triad</a></div></section>'''
