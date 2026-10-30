# -*- coding: utf-8 -*-
"""Genera fichas estaticas (SEO) para las marcas con producto.html?id= dinamico:
CST, SIDI, USWE, Giant Loop, Lucioli, Nitro Mousse.
Hornea title/meta/canonical/OG + H1/kicker/descripcion, fuerza el id (window.FORCE_ID),
y escribe un mapa id->archivo por marca para re-linkear listados/catalogo."""
import re, json, html, unicodedata
from pathlib import Path
ROOT = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web")
SITEM = "https://radsport.com.ar/marcas/"

def slug(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    s = re.sub(r'[^\w\s-]','',s); return re.sub(r'[\s_]+','-',s).strip('-')
def esc(s): return html.escape(s or '', quote=True)
def striptags(s): return re.sub(r'<[^>]+>','', s or '')
def desclist(d): return d if isinstance(d, list) else [d]

# por marca: nombre a mostrar, campo del nombre, prefijo de titulo, prefijo de archivo
CFG = {
 'cst':        dict(disp='CST',         namef='model', fslug='cubierta-cst',  tprefix=lambda p:'Cubierta CST'),
 'sidi':       dict(disp='SIDI',        namef='name',  fslug='botas-sidi',    tprefix=lambda p:'Botas SIDI'),
 'uswe':       dict(disp='USWE',        namef='name',  fslug='uswe',          tprefix=lambda p:(p.get('catlabel') or 'Mochila')+' USWE'),
 'giantloop':  dict(disp='Giant Loop',  namef='model', fslug='giant-loop',    tprefix=lambda p:'Giant Loop'),
 'lucioli':    dict(disp='Lucioli',     namef='model', fslug='lucioli',       tprefix=lambda p:'Lucioli'),
 'nitromousse':dict(disp='Nitro Mousse',namef='model', fslug='nitro-mousse',  tprefix=lambda p:'Nitro Mousse'),
}

def bake(t, _id, content):
    return re.sub(r'(id="'+_id+r'"[^>]*>)(</[a-zA-Z0-9]+>)',
                  lambda m: m.group(1)+content+m.group(2), t, count=1)

def build_brand(b):
    cfg = CFG[b]; bd = ROOT/'marcas'/b
    src = (bd/'producto.html').read_text(encoding='utf-8')
    # patch template: FORCE_ID + guard del title (idempotente)
    if 'window.FORCE_ID' not in src:
        src = src.replace("params.get('id')", "(window.FORCE_ID||params.get('id'))", 1)
        src = src.replace("document.title =", "if(!window.FORCE_ID) document.title =", 1)
        (bd/'producto.html').write_text(src, encoding='utf-8')
    P = json.loads(re.search(r'const PRODUCTS\s*=\s*(\{.*?\});', src, re.S).group(1))
    mp = {}; idx = []
    for pid, p in P.items():
        name = str(p.get(cfg['namef']) or p.get('name') or p.get('model') or pid)
        title = f"{cfg['tprefix'](p)} {name} | Radsport Geist"
        fname = f"{cfg['fslug']}-{slug(name)}.html"
        kicker = p.get('kicker') or p.get('catlabel') or ''
        dl = desclist(p.get('desc') or [])
        tagtxt = striptags(p.get('tag') or (striptags(dl[0]) if dl else ''))
        meta = (f"{cfg['disp']} {name}. {tagtxt} Radsport Geist, importador oficial en Argentina.").strip()
        meta = re.sub(r'\s+',' ', meta)[:300]
        t = src
        t = re.sub(r'<title>.*?</title>', '<title>'+esc(title)+'</title>', t, count=1, flags=re.S)
        head = ('\n    <meta name="description" content="'+esc(meta)+'">'
                '\n    <link rel="canonical" href="'+SITEM+b+'/'+fname+'">'
                '\n    <meta property="og:title" content="'+esc(title)+'">'
                '\n    <meta property="og:description" content="'+esc(meta)+'">'
                '\n    <meta property="og:type" content="product">'
                '\n    <script>window.FORCE_ID="'+esc(pid)+'";</script>')
        t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+head, 1)
        # hornear texto para no-JS
        t = bake(t, 'pTitle', esc(name))
        t = bake(t, 'bcName', esc(name))
        if kicker: t = bake(t, 'pKicker', esc(kicker))
        if dl: t = bake(t, 'pDesc', "".join('<p>'+d+'</p>' for d in dl))
        (bd/fname).write_text(t, encoding='utf-8')
        mp[pid] = fname
        idx.append(dict(id=pid, file=fname, name=name, title=title, kicker=kicker))
    json.dump(mp, open(ROOT/'_build'/f'static_map_{b}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(idx, open(ROOT/'_build'/f'static_idx_{b}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
    return mp

if __name__ == '__main__':
    import sys
    brands = sys.argv[1:] or list(CFG)
    total = 0
    for b in brands:
        mp = build_brand(b); total += len(mp)
        print(f"{b}: {len(mp)} fichas -> ej. {list(mp.values())[0]}")
    print("TOTAL:", total)
