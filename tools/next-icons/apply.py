#!/usr/bin/env python3
"""Release helper (v229): puts the new-character app icons + notification pictures in place.
Run from the repo root at release time:  python3 tools/next-icons/apply.py
Copies every file in tools/next-icons/ (except this script and favicon-64.png) to the same path in the repo,
and swaps the base64 favicon in index.html and beta/index.html for favicon-64.png."""
import os,re,shutil,base64
H=os.path.dirname(os.path.abspath(__file__));R=os.path.abspath(os.path.join(H,'..','..'))
for d,_,fs in os.walk(H):
    for f in fs:
        if f in('apply.py','favicon-64.png'):continue
        src=os.path.join(d,f);dst=os.path.join(R,os.path.relpath(src,H));os.makedirs(os.path.dirname(dst),exist_ok=True);shutil.copyfile(src,dst);print('copied',os.path.relpath(dst,R))
b=base64.b64encode(open(os.path.join(H,'favicon-64.png'),'rb').read()).decode()
for p in('index.html','beta/index.html'):
    fp=os.path.join(R,p);s=open(fp,encoding='utf-8').read()
    s2,n=re.subn(r'(<link rel="icon"[^>]*href=")data:image/png;base64,[^"]+(")',r'\g<1>data:image/png;base64,'+b+r'\g<2>',s,count=1)
    open(fp,'w',encoding='utf-8').write(s2);print(p,'favicon replaced' if n else 'favicon NOT found')
