"""Visual, exam-oriented attack terminology and conceptual practice."""
from html import escape
from security_topic import box, text, edge, svg
from drm_topics import card, chapter, note, flow

KEY='attacks'

def table(headers,rows):
    return '<div class="matrix-wrap"><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def heading(id,label):return f'<h3 class="subhead" id="{id}" tabindex="-1">{label}</h3>'

def ddos_picture():
    drawing=''
    for y,label in [(12,'공격 노드 A'),(83,'공격 노드 B'),(154,'공격 노드 C')]:
        drawing+=box(8,y,137,43,label)+edge(147,y+21,227,104)
    drawing+=box(230,82,122,48,'서비스 서버','node accent')+text(180,232,'분산된 여러 노드 → 자원 고갈·서비스 방해','muted')
    return svg(drawing,'여러 공격 노드가 하나의 서비스 서버를 공격하는 분산 서비스 거부의 개념도',252)

DOS_ROWS=[
 ('SYN Flooding','TCP 연결의 미완료 상태를 많이 만들어 자원을 소모.','SYN · 연결 대기'),
 ('Smurf','피해자 주소로 위장한 ICMP 요청에 대한 다수의 응답이 피해자에게 몰림.','ICMP · 반사·증폭'),
 ('LAND','출발지와 목적지를 피해자 자신으로 설정한 패킷으로 취약한 처리를 자극.','출발지 = 목적지'),
 ('Teardrop','비정상적으로 겹치는 IP 단편 등을 재조립하는 처리의 취약점 악용.','단편 · 재조립 오류'),
 ('Ping of Death','과도한 크기·비정상 ICMP 패킷의 재조립·처리 취약점 악용.','비정상 크기 · Ping'),
 ('Slowloris','HTTP 요청을 불완전하게 유지하여 연결 자원을 장시간 점유.','느린 요청 · 연결 유지')]

NETWORK=[
 ('스니핑','Sniffing','통신 패킷','내용 엿보기','통신 중인 패킷을 <b>몰래 관찰·도청</b>한다. 암호화된 패킷을 수집했다고 내용을 바로 해독할 수 있는 것은 아니다.','Sniffing = 엿듣기'),
 ('스푸핑','Spoofing','가짜 신원·주소','정상 대상으로 위장','신원이나 주소 정보를 <b>정상 대상처럼 속이는</b> 행위. IP·ARP·DNS 등 위장 대상에 따라 구분한다.','Spoofing = 속이기 · 아래 세 주소 구분'),
 ('세션 하이재킹','Session Hijacking','탈취한 세션','인증된 사용자 행세','인증된 세션을 탈취하거나 장악해 <b>정상 사용자처럼 접근</b>한다. 비밀번호 자체를 알아내는 공격과 구분한다.','Session Hijacking = 세션 가로채기'),
 ('중간자 공격','Man-in-the-Middle · MITM','통신 당사자 사이','가로채기 · 변경','통신 경로 중간에 끼어 <b>정보를 가로채거나 바꾼다</b>. ARP 스푸핑 등이 수단으로 쓰일 수 있으나 두 용어가 동의어인 것은 아니다.','MITM = 통신 사이에 끼어듦')]

WEB=[
 ('SQL 삽입','SQL Injection · SQLi','조작된 입력값','DB 질의에 영향','입력이 SQL 명령 구조에 섞여 <b>DB 조회·변조나 인증 우회</b>를 유발한다. 핵심 구분은 “데이터가 명령으로 해석되는가”이다.','SQLi = 데이터가 SQL 명령으로 해석'),
 ('크로스 사이트 스크립팅','Cross-Site Scripting · XSS','악성 스크립트','브라우저에서 실행','웹 페이지나 DOM 처리의 결함으로 <b>피해자 브라우저에서 스크립트</b>가 실행된다. 저장형·반사형·DOM 기반 등이 있다.','XSS = 브라우저의 스크립트 실행'),
 ('크로스 사이트 요청 위조','Cross-Site Request Forgery · CSRF','유도된 요청','사용자 권한 악용','로그인된 사용자의 브라우저가 <b>원치 않는 요청</b>을 보내게 유도한다. 브라우저가 자동 전송하는 인증 정보와 서버의 요청 검증 부족을 악용한다.','CSRF = 인증된 사용자의 요청 위조')]

SOCIAL=[
 ('피싱','Phishing','신뢰하는 기관 사칭','정보 입력 유도','정상 기관·사람인 것처럼 속여 <b>비밀번호 등 민감 정보나 행동</b>을 유도한다. 이메일·가짜 사이트 등 여러 매체를 이용한다.','Phishing = 신뢰를 미끼로 정보 낚기'),
 ('스피어 피싱','Spear Phishing','특정 개인·조직','맞춤형 미끼','특정 대상을 조사하고 그 대상에 맞춘 내용으로 속이는 <b>표적형 피싱</b>. 단순히 발송 횟수가 많다는 뜻이 아니다.','Spear = 표적을 정한 피싱'),
 ('파밍','Pharming','정상 사이트 접속','가짜 사이트로 유도','DNS나 호스트 설정 등의 변조로 정상 주소에 접속하려는 사용자를 <b>가짜 사이트로 돌린다</b>.','피싱 = 미끼 / 파밍 = 접속 경로 조작'),
 ('워터링 홀','Watering Hole','자주 방문하는 곳','방문자를 감염','목표 집단이 자주 방문하는 웹사이트를 침해해 <b>방문하는 표적을 노린다</b>.','사람을 직접 낚기보다 자주 가는 곳을 오염')]

MALWARE=[
 ('바이러스 · Virus','다른 파일·프로그램에 붙어 감염·복제','숙주에 결합'),
 ('웜 · Worm','숙주 파일에 붙지 않고 독립적으로 자기 복제·전파','자기 전파'),
 ('트로이 목마 · Trojan Horse','정상 프로그램처럼 위장해 악성 기능 수행','위장 · 자기 복제는 본질적 기능 아님'),
 ('랜섬웨어 · Ransomware','파일 암호화·접근 차단 등으로 금전 요구','데이터·접근권을 인질로 삼음'),
 ('루트킷 · Rootkit','침입 흔적·악성 동작·권한 유지를 숨기는 도구 집합','은폐'),
 ('백도어 · Backdoor','정상 인증·접근 절차를 우회하는 비밀 통로','우회 통로'),
 ('키로거 · Keylogger','키 입력 등을 기록해 정보 수집','입력 기록')]

def build_attack_chapter():
    body=note('먼저 큰 그림','<b>가용성을 방해하는가, 통신을 엿보거나 위장하는가, 입력·인증을 악용하는가, 사람을 속이는가?</b> 이 네 질문으로 먼저 분류하고, 악성코드 용어를 따로 연결하자. 아래 묶음은 학습용이며 서로 겹칠 수 있다.')
    body+='<div class="preset-row">'+''.join(f'<button type="button" data-concept-jump="attack-{id}">{label} ↓</button>' for id,label in [('dos','서비스 거부'),('network','도청·위장'),('web','웹·인증'),('social','사회공학'),('malware','악성코드')])+'</div>'
    body+=heading('attack-dos','A. 서비스 거부 · DoS / DDoS')
    body+='<div class="grid"><article class="concept"><h3>DDoS · 분산 서비스 거부</h3>'+ddos_picture()+'<p>정상 사용자가 서비스를 이용하지 못하도록 자원을 고갈시키거나 처리를 방해한다. <b>DDoS는 여러 분산된 공격원</b>이 참여한다.</p></article><article class="concept"><h3>공격 규모와 수법은 다른 축</h3><div class="mini-level">DoS: 서비스 거부</div><div class="mini-level">DDoS: 분산된 서비스 거부</div><p>분산 여부와 SYN·HTTP 같은 수법은 별개다. 같은 수법을 여러 노드가 사용하면 분산 공격이 될 수 있다.</p><p><b>봇넷</b>은 공격자가 제어하는 다수의 감염 장치 집합. 개별 장치를 좀비·봇, 지시 체계를 C&amp;C/C2라고 부른다.</p><div class="pattern-cue">연결: 가용성 A 침해</div></article></div>'
    body+=table(['수법','핵심 특징','암기 단서'],DOS_ROWS)
    body+='<p class="caption">LAND·Teardrop·Ping of Death는 과거의 취약한 처리 구현과 연결해 학습한다. ICMP나 단편 자체가 공격이라는 뜻은 아니다. Slowloris는 트래픽 양만 크게 만드는 공격과 구분한다.</p>'
    body+=heading('attack-network','B. 도청 · 위장 · 가로채기')+'<div class="grid">'
    for title,en,left,right,meaning,cue in NETWORK:body+=card(title,en,flow(left,right),meaning,cue)
    body+='</div>'+table(['스푸핑 종류','무엇을 속이나?'],[('IP 스푸핑','패킷의 출발지 IP 주소'),('ARP 스푸핑','같은 링크의 IP↔MAC 대응 정보'),('DNS 스푸핑·캐시 오염','이름 해석 응답·캐시의 이름↔주소 정보')])
    body+=heading('attack-web','C. 웹 · 입력 처리 · 인증 공격')+'<div class="grid three">'
    for title,en,left,right,meaning,cue in WEB:body+=card(title,en,flow(left,right),meaning,cue)
    body+='</div>'+table(['함께 구분할 공격','핵심'],[
      ('경로 조작 · Path/Directory Traversal','파일 경로 검증을 우회해 허용 영역 밖 파일에 접근'),
      ('버퍼 오버플로 · Buffer Overflow','버퍼 경계를 넘어 메모리를 덮어써 오동작·제어 흐름 훼손 유발'),
      ('무차별 대입 · Brute Force','가능한 후보를 반복 시도. 사전 공격은 단어·후보 목록을 활용'),
      ('크리덴셜 스터핑 · Credential Stuffing','다른 곳에서 유출된 계정·비밀번호 쌍을 재사용해 로그인 시도')])
    body+=note('SQLi · XSS · CSRF','<b>SQLi는 DB 명령 / XSS는 브라우저의 스크립트 / CSRF는 인증된 사용자의 요청.</b> CSRF에 악성 스크립트 실행이나 쿠키 탈취가 반드시 필요한 것은 아니다. XSS와 CSRF는 함께 악용될 수도 있다.')
    body+=heading('attack-social','D. 사람을 속이거나 표적을 노리는 공격')+'<div class="grid">'
    for title,en,left,right,meaning,cue in SOCIAL:body+=card(title,en,flow(left,right),meaning,cue)
    body+='</div>'+table(['피싱 변형·유사 용어','구별 기준'],[
      ('스미싱 · Smishing','SMS 등 문자 메시지'),('비싱 · Vishing','음성·전화'),('큐싱 · Qshing / Quishing','QR 코드로 유도'),('타이포스쿼팅 · Typosquatting','오타·유사 도메인을 이용')])
    body+='<div class="ribbon" style="margin-top:18px"><div><h3>APT · 지능형 지속 위협</h3>특정 표적에 장기간 침투·잠복하며 목적을 추구하는 위협. 여러 수법을 조합한다.</div><div><h3>제로데이 · Zero-day</h3>기존에 알려지지 않은 취약점을 악용하는 공격. 단순히 모든 미패치 취약점을 뜻하지 않는다.</div><div><h3>공급망 공격 · Supply Chain</h3>공급업체·의존성·빌드·업데이트 경로를 침해해 이용자까지 영향을 준다.</div></div>'
    body+=heading('attack-malware','E. 악성코드 · 공격에 쓰이는 프로그램과 기능')
    body+='<div class="grid"><article class="concept"><h3>위장과 전파는 다른 기준</h3>'+flow('정상 앱처럼 위장','악성 기능 실행')+'<p><b>트로이 목마</b>는 위장에, <b>바이러스·웜</b>은 감염·전파 방식에 초점이 있다. 한 악성 프로그램이 여러 특징을 함께 가질 수 있다.</p></article><article class="concept"><h3>기능으로 구분</h3>'+flow('침입 후 악성 동작','탈취 · 차단 · 은폐')+'<p>랜섬웨어는 금전 요구, 루트킷은 은폐, 백도어는 우회 통로, 키로거는 입력 기록을 중심으로 기억한다.</p></article></div>'+table(['용어','주된 특징','암기 단서'],MALWARE)
    body+=note('공격 기법과 보안 목표 연결','스니핑은 주로 <b>기밀성</b>, 데이터 변조는 <b>무결성</b>, 서비스 거부는 <b>가용성</b>과 연결된다. 실제 공격은 여러 보안 목표를 동시에 침해할 수 있다.')
    sources=[('시나공 · 시험 관련 공격 용어','https://www.sinagong.co.kr/pds/001001002/books/1074/download-data/297#page=67'),('Cisco · DDoS 분류','https://sec.cloudapps.cisco.com/security/center/resources/guide_ddos_defense.html'),('Cisco · ARP 스푸핑','https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus3000/sw/security/503_u2_2/Cisco_n3k_security_cg_503_u2_2_chapter11.pdf'),('OWASP · SQL 삽입','https://community.owasp.org/attacks/SQL_Injection'),('OWASP · XSS','https://community.owasp.org/attacks/xss/'),('OWASP · CSRF','https://community.owasp.org/attacks/csrf'),('OWASP · 세션 하이재킹','https://community.owasp.org/attacks/Session_hijacking_attack'),('OWASP · 계정 대입 공격 구분','https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html'),('OWASP · 경로 조작','https://community.owasp.org/attacks/Path_Traversal'),('OWASP · 버퍼 오버플로','https://community.owasp.org/vulnerabilities/Buffer_Overflow'),('FBI · 피싱·파밍·스푸핑','https://www.fbi.gov/how-we-can-help-you/common-frauds-and-scams/spoofing-and-phishing'),('CISA · 표적형·문자·음성 피싱','https://www.cisa.gov/sites/default/files/2024-02/Update%20to%20Phishing%20General%20Security%20Postcard_01.01.2024.pdf'),('Microsoft · 악성코드 분류','https://learn.microsoft.com/en-us/defender-xdr/criteria'),('NIST · 제로데이','https://csrc.nist.gov/glossary/term/Zero_Day_Attack')]
    return chapter(KEY,'14','공격 기법','서비스 거부 · 도청·위장 · 웹·인증 · 사회공학 · 악성코드',body,sources)

def attack_questions(question,field):
    return {KEY:[
      question('attack-dos-distributed','분산된 서비스 거부','다수의 공격 노드가 한 서비스로 요청을 보내 정상 이용을 방해합니다. “분산 서비스 거부”의 약어를 쓰세요.',[field('영문 약어','DDoS','Distributed Denial of Service')],
        'DDoS입니다. DoS는 서비스 거부, DDoS는 여러 분산된 공격원을 사용하는 서비스 거부입니다.'),
      question('attack-dos-keywords','서비스 거부 단서 연결','① TCP 연결 미완료 상태를 대량 생성, ② 피해자로 위장한 ICMP 요청의 다수 응답 집중, ③ 출발지와 목적지를 피해자 자신으로 설정. 각 수법을 쓰세요.',[
        field('① 연결 대기','SYN Flooding','SYN Flood','SYN 플러딩','SYN 플러딩 공격'),field('② 반사·증폭','Smurf','Smurf Attack','스머프','스머핑','Smurfing'),field('③ 동일 주소','LAND','LAND Attack','랜드','랜드 공격')],
        'SYN Flooding / Smurf / LAND입니다. 서비스 거부의 분산 여부와 구체적인 수법은 다른 분류 축입니다.'),
      question('attack-fragments','단편과 비정상 크기','① 겹치는 IP 단편의 재조립 처리 취약점 악용, ② 과도한 크기·비정상 ICMP 패킷 처리 취약점 악용. 이름을 쓰세요.',[
        field('① 단편 재조립','Teardrop','Teardrop Attack','티어드롭','티어드롭 공격'),field('② 비정상 Ping','Ping of Death','죽음의 핑','PoD')],
        'Teardrop / Ping of Death입니다. 과거 취약한 처리 구현과 연결되는 수법이며, 정상적인 단편이나 ICMP 자체가 공격인 것은 아닙니다.'),
      question('attack-network-terms','엿듣기·속이기·세션 탈취','① 패킷 내용을 도청, ② 신원·주소를 위장, ③ 인증된 세션을 탈취하여 정상 사용자처럼 접근. 용어를 쓰세요.',[
        field('① 도청','스니핑','Sniffing'),field('② 위장','스푸핑','Spoofing'),field('③ 세션 탈취','세션 하이재킹','세션 하이젝킹','세션 하이재킹 공격','Session Hijacking')],
        '스니핑 / 스푸핑 / 세션 하이재킹입니다. ARP 스푸핑은 IP와 MAC 대응 정보를 속이는 예입니다.'),
      question('attack-web-three','SQLi · XSS · CSRF','① 입력이 DB 질의 구조에 영향을 줌, ② 피해자 브라우저에서 악성 스크립트 실행, ③ 로그인된 사용자의 브라우저가 원치 않는 요청 전송. 약어·이름을 쓰세요.',[
        field('① DB','SQL Injection','SQLi','SQL 삽입','SQL 인젝션'),field('② 브라우저','XSS','Cross Site Scripting','크로스 사이트 스크립팅'),field('③ 인증된 요청','CSRF','Cross Site Request Forgery','크로스 사이트 요청 위조')],
        'SQL Injection / XSS / CSRF입니다. CSRF는 쿠키 탈취나 악성 스크립트 실행이 반드시 필요한 공격이 아닙니다.'),
      question('attack-social-target','표적·접속 경로·방문지','① 특정 개인·조직에 맞춘 피싱, ② DNS·호스트 설정 등으로 정상 접속을 가짜 사이트로 유도, ③ 표적이 자주 찾는 사이트를 침해하여 방문자를 노림. 용어를 쓰세요.',[
        field('① 표적 피싱','스피어 피싱','Spear Phishing'),field('② 가짜 접속','파밍','Pharming'),field('③ 방문지 오염','워터링 홀','워터링홀','Watering Hole','Watering Hole Attack')],
        '스피어 피싱 / 파밍 / 워터링 홀입니다. 특정 표적, 접속 경로, 자주 방문하는 사이트라는 단서를 구분하세요.'),
      question('attack-phishing-channels','문자·음성·QR 코드','피싱의 매체를 구분합니다. ① 문자 메시지, ② 음성·전화, ③ QR 코드에 해당하는 용어를 쓰세요.',[
        field('① 문자','스미싱','Smishing'),field('② 음성','비싱','Vishing','보이스 피싱'),field('③ QR','큐싱','Qshing','Quishing')],
        '스미싱 / 비싱 / 큐싱입니다. 피싱이라는 넓은 범주 안에서 유도 매체를 구분하는 용어입니다.'),
      question('attack-malware-propagation','바이러스·웜·트로이 목마','① 숙주 파일에 붙어 감염·복제, ② 숙주 파일에 붙지 않고 독립적으로 자기 복제·전파, ③ 정상 프로그램으로 위장해 악성 기능 실행. 용어를 쓰세요.',[
        field('① 숙주 감염','바이러스','Virus'),field('② 자기 전파','웜','Worm'),field('③ 위장','트로이 목마','트로이목마','Trojan','Trojan Horse')],
        '바이러스 / 웜 / 트로이 목마입니다. 실제 악성코드는 여러 특징을 함께 가질 수 있습니다.'),
      question('attack-malware-purpose','인질·은폐·우회 통로','① 파일 암호화·접근 차단 등으로 금전 요구, ② 침입·악성 동작을 숨기는 도구 집합, ③ 정상 인증을 우회하는 비밀 통로. 용어를 쓰세요.',[
        field('① 금전 요구','랜섬웨어','Ransomware'),field('② 은폐','루트킷','Rootkit'),field('③ 우회','백도어','Backdoor','Back Door','Trapdoor','Trap Door')],
        '랜섬웨어 / 루트킷 / 백도어입니다. 키로거는 입력 기록에 초점이 있습니다.'),
      question('attack-special-threats','지속 위협·미지 취약점·공급망','① 특정 표적에 장기간 침투·잠복하며 여러 수법을 조합, ② 기존에 알려지지 않은 취약점 악용, ③ 공급업체·빌드·업데이트 경로를 침해하여 이용자까지 공격. 이름·약어를 쓰세요.',[
        field('① 지속 위협','APT','지능형 지속 위협','지능형 지속 공격','Advanced Persistent Threat','Advanced Persistent Threats'),field('② 미지 취약점','제로데이','제로 데이','제로데이 공격','Zero Day','Zero Day Attack','0 day'),field('③ 공급 경로','공급망 공격','공급망','Supply Chain Attack')],
        'APT / 제로데이 / 공급망 공격입니다. APT는 하나의 도구명이 아니며, 제로데이를 모든 미패치 취약점의 동의어로 외우지 마세요.'),
      question('attack-credential-stuffing','유출된 계정 쌍 재사용','다른 서비스에서 이미 유출된 아이디·비밀번호 쌍을 이용해 로그인하는 공격은?',[
        field('공격 이름','크리덴셜 스터핑','크리덴셜 스터핑 공격','크리덴셜 스터핑 공격 기법','크리덴셜스터핑','Credential Stuffing')],
        '크리덴셜 스터핑입니다. 모든 가능한 후보를 추측하는 방식과 달리 유출된 계정 쌍의 재사용이 핵심 단서입니다.')]
    }
