/* ============================================================
   Radsport Geist — Widget de contacto WhatsApp
   Un solo archivo, se incluye con <script src="/js/whatsapp-widget.js" defer></script>
   Mejora progresiva: si falla el JS, el botón sigue abriendo WhatsApp normal.
   ============================================================ */
(function () {
  "use strict";
  var PHONE_DEALER = "5491135713234"; // Quiero ser punto de venta
  var PHONE_BUY = "5491177418982";    // Me interesa un producto
  var BRANDS = [
    { name: "CST",          logo: "/img/logos/cst.png" },
    { name: "Leo Vince",    logo: "/img/logos/leovince.png" },
    { name: "SHOT",         logo: "/img/logos/shot.png" },
    { name: "SIDI",         logo: "/img/logos/sidi.png" },
    { name: "USWE",         logo: "/img/logos/uswe.png" },
    { name: "NILS",         logo: "/img/logos/nils.png" },
    { name: "Nitro Mousse", logo: "/img/logos/nitromousse.png" },
    { name: "WRP",          logo: "/img/logos/wrp.png" },
    { name: "Lucioli",      logo: "/img/logos/lucioli.png" },
    { name: "Giant Loop",   logo: "/img/logos/giantloop.png" }
  ];

  function waLink(phone, msg) {
    return "https://wa.me/" + phone + "?text=" + encodeURIComponent(msg);
  }
  var MSG_DEALER = "¡Hola! Me gustaría ser punto de venta de Radsport Geist. ¿Me podrían brindar información para comercializar sus marcas?";
  function msgBuy(brand) {
    return "¡Hola! Me interesa un producto de " + brand + " de Radsport Geist. ¿Me podrían asesorar?";
  }

  var CSS = ''
  + '.rsw-panel{position:fixed;right:1.5rem;bottom:6.2rem;width:340px;max-width:calc(100vw - 2rem);'
  + 'background:#fff;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.22);z-index:1000;'
  + 'overflow:hidden;font-family:"Inter",system-ui,sans-serif;opacity:0;visibility:hidden;'
  + 'transform:translateY(16px) scale(.98);transition:opacity .22s ease,transform .22s ease,visibility .22s;}'
  + '.rsw-panel.rsw-open{opacity:1;visibility:visible;transform:translateY(0) scale(1);}'
  + '.rsw-head{background:#075E54;color:#fff;padding:1rem 1.1rem;display:flex;align-items:center;gap:.7rem;}'
  + '.rsw-ava{width:42px;height:42px;border-radius:50%;background:#128C7E;display:flex;align-items:center;justify-content:center;flex:0 0 42px;}'
  + '.rsw-ava svg{width:24px;height:24px;fill:#fff;}'
  + '.rsw-head-txt{line-height:1.2;flex:1;min-width:0;}'
  + '.rsw-head-txt b{font-size:.92rem;font-weight:700;display:block;}'
  + '.rsw-head-txt span{font-size:.72rem;opacity:.85;display:flex;align-items:center;gap:.3rem;}'
  + '.rsw-dot{width:7px;height:7px;border-radius:50%;background:#4ade80;display:inline-block;}'
  + '.rsw-close{background:none;border:none;color:#fff;cursor:pointer;font-size:1.3rem;line-height:1;opacity:.85;padding:.2rem;border-radius:6px;}'
  + '.rsw-close:hover{opacity:1;background:rgba(255,255,255,.12);}'
  + '.rsw-body{background:#E5DDD5;background-image:linear-gradient(rgba(229,221,213,.6),rgba(229,221,213,.6));'
  + 'padding:1.1rem;max-height:62vh;overflow-y:auto;}'
  + '.rsw-bubble{background:#fff;border-radius:0 12px 12px 12px;padding:.8rem .9rem;font-size:.86rem;color:#111;'
  + 'box-shadow:0 1px 1px rgba(0,0,0,.08);max-width:92%;margin-bottom:.9rem;line-height:1.45;}'
  + '.rsw-bubble b{font-weight:700;}'
  + '.rsw-opts{display:flex;flex-direction:column;gap:.55rem;}'
  + '.rsw-opt{display:flex;align-items:center;gap:.7rem;width:100%;text-align:left;cursor:pointer;'
  + 'background:#fff;border:1px solid #e3e3e3;border-radius:12px;padding:.8rem .9rem;font-family:inherit;'
  + 'font-size:.85rem;font-weight:600;color:#111;transition:border-color .15s,transform .12s,box-shadow .15s;}'
  + '.rsw-opt:hover{border-color:#25D366;transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.08);}'
  + '.rsw-opt .rsw-ico{width:34px;height:34px;flex:0 0 34px;border-radius:9px;background:#f0faf3;'
  + 'display:flex;align-items:center;justify-content:center;font-size:1.1rem;}'
  + '.rsw-opt .rsw-opt-sub{display:block;font-size:.72rem;font-weight:400;color:#777;margin-top:.1rem;}'
  + '.rsw-back{background:none;border:none;cursor:pointer;color:#075E54;font-weight:700;font-size:.8rem;'
  + 'font-family:inherit;display:inline-flex;align-items:center;gap:.3rem;margin-bottom:.7rem;padding:0;}'
  + '.rsw-brands{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;}'
  + '.rsw-brand{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.4rem;cursor:pointer;'
  + 'background:#fff;border:1px solid #e3e3e3;border-radius:12px;padding:.7rem .4rem;font-family:inherit;'
  + 'transition:border-color .15s,transform .12s,box-shadow .15s;min-height:74px;}'
  + '.rsw-brand:hover{border-color:#25D366;transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.08);}'
  + '.rsw-brand img{max-height:26px;max-width:84px;width:auto;object-fit:contain;}'
  + '.rsw-brand span{font-size:.68rem;font-weight:600;color:#444;}'
  + '.rsw-foot{background:#fff;padding:.5rem;text-align:center;font-size:.64rem;color:#9aa;border-top:1px solid #f0f0f0;}'
  + '@media (max-width:480px){.rsw-panel{right:1rem;left:1rem;width:auto;bottom:5.6rem;}}';

  var WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.55 4.19 1.6 6.02L4 29l8.13-1.55a12 12 0 0 0 3.9.65h.01C22.68 28.1 28.08 22.7 28.08 16.06 28.08 8.4 22.68 3 16.04 3zm5.44 14.5c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49 0 1.47 1.07 2.89 1.22 3.09.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.69.25-1.28.17-1.41-.07-.13-.27-.2-.57-.35z"/></svg>';

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function build() {
    var floats = document.querySelectorAll(".whatsapp-float");
    if (!floats.length) return;

    // estilos
    var style = document.createElement("style");
    style.textContent = CSS;
    document.head.appendChild(style);

    // panel
    var panel = el("div", "rsw-panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Contacto por WhatsApp");
    panel.innerHTML =
      '<div class="rsw-head">' +
        '<div class="rsw-ava">' + WA_SVG + '</div>' +
        '<div class="rsw-head-txt"><b>Radsport Geist</b><span><i class="rsw-dot"></i> En línea · responde rápido</span></div>' +
        '<button class="rsw-close" aria-label="Cerrar">&times;</button>' +
      '</div>' +
      '<div class="rsw-body"><div class="rsw-content"></div></div>' +
      '<div class="rsw-foot">Te atiende el equipo de Radsport Geist</div>';
    document.body.appendChild(panel);

    var content = panel.querySelector(".rsw-content");

    function renderHome() {
      content.innerHTML = "";
      content.appendChild(el("div", "rsw-bubble",
        "¡Hola! 👋 Bienvenido/a a <b>Radsport Geist</b>.<br>¿Cómo podemos ayudarte?"));
      var opts = el("div", "rsw-opts");
      var oBuy = el("button", "rsw-opt",
        '<span class="rsw-ico">🛒</span><span>Me interesa un producto<span class="rsw-opt-sub">Te asesoramos según la marca</span></span>');
      var oDealer = el("button", "rsw-opt",
        '<span class="rsw-ico">🤝</span><span>Quiero ser punto de venta<span class="rsw-opt-sub">Comercializá nuestras marcas</span></span>');
      oBuy.addEventListener("click", renderBrands);
      oDealer.addEventListener("click", function () { go(PHONE_DEALER, MSG_DEALER); });
      opts.appendChild(oBuy); opts.appendChild(oDealer);
      content.appendChild(opts);
    }

    function renderBrands() {
      content.innerHTML = "";
      var back = el("button", "rsw-back", "&larr; Volver");
      back.addEventListener("click", renderHome);
      content.appendChild(back);
      content.appendChild(el("div", "rsw-bubble", "Perfecto. ¿Qué <b>marca</b> te interesa?"));
      var grid = el("div", "rsw-brands");
      BRANDS.forEach(function (b) {
        var btn = el("button", "rsw-brand",
          '<img src="' + b.logo + '" alt="' + b.name + '" loading="lazy"><span>' + b.name + '</span>');
        btn.addEventListener("click", function () { go(PHONE_BUY, msgBuy(b.name)); });
        grid.appendChild(btn);
      });
      content.appendChild(grid);
    }

    function go(phone, msg) {
      window.open(waLink(phone, msg), "_blank", "noopener");
      close();
    }

    var open = false;
    function openPanel() { renderHome(); panel.classList.add("rsw-open"); open = true; }
    function close() { panel.classList.remove("rsw-open"); open = false; }
    function toggle() { open ? close() : openPanel(); }

    floats.forEach(function (f) {
      f.addEventListener("click", function (ev) {
        ev.preventDefault();
        toggle();
      });
    });
    panel.querySelector(".rsw-close").addEventListener("click", close);
    // Evita que los clicks internos lleguen al detector de "click afuera"
    panel.addEventListener("click", function (e) { e.stopPropagation(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    document.addEventListener("click", function (e) {
      if (open && !panel.contains(e.target) && !e.target.closest(".whatsapp-float")) close();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
