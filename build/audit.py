import json,re,html,sys
D=json.load(open('data/standards.json'));C=json.load(open('data/cci_struct.json'))
def strip(s): return re.sub(r'\s+','',html.unescape(re.sub(r'<[^>]+>','',re.sub(r'⟦\d+⟧','',s))))
corpus=[]
for ch in D['wcf']:
    for s in ch['secs']: corpus.append(s['text']+s.get('tail','')); corpus+= [v for v in s['refs'].values()]
for d in ('wlc','wsc'):
    for u in D[d]: corpus+=[u['ques'],u['ans']]+list(u['refs'].values())
corpus.append(D['wlc_act'])
def walk(o):
    if isinstance(o,str): corpus.append(o)
    elif isinstance(o,dict): [walk(v) for v in o.values()]
    elif isinstance(o,list): [walk(v) for v in o]
walk(C)
try: corpus.append(open('/workspace/rtf.txt').read())
except: pass
big=strip('\n'.join(corpus)); bigd=re.sub(r'\d','',big)
def ok(raw):
    q=strip(raw)
    if q in big or re.sub(r'\d','',q) in bigd: return True
    parts=[p for p in re.split(r'……|…',q) if len(p)>=2]
    return bool(parts) and all(re.sub(r'\d','',p.rstrip('。，；')) in bigd for p in parts)
files=sys.argv[1:] if __name__=='__main__' else []
bad=0
for f in files:
    s=open(f).read()
    for m in re.finditer(r'“([^”]{4,})”',s):
        q=strip(m.group(1))
        q2=re.sub(r'[……。，、；：！？「」『』（）()…\.]','',q)
        if q in big or re.sub(r'\d','',q) in bigd: continue
        # allow ellipsis-separated fragments
        parts=[p for p in re.split(r'……|…',strip(m.group(1))) if len(p)>=2]
        if parts and all(re.sub(r'\d','',p.rstrip('。，；')) in bigd for p in parts): continue
        bad+=1
        ln=s[:m.start()].count('\n')+1
        print(f'{f}:{ln}: “{m.group(1)[:80]}”')
if __name__=='__main__': print('nonmatching',bad)

