import json,re,html
d=json.load(open('pages.json'))
out={}
def san(b):
    b=re.sub(r'<(script|style)[^>]*>.*?</\1>','',b,flags=re.S)
    b=re.sub(r'<div class="alert[^"]*">','<div class="cbox">',b)
    b=re.sub(r'<ol class="reference-list">','<ol class="refl">',b)
    b=re.sub(r'<(/?)(p|h\d|sup|ol|ul|li|strong|em|b|i|br|blockquote|table|tr|td|th|tbody|thead)\b[^>]*?(/?)>',r'<\1\2\3>',b)
    b=re.sub(r'<(?!/?(p|h\d|sup|ol|ul|li|strong|em|b|i|br|blockquote|table|tr|td|th|tbody|thead|div class="cbox"|/div)\b)[^>]*>','',b)
    b=re.sub(r'</div>','',b); b=re.sub(r'<div class="cbox">','',b)  # flatten
    b=re.sub(r'\s*\n\s*','\n',b).strip()
    return b
for p,h in d.items():
    if not h: continue
    t=html.unescape(re.search(r'<title>(.*?)</title>',h,re.S).group(1).split('|')[0]).strip()
    i=h.find('id="block-tulip-content"'); j=h.find('<nav role="navigation" aria-labelledby="book-label',i)
    if j<0: j=h.find('</main>')
    raw=h[i:j]
    hascbox='alert' in raw
    out[p]={'title':t,'html':san(raw.split('>',1)[1]),'cbox':hascbox}
json.dump(out,open('cci.json','w'),ensure_ascii=False,indent=0)
for k in ['/books/book-of-praise/confessions/canons-of-dort/section1','/books/book-of-praise/confessions/the-belgic-confession/1','/books/book-of-praise/confessions/heidelberg-catechism/section1','/books/book-of-praise/creeds/athanasian-creed']:
    print(k,out[k]['title']); print(out[k]['html'][:1500]); print('====')
