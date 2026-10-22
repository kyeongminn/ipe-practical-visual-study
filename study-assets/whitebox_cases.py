"""Edge/corner examples that complement, rather than redefine, white-box testing."""
from html import escape
from security_topic import text, svg
from drm_topics import card, note

EXAMPLE='''def classify(n, r):
    # n: 항목 수 0~100 / r: 재시도 한도 0~3
    if not (0 <= n <= 100 and 0 <= r <= 3):
        return "INVALID"
    if n == 0 and r == 0:
        return "EMPTY_NO_RETRY"
    if n == 0:
        return "EMPTY"
    if r == 0:
        return "NO_RETRY"
    return "PROCESS"'''

def edge_diagram():
    drawing='<rect x="75" y="43" width="210" height="54" rx="9" class="zone"/>'
    drawing+='<path d="M15 70 H345" class="edge"/>'
    for x,value in [(25,-1),(75,0),(125,1),(235,99),(285,100),(335,101)]:
        drawing+=f'<circle cx="{x}" cy="70" r="5" class="node {"accent" if value in (0,100) else ""}"/>'
        drawing+=text(x,120,str(value),'muted')
    drawing+=text(180,23,'유효 범위 · 0 ≤ n ≤ 100')
    drawing+=text(75,157,'최솟값 0','muted')+text(285,157,'최댓값 100','muted')
    drawing+=text(180,195,'경계 자체 + 바로 안쪽·바깥쪽 확인','muted')
    return svg(drawing,'n의 유효 범위 0부터 100과 경계 이웃 -1 0 1 99 100 101. 숫자 사이 간격은 축약.',218)

def corner_diagram():
    drawing='<rect x="85" y="49" width="230" height="162" rx="0" class="zone"/>'
    drawing+='<path d="M85 130 H315 M200 49 V211" class="edge" stroke-dasharray="4 5"/>'
    for row,n in enumerate([100,20,0]):
        y=49+row*81
        drawing+=text(52,y+5,str(n),'muted')
        for col,r in enumerate([0,1,3]):
            x=85+col*115
            kind='C' if row!=1 and col!=1 else 'N' if row==col==1 else 'E'
            drawing+=f'<circle cx="{x}" cy="{y}" r="16" class="node {"accent" if kind=="C" else ""}"><title>n={n}, r={r}: {kind}</title></circle>'+text(x,y+5,kind)
    for x,label in [(85,'0'),(200,'1'),(315,'3')]:drawing+=text(x,245,label,'muted')
    drawing+=text(50,18,'n · 항목 수','muted')+text(200,277,'r · 재시도 한도','muted')
    drawing+=text(180,312,'C 코너 · E 한 축의 경계 · N 일반','muted')
    return svg(drawing,'항목 수와 재시도 한도의 2차원 범위. 모서리는 두 경계가 겹치는 코너, 변 중간은 한 축의 경계, 가운데는 일반 사례.',334)

def whitebox_cases_content():
    body='<h3 class="subhead" id="edge-corner-cases">F. 엣지 케이스 / 코너 케이스</h3>'
    body+=note('먼저 분류','엣지·코너 케이스는 <b>테스트할 상황</b>을 부르는 말이다. 화이트박스의 독립된 공식 기법 목록에 추가하는 항목은 아니다. <b>명세의 경계값 분석</b>으로도, <b>코드의 분기·조건·루프 분석</b>으로도 이런 사례를 찾을 수 있다.')
    body+='<div class="grid">'
    body+=card('엣지 케이스','Edge case · 경계·극단·드문 상황',edge_diagram(),'보통 입력과 달리 <b>경계나 극단 등 특수한 조건</b>에서 동작을 확인하는 사례. 빈 목록, 원소 1개, 최대 길이 등이 예다. 여기서는 한 입력 축의 경계를 움직이고 다른 축은 보통 값으로 둔다.','한 축 예시: 항목 수 n=0, 재시도 한도 r=1')
    body+=card('코너 케이스','Corner case · 여러 경계 조건의 결합',corner_diagram(),'<b>둘 이상의 경계 조건이 동시에 겹치는 상황</b>을 뜻하는 구분으로 설명한다. 각 조건을 따로 시험했을 때와 결합했을 때의 동작이 달라질 수 있다.','두 축 예시: 항목 수 n=0 + 재시도 한도 r=0')
    body+='</div><p class="caption">용어 사용 범위는 문맥에 따라 다르다. 이 예제에서는 “한 축의 경계”와 “여러 경계의 결합”을 구분한다. 경계 밖 입력은 명세에서 정한 오류 처리를 별도로 확인한다. 수직선의 간격과 격자의 눈금은 축약했다.</p>'
    body+='<div class="matrix-wrap"><table><thead><tr><th>사례</th><th>입력 (n, r)</th><th>확인할 것</th></tr></thead><tbody><tr><td>일반</td><td>(20, 1)</td><td>보통 값에서 정상 처리</td></tr><tr><td>엣지 · n의 최솟값</td><td>(0, 1)</td><td>빈 목록 처리 · 반복문 0회</td></tr><tr><td>엣지 · r의 최솟값</td><td>(20, 0)</td><td>재시도를 하지 않는 조건</td></tr><tr><td>코너 · 두 최솟값</td><td>(0, 0)</td><td>두 조건이 함께 참인 전용 경로</td></tr><tr><td>코너 · 두 최댓값</td><td>(100, 3)</td><td>최대 항목 수와 최대 재시도 한도의 결합</td></tr><tr><td>범위 밖 · 오류 처리</td><td>(101, 1) · (20, −1)</td><td>명세에 정한 거부·오류 응답</td></tr></tbody></table></div>'
    body+='<h3 class="subhead">G. 화이트박스와 연결 · 숨어 있는 결합 분기 찾기</h3><div class="grid"><div class="code-panel"><pre><code>'+escape(EXAMPLE)+'</code></pre></div><article class="concept"><h3>각 경계만 검사하면 놓칠 수 있다</h3><div class="pattern-cue">(0, 1) → EMPTY</div><div class="pattern-cue">(20, 0) → NO_RETRY</div><p>두 엣지 테스트에서 개별 조건을 각각 참으로 만들었어도 <b>n==0 AND r==0</b>의 참 분기는 아직 실행하지 않았다.</p><div class="mini-level">(0, 0) → EMPTY_NO_RETRY</div><p>코너 입력을 추가하여 결합 조건이 참인 경로를 실행한다. 이것만으로 전체 분기·조건 커버리지가 100%가 된다고 단정할 수는 없다.</p><p class="caption">반복문이 있다면 n=0·1·최대 부근도 함께 확인한다. 코드 예제는 분기 설명에 집중한 축약 예시이며 실제 반복 처리는 생략했다.</p></article></div>'
    body+=note('같은 입력, 다른 설계 근거','<b>명세의 0~100 범위로 -1·0·1·99·100·101을 고름 → 경계값 분석(블랙박스).</b><br><b>코드의 n==0 분기나 반복 종료 조건을 보고 입력을 고름 → 화이트박스 관점.</b> 입력값이 같아도 테스트를 설계한 근거가 다를 수 있다.')
    body+='<div class="source-row"><a class="source" href="https://swc-uiuc.github.io/python-testing/06-edges/index.html" target="_blank" rel="noopener noreferrer">↗ Software Carpentry · Edge and Corner Cases</a><a class="source" href="https://astqb.org/4-2-black-box-test-techniques/" target="_blank" rel="noopener noreferrer">↗ ASTQB · 경계값 분석의 분류</a></div>'
    return body

def whitebox_cases_questions(question,field):
    return [
      question('white-edge-corner','하나의 경계와 경계의 결합','항목 수 n은 0~100, 재시도 한도 r은 0~3입니다. 일반 입력은 (20, 1)입니다. 이 페이지의 구분에 따라 ① (0, 1), ② (0, 0)을 각각 엣지 케이스 또는 코너 케이스로 분류하세요.',[
        field('① (0, 1)','엣지 케이스','에지 케이스','엣지','에지','Edge case','Edge'),field('② (0, 0)','코너 케이스','코너','Corner case','Corner')],
        '엣지 케이스 / 코너 케이스입니다. (0, 1)은 n만 최솟값이고, (0, 0)은 n과 r 두 경계가 겹칩니다. 두 용어는 화이트박스 전용 기법이 아닙니다.'),
      question('white-corner-branch','놓친 결합 분기 실행하기','아래 코드에서 (0, 1)과 (20, 0)만 검사했습니다. EMPTY_NO_RETRY를 반환하는 경로를 실행하려면 어떤 (n, r)을 추가해야 하나요?',[
        field('추가 입력 (n, r)','(0, 0)','0 0','n=0 r=0','n=0, r=0')],
        '(0, 0)입니다. 각 조건을 따로 참으로 만들었다고 두 조건이 동시에 참인 경로까지 검사한 것은 아닙니다.',visual='<div class="code-panel"><pre><code>'+escape(EXAMPLE)+'</code></pre></div>'),
      question('white-edge-technique','엣지·코너는 화이트박스 전용인가?','엣지·코너 케이스는 화이트박스에서만 사용할 수 있는 독립된 공식 테스트 기법이다. 맞으면 O, 틀리면 X로 답하세요.',[
        field('O / X','X','아니오','아니요','No')],
        'X입니다. 테스트 상황을 부르는 말입니다. 명세 기반으로 경계를 고르면 경계값 분석, 코드의 분기·조건·루프를 근거로 설계하면 화이트박스 관점으로 연결할 수 있습니다.'),
      question('white-boundary-basis','같은 경계 입력의 설계 근거','코드를 보지 않고 “항목 수는 0~100”이라는 명세에 따라 -1·0·1·99·100·101을 시험합니다. ① 기법 이름, ② 블랙박스/화이트박스 중 분류를 쓰세요.',[
        field('① 기법','경계값 분석','경계 값 분석','경계값 분석 기법','경계값 테스트','Boundary Value Analysis','BVA'),field('② 분류','블랙박스','블랙박스 테스트','블랙 박스','Black-box','Black-box testing')],
        '경계값 분석 / 블랙박스입니다. 코드 내부 구조를 기준으로 설계한 것이 아닙니다. 범위 밖 -1·101은 오류 처리가 명세대로 동작하는지 확인합니다.')]
