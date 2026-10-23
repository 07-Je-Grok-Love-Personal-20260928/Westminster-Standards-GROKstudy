import re, json
L=open('body.txt').read().split('\n')
fns=json.load(open('fns.json'))
CN='一二三四五六七八九十'
def clean(s): return re.sub(r'[ \u3000]+',' ',s).strip()
units=[]  # dict(doc, ...,text)
def newunit(**k):
    u=dict(k); u['raw']=''; units.append(u); return u
cur=None; chap=None
wcf_ch=[]
for i,line in enumerate(L):
    ln=i+1
    if 573<=ln<3428:
        m=re.match(r'^(第[一二三四五六七八九十]+章)\s*(.+?)\s*$',re.sub(r'⟪F\d+⟫','',line))
        if m and '⟦' not in line:
            chap={'no':len(wcf_ch)+1,'title':m.group(2).strip(),'secs':[]}; wcf_ch.append(chap); cur=None; continue
        m=re.match(r'^([一二三四五六七八九十]+)、',line)
        if m and chap:
            cur=newunit(doc='wcf',ch=chap['no'],sec=m.group(1)); chap['secs'].append(cur)
        elif chap and cur is None and line.strip() and not line.startswith('⟪'):
            cur=newunit(doc='wcf',ch=chap['no'],sec=''); chap['secs'].append(cur)
        if cur is not None: cur['raw']+=line+'\n'
    elif 3753<ln:
        if cur is not None and cur['doc']=='wcf': cur=None
        m=re.match(r'^(?:第|问)\s*(\d+)\s*问?[：:]?\s*(.*)$',line)
        if m:
            doc='wlc' if ln<8420 else 'wsc'
            cur=newunit(doc=doc,q=int(m.group(1)),raw2='')
            cur['raw']=line[m.end(1):]+'\n'; cur['raw']='问：'+m.group(2)+'\n'; continue
        if ln==8420: cur=None; continue
        if cur is not None: cur['raw']+=line+'\n'
# footnote assignment: each unit, markers in raw; footnote placeholders positioned in raw
# collect placeholders globally in order with unit index
seq=[]
for ui,u in enumerate(units):
    for m in re.finditer(r'⟦(\d+)⟧|⟪F(\d+)⟫',u['raw']):
        if m.group(1): seq.append(('m',ui,m.group(1)))
        else: seq.append(('f',ui,int(m.group(2))))
pending=[]  # (ui,num)
for u in units: u['refs']={}
for kind,ui,v in seq:
    if kind=='m': pending.append((ui,v))
    else:
        num,txt=fns[v]
        for j in range(len(pending)-1,-1,-1):
            pu,pn=pending[j]
            if pn==num and num not in units[pu]['refs']:
                units[pu]['refs'][num]=clean(txt); pending.pop(j); break
        else:
            units[ui]['refs'].setdefault(num.rstrip('.'),clean(txt))
if pending: print('unmatched markers',len(pending),pending[:10])
def body(u):
    s=re.sub(r'⟪F\d+⟫','',u['raw'])
    s=s.replace('\n','')
    s=re.sub(r'\s*⟦(\d+)⟧\s*',r'⟦\1⟧',s)
    s=re.sub(r'(?<=[\u4e00-\u9fff，。；：、（）《》“”？！])\s+|\s+(?=[\u4e00-\u9fff，。；：、（）《》“”？！])','',s)
    return clean(s)
for u in units:
    u['text']=body(u); del u['raw']
out={'wcf':[{'no':c['no'],'title':c['title'],'secs':[{'sec':s['sec'],'text':s['text'],'refs':s['refs']} for s in c['secs']]} for c in wcf_ch],
 'wlc':[{'q':u['q'],'text':u['text'],'refs':u['refs']} for u in units if u['doc']=='wlc'],
 'wsc':[{'q':u['q'],'text':u['text'],'refs':u['refs']} for u in units if u['doc']=='wsc']}
for k in out: print(k,len(out[k]))
print([ (c['no'],c['title'],len(c['secs'])) for c in out['wcf']])
print([u['q'] for u in out['wlc']][:5], [u['q'] for u in out['wlc']][-3:], len(set(u['q'] for u in out['wlc'])))

for k in ['wlc','wsc']:
    for u in out[k]:
        t=u.pop('text'); i=t.find('答：')
        u['ques']=t[2:i] if t.startswith('问：') else t[:i]; u['ans']=t[i+2:]
w=out['wsc'][-1]; w['ans']=w['ans'].replace('www.rtf-usa.comrtfdirector@gmail.com','')
w['refs']['3']=w['refs']['3'].split(' 唉！')[0]
act=re.sub(r'⟪F\d+⟫|\n','',''.join(L[3752:3786]))
out['wlc_act']=clean(act)
import re as _r
json.dump(out,open('standards.json','w'),ensure_ascii=False,indent=1)

# fix WCF 1.2 book list
i0=[i for i,l in enumerate(L) if l.startswith('二、通常所说的《圣经》')][0]
blk=[];j=i0
while '所有这些书卷' not in L[j]: blk.append(re.sub(r'⟪F\d+⟫','',L[j]).strip()); j+=1
blk=[b for b in blk if b]
ot_i=blk.index('旧约：'); nt_i=blk.index('新约：')
ot=blk[ot_i+1:nt_i]; nt=blk[nt_i+1:]
ot=ot[0::3]+ot[1::3]+ot[2::3]; nt=nt[0::3]+nt[1::3]+nt[2::3]
s=out['wcf'][0]['secs'][1]
s['text']='二、通常所说的《圣经》是神成文的话，包括旧约和新约所有的书卷：'
s['ot']=ot; s['nt']=nt; s['tail']='所有这些书卷都是神所默示的，是信仰和生活的准则⟦7⟧。'
print(len(ot),len(nt),ot[:6],nt[:6])
json.dump(out,open('standards.json','w'),ensure_ascii=False,indent=1)
