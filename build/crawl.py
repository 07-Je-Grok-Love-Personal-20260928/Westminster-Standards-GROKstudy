import re,urllib.request,json,html,time
from html.parser import HTMLParser
base='https://ccifellowship.org'
seen={};queue=['/books/book-of-praise/creeds','/books/book-of-praise/confessions/heidelberg-catechism','/books/book-of-praise/confessions/the-belgic-confession','/books/book-of-praise/confessions/canons-of-dort']
def get(p):
    r=urllib.request.Request(base+p,headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(r,timeout=60).read().decode('utf8')
while queue:
    p=queue.pop(0)
    if p in seen: continue
    try: h=get(p)
    except Exception as e: print('ERR',p,e); seen[p]=None; continue
    seen[p]=h
    for l in re.findall(r'href="(/books/book-of-praise/(?:creeds|confessions)[^"#?]*)"',h):
        if l not in seen and l not in queue: queue.append(l)
print(len(seen))
json.dump(seen,open('pages.json','w'),ensure_ascii=False)
