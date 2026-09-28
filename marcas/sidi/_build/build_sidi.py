# -*- coding: utf-8 -*-
import openpyxl, json, re, sys, os, unicodedata
from pathlib import Path
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web\marcas\sidi")
PRODdir = BASE / 'productos'
def clean(v): return str(v).strip() if v is not None else ""
def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\([^)]*\)','',s); s=re.sub(r'[^\w\s/-]','',s); s=re.sub(r'[\s/_]+','-',s).strip('-'); s=re.sub(r'-+','-',s); return s

photomap = json.load(open('sidi_photomap.json', encoding='utf-8'))
def color_tokens(s):
    s = s.replace('grey', 'gray')
    return set(t for t in re.split(r'[^a-z0-9]+', s.lower()) if t)
photos_by_model = defaultdict(list)   # mslug -> [(tokenset, filename)]
for key, fn in photomap.items():
    ms, cs = key.split('|', 1)
    photos_by_model[ms].append((color_tokens(cs), fn))
def photo_for(model, color):
    ctok = color_tokens(slug(color))
    ms = slug(model)
    cands = photos_by_model.get(ms) or photos_by_model.get(re.sub(r'-?wom[ae]n$', '', ms))
    if not cands: return None
    best, bs = None, 0.0
    for tok, fn in cands:
        inter = len(ctok & tok); union = len(ctok | tok) or 1
        sc = inter / union
        if sc > bs: bs, best = sc, fn
    return best if bs > 0 else None

# --- stock: base -> {talles disponibles} ---
wb = openpyxl.load_workbook('stock.xlsx', data_only=True); ws = wb['Stock']; hdr=[str(c.value) for c in ws[1]]
ci=hdr.index('Código Interno'); di=hdr.index('Disponible'); mi=hdr.index('Marca'); ti=hdr.index('Talle')
stock = defaultdict(int); talles = defaultdict(set)
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r[ci] or clean(r[mi]).lower()!='sidi': continue
    base = re.sub(r'-\d+(?:\.\d+)?$','',clean(r[ci]))
    try: disp = int(r[di] or 0)
    except: disp = 0
    stock[base]+=disp
    if disp>0 and r[ti] not in (None,''): talles[base].add(str(r[ti]).strip())
def sort_talles(ts):
    def k(x):
        try: return float(x)
        except: return 999
    return sorted(ts, key=k)

CATLABEL = {'off-road':'Off Road','touring':'Touring','mtb':'MTB','gravel':'Gravel','ruta':'Ruta','on-road':'On Road'}
APTO2CAT = {'off road':'off-road','touring':'touring','mtb':'mtb','gravel':'gravel','ruta':'ruta','on road':'on-road'}

def describe(name, seg, catlabel):
    if seg=='moto':
        return [f"La <em>{name}</em> es una bota de moto Sidi, fabricada en Italia con la calidad y protección que distinguen a la marca ({catlabel}).",
                "Construcción robusta, hebillas regulables y suela de alto agarre para máximo control y durabilidad."]
    return [f"La <em>{name}</em> es una zapatilla de ciclismo Sidi ({catlabel}), fabricada en Italia con el ajuste preciso y la transferencia de potencia que caracterizan a la marca.",
            "Cierre de precisión, suela rígida y materiales premium para pedalear con la máxima eficiencia."]

# --- precios (secciones) + filtro por stock ---
wb = openpyxl.load_workbook('sidi_precios.xlsx', data_only=True); ws = wb['Precios']
seg='moto'; prods={}; order=0; sinfoto=[]
for r in ws.iter_rows(min_row=7, values_only=True):
    c0=clean(r[0])
    if 'bici' in c0.lower(): seg='bici'; continue
    if 'moto' in c0.lower() and not r[2]: seg='moto'; continue
    if not r[2]: continue
    cod=clean(r[2])
    if stock.get(cod,0)<=0: continue
    model=clean(r[3]); color=clean(r[4]); apto=clean(r[7])
    vid=slug(model)
    catk=APTO2CAT.get(apto.lower(), 'ruta' if seg=='bici' else 'off-road')
    if vid not in prods:
        order+=1
        prods[vid]=dict(name=model, seg=seg, cat=catk, catlabel=CATLABEL.get(catk,apto),
                        apto=apto, colors=[], order=order, desc=describe(model,seg,CATLABEL.get(catk,apto)))
    ph=photo_for(model,color)
    if not ph: sinfoto.append((model,color))
    prods[vid]['colors'].append(dict(color=color, cod=cod, photo=ph,
                                     talles=sort_talles(talles.get(cod,set())), has=bool(ph)))

# fallback de foto: si un color no tiene, usar la 1ra del modelo que tenga; sino logo
for p in prods.values():
    first = next((c['photo'] for c in p['colors'] if c['photo']), None)
    for c in p['colors']:
        if not c['photo']:
            c['photo'] = first
        c['img'] = ('productos/'+c['photo']) if c['photo'] else '../../img/logos/sidi.png'

json.dump(prods, open('sidi_data.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(f"Modelos en stock: {len(prods)} | variantes: {sum(len(p['colors']) for p in prods.values())} | sin foto propia: {len(sinfoto)}")
print("Categorias:", dict(Counter(p['cat'] for p in prods.values())))
print("Sin foto propia:", sinfoto)

# =============== CATALOGO (productos.html) ===============
cat = (BASE/'productos.html').read_text(encoding='utf-8')
CAT_ORDER=['off-road','touring','on-road','mtb','gravel','ruta']
plist=sorted(prods.items(), key=lambda kv:(kv[1]['seg']!='moto', CAT_ORDER.index(kv[1]['cat']) if kv[1]['cat'] in CAT_ORDER else 9, kv[1]['order']))
cards=[]
for vid,p in plist:
    c0=p['colors'][0]
    thumbs="".join(f'<img src="{c["img"]}" alt="{p["name"]} {c["color"]}" title="{c["color"]}">' for c in p['colors'][1:])
    tb=f'\n                <div class="product-card-color-thumbs">{thumbs}</div>' if thumbs else ''
    name_search=f"{p['name']} {' '.join(c['color'] for c in p['colors'])} {p['catlabel']}".lower()
    cards.append(f'''        <a href="producto.html?id={vid}" class="product-card" data-category="{p['cat']}" data-segment="{p['seg']}" data-name="{name_search}">
            <div class="product-card-img"><img src="{c0['img']}" alt="Sidi {p['name']} {c0['color']}" loading="lazy"></div>
            <div class="product-card-body">
                <div class="product-card-category">{p['catlabel']}</div>
                <h3>{p['name']}</h3>{tb}
            </div>
        </a>''')
grid='<div class="products-grid" id="productsGrid">\n\n'+"\n\n".join(cards)+'\n\n        <div class="no-results" id="noResults">No hay productos en esta categoría.</div>\n    </div>'
cat=re.sub(r'<div class="products-grid" id="productsGrid">.*?<div class="no-results"[^>]*>[^<]*</div>\s*</div>', grid, cat, count=1, flags=re.DOTALL)
# filtros presentes
cats_present=[c for c in CAT_ORDER if any(p['cat']==c for p in prods.values())]
fbtns='    <div class="filters" id="filters">\n        <button class="filter-btn active" data-filter="todos">Todos</button>\n'+ \
      "\n".join(f'        <button class="filter-btn" data-filter="{c}">{CATLABEL[c]}</button>' for c in cats_present)+'\n    </div>'
cat=re.sub(r'<div class="filters" id="filters">.*?</div>', fbtns.strip(), cat, count=1, flags=re.DOTALL)
# CSS de thumbs de color (idempotente)
if '.thumb-active {' not in cat:
    THUMB_CSS=('        .product-card-color-thumbs { display:flex; gap:0.4rem; margin-top:0.7rem; flex-wrap:wrap; align-items:center; }\n'
               '        .product-card-color-thumbs img { width:44px; height:44px; object-fit:contain; border-radius:6px; border:1px solid #e0e0e0; padding:3px; background:white; cursor:pointer; transition:border-color 0.15s, transform 0.15s; }\n'
               '        .product-card-color-thumbs img:hover { border-color:var(--brand-accent); transform:translateY(-1px); }\n'
               '        .thumb-active { border-color:var(--brand-accent); border-width:2px; padding:2px; }\n')
    cat=cat.replace('</style>', THUMB_CSS+'</style>', 1)
# JS: hover en thumb -> cambia imagen principal (inserta el color principal como 1er thumb)
if 'insertBefore(mainThumb' not in cat:
    SWAP_JS='''<script>
document.querySelectorAll('.product-card').forEach(function(card){
  var wrap=card.querySelector('.product-card-img'); if(!wrap) return;
  var mainImg=wrap.querySelector('img'); if(!mainImg) return;
  var thumbsWrap=card.querySelector('.product-card-color-thumbs'); if(!thumbsWrap) return;
  var defaultSrc=mainImg.getAttribute('src'), defaultAlt=mainImg.getAttribute('alt');
  var mainThumb=document.createElement('img'); mainThumb.src=defaultSrc; mainThumb.alt=defaultAlt; mainThumb.classList.add('thumb-active');
  thumbsWrap.insertBefore(mainThumb, thumbsWrap.firstChild);
  var thumbs=Array.prototype.slice.call(thumbsWrap.querySelectorAll('img'));
  if(thumbs.length<=1){ thumbsWrap.style.display='none'; return; }
  var activeThumb=thumbs[0];
  function swap(t){ if(mainImg.src!==t.src) mainImg.src=t.src; mainImg.alt=t.alt||defaultAlt; }
  function highlight(t){ thumbs.forEach(function(x){ x.classList.toggle('thumb-active', x===t); }); }
  thumbs.forEach(function(t){
    t.addEventListener('mouseenter', function(){ highlight(t); swap(t); });
    t.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); activeThumb=t; highlight(t); swap(t); });
  });
  thumbsWrap.addEventListener('mouseleave', function(){ highlight(activeThumb); swap(activeThumb); });
});
</script>'''
    cat=cat.replace('</body>', SWAP_JS+'\n</body>', 1)
(BASE/'productos.html').write_text(cat, encoding='utf-8')
print(f"OK productos.html: {len(cards)} cards | filtros: {cats_present}")

# =============== FICHA (producto.html) ===============
prod=(BASE/'producto.html').read_text(encoding='utf-8')
PAGEWRAP='''    <div class="page-wrap">
        <div class="breadcrumb">
            <a href="../../index.html">Inicio</a> <span>&rsaquo;</span>
            <a href="../../productos.html">Productos</a> <span>&rsaquo;</span>
            <a href="productos.html">SIDI</a> <span>&rsaquo;</span>
            <span id="bcName">Producto</span>
        </div>
        <div class="product-hero">
            <div class="product-gallery" id="gallery">
                <div class="gallery-main" id="galleryMain">
                    <svg class="gallery-zoom-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    <img id="mainImg" src="" alt="">
                </div>
                <div class="gallery-thumbs" id="galleryThumbs"></div>
            </div>
            <div class="product-info-side">
                <div class="product-kicker" id="pKicker"></div>
                <h1 class="product-title" id="pTitle"></h1>
                <div class="color-pick"><span class="color-pick-label">Color:</span> <span id="pColorName"></span></div>
                <div class="specs-table" id="specsTable"></div>
                <div class="product-description">
                    <div class="description-header">Descripción</div>
                    <div id="pDesc"></div>
                </div>
            </div>
        </div>
    </div>
'''
prod=re.sub(r'    <div class="page-wrap">.*?</div>\s*(?=<footer)', PAGEWRAP, prod, count=1, flags=re.DOTALL)
SIDI_CSS='''        .color-pick { font-size:0.85rem; color:var(--gray); margin-bottom:1.3rem; }
        .color-pick-label { font-weight:700; color:var(--brand-accent); text-transform:uppercase; letter-spacing:1px; font-size:0.7rem; }
        #pColorName { font-weight:600; }
        .talle-tags { display:flex; flex-wrap:wrap; gap:0.35rem; }
        .talle-tag { font-size:0.72rem; font-weight:600; border:1px solid #ddd; border-radius:5px; padding:0.15rem 0.5rem; color:var(--gray); }
'''
prod=re.sub(r'[ \t]*\.color-pick \{.*?(?=[ \t]*</style>)', '\n', prod, count=1, flags=re.DOTALL)
prod=prod.replace('</style>', SIDI_CSS+'</style>', 1)
PAD_SCRIPT='''    <script>
        const PRODUCTS = '''+json.dumps(prods, ensure_ascii=False)+''';
        const id = new URLSearchParams(location.search).get('id');
        const p = PRODUCTS[id] || PRODUCTS[Object.keys(PRODUCTS)[0]];
        const mainImg = document.getElementById('mainImg');
        function setColor(c){
            mainImg.src = c.img; mainImg.alt = 'Sidi ' + p.name + ' ' + c.color;
            document.getElementById('pColorName').textContent = c.color;
            document.getElementById('spColor').textContent = c.color;
            document.getElementById('spCod').textContent = c.cod;
        }
        if (p) {
            document.title = p.name + ' | SIDI · Radsport Geist';
            document.getElementById('bcName').textContent = p.name;
            document.getElementById('pKicker').textContent = (p.seg==='moto'?'Bota':'Zapatilla') + ' · ' + p.catlabel;
            document.getElementById('pTitle').textContent = p.name;
            const specs = [];
            specs.push(['Color', '<span id="spColor"></span>']);
            specs.push(['Código', '<span id="spCod"></span>']);
            if (p.apto) specs.push(['Disciplina', p.apto]);
            specs.push(['Fabricación', 'Italia']);
            document.getElementById('specsTable').innerHTML = specs.map(function(s){
                return '<div class="specs-row"><span class="specs-key">'+s[0]+'</span><span class="specs-value">'+s[1]+'</span></div>'; }).join('');
            document.getElementById('pDesc').innerHTML = p.desc.map(function(x){ return '<p>'+x+'</p>'; }).join('');
            const tw = document.getElementById('galleryThumbs');
            tw.innerHTML = p.colors.map(function(c,i){
                return '<div class="gallery-thumb'+(i===0?' active':'')+'" data-i="'+i+'" title="'+c.color+'"><img src="'+c.img+'" alt="'+c.color+'"></div>'; }).join('');
            const th = tw.querySelectorAll('.gallery-thumb');
            th.forEach(function(t){ t.addEventListener('click', function(){
                setColor(p.colors[parseInt(t.dataset.i,10)]);
                th.forEach(function(x){ x.classList.remove('active'); }); t.classList.add('active'); }); });
            setColor(p.colors[0]);
        }
        const galleryMain = document.getElementById('galleryMain');
        if (galleryMain) {
            galleryMain.addEventListener('mousemove', function(e){ const r=galleryMain.getBoundingClientRect(); mainImg.style.transformOrigin=((e.clientX-r.left)/r.width*100)+'% '+((e.clientY-r.top)/r.height*100)+'%'; });
            galleryMain.addEventListener('mouseleave', function(){ mainImg.style.transformOrigin='center center'; });
        }
    </script>
'''
prod=re.sub(r'    <script>.*?</script>\n', PAD_SCRIPT, prod, count=1, flags=re.DOTALL)
(BASE/'producto.html').write_text(prod, encoding='utf-8')
print("OK producto.html (ficha SIDI con selector de color + talles) generado.")
