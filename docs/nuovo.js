/* L.M. Autoservizi — sito nuovo
   Librerie locali (le stesse del sito attuale): GSAP + ScrollTrigger per le animazioni, Lenis per lo scorrimento.
   I contenuti restano accessibili senza questo file e con "riduci movimento".
   Con JavaScript, i moduli preparano richieste su WhatsApp o email. */
(function () {
  "use strict";
  window.__nuovoPronto = true;

  var TELEFONO_WA = "393426436085";
  var EMAIL = "lucamiglietta4@gmail.com";
  var ORARI = { 1: [450, 1170], 2: [450, 1170], 3: [450, 1170], 4: [450, 1170], 5: [450, 1170] };
  var GIORNI = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"];
  var H = document.documentElement;
  var RIDOTTO = H.classList.contains("fermo");
  var SALTA = H.classList.contains("salta");
  var MOTO = !!(window.gsap && window.ScrollTrigger) && !RIDOTTO;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  if (!MOTO) H.classList.add("salta");   // senza animazioni niente stati iniziali nascosti

  var lenis = null;
  var MOTION = { fast: .16, change: .28, entry: .9, ease: "power3.out" };
  var FORZA_MOTO = false, avviaApertura = null, animaPannello = null;
  var ripetiApertura = $("[data-ripeti-apertura]");
  function aggiornaComandoMotion() {
    if (!ripetiApertura) return;
    ripetiApertura.hidden = false;
    $("span", ripetiApertura).textContent = MOTO ? "Rivedi l'apertura" : "Attiva animazioni";
  }

  /* ======================================================================
     Funzioni del sito
     ====================================================================== */

  /* ---------- Aperto / chiuso in ora italiana ---------- */
  function oraItalia() {
    var parti = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    var mappa = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, g, h, m;
    parti.forEach(function (p) {
      if (p.type === "weekday") g = mappa[p.value];
      if (p.type === "hour") h = parseInt(p.value, 10) % 24;
      if (p.type === "minute") m = parseInt(p.value, 10);
    });
    return { giorno: g, minuti: h * 60 + m };
  }
  function hhmm(min) { return Math.floor(min / 60) + ":" + String(min % 60).padStart(2, "0"); }
  function statoAttuale() {
    var ora = oraItalia(), oggi = ORARI[ora.giorno];
    if (oggi && ora.minuti >= oggi[0] && ora.minuti < oggi[1]) return { aperto: true, testo: "Aperto ora, fino alle " + hhmm(oggi[1]) };
    if (oggi && ora.minuti < oggi[0]) return { aperto: false, testo: "Chiuso, apre alle " + hhmm(oggi[0]) };
    for (var i = 1; i <= 7; i++) {
      var g = (ora.giorno + i) % 7;
      if (ORARI[g]) return { aperto: false, testo: "Chiuso, riapre " + (i === 1 ? "domani" : GIORNI[g]) + " alle " + hhmm(ORARI[g][0]) };
    }
    return { aperto: false, testo: "Chiuso" };
  }
  function aggiornaStato() {
    var s = statoAttuale(), oggi = oraItalia().giorno;
    $$("[data-stato]").forEach(function (el) { el.textContent = s.testo; el.setAttribute("data-aperto", s.aperto ? "si" : "no"); });
    $$(".orari tr[data-giorni]").forEach(function (tr) { tr.classList.toggle("oggi", tr.getAttribute("data-giorni").split(",").map(Number).indexOf(oggi) !== -1); });
  }
  aggiornaStato(); setInterval(aggiornaStato, 60000);
  $$("[data-anno]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Menu ---------- */
  var testata = $(".testata"), bottone = $(".menu-bottone"), menu = $("#menu");
  if (bottone && menu) {
    var chiudiMenu = function () { menu.classList.remove("is-open"); bottone.setAttribute("aria-expanded", "false"); bottone.setAttribute("aria-label", "Apri il menu"); document.body.style.overflow = ""; if (lenis) lenis.start(); };
    bottone.addEventListener("click", function () {
      if (menu.classList.contains("is-open")) { chiudiMenu(); return; }
      menu.classList.add("is-open"); bottone.setAttribute("aria-expanded", "true"); bottone.setAttribute("aria-label", "Chiudi il menu"); document.body.style.overflow = "hidden";
      testata.classList.remove("nascosto"); if (lenis) lenis.stop();
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menu.classList.contains("is-open")) { chiudiMenu(); bottone.focus(); } });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", chiudiMenu); });
  }

  /* ---------- Testata: trasparente in cima, si nasconde scorrendo verso il basso ---------- */
  var ultimoY = 0;
  function suScroll(y) {
    if (!testata) return;
    testata.classList.toggle("solido", y > 24);
    var giu = y > ultimoY && y > 220;
    if (!(menu && menu.classList.contains("is-open"))) testata.classList.toggle("nascosto", giu);
    ultimoY = y;
  }
  window.addEventListener("scroll", function () { if (!lenis) suScroll(window.scrollY); }, { passive: true });
  suScroll(window.scrollY);

  /* ---------- Targa: maiuscole, solo lettere e numeri ---------- */
  $$(".targa-campo").forEach(function (c) {
    c.addEventListener("input", function () { var v = c.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 7); if (v !== c.value) c.value = v; });
  });

  /* ---------- Scheda "Chiedi il ritiro" ---------- */
  var foglio = $("#foglio-ritiro");
  function apriRitiro(targa) {
    if (!foglio || typeof foglio.showModal !== "function") { location.href = "contatti.html#scrivimi"; return; }
    var t = $("#f-targa"); if (t && targa) t.value = targa;
    foglio.showModal(); if (lenis) lenis.stop();
    var primo = targa ? $("#f-comune") : $("#f-targa"); if (primo) primo.focus({ preventScroll: true });
    if (MOTO) gsap.fromTo($("form", foglio), { y: 34, opacity: 0, scale: .97 }, { y: 0, opacity: 1, scale: 1, duration: .55, ease: "expo.out" });
  }
  if (foglio) {
    $$("[data-chiudi]", foglio).forEach(function (b) { b.addEventListener("click", function () { foglio.close(); }); });
    foglio.addEventListener("click", function (e) { if (e.target === foglio) foglio.close(); });
    foglio.addEventListener("close", function () { if (lenis) lenis.start(); });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-apri='ritiro']");
    if (b) { e.preventDefault(); apriRitiro(""); }
  });
  var barra = $("[data-targa-barra]");
  if (barra) barra.addEventListener("submit", function (e) { if (!foglio) return; e.preventDefault(); apriRitiro($(".targa-campo", barra).value); });

  /* ---------- Moduli: diventano un messaggio WhatsApp o email già scritto ---------- */
  function erroreDi(campo) {
    var box = campo.closest(".campo, .consenso, .misura"), e = null;
    if (box) { e = $(".errore", box); if (!e && box.nextElementSibling && box.nextElementSibling.classList.contains("errore")) e = box.nextElementSibling; }
    return e;
  }
  function controlla(campo) {
    var v = (campo.value || "").trim(), t = "";
    if (campo.type === "checkbox") t = campo.checked ? "" : "Per inviare la richiesta serve il consenso.";
    else if (campo.required && !v) t = campo.closest(".misura") ? "Scrivi la misura completa, per esempio 205 / 55 / 16." : "Compila questo campo.";
    else if (campo.type === "tel" && v.replace(/\D/g, "").length < 8) t = "Scrivi un numero valido, così posso richiamarti.";
    else if (campo.closest(".misura") && !/^\d+$/.test(v)) t = "Scrivi la misura completa, per esempio 205 / 55 / 16.";
    var e = erroreDi(campo); if (e) e.textContent = t;
    campo.setAttribute("aria-invalid", t ? "true" : "false");
    return !t;
  }
  $$("form[data-modulo]").forEach(function (form) {
    $$("input[required], textarea[required], select[required]", form).forEach(function (c) {
      c.addEventListener("blur", function () { if (c.value || c.type === "checkbox") controlla(c); });
      // Correggi l'errore mentre si scrive, prima che il clic su Invia sposti il pulsante.
      var aggiornaErrore = function () { if (c.hasAttribute("aria-invalid")) controlla(c); };
      c.addEventListener("input", aggiornaErrore);
      c.addEventListener("change", aggiornaErrore);
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var primo = null;
      $$("input[required], textarea[required], select[required]", form).forEach(function (c) { if (!controlla(c) && !primo) primo = c; });
      if (primo) { primo.focus(); return; }
      var f = form.elements, righe = [form.getAttribute("data-intro") || "Ciao Luca,", ""];
      if (f.larghezza) righe.push("Misura: " + f.larghezza.value + "/" + f.spalla.value + " R" + f.cerchio.value);
      $$("[data-etichetta]", form).forEach(function (c) {
        if (c.name === "larghezza" || c.name === "spalla" || c.name === "cerchio") return;
        if (c.type === "radio" && !c.checked) return;
        var v = (c.value || "").trim(); if (!v) return;
        righe.push(c.getAttribute("data-etichetta") + ": " + v);
      });
      var testo = righe.join("\n");
      var email = e.submitter && e.submitter.value === "email";
      var esito = $(".esito", form);
      if (esito) { esito.hidden = false; esito.textContent = email ? "Si è aperta la tua email con la richiesta già scritta: premi Invia." : "Si è aperto WhatsApp con la richiesta già scritta: premi Invia."; }
      if (email) location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Richiesta dal sito") + "&body=" + encodeURIComponent(testo);
      else window.open("https://wa.me/" + TELEFONO_WA + "?text=" + encodeURIComponent(testo), "_blank", "noopener");
    });
  });

  /* ---------- Gomme: la misura rimane testo leggibile accanto al render ---------- */
  var testoMisura = $("#testo-misura");
  var etichettaMisura = $("[data-misura-label]");
  $$("form[data-misura]").forEach(function (form) {
    var l = form.elements.larghezza, s = form.elements.spalla, c = form.elements.cerchio;
    var agg = function () {
      var vuota = !l.value && !s.value && !c.value;
      if (testoMisura) testoMisura.textContent = vuota ? "205/55 R16" : (l.value || "—") + "/" + (s.value || "—") + " R" + (c.value || "—");
      if (etichettaMisura) etichettaMisura.textContent = vuota ? "Esempio di misura" : "La misura che cerchi";
    };
    [l, s, c].forEach(function (x) { x.addEventListener("input", function () { x.value = x.value.replace(/\D/g, ""); agg(); }); });
    agg(); window.addEventListener("pageshow", agg);
  });

  /* ---------- Recensioni: frecce ---------- */
  var voci = $(".voci");
  function aggiornaFrecceRecensioni() {
    if (!voci) return;
    var massimo = Math.max(0, voci.scrollWidth - voci.clientWidth);
    $$("[data-rec]").forEach(function (b) { b.disabled = Number(b.dataset.rec) < 0 ? voci.scrollLeft <= 2 : voci.scrollLeft >= massimo - 2; });
  }
  if (voci) {
    voci.addEventListener("scroll", aggiornaFrecceRecensioni, { passive: true });
    if (window.ResizeObserver) new ResizeObserver(aggiornaFrecceRecensioni).observe(voci);
    window.addEventListener("load", aggiornaFrecceRecensioni);
    aggiornaFrecceRecensioni();
  }
  $$("[data-rec]").forEach(function (b) {
    b.addEventListener("click", function () {
      var carta = $(".voce", voci); if (!carta) return;
      voci.scrollBy({ left: parseInt(b.getAttribute("data-rec"), 10) * (carta.offsetWidth + 20), behavior: RIDOTTO ? "auto" : "smooth" });
    });
  });

  /* ---------- Attestati ingranditi ---------- */
  var dialog = $("#lightbox");
  if (dialog && typeof dialog.showModal === "function") {
    var img = $("img", dialog), cap = $("p", dialog);
    $$("[data-lightbox]").forEach(function (b) {
      b.addEventListener("click", function () { img.src = b.getAttribute("data-lightbox"); img.alt = b.getAttribute("data-titolo"); cap.textContent = b.getAttribute("data-titolo"); dialog.showModal(); if (lenis) lenis.stop(); });
    });
    $(".lightbox-chiudi", dialog).addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener("close", function () { img.removeAttribute("src"); if (lenis) lenis.start(); });
  }

  /* ---------- Il ponte: scelta del servizio (vale anche senza animazioni) ---------- */
  var ponte = $("#ponte"), ponteApi = null;
  if (ponte) {
    var disegno = $(".ponte-disegno", ponte), servizi = $$(".servizio", ponte), indice = $$(".ponte-indice li", ponte), punti = $$(".punto", ponte);
    var ids = servizi.map(function (s) { return s.getAttribute("data-servizio"); }), corrente = -2;
    var seleziona = function (i) {
      if (i === corrente) return; corrente = i;
      servizi.forEach(function (s, k) { s.classList.toggle("attivo", k === i); });
      indice.forEach(function (s, k) { s.classList.toggle("attivo", k === i); });
      punti.forEach(function (p, k) { p.classList.toggle("attivo", k === i); });
      disegno.setAttribute("data-sel", ids[i] || "");
    };
    var sale = function (v) { disegno.style.setProperty("--sale", (clamp(v, 0, 1) * 19).toFixed(2)); };
    ponteApi = { seleziona: seleziona, sale: sale, n: servizi.length, vai: function (i) { seleziona(i); } };
    punti.forEach(function (p, i) { p.addEventListener("click", function () { ponteApi.vai(i); }); });
    $$(".ponte-indice button", ponte).forEach(function (b, i) { b.addEventListener("click", function () { ponteApi.vai(i); }); });
    seleziona(0);
  }

  /* ---------- Servizi: prepara la richiesta con il servizio scelto ---------- */
  var richiesta = $("[data-richiesta-guidata]");
  function impostaProblema(valore) {
    if (!richiesta) return;
    var campo = richiesta.elements.problema;
    if (!$$("option", campo).some(function (opzione) { return opzione.value === valore; })) return;
    campo.value = valore;
    campo.dispatchEvent(new Event("change", { bubbles: true }));
    richiesta.dispatchEvent(new Event("rqs:inizio"));
  }
  $$("[data-richiesta-servizio]").forEach(function (a) {
    a.addEventListener("click", function () { impostaProblema(a.dataset.richiestaServizio); });
  });

  /* ---------- Inviti diretti al modulo, senza una seconda scelta duplicata ---------- */
  function impostaModalita(valore) {
    if (!richiesta) return;
    var radio = $$("input[name='modalita']", richiesta).find(function (r) { return r.value === valore; });
    if (radio) { radio.checked = true; radio.dispatchEvent(new Event("change", { bubbles: true })); }
  }
  $$("[data-preferisci-ritiro]").forEach(function (a) { a.addEventListener("click", function () { impostaModalita("Ritiro e consegna"); }); });
  $$("[data-preferisci-officina]").forEach(function (a) { a.addEventListener("click", function () { impostaModalita("La porto in officina"); }); });

  /* ---------- Pannelli manuali: swipe, tastiera e comandi; nessun pin ---------- */
  function sfogliatore(traccia, pannelli, aggiorna) {
    if (!traccia) return null;
    var corrente = 0, ultimoAnimato = 0;
    function leggi() {
      corrente = Math.max(0, Math.min(pannelli.length - 1, Math.round(traccia.scrollLeft / traccia.clientWidth)));
      if (corrente !== ultimoAnimato) {
        if (MOTO && animaPannello) animaPannello(pannelli[corrente], corrente > ultimoAnimato ? 1 : -1);
        ultimoAnimato = corrente;
      }
      aggiorna(corrente);
    }
    function vai(i, focus) {
      i = Math.max(0, Math.min(pannelli.length - 1, i));
      corrente = i;
      traccia.scrollTo({ left: i * traccia.clientWidth, behavior: RIDOTTO ? "instant" : "smooth" });
      aggiorna(i);
      if (focus) {
        var titolo = $("h3", pannelli[i]);
        if (titolo) titolo.focus({ preventScroll: true });
      }
    }
    traccia.addEventListener("scroll", leggi, { passive: true });
    traccia.addEventListener("keydown", function (event) {
      if (event.target !== traccia || (event.key !== "ArrowRight" && event.key !== "ArrowLeft")) return;
      event.preventDefault(); vai(corrente + (event.key === "ArrowRight" ? 1 : -1), false);
    });
    if (window.ResizeObserver) new ResizeObserver(function () {
      traccia.scrollTo({ left: corrente * traccia.clientWidth, behavior: "instant" }); leggi();
    }).observe(traccia);
    leggi();
    return { vai: vai, indice: function () { return corrente; } };
  }
  var vociServizi = $$(".servizio-editoriale"), comandiServizi = $$("[data-servizio-direzione]");
  var serviziApi = sfogliatore($(".servizi-editoriali-griglia"), vociServizi, function (i) {
    var stato = $("[data-servizio-posizione]"); if (stato) stato.textContent = (i + 1) + " / " + vociServizi.length;
    comandiServizi.forEach(function (b) { b.disabled = b.dataset.servizioDirezione === "-1" ? i === 0 : i === vociServizi.length - 1; });
  });
  comandiServizi.forEach(function (b) { b.addEventListener("click", function () { serviziApi.vai(serviziApi.indice() + Number(b.dataset.servizioDirezione), false); }); });
  var pannelliOrizzonte = $$(".orizzonte-pannello"), vociOrizzonte = $$("[data-orizzonte-vai]");
  var orizzonteApi = sfogliatore($(".orizzonte-traccia"), pannelliOrizzonte, function (i) {
    vociOrizzonte.forEach(function (a, k) { if (i === k) a.setAttribute("aria-current", "step"); else a.removeAttribute("aria-current"); });
  });
  vociOrizzonte.forEach(function (a, i) { a.addEventListener("click", function (event) { event.preventDefault(); event.stopPropagation(); orizzonteApi.vai(i, true); }); });

  if (!(window.gsap && window.ScrollTrigger)) return;

  /* ======================================================================
     Animazioni
     ====================================================================== */
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });
  var preferenzeMotion = gsap.matchMedia();
  function configuraMotion() {
  preferenzeMotion.revert();
  preferenzeMotion.add({ base: "all", ridotto: "(prefers-reduced-motion: reduce)" }, function (contestoMotion) {
  if (contestoMotion.conditions.ridotto && !FORZA_MOTO) {
    MOTO = false; RIDOTTO = true; H.classList.add("fermo", "salta");
    H.dataset.motionApertura = "ridotta";
    aggiornaComandoMotion();
    return;
  }
  MOTO = true; RIDOTTO = false; H.classList.remove("fermo");
  if (!SALTA) H.classList.remove("salta");
  aggiornaComandoMotion();
  var mm = gsap.matchMedia();
  var pulizieMotion = [], lenisTick, ancoraLenis;

  contestoMotion.add("cambioPannello", function (pannello, direzione) {
    var foto = $(".foto-editoriale", pannello);
    var testo = $(".orizzonte-testo, .servizio-editoriale-testo", pannello);
    if (foto) gsap.fromTo(foto, { clipPath: direzione > 0 ? "inset(0% 0% 0% 38%)" : "inset(0% 38% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: .8, ease: "power3.out", overwrite: true, clearProps: "clipPath" });
    if (testo) gsap.fromTo(testo, { x: direzione * 26, opacity: .5 }, { x: 0, opacity: 1, duration: .65, ease: "power3.out", overwrite: true, clearProps: "transform,opacity" });
  });
  animaPannello = contestoMotion.cambioPannello;

  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.12, smoothWheel: true });
    lenis.on("scroll", function (l) { ScrollTrigger.update(); suScroll(l.scroll); });
    lenisTick = function (t) { if (lenis) lenis.raf(t * 1000); };
    gsap.ticker.add(lenisTick, false, true);
    gsap.ticker.lagSmoothing(0);
    ancoraLenis = function (e) {
      var a = e.target.closest && e.target.closest('a[href*="#"]');
      if (!a) return;
      var url; try { url = new URL(a.getAttribute("href"), location.href); } catch (err) { return; }
      if (url.pathname !== location.pathname || url.hash.length < 2) return;
      var dest = document.getElementById(url.hash.slice(1));
      if (dest) { e.preventDefault(); lenis.scrollTo(dest, { offset: -90 }); }
    };
    document.addEventListener("click", ancoraLenis);
  }
  var scorriA = function (y) { if (lenis) lenis.scrollTo(y, { duration: 1.2 }); else window.scrollTo({ top: y, behavior: "smooth" }); };

  /* ---------- Ingresso: righe del titolo, testo, e l'auto che si disegna ---------- */
  var eroe = $(".eroe");
  var tracciati = eroe ? $$(".eroe .auto [data-draw]") : [];
  if (!SALTA) {
    tracciati.forEach(function (p) { var L = p.getTotalLength ? p.getTotalLength() : 0; if (L) { p.style.strokeDasharray = L; p.style.strokeDashoffset = L; p.setAttribute("data-len", L); } });
    $$(".eroe .auto .t-corpo, .eroe .auto .t-vetri").forEach(function (p) { p.style.fillOpacity = 0; });
  }
  var partito = false;
  function parti() {
    if (partito) return; partito = true;
    if (eroe && document.body.classList.contains("home")) {
      var apertura = gsap.timeline({ defaults: { ease: "expo.out" },
        onStart: function () { H.dataset.motionApertura = "in-corso"; },
        onComplete: function () { H.dataset.motionApertura = "pronta"; }
      });
      apertura.addLabel("accensione", 0)
        .fromTo(".eroe-anello", { rotation: -110, scale: .62, opacity: .35, transformOrigin: "50% 50%" }, { rotation: 0, scale: 1, opacity: 1, duration: 1.8, ease: "power3.out" }, "accensione")
        .fromTo(".eroe-finestra", { clipPath: "inset(49% 0% 49% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.2, clearProps: "clipPath" }, "accensione+=0.25")
        .fromTo(".eroe-finestra img", { scale: 1.35, yPercent: 8 }, { scale: 1, yPercent: 0, duration: 1.6, clearProps: "transform" }, "accensione+=0.25")
        .fromTo(".eroe-riga-a > span", { xPercent: -18, yPercent: 118, y: 0 }, { xPercent: 0, yPercent: 0, duration: 1.2 }, "accensione+=0.32")
        .fromTo(".eroe-riga-b > span", { xPercent: 14, yPercent: 118, y: 0 }, { xPercent: 0, yPercent: 0, duration: 1.2 }, "accensione+=0.52")
        .fromTo(".eroe-testo", { opacity: .35, y: 28 }, { opacity: 1, y: 0, duration: .8 }, "accensione+=0.7")
        .fromTo(".eroe-fascio", { xPercent: -180, opacity: 0 }, { xPercent: 520, opacity: 1, duration: 1.7, ease: "power1.inOut" }, "accensione+=0.1")
        .to(".eroe-fascio", { opacity: 0, duration: .35 }, "accensione+=1.5");
      avviaApertura = function () {
        SALTA = false; H.classList.remove("salta");
        apertura.restart();
      };
      return;
    }
    var tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    var righe = $$(".riga > span"), entra = $$("[data-entra]");
    if (righe.length) tl.fromTo(righe, { yPercent: 112, y: 0 }, { yPercent: 0, y: 0, duration: 1.1, stagger: .12 }, .05);
    if (entra.length) tl.fromTo(entra, { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: .9, stagger: .1 }, .45);
    var targa = $(".barra-targa .targa");
    if (targa) tl.fromTo(targa, { y: -40, rotation: -3, transformOrigin: "50% 0" }, { y: 0, rotation: 0, duration: 1.1, ease: "back.out(1.6)" }, .85);
    if (eroe) {
      tracciati.forEach(function (p, i) {
        tl.to(p, { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut", onComplete: function () { p.style.strokeDasharray = "none"; } }, .3 + i * .06);
      });
      var corpi = $$(".eroe .auto .t-corpo, .eroe .auto .t-vetri");
      if (corpi.length) tl.to(corpi, { fillOpacity: 1, duration: .9, ease: "power1.out" }, 1.4);
      var anello = $(".eroe-anello");
      if (anello) tl.fromTo(anello, { rotation: -24 }, { rotation: 0, duration: 1.4, ease: "power3.out" }, 0);
    }
    var intro = $(".intro-pagina .lead");
    if (intro) tl.fromTo(intro, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .9 }, .4);
  }
  if (!SALTA || document.body.classList.contains("home")) parti();

  // Il logo continua il movimento della prima demo, con uno scroll libero.
  var gearHero = $(".eroe-ingranaggio");
  if (gearHero) {
    gsap.to(gearHero, { rotation: 38, scale: 1.2, ease: "none", scrollTrigger: { trigger: eroe, start: "top top", end: "bottom top", scrub: .6 } });
  }

  /* Reportage prosegue l'apertura della demo con una fotografia ampia. */
  if ($(".eroe--reportage")) {
    gsap.to(".eroe-riga-a", { xPercent: -5, ease: "none", scrollTrigger: { trigger: eroe, start: "top top", end: "bottom top", scrub: .5 } });
    gsap.to(".eroe-riga-b", { xPercent: 5, ease: "none", scrollTrigger: { trigger: eroe, start: "top top", end: "bottom top", scrub: .5 } });
    var reportage = gsap.timeline({ scrollTrigger: { id: "reportage-apertura", trigger: ".reportage-finestra", start: "top 78%", once: true } });
    reportage.fromTo(".reportage-finestra", { clipPath: "inset(12% 42% 12% 42%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.25, ease: "expo.out", clearProps: "clipPath" }, 0)
      .fromTo(".reportage-finestra img", { scale: 1.18 }, { scale: 1, duration: 1.4, ease: "power3.out", clearProps: "transform" }, 0);
    var fotoServizi = $$(".servizio-editoriale-foto .foto-editoriale");
    gsap.fromTo(fotoServizi, { clipPath: "inset(0% 0% 94% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1, stagger: .14, ease: "expo.out", clearProps: "clipPath", scrollTrigger: { id: "servizi-apertura", trigger: ".servizi-editoriali-griglia", start: "top 84%", once: true } });
  }

  /* ---------- Comparse morbide (poche, solo dove aiutano) ---------- */
  var rivela = $$("[data-rivela], .finale-riga > *, .gomme-testo > *");
  rivela.forEach(function (el) { if (!el.hasAttribute("data-rivela")) gsap.set(el, { opacity: 0, y: 28 }); });
  if (rivela.length) ScrollTrigger.batch(rivela, { start: "top 90%", once: true, onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: 1.1, stagger: .1, ease: "expo.out" }); } });

  /* ---------- Il ponte: l'auto sale e i servizi si accendono uno dopo l'altro ---------- */
  if (ponteApi) {
    mm.add("(min-width: 900px)", function () {
      var n = ponteApi.n, FASE = 0.14;
      ponteApi.sale(0); ponteApi.seleziona(-1);
      var st = ScrollTrigger.create({
        trigger: $(".ponte-pin", ponte), start: "top top", end: function () { return "+=" + Math.round(window.innerHeight * (n * 0.62 + 0.9)); },
        pin: true, anticipatePin: 1, invalidateOnRefresh: true,
        onUpdate: function (self) {
          var p = self.progress, t = clamp(p / FASE, 0, 1);
          ponteApi.sale(1 - Math.pow(1 - t, 3));
          ponteApi.seleziona(p < FASE ? -1 : Math.min(n - 1, Math.floor((p - FASE) / (1 - FASE) * n)));
        }
      });
      ponteApi.vai = function (i) { scorriA(st.start + (FASE + (i + .5) / n * (1 - FASE)) * (st.end - st.start)); };
      return function () { ponteApi.vai = function (i) { ponteApi.seleziona(i); }; ponteApi.sale(1); };
    });
    mm.add("(max-width: 899px)", function () {
      var v = { t: 0 };
      ponteApi.sale(0); ponteApi.seleziona(0);
      ScrollTrigger.create({ trigger: $(".ponte-disegno", ponte), start: "top 80%", once: true, onEnter: function () {
        gsap.to(v, { t: 1, duration: 1.6, ease: "power3.out", onUpdate: function () { ponteApi.sale(v.t); } });
      } });
    });
  }

  /* ---------- Gomme: il prodotto si posa nel suo spazio, senza ruotare ---------- */
  var prodottoGomma = $(".gomma-foto");
  if (prodottoGomma) gsap.fromTo(prodottoGomma, { x: 46, scale: .82, opacity: .5 }, { x: 0, scale: 1, opacity: 1, duration: 1.25, ease: "expo.out", clearProps: "transform,opacity", scrollTrigger: { trigger: prodottoGomma, start: "top 84%", once: true } });

  /* ---------- Officina: l'indice segue la lettura ---------- */
  $$(".dettaglio").forEach(function (sez) {
    var voce = $('.indice a[href="#' + sez.id + '"]'); if (!voce) return;
    ScrollTrigger.create({ trigger: sez, start: "top 45%", end: "bottom 45%", onToggle: function (s) { voce.classList.toggle("attivo", s.isActive); } });
  });

  /* ---------- Pulsanti magnetici (solo mouse) ---------- */
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    $$(".btn--arancio").forEach(function (b) {
      var mx = gsap.quickTo(b, "x", { duration: .4, ease: "power3" }), my = gsap.quickTo(b, "y", { duration: .4, ease: "power3" });
      var muovi = function (e) { if (!MOTO) return; var r = b.getBoundingClientRect(); mx((e.clientX - r.left - r.width / 2) * .25); my((e.clientY - r.top - r.height / 2) * .35); };
      var lascia = function () { if (MOTO) gsap.to(b, { x: 0, y: 0, duration: .5, ease: MOTION.ease }); };
      b.addEventListener("pointermove", muovi);
      b.addEventListener("pointerleave", lascia);
      pulizieMotion.push(function () { b.removeEventListener("pointermove", muovi); b.removeEventListener("pointerleave", lascia); });
    });
  }

  /* ---------- Posizioni: un ricalcolo quando font e immagini sono pronti ---------- */
  var ric = function () { ScrollTrigger.refresh(); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(ric, 100); });
  window.addEventListener("load", function () { setTimeout(ric, 200); });

  return function () {
    MOTO = false; RIDOTTO = true; H.classList.add("fermo");
    avviaApertura = null; animaPannello = null;
    mm.revert();
    pulizieMotion.forEach(function (pulisci) { pulisci(); });
    if (ancoraLenis) document.removeEventListener("click", ancoraLenis);
    if (lenisTick) gsap.ticker.remove(lenisTick);
    if (lenis) { lenis.destroy(); lenis = null; }
    gsap.killTweensOf(".foglio form");
    gsap.set(".foglio form", { clearProps: "transform,opacity" });
  };
  });
  }
  configuraMotion();
  if (ripetiApertura) ripetiApertura.addEventListener("click", function () {
    if (!MOTO) { FORZA_MOTO = true; SALTA = false; configuraMotion(); }
    else if (avviaApertura) avviaApertura();
  });

})();
