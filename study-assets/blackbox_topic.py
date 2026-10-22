"""Black-box techniques embedded in the existing white-box study page."""
from security_topic import box, text, edge, svg
from drm_topics import card, note, flow

def equivalence_picture():
    drawing=''
    for x,label,value in [(7,'18세 미만','대표 10'),(128,'18~60세','대표 35'),(249,'60세 초과','대표 70')]:
        drawing+=f'<rect x="{x}" y="24" width="104" height="67" rx="9" class="node {"accent" if x==128 else ""}"/>'
        drawing+=text(x+52,49,label)+text(x+52,73,value,'muted')
    drawing+=text(180,127,'같게 처리할 그룹 → 그룹별 대표값','muted')
    return svg(drawing,'허용 나이 18부터 60. 미만 그룹 10, 유효 그룹 35, 초과 그룹 70을 대표값으로 선택',149)

def boundary_picture():
    drawing='<rect x="75" y="35" width="210" height="46" rx="8" class="zone"/><path d="M15 58 H345" class="edge"/>'
    for x,value in [(25,17),(75,18),(125,19),(235,59),(285,60),(335,61)]:
        drawing+=f'<circle cx="{x}" cy="58" r="5" class="node {"accent" if value in (18,60) else ""}"/>'+text(x,106,str(value),'muted')
    drawing+=text(180,143,'18·60의 바로 앞 / 경계 / 바로 뒤','muted')
    return svg(drawing,'정수 나이 18부터 60의 3값 경계 예시: 17 18 19 59 60 61. 숫자 간격은 축약.',163)

def cause_picture():
    drawing=box(7,17,111,43,'회원')+box(7,98,111,43,'5만원 이상')
    drawing+=edge(120,39,160,73)+edge(120,119,160,86)+box(163,57,63,46,'AND','node accent')
    drawing+=edge(228,80,248,80)+box(251,57,103,46,'무료배송')
    drawing+=text(180,182,'원인 두 개의 논리 관계 → 결과','muted')
    return svg(drawing,'회원과 주문금액 5만원 이상이 모두 참이면 무료배송인 원인 효과 관계',202)

def comparison_picture():
    drawing=box(7,67,98,43,'같은 입력')
    drawing+=edge(107,80,147,37)+edge(107,96,147,132)
    drawing+=box(150,15,111,43,'버전 A')+box(150,111,111,43,'버전 B')
    drawing+=edge(263,37,290,37)+edge(263,132,290,132)+text(324,42,'결과 A')+text(324,137,'결과 B')
    drawing+='<path d="M324 57 V110" class="edge"/>'+text(324,89,'비교','muted')
    drawing+=text(180,190,'동일 명세 · 동일 입력에서 결과 비교','muted')
    return svg(drawing,'같은 명세를 구현한 두 버전에 동일한 입력을 넣어 결과를 비교한다',211)

def decision_picture():
    drawing=''
    values=[['조건 / 규칙','1','2','3','4'],['회원','T','T','F','F'],['5만원 이상','T','F','T','F'],['무료배송','O','X','X','X']]
    for row,entries in enumerate(values):
        for col,value in enumerate(entries):
            x=7 if col==0 else 130+(col-1)*56
            width=122 if col==0 else 56
            drawing+=f'<rect x="{x}" y="{12+row*34}" width="{width}" height="34" class="node {"accent" if row==3 else ""}"/>'
            drawing+=text(x+width/2,34+row*34,value,'muted')
    drawing+=text(180,179,'조건 조합을 열로 · 결과를 행으로','muted')
    return svg(drawing,'회원 여부와 5만원 이상 여부의 네 조합을 나타낸 결정 테이블. TT일 때만 무료배송.',199)

def state_picture():
    drawing=box(7,25,99,43,'결제 전')+edge(108,47,131,47)+box(134,25,99,43,'결제 완료','node accent')+edge(235,47,251,47)+box(254,25,99,43,'배송 중')
    drawing+=text(120,18,'결제','muted')+text(244,18,'발송','muted')
    drawing+=edge(56,70,56,125)+text(88,104,'취소','muted')+box(7,130,99,43,'취소 완료')
    drawing+=text(233,147,'현재 상태 + 이벤트','muted')+text(233,173,'→ 다음 상태','muted')
    return svg(drawing,'결제 전에서 결제 이벤트로 결제 완료, 발송 이벤트로 배송 중으로 이동하고 결제 전 취소는 취소 완료로 이동한다',198)

def blackbox_content():
    body='<h3 class="subhead" id="blackbox-techniques" tabindex="-1">H. 블랙박스 테스트 기법</h3>'
    body+=note('설계 근거','<b>명세·요구사항의 입력과 기대 출력</b>을 기준으로 사례를 설계한다. 내부 코드를 몰라도 설계할 수 있으며, 정상 입력뿐 아니라 잘못된 입력의 기대 오류 처리도 포함한다.')
    body+='<div class="grid">'
    body+=card('동치 분할 검사 · 동등 분할','Equivalence Partitioning · EP',equivalence_picture(),'같은 방식으로 처리될 것으로 예상되는 입력을 <b>동치 그룹</b>으로 나누고 각 그룹에서 대표값을 선택한다. 유효 그룹과 무효 그룹을 모두 살핀다.','나이 18~60 허용 → 10 / 35 / 70으로 그룹 대표')
    body+=card('경계값 분석','Boundary Value Analysis · BVA',boundary_picture(),'순서가 있는 입력 범위의 <b>경계와 그 이웃</b>에 집중한다. 예를 들어 정수 나이 18~60은 17·18·19와 59·60·61을 살핀다.','동치 분할 = 그룹 대표 / 경계값 = 경계 주변')
    body+=card('원인–효과 그래프 검사','Cause–Effect Graphing',cause_picture(),'입력 조건인 <b>원인</b>과 출력인 <b>효과</b>의 논리 관계를 그래프로 표현하고 테스트 조합을 선정한다. 필요하면 결정 테이블로 정리한다.','원인·조건 → AND / OR / NOT → 효과·출력')
    body+=card('오류 예측 검사','Error Guessing',flow('과거 결함 · 경험','누락 · 중복 입력'),'경험과 과거 결함을 바탕으로 <b>오류가 날 만한 사례</b>를 예상한다. 필수값 누락, 중복 클릭, 특수문자 등에서 명세에 맞는 처리를 확인한다.','과거 오류·경험으로 취약 사례 예상')
    body+=card('비교 검사','Comparison Testing',comparison_picture(),'<b>같은 명세를 구현한 여러 버전</b>에 동일한 테스트 자료를 주고 결과를 비교한다. 차이가 나면 원인을 조사하며, 결과가 같아도 모두 옳다는 증명은 아니다.','여러 버전 + 동일 입력 + 출력 비교')
    body+='</div><p class="caption">위 다섯 기법은 정보처리기사 수험서에서 블랙박스와 함께 다루는 대표 항목이다. <b>ISTQB CTFL에서는 오류 예측을 경험 기반 기법으로 별도 분류</b>한다. 문제에서 사용하는 분류 문맥을 확인하자.</p>'
    body+='<h3 class="subhead">I. 함께 알아둘 명세 기반 기법</h3><div class="grid">'
    body+=card('결정 테이블 테스트','Decision Table Testing',decision_picture(),'여러 조건의 <b>조합과 그에 따른 결과</b>를 표로 정리한다. 이 예시는 회원 AND 5만원 이상일 때만 무료배송이다.','조건 조합 → 규칙 열 → 기대 결과')
    body+=card('상태 전이 테스트','State Transition Testing',state_picture(),'<b>현재 상태와 이벤트</b>에 따른 다음 상태·동작을 검사한다. 허용된 전이와 명세에서 금지한 전이를 확인하며, 이력·순서가 결과에 영향을 주는 기능에 적합하다.','같은 입력이어도 현재 상태가 다르면 결과가 다름')
    body+='</div>'
    body+='<h3 class="subhead">J. 화이트박스와 블랙박스 · 무엇을 보고 고를까?</h3><div class="matrix-wrap"><table><thead><tr><th>구분</th><th>화이트박스</th><th>블랙박스</th></tr></thead><tbody><tr><td>설계 근거</td><td>내부 구조·코드·제어/데이터 흐름</td><td>명세·요구사항·입출력 동작</td></tr><tr><td>대표 질문</td><td>어느 문장·분기·조건을 실행했나?</td><td>이 입력·상태에서 기대 결과가 맞나?</td></tr><tr><td>대표 기법</td><td>기초 경로·조건·루프·데이터 흐름</td><td>동치 분할·경계값·원인–효과·결정 테이블·상태 전이 등</td></tr><tr><td>확인 기준의 예</td><td>문장·분기·조건 커버리지</td><td>동치 그룹·경계·규칙·전이의 검사 여부</td></tr></tbody></table></div>'
    body+=note('한 줄 암기','<b>구조·코드를 보고 설계 → 화이트박스 / 명세·기능을 보고 설계 → 블랙박스.</b> 같은 입력을 사용할 수도 있고 두 관점은 서로 보완한다. 블랙박스의 “결정 테이블”과 화이트박스의 “결정 커버리지”는 다른 개념이다.')
    body+='<div class="source-row"><a class="source" href="https://www.sinagong.co.kr/pds/001001002/books/1074/download-data/297#page=48" target="_blank" rel="noopener noreferrer">↗ 시나공 · 블랙박스 대표 기법</a><a class="source" href="https://astqb.org/4-2-black-box-test-techniques/" target="_blank" rel="noopener noreferrer">↗ ASTQB · 명세 기반 4가지 기법</a><a class="source" href="https://astqb.org/assets/documents/ISTQB_CTFL_Syllabus_v4.0.1.pdf#page=43" target="_blank" rel="noopener noreferrer">↗ ISTQB CTFL · 경험 기반 오류 예측</a></div>'
    return body

def blackbox_questions(question,field):
    return [
      question('black-ep-bva','그룹 대표와 경계 주변','허용 나이는 정수 18~60세입니다. ① 18세 미만·18~60·60세 초과에서 10·35·70을 선택, ② 17·18·19·59·60·61을 선택했습니다. 각각의 기법 이름을 쓰세요.',[
        field('① 그룹 대표','동치 분할 검사','동치 분할','동등 분할','동등 분할 검사','동등 분할 기법','Equivalence Partitioning','EP'),
        field('② 경계 주변','경계값 분석','경계 값 분석','경계값 분석 기법','Boundary Value Analysis','BVA')],
        '동치 분할 / 경계값 분석입니다. 그룹마다 대표를 선택하는지, 경계와 바로 옆 값을 선택하는지 구분하세요.'),
      question('black-cause','입력 조건에서 출력까지','회원 여부와 주문금액 조건을 AND로 연결하여 무료배송 결과에 미치는 논리 관계를 그래프로 표현합니다. 어떤 기법인가요?',[
        field('검사 기법','원인 효과 그래프 검사','원인 효과 그래프','원인-효과 그래프 검사','원인-효과 그래프','원인–효과 그래프 검사','Cause Effect Graphing','Cause Effect Graphing Testing','Cause and Effect Graphing')],
        '원인–효과 그래프 검사입니다. 원인은 입력 조건, 효과는 출력 결과이며 그 사이의 논리 관계를 분석합니다.'),
      question('black-comparison','여러 버전에 같은 자료 입력','동일 명세를 구현한 여러 프로그램 버전에 똑같은 테스트 자료를 제공하고 출력 결과를 비교합니다. 기법 이름을 쓰세요.',[
        field('검사 기법','비교 검사','비교 테스트','Comparison Testing','Comparison Test')],
        '비교 검사입니다. 결과의 차이는 조사 대상이며, 모든 버전의 결과가 같아도 같은 결함을 공유할 수 있습니다.'),
      question('black-error-guessing','경험과 과거 결함을 활용하기','과거에 중복 클릭으로 문제가 발생한 경험을 바탕으로 중복 요청과 필수값 누락 사례를 예상합니다. ① 기법 이름, ② ISTQB CTFL에서의 분류를 쓰세요.',[
        field('① 기법','오류 예측 검사','오류 예측','오류 추정','Error Guessing'),field('② ISTQB 분류','경험 기반','경험 기반 테스트','경험 기반 기법','경험 기반 테스트 기법','Experience based','Experience based testing')],
        '오류 예측 / 경험 기반입니다. 정보처리기사 수험서에서는 블랙박스 기법 목록에 함께 넣기도 하지만, ISTQB CTFL은 경험 기반으로 분리합니다.'),
      question('black-decision-table','조건 조합과 결과를 표로','회원 여부와 5만원 이상 여부의 T/F 조합 네 개를 열로 놓고 무료배송 O/X를 표로 정리하여 테스트합니다. 어떤 기법인가요?',[
        field('검사 기법','결정 테이블 테스트','결정 테이블','의사결정 테이블','의사결정 테이블 테스트','Decision Table','Decision Table Testing')],
        '결정 테이블 테스트입니다. 조건 조합에 대한 업무 규칙을 검사하며, 코드의 참·거짓 분기 실행률인 결정 커버리지와 구분합니다.'),
      question('black-state-transition','현재 상태와 이벤트 검사','주문이 결제 전인지 결제 완료인지에 따라 취소 이벤트의 허용 여부와 다음 상태를 확인합니다. 어떤 기법인가요?',[
        field('검사 기법','상태 전이 테스트','상태 전이','상태 전이 검사','상태 전이 테스팅','State Transition','State Transition Testing')],
        '상태 전이 테스트입니다. 현재 상태와 이벤트의 조합, 전이 순서 및 허용·금지 전이를 명세에 맞게 검사합니다.')]
