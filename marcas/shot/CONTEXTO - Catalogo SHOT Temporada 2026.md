# Contexto — Catálogo web SHOT, Temporada 2026 (subir productos faltantes)

Documento para pegarle a Code: qué hay que subir a radsport.com.ar, de dónde salió cada cosa, y qué
falta antes de poder subirlo del todo.

Última actualización: 2026-09-13

---

## 1. Objetivo

Subir a la sección SHOT del sitio (carpeta del repo: `marcas/shot/`) los productos/colores que
Radsport **ya tiene en stock** pero que hoy **no están publicados** en la web. Es la "Temporada
2026": no son productos nuevos del próximo contenedor (eso es una fase aparte, "Temporada 2027",
todavía no armada).

No confundir con reposición de stock: esto es catálogo (páginas, fotos, texto), no disponibilidad.

## 2. Dónde está todo

| Qué | Dónde |
|---|---|
| Fotos + `_indice_shot.csv` (26 variantes, 30 archivos) | `Radsport\01_Importacion\01_Marcas\01_SHOT\15_Multimedia\Productos\Temporada 2026\` |
| Análisis completo con criterio de cada item (por qué se agrega, como variante o modelo nuevo) | `Radsport\01_Importacion\01_Marcas\01_SHOT\Claude outputs\SHOT_Catalogo_Analisis.xlsx` (hoja "Stock no en la web") |
| Código fuente del sitio (HTML) | `Radsport\06_Pagina Web\marcas\shot\` |
| Origen de las fotos | `Radsport\01_Importacion\01_Marcas\01_SHOT\04_Listas de precios\Lista de Precios SHOT - Agosto 2026.xlsx` (hoja "Novedades") |

`Temporada 2026\` está organizada `categoria/modelo/` igual que el criterio del sitio, y cada foto
sigue el patrón `{modelo}_{color}_{n}_{SKU}.png` (`n` = ángulo). El `_indice_shot.csv` tiene una fila
por variante: `categoria, modelo, color, sku, talles, url_oficial, fotos`.

## 3. Cómo está el sitio hoy (para no romper el patrón)

- Cada modelo tiene su propia página `marcas/shot/producto-{categoria}-{modelo}.html` (ej.
  `producto-casco-lite.html`, `producto-guantes-core.html`).
- El listado general está en `marcas/shot/productos.html`: tarjetas por modelo agrupadas en
  categorías. Las categorías que existen hoy en la nav/listado son **solo 7**: cascos, antiparras,
  guantes, botas, camperas, conjuntos, protecciones (+ pantalones/jerseys si aplican). **No hay
  categoría de Niños ni de Equipaje todavía** — hay que crearlas (nav, listado, template de página).
- Los colores de cada modelo viven o bien en un array JS `colors: [{name: '...', ...}]` dentro del
  `producto-*.html` (ej. Lite, Race 2, Race 8), o bien como imágenes sueltas referenciadas
  directamente en el HTML (la mayoría de los modelos). Al agregar un color nuevo a un modelo
  existente, seguir el mismo mecanismo que ya use esa página puntual — no son todas iguales.
- Nomenclatura de fotos ya usada en el sitio: `productos/{modelo}_{color}_{terminacion}_{n}_{SKU}.png`
  cuando viene del portal oficial de SHOT tal cual, o `lp-{modelo}-{color}.png` para las miniaturas
  del listado general. Nuestras fotos nuevas (carpeta Temporada 2026) todavía no tienen ese
  `lp-` correspondiente — falta generarlo (recorte/miniatura) si el patrón del listado lo requiere.

## 4. Los 26 items a subir

| Categoría | Modelo | Color | SKU | Talles | Tipo de alta |
|---|---|---|---|---|---|
| Cascos - Niños | Speed Kid | Ghost Neon Yellow Glossy | *pendiente* | S,M,L | Categoría Niños nueva |
| Cascos - Niños | Speed Kid | Olymp Blue Pearly | *pendiente* | S,M,L | Categoría Niños nueva |
| Cascos - Niños | Speed Kid | Olymp Purple Pearly | *pendiente* | S,M,L | Categoría Niños nueva |
| Antiparras - Niños | Rocket Kid 2.0 | Solid Black | *pendiente* | Único | Categoría Niños nueva |
| Antiparras - Niños | Rocket Kid 2.0 | Solid Neon Yellow | *pendiente* | Único | Categoría Niños nueva |
| Antiparras - Niños | Rocket Kid 2.0 | Navy Matt | *pendiente* | Único | Categoría Niños nueva |
| Antiparras - Niños | Rocket Kid 2.0 | Solid White Glossy | *pendiente* | Único | Categoría Niños nueva |
| Botas - Niños | Race 2 Kid | Black | **A09-24D2-A02** | 30,34,38 (y talles intermedios según stock) | Categoría Niños nueva. OJO: disponible=0 hoy, llega en el contenedor (no subir precio/stock hasta que entre) |
| Protecciones - Niños | T-Shirt Airlight Kid | Black Neon Yellow | *pendiente* | YS,YM,YL | Categoría Niños nueva |
| Protecciones - Niños | Neck Brace Kid | Black Neon Yellow | *pendiente* | Único | Categoría Niños nueva |
| Protecciones - Niños | Knee Guard Airlight Kid | — | *pendiente* | YS-YM,YL-YXL | Categoría Niños nueva |
| Protecciones - Niños | Elbow Guard Airlight Kid | — | *pendiente* | YS-YM,YL-YXL | Categoría Niños nueva |
| Protecciones | Chest Protector Prime | Black Neon Yellow | *pendiente* | M,L,XL,2XL | Modelo nuevo, propio (no variante del Chest Protector Airflow) |
| Protecciones | Body Armor Race D3O | Black | *pendiente* | XS,S,M,L,XL,2XL | Modelo nuevo, propio (no variante del Chest Protector Airflow) |
| Protecciones | Knee Guard Race D3O | Black | *pendiente* | XS-S,M-L,XL-2XL | Modelo nuevo, propio (no variante del Knee Guard Airflow) |
| Protecciones | Elbow Guard Race D3O | Black | *pendiente* | XS-S,M-L,XL-2XL | Modelo nuevo, propio |
| Guantes | Core Max | Black | **A06-13C1-A03** | M,L,XL,2XL | Sub-línea nueva dentro de Guantes (no confundir con el "Core" clásico ya publicado) |
| Guantes | Core Max | Blue | **A06-13C1-A02** | M,L,XL,2XL | Idem |
| Guantes | Core Max | Neon Yellow | **A06-13C1-A05** | M,XL,2XL | Idem |
| Guantes | Core Max | Red | **A06-13C1-A01** | M,L,XL,2XL | Idem |
| Botas | Race 8 | Neon Yellow | *pendiente* | 41,42,43,44,45,46 | Color nuevo del modelo Race 8 (ya publicado) |
| Botas | Race 2 | Enduro Black | **A07-24D1-A10** | 42,44,45,46 | Color nuevo del modelo Race 2 (ya publicado) |
| Equipaje | Travel Bag | Climatic Black | *pendiente* | Único | Categoría Equipaje nueva |
| Equipaje | Boots Bag | Climatic Black | *pendiente* | Único | Categoría Equipaje nueva |
| Conjuntos | Contact | Shield Blue | *pendiente* | S,M (jersey) / 30,32 (pantalón) | Color nuevo del conjunto Contact (ya publicado); jersey+pantalón ya están en stock |
| Conjuntos | Contact | Shield Gold | *pendiente* | S,M,L (jersey) / 30,32,34 (pantalón) | Idem |

## 5. Lo que falta / hay que decidir antes de subir todo

- **SKU pendiente en 20 de 26 items.** La Lista de Precios interna no trae SKU en ninguna hoja; los
  6 que sí tienen SKU (arriba, en negrita) salieron porque también aparecen en el contenedor que
  llega en ~1 mes (facturas de Powersports). Si hace falta el SKU real de los otros 20 antes de
  publicar, buscarlo en el portal oficial de SHOT o pedírselo a Matías.
- **Sin fotos disponibles (no incluidas en esta tanda):** Gorra (Black Symbol, Camo Symbol, Stoke
  Black), Remera (Symbol White, Team Black), y la categoría Repuestos. Ninguna tiene foto cargada
  en la Lista de Precios — confirmado en `01_SHOT\04_Listas de precios\CONTEXTO - Lista de Precios
  SHOT.md` ("Gorra y Remera existen en el ERP pero no en la lista de precios: se ignoran").
- **Race 2 Kid Black**: hoy 0 disponible en stock (llega en el contenedor). Sugerencia: crear la
  ficha pero no activarla a la venta hasta que haya stock real.
- **Categorías nuevas a crear en el sitio**: Niños (con sus 4 sub-secciones: cascos, antiparras,
  botas, protecciones) y Equipaje. Ninguna existe hoy en la navegación ni en `productos.html`.
- **Miniaturas de listado (`lp-*.png`)** todavía no están generadas para ninguno de estos 26 items —
  ver punto 3.

## 6. Temporada 2027 (todavía no arrancada)

Los productos nuevos del contenedor (Speed, Drop, refresh de Furious/Lite, guantes Race Evo/Drift/
Vision, botas ATV 2.0/Race 6, campera Climatic, codera Optimal 2.0) **no están en esta entrega**.
Esos no tienen foto en la Lista de Precios (es la colección que todavía no se cargó); hace falta el
catálogo oficial de la temporada 27 de SHOT (o el portal oficial) para conseguir las fotos. Ver hoja
"Contenedor - Proximamente" del archivo de análisis para el detalle completo de qué entra ahí.
