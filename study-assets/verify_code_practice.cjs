// Deployment checks for the user-supplied code/SQL/theory practice page.
// Runs the page's actual grading helpers; does not claim browser layout testing.
const fs=require('fs'), path=require('path'), vm=require('vm'), assert=require('assert/strict');
const root=path.join(__dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8').replace(/\r\n/g,'\n');
const source=read('정처기_실기_코드문제풀이.html'), deployed=read('code-practice.html');
assert.equal(source,deployed,'Published copy must match the original practice page');
assert(/^<!doctype html>/i.test(source));
assert(source.includes('<html lang="ko">'));
assert(/<meta charset="utf-8">/.test(source));
assert(/<meta name="viewport"/.test(source));
assert(source.includes('href="index.html#home"'));
assert(read('index.html').includes('href="code-practice.html"'));
assert(read('정보처리기사_핵심이론_그림정리.html').includes('href="code-practice.html"'));
const P=JSON.parse(source.match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1]);
const code=[...source.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]).join('\n');
new Function(code);
assert.equal(P.length,173);assert.equal(new Set(P.map(p=>p.id)).size,P.length);
assert.deepEqual(P.map(p=>p.id),Array.from({length:P.length},(_,i)=>i+1));
const types=Object.fromEntries(['code','blank','sql'].map(k=>[k,P.filter(p=>p.type===k).length]));
assert.deepEqual(types,{code:81,blank:87,sql:5});
assert(code.includes("const LS = 'jcg-quiz-v1'"));
assert(!code.includes("const LS = 'visual-study-practice-v2'"));
const localDependencies=[...source.matchAll(/<(?:script|link)[^>]+(?:src|href)="([^"]+)"/g)].map(x=>x[1]).filter(x=>!/^https:\/\//.test(x));
assert.deepEqual(localDependencies,[],'Question data is embedded; no missing question bank file');
const helperStart=code.indexOf('function norm(s)'), helperEnd=code.indexOf('// ---------- 렌더링');
assert(helperStart>=0 && helperEnd>helperStart);
const grading=vm.createContext({});
vm.runInContext(code.slice(helperStart,helperEnd),grading);
let variants=0;
for(const p of P){
  assert(p.title && p.expl && Number.isInteger(p.ch));
  assert(['book','bank','extra'].includes(p.src));
  if(p.type==='code'){
    assert(p.code && typeof p.output==='string');
    assert.equal(grading.grade(p,p.output),'exact','Canonical code output '+p.id);
    assert.equal(grading.grade(p,'__wrong_answer__'),'wrong');
    if(p.console)assert.equal(grading.grade(p,p.console),'exact');
    variants++;
  }else if(p.type==='blank'){
    assert(p.blanks.length>0 && p.blanks.every(b=>b.a.length>0));
    const canonical=p.blanks.map(b=>b.a[0]);
    assert(grading.gradeBlanks(p,canonical).every(Boolean),'Canonical blanks '+p.id);
    assert(grading.gradeBlanks(p,p.blanks.map(()=> '__wrong_answer__')).every(v=>!v));
    for(let i=0;i<p.blanks.length;i++)for(const a of p.blanks[i].a){
      const answers=[...canonical];answers[i]=a;
      assert(grading.gradeBlanks(p,answers).every(Boolean),'Accepted blank '+p.id);variants++;
    }
    if(p.anyOrder){
      assert(grading.gradeBlanks(p,[...canonical].reverse()).every(Boolean));
      if(p.blanks.length>1 && new Set(canonical).size>1)assert(!grading.gradeBlanks(p,p.blanks.map(()=>canonical[0])).every(Boolean));
    }
  }else{
    assert(p.model);
    for(const answer of [p.model,...(p.accept||[])]){assert(grading.normSql(answer));variants++;}
    assert.notEqual(grading.normSql(p.model),grading.normSql('__wrong_answer__'));
  }
}
// Highlighting has an escaped-code fallback when the optional CDN is unavailable.
const highlight=code.slice(code.indexOf('function highlight(p)'),code.indexOf('function markSvg(kind)'));
const fallback={window:{},esc:s=>s.replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))};
vm.createContext(fallback);vm.runInContext(highlight,fallback);
assert.equal(fallback.highlight({lang:'C',code:'a < b'}),'a &lt; b');
console.log(JSON.stringify({questionCount:P.length,types,acceptedVariantsChecked:variants,sourceAndPublishedCopyMatch:true,embeddedQuestionData:true,bidirectionalNavigation:true,separateStorageKey:true,optionalHighlightFallback:true,scriptSyntax:'passed'},null,2));
