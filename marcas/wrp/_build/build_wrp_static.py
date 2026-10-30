# -*- coding: utf-8 -*-
"""Fichas estaticas SEO para WRP (pastillas de freno). Una por codigo de pastilla,
con motos compatibles + equivalencias (SBS/Brembo/EBC/Ferodo/AP) horneadas."""
import re, json, html, unicodedata
from pathlib import Path
BASE = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web\marcas\wrp")
SITE = "https://radsport.com.ar/marcas/wrp/"
src = (BASE/'producto.html').read_text(encoding='utf-8')
PADS = json.loads(re.search(r'const PADS\s*=\s*(\{.*?\});', src, re.S).group(1))
def slug(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    s = re.sub(r'[^\w\s-]','',s); return re.sub(r'[\s_]+','-',s).strip('-')
def esc(s): return html.escape(str(s or ''), quote=True)
def pos_es(p): return 'Delantera' if re.match(r'^front', str(p), re.I) else 'Trasera'

# patch template: FORCE_CODE + guard + map script (idempotente)
if 'window.FORCE_CODE' not in src:
    src = src.replace("const code = new URLSearchParams(location.search).get('code');",
                      "const code = window.FORCE_CODE || new URLSearchParams(location.search).get('code');", 1)
    src = src.replace("document.title = realCode", "if(!window.FORCE_CODE) document.title = realCode", 1)
    src = src.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <script src="wrp_static_map.js"></script>', 1)
    (BASE/'producto.html').write_text(src, encoding='utf-8')

def bake(t, _id, content):
    return re.sub(r'(id="'+_id+r'"[^>]*>)(</[a-zA-Z0-9]+>)',
                  lambda m: m.group(1)+content+m.group(2), t, count=1)

mp = {}; idx = []
for code, p in PADS.items():
    cat, mat, use = p.get('c',''), p.get('mat',''), p.get('u','')
    fits = p.get('fits', []); eq = p.get('eq', {})
    fname = 'pastilla-wrp-'+slug(code)+'.html'
    title = f"Pastilla de freno WRP {code} – {cat} {mat} | Radsport Geist"
    motos_txt = ", ".join(sorted(set(f"{f[0]} {f[1]}" for f in fits))[:4])
    eq_txt = ", ".join(f"{k} {v}" for k,v in eq.items())
    meta = (f"Pastilla de freno WRP {code} ({cat}, {mat}, {use}). "
            f"{'Para '+motos_txt+'. ' if motos_txt else ''}{'Equivale a '+eq_txt+'. ' if eq_txt else ''}"
            f"Radsport Geist, importador oficial en Argentina.")
    meta = re.sub(r'\s+',' ', meta)[:300]
    # fits baked
    byb = {}
    for f in fits: byb.setdefault(f[0], []).append(f)
    fit = ""
    for br, ms in byb.items():
        fit += '<div class="fit-brand"><h3>'+esc(br)+'</h3><div class="fit-grid">'
        for f in ms: fit += '<div class="fit-item"><span>'+esc(f[1])+'</span><span class="fit-meta">'+esc(f[2] if len(f)>2 else '')+'</span></div>'
        fit += '</div></div>'
    equiv = ('<p><strong>Equivalencias:</strong> '+esc(eq_txt)+'.</p>') if eq_txt else ''
    t = src
    t = re.sub(r'<title>.*?</title>', '<title>'+esc(title)+'</title>', t, count=1, flags=re.S)
    head = ('\n    <meta name="description" content="'+esc(meta)+'">'
            '\n    <link rel="canonical" href="'+SITE+fname+'">'
            '\n    <meta property="og:title" content="'+esc(title)+'">'
            '\n    <meta property="og:description" content="'+esc(meta)+'">'
            '\n    <meta property="og:type" content="product">'
            '\n    <script>window.FORCE_CODE="'+esc(code)+'";</script>')
    t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+head, 1)
    t = bake(t, 'pTitle', esc(code))
    t = bake(t, 'bcName', esc(code))
    t = bake(t, 'pKicker', 'Pastilla de freno · '+pos_es(p.get('p','')))
    t = bake(t, 'pDesc', '<p><em>'+esc(cat)+' ('+esc(mat)+')</em>. '+esc(p.get('d',''))+'</p>')
    t = bake(t, 'fitList', fit or '<p>Consultá compatibilidad.</p>')
    t = bake(t, 'equivBlock', equiv)
    (BASE/fname).write_text(t, encoding='utf-8')
    mp[code] = fname
    idx.append(dict(code=code, file=fname, cat=cat, mat=mat, motos=motos_txt))

open(BASE/'wrp_static_map.js','w',encoding='utf-8').write('window.WRP_STATIC = '+json.dumps(mp, ensure_ascii=False)+';\n')
json.dump(idx, open(BASE/'_build'/'wrp_static_idx.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('WRP: generadas', len(mp), 'fichas | ej.', list(mp.values())[0])
