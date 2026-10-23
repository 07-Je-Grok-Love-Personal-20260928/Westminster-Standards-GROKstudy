import json,collections,sys
c=collections.Counter();tot=0
for w in (390,768,1440):
    for r in json.load(open(f'/workspace/perf/check_all_{w}.json')):
        tot+=1;k=[]
        if r.get('docOverflow',0)>0: k.append('docOverflow')
        if r.get('bad'): k.append('bad:'+r['bad'][0][:60])
        if r.get('trunc'): k.append('trunc:'+r['trunc'][0][:60])
        if r.get('topbarOverlap'): k.append('topbar')
        if r['errs']: k.append('err:'+r['errs'][0][:100])
        if r.get('mermaid') and not r['mermaid'].startswith('0/'): k.append('mm')
        if r.get('imgs'): k.append('imgs')
        if r.get('map')==0: k.append('map0')
        if r.get('tabsOverflow'): k.append('tabs')
        for s,v in (r.get('contrast') or {}).items():
            if v<4.5: k.append(f"contrast {s} {v} {r['pal']}/{r['mode']}")
        for x in k: c[(r['page'],x)]+=1
print('page loads checked',tot,'problem kinds',len(c))
for k,v in c.most_common(40): print(v,k)
