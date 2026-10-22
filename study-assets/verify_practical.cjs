// Current offline validation: node study-assets/verify_practical.cjs
// Validates the emitted question bank and executes the actual grading listeners
// with small DOM doubles. This is not a browser layout or visual test.
const fs = require('fs'), path = require('path'), vm = require('vm');
const assert = require('assert/strict');
const file = path.join(__dirname, '..', '정보처리기사_핵심이론_그림정리.html');
const html = fs.readFileSync(file, 'utf8');
assert.equal(fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8'), html, 'Pages and offline entry points must match');
const json = id => JSON.parse(html.match(new RegExp('id="'+id+'">([\\s\\S]*?)</script>'))[1]);
const bank = json('practice-data'), topics = json('topic-data');
const all = Object.values(bank).flat();
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n');
new Function(code);
const normalize = vm.runInNewContext('('+code.match(/function normalize\(s\)\{[^\n]+/)[0]+')');
const expected = {'uml-rel':1,'uml-types':2,cocomo:1,patterns:3,network:3,whitebox:5,principles:1,'security-cia':1,'drm-components':1,'drm-technologies':1,'routing-protocols':2,'version-control':1,encryption:3,attacks:6,storage:0,'security-protocols':1,'osi-layers':1,algorithms:0};
assert.deepEqual(Object.fromEntries(Object.entries(bank).map(([k,v])=>[k,v.length])), expected);
assert.deepEqual(topics.map(t=>t[0]), Object.keys(bank));
assert.equal(all.length, 33);
assert.equal(new Set(all.map(q=>q.provenance.canonical_id)).size, 32);
assert.equal(new Set(all.map(q=>q.id)).size, all.length);
const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]);
assert.equal(new Set(ids).size, ids.length, 'HTML ids must be unique');
assert.equal((html.match(/<a class="topic-box"/g)||[]).length, 18);
assert.equal((html.match(/class="chapter concept-page"/g)||[]).length, 18);
assert.equal((html.match(/<form class="question-box"/g)||[]).length, 33);
assert(!/<aside\b|class="sidebar"/.test(html));
assert(html.includes('border:1px solid var(--line);border-radius:16px'));
assert(html.includes('visual-study-practice-v2'));
assert(!html.includes('160번 문제를 푸는'));
for (const [key, qs] of Object.entries(bank)) {
  assert(html.includes('href="#concept/'+key+'"'));
  assert(html.includes('id="practice-'+key+'"'));
  for (const q of qs) {
    const p=q.provenance;
    assert(q.id.startsWith('ipe-past-'));
    assert.equal(p.qualification,'정보처리기사'); assert.equal(p.exam_type,'실기');
    assert(Number.isInteger(p.year) && p.year>=2019 && p.year<=2025);
    assert([1,2,3].includes(p.round));
    assert.equal(p.verified_on,'2026-10-22');
    assert(['publisher','public_reconstruction'].includes(p.source_kind));
    assert(p.source_locator && p.wording && q.explain && q.source);
    assert(q.exam.includes(p.year+'년 '+p.round+'회 실기'));
    assert(!q.exam.includes('필기') && !q.origin);
    assert.equal(new URL(q.url).protocol,'https:');
    if(p.year<2020) assert(q.exam.includes('개편 전'));
    if(p.part) assert(q.exam.includes(p.part));
    const form=html.split('data-question="'+q.id+'"')[1].split('</form>')[0];
    assert.equal((form.match(/data-answer="\d+"/g)||[]).length,q.fields.length);
    assert(form.includes(q.url.replaceAll('&','&amp;')));
    for (const [i,f] of q.fields.entries()) {
      assert(f.answers.length>0 && f.answers.every(a=>typeof a==='string' && normalize(a)));
      assert(html.includes('for="answer-'+q.id+'-'+i+'"'));
      assert(!f.answers.some(a=>normalize(a)===normalize('zzwrongzz')));
    }
  }
}
assert.deepEqual(all.filter(q=>q.self_check).map(q=>q.id),['ipe-past-pesticide-2020-1']);
assert(html.includes('COCOMO 유형을 직접 묻는 문제가 아니라'));
assert(html.includes('DRM 구성요소 페이지와 같은 출제 문항'));
assert.equal(new Set(all.map(q=>q.url.split('#')[0])).size,14);
const find = fragment => all.find(q=>q.id==='ipe-past-'+fragment);
const accepts = (q,i,v) => q.fields[i].answers.some(a=>normalize(a)===normalize(v));
assert(accepts(find('uml-rel-2024-3'),0,'연관 관계'));
assert(accepts(find('class-2021-3'),0,'Class Diagram'));
assert(accepts(find('mcdc-2024-1'),0,'MC/DC'));
assert(accepts(find('vcs-2022-3'),0,'Git, CVS, SVN'));
assert(!accepts(find('vcs-2022-3'),0,'Git, CVS'));
assert(accepts(find('asymmetric-2023-2'),0,'SEED, ARIA, AES, DES'));
assert(accepts(find('asymmetric-2023-2'),1,'ECC, RSA'));
assert(!accepts(find('asymmetric-2023-2'),0,'RSA, ECC'));

// Execute the emitted input, submit, reveal and retry code rather than a copy.
class Control {
  constructor(){this.listeners={};this.value='';this.validity='';this.focused=false;}
  addEventListener(event,fn,options){(this.listeners[event]??=[]).push({fn,once:!!options?.once});}
  fire(event){const events=[...(this.listeners[event]||[])];this.listeners[event]=(this.listeners[event]||[]).filter(x=>!x.once);for(const {fn} of events)fn({preventDefault(){}});}
  setCustomValidity(v){this.validity=v;} reportValidity(){this.reported=true;} focus(){this.focused=true;}
}
const forms=new Map(), state=new Map(); let saves=0, progress=0, feedbacks=0;
for(const q of all){
  const inputs=q.fields.map(()=>new Control());
  const buttons={'[data-reveal]':new Control(),'[data-retry]':new Control()};
  const form=new Control();
  form.inputs=inputs;
  form.querySelectorAll=s=>{assert.equal(s,'[data-answer]');return inputs;};
  form.querySelector=s=>buttons[s]||(s==='[data-answer]'?inputs[0]:inputs[Number(s.match(/data-answer="(\d+)"/)[1])]);
  forms.set(q.id,form);
}
const get=q=>{if(!state.has(q.id))state.set(q.id,{values:q.fields.map(()=>''),result:null,revealed:false,show:false});return state.get(q.id);};
const start=code.indexOf('for(const q of all){const form=');
const end=code.indexOf('for(const [key,qs]of Object.entries(bank)){const panel=',start);
assert(start>=0 && end>start);
vm.runInNewContext(code.slice(start,end),{all,get,normalize,$:s=>forms.get(s.match(/data-question="([^"]+)"/)[1]),feedback:()=>feedbacks++,save:()=>saves++,refreshProgress:()=>progress++});
let variantChecks=0;
for(const q of all){
  const form=forms.get(q.id),s=get(q);
  form.fire('submit'); assert.equal(s.show,false); assert.equal(form.inputs[0].validity,'답을 입력한 뒤 확인해 주세요.');
  for(let i=0;i<q.fields.length;i++){form.inputs[i].value=q.fields[i].answers[0];form.inputs[i].fire('input');}
  assert.equal(form.inputs[0].validity,'');
  form.fire('submit'); assert.equal(s.show,true);
  if(q.self_check)assert.equal(s.result,null);else assert.equal(s.result,'correct',q.id);
  if(!q.self_check){
    for(let i=0;i<q.fields.length;i++)for(const answer of q.fields[i].answers){
      form.inputs[i].value=answer; form.inputs[i].fire('input');form.fire('submit');
      assert.equal(s.result,'correct',q.id+' alias '+answer);variantChecks++;
    }
    form.inputs[0].value='zzwrongzz';form.inputs[0].fire('input');
    assert.equal(s.result,null);assert.equal(s.show,false);
    form.fire('submit');assert.equal(s.result,'incorrect',q.id);
  }
  form.querySelector('[data-retry]').fire('click');
  assert.equal(s.result,null);assert.equal(s.show,false);assert(s.values.every(v=>v===''));assert(form.inputs[0].focused);
  form.querySelector('[data-reveal]').fire('click');
  assert.equal(s.show,true);assert.equal(s.revealed,true);assert.equal(s.result,null);
}
assert(saves>0 && progress>0 && feedbacks>0);
const report={verifiedOn:'2026-10-22',mode:'static HTML + Node VM grading listeners; no browser layout claim',conceptCount:topics.length,questionPlacements:all.length,distinctExamItems:32,sourcePages:14,writtenExamQuestions:0,selfAuthoredQuestions:0,questionCounts:expected,acceptedAnswerVariantsChecked:variantChecks,checks:['script syntax','unique IDs and labels','17 concept routes and question forms','year/round/source metadata for every item','pre-reform and partial question labels','related-scope and duplicated DRM disclosure','actual input/submit/reveal/retry handlers','correct and incorrect answers','empty input validity','unordered tool and algorithm answers']};
fs.writeFileSync(path.join(__dirname,'practical-verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
