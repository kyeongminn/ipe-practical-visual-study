"""DRM role diagrams and the eight exam-oriented technology categories."""
from html import escape
from security_topic import box, text, edge, svg

COMPONENT_SOURCE='https://www.sinagong.co.kr/pds/001001002/books/1074/download-data/297#page=117'
TECH_SOURCE='https://www.sinagong.co.kr/pds/001001001/books/1041/download-data/270#page=34'
PAST_SOURCE='https://cbt.algisa.com/bank/exam_view.jsp?cid=236&id=426&iid=136&page=2'
FIRST_PAST='https://devinus.tistory.com/19?category=982939'

def flow(left,right,caption=''):
    shape=box(7,28,143,47,left)+edge(151,51,206,51)+box(209,28,144,47,right,'node accent')
    if caption:shape+=text(180,115,caption,'muted')
    return svg(shape,left+' → '+right,137)

def card(title,en,picture,meaning,cue):
    return f'<article class="concept"><h3>{title}</h3><div class="en">{en}</div>{picture}<p>{meaning}</p><div class="pattern-cue">{cue}</div></article>'

def note(label,body):return f'<div class="note"><b>{label}</b><span>{body}</span></div>'

def chapter(key,number,title,subtitle,content,sources):
    return f'<section id="{key}" class="chapter"><header class="chapter-head"><span class="chapter-no">{number}</span><div><p class="eyebrow">CONCEPT MAP / {number}</p><h2>{title}</h2><p>{subtitle}</p></div></header>{content}<div class="source-row">'+''.join(f'<a class="source" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">↗ {escape(label)}</a>' for label,url in sources)+'</div></section>'

def build_drm_chapters():
    # Content delivery and license issuance use separate lanes so roles remain distinct.
    delivery=''
    for y,label in [(10,'콘텐츠 제공자'),(87,'패키저'),(164,'보안 컨테이너'),(241,'콘텐츠 분배자'),(318,'콘텐츠 소비자')]:
        delivery+=box(77,y,206,48,label,'node accent' if label=='패키저' else 'node')
        if y<318:delivery+=edge(180,y+49,180,y+74)
    delivery+=text(180,400,'원본 → 포장 → 보호 → 유통 → 이용','muted')
    licenseflow=box(86,11,188,49,'클리어링 하우스','node accent')
    licenseflow+=edge(180,61,180,114)+text(250,91,'② 발급','muted')
    licenseflow+='<rect x="76" y="118" width="208" height="65" rx="10" class="node"/>'+text(180,143,'라이선스')+text(180,165,'이용 조건 · 키 관련 정보','muted')
    licenseflow+=edge(180,184,180,263)+text(250,229,'③ 확인','muted')
    licenseflow+='<rect x="41" y="267" width="278" height="99" rx="12" class="zone"/>'+text(180,291,'소비자 측 프로그램')+box(66,307,228,41,'DRM 컨트롤러','node accent')
    licenseflow+='<path d="M66 327 H20 V36 H84" class="edge" marker-end="url(#arrow)"/>'+text(51,221,'① 요청','muted')
    licenseflow+=text(180,400,'사용권 발급과 실제 이용 통제는 구분','muted')
    content=note('DRM의 목적','<b>Digital Rights Management · 디지털 저작권 관리.</b> 콘텐츠의 생성·유통·이용 과정에서 권리와 사용 조건을 관리한다.')
    content+='<div class="grid drm-overview"><article class="concept"><h3>콘텐츠 전달 경로</h3>'+svg(delivery,'콘텐츠 제공자 → 패키저 → 보안 컨테이너 → 콘텐츠 분배자 → 콘텐츠 소비자',422)+'</article><article class="concept"><h3>사용권 확인 경로</h3>'+svg(licenseflow,'소비자 측에서 사용권을 요청하고 클리어링 하우스가 라이선스를 발급하면 DRM 컨트롤러가 이용 조건을 확인한다',422)+'</article></div><p class="caption">역할을 구분하기 위한 개념 흐름도다. 라이선스는 미리 발급·저장될 수도 있으며, 실제 서비스에서는 여러 역할을 하나의 시스템이 맡기도 한다.</p>'
    rows=[
      ('콘텐츠 제공자','Contents Provider',flow('저작권자','원본 제공'),'보호할 원본 콘텐츠와 권리의 출발점.','제공자 = 콘텐츠를 제공하는 저작권자'),
      ('패키저','Packager',flow('원본 + 설명 정보','포장 · 암호화'),'콘텐츠와 메타데이터를 묶어 보호된 배포물을 만든다.','포장·암호화는 패키저 / 유통은 분배자'),
      ('보안 컨테이너','Security Container',flow('원본 콘텐츠','보호된 유통 용기'),'콘텐츠를 안전하게 전달하도록 보호하는 전자적 수단.','컨테이너 = 보호하여 담는 역할'),
      ('콘텐츠 분배자','Contents Distributor',flow('보호된 콘텐츠','유통 · 전달'),'보호된 배포물을 소비자에게 전달하는 유통 주체.','분배자는 패키징 프로그램을 뜻하지 않음'),
      ('콘텐츠 소비자','Customer / Consumer',flow('구매 · 사용 허가','콘텐츠 이용'),'허가된 조건에 따라 콘텐츠를 사용하는 주체.','소비자 = 구매·이용하는 쪽'),
      ('DRM 컨트롤러','DRM Controller',flow('이용 요청','권한 · 조건 확인'),'배포된 콘텐츠를 허용 범위 안에서 쓰도록 통제한다.','컨트롤러 = 실제 이용을 통제하는 프로그램'),
      ('클리어링 하우스','Clearing House',flow('사용권 · 키 관리','라이선스 발급'),'사용권·키·라이선스를 관리하며 사용량에 따른 정산도 맡는다.','하우스 = 라이선스·키·정산의 관리 창구')]
    content+='<h3 class="subhead">구성요소 7개 · 누가 무엇을 맡는가?</h3><div class="grid three">'+''.join(card(*row) for row in rows)+'</div>'
    content+=note('핵심 구분','<b>패키저는 만든다 → 분배자는 전달한다 → 컨트롤러는 사용을 통제한다.</b> 클리어링 하우스는 사용권과 라이선스를 관리한다.')
    content+='<div class="matrix-wrap"><table><thead><tr><th>비교</th><th>첫 번째 역할</th><th>두 번째 역할</th></tr></thead><tbody><tr><td>패키저 / 분배자</td><td>포장·암호화</td><td>보호된 콘텐츠 유통</td></tr><tr><td>컨테이너 / 컨트롤러</td><td>안전하게 담고 전달</td><td>실제로 쓸 수 있는지 통제</td></tr><tr><td>하우스 / 컨트롤러</td><td>라이선스 발급·관리</td><td>발급된 조건에 따라 이용 통제</td></tr></tbody></table></div>'
    components=chapter('drm-components','09','DRM 구성요소','콘텐츠는 어떻게 전달되고, 누가 사용 권한을 관리할까?',content,[('시나공 2026 실기 · 구성요소',COMPONENT_SOURCE),('Microsoft PlayReady · 라이선스 획득의 구현 예','https://learn.microsoft.com/en-us/playready/overview/license-acquisition')])
    # Eight syllabus categories. Grouping is a study aid, not a separate standard.
    tech_rows=[
      ('암호화','Encryption',flow('읽을 수 있는 내용','암호로 보호'),'콘텐츠·라이선스의 내용을 암호로 보호한다.','핵심: 내용을 보호'),
      ('키 관리','Key Management',flow('암호 키','보관 · 배포'),'암호화에 쓰는 키를 안전하게 저장하고 전달한다.','핵심: 키의 저장·분배'),
      ('암호화 파일 생성','Packager / Encrypted file creation',flow('원본 + 메타데이터','보호 배포물 생성'),'보호된 콘텐츠 파일로 포장·생성한다.','구성요소 “패키저”가 수행하는 기능'),
      ('식별 기술','Identification',flow('콘텐츠','콘텐츠 식별자'),'어떤 콘텐츠인지 구별할 식별 체계를 표현한다.','핵심: 어떤 콘텐츠인가?'),
      ('저작권 표현','Right Expression',flow('이용 권리 · 조건','라이선스에 표현'),'허용 행위·제약 등 사용권 내용을 기술한다.','예: 7일 열람 · 인쇄 불가'),
      ('정책 관리','Policy Management',flow('발급 · 이용 규칙','정책 설정 · 관리'),'라이선스 발급과 이용에 적용할 정책을 관리한다.','권리 표현은 조건 기술 / 정책 관리는 규칙 운영'),
      ('크랙 방지','Tamper Resistance',flow('우회 · 변조 시도','보호 기능 방어'),'프로그램 변조·우회로 무단 사용되는 것을 막는다.','핵심: 보호 장치의 우회를 어렵게'),
      ('인증','Authentication',flow('사용자 제시 정보','신원 확인'),'발급·이용 판단의 기준이 되는 사용자를 확인한다.','인증: 누구인가? / 인가: 무엇을 할 수 있는가?')]
    content=note('분류 기준','<b>구성요소는 역할·주체·도구</b>, <b>기술요소는 구현 기능</b>이다. 아래 8개는 수험서 분류이며 실제 구현은 여러 기능을 결합한다.')
    content+='<div class="ribbon"><div><h3>보호 · 생성</h3><p>암호화 · 키 관리<br>암호화 파일 생성</p></div><div><h3>식별 · 규칙</h3><p>식별 기술 · 저작권 표현<br>정책 관리</p></div><div><h3>확인 · 방어</h3><p>인증 · 크랙 방지</p></div></div><p class="caption">위의 세 묶음은 8가지 기술요소를 기억하기 위한 학습용 분류다.</p><div class="grid three">'+''.join(card(*row) for row in tech_rows)+'</div>'
    content+=note('8개 암기','<b>암 · 키 · 파 / 식 · 저 · 정 / 크 · 인</b><br>암호화 · 키 관리 · 파일 생성 / 식별 · 저작권 표현 · 정책 관리 / 크랙 방지 · 인증')
    content+='<h3 class="subhead">기출에서 자주 헷갈리는 구분</h3><div class="grid"><article class="concept"><h3>방화벽은 이 8개에 포함되지 않음</h3><p>네트워크 접근 통제 기술이다. 서비스 보안에 쓸 수 있지만, 수험서의 DRM 기술요소 목록에 넣지 않는다.</p></article><article class="concept"><h3>콘텐츠 오류 감지·복구도 별도</h3><p>파일 손상을 찾아 복구하는 기능과, 저작권·이용 권한을 보호하는 DRM의 목적을 구분한다.</p></article></div><div class="matrix-wrap" style="margin-top:18px"><table><thead><tr><th>질문</th><th>연결할 기술요소</th></tr></thead><tbody><tr><td>암호 키는 어디에 보관하고 어떻게 전달하나?</td><td>키 관리</td></tr><tr><td>어떤 콘텐츠인지 구별하나?</td><td>식별 기술</td></tr><tr><td>라이선스에 이용 조건을 어떻게 적나?</td><td>저작권 표현</td></tr><tr><td>발급·사용 규칙을 어떻게 운영하나?</td><td>정책 관리</td></tr><tr><td>요청한 사용자는 누구인가?</td><td>인증</td></tr></tbody></table></div>'
    technologies=chapter('drm-technologies','10','DRM 기술요소','암호화만으로 끝나지 않는 콘텐츠 보호 기능 8가지',content,[('시나공 2025 필기 · 기술요소 8개',TECH_SOURCE),('W3C ODRL · 권리와 조건의 표현','https://www.w3.org/TR/odrl-model/'),('Microsoft PlayReady · 콘텐츠 암호화 구현 예','https://learn.microsoft.com/en-us/playready/packaging/content-encryption')])
    return [components,technologies]

def drm_questions(question,field):
    return {
    'drm-components':[
      question('drm-role-past','잘못 붙은 구성요소 이름','“원본과 메타데이터를 배포 가능한 형태로 묶어 암호화한다”를 콘텐츠 분배자의 역할로 적었습니다. 올바른 구성요소 이름으로 고치세요.',[field('올바른 명칭','패키저','Packager')],
        '패키저입니다. 콘텐츠 분배자는 보호된 콘텐츠를 유통하는 주체입니다. 역할을 바꿔 적는 선지를 구분하는 기출 요지를 재구성했습니다.',
        '2020년 4회 필기 36번 · 기출 재구성',PAST_SOURCE,'지안에듀 CBT · 필기 보강'),
      question('drm-role-house','사용권·키·정산 관리','사용권 관리와 라이선스 발급, 암호 키 관리, 사용량에 따른 정산을 맡는 곳은?',[
        field('구성요소','클리어링 하우스','클리어링하우스','Clearing House')], '클리어링 하우스입니다. 소비자 측의 실제 이용 통제 프로그램은 DRM 컨트롤러입니다.'),
      question('drm-role-container','담는 것과 통제하는 것','① 콘텐츠를 안전하게 유통하도록 보호하는 전자적 수단, ② 배포된 콘텐츠의 이용 권한을 통제하는 프로그램.',[
        field('① 보호하여 담는 역할','보안 컨테이너','Security Container'),field('② 이용 통제 역할','DRM 컨트롤러','DRM Controller','컨트롤러')],
        '보안 컨테이너 / DRM 컨트롤러입니다. Container는 보호하여 담는 역할, Controller는 허용된 이용을 통제하는 역할입니다.'),
      question('drm-role-parties','제공자와 소비자','① 콘텐츠의 원본을 제공하는 저작권자, ② 구매·사용 허가를 받아 콘텐츠를 이용하는 주체.',[
        field('① 원본 제공','콘텐츠 제공자','컨텐츠 제공자','Contents Provider','Content Provider'),field('② 이용 주체','콘텐츠 소비자','컨텐츠 소비자','Customer','Consumer')],
        '콘텐츠 제공자 / 콘텐츠 소비자입니다. 보호된 콘텐츠를 중간에서 유통하는 주체는 콘텐츠 분배자입니다.'),
      question('drm-role-license','파일을 받았으니 무제한 이용할까?','DRM으로 보호된 파일을 내려받았다는 사실만으로 이용 기간·기기·행위의 제한이 모두 사라지나요? O 또는 X.',[
        field('O / X','X','아니오','아니요','No')], 'X입니다. 파일 전달과 사용권은 별개입니다. 라이선스의 이용 조건을 DRM 컨트롤러 등이 적용합니다.')],
    'drm-technologies':[
      question('drm-tech-firewall','기술요소 목록 밖의 항목','크랙 방지, 정책 관리, 암호화, 방화벽 중 수험서의 DRM 기술요소 8개에 포함되지 않는 항목을 쓰세요.',[
        field('해당하지 않는 기술','방화벽','방화벽 기술','Firewall')],
        '방화벽입니다. 서비스 보안에는 활용될 수 있지만 DRM의 8가지 기술요소 분류와 구분합니다.',
        '2020년 1·2회 통합 필기 27번 · 기출 재구성',FIRST_PAST,'공개 기출 정리: devinus · 필기 보강'),
      question('drm-tech-recovery','권리 보호와 오류 복구','암호화·키 관리, 콘텐츠 식별, 오류 감지·복구, 라이선스 발급·관리 중 DRM 목적과 가장 거리가 먼 항목은?',[
        field('해당 항목','오류 감지 및 복구','콘텐츠 오류 감지 및 복구','오류 감지·복구','오류 감지 복구')],
        '콘텐츠 오류 감지 및 복구입니다. 저작권과 허가된 사용을 관리하는 기능과 파일 오류 복구를 구분합니다.',
        '2020년 4회 필기 40번 · 기출 재구성',PAST_SOURCE,'지안에듀 CBT · 필기 보강'),
      question('drm-tech-protect','보호와 파일 생성','① 내용을 암호로 보호, ② 암호 키를 보관·전달, ③ 원본을 보호된 배포 파일로 포장·생성하는 기술.',[
        field('① 내용 보호','암호화','Encryption'),field('② 키 보관·전달','키 관리','Key Management'),field('③ 보호 파일 생성','암호화 파일 생성','Packager','패키저')],
        '암호화 / 키 관리 / 암호화 파일 생성입니다. 생성 기능을 수행하는 도구를 구성요소 분류에서는 패키저라고 합니다.'),
      question('drm-tech-rights','식별·표현·정책 관리','① 어떤 콘텐츠인지 구분하는 체계, ② 라이선스의 이용 조건을 기술, ③ 라이선스 발급·이용 규칙을 관리.',[
        field('① 콘텐츠 구별','식별 기술','식별','Identification'),field('② 이용 조건 기술','저작권 표현','Right Expression','Rights Expression'),field('③ 규칙 운영','정책 관리','Policy Management')],
        '식별 기술 / 저작권 표현 / 정책 관리입니다. 같은 라이선스를 다뤄도 표현하는 일과 정책을 운영하는 일을 구분합니다.'),
      question('drm-tech-tamper','우회 방어와 신원 확인','① 프로그램을 변조해 보호 기능을 우회하는 시도를 방어, ② 라이선스 요청 사용자가 누구인지 확인.',[
        field('① 우회·변조 방어','크랙 방지','Tamper Resistance'),field('② 사용자 신원 확인','인증','Authentication','사용자 인증')],
        '크랙 방지 / 인증입니다. 인증은 신원 확인이고, 인가는 확인된 대상에게 무엇을 허용할지 결정하는 것입니다.')]
    }
