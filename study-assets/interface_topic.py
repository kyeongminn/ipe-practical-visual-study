"""Interface implementation verification tools (xUnit, STAF, FitNesse, NTAF, Selenium, watir) and APM monitoring tools."""
from html import escape
from security_topic import text, box, edge, svg

# name, en, group, keywords, description, cue
TOOLS=[
 ('xUnit','JUnit · CppUnit · NUnit · PyUnit','단위 테스트','단위 테스트 · 다양한 언어 · JUnit','Java의 JUnit, C++의 CppUnit, .NET의 NUnit, Python의 PyUnit처럼 언어별로 제공되는 단위 테스트 프레임워크의 총칭이다. 테스트 코드를 작성해 메서드·함수 단위의 결과를 자동으로 검증한다.','“JUnit·CppUnit·NUnit 등 다양한 언어를 지원하는 단위 테스트 프레임워크” → xUnit'),
 ('STAF','Software Testing Automation Framework','테스트 프레임워크','서비스 호출 · 컴포넌트 재사용 · 분산 환경 · 데몬','서비스 호출과 컴포넌트 재사용 등 다양한 환경을 지원하는 테스트 프레임워크다. 각 테스트 대상에 데몬을 두고 분산 환경에서 테스트를 수행한 뒤 결과를 통합해 자동화한다.','“서비스 호출, 컴포넌트 재사용, 데몬을 이용한 분산 환경 테스트” → STAF'),
 ('FitNesse','Framework for Integrated Test + Wiki','테스트 프레임워크','웹 기반 · 위키 · 테이블 형태 테스트케이스','웹 기반으로 테스트케이스의 설계·실행·결과 확인을 지원하는 테스트 프레임워크다. 위키 페이지에 표(테이블) 형태로 테스트를 작성하고 브라우저에서 실행한다.','“웹 기반으로 테스트케이스 설계·실행·결과 확인을 지원” → FitNesse'),
 ('NTAF','NHN Test Automation Framework','테스트 프레임워크','STAF + FitNesse 통합 · NHN(네이버)','NHN(네이버)의 테스트 자동화 프레임워크로, FitNesse의 웹 기반 협업 기능과 STAF의 재사용·분산 테스트 기능을 통합했다.','“STAF와 FitNesse를 통합한 NHN의 프레임워크” → NTAF'),
 ('Selenium','Selenium WebDriver','웹 UI 테스트','다양한 브라우저 · 다양한 개발 언어 · 스크립트 학습 불필요','다양한 브라우저와 개발 언어를 지원하는 웹 애플리케이션 테스트 프레임워크다. 브라우저 조작을 기록·재생하거나 코드로 작성해, 별도의 테스트 스크립트 언어를 배우지 않고도 기능 테스트를 만들 수 있다.','“다양한 브라우저와 개발 언어를 지원하는 웹 애플리케이션 테스트” → Selenium'),
 ('watir','Web Application Testing in Ruby','웹 UI 테스트','Ruby · 모든 언어 기반 웹 앱 · 브라우저 호환성','Ruby를 사용하는 웹 애플리케이션 테스트 프레임워크다. 어떤 언어로 만든 웹 애플리케이션이든 브라우저를 직접 조작해 테스트하며, 브라우저 호환성 테스트에도 쓴다.','“Ruby 기반 웹 애플리케이션 테스트 프레임워크” → watir')]

# name, vendor, license, keywords
APM=[
 ('스카우터','Scouter','LG CNS 공개 · 오픈소스','애플리케이션 서버(WAS)와 DB 모니터링 · 트랜잭션 추적'),
 ('제니퍼','Jennifer','제니퍼소프트 · 상용','애플리케이션 성능 관리 · 실시간 응답시간·사용자 수 시각화')]

APM_TYPES=[
 ('리소스 방식','Nagios · Zabbix · Cacti','CPU·메모리·디스크 같은 자원 사용량을 모니터링한다.'),
 ('엔드투엔드 방식','VisualVM · 제니퍼 · 스카우터','사용자 요청이 처리되는 트랜잭션 전체 흐름과 응답시간을 추적한다.')]

def tool_map():
    drawing='<path d="M173 94 V154" class="edge" style="stroke-dasharray:4 3"/>'
    columns=[(8,86,'단위 테스트',['xUnit']),(104,138,'테스트 프레임워크',['STAF','FitNesse','NTAF']),(252,100,'웹 UI 테스트',['Selenium','watir'])]
    for x,width,title,tools in columns:
        center=x+width/2
        drawing+=box(x,10,width,36,title,'node accent')+edge(center,47,center,60)
        for row,tool in enumerate(tools):
            drawing+=box(center-45,62+row*46,90,32,tool)
    drawing+=text(68,180,'JUnit · CppUnit · NUnit','muted')+text(290,180,'STAF + FitNesse = NTAF','muted')
    return svg(drawing,'인터페이스 구현 검증 도구: 단위 테스트의 xUnit, 테스트 프레임워크 STAF·FitNesse·NTAF, 웹 UI 테스트 Selenium·watir',196)

def apm_flow():
    drawing=box(8,30,104,46,'앱 서버 (WAS)')+text(60,96,'에이전트 설치','muted')
    drawing+=edge(113,53,133,53)+box(136,30,88,46,'APM 서버','node accent')+text(180,96,'수집 · 저장','muted')
    drawing+=edge(225,53,245,53)+box(248,30,104,46,'모니터링 화면')+text(300,96,'응답시간 · 오류','muted')
    drawing+=text(180,132,'운영 중인 인터페이스의 상태를 실시간으로 감시한다','muted')
    return svg(drawing,'APM 감시 구조: 애플리케이션 서버의 에이전트가 보낸 데이터를 APM 서버가 수집하고 화면에 응답시간과 오류를 보여준다',145)

def interface_preview():
    verify='<b>검증 도구 6</b><p>단위: xUnit<br>프레임워크: STAF · FitNesse<br>↳ NTAF = STAF + FitNesse<br>웹 UI: Selenium · watir</p>'
    monitor='<b>감시 도구 · APM</b><p>스카우터 (오픈소스)<br>제니퍼 (상용)<br><span>리소스 vs 엔드투엔드</span></p>'
    return '<div class="mini-groups"><div>'+verify+'</div><div>'+monitor+'</div></div><p class="mini-hint">STAF = 데몬·분산 / FitNesse = 웹·위키 / watir = Ruby<br>Selenium = 다양한 브라우저·언어</p>'

def build_interface_chapter():
    body='<div class="note"><b>먼저 구분</b><span><b>인터페이스 구현 검증</b>은 구현된 인터페이스가 명세대로 동작하는지 확인하는 일입니다. 테스트를 직접 실행해 결과를 확인하는 <b>검증 도구</b>(xUnit·STAF·FitNesse·NTAF·Selenium·watir)와, 운영 중인 인터페이스의 동작을 지켜보는 <b>감시 도구</b>(APM: 스카우터·제니퍼)를 나누어 기억합니다. 검증 방법으로는 단위·통합 테스트, 검증 도구 활용, 감시 도구 활용을 함께 듭니다.</span></div>'
    body+='<h3 class="subhead">1. 검증 도구 여섯 가지를 한 그림으로 보기</h3><div class="osi-overview">'+tool_map()+'</div><p class="caption">무엇을 테스트하는가로 나누면 외우기 쉽습니다. 메서드 단위는 xUnit, 분산·웹 기반 테스트 프레임워크는 STAF·FitNesse와 둘을 합친 NTAF, 브라우저를 조작하는 웹 UI 테스트는 Selenium·watir입니다.</p>'
    body+='<div class="matrix-wrap"><table><caption class="caption">도구별 분류와 출제 키워드</caption><thead><tr><th>도구</th><th>분류</th><th>키워드</th><th>한 줄 설명</th></tr></thead><tbody>'
    for name,en,group,keywords,desc,_ in TOOLS:
        body+=f'<tr><th>{name}<br><small>{en}</small></th><td>{group}</td><td><b>{keywords}</b></td><td>{desc.split(". ")[0]}.</td></tr>'
    body+='</tbody></table></div>'
    body+='<h3 class="subhead">2. 도구마다 붙는 설명</h3><div class="grid three">'
    for name,en,group,keywords,desc,cue in TOOLS:
        body+=f'<article class="concept"><div class="card-top"><h3>{name}</h3><span class="tag">{group}</span></div><div class="en">{en}</div><div class="mini-level">{keywords}</div><p>{desc}</p><div class="pattern-cue">↳ {cue}</div></article>'
    body+='</div><div class="note"><b>헷갈리는 짝</b><span><b>STAF vs FitNesse</b>: 데몬·분산 환경·재사용이면 STAF, 웹·위키·테이블이면 FitNesse. / <b>Selenium vs watir</b>: 여러 브라우저와 여러 언어를 지원하면 Selenium, Ruby 한 가지를 명시하면 watir. / <b>NTAF</b>는 새 기능이 아니라 STAF와 FitNesse의 통합입니다.</span></div>'
    body+='<h3 class="subhead">3. 감시 도구 · APM</h3><div class="grid"><article class="concept"><h3>APM 감시 구조</h3><div class="en">Application Performance Management</div>'+apm_flow()+'<p>운영 중인 인터페이스의 응답시간·트랜잭션·오류를 실시간으로 모니터링하는 도구입니다. 검증 도구가 테스트 단계에서 쓰인다면, 감시 도구는 운영 단계에서 인터페이스 동작을 지켜봅니다.</p></article><article class="concept"><h3>대표 APM 도구</h3><div class="en">Scouter · Jennifer</div><div class="matrix-wrap"><table><thead><tr><th>도구</th><th>구분</th><th>기억 포인트</th></tr></thead><tbody>'
    for ko,en,vendor,keywords in APM:
        body+=f'<tr><th>{ko}<br><small>{en}</small></th><td>{vendor}</td><td>{keywords}</td></tr>'
    body+='</tbody></table></div><p><b>APM의 두 방식</b></p>'
    for kind,examples,desc in APM_TYPES:
        body+=f'<p><b>{kind}</b> · {examples}<br>{desc}</p>'
    body+='</article></div>'
    body+='<div class="note"><b>한 줄 암기</b><span>검증 도구: <b>엑(xUnit) · 스(STAF) · 핏(FitNesse) · 엔(NTAF) · 셀(Selenium) · 와(watir)</b>. 감시 도구: <b>스카우터(오픈소스) · 제니퍼(상용)</b>. 키워드 한 개씩: 단위 · 데몬 · 위키 · 통합 · 브라우저 · Ruby.</span></div>'
    body+='<div class="source-row"><a class="source" href="https://staf.sourceforge.net/" target="_blank" rel="noopener noreferrer">↗ STAF · SourceForge</a><a class="source" href="https://fitnesse.org/" target="_blank" rel="noopener noreferrer">↗ FitNesse</a><a class="source" href="https://www.selenium.dev/documentation/" target="_blank" rel="noopener noreferrer">↗ Selenium · Documentation</a><a class="source" href="https://watir.com/" target="_blank" rel="noopener noreferrer">↗ Watir</a><a class="source" href="https://github.com/scouter-project/scouter" target="_blank" rel="noopener noreferrer">↗ Scouter · GitHub</a></div>'
    return '<section id="interface-tools" class="chapter"><header class="chapter-head"><span class="chapter-no">19</span><div><p class="eyebrow">CONCEPT MAP / 19</p><h2>인터페이스 구현 검증 도구</h2><p>테스트를 실행하는 검증 도구 여섯 가지와 운영을 지켜보는 감시 도구를 키워드로 구분합니다.</p></div></header>'+body+'</section>'
