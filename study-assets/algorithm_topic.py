"""Sorting and searching algorithms: average time complexity with best/worst, space and stability."""
from html import escape
import math
from security_topic import text, box, edge, svg

# name, en, best, average, worst, extra space, stability, group, cue
SORTS=[
 ('버블 정렬','Bubble sort','O(n²)','O(n²)','O(n²)','O(1)','안정','quadratic','인접한 두 값을 비교·교환하며 큰 값을 끝으로 보낸다. 교환이 없으면 멈추는 개선형은 최선 O(n).'),
 ('선택 정렬','Selection sort','O(n²)','O(n²)','O(n²)','O(1)','불안정','quadratic','남은 구간에서 최솟값을 골라 앞과 교환한다. 입력이 이미 정렬되어 있어도 비교 횟수는 같다.'),
 ('삽입 정렬','Insertion sort','O(n)','O(n²)','O(n²)','O(1)','안정','quadratic','앞쪽의 정렬된 구간에 새 값을 끼워 넣는다. 거의 정렬된 입력에서는 O(n)에 가깝다.'),
 ('셸 정렬','Shell sort','간격 수열에 따름','O(n^1.5)','O(n²)','O(1)','불안정','quadratic','간격(gap)을 두고 삽입 정렬을 반복하며 간격을 줄인다. 수험서는 평균 O(n^1.5)로 표기한다.'),
 ('퀵 정렬','Quick sort','O(n log n)','O(n log n)','O(n²)','O(log n)','불안정','nlogn','피벗을 기준으로 작은 쪽·큰 쪽으로 분할한다. 평균은 가장 빠른 편이지만 피벗이 치우치면 최악 O(n²).'),
 ('합병(병합) 정렬','Merge sort','O(n log n)','O(n log n)','O(n log n)','O(n)','안정','nlogn','반으로 나눈 뒤 정렬된 두 구간을 병합한다. 항상 O(n log n)이지만 병합용 추가 배열 O(n)이 필요하다.'),
 ('힙 정렬','Heap sort','O(n log n)','O(n log n)','O(n log n)','O(1)','불안정','nlogn','힙을 만들고 루트(최댓값)를 꺼내 재구성하기를 반복한다. 추가 공간 없이 항상 O(n log n).'),
 ('기수 정렬','Radix sort','O(dn)','O(dn)','O(dn)','O(n+k)','안정','linear','자릿수(d)마다 버킷에 분배·수집한다. 값을 비교하지 않는 정렬이며 k는 기수(10진수면 10).'),
 ('계수 정렬','Counting sort','O(n+k)','O(n+k)','O(n+k)','O(n+k)','안정','linear','값의 등장 횟수를 센 뒤 누적합으로 자리를 정한다. 값의 범위 k가 n에 비해 작을 때 유리하다.')]

# name, en, best, average, worst, precondition, cue
SEARCHES=[
 ('순차(선형) 탐색','Sequential · Linear search','O(1)','O(n)','O(n)','없음 · 정렬 불필요','처음부터 차례로 비교한다. 탐색 성공 시 평균 비교 횟수는 (n+1)/2.'),
 ('이진 탐색','Binary search','O(1)','O(log n)','O(log n)','정렬된 배열','중간값과 비교해 절반을 버리기를 반복한다. 정렬이 전제이며 n=1,000이면 약 10번 비교.'),
 ('보간 탐색','Interpolation search','O(1)','O(log log n)','O(n)','정렬 + 값이 고르게 분포','값의 위치를 비례식으로 추정해 바로 접근한다. 분포가 치우치면 순차 탐색처럼 느려진다.'),
 ('피보나치 탐색','Fibonacci search','O(1)','O(log n)','O(log n)','정렬된 배열','피보나치 수로 구간을 나눈다. 곱셈·나눗셈 없이 덧셈·뺄셈만으로 분할 위치를 구한다.'),
 ('블록(점프) 탐색','Block · Jump search','O(1)','O(√n)','O(√n)','정렬된 배열','√n 크기의 블록 단위로 건너뛴 뒤 해당 블록 안에서 순차 탐색한다.'),
 ('이진 탐색 트리','Binary search tree','O(1)','O(log n)','O(n)','트리 구조','평균은 트리 높이 log n. 한쪽으로 치우친 편향 트리는 연결 리스트처럼 O(n).'),
 ('균형 이진 탐색 트리','AVL · Red-black tree','O(1)','O(log n)','O(log n)','자동 균형 트리','회전으로 높이를 log n으로 유지해 최악도 O(log n). B-트리·B+트리도 같은 O(log n) 계열.'),
 ('해싱','Hashing','O(1)','O(1)','O(n)','해시 함수 + 해시 테이블','키로 주소를 계산해 바로 접근한다. 충돌이 한곳에 몰리면 최악 O(n).')]

GROUPS=[
 ('quadratic','O(n²) 묶음','버블 · 선택 · 삽입 (+ 셸 O(n^1.5))','단순 비교 정렬. 입력이 두 배가 되면 시간은 네 배. 삽입은 거의 정렬된 입력에서 O(n), 선택은 항상 O(n²).'),
 ('nlogn','O(n log n) 묶음','퀵 · 합병 · 힙','비교 정렬의 평균 하한. 퀵은 최악 O(n²), 합병은 공간 O(n), 힙은 공간 O(1)이면서 항상 O(n log n).'),
 ('linear','분포 기반 묶음','기수 · 계수','값을 비교하지 않고 자릿수·횟수로 배치. O(dn)·O(n+k)로 선형에 가깝지만 값의 범위에 의존.')]

def growth_curves():
    left,right,bottom,top=42,340,240,18
    limit=40.0
    curves=[('O(n²)',lambda n:n*n,'#b8434c'),('O(n log n)',lambda n:n*math.log2(n) if n>1 else 0,'#9c650c'),('O(n)',lambda n:n,'#345ce0'),('O(log n)',lambda n:math.log2(n),'#087f84'),('O(1)',lambda n:1,'#7751cd')]
    drawing=f'<path d="M{left} {top} V{bottom} H{right}" class="edge"/>'+text(left-6,bottom+14,'n →','muted','start')+text(left-10,top+4,'시간','muted','end')
    for label,fn,color in curves:
        points=[]
        steps=80
        for i in range(steps+1):
            n=1+19*i/steps
            v=fn(n)
            if v>limit:
                if points:
                    prev_n,prev_v=points[-1][2],points[-1][3]
                    ratio=(limit-prev_v)/(v-prev_v)
                    n=prev_n+(n-prev_n)*ratio
                    v=limit
                else:
                    break
            x=left+(n-1)/19*(right-left)
            y=bottom-v/limit*(bottom-top)
            points.append((round(x,1),round(y,1),n,v))
            if v>=limit:break
        path=' '.join(('M' if i==0 else 'L')+f'{x} {y}' for i,(x,y,_,_) in enumerate(points))
        x,y=points[-1][0],points[-1][1]
        drawing+=f'<path d="{path}" class="edge" style="stroke:{color};stroke-width:2.4"/>'
        anchor={'O(n²)':'middle','O(n log n)':'start'}.get(label,'end')
        lx,ly=(x,y-6) if label=='O(n²)' else (x+4,y-6) if label=='O(n log n)' else (x-4,y-6)
        drawing+=f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" style="fill:{color};font-weight:700">{escape(label)}</text>'
    return svg(drawing,'입력 크기 n이 커질 때의 증가율: O(1), O(log n), O(n), O(n log n), O(n²) 순서로 가파르다',258)

def halving():
    drawing=''
    sizes=[16,8,4,2,1]
    for index,size in enumerate(sizes):
        width=size*18
        y=10+index*40
        x=20+(288-width)/2
        drawing+=f'<rect x="{x}" y="{y}" width="{width}" height="28" rx="7" class="node{" accent" if index in (0,4) else ""}"/>'
        drawing+=text(x+width+12,y+19,f'{size}개'+(' · 시작' if index==0 else ' · 찾음' if index==4 else ''),'' ,'start')
        if index<len(sizes)-1:drawing+=edge(164,y+29,164,y+38)
    drawing+=text(180,216,'16 → 8 → 4 → 2 → 1 : 4번 = log₂16','muted')
    return svg(drawing,'이진 탐색은 비교마다 후보를 절반으로 줄여 16개를 4번 만에 찾는다',226)

def compare_counts():
    rows=[('n = 10','10','33','100'),('n = 100','100','664','10,000'),('n = 1,000','1,000','9,966','1,000,000'),('n = 10,000','10,000','132,877','100,000,000')]
    out='<div class="matrix-wrap"><table><caption class="caption">같은 n에서 연산 횟수가 어떻게 벌어지는지 (log는 밑 2, 소수점 반올림)</caption><thead><tr><th>입력 크기</th><th>O(n)</th><th>O(n log n)</th><th>O(n²)</th></tr></thead><tbody>'
    for n,a,b,c in rows:
        out+=f'<tr><th>{n}</th><td>{a}</td><td>{b}</td><td><b>{c}</b></td></tr>'
    return out+'</tbody></table></div>'

def algorithm_preview():
    sort_lines='O(n²): 버블 · 선택 · 삽입<br>O(n^1.5): 셸<br>O(n log n): 퀵 · 합병 · 힙<br>O(dn): 기수 / O(n+k): 계수'
    search_lines='O(n): 순차<br>O(log n): 이진 · 피보나치 · BST<br>O(log log n): 보간<br>O(1): 해싱'
    return '<div class="mini-groups"><div><b>정렬 · 평균</b><p>'+sort_lines+'</p></div><div><b>탐색 · 평균</b><p>'+search_lines+'</p></div></div><p class="mini-hint">퀵 최악 O(n²) · 합병 공간 O(n) · 힙 공간 O(1)<br>이진 탐색은 정렬이 전제 / 해싱 최악 O(n)</p>'

def build_algorithm_chapter():
    body='<div class="note"><b>먼저 구분</b><span><b>시간복잡도는 입력 크기 n이 커질 때 연산 횟수가 늘어나는 비율</b>을 빅오(Big-O)로 적은 것입니다. 같은 알고리즘이라도 입력 상태에 따라 <b>최선·평균·최악</b>이 달라질 수 있으며, 실기에서 “시간복잡도를 쓰시오”라고만 하면 보통 <b>평균</b>을 묻습니다. 낮은 차수부터 <b>O(1) &lt; O(log n) &lt; O(n) &lt; O(n log n) &lt; O(n²) &lt; O(2ⁿ) &lt; O(n!)</b> 순서로 느려집니다.</span></div>'
    body+='<h3 class="subhead">1. 증가율을 그림으로 보기</h3><div class="grid"><article class="concept"><h3>차수별 증가 곡선</h3><div class="en">Growth of functions</div>'+growth_curves()+'<p>n이 커질수록 O(n²)는 급격히 위로 꺾이고, O(log n)은 거의 평평합니다. 정렬은 <b>O(n²)와 O(n log n)</b>, 탐색은 <b>O(n)과 O(log n)</b>의 차이를 구분하는 것이 핵심입니다.</p></article><article class="concept"><h3>연산 횟수로 체감하기</h3><div class="en">Why n log n matters</div>'+compare_counts()+'<p>n이 10배가 되면 O(n)은 10배, O(n²)는 100배가 됩니다. 10,000개를 정렬할 때 O(n²) 정렬은 O(n log n) 정렬보다 약 750배 많은 연산을 합니다.</p></article></div>'
    body+='<h3 class="subhead">2. 정렬 알고리즘 비교표</h3><div class="matrix-wrap"><table><caption class="caption">정렬 알고리즘의 최선 · 평균 · 최악 시간복잡도, 추가 공간, 안정성 (n = 원소 수, d = 자릿수, k = 값의 범위 또는 기수)</caption><thead><tr><th>알고리즘</th><th>최선</th><th>평균</th><th>최악</th><th>추가 공간</th><th>안정성</th></tr></thead><tbody>'
    for name,en,best,avg,worst,space,stable,_,_ in SORTS:
        body+=f'<tr><th>{name}<br><small>{en}</small></th><td>{best}</td><td><b>{avg}</b></td><td>{worst}</td><td>{space}</td><td>{stable}</td></tr>'
    body+='</tbody></table></div><p class="caption">안정 정렬은 같은 값의 원래 순서가 유지되는 정렬입니다. 셸 정렬의 복잡도는 간격 수열에 따라 달라지며 표는 수험서의 일반적인 표기를 따랐습니다. 버블 정렬은 교환이 없을 때 멈추는 개선형이면 최선 O(n)이지만, 기본형은 세 경우 모두 O(n²)입니다.</p>'
    body+='<h3 class="subhead">3. 정렬을 세 묶음으로 외우기</h3><div class="grid three">'
    for key,title,members,detail in GROUPS:
        cards=''.join(f'<p><b>{name}</b><br>{cue}</p>' for name,_,_,_,_,_,_,group,cue in SORTS if group==key)
        body+=f'<article class="concept"><div class="card-top"><h3>{title}</h3><span class="tag">{"평균" if key!="linear" else "선형"}</span></div><div class="mini-level">{members}</div><p>{detail}</p>{cards}</article>'
    body+='</div><div class="note"><b>자주 묻는 비교</b><span><b>퀵 정렬</b>: 평균 O(n log n), 최악 O(n²) — 피벗이 최솟값·최댓값으로만 뽑히는 경우. / <b>합병 정렬</b>: 항상 O(n log n)이지만 추가 메모리 O(n). / <b>힙 정렬</b>: 항상 O(n log n), 추가 메모리 O(1). / <b>삽입 정렬</b>: 거의 정렬된 입력에서 O(n). / <b>선택 정렬</b>: 어떤 입력이든 O(n²).</span></div>'
    body+='<h3 class="subhead">4. 탐색 알고리즘 비교표</h3><div class="matrix-wrap"><table><caption class="caption">탐색 알고리즘의 최선 · 평균 · 최악 시간복잡도와 전제 조건</caption><thead><tr><th>알고리즘</th><th>최선</th><th>평균</th><th>최악</th><th>전제 조건</th><th>기억 포인트</th></tr></thead><tbody>'
    for name,en,best,avg,worst,pre,cue in SEARCHES:
        body+=f'<tr><th>{name}<br><small>{en}</small></th><td>{best}</td><td><b>{avg}</b></td><td>{worst}</td><td>{pre}</td><td>{cue}</td></tr>'
    body+='</tbody></table></div><p class="caption">최선 O(1)은 첫 비교에서 찾는 경우입니다. 그래프 탐색인 DFS·BFS는 정점 V와 간선 E에 대해 O(V+E)로 따로 기억합니다.</p>'
    body+='<h3 class="subhead">5. 절반씩 줄이기와 바로 접근하기</h3><div class="grid"><article class="concept"><h3>이진 탐색 · O(log n)</h3><div class="en">Binary search</div>'+halving()+'<p>비교할 때마다 남은 후보가 절반이 되므로 n개를 찾는 데 약 log₂n번 비교합니다. <b>정렬된 배열</b>에서만 쓸 수 있고, 삽입·삭제가 잦으면 정렬 유지 비용이 따로 듭니다.</p><div class="pattern-cue">↳ 순차 탐색 평균 (n+1)/2번 vs 이진 탐색 약 log₂n번</div></article><article class="concept"><h3>해싱 · O(1)</h3><div class="en">Hashing</div><div class="mini-level">키 → 해시 함수 → 주소 → 바로 접근</div><p>키 값으로 저장 주소를 계산하므로 비교 없이 평균 O(1)에 접근합니다. 서로 다른 키가 같은 주소로 가는 <b>충돌</b>이 많아지면 체이닝·개방 주소법의 탐색 길이가 늘어 최악 O(n)이 됩니다.</p><p><b>트리 계열</b><br>이진 탐색 트리는 평균 O(log n)이지만 편향되면 O(n). AVL·레드블랙·B-트리처럼 균형을 유지하면 최악도 O(log n)입니다.</p></article></div>'
    body+='<div class="note"><b>한 줄 암기</b><span>정렬: <b>버·선·삽은 n², 퀵·합·힙은 n log n</b>, 기수·계수는 비교 없이 선형. / 탐색: <b>순차 n, 이진 log n, 보간 log log n, 해싱 1</b>. 예외 세 가지: 퀵 최악 n², 이진 탐색 트리 최악 n, 해싱 최악 n.</span></div>'
    body+='<div class="source-row"><a class="source" href="https://xlinux.nist.gov/dads/HTML/quicksort.html" target="_blank" rel="noopener noreferrer">↗ NIST DADS · quicksort</a><a class="source" href="https://xlinux.nist.gov/dads/HTML/binarySearch.html" target="_blank" rel="noopener noreferrer">↗ NIST DADS · binary search</a><a class="source" href="https://en.wikipedia.org/wiki/Sorting_algorithm#Comparison_of_algorithms" target="_blank" rel="noopener noreferrer">↗ Wikipedia · Comparison of sorting algorithms</a></div>'
    return '<section id="algorithms" class="chapter"><header class="chapter-head"><span class="chapter-no">18</span><div><p class="eyebrow">CONCEPT MAP / 18</p><h2>정렬·탐색 알고리즘의 시간복잡도</h2><p>평균 시간복잡도로 묶어 외우고, 최선·최악이 달라지는 알고리즘만 따로 기억합니다.</p></div></header>'+body+'</section>'
