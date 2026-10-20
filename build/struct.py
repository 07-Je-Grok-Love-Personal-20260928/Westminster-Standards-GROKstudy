import json,re
c=json.load(open('cci.json'))
B='/books/book-of-praise/'
out={}
out['creeds_intro']=c[B+'creeds']['html']
cr=[]
for k,name in [('apostles-creed','使徒信经'),('nicene-creed','尼西亚信经'),('athanasian-creed','亚他那修信经')]:
    h=c[B+'creeds/'+k]['html']
    ps=re.findall(r'<p>(.*?)</p>',h,re.S)
    cr.append({'id':k,'title':c[B+'creeds/'+k]['title'],'intro':ps[0],'body':ps[1:],'url':'https://ccifellowship.org/'+B+'creeds/'+k})
out['creeds']=cr
out['bc_intro']=c[B+'confessions/the-belgic-confession']['html']
out['bc']=[{'no':i,'title':c[B+'confessions/the-belgic-confession/%d'%i]['title'],'html':c[B+'confessions/the-belgic-confession/%d'%i]['html'],'url':'https://ccifellowship.org/'+B+'confessions/the-belgic-confession/%d'%i} for i in range(1,38)]
out['hc_intro']=c[B+'confessions/heidelberg-catechism']['html']
ld={}
for k,v in c.items():
    m=re.search(r'lord-day-(\d+)$',k)
    if m: ld[int(m.group(1))]=(k,v)
hc=[];qs={}
for n in range(1,53):
    k,v=ld[n]
    h=v['html']
    parts=re.split(r'<h4>',h)
    items=[]
    for p in parts[1:]:
        qh,rest=p.split('</h4>',1)
        qh=re.sub(r'<[^>]+>','',qh).strip()
        m=re.match(r'(\d+)[．.]\s*问：(.*)',qh)
        q=int(m.group(1)); items.append({'q':q,'ques':m.group(2).strip(),'html':rest.strip()})
        qs[q]=n
    hc.append({'ld':n,'items':items,'url':'https://ccifellowship.org'+k})
out['hc']=hc
print('HC Q count',sum(len(x['items']) for x in hc), min(qs),max(qs))
# HC section structure from paths
secs={}
for k in c:
    m=re.search(r'heidelberg-catechism/(section\d)(?:/(part\d))?$',k)
    if m: secs[m.group(0)]=c[k]['title']
out['hc_secs']=secs
out['cd_intro']=c[B+'confessions/canons-of-dort']['html']
cd=[]
for s in ['section1','section2','section3-4','section5']:
    arts=[]
    i=1
    while B+'confessions/canons-of-dort/%s/%d'%(s,i) in c:
        p=c[B+'confessions/canons-of-dort/%s/%d'%(s,i)]
        arts.append({'no':i,'title':p['title'],'html':p['html'],'url':'https://ccifellowship.org/'+B+'confessions/canons-of-dort/%s/%d'%(s,i)}); i+=1
    cd.append({'id':s,'title':c[B+'confessions/canons-of-dort/'+s]['title'],'intro':c[B+'confessions/canons-of-dort/'+s]['html'],'arts':arts})
out['cd']=cd
print([(x['title'],len(x['arts'])) for x in cd]); print(secs)
json.dump(out,open('../build/cci_struct.json','w'),ensure_ascii=False,indent=1)
