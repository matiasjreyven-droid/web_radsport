# -*- coding: utf-8 -*-
"""Fase 4b: titulos + meta description a paginas de marca, listados y paginas principales."""
import re, html
from pathlib import Path
ROOT = Path(r"C:\Users\matia\OneDrive\Escritorio\Radsport\06_Pagina Web")
def esc(s): return html.escape(str(s or ''), quote=True)

# file -> (title|None, meta)
CFG = {
 # paginas de marca (landing)
 'marcas/shot/shot.html': ("SHOT Race Gear Argentina – Importador oficial | Radsport Geist",
   "Importador oficial de SHOT Race Gear en Argentina: cascos, botas, antiparras, guantes, protecciones y conjuntos de motocross y enduro."),
 'marcas/nils/nils.html': ("NILS Argentina – Importador oficial de lubricantes | Radsport Geist",
   "Importador oficial de lubricantes NILS en Argentina: aceites de motor, cadena, horquilla, refrigerantes y limpiadores para moto."),
 'marcas/cst/cst.html': ("CST Argentina – Importador oficial de cubiertas | Radsport Geist",
   "Importador oficial de cubiertas CST en Argentina para moto, ATV y bicicleta: off-road, on-road y MTB."),
 'marcas/sidi/sidi.html': ("SIDI Argentina – Importador oficial de botas | Radsport Geist",
   "Importador oficial de botas SIDI en Argentina para motocross, enduro y ruta. Calidad italiana."),
 'marcas/uswe/uswe.html': ("USWE Argentina – Importador oficial | Radsport Geist",
   "Importador oficial de USWE en Argentina: mochilas de hidratación con arnés NDM para moto y bici."),
 'marcas/giantloop/giantloop.html': ("Giant Loop Argentina – Importador oficial | Radsport Geist",
   "Importador oficial de Giant Loop en Argentina: alforjas y equipaje blando para moto adventure y enduro."),
 'marcas/lucioli/lucioli.html': ("Lucioli Argentina – Importador oficial | Radsport Geist",
   "Importador oficial de Lucioli en Argentina: cámaras y accesorios para moto."),
 'marcas/nitromousse/nitromousse.html': ("Nitro Mousse Argentina – Importador oficial | Radsport Geist",
   "Importador oficial de Nitro Mousse en Argentina: mousse antipinchaduras para moto de off-road y enduro."),
 # paginas principales
 'index.html': ("Radsport Geist – Importador y distribuidor de accesorios de moto en Argentina",
   "Importador y distribuidor oficial en Argentina de CST, LeoVince, SHOT, SIDI, USWE, NILS, Nitro Mousse, Lucioli, WRP y Giant Loop. Encontrá tu punto de venta."),
 'productos.html': ("Catálogo de productos – Moto, ATV y Bici | Radsport Geist",
   "Catálogo completo de Radsport Geist: cubiertas, escapes, cascos, botas, lubricantes, pastillas y más. Buscá por marca, segmento o tu moto."),
 'sobre-nosotros.html': ("Sobre Radsport Geist – Importador y distribuidor | Argentina",
   "Radsport Geist: importación y distribución de las mejores marcas de moto, ATV y bici en Argentina."),
 # listados de marca (title; meta generica)
 'marcas/shot/productos.html': ("Productos SHOT Race Gear Argentina | Radsport Geist",
   "Cascos, botas, antiparras, guantes, protecciones y conjuntos SHOT. Importador oficial en Argentina."),
 'marcas/nils/productos.html': ("Productos NILS Argentina – Lubricantes | Radsport Geist",
   "Aceites y lubricantes NILS para moto. Importador oficial en Argentina."),
 'marcas/cst/productos.html': ("Cubiertas CST Argentina – Moto, ATV y Bici | Radsport Geist",
   "Catálogo de cubiertas CST para moto, ATV y bicicleta. Importador oficial en Argentina."),
 'marcas/sidi/productos.html': ("Botas SIDI Argentina | Radsport Geist",
   "Botas SIDI para motocross, enduro y ruta. Importador oficial en Argentina."),
 'marcas/uswe/productos.html': ("Mochilas de hidratación USWE Argentina | Radsport Geist",
   "Mochilas de hidratación USWE para moto y bici. Importador oficial en Argentina."),
 'marcas/giantloop/productos.html': ("Alforjas y equipaje Giant Loop Argentina | Radsport Geist",
   "Equipaje blando Giant Loop para moto adventure. Importador oficial en Argentina."),
 'marcas/nitromousse/productos.html': ("Nitro Mousse Argentina | Radsport Geist",
   "Mousse antipinchaduras Nitro Mousse para off-road. Importador oficial en Argentina."),
 'marcas/lucioli/productos.html': ("Lucioli Argentina | Radsport Geist",
   "Cámaras y accesorios Lucioli para moto. Importador oficial en Argentina."),
 # segmentos (solo meta; titulo lo dejamos)
 'segmentos/moto.html': (None,"Accesorios y repuestos de moto en Argentina: cubiertas, escapes, cascos, botas, lubricantes y más. Radsport Geist, importador oficial."),
 'segmentos/atv.html': (None,"Accesorios y cubiertas para ATV / UTV / SSV en Argentina. Radsport Geist, importador oficial."),
 'segmentos/bici.html': (None,"Cubiertas, hidratación y accesorios de bicicleta en Argentina. Radsport Geist."),
 'segmentos/industrial.html': (None,"Cubiertas industriales y de autoelevador CST en Argentina. Radsport Geist."),
 'donde-comprar/moto.html': (None,"Encontrá dónde comprar productos de moto de Radsport Geist: puntos de venta en toda Argentina."),
}
done=0
for rel,(title,meta) in CFG.items():
    p=ROOT/rel
    if not p.exists(): print('NO existe:',rel); continue
    t=p.read_text(encoding='utf-8'); orig=t
    if title:
        t=re.sub(r'<title>.*?</title>','<title>'+esc(title)+'</title>',t,count=1,flags=re.S)
    headend=t.find('</head>'); head=t[:headend]
    if '<meta name="description"' not in head and meta:
        t=t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <meta name="description" content="'+esc(meta)+'">',1)
    if t!=orig: p.write_text(t,encoding='utf-8'); done+=1
print('paginas actualizadas:',done,'/',len(CFG))
