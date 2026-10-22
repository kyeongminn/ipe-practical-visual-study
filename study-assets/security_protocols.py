"""Security protocol revision: layer, protected object, and common distinctions."""
from html import escape
from security_topic import text, box, edge, svg

# Layer numbers are the functional classification commonly used in exam guides.
# TLS is deliberately qualified: it runs above a reliable transport such as TCP.
PROTOCOLS=[
 ('IPsec','L3 · 네트워크','IP 패킷 인증·암호화','IP 계층의 보안 기술 집합. AH·ESP로 IP 패킷을 보호하며 VPN에 활용한다.'),
 ('SSL/TLS','L4* · 전송 보안','응용 통신 채널 보호','TLS는 통신 상대 인증·기밀성·무결성을 제공한다. SSL은 이전 규약이다. 실제 위치는 TCP 위, 응용 프로토콜 아래다.'),
 ('HTTPS','L7 · 응용','HTTP를 TLS로 보호','웹 통신에 TLS를 적용한다. 기본 포트는 443이며, HTTP 메시지를 보호된 연결로 전달한다.'),
 ('S-HTTP','L7 · 응용','HTTP 메시지별 보호','HTTP 메시지 단위로 서명·암호화 등의 보호를 적용하는 별도의 과거 규약. HTTPS와 구분한다.'),
 ('SSH','L7 · 응용','암호화된 원격 접속','보안 원격 로그인·명령 실행 등에 사용한다. 통상 TCP 22번을 쓰며 SFTP도 SSH 기반이다.'),
 ('S/MIME','L7 · 응용','인증서 기반 메일 보안','MIME 메시지에 전자서명·암호화를 적용한다. X.509 인증서를 이용한다.'),
 ('PGP','L7 · 응용','메일·파일 서명·암호화','공개키·대칭키 암호와 전자서명을 조합해 메시지·파일을 보호한다. OpenPGP가 공개 표준 형식이다.'),
 ('L2TP','L2 · 데이터링크','터널링; 암호화 별도','PPP를 터널로 전달한다. L2TP 자체가 데이터 암호화를 제공하는 것은 아니며 IPsec과 결합할 수 있다.'),
 ('PPTP','L2 · 데이터링크','PPP를 GRE로 터널링','PPP 프레임을 GRE로 운반하는 과거 터널링 규약. 터널을 만드는 기능과 암호화 기능을 구분한다.')]

def protocol_preview():
    rows='<div class="mini-protocol-row mini-protocol-head" role="row"><b role="columnheader">프로토콜</b><b role="columnheader">계층 · 수험</b><b role="columnheader">한 줄 요약</b></div>'
    for name,layer,summary,_ in PROTOCOLS:
        rows+=f'<div class="mini-protocol-row" role="row" data-protocol="{escape(name)}"><b role="cell">{escape(name)}</b><span class="mini-protocol-layer" role="cell">{escape(layer)}</span><span role="cell">{escape(summary)}</span></div>'
    return '<div class="mini-protocols" role="table" aria-label="주요 보안 프로토콜의 계층과 역할">'+rows+'</div><p class="mini-hint">* TLS: 실제로 TCP 위·응용 아래<br>IPsec = IP / TLS = 채널 / S/MIME·PGP = 메시지</p>'

def layer_diagram():
    s=''
    for y,level,names in [(8,'L7 · 응용','HTTPS · S-HTTP · SSH · 메일 보안'),(66,'L4* · 전송 보안','SSL/TLS · TCP 위의 보안 채널'),(124,'L3 · 네트워크','IPsec · IP 패킷 보호'),(182,'L2 · 데이터링크','L2TP · PPTP · PPP 터널링')]:
        s+=box(8,y,344,48,'','node')+text(24,y+20,level,'muted','start')+text(24,y+39,names,'','start')
    s+=text(180,253,'계층은 수험 분류 · 보호 대상과 함께 기억','muted')
    return svg(s,'보안 프로토콜의 수험 분류: 응용, 전송 보안, 네트워크, 데이터링크',270)

def channel_diagram():
    s=box(18,8,324,37,'HTTP · 응용 데이터')+edge(180,45,180,65)
    s+=box(18,68,324,43,'TLS · 인증 + 암호화 + 무결성','node accent')+edge(180,111,180,131)
    s+=box(18,134,324,37,'TCP · 신뢰성 있는 데이터 전달')
    s+=text(180,197,'HTTPS의 대표 구조: HTTP → TLS → TCP','muted')
    return svg(s,'HTTP는 TLS 보호를 받고 TLS는 TCP 위에서 동작하는 대표 구조',213)

def packet_diagram(tunnel):
    s=text(180,20,'터널 모드' if tunnel else '전송 모드')
    if tunnel:
        s+=box(8,40,80,49,'새 IP')+box(93,40,65,49,'ESP','node accent')+box(163,40,189,49,'원래 IP + 데이터','zone')
        s+=text(180,121,'원래 IP 패킷 전체를 캡슐화','muted')
    else:
        s+=box(8,40,103,49,'원래 IP')+box(116,40,65,49,'ESP','node accent')+box(186,40,166,49,'상위 계층 데이터','zone')
        s+=text(180,121,'원래 IP 헤더를 유지하고 페이로드 보호','muted')
    return svg(s,'IPsec '+('터널 모드의 캡슐화' if tunnel else '전송 모드의 보호 범위')+' 개념도',141)

def source(name,rfc):
    return f'<a class="source" href="https://www.rfc-editor.org/rfc/rfc{rfc}" target="_blank" rel="noopener noreferrer">↗ IETF RFC {rfc} · {name}</a>'

def build_security_protocols_chapter():
    body='<div class="note"><b>암기 기준</b><span><b>계층 + 보호 대상</b>을 한 쌍으로 기억하세요. IP 패킷은 IPsec, 통신 채널은 TLS, 원격 접속은 SSH, 메일 메시지는 S/MIME·PGP입니다.</span></div>'
    body+='<h3 class="subhead">1. 어느 계층에서 무엇을 보호하는가?</h3><div style="max-width:580px;margin:0 auto">'+layer_diagram()+'</div>'
    body+='<p class="caption">L2·L3·L7은 수험서의 기능 중심 분류입니다. TLS는 통상 “전송계층 보안”으로 묶지만 실제 TCP 위·응용 아래에서 동작하며, OSI 5·6계층으로 설명하는 자료도 있습니다. TLS라는 이름만으로 TCP 자체의 보안 기능이라고 해석하지 말고, 문제의 분류 기준을 따르세요.</p>'
    body+='<div class="matrix-wrap"><table><caption class="caption">프로토콜 · 계층 · 한 줄 요약</caption><thead><tr><th>프로토콜</th><th>계층 · 수험 분류</th><th>핵심 역할</th></tr></thead><tbody>'
    body+=''.join(f'<tr><th>{escape(name)}</th><td>{escape(layer)}</td><td>{escape(summary)}</td></tr>' for name,layer,summary,_ in PROTOCOLS)+'</tbody></table></div>'
    body+='<h3 class="subhead">2. IPsec · AH / ESP / IKE</h3><div class="grid three">'
    for title,cue,desc in [
      ('AH · Authentication Header','인증 · 무결성','데이터 출처 인증과 무결성, 재전송 공격 방지 등에 쓰입니다. <b>내용 암호화에 의한 기밀성은 제공하지 않습니다.</b>'),
      ('ESP · Encapsulating Security Payload','암호화 + 인증·무결성','기밀성을 제공할 수 있고 인증·무결성도 지원합니다. 실제 제공 기능은 설정에 따르므로 “ESP는 암호화만 한다”로 외우지 마세요.'),
      ('IKE · Internet Key Exchange','인증 · 키 합의 · SA 관리','통신 상대를 인증하고 사용할 알고리즘·키와 SA(Security Association, 보안 연관)를 협상·관리합니다. AH·ESP가 사용할 보호 조건을 마련합니다.')]:
        body+=f'<article class="concept"><h3>{title}</h3><div class="mini-level">{cue}</div><p>{desc}</p></article>'
    body+='</div><div class="grid"><article class="concept"><h3>전송 모드 · Transport</h3>'+packet_diagram(False)+'<p>주로 호스트 간 통신에서 사용합니다. 그림은 보호 범위를 이해하기 위한 ESP 축약도입니다.</p></article><article class="concept"><h3>터널 모드 · Tunnel</h3>'+packet_diagram(True)+'<p>VPN 게이트웨이 간 연결 등에 사용합니다. 원래 패킷 바깥에 새 IP 헤더가 붙습니다.</p></article></div>'
    body+='<h3 class="subhead">3. TLS와 응용 보안 프로토콜</h3><div class="grid"><article class="concept"><h3>TLS · 통신 경로 보호</h3>'+channel_diagram()+'<p>TLS의 핸드셰이크로 상대를 인증하고 키를 합의한 뒤, 레코드 계층에서 데이터를 보호합니다. 일반적으로 서버 인증을 하며 클라이언트 인증도 가능합니다.</p></article><article class="concept"><h3>HTTPS vs S-HTTP</h3><div class="mini-level">HTTPS = HTTP 통신에 TLS 적용</div><div class="mini-level">S-HTTP = HTTP 메시지 단위 보호</div><p>HTTPS는 보호된 채널로 웹 통신을 전달합니다. S-HTTP는 별도의 메시지 중심 규약입니다. 두 이름을 같은 뜻으로 쓰지 않습니다.</p><p><b>포트 암기</b>: HTTPS 기본 443 / SSH 통상 22. SSL/TLS 자체에 모든 용도가 공유하는 단일 포트가 있는 것은 아닙니다.</p></article></div>'
    body+='<div class="grid">'
    for name,layer,summary,detail in PROTOCOLS:
        if name in ['SSH','S/MIME','PGP']:
            body+=f'<article class="concept"><h3>{name}</h3><div class="en">{layer}</div><div class="mini-level">{summary}</div><p>{detail}</p></article>'
    body+='</div><div class="note"><b>메일 보안 구분</b><span>S/MIME은 X.509 인증서 기반, PGP는 공개키·대칭키·서명을 조합한 메시지 보호로 기억합니다. HTTPS나 메일 전송 구간 TLS와 달리 메시지 자체를 암호화·서명할 수 있습니다.</span></div>'
    body+='<h3 class="subhead">4. 터널링과 암호화 구분</h3><div class="grid">'
    for name,layer,summary,detail in PROTOCOLS:
        if name in ['L2TP','PPTP']:
            body+=f'<article class="concept"><h3>{name}</h3><div class="en">{layer}</div><div class="mini-level">{summary}</div><p>{detail}</p></article>'
    body+='</div><div class="note"><b>시험 키워드 연결</b><span>AH·ESP·IP 계층 → <b>IPsec</b> / 보안 채널·SSL 후속 → <b>TLS</b> / 원격 로그인 → <b>SSH</b> / MIME·인증서·메일 서명 → <b>S/MIME</b> / PPP 터널링·IPsec과 결합 → <b>L2TP</b></span></div>'
    body+='<div class="source-row">'+''.join(source(name,rfc) for name,rfc in [('IPsec',4301),('TLS 1.3',8446),('HTTP·HTTPS',9110),('SSH',4251),('S/MIME',8551),('OpenPGP',9580),('L2TP',2661),('PPTP',2637),('S-HTTP',2660),('IKEv2',7296)])+'</div>'
    return '<section id="security-protocols" class="chapter"><header class="chapter-head"><span class="chapter-no">16</span><div><p class="eyebrow">CONCEPT MAP / 16</p><h2>보안 프로토콜</h2><p>계층과 보호 대상을 함께 보고, IPsec·TLS·응용 보안·터널링을 구분합니다.</p></div></header>'+body+'</section>'
