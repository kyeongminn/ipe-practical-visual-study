"""Algorithm-first classification of symmetric and asymmetric cryptography."""
from security_topic import box, text, edge, svg
from drm_topics import card, chapter, note

KEY='encryption'

BLOCK_ALGORITHMS=[
    ('DES','Data Encryption Standard','64','56','Feistel 구조 · 16라운드. DES의 실제 암호 키는 56비트이며 패리티를 포함한 표현은 64비트다.','DES = 블록 64 / 키 56'),
    ('3DES','Triple DES · TDEA','64','DES 키 2·3개','DES 연산을 세 번 조합한 방식. DES보다 키를 확장했지만 블록 크기는 여전히 64비트다.','3DES = DES 세 번 / 블록은 64'),
    ('AES','Advanced Encryption Standard','128','128·192·256','Rijndael을 기반으로 한 SPN 계열 블록 암호. AES-128·192·256의 숫자는 키 길이이며 블록 크기는 모두 128비트다.','AES = 블록 128 / 키 128·192·256'),
    ('SEED','국산 블록 암호','128','128','KISA에서 개발. 16라운드 Feistel 구조로, 블록과 키의 길이가 모두 128비트다.','SEED = 128 / 128 / Feistel'),
    ('ARIA','국산 범용 블록 암호','128','128·192·256','Involutional SPN 구조. 키 길이에 따라 12·14·16라운드를 수행한다.','ARIA = 128 / 128·192·256 / SPN'),
    ('IDEA','International Data Encryption Algorithm','64','128','스위스에서 개발한 PES를 개선한 알고리즘. 64비트 블록과 128비트 키를 연결해 기억한다.','IDEA = 블록 64 / 키 128'),
    ('Skipjack','NSA · Clipper Chip','64','80','미국 NSA에서 개발했으며 Clipper Chip과 연결되는 과거 블록 암호다.','Skipjack = 블록 64 / 키 80 / Clipper Chip')]

def algorithm_size(block,key):
    drawing=''
    for x,label,value in [(7,'블록 크기 · 비트',block),(190,'키 구성' if key.startswith('DES') else '키 길이 · 비트',key)]:
        drawing+=f'<rect x="{x}" y="15" width="163" height="69" rx="9" class="node {"accent" if x==190 else ""}"/>'
        drawing+=text(x+81.5,39,label,'muted')+text(x+81.5,66,value)
    return svg(drawing,f'블록 크기 {block}비트, 키 길이 {key}'+('비트' if not key.startswith('DES') else ''),103)

def role_diagram(name,role):
    drawing=box(7,27,134,47,name)+edge(143,51,211,51)+box(214,27,139,47,role,'node accent')
    return svg(drawing,name+'의 주된 역할: '+role,103)

def key_flow(kind):
    if kind=='symmetric':
        left,right='송신자 · 암호화','수신자 · 복호화'
        key_left=key_right='공유 비밀키 K'
        top_left,top_right,transit='평문 입력','평문 복원','암호문'
        caption='같은 비밀키 K를 안전하게 공유'
    elif kind=='asymmetric':
        left,right='송신자 · 암호화','수신자 · 복호화'
        key_left,key_right='수신자 공개키','수신자 개인키'
        top_left,top_right,transit='평문 입력','평문 복원','암호문'
        caption='수신자의 한 쌍 · 공개키 ≠ 개인키'
    else:
        left,right='송신자 · 서명','수신자 · 검증'
        key_left,key_right='송신자 개인키','송신자 공개키'
        top_left,top_right,transit='메시지의 해시','검증 결과','전자서명'
        caption='서명은 송신자 개인키 / 검증은 공개키'
    drawing=text(74,20,top_left,'muted')+text(286,20,top_right,'muted')
    drawing+=box(6,39,136,48,left)+edge(144,63,214,63)+box(218,39,136,48,right)
    drawing+=text(180,49,transit,'muted')
    drawing+=box(6,133,136,44,key_left,'node accent')+edge(74,131,74,89)
    drawing+=box(218,133,136,44,key_right,'node accent')+edge(286,131,286,89)
    drawing+=text(180,215,caption,'muted')
    return svg(drawing,f'{left}에는 {key_left}, {right}에는 {key_right}를 사용한다',238)

def block_stream(block):
    if block:
        drawing=''.join(box(9+i*115,27,111,45,label,'node accent') for i,label in enumerate(['블록 1','블록 2','블록 3']))
        drawing+=text(180,112,'고정 크기 블록 단위로 처리','muted')
    else:
        drawing=box(7,27,139,45,'평문 스트림')+text(180,58,'⊕')+box(214,27,139,45,'키 스트림','node accent')
        drawing+=text(180,112,'비트·바이트 흐름을 키 스트림과 결합','muted')
    return svg(drawing,'블록 암호의 고정 크기 단위' if block else '스트림 암호의 키 스트림 결합',137)

def build_encryption_chapter():
    body=note('종류부터 구분','<b>대칭키 = 같은 비밀키</b> / <b>비대칭키 = 공개키·개인키 한 쌍.</b> 알고리즘 이름을 먼저 두 계열로 나누고, 대칭키는 블록·스트림, 비대칭키 계열은 암호화·키 합의·서명 역할까지 연결해 기억하자.')
    body+='<h3 class="subhead">1. 알고리즘 분류 지도</h3><div class="branch-tree"><div class="family"><h3>대칭키 종류</h3><ul class="tree-list"><li><b>블록 암호</b><span>DES · 3DES · AES<br>SEED · ARIA · IDEA · Skipjack</span></li><li><b>스트림 암호</b><span>RC4 · ChaCha20</span></li></ul></div><div class="family"><h3>비대칭키 계열 종류</h3><ul class="tree-list"><li><b>암호화</b><span>RSA · ElGamal</span></li><li><b>타원곡선 계열</b><span>ECC · ECDH / ECDSA 등으로 구체화</span></li><li><b>키 합의 / 전자서명</b><span>DH / DSA · ECDSA</span></li></ul></div></div>'
    body+='<h3 class="subhead">2. 대칭키 · 대표 블록 암호 7종</h3><p class="caption">한 번에 고정 크기의 블록을 처리한다. 시험 학습용 대표 알고리즘을 정리했으며, 아래 숫자는 비트 단위다. 블록 크기와 키 길이를 따로 읽는다.</p><div class="grid three">'
    for name,en,block,key,description,cue in BLOCK_ALGORITHMS:
        body+=card(name,en,algorithm_size(block,key),description,cue)
    body+='</div><div class="matrix-wrap" style="margin-top:18px"><table><thead><tr><th>알고리즘</th><th>블록 크기</th><th>키 길이·구성</th><th>구별 키워드</th></tr></thead><tbody>'
    keywords=['Feistel · 16라운드','DES 세 번','Rijndael · SPN','국산 · Feistel','국산 · Involutional SPN','PES 개선','NSA · Clipper Chip']
    for row,keyword in zip(BLOCK_ALGORITHMS,keywords):
        name,_,block,key,_,_=row
        body+=f'<tr><td><b>{name}</b></td><td>{block}비트</td><td>{key}'+('' if key.startswith('DES') else '비트')+f'</td><td>{keyword}</td></tr>'
    body+='</tbody></table></div>'
    body+=note('숫자 암기','<b>블록 64:</b> DES · 3DES · IDEA · Skipjack<br><b>블록 128:</b> AES · SEED · ARIA<br><b>키 길이 비교:</b> DES 56 / Skipjack 80 / IDEA·SEED 128. AES-256도 블록 크기는 128비트다.')
    body+='<h3 class="subhead">3. 대칭키 · 스트림 암호</h3><div class="grid">'
    body+=card('RC4','Rivest Cipher 4',block_stream(False),'키 스트림을 만들어 평문과 XOR하는 <b>스트림 암호</b>. 블록 암호인 AES·SEED와 구분한다.','RC4 → 대칭키 → 스트림')
    body+=card('ChaCha20','스트림 암호 · 추가 비교',role_diagram('ChaCha20','키 스트림'),'256비트 키를 사용하는 스트림 암호. ARX 연산(덧셈·회전·XOR)을 사용한다.','ChaCha20도 대칭키 · 스트림')
    body+='</div><p class="caption">DES·3DES·RC4·Skipjack 등 과거 알고리즘도 시험 분류 학습을 위해 포함했다. 목록에 있다는 사실이 현재 시스템의 채택을 권장한다는 뜻은 아니다.</p>'
    body+='<h3 class="subhead">4. 비대칭키 계열 · 이름과 역할</h3><div class="grid three">'
    asymmetric=[
      ('RSA','Rivest–Shamir–Adleman','암호화 · 서명','큰 정수의 <b>소인수분해 문제</b>와 연결한다. 암호화와 전자서명에 각각 적절한 방식으로 사용한다.','RSA = 소인수분해'),
      ('ElGamal','이산 로그 계열','공개키 암호화','<b>이산 로그 계열의 수학적 문제</b>에 기반한 공개키 암호화 방식. 같은 이름의 서명 방식과는 절차를 구분한다.','ElGamal = 이산 로그 계열'),
      ('ECC','Elliptic Curve Cryptography','타원곡선 계열','<b>타원곡선 이산 로그 문제</b>를 이용하는 공개키 암호 기술 계열. ECDH는 키 합의, ECDSA는 서명에 사용한다.','ECC = 타원곡선 / ECDH ≠ ECDSA'),
      ('DH','Diffie–Hellman','키 합의','통신 당사자가 <b>공유 비밀을 합의</b>하는 공개키 기법. 실제 메시지를 직접 암·복호화하는 알고리즘과 구분한다.','DH = 키 합의 / ECDH = 타원곡선 기반'),
      ('DSA · ECDSA','Digital Signature Algorithm','전자서명','DSA는 전자서명 알고리즘, ECDSA는 타원곡선 기반 서명 알고리즘. <b>메시지 암호화용이 아니다.</b>','DSA·ECDSA = 서명 생성·검증')]
    for name,en,role,description,cue in asymmetric:
        body+=card(name,en,role_diagram('DSA / ECDSA' if name.startswith('DSA') else name,role),description,cue)
    body+='</div>'+note('공개키 계열 ≠ 모두 암호화','<b>RSA·ElGamal은 암호화</b>, <b>DH·ECDH는 키 합의</b>, <b>DSA·ECDSA는 서명</b>으로 구분한다. ECC는 여러 구체적 방식의 기반이 되는 계열명이다. SHA-256 등 해시는 별도의 단방향 요약 함수다.')
    body+='<h3 class="subhead">5. 이름만 보고 빠르게 분류하기</h3><div class="ribbon"><div><h3>대칭키 · 블록</h3><b>DES · 3DES · AES<br>SEED · ARIA · IDEA · Skipjack</b></div><div><h3>대칭키 · 스트림</h3><b>RC4 · ChaCha20</b></div><div><h3>비대칭키 계열</h3><b>RSA · ElGamal · ECC<br>DH · DSA · ECDSA</b></div></div>'
    body+='<h3 class="subhead">보충 · 키 사용 원리와 계산</h3><details class="recall"><summary>키 흐름 · 전자서명 · 하이브리드 · 키 개수 펼쳐 보기</summary><div class="grid"><article class="concept"><h3>대칭키 · 같은 키</h3>'+key_flow('symmetric')+'</article><article class="concept"><h3>RSA 등 공개키 암호화</h3>'+key_flow('asymmetric')+'</article></div><p><b>전자서명:</b> 송신자 개인키로 서명 → 송신자 공개키로 검증. 서명 자체는 내용을 숨기지 않으며 “개인키 암호화”로 단순화하지 않는다.</p><p><b>하이브리드:</b> 공개키 기법으로 세션키를 설정하고 대칭키로 데이터를 처리한다. 키 전달과 (EC)DH 키 합의는 다른 절차다.</p><p><b>키 개수:</b> n명의 모든 사용자 쌍마다 별도 대칭키를 쓰면 n(n−1)/2개. 각 사용자가 비대칭키 한 쌍씩 가지면 n쌍=2n개. 4명일 때 각각 6개 / 8개다.</p><p><b>용어:</b> 수험서의 “개인키 암호화”는 대칭키를 뜻하기도 한다. 공개키와 짝인 개인키라는 의미와 문맥으로 구분한다.</p></details>'
    return chapter(KEY,'13','암호화 방식 · 대칭키 / 비대칭키','알고리즘 종류 중심 · 블록·스트림 분류, 블록·키 길이, 공개키 계열의 역할',body,[('시나공 · DES·AES·IDEA·Skipjack','https://www.sinagong.co.kr/pds/001001002/books/1074/download-data/297#page=65'),('NIST FIPS 197 · AES','https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf'),('RFC 4269 · SEED','https://www.rfc-editor.org/rfc/rfc4269.html'),('RFC 5794 · ARIA','https://www.rfc-editor.org/rfc/rfc5794.html'),('RFC 8439 · ChaCha20','https://www.rfc-editor.org/rfc/rfc8439.html'),('RFC 6090 · ECC·ECDH·ECDSA','https://www.rfc-editor.org/rfc/rfc6090.html'),('Berkeley · 키 교환·ElGamal','https://securitybook.eecs.berkeley.edu/chapters/lec10.html')])

def encryption_questions(question,field):
    return {KEY:[
      question('crypto-type-des','64비트 블록 · 56비트 키','64비트 블록, 실제 암호 키 56비트, 16라운드 Feistel 구조인 대칭키 알고리즘의 약어는?',[
        field('알고리즘','DES','Data Encryption Standard')],
        'DES입니다. 패리티를 포함한 키 표현은 64비트이지만 실제 암호 키는 56비트입니다.'),
      question('crypto-type-aes','AES의 이름과 블록 크기','① Rijndael 기반으로 128·192·256비트 키를 쓰는 표준 블록 암호의 약어, ② AES-256의 블록 크기를 비트 단위 숫자로 쓰세요.',[
        field('① 알고리즘','AES','Advanced Encryption Standard'),field('② 블록 크기 (비트)','128','128비트','128 bit','128 bits')],
        'AES / 128비트입니다. AES-256의 256은 키 길이이며 블록 크기는 항상 128비트입니다.'),
      question('crypto-type-seed','국산 암호 · Feistel','KISA에서 개발한 국산 블록 암호입니다. 블록 128비트, 키 128비트, 16라운드 Feistel 구조에 해당하는 알고리즘은?',[
        field('알고리즘','SEED','시드')],
        'SEED입니다. 국산 암호인 ARIA와 구분하며, SEED는 블록과 키 모두 128비트입니다.'),
      question('crypto-type-aria','국산 암호 · Involutional SPN','128비트 블록과 128·192·256비트 키를 쓰는 국산 범용 암호로, Involutional SPN 구조에 해당하는 알고리즘은?',[
        field('알고리즘','ARIA','아리아')],
        'ARIA입니다. SEED는 Feistel 구조이며 키 길이도 128비트로 고정됩니다.'),
      question('crypto-type-idea-skipjack','64비트 블록을 쓰는 두 암호','① PES를 개선한 스위스의 알고리즘으로 키 128비트, ② NSA가 개발하여 Clipper Chip에 사용된 알고리즘으로 키 80비트. 두 알고리즘을 쓰세요.',[
        field('① PES 개선','IDEA','International Data Encryption Algorithm','아이디어'),field('② Clipper Chip','Skipjack','Skip jack','스킵잭','스킵 잭')],
        'IDEA / Skipjack입니다. 둘 다 블록 크기는 64비트지만 키 길이는 각각 128비트, 80비트입니다.'),
      question('crypto-type-rsa','소인수분해와 공개키 암호','큰 정수의 소인수분해 문제와 연결되는 공개키 알고리즘으로, 암호화와 전자서명에 사용되는 알고리즘의 약어는?',[
        field('알고리즘','RSA','Rivest Shamir Adleman')],
        'RSA입니다. 대칭키 블록 암호인 AES와 분류가 다릅니다.'),
      question('crypto-type-ecc','타원곡선 계열의 두 역할','ECC 계열에서 ① 키 합의에 사용하는 대표 약어, ② 전자서명에 사용하는 대표 약어를 쓰세요.',[
        field('① 키 합의','ECDH','Elliptic Curve Diffie Hellman'),field('② 전자서명','ECDSA','Elliptic Curve Digital Signature Algorithm')],
        'ECDH / ECDSA입니다. ECC는 타원곡선 기반 기술 계열명이며 구체적인 알고리즘의 역할을 구분해야 합니다.'),
      question('crypto-type-dh-elgamal','공개키 계열의 역할 연결','① 공유 비밀을 합의하는 Diffie–Hellman의 약어, ② 이산 로그 계열의 문제에 기반하며 이름이 El로 시작하는 공개키 암호화 방식을 쓰세요.',[
        field('① 키 합의 약어','DH','Diffie Hellman'),field('② 공개키 암호화','ElGamal','엘가말','엘 가말')],
        'DH / ElGamal입니다. 둘 다 공개키 계열로 학습하지만 DH는 키 합의이며 메시지를 직접 암·복호화하는 역할과 구분합니다.'),
      question('crypto-key-types','같은 키인가, 키 쌍인가?','① 암호화와 복호화에 동일한 비밀키를 쓰는 방식, ② 공개키·개인키 한 쌍을 쓰는 방식을 쓰세요.',[
        field('① 방식','대칭키','대칭키 암호화','대칭키 암호','대칭키 방식','대칭키 암호화 방식','비밀키 암호화','비밀키','공통키','단일키','Symmetric','Symmetric Encryption'),
        field('② 방식','비대칭키','비대칭키 암호화','비대칭키 암호','비대칭키 방식','비대칭키 암호화 방식','공개키','공개키 암호화','Asymmetric','Asymmetric Encryption','Public Key Encryption')],
        '대칭키 / 비대칭키입니다. 대칭키는 같은 비밀키를 공유하고, 비대칭키는 서로 관련된 공개키와 개인키를 사용합니다.'),
      question('crypto-receiver','비밀 메시지를 B에게 보내기','A가 B만 읽을 수 있는 메시지를 RSA 공개키 암호화로 보냅니다. ① A가 암호화에 쓸 키, ② B가 복호화에 쓸 키를 소유자 B까지 포함해 쓰세요.',[
        field('① 암호화 키','B의 공개키','B 공개키','수신자의 공개키','수신자 공개키','받는 사람의 공개키'),
        field('② 복호화 키','B의 개인키','B 개인키','B의 비밀키','수신자의 개인키','수신자 개인키','받는 사람의 개인키')],
        'B(수신자)의 공개키 / B(수신자)의 개인키입니다. 공개키는 배포할 수 있지만 개인키는 B가 비밀로 보관합니다.'),
      question('crypto-signature','A가 보낸 전자서명 검증하기','A가 메시지에 전자서명을 하고 B가 검증합니다. ① A가 서명에 사용할 키, ② B가 검증에 사용할 키를 소유자 A까지 포함해 쓰세요.',[
        field('① 서명 키','A의 개인키','A 개인키','A의 비밀키','송신자의 개인키','송신자 개인키'),
        field('② 검증 키','A의 공개키','A 공개키','송신자의 공개키','송신자 공개키')],
        'A(송신자)의 개인키 / A(송신자)의 공개키입니다. 전자서명은 기밀성이 아니라 무결성·인증·부인 방지를 지원합니다.'),
      question('crypto-block-stream','알고리즘 분류하기','대칭키 암호에서 ① AES·SEED·ARIA, ② RC4의 처리 단위에 따른 암호 분류를 쓰세요.',[
        field('① 분류','블록','블록 암호','블록 암호화','블록 암호화 방식','Block','Block Cipher'),
        field('② 분류','스트림','스트림 암호','스트림 암호화','스트림 암호화 방식','Stream','Stream Cipher')],
        '블록 암호 / 스트림 암호입니다. AES·SEED·ARIA는 고정 크기 블록을 처리하고, RC4는 키 스트림을 이용하는 과거 스트림 암호입니다.'),
      question('crypto-key-count','4명이 통신할 때 키 수','4명이 모든 상대와 통신합니다. ① 대칭키는 서로 다른 사용자 쌍마다 별도 키 하나를 공유합니다. ② 비대칭키는 각자 키 쌍을 하나씩 가집니다. 각 경우의 전체 키 개수를 쓰세요. 키의 복사본은 세지 않습니다.',[
        field('① 대칭키 개수','6','6개'),field('② 비대칭키 개수 (쌍 아닌 낱개)','8','8개')],
        '6개 / 8개입니다. 대칭키: 4×3÷2=6. 비대칭키: 4쌍×2=8. 키 쌍 개수를 묻는다면 4쌍입니다.'),
      question('crypto-hybrid','두 방식을 조합한 구성','공개키 기법으로 세션키를 설정하고, 대량 데이터는 대칭키로 암호화하는 조합 방식을 무엇이라고 하나요?',[
        field('조합 방식','하이브리드','하이브리드 암호','하이브리드 암호화','하이브리드 방식','하이브리드 암호화 방식','혼합 암호','혼합 암호화','Hybrid','Hybrid Encryption')],
        '하이브리드 방식입니다. 공개키 기법으로 키를 설정하고 대칭키로 실제 데이터를 처리합니다. 키 합의는 키 자체를 암호화해 전달하는 방식과 구분합니다.'),
      question('crypto-not-encryption','DH와 SHA-256의 역할','① Diffie–Hellman(DH), ② SHA-256의 주된 역할을 쓰세요. 선택 용어: 키 합의 / 단방향 해시 / 대칭키 복호화.',[
        field('① DH','키 합의','키 교환','키 합의 알고리즘','Key Agreement','Key Exchange'),
        field('② SHA-256','단방향 해시','해시','해시 함수','단방향 해시 함수','Hash','Hash Function','One-way Hash')],
        '키 합의 / 단방향 해시입니다. DH는 공유 비밀을 합의하며, SHA-256은 메시지를 요약합니다. SHA-256에 복호화 키가 있는 것은 아닙니다.')]
    }
