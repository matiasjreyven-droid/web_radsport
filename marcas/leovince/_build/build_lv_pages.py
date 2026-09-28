# -*- coding: utf-8 -*-
import json, re, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web\marcas\leovince")
data = json.load(open('lv_data.json', encoding='utf-8'))
products, motos = data['products'], data['motos']

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
    s = re.sub(r'[^\w\s-]','',s); s = re.sub(r'[\s_]+','-',s).strip('-'); return s

LINE_DESC = {
 'LV One Evo': 'Slip-on homologado de acero, el equilibrio perfecto entre sonido deportivo, estética y prestaciones para uso diario y ruta.',
 'LV One Evo Black Edition': 'La versión Black Edition del LV One Evo: acabado negro total, sonido profundo y look agresivo, homologado.',
 'LV-10': 'Slip-on de inspiración racing, liviano y compacto, con un sonido lleno y una estética inconfundible.',
 'LV-10 Black': 'El LV-10 en acabado negro: el mismo espíritu racing con un look más oscuro y agresivo.',
 'LV-14': 'Slip-on de perfil deportivo, sonido potente y construcción liviana para el uso más exigente.',
 'LV-14 Black Edition': 'El LV-14 en acabado negro total: máxima presencia y sonido racing.',
 'LV-X Evo': 'Slip-on de diseño moderno y compacto, ideal para maxi-enduro y trail, con gran sonido y peso reducido.',
 'LV-X': 'Slip-on compacto de estética moderna, pensado para adventure y trail.',
 'LV Corsa': 'Silenciador de competición con el ADN racing de Leo Vince: máximo rendimiento y sonido.',
 'LV Pro': 'Línea Pro de altas prestaciones, construcción premium y sonido racing.',
 'GP Corsa Evo': 'Silenciador GP de competición, mínimo peso y máxima performance en pista.',
 'GP One': 'Silenciador GP de estilo racing, liviano y con sonido agresivo.',
 'Classic Racer': 'Silenciador de estética café-racer / clásica, con el sonido característico Leo Vince.',
 'Classic Racer Black Edition': 'Classic Racer en acabado negro: estética retro con presencia moderna.',
 'Nero': 'Slip-on de línea Nero, acabado oscuro y sonido deportivo.',
 'Tubo supresor de catalizador': 'Tubo de-cat que reemplaza el catalizador para liberar flujo y sonido (uso en pista).',
 'Colector': 'Colector de escape de alto flujo para completar tu sistema Leo Vince.',
 'Protección carbono': 'Protección de carbono para el silenciador, suma estética y resistencia al calor.',
 'LV 10 db killer': 'DB killer para la línea LV-10, regula el nivel de sonido.',
 'LV-12 R Black Edition': 'Slip-on LV-12 R en acabado negro: perfil racing y sonido pleno.',
 'Sistema completo - LV One Evo': 'Sistema completo LV One Evo (colector + silenciador): máxima ganancia de prestaciones y sonido.',
}
def describe(name, material):
    base = LINE_DESC.get(name, 'Escape Leo Vince fabricado en Italia, con materiales de primera calidad para mejorar sonido, estética y prestaciones.')
    mat = (' Acabado en ' + material.lower() + '.') if material else ''
    return [base + mat, 'Diseñado y fabricado en Italia. Consultá la homologación y la compatibilidad exacta para tu moto en la ficha oficial.']

# ---- GRUPOS (para la grilla) + CODE2GROUP ----
groups = {}; code2group = {}
for code, p in products.items():
    key = slug(p['name'] + ('-' + p['material'] if p['material'] else ''))
    code2group[code] = key
    g = groups.setdefault(key, dict(n=p['name'], mat=p['material'], mcat=p['material_cat'],
                                    main=None, ph=[], motos=[], o=p['order']))
    g['o'] = min(g['o'], p['order'])
    if not g['ph'] and p['has_photo']:      # foto representativa del grupo = studio/producto (SIN bike)
        g['ph'] = p['photos']; g['main'] = p['main']
    for m in p['motos']:
        g['motos'].append([m['brand'], m['model'], m['anios'], code, p['url']])
for g in groups.values():
    if not g['main']: g['main'] = '../../img/logos/leovince.png'
    g['desc'] = describe(g['n'], g['mat'])

# ---- PRODUCTS por código (foto propia) ----
PRODUCTS_JS = {}
for code, p in products.items():
    PRODUCTS_JS[code] = dict(g=code2group[code], hp=p['has_photo'], ph=p['photos'], mt=p['mounted'], url=p['url'])
GROUPS_JS = groups
CODE2GROUP_JS = code2group
MOTOS_JS = [dict(b=m['brand'], m=m['model'], an=m['anios'], c=m['code']) for m in motos]
print(f"Escapes: {len(products)} | Grupos: {len(groups)} | Motos: {len(MOTOS_JS)}")

# ================= 1) FICHA (producto.html) =================
prod = (BASE / 'producto.html').read_text(encoding='utf-8')
PAGEWRAP = '''    <div class="page-wrap">
        <div class="breadcrumb">
            <a href="../../index.html">Inicio</a> <span>&rsaquo;</span>
            <a href="../../productos.html">Productos</a> <span>&rsaquo;</span>
            <a href="productos.html">Leo Vince</a> <span>&rsaquo;</span>
            <span id="bcName">Escape</span>
        </div>
        <div class="product-hero">
            <div class="hero-left">
                <div class="product-gallery" id="gallery">
                    <div class="gallery-main" id="galleryMain">
                        <svg class="gallery-zoom-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                        <img id="mainImg" src="" alt="">
                    </div>
                    <div class="gallery-thumbs" id="galleryThumbs"></div>
                </div>
            </div>
            <div class="product-info-side">
                <div class="product-kicker" id="pKicker"></div>
                <h1 class="product-title" id="pTitle"></h1>
                <p class="product-tagline" id="pTag"></p>
                <div class="specs-table" id="specsTable"></div>
                <div class="product-description">
                    <div class="description-header">El escape</div>
                    <div id="pDesc"></div>
                </div>
            </div>
        </div>
        <section class="fitment">
            <h2 id="fitTitle">Motos compatibles</h2>
            <div id="fitList"></div>
        </section>
    </div>
'''
prod = re.sub(r'    <div class="page-wrap">.*?</div>\s*(?=<footer)', PAGEWRAP, prod, count=1, flags=re.DOTALL)
LV_CSS = '''        .hero-left { display:flex; flex-direction:column; }
        .gallery-main img { padding:0.35rem; }
        .gallery-main:hover img { padding:0; }
        .fitment { margin-top:2.5rem; }
        .fitment > h2 { font-size:1.2rem; font-weight:800; margin-bottom:1.4rem; color:var(--gray); }
        .fitment-note { font-size:0.8rem; font-weight:500; color:var(--brand-subtle); letter-spacing:0; text-transform:none; }
        .fit-brand { margin-bottom:1.4rem; }
        .fit-brand h3 { font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; color:var(--brand-accent); margin-bottom:0.7rem; border-bottom:1px solid #eee; padding-bottom:0.4rem; }
        .fit-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:0.5rem; }
        .fit-item { background:white; border:1px solid #ececec; border-radius:8px; padding:0.55rem 0.9rem; font-size:0.85rem; display:flex; justify-content:space-between; align-items:center; gap:0.6rem; }
        .fit-item.active { border-color:var(--brand-accent); box-shadow:0 0 0 1px var(--brand-accent); }
        a.fit-item { text-decoration:none; color:inherit; }
        .fit-clickable { cursor:pointer; transition:border-color 0.15s, box-shadow 0.15s; }
        .fit-clickable:hover { border-color:var(--brand-accent); box-shadow:0 2px 10px rgba(0,0,0,0.06); }
        .fit-meta { color:var(--brand-subtle); font-size:0.72rem; white-space:nowrap; display:flex; gap:0.5rem; align-items:center; }
        .fit-code { color:var(--brand-accent); text-decoration:none; font-weight:800; font-size:0.78rem; }
        .fit-code:hover { text-decoration:underline; }
'''
prod = re.sub(r'[ \t]*\.hero-left \{ display:flex;.*?(?=[ \t]*</style>)', '\n', prod, count=1, flags=re.DOTALL)
prod = prod.replace('</style>', LV_CSS + '</style>', 1)
PAD_SCRIPT = '''    <script>
        const PRODUCTS = ''' + json.dumps(PRODUCTS_JS, ensure_ascii=False) + ''';
        const GROUPS = ''' + json.dumps(GROUPS_JS, ensure_ascii=False) + ''';
        const CODE2GROUP = ''' + json.dumps(CODE2GROUP_JS, ensure_ascii=False) + ''';
        const params = new URLSearchParams(location.search);
        const code = params.get('code');
        let key = params.get('model');
        let escPhotos = null, mounted = [], url = '';
        if (code && PRODUCTS[code]) {
            const pr = PRODUCTS[code]; key = pr.g; url = pr.url;
            escPhotos = pr.hp ? pr.ph.slice() : null;   // escape solo (portada + ángulos)
            mounted = pr.mt ? pr.mt.slice() : [];       // escape puesto en la moto
        }
        if (!key || !GROUPS[key]) key = Object.keys(GROUPS)[0];
        const g = GROUPS[key];
        if (!escPhotos || !escPhotos.length) escPhotos = (g.ph && g.ph.length) ? g.ph.slice() : [g.main];
        const gallery = escPhotos.concat(mounted);   // galería: el escape primero, luego cómo queda instalado
        if (!url) { for (var i=0;i<g.motos.length;i++){ if(g.motos[i][4]){ url=g.motos[i][4]; break; } } }
        if (g) {
            document.title = g.n + ' | Leo Vince · Radsport Geist';
            document.getElementById('bcName').textContent = g.n + (g.mat ? ' · ' + g.mat : '');
            document.getElementById('pKicker').textContent = 'Escape Leo Vince';
            document.getElementById('pTitle').textContent = g.n;
            document.getElementById('pTag').textContent = g.mat || '';
            const img = document.getElementById('mainImg');
            img.src = gallery[0]; img.alt = 'Leo Vince ' + g.n;
            const tw = document.getElementById('galleryThumbs');
            if (gallery.length > 1) {
                tw.innerHTML = gallery.map(function(m,i){ return '<div class="gallery-thumb'+(i===0?' active':'')+'" data-src="'+m+'"><img src="'+m+'" alt=""></div>'; }).join('');
                const th = tw.querySelectorAll('.gallery-thumb');
                th.forEach(function(t){ t.addEventListener('click', function(){ img.src=t.dataset.src; th.forEach(function(x){x.classList.remove('active');}); t.classList.add('active'); }); });
            }
            const perCode = !!(code && PRODUCTS[code]);
            const specs = [['Línea', g.n]];
            if (g.mat) specs.push(['Material', g.mat]);
            if (perCode) specs.push(['Código', url ? '<a class="fit-code" href="'+url+'" target="_blank" rel="noopener">'+code+'</a>' : code]);
            specs.push(['Fabricación', 'Italia']);
            document.getElementById('specsTable').innerHTML = specs.map(function(s){
                return '<div class="specs-row"><span class="specs-key">'+s[0]+'</span><span class="specs-value">'+s[1]+'</span></div>'; }).join('');
            document.getElementById('pDesc').innerHTML = g.desc.map(function(x){ return '<p>'+x+'</p>'; }).join('');
            // Motos compatibles: por CÓDIGO (solo las que usan este escape) o, si venís del catálogo, por modelo
            const motosShow = perCode ? g.motos.filter(function(m){ return m[3] === code; }) : g.motos;
            const byBrand = {};
            motosShow.forEach(function(m){ (byBrand[m[0]] = byBrand[m[0]] || []).push(m); });
            let html = '';
            Object.keys(byBrand).forEach(function(br){
                html += '<div class="fit-brand"><h3>'+br+'</h3><div class="fit-grid">';
                byBrand[br].forEach(function(m){
                    if (perCode) {
                        var cls = mounted.length ? ' fit-clickable' : '';
                        html += '<div class="fit-item'+cls+'"><span>'+m[1]+'</span><span class="fit-meta">'+(m[2]||'')+'</span></div>';
                    } else {
                        // desde el catálogo: cada moto lleva a la ficha del escape exacto que le corresponde
                        html += '<a class="fit-item fit-clickable" href="producto.html?code='+encodeURIComponent(m[3])+'"><span>'+m[1]+'</span><span class="fit-meta">'+(m[2]?m[2]+' · ':'')+'<span class="fit-code">Ver escape &rsaquo;</span></span></a>';
                    }
                });
                html += '</div></div>';
            });
            document.getElementById('fitList').innerHTML = html;
            const fitTitleEl = document.getElementById('fitTitle');
            if (perCode) {
                fitTitleEl.innerHTML = mounted.length
                    ? 'Motos compatibles <span class="fitment-note">— tocá una para ver cómo queda instalado</span>'
                    : 'Motos compatibles';
                if (mounted.length) {
                    var mi = 0;
                    document.querySelectorAll('#fitList .fit-clickable').forEach(function(it){
                        it.addEventListener('click', function(){
                            img.src = mounted[mi % mounted.length]; mi++;
                            document.querySelectorAll('.fit-item.active').forEach(function(x){ x.classList.remove('active'); });
                            it.classList.add('active');
                            document.querySelectorAll('.gallery-thumb').forEach(function(t){ t.classList.toggle('active', t.dataset.src===img.src); });
                            document.getElementById('galleryMain').scrollIntoView({behavior:'smooth', block:'center'});
                        });
                    });
                }
            } else {
                fitTitleEl.innerHTML = 'Motos compatibles <span class="fitment-note">— elegí tu moto para ver su escape</span>';
            }
        }
        const galleryMain = document.getElementById('galleryMain');
        const mImg = document.getElementById('mainImg');
        if (galleryMain) {
            galleryMain.addEventListener('mousemove', function(e){ const r=galleryMain.getBoundingClientRect(); mImg.style.transformOrigin=((e.clientX-r.left)/r.width*100)+'% '+((e.clientY-r.top)/r.height*100)+'%'; });
            galleryMain.addEventListener('mouseleave', function(){ mImg.style.transformOrigin='center center'; });
        }
    </script>
'''
prod = re.sub(r'    <script>.*?</script>\n', PAD_SCRIPT, prod, count=1, flags=re.DOTALL)
(BASE / 'producto.html').write_text(prod, encoding='utf-8')
print("OK producto.html (ficha por código con foto propia) generado.")

# ================= 2) FINDER (productos.html) =================
cat = (BASE / 'productos.html').read_text(encoding='utf-8')
head, _, rest = cat.partition('</nav>')
_, _, tail = rest.partition('<footer')
tail = re.sub(r'<script>.*?</script>', '', tail, flags=re.DOTALL)

BRAND_BAR = '''
    <!-- BRAND BAR (filtros de marca Radsport) -->
    <div class="brand-bar">
        <a href="../../productos.html" class="brand-all" data-brand="todos" title="Catálogo Completo">Todos</a>
        <a href="../cst/productos.html" data-brand="cst" title="CST Tires"><img src="../../img/logos/cst.png" alt="CST"></a>
        <a href="#" class="active" data-brand="leovince" title="Leo Vince"><img src="../../img/logos/leovince.png" alt="Leo Vince"></a>
        <a href="../shot/productos.html" data-brand="shot" title="SHOT Race Gear"><img src="../../img/logos/shot.png" alt="SHOT"></a>
        <a href="../uswe/productos.html" data-brand="uswe" title="USWE"><img src="../../img/logos/uswe.png" alt="USWE"></a>
        <a href="../giantloop/productos.html" data-brand="giantloop" title="Giant Loop"><img src="../../img/logos/giantloop.png" alt="Giant Loop"></a>
        <a href="../nils/productos.html" data-brand="nils" title="NILS"><img src="../../img/logos/nils.png" alt="NILS"></a>
        <a href="../nitromousse/productos.html" data-brand="nitromousse" title="Nitro Mousse"><img src="../../img/logos/nitromousse.png" alt="Nitro Mousse"></a>
        <a href="../lucioli/productos.html" data-brand="lucioli" title="Lucioli"><img src="../../img/logos/lucioli.png" alt="Lucioli"></a>
        <a href="../wrp/productos.html" data-brand="wrp" title="WRP"><img src="../../img/logos/wrp.png" alt="WRP"></a>
        <a href="../sidi/productos.html" data-brand="sidi" title="SIDI"><img src="../../img/logos/sidi.png" alt="SIDI"></a>
    </div>
'''
FINDER_BODY = BRAND_BAR + '''
    <div class="finder">
        <div class="finder-head">
            <div class="finder-eyebrow">Leo Vince · Escapes</div>
            <h1 class="finder-h1">Encontrá tu escape</h1>
        </div>
        <div class="finder-tabs">
            <button class="finder-tab active" data-panel="moto">Tu Moto</button>
            <button class="finder-tab" data-panel="todos">Todos los productos</button>
        </div>
        <div class="panel active" id="panel-moto">
            <div class="finder-step-label">1 · Elegí la marca</div>
            <div class="combo" id="marcaCombo">
                <input type="text" class="combo-input" id="marcaInput" placeholder="Elegí o buscá la marca…" autocomplete="off">
                <div class="combo-list" id="marcaList"></div>
            </div>
            <div class="finder-step-label">2 · Elegí el modelo</div>
            <select class="model-select" id="modelSelect" disabled>
                <option value="">Primero elegí una marca</option>
            </select>
            <div class="finder-result" id="finderResult">
                <div class="result-hint">Seleccioná tu moto para ver los escapes que le corresponden.</div>
            </div>
        </div>
        <div class="panel" id="panel-todos">
            <div class="pad-search-wrap">
                <input type="text" id="prodSearch" class="pad-search" placeholder="Buscá por modelo de escape o moto…">
            </div>
            <div class="pad-filters" id="prodFilters">
                <button class="pad-filter active" data-f="todos">Todos</button>
                <button class="pad-filter" data-f="Inoxidable">Inoxidable</button>
                <button class="pad-filter" data-f="Negro">Negro</button>
                <button class="pad-filter" data-f="Carbono">Carbono</button>
            </div>
            <div class="pad-grid" id="prodGrid"></div>
            <div class="pad-noresults" id="prodNoResults" style="display:none">No encontramos escapes con ese criterio.</div>
            <div class="pad-pagination" id="prodPagination"></div>
        </div>
    </div>
'''
FINDER_CSS = '''        .finder { max-width:1100px; margin:0 auto; padding:2.5rem 2rem 3rem; }
        .finder-head { text-align:center; margin-bottom:2.5rem; }
        .finder-eyebrow { font-size:0.72rem; text-transform:uppercase; letter-spacing:3px; color:var(--brand-accent); font-weight:700; margin-bottom:0.6rem; }
        .finder-h1 { font-size:clamp(1.9rem,4vw,2.8rem); font-weight:900; color:var(--gray); letter-spacing:-0.02em; }
        .finder-tabs { display:flex; gap:0.6rem; justify-content:center; margin-bottom:2.8rem; }
        .finder-tab { padding:0.8rem 1.8rem; border:2px solid #e5e5e5; background:white; border-radius:50px; font-size:0.78rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; cursor:pointer; color:var(--brand-subtle); transition:all 0.2s; }
        .finder-tab:hover { border-color:var(--brand-accent); color:var(--brand-accent); }
        .finder-tab.active { background:var(--brand-accent); border-color:var(--brand-accent); color:white; }
        .panel { display:none; } .panel.active { display:block; }
        .finder-step-label { font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; color:var(--brand-accent); font-weight:700; margin-bottom:0.9rem; }
        .model-select { width:100%; max-width:440px; padding:0.8rem 1rem; border:1.5px solid #e0e0e0; border-radius:10px; font-size:0.95rem; font-family:inherit; color:var(--gray); margin-bottom:2.5rem; cursor:pointer; }
        .model-select:disabled { opacity:0.5; cursor:default; }
        .combo { position:relative; max-width:440px; margin-bottom:2.5rem; }
        .combo-input { width:100%; padding:0.8rem 1rem; border:1.5px solid #e0e0e0; border-radius:10px; font-size:0.95rem; font-family:inherit; color:var(--gray); outline:none; }
        .combo-input:focus { border-color:var(--brand-accent); }
        .combo-list { position:absolute; top:100%; left:0; right:0; background:white; border:1px solid #e5e5e5; border-radius:10px; box-shadow:0 8px 26px rgba(0,0,0,0.10); margin-top:5px; max-height:260px; overflow-y:auto; z-index:50; display:none; }
        .combo-list.open { display:block; }
        .combo-option { padding:0.65rem 1rem; font-size:0.9rem; cursor:pointer; color:var(--gray); }
        .combo-option:hover, .combo-option.active { background:var(--gray-light); color:var(--brand-accent); }
        .combo-empty { padding:0.7rem 1rem; color:var(--brand-subtle); font-size:0.85rem; }
        .finder-result { min-height:80px; }
        .result-hint { text-align:center; color:var(--brand-subtle); padding:2rem; font-size:0.95rem; border:2px dashed #ececec; border-radius:14px; }
        .result-title { font-size:1.05rem; font-weight:800; margin-bottom:1.3rem; color:var(--gray); }
        .result-title span { color:var(--brand-accent); }
        .prod-cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(190px,1fr)); gap:1.2rem; }
        .pad-search-wrap { max-width:560px; margin:0 auto 1.5rem; }
        .pad-search { width:100%; padding:0.8rem 1.2rem; border:1.5px solid #e0e0e0; border-radius:50px; font-size:0.9rem; font-family:inherit; color:var(--gray); outline:none; }
        .pad-search:focus { border-color:var(--brand-accent); }
        .pad-filters { display:flex; gap:0.5rem; justify-content:center; flex-wrap:wrap; margin-bottom:2rem; }
        .pad-filter { padding:0.5rem 1.1rem; border:1.5px solid #e5e5e5; background:white; border-radius:50px; font-size:0.72rem; font-weight:700; letter-spacing:0.6px; text-transform:uppercase; cursor:pointer; color:var(--brand-subtle); transition:all 0.2s; }
        .pad-filter:hover { border-color:var(--brand-accent); color:var(--brand-accent); }
        .pad-filter.active { background:var(--brand-accent); border-color:var(--brand-accent); color:white; }
        .pad-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:1.1rem; }
        .prod-gcard { background:white; border:1px solid #eaeaea; border-radius:14px; overflow:hidden; text-decoration:none; color:var(--gray); display:flex; flex-direction:column; transition:transform 0.2s, box-shadow 0.2s, border-color 0.2s; box-shadow:0 2px 12px rgba(0,0,0,0.03); }
        .prod-gcard:hover { border-color:var(--brand-accent); transform:translateY(-3px); box-shadow:0 10px 26px rgba(0,0,0,0.08); }
        .prod-gcard-img { background:#fafafa; aspect-ratio:1/1; display:flex; align-items:center; justify-content:center; padding:0.9rem; }
        .prod-gcard-img img { max-width:100%; max-height:100%; object-fit:contain; }
        .prod-gcard-body { padding:0.85rem 1rem 1rem; }
        .prod-gcard-line { font-size:0.66rem; text-transform:uppercase; letter-spacing:1.2px; color:var(--brand-accent); font-weight:700; }
        .prod-gcard-name { font-size:1rem; font-weight:900; margin:0.25rem 0 0.15rem; letter-spacing:-0.01em; }
        .prod-gcard-sub { font-size:0.78rem; color:var(--brand-subtle); line-height:1.4; }
        .pad-noresults { text-align:center; color:var(--brand-subtle); padding:2.5rem; font-size:0.95rem; }
        .pad-pagination { display:flex; gap:0.4rem; justify-content:center; flex-wrap:wrap; margin-top:2.5rem; }
        .pad-pagination button { min-width:38px; padding:0.5rem 0.8rem; border:1.5px solid #e5e5e5; background:white; border-radius:8px; font-size:0.82rem; font-weight:600; cursor:pointer; color:var(--gray); transition:all 0.2s; }
        .pad-pagination button:hover:not(:disabled) { border-color:var(--brand-accent); color:var(--brand-accent); }
        .pad-pagination button.active { background:var(--brand-accent); border-color:var(--brand-accent); color:white; }
        .pad-pagination button:disabled { opacity:0.4; cursor:default; }
        @media (max-width:900px){ .pad-grid{ grid-template-columns:repeat(3,1fr); } }
        @media (max-width:640px){ .pad-grid{ grid-template-columns:repeat(2,1fr); } }
        @media (max-width:420px){ .pad-grid{ grid-template-columns:1fr; } }
'''
FINDER_SCRIPT = '''    <script>
        const PRODUCTS = ''' + json.dumps(PRODUCTS_JS, ensure_ascii=False) + ''';
        const GROUPS = ''' + json.dumps(GROUPS_JS, ensure_ascii=False) + ''';
        const CODE2GROUP = ''' + json.dumps(CODE2GROUP_JS, ensure_ascii=False) + ''';
        const MOTOS = ''' + json.dumps(MOTOS_JS, ensure_ascii=False) + ''';

        function codePhoto(code){ var pr=PRODUCTS[code]; if(pr&&pr.hp&&pr.ph.length) return pr.ph[0]; return GROUPS[CODE2GROUP[code]].main; }
        function groupCard(key){
            const g = GROUPS[key];
            return '<a class="prod-gcard" href="producto.html?model='+encodeURIComponent(key)+'">' +
                     '<div class="prod-gcard-img"><img src="'+g.main+'" alt="Leo Vince '+g.n+'"></div>' +
                     '<div class="prod-gcard-body"><div class="prod-gcard-line">'+(g.mat||'Escape')+'</div>' +
                       '<div class="prod-gcard-name">'+g.n+'</div></div></a>';
        }
        function motoCard(code, anios){
            const g = GROUPS[CODE2GROUP[code]];
            return '<a class="prod-gcard" href="producto.html?code='+encodeURIComponent(code)+'">' +
                     '<div class="prod-gcard-img"><img src="'+codePhoto(code)+'" alt="Leo Vince '+g.n+'"></div>' +
                     '<div class="prod-gcard-body"><div class="prod-gcard-line">'+(g.mat||'Escape')+'</div>' +
                       '<div class="prod-gcard-name">'+g.n+'</div>' +
                       '<div class="prod-gcard-sub">Código '+code+(anios?' · '+anios:'')+'</div></div></a>';
        }

        // ===== TU MOTO =====
        const BRANDS = [];
        MOTOS.forEach(function(m){ if (BRANDS.indexOf(m.b) < 0) BRANDS.push(m.b); });
        BRANDS.sort();
        const modelSelect = document.getElementById('modelSelect');
        const finderResult = document.getElementById('finderResult');
        function selectMarca(brand){
            if (!brand){ modelSelect.disabled = true; modelSelect.innerHTML = '<option value="">Primero elegí una marca</option>';
                finderResult.innerHTML = '<div class="result-hint">Seleccioná tu moto para ver los escapes que le corresponden.</div>'; return; }
            const mods = [];
            MOTOS.forEach(function(m){ if (m.b === brand && mods.indexOf(m.m) < 0) mods.push(m.m); });
            modelSelect.disabled = false;
            modelSelect.innerHTML = '<option value="">Elegí tu modelo…</option>' + mods.map(function(mm){ return '<option value="'+mm.replace(/"/g,'&quot;')+'">'+mm+'</option>'; }).join('');
            modelSelect.dataset.brand = brand;
            finderResult.innerHTML = '<div class="result-hint">Elegí el modelo para ver los escapes.</div>';
        }
        modelSelect.addEventListener('change', function(){
            const brand = this.dataset.brand, model = this.value;
            if (!model){ finderResult.innerHTML = '<div class="result-hint">Elegí el modelo para ver los escapes.</div>'; return; }
            const seen = {}, cards = [];
            MOTOS.forEach(function(m){ if (m.b === brand && m.m === model && !seen[m.c]){ seen[m.c]=1; cards.push(motoCard(m.c, m.an)); } });
            finderResult.innerHTML = '<div class="result-title">Escapes para <span>'+brand+' '+model+'</span></div><div class="prod-cards">' + cards.join('') + '</div>';
        });
        (function(){
            const input = document.getElementById('marcaInput'); const list = document.getElementById('marcaList');
            let filtered = BRANDS.slice();
            function render(){ const f = input.value.trim().toLowerCase();
                filtered = BRANDS.filter(function(b){ return b.toLowerCase().indexOf(f) >= 0; });
                if (!filtered.length){ list.innerHTML = '<div class="combo-empty">Sin resultados</div>'; return; }
                list.innerHTML = filtered.map(function(b,i){ return '<div class="combo-option'+(i===0?' active':'')+'" data-v="'+b+'">'+b+'</div>'; }).join('');
                list.querySelectorAll('.combo-option').forEach(function(el){ el.addEventListener('mousedown', function(e){ e.preventDefault(); choose(el.dataset.v); }); }); }
            function choose(b){ input.value = b; list.classList.remove('open'); selectMarca(b); }
            input.addEventListener('focus', function(){ render(); list.classList.add('open'); });
            input.addEventListener('input', function(){ render(); list.classList.add('open'); selectMarca(''); });
            input.addEventListener('keydown', function(e){ if (e.key==='Enter'){ e.preventDefault(); if (filtered.length) choose(filtered[0]); } else if (e.key==='Escape'){ list.classList.remove('open'); input.blur(); } });
            document.addEventListener('click', function(e){ if (!e.target.closest('#marcaCombo')) list.classList.remove('open'); });
        })();

        // ===== TODOS LOS PRODUCTOS =====
        const allKeys = Object.keys(GROUPS).sort(function(a,b){ return GROUPS[a].o - GROUPS[b].o; });
        const prodGrid = document.getElementById('prodGrid'); const prodSearch = document.getElementById('prodSearch');
        const prodNoResults = document.getElementById('prodNoResults'); const prodPagination = document.getElementById('prodPagination');
        const PER_PAGE = 15; var prodState = { f:'todos', q:'' }, prodPage = 1;
        function groupSearchStr(key){ const g = GROUPS[key]; var m = g.motos.map(function(x){ return x[0]+' '+x[1]+' '+x[3]; }).join(' '); return (g.n+' '+g.mat+' '+m).toLowerCase(); }
        function renderProdPagination(totalPages){
            if (totalPages <= 1){ prodPagination.innerHTML=''; return; }
            var h = '<button data-p="'+(prodPage-1)+'"'+(prodPage===1?' disabled':'')+'>&larr;</button>';
            for (var i=1;i<=totalPages;i++){ h += '<button class="'+(i===prodPage?'active':'')+'" data-p="'+i+'">'+i+'</button>'; }
            h += '<button data-p="'+(prodPage+1)+'"'+(prodPage===totalPages?' disabled':'')+'>&rarr;</button>';
            prodPagination.innerHTML = h;
            prodPagination.querySelectorAll('button[data-p]').forEach(function(b){ b.addEventListener('click', function(){ var np=parseInt(b.dataset.p,10); if(np>=1&&np<=totalPages){ prodPage=np; renderProds(); window.scrollTo({top:document.querySelector('.finder-tabs').offsetTop-20,behavior:'smooth'}); } }); });
        }
        function renderProds(){
            const out = allKeys.filter(function(key){ const g = GROUPS[key]; var okF = prodState.f==='todos' || g.mcat===prodState.f; var okQ = !prodState.q || groupSearchStr(key).indexOf(prodState.q) >= 0; return okF && okQ; });
            const totalPages = Math.max(1, Math.ceil(out.length / PER_PAGE));
            if (prodPage > totalPages) prodPage = totalPages;
            const start = (prodPage-1)*PER_PAGE;
            prodGrid.innerHTML = out.slice(start, start+PER_PAGE).map(groupCard).join('');
            prodNoResults.style.display = out.length ? 'none' : '';
            renderProdPagination(totalPages);
        }
        document.getElementById('prodFilters').querySelectorAll('.pad-filter').forEach(function(b){ b.addEventListener('click', function(){ document.querySelectorAll('#prodFilters .pad-filter').forEach(function(x){x.classList.remove('active');}); b.classList.add('active'); prodState.f=b.dataset.f; prodPage=1; renderProds(); }); });
        prodSearch.addEventListener('input', function(){ prodState.q=this.value.trim().toLowerCase(); prodPage=1; renderProds(); });
        renderProds();

        document.querySelectorAll('.finder-tab').forEach(function(tab){ tab.addEventListener('click', function(){
            document.querySelectorAll('.finder-tab').forEach(function(t){ t.classList.remove('active'); });
            document.querySelectorAll('.panel').forEach(function(pp){ pp.classList.remove('active'); });
            tab.classList.add('active'); document.getElementById('panel-' + tab.dataset.panel).classList.add('active'); }); });
    </script>
'''
head = re.sub(r'[ \t]*\.finder \{ max-width:1100px;.*?(?=[ \t]*</style>)', '\n', head, count=1, flags=re.DOTALL)
head = head.replace('</style>', FINDER_CSS + '</style>', 1)
tail = tail.replace('</body>', FINDER_SCRIPT + '\n</body>')
cat = head + '</nav>\n' + FINDER_BODY + '\n    <footer' + tail
cat = re.sub(r'<title>.*?</title>', '<title>Escapes Leo Vince — Radsport Geist</title>', cat, count=1)
(BASE / 'productos.html').write_text(cat, encoding='utf-8')
print("OK productos.html (finder, Tu Moto -> ?code) generado.")
