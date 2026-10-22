"""Only practical-exam questions with checked year/round and public evidence.

Prompts are concise study restatements of the identified exam questions, not
new exercises relabelled as past papers. Original official wording is not claimed.
"""
from itertools import permutations
from security_topic import text, svg

SOURCES={
 'gilbut2020':('길벗 · 2020년 1회 실기 기출 수록 PDF','https://marketing.gilbut.co.kr/files/event/sinagongit/sinagong_pass100.pdf'),
 'sso2019':('코딩하는 핑가 · 2019년 2회 실기 복원','https://ss-o.tistory.com/112'),
 'sso2021':('코딩하는 핑가 · 2021년 3회 실기 복원','https://ss-o.tistory.com/162'),
 'ja2021':('J.A. · 2021년 실기 회차별 복원','https://yumei1992.tistory.com/entry/정처기-실기-2021'),
 'patterns':('greenyellow-s · 실기 디자인 패턴 기출','https://greenyellow-s.tistory.com/215'),
 'ang2022':('AngzavA · 2022년 3회 실기 복원','https://ang-z-ava.tistory.com/18'),
 'min2022':('minlog · 2022년 3회 실기 복원','https://jimin-log.tistory.com/116'),
 'juble2023':('juble · 2023년 3회 실기 복원','https://juble00.tistory.com/entry/정보처리기사-실기-기출-2023년-3회'),
 'juble2024':('juble · 2024년 3회 실기 복원','https://juble00.tistory.com/entry/정보처리기사-실기-기출-2024년-3회'),
 'pill2024':('코딩 알약 · 2024년 1회 실기 오답노트','https://coding-pill.tistory.com/entry/2024년-1회-정보처리기사-실기-기출문제-오답노트'),
 'movie2024':('우리의 영화를 시작해 · 2024년 2회 실기 풀이','https://start-our-movie.tistory.com/38'),
 'life2023':('Life-Journey · 2023년 2회 실기 복원','https://chobopark.tistory.com/420'),
 'juble2025':('juble · 2025년 1회 실기 복원','https://juble00.tistory.com/entry/정보처리기사-실기-기출-2025년-1회')}

PRACTICE_NOTES={
 'cocomo':'연관 실기 기출: 아래 문항은 COCOMO 유형을 직접 묻는 문제가 아니라 같은 비용·일정 산정 영역의 LOC 계산 기출입니다.',
 'drm-components':'연관 실기 기출: 개편 전 전산영어에서 출제된 DRM 식별 소문항입니다. 구성요소 7개의 이름을 각각 묻는 기출로 바꿔 표시하지 않았습니다.',
 'drm-technologies':'연관 실기 기출: DRM 보호 기술을 식별하는 개편 전 전산영어 소문항입니다. DRM 구성요소 페이지와 같은 출제 문항을 연결했으며, 기술요소 8개를 각각 묻는 기출은 아닙니다.',
 'patterns':'선택한 7가지 패턴의 범위에서 회차·출처를 확인한 실기 기출만 연결했습니다.',
 'routing-protocols':'기존 문제은행 160번은 직접 작성 예시여서 제외하고, 회차가 확인된 RIP·OSPF 실기 기출로 교체했습니다.'}

def package_picture():
    drawing='<path d="M65 45 V26 H145 L163 45 H295 V155 H65 Z" class="node"/>'
    drawing+='<path d="M65 45 H295" class="edge"/>'+text(180,106,'관련 모델 요소 묶음')
    return svg(drawing,'원문 폴더 형태 기호를 개념적으로 다시 그린 그림',178)

def build_practical_bank(question,field):
    bank={key:[] for key in ['uml-rel','uml-types','cocomo','patterns','network','whitebox','principles','security-cia','drm-components','drm-technologies','routing-protocols','version-control','encryption','attacks']}
    def add(key,slug,year,round,title,prompt,fields,explain,source,locator,*,part='',related='',visual='',self_check=False,page=None,canonical=None):
        label,url=SOURCES[source]
        if page:url+=f'#page={page}'
        exam=f'{year}년 {round}회 실기 · '+('개편 전 · ' if year<2020 else '')+'복원 기출'
        if part:exam+=' · '+part
        q=question('ipe-past-'+slug,title,prompt,fields,explain,exam,url,label,visual,self_check)
        q['provenance']={'qualification':'정보처리기사','exam_type':'실기','year':year,'round':round,'source_kind':'publisher' if source=='gilbut2020' else 'public_reconstruction','source_locator':locator,'verified_on':'2026-10-22','canonical_id':canonical or f'{year}-{round}-{slug}','part':part,'related_scope':related,'wording':'출제 내용 유지 · 학습용 요약 표현'}
        bank[key].append(q)
        return q

    add('uml-rel','uml-rel-2024-3',2024,3,'UML 관계 기호','세 관계 기호의 이름을 그림 순서대로 쓰세요. 복원 도형은 같은 의미의 기호로 다시 그렸습니다.',[
        field('① 관계','연관','연관 관계','Association'),field('② 관계','일반화','Generalization'),field('③ 관계','의존','Dependency')],
        '연관 / 일반화 / 의존입니다. 연결선의 종류와 삼각형 끝을 구분합니다.','juble2024','UML 클래스 관계 문항',visual='relations')

    add('uml-types','class-2021-3',2021,3,'속성과 메서드를 담는 UML','UML에서 속성과 메서드를 포함하는 다이어그램의 이름을 쓰세요.',[field('다이어그램','클래스','클래스 다이어그램','Class','Class Diagram')],
        '클래스 다이어그램입니다.','sso2021','속성·메서드 다이어그램 문항')
    add('uml-types','package-2023-3',2023,3,'폴더 모양으로 요소를 묶는 UML','폴더 형태로 관련 모델 요소를 그룹화하고 그룹 사이 관계를 표현하는 UML 다이어그램은? 원문의 폴더 기호를 다시 그렸습니다.',[field('다이어그램','패키지','패키지 다이어그램','Package','Package Diagram')],
        '패키지 다이어그램입니다.','juble2023','폴더 기호의 다이어그램 문항',visual=package_picture())

    add('cocomo','loc-2020-1',2020,1,'연관 기출 · LOC 개발 기간','LOC로 예측한 규모는 30,000라인입니다. 개발자 5명이 각각 월 300라인을 작성할 때 개발 기간은 몇 개월인가요?',[field('기간 (개월)','20','20개월')],
        '30,000 ÷ (5×300) = 20개월. COCOMO 모형 식을 적용하는 문항은 아닙니다.','gilbut2020','2020년 1회 실기 6번',page=6,related='비용·기간 산정의 LOC 연관 기출')

    add('patterns','factory-2021-3',2021,3,'생성을 하위 클래스에 맡기기','상위 클래스는 객체 생성의 규약을 두고, 생성할 구체 객체는 하위 클래스가 결정하는 디자인 패턴은?',[
        field('패턴','팩토리 메서드','팩토리 메소드','팩토리','Factory Method','FactoryMethod')],
        '팩토리 메서드입니다.','sso2021','하위 클래스의 객체 생성 문항')
    add('patterns','bridge-observer-2022-3',2022,3,'추상·구현 분리와 변경 통지','① 추상과 구현을 따로 변화시킬 수 있게 분리, ② 한 객체의 변경을 관련된 여러 객체에 알림. 각 패턴을 쓰세요.',[
        field('① 분리','브리지','브릿지','Bridge'),field('② 통지','옵저버','관찰자','Observer')],
        'Bridge / Observer입니다.','ang2022','Bridge·Observer 빈칸 문항')
    add('patterns','proxy-2023-1',2023,1,'실제 객체 앞의 대리 객체','실제 객체를 대신하는 객체를 두어 호출·참조·실행 시점 등을 제어하는 패턴은?',[field('패턴','프록시','프락시','Proxy')],
        '프록시입니다.','patterns','2023년 1회차 proxy 문항')

    add('network','adhoc-2021-2',2021,2,'기반 시설 없는 임시 네트워크','고정된 기반 시설 없이 단말이 망을 구성하며 연결 구조가 동적으로 바뀝니다. 긴급 구조·군사 현장 등에 쓰이는 이 네트워크는?',[
        field('네트워크','애드혹','애드 혹','애드혹 네트워크','Ad hoc','Ad hoc Network','MANET')],
        '애드혹 네트워크입니다.','ja2021','2021년 2회 네트워크 문항')
    add('network','vpn-2024-3',2024,3,'공용망 위의 사설 연결','공용 네트워크에서 사설 네트워크의 연결을 확장하며, IPsec·SSL·L2TP 등의 기술과 관련되는 용어의 약어는?',[field('약어','VPN','Virtual Private Network')],
        'VPN입니다.','juble2024','VPN 설명 문항')
    add('network','adhoc-2024-3',2024,3,'중앙 관리 없는 무선 연결','중앙 관리나 고정 인프라 없이 노드들이 직접 연결되고, 긴급 회의·구조 등의 상황에서 임시로 구성되는 네트워크는?',[
        field('네트워크','애드혹','애드 혹','애드혹 네트워크','Ad hoc','Ad hoc Network')],
        'Ad-hoc Network입니다.','juble2024','인프라 없는 네트워크 문항')

    coverage_fields=lambda:[field('① 문장 실행','문장','구문','Statement','Statement Coverage'),field('② 참·거짓 분기','결정','분기','Decision','Branch','Decision Coverage','Branch Coverage'),field('③ 개별 조건','조건','Condition','Condition Coverage')]
    add('whitebox','coverage-2021-2',2021,2,'화이트박스 검증 기준','① 모든 실행문을 적어도 한 번 검사, ② 결정 결과의 참·거짓 검사, ③ 각 개별 조건의 참·거짓 검사. 각 검증 기준을 쓰세요.',coverage_fields(),
        '문장 / 결정(분기) / 조건입니다.','ja2021','2021년 2회 화이트박스 검증 문항')
    add('whitebox','coverage-2024-3',2024,3,'테스트 커버리지 구분','① 각 문장의 실행 여부, ② 각 분기의 실행 여부, ③ 복합식 속 개별 조건의 T/F 검사 여부. 해당 커버리지를 쓰세요.',coverage_fields(),
        '문장 / 분기 / 조건 커버리지입니다.','juble2024','테스트 커버리지 문항')
    add('whitebox','ep-2023-3',2023,3,'점수 구간의 대표값','점수를 0~59, 60~69, 70~79, 80~89, 90~100으로 나누고 각각 55·66·77·88·99를 검사했습니다. F·D·C·B·A의 기대 결과와 비교하는 기법은?',[
        field('기법','동치 분할','동치 분할 검사','동등 분할','동등 분할 검사','Equivalence Partitioning','Equivalence Partitioning Testing')],
        '동치(동등) 분할 검사입니다.','juble2023','구간별 대표 점수의 기법 식별 문항')
    add('whitebox','cause-effect-2021-3',2021,3,'입력과 출력의 논리 관계','입력 조건 사이 관계와 출력에 대한 영향을 정리해 효과적인 테스트 조합을 고릅니다. 해당 기법을 쓰세요.',[
        field('기법','원인 효과 그래프','원인 효과 그래프 검사','원인-효과 그래프','Cause Effect Graph','Cause Effect Graphing','Cause Effect Graphing Testing')],
        '원인–효과 그래프 검사입니다.','sso2021','입력·출력 관계 기반 테스트 문항')
    add('whitebox','mcdc-2024-1',2024,1,'개별 조건의 독립적인 영향','각 조건이 다른 조건의 영향을 받지 않고 전체 결정 결과를 독립적으로 바꾸는지 확인하는 커버리지는?',[
        field('커버리지','MC/DC','MCDC','Modified Condition Decision Coverage','변경 조건 결정','변경 조건 결정 커버리지','변경 조건 결정 검증 기준')],
        'MC/DC(변경 조건·결정 커버리지)입니다.','pill2024','개별 조건의 독립적 영향 커버리지 문항')

    add('principles','pesticide-2020-1',2020,1,'살충제 패러독스 설명','테스트의 살충제 패러독스가 뜻하는 현상을 설명하세요.',[
        field('서술 답안','같은 테스트 케이스를 반복하면 새로운 결함을 발견하는 효과가 줄어드는 현상이다.')],
        '같은 사례의 반복으로 새 결함 발견 효과가 줄어든다는 뜻을 포함했는지 비교하세요. 서술형은 직접 평가합니다.','gilbut2020','2020년 1회 실기 13번',self_check=True,page=167)

    add('security-cia','availability-2019-2',2019,2,'정보 접근을 계속 보장하기','DoS/DDoS나 접속 경로 장애로 저해되며, 인가된 사람이 필요할 때 정보에 접근할 수 있어야 한다는 보안 요소는?',[
        field('보안 요소','가용성','Availability')],
        '가용성입니다.','sso2019','정보보호 문항의 가용성 소문항',part='가용성 소문항')

    for key in ['drm-components','drm-technologies']:
        add(key,key+'-2019-2',2019,2,'연관 기출 · 전산영어 DRM','디지털 매체의 저작권을 보호하고 무단 유통을 제한하며, 암호화·워터마크 등으로 허가된 이용을 관리하는 시스템의 약어 또는 영문 명칭은?',[
            field('용어','DRM','Digital Rights Management','디지털 저작권 관리')],
            'DRM입니다. 구성요소나 기술요소 목록을 묻는 문항이 아니라 DRM을 식별하는 출제 소문항입니다.','sso2019','전산영어 문항 중 DRM 소문항',part='DRM 소문항',related='DRM 정의의 연관 기출',canonical='2019-2-drm')

    add('routing-protocols','rip-2023-3',2023,3,'홉 수와 거리 벡터','거리 벡터 방식으로 홉 수를 기준 삼아 경로를 고르고 최대 유효 홉 수가 15인 라우팅 프로토콜의 약어는?',[field('약어','RIP','Routing Information Protocol')],
        'RIP입니다.','juble2023','거리 벡터·15홉 프로토콜 문항')
    add('routing-protocols','ospf-2024-1',2024,1,'Dijkstra와 링크 상태','RIP를 보완하고, 링크 상태를 반영하며 Dijkstra 알고리즘으로 최단 경로를 구하는 라우팅 프로토콜은?',[field('약어','OSPF','Open Shortest Path First')],
        'OSPF입니다.','pill2024','Dijkstra 라우팅 프로토콜 문항')

    orders=[' '.join(items) for items in permutations(['CVS','SVN','Git'])]
    add('version-control','vcs-2022-3',2022,3,'형상관리 도구 선택','보기에서 형상관리 도구 세 개를 골라 이름을 쓰세요. 순서는 자유입니다.\n보기: ATM, CVS, OLAP, DDoS, SVN, Cyber Kill Chain, OLTP, Git',[
        field('도구 세 개 · 순서 자유',*orders)],
        'CVS / SVN / Git입니다.','min2022','형상관리 도구 선택 문항')

    add('encryption','des-2021-3',2021,3,'64비트 블록 · 56비트 키','블록 크기가 64비트, 실제 키 길이가 56비트이며 16라운드를 쓰는 암호 알고리즘은?',[field('알고리즘','DES','Data Encryption Standard')],
        'DES입니다.','sso2021','IBM·64비트 블록·56비트 키 문항')
    add('encryption','aes-2024-2',2024,2,'고정 블록과 세 가지 키 길이','DES를 대체하는 대칭키 블록 암호로, 블록은 128비트이며 키는 128·192·256비트를 사용하는 알고리즘은?',[field('알고리즘','AES','Advanced Encryption Standard')],
        'AES입니다.','movie2024','AES 설명 문항')
    add('encryption','asymmetric-2023-2',2023,2,'대칭키·비대칭키 알고리즘 나누기','보기의 알고리즘을 대칭키와 비대칭키 계열로 나누어 쓰세요. 각 답안 칸 안의 순서는 자유입니다.\n보기: DES, RSA, AES, ECC, ARIA, SEED',[
        field('① 대칭키 네 개',*[' '.join(items) for items in permutations(['DES','AES','ARIA','SEED'])]),field('② 비대칭키 두 개','RSA ECC','ECC RSA')],
        '대칭키: DES·AES·ARIA·SEED / 비대칭키: RSA·ECC입니다.','life2023','대칭키·비대칭키 알고리즘 선택 문항')

    add('attacks','apt-2024-1',2024,1,'장기간 표적 침투','특정 조직에 거점을 만든 뒤 오랜 기간 여러 수법으로 정보 수집과 외부 유출을 진행하는 위협의 약어는?',[
        field('약어','APT','Advanced Persistent Threat','Advanced Persistent Threats','지능형 지속 위협')],
        'APT입니다.','pill2024','지속적 표적 침투 문항')
    add('attacks','rootkit-2024-1',2024,1,'침입 흔적과 프로세스 은폐','침입 사실과 실행 파일·프로세스 등을 숨겨 탐지를 회피하고, 원격 접근·권한 유지 등을 돕는 악성 도구 집합은?',[field('용어','루트킷','Rootkit')],
        '루트킷입니다.','pill2024','침입 은폐 도구 집합 문항')
    add('attacks','smurf-2024-3',2024,3,'집중되는 ICMP 응답','IP·ICMP 특성을 악용해 여러 호스트의 응답이 한 대상에 집중되도록 하여 서비스 거부를 일으키는 공격은?',[
        field('공격','스머핑','스머프','Smurf','Smurfing','Smurf Attack')],
        '스머프(스머핑)입니다.','juble2024','다수 ICMP Echo Reply 공격 문항')
    add('attacks','session-2025-1',2025,1,'정상 세션을 빼앗기','다른 사용자의 접속 세션을 탈취해 접근하며, TCP 통신에서는 인증 이후의 정상 연결을 가로채는 기법은?',[
        field('공격','세션 하이재킹','세션 하이재킹 공격','Session Hijacking')],
        '세션 하이재킹입니다.','juble2025','세션 가로채기 문항')
    add('attacks','typo-2022-3',2022,3,'오타 도메인 이용','사용자가 주소의 철자를 틀릴 가능성을 노려 유명 주소와 유사한 도메인을 선점하는 행위는?',[
        field('공격','타이포스쿼팅','타이포 스쿼팅','Typosquatting','URL 하이재킹','URL Hijacking')],
        '타이포스쿼팅입니다.','min2022','TrustZone·타이포스쿼팅 문항 중 후자',part='타이포스쿼팅 소문항')
    add('attacks','ddos-2019-2',2019,2,'감염된 여러 시스템의 서비스 방해','공격자가 장악한 여러 시스템을 분산 동원하여 단일 표적의 정상 서비스를 방해하는 공격의 약어는?',[
        field('약어','DDoS','Distributed Denial of Service')],
        'DDoS입니다.','sso2019','전산영어 문항 중 DDoS 소문항',part='DDoS 소문항')

    assert all(bank.values()), 'Every concept must have checked practical-exam coverage.'
    return bank
