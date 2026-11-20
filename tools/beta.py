#!/usr/bin/env python3
"""Test version of the calendar (owner, v149: "a section where I can test new features before they get released").
  python3 tools/beta.py start    -> beta/index.html = a copy of index.html with the TEST markers (start a new round of changes)
  python3 tools/beta.py promote  -> index.html = beta/index.html without the markers (release what was tested)
  python3 tools/beta.py status   -> CC_VER of both
The markers sit right after <meta charset>: <base href="../"> makes every relative file (fonts, siddur, sefaria, sw.js…) load
from the main folder, and window.CC_BETA / class cc-beta switch on the test look. Same address = same accounts and data."""
import re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
MAIN, BETA = R / 'index.html', R / 'beta' / 'index.html'
A, B = '<!--BETA-->', '<!--/BETA-->'
MARK = A + '<base href="../"><script>window.CC_BETA=1;document.documentElement.classList.add("cc-beta")</script>' + B
CS = '<meta charset="utf-8">'
ver = lambda s: int(re.search(r'const CC_VER=(\d+);', s).group(1))
def start():
    s = MAIN.read_text(encoding='utf-8'); assert A not in s and CS in s
    BETA.parent.mkdir(exist_ok=True); BETA.write_text(s.replace(CS, CS + MARK, 1), encoding='utf-8'); print('beta = main, CC_VER', ver(s))
def promote():
    s = BETA.read_text(encoding='utf-8'); assert s.count(A) == 1
    s = re.sub(re.escape(A) + '.*?' + re.escape(B), '', s, count=1, flags=re.S); MAIN.write_text(s, encoding='utf-8'); print('released CC_VER', ver(s))
def status():
    print('main', ver(MAIN.read_text(encoding='utf-8')), '| test', ver(BETA.read_text(encoding='utf-8')) if BETA.exists() else '-')
{'start': start, 'promote': promote, 'status': status}[sys.argv[1] if len(sys.argv) > 1 else 'status']()
