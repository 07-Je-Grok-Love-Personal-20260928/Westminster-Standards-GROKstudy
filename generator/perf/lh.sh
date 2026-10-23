#!/bin/bash
# usage: lh.sh port tag
for p in index wcf recite history; do
 CHROME_PATH=/usr/bin/google-chrome npx -y lighthouse http://127.0.0.1:$1/$p.html --only-categories=performance --chrome-flags="--headless=new --no-sandbox" --output=json --output-path=$2-$p.json --quiet >/dev/null 2>&1
 python3 -c "
import json;d=json.load(open('$2-$p.json'));a=d['audits']
print('$2','$p','score',round(d['categories']['performance']['score']*100),'FCP',a['first-contentful-paint']['displayValue'],'LCP',a['largest-contentful-paint']['displayValue'],'TBT',a['total-blocking-time']['displayValue'],'CLS',a['cumulative-layout-shift']['displayValue'],'TTI',a['interactive']['displayValue'])"
done
