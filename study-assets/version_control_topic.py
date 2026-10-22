"""Exam-oriented version-control categories and repository diagrams."""
from security_topic import box, text, edge, svg
from drm_topics import card, chapter, note

KEY='version-control'

def repository_map(kind):
    if kind=='shared':
        drawing=box(74,14,212,48,'공유 폴더 · 버전 자료','node accent')
        drawing+=edge(100,63,71,120)+edge(82,120,111,63)+edge(250,63,279,120)+edge(290,120,261,63)
        drawing+=box(9,125,135,46,'개발자 A')+box(216,125,135,46,'개발자 B')
        drawing+=text(180,104,'파일 접근 · 복사','muted')+text(180,207,'약속된 폴더로 파일을 모아 관리','muted')
        label='공유 폴더 방식: 개발자가 공통 폴더의 버전 자료를 이용한다'
    elif kind=='central':
        drawing=box(74,14,212,48,'서버 · 중앙 저장소','node accent')
        drawing+=edge(99,64,72,120)+edge(83,120,110,64)+edge(251,64,278,120)+edge(289,120,262,64)
        drawing+=box(9,125,135,46,'A · 작업본')+box(216,125,135,46,'B · 작업본')
        drawing+=text(180,104,'받기 / 서버에 커밋','muted')+text(180,207,'버전 이력의 중심 = 중앙 서버','muted')
        label='클라이언트 서버 방식: 중앙 저장소에 이력을 보관하고 개발자에게 작업본을 제공한다'
    else:
        drawing=box(74,14,212,48,'협업용 원격 저장소','node accent')
        drawing+=edge(99,64,72,112)+edge(83,112,110,64)+edge(251,64,278,112)+edge(289,112,262,64)+text(180,99,'push / pull','muted')
        drawing+=box(7,118,148,43,'A · 로컬 저장소')+box(205,118,148,43,'B · 로컬 저장소')
        drawing+=text(81,185,'이력 + 작업본','muted')+text(279,185,'이력 + 작업본','muted')
        drawing+=text(180,215,'각자 로컬에서 커밋 → 서로 동기화','muted')
        label='분산 저장소 방식: 원격 저장소와 개발자별 로컬 저장소가 있고 각자 로컬에서 버전을 기록한다'
    return svg(drawing,label,237)

def commit_flow(distributed):
    if distributed:
        drawing=box(6,18,132,44,'작업 내용')+edge(140,40,215,40)+box(219,18,135,44,'로컬 저장소','node accent')
        drawing+=text(180,25,'commit','muted')+edge(286,64,286,116)
        drawing+=text(234,97,'push','muted')+box(219,120,135,44,'원격 저장소')
        drawing+=text(100,143,'공유는 별도 단계','muted')
        return svg(drawing,'Git은 commit으로 로컬에 기록하고 push로 원격에 전송한다',185)
    drawing=box(6,18,132,44,'작업 내용')+edge(140,40,215,40)+box(219,18,135,44,'서버 저장소','node accent')
    drawing+=text(180,25,'commit','muted')+text(180,123,'서버에 연결하여 변경 이력 반영','muted')
    return svg(drawing,'SVN은 commit으로 서버 저장소에 변경을 반영한다',185)

def build_version_control_chapter():
    body=note('버전 관리란?','파일의 <b>변경 이력</b>을 기록하여 이전 버전 확인·비교·복구와 협업을 돕는 것. 세 방식은 <b>버전 자료와 이력을 두는 위치</b>로 구분한다.')
    body+='<h3 class="subhead">1. 세 방식 · 저장소 위치를 그림으로 기억하기</h3><div class="grid three">'
    body+=card('공유 폴더 방식','RCS · SCCS',repository_map('shared'),'로컬 컴퓨터의 <b>공유 폴더</b>에 버전 자료를 모아 관리한다. 개발자는 약속된 폴더를 이용해 파일을 공유한다.','폴더를 공유 → RCS · SCCS')
    body+=card('클라이언트/서버 방식','CVS · SVN',repository_map('central'),'<b>중앙 서버 저장소</b>에서 버전 이력을 관리한다. 개발자는 작업본을 받아 수정한 뒤 서버에 커밋한다.','서버가 이력의 중심 → CVS · SVN')
    body+=card('분산 저장소 방식','Git · BitKeeper',repository_map('distributed'),'<b>개발자별 로컬 저장소</b>에서 버전을 기록한다. 원격 저장소와 변경 이력을 주고받아 협업한다.','로컬에도 저장소 → Git · BitKeeper')
    body+='</div><p class="caption">수험서의 세 가지 분류를 따른 개념도다. RCS·SCCS는 파일 단위의 로컬 버전 관리 도구로도 설명된다. 분산 그림의 각 개발자 영역에는 작업본과 로컬 이력을 함께 표시했다.</p>'
    body+='<h3 class="subhead">2. 여섯 도구 · 이름과 짝 연결</h3><div class="matrix-wrap"><table><thead><tr><th>방식</th><th>도구</th><th>기억할 특징</th></tr></thead><tbody><tr><td rowspan="2">공유 폴더</td><td><b>RCS</b><br>Revision Control System</td><td>파일의 변경 이력 관리</td></tr><tr><td><b>SCCS</b><br>Source Code Control System</td><td>소스 코드의 버전 관리</td></tr><tr><td rowspan="2">클라이언트/서버</td><td><b>CVS</b><br>Concurrent Versions System</td><td>중앙 저장소를 사용하는 협업</td></tr><tr><td><b>SVN</b><br>Apache Subversion</td><td>CVS를 개선한 중앙 집중형 도구</td></tr><tr><td rowspan="2">분산 저장소</td><td><b>Git</b></td><td>로컬 커밋 후 원격 저장소와 동기화</td></tr><tr><td><b>BitKeeper</b></td><td>개발자별 저장소를 이용하는 분산형 도구</td></tr></tbody></table></div>'
    body+='<h3 class="subhead">3. 커밋은 어디에 기록될까?</h3><div class="grid"><article class="concept"><h3>SVN · 서버에 기록</h3>'+commit_flow(False)+'<p>commit은 <b>중앙 서버 저장소</b>에 변경을 반영한다. 서버 연결이 끊겨도 작업본 편집은 가능하지만 서버에 커밋할 수 없다.</p></article><article class="concept"><h3>Git · 로컬 기록 후 공유</h3>'+commit_flow(True)+'<p>commit은 <b>로컬 저장소</b>에 기록한다. push는 로컬 커밋을 원격으로 보낸다. 원격 연결 없이도 로컬 커밋과 이력 조회가 가능하다.</p></article></div>'
    body+=note('헷갈림 방지','<b>작업본 ≠ 이력 저장소.</b> 파일이 내 PC에 있다고 모두 분산형은 아니다. Git의 <b>commit ≠ push</b>이며, GitHub는 Git 저장소를 호스팅하는 서비스다. 분산형도 원격 서버를 사용할 수 있고 병합 충돌이 발생할 수 있다.')
    body+='<h3 class="subhead">4. 시험 직전 · 세 쌍으로 외우기</h3><div class="ribbon"><div><h3>공유 폴더</h3><span class="big">RCS · SCCS</span>폴더에 버전 자료</div><div><h3>클라이언트/서버</h3><span class="big">CVS · SVN</span>중앙 서버에 이력</div><div><h3>분산 저장소</h3><span class="big">Git · BitKeeper</span>각자 로컬에도 이력</div></div>'
    return chapter(KEY,'12','버전관리 도구','공유 폴더 · 클라이언트/서버 · 분산 저장소와 여섯 도구',body,[('시나공 · 버전 관리 방식 분류','https://www.sinagong.co.kr/pds/001001001/books/1041/download-data/270#page=36'),('Git 공식 문서 · 버전 관리의 종류','https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control.html'),('Git 공식 문서 · 원격 저장소','https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes')])

def version_control_questions(question,field):
    return {KEY:[
      question('vcs-tool-pairs','방식별 도구 두 개씩','각 방식의 대표 도구 두 개를 각각 쓰세요. 같은 방식 안에서는 순서가 바뀌어도 됩니다.',[
        field('① 공유 폴더','RCS SCCS','SCCS RCS','RCS, SCCS','SCCS, RCS','RCS/SCCS','SCCS/RCS'),
        field('② 클라이언트/서버','CVS SVN','SVN CVS','CVS, SVN','SVN, CVS','CVS/SVN','SVN/CVS'),
        field('③ 분산 저장소','Git BitKeeper','BitKeeper Git','Git, BitKeeper','BitKeeper, Git','Git/BitKeeper','BitKeeper/Git')],
        '공유 폴더는 RCS·SCCS, 클라이언트/서버는 CVS·SVN, 분산 저장소는 Git·BitKeeper입니다.'),
      question('vcs-storage','저장 위치로 분류하기','① 로컬 컴퓨터의 공유 폴더에 버전 자료를 모음, ② 중앙 서버가 이력을 관리하고 개발자는 작업본을 받음, ③ 개발자마다 로컬 저장소에서 버전을 기록함. 각 버전 관리 방식을 쓰세요.',[
        field('① 방식','공유 폴더','공유 폴더 방식'),field('② 방식','클라이언트/서버','클라이언트/서버 방식','클라이언트 서버','클라이언트 서버 방식','중앙 집중형','중앙 집중 방식'),field('③ 방식','분산 저장소','분산 저장소 방식','분산형','분산 방식')],
        '공유 폴더 / 클라이언트·서버 / 분산 저장소입니다. 작업본이 내 PC에 있는지보다 버전 이력을 어디에서 관리하는지를 보세요.'),
      question('vcs-svn-name','CVS를 개선한 도구','CVS를 개선한 중앙 집중형 버전 관리 도구로, 약어가 SVN인 도구의 이름을 쓰세요.',[
        field('도구 이름','Subversion','Apache Subversion','서브버전','서브 버전','아파치 서브버전','SVN')],
        'Subversion(SVN)입니다. SVN은 클라이언트/서버 방식이며 Git·BitKeeper와 분류가 다릅니다.'),
      question('vcs-commit-push','Git의 기록과 전송','Git에서 ① 변경 사항을 로컬 저장소에 기록하는 명령, ② 로컬 커밋을 원격 저장소로 보내는 명령을 쓰세요.',[
        field('① 로컬 기록','commit','git commit','커밋'),field('② 원격 전송','push','git push','푸시','푸쉬')],
        'commit / push입니다. 로컬 커밋을 했다고 원격 저장소에 자동으로 전송되지는 않습니다.'),
      question('vcs-offline','원격 서버가 연결되지 않을 때','Git의 일반적인 로컬 저장소에 필요한 이력이 이미 있습니다. 원격 서버에 연결할 수 없을 때 가능한 작업은? ① 로컬 커밋 및 이력 조회 ② 연결할 수 없는 원격 서버로 push. 가능한 번호 하나를 쓰세요.',[
        field('가능한 작업 번호','1','①','1번')],
        '①입니다. 로컬 저장소에서 커밋·조회할 수 있습니다. 원격 전송은 연결이 복구되어야 합니다. SVN도 작업본 편집 자체는 가능하지만 서버 커밋에는 서버 연결이 필요합니다.')]
    }
