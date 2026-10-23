import pymupdf, re, json
d=pymupdf.open('../rtf.pdf')
stream=[]  # tokens: ('b',text) ('m',n) ('fn',n) ('ft',text) ('nl',)
start=None
for pn in range(len(d)):
    for b in d[pn].get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                t=s['text']; sz=s['size']
                if not t.strip(): continue
                if sz>=11.5: stream.append(('b',t))
                elif 5.5<=sz<7: stream.append(('m',t.strip()))
                elif sz<5.5: stream.append(('fn',t.strip()))
                elif 9.5<=sz<11: stream.append(('ft',t))
            stream.append(('nl',pn))
# build body text with markers
body=[];fns=[]
cur=None
for tok in stream:
    if tok[0]=='b': body.append(tok[1])
    elif tok[0]=='m': body.append('⟦%s⟧'%tok[1])
    elif tok[0]=='nl': body.append('\n')
    elif tok[0]=='fn': fns.append([tok[1],'']); body.append('⟪F%d⟫'%(len(fns)-1))
    elif tok[0]=='ft':
        if fns: fns[-1][1]+=tok[1]
txt=''.join(body)
open('body.txt','w').write(txt)
json.dump(fns,open('fns.json','w'),ensure_ascii=False)
