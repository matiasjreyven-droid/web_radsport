# -*- coding: utf-8 -*-
"""
Genera el catálogo global (06_Pagina Web/productos.html) alimentándose de los
catálogos de cada marca (marcas/{marca}/productos.html).
- Marcas con cards estáticas: se regeneran desde su catálogo (prefijo de rutas,
  data-brand, data-name, logo de marca).
- Marcas con 'finder' (Leo Vince, WRP): se preservan las cards actuales del global.
- El rótulo de marca es el LOGO (no texto), arriba-derecha.
Reutilizable: correr después de actualizar cualquier marca.
"""
import re, os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOBAL = os.path.join(ROOT, 'productos.html')

LOGOS = {'cst':'CST','shot':'SHOT','nils':'NILS','uswe':'USWE','giantloop':'Giant Loop',
         'nitromousse':'Nitro Mousse','lucioli':'Lucioli','sidi':'SIDI','leovince':'Leo Vince','wrp':'WRP'}
STATIC = ['cst','shot','nils','uswe','giantloop','nitromousse','lucioli','sidi']
FINDER = ['leovince','wrp']
ORDER  = ['cst','leovince','shot','uswe','giantloop','nils','nitromousse','lucioli','wrp','sidi']

def logo_div(b):
    return f'<div class="product-card-brand"><img src="img/logos/{b}.png" alt="{LOGOS[b]}"></div>'

def transform(card, b):
    name = re.search(r'<h3[^>]*>([^<]*)</h3>', card); name = name.group(1).strip() if name else ''
    cat  = re.search(r'product-card-category">([^<]*)<', card); cat = cat.group(1).strip() if cat else ''
    dn = re.sub(r'\s+',' ', f'{b} {name} {cat}').strip().lower()
    card = re.sub(r'href="(producto[^"]*)"', lambda m: f'href="marcas/{b}/{m.group(1)}"', card, count=1)
    card = re.sub(r'(src=")((?!https?:|/|\.\.|marcas/|img/)[^"]+)(")',
                  lambda m: m.group(1)+f'marcas/{b}/'+m.group(2)+m.group(3), card)
    card = re.sub(r'(<a [^>]*class="product-card"[^>]*?)(>)',
                  lambda m: f'{m.group(1)} data-brand="{b}" data-name="{dn}"{m.group(2)}', card, count=1)
    card = re.sub(r'(<a [^>]*class="product-card"[^>]*>)',
                  lambda m: m.group(1)+'\n            '+logo_div(b), card, count=1)
    return card

def swap_brand_logo(card, b):
    return re.sub(r'<div class="product-card-brand">[\s\S]*?</div>', logo_div(b), card, count=1)

g = open(GLOBAL, encoding='utf-8').read()
shutil.copy(GLOBAL, GLOBAL+'.bak')

# 1) preservar cards finder (Leo Vince, WRP) del global -> con logo
preserved = {}
for b in FINDER:
    cards = re.findall(r'<a [^>]*class="product-card"[^>]*data-brand="'+b+r'"[\s\S]*?</a>', g)
    preserved[b] = [swap_brand_logo(c, b) for c in cards]

# 2) regenerar static desde catálogo de marca
generated = {}
for b in STATIC:
    bh = open(os.path.join(ROOT,'marcas',b,'productos.html'), encoding='utf-8').read()
    cards = re.findall(r'<a [^>]*class="product-card"[^>]*>[\s\S]*?</a>', bh)
    generated[b] = [transform(c, b) for c in cards]

# 3) ensamblar en orden
blocks=[]
for b in ORDER:
    blocks += generated.get(b) or preserved.get(b) or []
new_grid = '\n\n'+'\n\n'.join('        '+c.lstrip() if not c.startswith('        ') else c for c in blocks)+'\n'

# 4) reemplazar contenido del grid (sacar todas las cards, insertar assembly)
head, sep, rest = g.partition('<div class="products-grid" id="productsGrid">')
rest = re.sub(r'\n* *<a [^>]*class="product-card"[\s\S]*?</a>', '', rest)   # saca cards viejas
g = head + sep + new_grid + rest

# 5) CSS del rótulo -> logo, arriba-derecha
g = re.sub(r'\.product-card-brand\s*\{[^}]*\}',
    '.product-card-brand { position: absolute; top: 0.8rem; right: 0.8rem; background: white; padding: 0.3rem 0.5rem; border-radius: 5px; box-shadow: 0 2px 6px rgba(0,0,0,0.12); z-index: 2; display: flex; align-items: center; height: 22px; }\n        .product-card-brand img { height: 15px; width: auto; max-width: 62px; object-fit: contain; display: block; }',
    g, count=1)

# 6) asegurar CSS de cards específicas de marca que el global necesita
#    (las cards se copian de cada marca pero su CSS vive en la marca; acá garantizamos
#    las reglas que el global no trae por defecto). Idempotente.
_global_css = []
if '.size-tag' not in g:
    _global_css.append('        .product-card-sizes { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.5rem; }')
    _global_css.append('        .size-tag { font-size: 0.6rem; font-weight: 600; letter-spacing: 0.3px; color: var(--brand-subtle); background: var(--gray-light); border: 1px solid #e3e3e3; border-radius: 4px; padding: 0.18rem 0.4rem; white-space: nowrap; }')
if '.card-sold-badge' not in g:
    _global_css.append('        .card-sold-badge { position: absolute; top: 12px; left: 12px; z-index: 3; background: #9e2b25; color: #fff; font-size: 0.64rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; padding: 6px 11px; border-radius: 7px; box-shadow: 0 3px 10px rgba(0,0,0,0.22); }')
if _global_css:
    css_fix = '    <style id="global-card-fixes-'+str(abs(hash(''.join(_global_css)))%10000)+'">\n'+'\n'.join(_global_css)+'\n    </style>\n</head>'
    g = g.replace('</head>', css_fix, 1)

open(GLOBAL,'w',encoding='utf-8').write(g)
tot = sum(len(v) for v in generated.values()) + sum(len(v) for v in preserved.values())
print('GLOBAL regenerado |', {b:(len(generated.get(b,[])) or len(preserved.get(b,[]))) for b in ORDER}, '| total', tot)
