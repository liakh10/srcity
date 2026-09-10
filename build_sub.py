#!/usr/bin/env python3
"""Builds every resident's sub-site into /<id>/index.html from citizens.js + _sub.tpl.html. Run: python3 build_sub.py"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).parent
src = (ROOT / 'citizens.js').read_text()
data = json.loads(re.search(r'window\.CITIZENS\s*=\s*(\[.*\]);', src, re.S).group(1))
tpl = (ROOT / '_sub.tpl.html').read_text()
for i, c in enumerate(data):
    shots = ''.join('<button data-i="%d" aria-label="%s"><img src="../assets/%s/t%d.webp" alt="%s %s" loading="lazy" /><b>%s</b></button>'
                    % (k, cap, c['id'], k + 1, c['name'], cap.lower(), cap) for k, cap in enumerate(c['caps']))
    neigh = ''.join('<a href="../%s/" title="%s · %s"><img src="../assets/h-%s.webp" alt="%s" /><span>%s</span></a>'
                    % (d['id'], d['name'], d['district'], d['id'], d['name'], d['name']) for d in data if d['id'] != c['id'])
    lore = ''.join('<p>%s</p>' % l for l in c['lore'])
    prev, nxt = data[i - 1], data[(i + 1) % len(data)]
    rep = {'ID': c['id'], 'NAME': c['name'], 'DISTRICT': c['district'], 'HEAD': c['head'], 'BODY': c['body'],
           'ACCENT': c['accent'], 'LINE': c['line'], 'SEEN': c['seen'], 'LORE': lore, 'SHOTS': shots, 'NEIGH': neigh,
           'N': str(len(c['caps'])), 'NUM': '%02d' % (i + 1), 'PREV': prev['id'], 'PREVNAME': prev['name'],
           'NEXT': nxt['id'], 'NEXTNAME': nxt['name'], 'CAPS': json.dumps(c['caps']),
           'DESC': re.sub(r'<[^>]+>', '', c['line'])}
    html = tpl
    for k, v in rep.items():
        html = html.replace('{{' + k + '}}', v)
    out = ROOT / c['id']; out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(html)
    print('built', c['id'])
