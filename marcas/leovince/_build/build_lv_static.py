# -*- coding: utf-8 -*-
import re, json, sys, unicodedata, html
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web\marcas\leovince")
SITE = "https://radsport.com.ar/marcas/leovince/"
src = (BASE/'producto.html').read_text(encoding='utf-8')
def getobj(n): return json.loads(re.search(r'const '+n+r'\s*=\s*(\{.*?\});',src,re.S).group(1))
PRODUCTS=getobj('PRODUCTS'); GROUPS=getobj('GROUPS'); CODE2GROUP=getobj('CODE2GROUP')
def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'[^\w\s-]','',s); return re.sub(r'[\s_]+','-',s).strip('-')
def esc(s): return html.escape(s or '', quote=True)
ACC=['colector','tubo supresor','db killer','proteccion','protección','carbono']
def is_acc(name): nl=name.lower(); return any(k in nl for k in ACC)

# 1) calcular datos + nombres base (para dedupe)
items=[]
for code in PRODUCTS:
    g=GROUPS[CODE2GROUP[code]]; name=g['n']; mat=g['mat']
    motos=[m for m in g['motos'] if m[3]==code] or g['motos']
    acc=is_acc(name)
    if motos and not acc:
        b0,m0=motos[0][0],motos[0][1]
        base='escape-leovince-'+slug(name)+('-'+slug(mat) if mat else '')+'-'+slug(b0+' '+m0)
    else:
        base='leovince-'+slug(name)+('-'+slug(mat) if mat else '')
    items.append(dict(code=code,g=g,name=name,mat=mat,motos=motos,acc=acc,base=base))
from collections import Counter
cnt=Counter(i['base'] for i in items)
for i in items:
    i['file']=(i['base']+('-'+i['code'].lower() if cnt[i['base']]>1 else ''))+'.html'

def build(i):
    code,g,name,mat,motos,acc=i['code'],i['g'],i['name'],i['mat'],i['motos'],i['acc']
    fname=i['file']
    motos_txt=", ".join(f"{m[0]} {m[1]}" for m in motos[:4])
    if motos and not acc:
        b0,m0=motos[0][0],motos[0][1]
        title=f"Escape LeoVince {name} para {b0} {m0} | Radsport Geist"
    else:
        title=f"{name} LeoVince{(' '+mat) if mat else ''} | Radsport Geist"
    meta=(f"{'Escape ' if (motos and not acc) else ''}LeoVince {name} {mat} "
          f"{'para '+motos_txt if motos else ''}. {g['desc'][0]} Radsport Geist, importador oficial en Argentina.")[:300]
    byb={}; 
    for m in motos: byb.setdefault(m[0],[]).append(m)
    fit=""
    for br,ms in byb.items():
        fit+=f'<div class="fit-brand"><h3>{esc(br)}</h3><div class="fit-grid">'
        for m in ms: fit+=f'<div class="fit-item"><span>{esc(m[1])}</span><span class="fit-meta">{esc(m[2])}</span></div>'
        fit+='</div></div>'
    deschtml="".join(f"<p>{esc(p)}</p>" for p in g['desc'])
    t=src
    t=re.sub(r'<title>.*?</title>','<title>'+esc(title)+'</title>',t,count=1,flags=re.S)
    head=('\n    <meta name="description" content="'+esc(meta)+'">'
          '\n    <link rel="canonical" href="'+SITE+fname+'">'
          '\n    <meta property="og:title" content="'+esc(title)+'">'
          '\n    <meta property="og:description" content="'+esc(meta)+'">'
          '\n    <meta property="og:type" content="product">'
          '\n    <script>window.LV_FORCE_CODE="'+code+'";</script>')
    t=t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+head,1)
    t=t.replace('<div class="product-kicker" id="pKicker"></div>','<div class="product-kicker" id="pKicker">Escape Leo Vince</div>',1)
    t=t.replace('<h1 class="product-title" id="pTitle"></h1>','<h1 class="product-title" id="pTitle">'+esc(name)+'</h1>',1)
    t=t.replace('<p class="product-tagline" id="pTag"></p>','<p class="product-tagline" id="pTag">'+esc(mat)+'</p>',1)
    t=t.replace('<div id="pDesc"></div>','<div id="pDesc">'+deschtml+'</div>',1)
    t=t.replace('<div id="fitList"></div>','<div id="fitList">'+fit+'</div>',1)
    (BASE/fname).write_text(t,encoding='utf-8')
    return dict(code=code,file=fname,name=name,mat=mat,motos=[[m[0],m[1],m[2]] for m in motos],title=title)

res=[build(i) for i in items]
json.dump({r['code']:r['file'] for r in res}, open('lv_static_map.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(res, open('lv_static_index.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print("generadas",len(res),"fichas estaticas")
print("ejemplos:");  [print("  ",r['file']) for r in res[:4]]
