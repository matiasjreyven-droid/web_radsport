# -*- coding: utf-8 -*-
"""Fase 4: a TODAS las fichas de producto les agrega (si falta) meta description,
canonical, OG, y JSON-LD de Producto. Enumera marcas/*/*.html excluyendo
landing ({brand}.html), productos.html y producto.html."""
import re, json, glob, html
from pathlib import Path
ROOT = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web")
SITE = "https://radsport.com.ar/"
DISP = {'leovince':'LeoVince','cst':'CST','shot':'SHOT','nils':'NILS','sidi':'SIDI',
        'uswe':'USWE','giantloop':'Giant Loop','lucioli':'Lucioli','nitromousse':'Nitro Mousse','wrp':'WRP'}
def esc(s): return html.escape(str(s or ''), quote=True)
def striptags(s): return re.sub(r'\s+',' ', re.sub(r'<[^>]+>','', s or '')).strip()

fichas=[]
for f in glob.glob(str(ROOT/'marcas'/'*'/'*.html')):
    p=Path(f); brand=p.parent.name; base=p.name
    if base in ('productos.html','producto.html',f'{brand}.html'): continue
    if '_' in p.parts[-2] or p.parts[-2]=='_build': continue
    fichas.append((p,brand))

done=0; added_meta=0; added_jsonld=0
for p,brand in fichas:
    t=p.read_text(encoding='utf-8'); orig=t
    rel=str(p.relative_to(ROOT)).replace('\\','/')
    url=SITE+rel
    disp=DISP.get(brand,brand)
    head=t.split('</head>')[0]
    # name: primer <h1>
    h1=re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    name=striptags(h1.group(1)) if h1 else ''
    if not name:
        tm=re.search(r'<title>(.*?)</title>', t, re.S)
        name=re.split(r'\s[|–-]\s', striptags(tm.group(1)))[0] if tm else disp
    # description
    dm=re.search(r'<meta name="description" content="([^"]*)"', head)
    if dm: desc=dm.group(1)
    else:
        pm=re.search(r'id="pDesc"[^>]*>(.*?)</div>', t, re.S) or re.search(r'<p>(.*?)</p>', t, re.S)
        desc=striptags(pm.group(1))[:200] if pm else f"{disp} {name}. Radsport Geist, importador oficial en Argentina."
    # image: mainImg con src real
    im=re.search(r'id="mainImg"[^>]*src="([^"]+)"', t)
    img=None
    if im and im.group(1).strip():
        src=im.group(1).strip()
        img=src if src.startswith('http') else SITE+'/'.join(rel.split('/')[:-1])+'/'+src
    # inserciones en <head> (si faltan)
    ins=''
    if '<meta name="description"' not in head:
        ins+='\n    <meta name="description" content="'+esc(desc)+'">'; added_meta+=1
    if '<link rel="canonical"' not in head:
        ins+='\n    <link rel="canonical" href="'+esc(url)+'">'
    if 'property="og:title"' not in head:
        tm=re.search(r'<title>(.*?)</title>',t,re.S); ogt=striptags(tm.group(1)) if tm else name
        ins+='\n    <meta property="og:title" content="'+esc(ogt)+'">\n    <meta property="og:description" content="'+esc(desc)+'">\n    <meta property="og:type" content="product">'
        if img: ins+='\n    <meta property="og:image" content="'+esc(img)+'">'
    if ins:
        t=t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+ins,1)
    # JSON-LD Product
    if 'application/ld+json' not in t:
        ld={"@context":"https://schema.org/","@type":"Product","name":name,
            "brand":{"@type":"Brand","name":disp},"description":desc,"url":url}
        if img: ld["image"]=img
        block='\n    <script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'
        t=t.replace('</head>', block+'</head>',1); added_jsonld+=1
    if t!=orig:
        p.write_text(t,encoding='utf-8'); done+=1

print(f"fichas procesadas: {len(fichas)} | modificadas: {done} | meta agregadas: {added_meta} | JSON-LD agregados: {added_jsonld}")
