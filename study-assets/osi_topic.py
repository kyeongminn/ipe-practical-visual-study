"""OSI seven-layer study page: mnemonic, roles, PDUs and encapsulation."""
from html import escape
from security_topic import text, box, edge, svg

LAYERS=[
 (1,'물','물리','Physical','비트를 신호로 전송','Bit · 비트','리피터 · 허브 · 전송 매체','전기·광·무선 신호, 물리 인터페이스','비트 스트림을 매체에 실어 보낸다. 접속·절단과 전기적·기계적 특성 등을 규정한다.'),
 (2,'대','데이터링크','Data Link','인접 노드 간 프레임 전달','Frame · 프레임','브리지 · L2 스위치 / MAC 주소','Ethernet MAC · PPP · HDLC','한 링크의 인접 노드 사이에서 프레임을 전달한다. 매체 접근과 오류 검출, 프로토콜에 따른 흐름·오류 제어 등을 맡는다.'),
 (3,'네','네트워크','Network','IP 주소와 경로 선택','Packet · 패킷','라우터 · L3 스위치 / IP 주소','IP · ICMP','서로 다른 네트워크를 거치는 전달 경로를 선택하고 패킷을 중계한다. 논리 주소를 사용한다.'),
 (4,'전','전송','Transport','종단 간 전달 · 포트 구분','TCP: Segment / UDP: Datagram','포트 번호 / L4 스위치의 분류 기준','TCP · UDP','송신·수신 종단의 프로세스 사이 전달을 담당한다. TCP는 순서·흐름·오류 복구를 지원하고 UDP는 같은 신뢰성 보장을 제공하지 않는다.'),
 (5,'세','세션','Session','대화 연결 관리 · 동기화','Data · 데이터','특정 물리 장비와 일대일 대응 없음','기능 예: 대화 제어 · 체크포인트','대화의 설정·유지·종료, 데이터 교환의 동기화와 복구 지점 관리 등의 역할을 설명하는 계층이다.'),
 (6,'표','표현','Presentation','형식 변환 · 압축 · 암호화','Data · 데이터','특정 물리 장비와 일대일 대응 없음','형식 예: 문자 인코딩 · JPEG · MPEG','서로 이해할 수 있는 데이터 표현으로 변환한다. 인코딩 변환, 압축과 암호화·복호화 같은 기능을 다룬다.'),
 (7,'응','응용','Application','응용 프로그램의 통신 서비스','Data · 데이터','응용 계층 프로토콜을 쓰는 서비스','HTTP · FTP · SMTP · DNS','사용자 응용 프로그램에 파일 전송·메일·이름 해석 등의 네트워크 서비스를 제공한다. 브라우저 프로그램 전체를 가리키는 말은 아니다.')]

def mnemonic():
    return '<div class="osi-memory" aria-label="1계층부터 물대네전세표응">'+''.join(f'<div><b>{mark}</b><span>{number} · {name}</span></div>' for number,mark,name,*_ in LAYERS)+'</div>'

def osi_preview():
    rows=''.join(f'<div class="mini-osi-row" data-osi-layer="{number}"><b>{number}</b><strong>{name}</strong><span>{cue}</span></div>' for number,_,name,_,cue,*_ in LAYERS)
    return '<div class="mini-osi">'+rows+'</div><p class="mini-hint"><b>물대네전세표응 = 1 → 7계층</b><br>단위: 비트 → 프레임 → 패킷 → 세그먼트(TCP)<br>주소: MAC(2) · IP(3) · 포트(4)</p>'

def layer_stack():
    drawing=''
    short=['비트 · 신호','프레임 · MAC','패킷 · IP · 경로','종단 간 전달 · 포트','대화 관리 · 동기화','형식 변환 · 압축·암호화','응용 프로그램의 통신 서비스']
    for index,(number,_,name,*_) in enumerate(reversed(LAYERS)):
        y=8+index*47
        drawing+=box(8,y,344,40,'','node')+text(24,y+25,f'{number} · {name}','','start')+text(160,y+25,short[number-1],'muted','start')
    drawing+=text(180,355,'송신: 7 → 1 ↓  /  수신: 1 → 7 ↑','muted')
    return svg(drawing,'위에서 응용·표현·세션·전송·네트워크·데이터링크·물리, 암기 순서는 아래 1계층부터 물대네전세표응',373)

def encapsulation():
    drawing=box(80,8,200,36,'데이터')+edge(180,45,180,62)
    drawing+=box(32,66,64,36,'TCP H','node accent')+box(96,66,232,36,'데이터')+edge(180,103,180,120)
    drawing+=box(16,124,54,36,'IP H','node accent')+box(70,124,72,36,'TCP H')+box(142,124,202,36,'데이터')+edge(180,161,180,178)
    drawing+=box(4,182,58,36,'링크 H','node accent')+box(62,182,48,36,'IP H')+box(110,182,60,36,'TCP H')+box(170,182,144,36,'데이터')+box(314,182,42,36,'FCS')
    drawing+=edge(180,219,180,236)+text(180,260,'0101… → 전기·광·무선 신호')
    return svg(drawing,'TCP/IP와 Ethernet의 캡슐화 예: 데이터에 TCP 헤더, IP 헤더, 링크 헤더와 FCS를 붙인 뒤 신호로 전송',279)

def tcp_mapping():
    drawing=''
    for index,(number,_,name,*_) in enumerate(reversed(LAYERS)):
        y=12+index*40
        drawing+=box(8,y,137,32,f'{number} · {name}')
    for y,height,label in [(12,112,'응용'),(132,32,'전송'),(172,32,'인터넷'),(212,72,'네트워크 액세스')]:
        drawing+=box(208,y,144,height,label,'node accent')
    for y in [28,68,108]:drawing+=edge(146,y,206,68)
    for y in [148,188]:drawing+=edge(146,y,206,y)
    for y in [228,268]:drawing+=edge(146,y,206,248)
    drawing+=text(76,311,'OSI 7계층','muted')+text(280,311,'TCP/IP 4계층','muted')
    return svg(drawing,'OSI 응용·표현·세션은 TCP/IP 응용, 전송은 전송, 네트워크는 인터넷, 데이터링크·물리는 네트워크 액세스로 대응',326)

def build_osi_chapter():
    body=mnemonic()+'<p class="caption">낮은 계층부터 <b>물리 → 데이터링크 → 네트워크 → 전송 → 세션 → 표현 → 응용</b>. “대”는 데이터링크를 기억하기 위한 글자입니다.</p>'
    body+='<h3 class="subhead">1. 일곱 계층을 한 그림으로 보기</h3><div class="osi-overview">'+layer_stack()+'</div>'
    body+='<div class="matrix-wrap"><table><caption class="caption">계층별 역할 · 데이터 단위(PDU) · 예시</caption><thead><tr><th>계층</th><th>역할</th><th>데이터 단위</th><th>대표 장비·주소</th><th>프로토콜·기능 예시</th></tr></thead><tbody>'
    for number,_,name,en,cue,pdu,device,examples,_ in LAYERS:
        body+=f'<tr><th>{number} · {name}<br><small>{en}</small></th><td>{cue}</td><td>{pdu}</td><td>{device}</td><td>{examples}</td></tr>'
    body+='</tbody></table></div><p class="caption">PDU 이름은 TCP/IP·Ethernet을 설명할 때 쓰는 대표 구분입니다. 장비는 여러 계층을 함께 처리할 수 있습니다. 세션·표현 계층의 예시는 특정 TCP/IP 프로토콜과의 엄격한 일대일 대응이 아니라 기능을 이해하기 위한 것입니다.</p>'
    body+='<h3 class="subhead">2. 계층마다 던지는 질문</h3><div class="grid">'
    questions=['어떤 신호로 전달할까?','바로 이웃 장치에 어떻게 전달할까?','어느 네트워크로 가야 할까?','어떤 프로세스에 어떻게 전달할까?','대화를 어떻게 관리할까?','어떤 형식으로 이해할까?','응용 프로그램이 어떤 통신 서비스를 쓸까?']
    for number,_,name,en,cue,pdu,device,examples,detail in LAYERS:
        body+=f'<article class="concept"><div class="card-top"><h3>{number} · {name}</h3><span class="tag">L{number}</span></div><div class="en">{en}</div><div class="mini-level">{questions[number-1]}</div><p>{detail}</p><div class="pattern-cue">↳ {cue}</div></article>'
    body+='</div><div class="note"><b>주소 세 가지</b><span><b>MAC 주소 · L2</b> = 같은 링크에서 프레임을 전달할 대상 / <b>IP 주소 · L3</b> = 네트워크를 넘는 논리 주소 / <b>포트 번호 · L4</b> = 호스트 안의 통신 종단을 구분. <b>2 맥 · 3 아이피 · 4 포트</b>로 연결해 외우세요.</span></div>'
    body+='<h3 class="subhead">3. 송신은 감싸고, 수신은 벗기기</h3><div class="grid"><article class="concept"><h3>캡슐화 · 7 → 1</h3>'+encapsulation()+'<p>아래 계층으로 내려가며 제어 정보를 덧붙입니다. 그림의 H는 헤더, FCS는 프레임 오류 검출용 값입니다. TCP와 Ethernet을 사용하는 예시입니다.</p></article><article class="concept"><h3>역캡슐화 · 1 → 7</h3><div class="mini-level">신호 → 프레임 → 패킷 → TCP 세그먼트 → 데이터</div><p>받는 쪽은 계층별 제어 정보를 확인하고 벗겨 상위 계층으로 전달합니다. “물대네전세표응”은 계층 번호가 올라가는 순서이며, 송신 데이터가 내려가는 순서는 반대입니다.</p><p><b>UDP를 쓰면?</b><br>L4의 단위는 UDP 데이터그램으로 부릅니다. 전송 계층이라는 이유만으로 항상 재전송·순서 보장을 제공하는 것은 아닙니다.</p></article></div>'
    body+='<h3 class="subhead">4. OSI 7계층과 TCP/IP 4계층 연결</h3><div class="osi-overview">'+tcp_mapping()+'</div><p class="caption">OSI는 기능을 나누는 참조 모델이고 TCP/IP는 실제 인터넷 프로토콜을 설명하는 모델입니다. 5계층 TCP/IP 설명에서는 네트워크 액세스를 데이터링크·물리로 나누기도 합니다.</p>'
    body+='<div class="note"><b>보안 프로토콜과 연결</b><span>표현 계층의 기능에 암호화가 있다는 것과 모든 암호화 프로토콜을 L6으로 분류한다는 것은 별개입니다. IPsec은 IP 계층을 보호하고, TLS는 실제 TCP 위·응용 아래에서 동작합니다. <a href="#concept/security-protocols">보안 프로토콜의 계층 비교 보기 →</a></span></div>'
    body+='<div class="source-row"><a class="source" href="https://www.ibm.com/think/topics/osi-model" target="_blank" rel="noopener noreferrer">↗ IBM · OSI model</a><a class="source" href="https://learn.microsoft.com/en-us/windows-hardware/drivers/network/windows-network-architecture-and-the-osi-model" target="_blank" rel="noopener noreferrer">↗ Microsoft · OSI 하위 계층</a><a class="source" href="https://docs.oracle.com/cd/E19253-01/816-4554/ipov-7/index.html" target="_blank" rel="noopener noreferrer">↗ Oracle · OSI 참조 모델</a></div>'
    return '<section id="osi-layers" class="chapter"><header class="chapter-head"><span class="chapter-no">17</span><div><p class="eyebrow">CONCEPT MAP / 17</p><h2>OSI 7계층 · 물대네전세표응</h2><p>각 계층의 역할과 데이터 단위를 연결하고, 주소·장비·캡슐화 순서를 구분합니다.</p></div></header>'+body+'</section>'
