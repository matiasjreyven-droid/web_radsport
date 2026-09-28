# -*- coding: utf-8 -*-
"""
Generador de fichas + tarjetas para NILS (Radsport Geist).
- Toma producto-fork.html como plantilla (head/style/nav/footer/script constantes).
- Genera producto-{slug}.html para cada producto de NUEVOS.
- Inserta las tarjetas en productos.html (agrupadas por categoria) y agrega el filtro 'mantenimiento'.
Reutilizable: agregar entradas a NUEVOS y correr de nuevo.
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\marcas\nils
def rd(f): return open(os.path.join(BASE,f),encoding='utf-8').read()
def wr(f,s): open(os.path.join(BASE,f),'w',encoding='utf-8').write(s)

CATLABEL = {'aceite-4t':'Aceite Motor 4T','aceite-2t':'Aceite Motor 2T','embrague':'Embrague',
 'cadena':'Cadena','freno':'Líq. Freno','amortiguador':'Suspensión','refrigerante':'Refrigerante',
 'transmision':'Transmisión','filtro-aire':'Filtro Aire','grasas':'Grasas / Limpieza',
 'mantenimiento':'Mantenimiento / Limpieza'}

# ---------- plantilla ----------
tpl = rd('producto-fork.html')
head_html = tpl[:tpl.index('<div class="page-wrap">')]      # <!DOCTYPE>..nav..brand-strip  (title se reemplaza)
footer_html = tpl[tpl.index('        <div class="related-section">'):]  # se corta antes de related; lo re-hacemos
FOOT = tpl[tpl.index('    <footer>'):]                       # footer + script + whatsapp + </body></html>

def set_title(h, t): return re.sub(r'<title>.*?</title>', '<title>'+t+'</title>', h, count=1, flags=re.DOTALL)

# ---------- registro de productos existentes (para 'productos relacionados') ----------
cat_html = rd('productos.html')
REG = {}
for m in re.finditer(r'<a href="(producto[^"]*)" class="product-card" data-category="([^"]*)"[^>]*>\s*<div class="product-card-img"><img src="([^"]*)" alt="([^"]*)"', cat_html, re.DOTALL):
    href, c, img, alt = m.groups()
    REG[alt] = dict(href=href, cat=c, img=img.replace('productos/',''), name=alt, cardcat=CATLABEL.get(c,c))

def P(*paras): return list(paras)

# ---------- datos de los 12 nuevos ----------
NUEVOS = [
 dict(slug='duo-synt-jet', name='Duo Synt Jet', cat='aceite-2t', img='NILS-DUO-SYNT-JET.jpg',
   kicker='Aceite Motor 2T · Inyección TPI', tagline='100% sintético PAO para motores 2T de inyección (TPI) de alta performance.',
   variants=['100% Sintético','Competición','Inyección TPI'],
   specs=[('Formulación','100% Sintético PAO competición'),('Aplicación','Motor 2T · Inyección (TPI)'),
          ('Especificación','Sistemas de inyección'),('Envase','1 L')],
   desc=P('<em>Duo Synt Jet</em> es un aceite 2T 100% sintético PAO diseñado específicamente para motores de inyección (TPI) de alta performance.',
          'Garantiza una lubricación limpia y estable, minimizando depósitos y humo, con excelente protección a alta temperatura.'),
   related=['Duo Synt','Duo Mix','Duo Synt R','Race']),
 dict(slug='duo-synt', name='Duo Synt', cat='aceite-2t', img='NILS-DUO-SYNT.jpg',
   kicker='Aceite Motor 2T', tagline='100% sintético PAO para motores 2T de alto rendimiento.',
   variants=['100% Sintético'],
   specs=[('Formulación','100% Sintético PAO'),('Aplicación','Motor 2T'),('Mezcla','Premezcla y bomba separada'),('Envase','1 L')],
   desc=P('<em>Duo Synt</em> es un aceite 2T 100% sintético PAO para motores de alto rendimiento, apto para premezcla y sistemas de bomba separada.',
          'Ofrece máxima protección antidesgaste, combustión limpia y bajo nivel de residuos.'),
   related=['Duo Synt Jet','Duo Mix','Duo Synt R','Sport']),
 dict(slug='duo-mix', name='Duo Mix', cat='aceite-2t', img='NILS-DUO-MIX.jpg',
   kicker='Aceite Motor 2T', tagline='Semi-sintético para motores 2T, uso general.',
   variants=['Semi-Sintético'],
   specs=[('Formulación','Semi Sintético'),('Aplicación','Motor 2T'),('Mezcla','Premezcla y bomba separada'),('Envase','1 L')],
   desc=P('<em>Duo Mix</em> es un aceite 2T semi-sintético para uso general en motores de dos tiempos.',
          'Buena protección y lubricación con combustión limpia, ideal para uso diario y recreativo.'),
   related=['Duo Synt','Duo Synt Jet','Duo Synt R','Sport']),
 dict(slug='hydraulic-command', name='Hydraulic Command', cat='embrague', img='NILS-HYDRAULIC-COMMAND.jpg',
   kicker='Embrague Hidráulico', tagline='Fluido mineral para embragues hidráulicos que piden aceite (no DOT).',
   variants=['Mineral','No DOT'],
   specs=[('Tipo','Fluido mineral'),('Aplicación','Embragues hidráulicos'),
          ('Característica','Estable en frío y calor · compatible con juntas'),('Envase','250 ml')],
   desc=P('<em>Hydraulic Command</em> es un fluido mineral formulado para embragues hidráulicos que requieren aceite mineral y no líquido DOT.',
          'Mantiene un accionamiento estable en frío y en caliente, con excelente compatibilidad con juntas y retenes.'),
   related=['Clutch','Clutch Trial','Nils Brake Fluid DOT 4 -1 Litro-','Transmission']),
 dict(slug='fork-x', name='Fork X', cat='amortiguador', img='NILS-FORK-X.jpg',
   kicker='Aceite Suspensión · Horquilla', tagline='SAE 4W diseñado para horquillas WP: ultra fluido y estable.',
   variants=['SAE 4W','Horquillas WP'],
   specs=[('Viscosidad','SAE 4W'),('Aplicación','Horquilla · esp. WP'),
          ('Formulación','Altísimo índice de viscosidad'),('Característica','Sin formación de espuma ni burbujas'),('Envase','1 L')],
   desc=P('<em>Fork X</em> es un lubricante SAE 4W de altísimo índice de viscosidad, diseñado para horquillas WP y suspensiones de competición.',
          'Su bajo grado asegura una respuesta ultra sensible manteniendo funcionamiento consistente en todo el rango de temperatura, sin espuma ni burbujas.'),
   related=['Fork','Shock H','Race','Off Road']),
 dict(slug='air-filter-cleaner', name='Air Filter Cleaner', cat='filtro-aire', img='NILS-AIR-FILTER-CLEANER.jpg',
   kicker='Filtro de Aire · Limpieza', tagline='Limpiador para lavar y reutilizar tu filtro de aire de espuma.',
   variants=['5 L','Lavado de filtros'],
   specs=[('Uso','Lavado de filtros de espuma'),('Aplicación','Filtro de aire'),('Rinde','Reutilización del filtro'),('Envase','5 L')],
   desc=P('<em>Air Filter Cleaner</em> es un limpiador específico para lavar filtros de aire de espuma y dejarlos listos para volver a aceitar.',
          'Remueve grasa y suciedad en profundidad sin dañar la espuma, extendiendo la vida útil del filtro.'),
   related=['Air Filter','Air Filter Spray','Chain Cleaner','Off Road Chain']),
 dict(slug='silicon-race', name='Silicon Race', cat='mantenimiento', img='NILS-SILICON-RACE.jpg',
   kicker='Mantenimiento · Protector', tagline='Protector y abrillantador de plásticos y superficies.',
   variants=['Spray 400 ml','Plásticos'],
   specs=[('Uso','Protección y brillo de plásticos'),('Aplicación','Carrocería · plásticos'),('Formato','Spray'),('Envase','400 ml')],
   desc=P('<em>Silicon Race</em> protege y realza plásticos, gomas y superficies pintadas, dejando un acabado brillante y repelente a la suciedad.',
          'Ideal para el detallado final de la moto luego del lavado.'),
   related=['Uni Lube','Foam & Shine','Multi Cleaner','Contact Cleaner']),
 dict(slug='uni-lube', name='Uni Lube', cat='mantenimiento', img='NILS-UNI-LUBE.jpg',
   kicker='Mantenimiento · Lubricante', tagline='Lubricante universal multiuso en spray.',
   variants=['Spray 400 ml','Multiuso'],
   specs=[('Uso','Lubricante universal'),('Aplicación','Multiuso · antihumedad'),('Formato','Spray'),('Envase','400 ml')],
   desc=P('<em>Uni Lube</em> es un lubricante universal multiuso que lubrica, protege y desplaza la humedad en todo tipo de mecanismos.',
          'Afloja piezas, previene la oxidación y deja una película protectora duradera.'),
   related=['Silicon Race','Contact Cleaner','Chain Cleaner','Foam & Shine']),
 dict(slug='foam-shine', name='Foam & Shine', cat='mantenimiento', img='NILS-FOAM-SHINE.jpg',
   kicker='Mantenimiento · Limpieza', tagline='Espuma limpiadora y abrillantadora para toda la moto.',
   variants=['Spray 500 ml','Limpieza'],
   specs=[('Uso','Limpieza y brillo'),('Aplicación','Toda la moto'),('Formato','Espuma en spray'),('Envase','500 ml')],
   desc=P('<em>Foam & Shine</em> es una espuma activa que limpia y abrillanta todas las superficies de la moto en un solo paso.',
          'Su acción envolvente disuelve la suciedad sin esfuerzo y realza el brillo de plásticos, metales y pintura.'),
   related=['Multi Cleaner','Solvent','Silicon Race','Contact Cleaner']),
 dict(slug='multi-cleaner', name='Multi Cleaner', cat='mantenimiento', img='NILS-MULTI-CLEANER.jpg',
   kicker='Mantenimiento · Limpieza', tagline='Espuma limpiadora multiuso de acción profunda.',
   variants=['Spray 500 ml','Limpieza'],
   specs=[('Uso','Limpiador espuma multiuso'),('Aplicación','Superficies varias'),('Formato','Espuma en spray'),('Envase','500 ml')],
   desc=P('<em>Multi Cleaner</em> es una espuma limpiadora especial de acción profunda para múltiples superficies.',
          'Remueve grasa, polvo y suciedad incrustada respetando los materiales, con enjuague fácil.'),
   related=['Foam & Shine','Solvent','Contact Cleaner','Silicon Race']),
 dict(slug='solvent', name='Solvent', cat='mantenimiento', img='NILS-SOLVENT.jpg',
   kicker='Mantenimiento · Desengrasante', tagline='Desengrasante y solvente de acción rápida.',
   variants=['Spray 500 ml','Desengrasante'],
   specs=[('Uso','Desengrasante / solvente'),('Aplicación','Piezas y superficies'),('Formato','Spray'),('Envase','500 ml')],
   desc=P('<em>Solvent</em> es un desengrasante solvente de acción rápida para limpiar piezas, motores y superficies metálicas.',
          'Disuelve grasa, aceite y adhesivos, evaporando sin dejar residuos.'),
   related=['Multi Cleaner','Foam & Shine','Contact Cleaner','Chain Cleaner']),
 dict(slug='contact-cleaner', name='Contact Cleaner', cat='mantenimiento', img='NILS-CONTACT-CLEANER.jpg',
   kicker='Mantenimiento · Eléctrico', tagline='Limpiador de contactos eléctricos, secado rápido.',
   variants=['Spray 400 ml','Contactos eléctricos'],
   specs=[('Uso','Limpieza de contactos eléctricos'),('Aplicación','Conexiones · electrónica'),
          ('Característica','Secado rápido · no deja residuos'),('Envase','400 ml')],
   desc=P('<em>Contact Cleaner</em> limpia contactos y conexiones eléctricas dejándolos libres de suciedad, humedad y oxidación.',
          'De secado rápido y sin residuos, restablece la conductividad sin dañar plásticos ni componentes.'),
   related=['Solvent','Uni Lube','Multi Cleaner','Silicon Race']),
 dict(slug='sport-tacho-50kg', name='Sport 50 kg', cat='aceite-4t', img='NILS-TACHO-50KG.jpg',
   kicker='Aceite Motor 4T · Tacho 50 kg', tagline='Sport 100% sintético en tacho de 50 kg: el mismo producto, con menor costo por litro.',
   variants=['100% Sintético','Tacho 50 kg'],
   specs=[('Formulación','100% Sintético PAO'),('Viscosidad',['10W-40','10W-50']),('Aplicación','Motor 4T'),('Envase','Tacho 50 kg')],
   desc=P('<em>Sport 50 kg</em> es la presentación en tacho del aceite Sport 100% sintético PAO, disponible en 10W-40 y 10W-50.',
          'Pensado para talleres y flotas: el mismo rendimiento del Sport con un menor costo por litro.'),
   related=['Sport','Ride 50 kg','Race','Off Road']),
 dict(slug='ride-tacho-50kg', name='Ride 50 kg', cat='aceite-4t', img='NILS-TACHO-50KG.jpg',
   kicker='Aceite Motor 4T · Tacho 50 kg', tagline='Ride semi-sintético 15W-50 en tacho de 50 kg: rendimiento con menor costo por litro.',
   variants=['Semi-Sintético','Tacho 50 kg'],
   specs=[('Formulación','Semi Sintético PAO'),('Viscosidad','SAE 15W-50'),('Aplicación','Motor 4T'),('Envase','Tacho 50 kg')],
   desc=P('<em>Ride 50 kg</em> es la presentación en tacho del aceite Ride semi-sintético SAE 15W-50.',
          'Ideal para talleres y flotas: el mismo Ride con un menor costo por litro.'),
   related=['Ride','Sport 50 kg','Sport','Off Road']),
]

# registrar los nuevos en REG (para relacionados cruzados)
for p in NUEVOS:
    REG[p['name']] = dict(href=f"producto-{p['slug']}.html", cat=p['cat'], img=p['img'], name=p['name'], cardcat=CATLABEL[p['cat']])

# ---------- helpers de armado ----------
def specs_html(specs):
    rows=[]
    for k,v in specs:
        if isinstance(v,list):
            pills=''.join(f'<span class="specs-pill">{x}</span>' for x in v)
            rows.append(f'                    <div class="specs-row">\n                        <span class="specs-key">{k}</span>\n                        <div class="specs-pills">{pills}</div>\n                    </div>')
        else:
            rows.append(f'                    <div class="specs-row">\n                        <span class="specs-key">{k}</span>\n                        <span class="specs-value">{v}</span>\n                    </div>')
    return '\n'.join(rows)

def related_html(names):
    out=[]
    for n in names:
        r=REG.get(n)
        if not r: continue
        out.append(f'''                <a href="{r['href']}" class="related-card">
                    <div class="related-img"><img src="productos/{r['img']}" alt="NILS {r['name']}"></div>
                    <div class="related-body">
                        <div class="related-cat">{r['cardcat']}</div>
                        <div class="related-name">{r['name']}</div>
                    </div>
                </a>''')
    return '\n'.join(out)

def page_html(p):
    title=f"NILS {p['name']} &middot; {CATLABEL[p['cat']]} | Radsport Geist"
    head=set_title(head_html, title)
    wa=('https://wa.me/5491135713234?text=Hola%2C%20quiero%20comercializar%20NILS%20'+p['name'].replace(' ','%20'))
    body=f'''<div class="page-wrap">
        <div class="breadcrumb">
            <a href="../../index.html">Inicio</a> <span>&rsaquo;</span>
            <a href="../../productos.html">Productos</a> <span>&rsaquo;</span>
            <a href="productos.html">NILS</a> <span>&rsaquo;</span>
            <span>{p['name']}</span>
        </div>

        <div class="product-hero">
            <div class="product-gallery">
                <div class="gallery-thumbs">
                    <button class="gallery-thumb active" data-src="productos/{p['img']}" type="button">
                        <img src="productos/{p['img']}" alt="vista">
                    </button>
                </div>
                <div class="gallery-main" id="galleryMain">
                    <svg class="gallery-zoom-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <img id="mainImg" src="productos/{p['img']}" alt="NILS {p['name']}">
                </div>
            </div>

            <div class="product-info-side">
                <div class="product-kicker">{p['kicker']}</div>
                <h1 class="product-title">{p['name']}</h1>
                <p class="product-tagline">{p['tagline']}</p>

                <div class="specs-table">
{specs_html(p['specs'])}
                </div>

                <div class="product-cta-row">
                    <a href="../../donde-comprar/moto.html?marca=nils" class="cta-btn primary">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                        </svg>
                        Dónde Comprar
                    </a>
                    <a href="{wa}" target="_blank" class="cta-btn secondary">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                            <path d="M3 7l9 6 9-6"/>
                            <rect x="3" y="5" width="18" height="14" rx="2"/>
                        </svg>
                        Soy Comercio
                    </a>
                </div>
            </div>
        </div>

        <div class="product-description-section">
            <div class="description-header">Descripción</div>
{chr(10).join('            <p>'+d+'</p>' for d in p['desc'])}
        </div>

        <div class="related-section">
            <h2 class="related-header">Otros productos que <span>te pueden interesar</span></h2>
            <div class="related-grid">
{related_html(p['related'])}
            </div>
        </div>
    </div>

'''
    return head + body + FOOT

# ---------- 1) generar fichas ----------
for p in NUEVOS:
    wr(f"producto-{p['slug']}.html", page_html(p))
print(f"OK fichas generadas: {len(NUEVOS)}")

# ---------- 2) tarjeta del catalogo ----------
def card_html(p):
    variants=''.join(f'<span class="variant-tag">{v}</span>' for v in p['variants'])
    return f'''        <a href="producto-{p['slug']}.html" class="product-card" data-category="{p['cat']}" data-segment="moto">
            <div class="product-card-img"><img src="productos/{p['img']}" alt="{p['name']}" loading="lazy"></div>
            <div class="product-card-body">
                <div class="product-card-category">{CATLABEL[p['cat']]}</div>
                <h3>{p['name']}</h3>
                <div class="product-card-variants">{variants}</div>
            </div>
        </a>
'''

# idempotente: sacar tarjetas ya insertadas de estos slugs (para poder re-correr sin duplicar)
for p in NUEVOS:
    cat_html = re.sub(r'[ \t]*<a href="producto-'+re.escape(p['slug'])+r'\.html" class="product-card".*?</a>\n?',
                      '', cat_html, flags=re.DOTALL)

# limites de la zona de tarjetas: desde la grilla hasta el div 'no-results' (marcador estable, va al final de las cards)
gopen = cat_html.index('<div class="products-grid" id="productsGrid">')
gclose = cat_html.index('<div class="no-results" id="noResults">')

# spans de tarjetas existentes con su categoria
existing=[(m.group(1), m.end()) for m in re.finditer(r'data-category="([^"]*)"[^>]*>.*?</a>\n', cat_html[gopen:gclose], re.DOTALL)]
existing=[(c, gopen+e) for c,e in existing]

# insercion: cada tarjeta despues de la ultima de su categoria; si no hay, al cierre de la grilla
ins=[]
for p in NUEVOS:
    same=[e for c,e in existing if c==p['cat']]
    pos = max(same) if same else gclose
    ins.append((pos, card_html(p)))
    # si comparten categoria entre nuevos, encadenar
    existing.append((p['cat'], pos))
# aplicar de atras hacia adelante
out=cat_html
for pos,html in sorted(ins,key=lambda x:-x[0]):
    out = out[:pos] + html + out[pos:]
# normalizar separacion entre tarjetas (evitar glue '</a>        <a')
out = re.sub(r'</a>[ \t]+<a href="producto', '</a>\n        <a href="producto', out)

# ---------- 3) filtro 'mantenimiento' ----------
if 'data-filter="mantenimiento"' not in out:
    out = out.replace('<button class="filter-btn" data-filter="grasas">Grasas / Limpieza</button>',
                      '<button class="filter-btn" data-filter="grasas">Grasas / Limpieza</button>\n        <button class="filter-btn" data-filter="mantenimiento">Mantenimiento / Limpieza</button>')
wr('productos.html', out)
print("OK productos.html actualizado (tarjetas + filtro mantenimiento)")
