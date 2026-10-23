/* L.M. Autoservizi, versione semplice.
   Librerie locali: GSAP + ScrollTrigger per le animazioni legate allo scorrimento, Lenis per lo scroll morbido.
   La tendina e le finestre usano le Web Animations: GSAP sposta nel DOM gli elementi fixed per misurarli
   e un <dialog> aperto perderebbe lo stato modale.
   Tutti i messaggi si preparano in locale: l'invio lo conferma il cliente in WhatsApp. */
(function () {
  "use strict";
  var H = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var TEL_WA = "393426436085";
  var ESCE = "cubic-bezier(.16, 1, .3, 1)";
  var RIDOTTO = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MOTO = !!(window.gsap && window.ScrollTrigger) && !RIDOTTO;
  // Gli stati iniziali esistono solo sotto .mo; se il paracadute di 4 secondi l'ha già tolta, niente entrate.
  var ENTRATA = MOTO && H.classList.contains("mo");
  var WAAPI = !RIDOTTO && !!document.body.animate;
  var telefono = matchMedia("(max-width: 599px)");
  var lenis = null;

  var TESTI = {
    it: {
      giorni: ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"],
      aperto: "Aperto ora, fino alle ", apre: "Chiuso, apre alle ", riapre: "Chiuso, riapre ", domani: "domani", alle: " alle ", chiuso: "Chiuso",
      ciao: "Ciao Luca, ti scrivo dal sito.", servizio: "Servizio: ", mezzo: "Mezzo: ",
      pronto: "Messaggio pronto: premi Invia in WhatsApp. Se non si è aperto, ", apriQui: "aprilo da qui",
      misura: "Misura: ", erroreMisura: "Scrivi la misura completa, per esempio 205 / 55 / 16.", errorePezzo: "Scrivi quale pezzo ti serve.",
      esempioMisura: "Esempio di misura", tuaMisura: "La misura che cerchi",
      apriMenu: "Apri il menu", chiudiMenu: "Chiudi il menu",
      temaChiaro: "Passa al tema chiaro", temaScuro: "Passa al tema scuro", breveChiaro: "Tema chiaro", breveScuro: "Tema scuro"
    },
    en: {
      giorni: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      aperto: "Open now, until ", apre: "Closed, opens at ", riapre: "Closed, reopens ", domani: "tomorrow", alle: " at ", chiuso: "Closed",
      ciao: "Hi Luca, I'm writing from your website.", servizio: "Service: ", mezzo: "Vehicle: ",
      pronto: "Message ready: tap Send in WhatsApp. If it didn't open, ", apriQui: "open it here",
      misura: "Size (misura): ", erroreMisura: "Enter the full size, for example 205 / 55 / 16.", errorePezzo: "Tell me which part you need.",
      esempioMisura: "Example size", tuaMisura: "Your size",
      apriMenu: "Open the menu", chiudiMenu: "Close the menu",
      temaChiaro: "Switch to light theme", temaScuro: "Switch to dark theme", breveChiaro: "Light theme", breveScuro: "Dark theme"
    }
  };
  var T = TESTI[H.lang === "en" ? "en" : "it"];

  function anima(el, fotogrammi, opzioni) {
    if (!WAAPI || !el) return null;
    return el.animate(fotogrammi, opzioni);
  }
  function wa(testo) { return "https://wa.me/" + TEL_WA + "?text=" + encodeURIComponent(testo); }
  // Nelle pagine inglesi Luca legge anche il nome italiano, tra parentesi.
  function conItaliano(valore, italiano) { return italiano && italiano !== valore ? valore + " (" + italiano + ")" : valore; }
  function esitoPronto(el, url) {
    el.hidden = false;
    el.textContent = T.pronto;
    var a = document.createElement("a");
    a.href = url; a.target = "_blank"; a.rel = "noopener"; a.textContent = T.apriQui;
    el.appendChild(a);
    el.appendChild(document.createTextNode("."));
  }

  /* ---------- aperto / chiuso in ora italiana ---------- */
  var ORARI = { 1: [450, 1170], 2: [450, 1170], 3: [450, 1170], 4: [450, 1170], 5: [450, 1170] };
  function oraItalia() {
    var mappa = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, g = 0, h = 0, m = 0;
    new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false })
      .formatToParts(new Date()).forEach(function (p) {
        if (p.type === "weekday") g = mappa[p.value];
        if (p.type === "hour") h = parseInt(p.value, 10) % 24;
        if (p.type === "minute") m = parseInt(p.value, 10);
      });
    return { giorno: g, minuti: h * 60 + m };
  }
  function hhmm(min) { return Math.floor(min / 60) + ":" + String(min % 60).padStart(2, "0"); }
  function aggiornaStato() {
    var ora = oraItalia(), oggi = ORARI[ora.giorno], s = { aperto: false, testo: T.chiuso };
    if (oggi && ora.minuti >= oggi[0] && ora.minuti < oggi[1]) s = { aperto: true, testo: T.aperto + hhmm(oggi[1]) };
    else if (oggi && ora.minuti < oggi[0]) s = { aperto: false, testo: T.apre + hhmm(oggi[0]) };
    else {
      for (var i = 1; i <= 7; i++) {
        var g = (ora.giorno + i) % 7;
        if (ORARI[g]) { s = { aperto: false, testo: T.riapre + (i === 1 ? T.domani : T.giorni[g]) + T.alle + hhmm(ORARI[g][0]) }; break; }
      }
    }
    $$("[data-stato]").forEach(function (el) { el.textContent = s.testo; el.setAttribute("data-aperto", s.aperto ? "si" : "no"); });
    $$(".orari tr[data-giorni]").forEach(function (tr) { tr.classList.toggle("oggi", tr.getAttribute("data-giorni").split(",").map(Number).indexOf(ora.giorno) !== -1); });
  }
  aggiornaStato();
  setInterval(aggiornaStato, 60000);
  $$("[data-anno]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- tema chiaro / scuro ---------- */
  var bottoniTema = $$("[data-tema-bottone]");
  function segnaTema(chiaro) {
    bottoniTema.forEach(function (b) { b.setAttribute("aria-label", chiaro ? T.temaScuro : T.temaChiaro); });
    $$("[data-tema-testo]").forEach(function (el) { el.textContent = chiaro ? T.breveScuro : T.breveChiaro; });
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.content = chiaro ? "#f3f4f6" : "#0b0d10";
  }
  function applicaTema(chiaro) {
    if (chiaro) H.setAttribute("data-tema", "chiaro"); else H.removeAttribute("data-tema");
    segnaTema(chiaro);
    try { localStorage.setItem("lm-tema", chiaro ? "chiaro" : "scuro"); } catch (e) { /* senza memoria il tema vale per questa pagina */ }
  }
  segnaTema(H.getAttribute("data-tema") === "chiaro");
  bottoniTema.forEach(function (b) {
    b.addEventListener("click", function () {
      var chiaro = H.getAttribute("data-tema") !== "chiaro";
      if (!document.startViewTransition || RIDOTTO) { applicaTema(chiaro); return; }
      // il nuovo tema si allarga a cerchio partendo dal pulsante
      var r = b.getBoundingClientRect();
      H.style.setProperty("--tema-x", (r.left + r.width / 2) + "px");
      H.style.setProperty("--tema-y", (r.top + r.height / 2) + "px");
      H.classList.add("cambio-tema");
      document.startViewTransition(function () { applicaTema(chiaro); }).finished.finally(function () { H.classList.remove("cambio-tema"); });
    });
  });

  /* ---------- testata e barra rapida ---------- */
  var testata = $(".testata"), barra = $(".barra"), menu = $("#menu"), bottoneMenu = $(".menu-bottone"), scheda = $("#scheda");
  var ultimoY = 0;
  function bloccata() { return document.body.classList.contains("menu-aperto") || (scheda && scheda.open); }
  function suScroll(y) {
    if (bloccata()) return;
    testata.classList.toggle("is-piena", y > 24);
    testata.classList.toggle("is-nascosta", y > ultimoY && y > 420);
    ultimoY = y;
  }
  suScroll(window.scrollY);
  window.addEventListener("scroll", function () { if (!lenis) suScroll(window.scrollY); }, { passive: true });
  function nascondiBarra(si) { if (barra) barra.classList.toggle("is-nascosta", si); }

  /* ---------- menu del telefono ---------- */
  function chiudiMenu(rifocus) {
    if (!menu || menu.hidden) return;
    menu.hidden = true;
    document.body.classList.remove("menu-aperto");
    bottoneMenu.setAttribute("aria-expanded", "false");
    bottoneMenu.setAttribute("aria-label", T.apriMenu);
    if (lenis) lenis.start();
    nascondiBarra(false);
    if (rifocus) bottoneMenu.focus();
  }
  if (menu && bottoneMenu) {
    bottoneMenu.addEventListener("click", function () {
      if (!menu.hidden) { chiudiMenu(false); return; }
      menu.hidden = false;
      document.body.classList.add("menu-aperto");
      testata.classList.remove("is-nascosta");
      bottoneMenu.setAttribute("aria-expanded", "true");
      bottoneMenu.setAttribute("aria-label", T.chiudiMenu);
      if (lenis) lenis.stop();
      nascondiBarra(true);
      $$("li, .menu-piede", menu).forEach(function (el, i) {
        anima(el, [{ opacity: 0, transform: "translateY(18px)" }, { opacity: 1, transform: "none" }], { duration: 520, delay: 40 + i * 45, easing: ESCE, fill: "backwards" });
      });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !menu.hidden) chiudiMenu(true); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { chiudiMenu(false); }); });
    matchMedia("(min-width: 1240px)").addEventListener("change", function (e) { if (e.matches) chiudiMenu(false); });
  }

  /* ---------- tendina "scrivi a Luca" ---------- */
  if (scheda) {
    var form = $("form", scheda), titolo = $("#scheda-t", scheda), mezzi = $("[data-mezzi]", scheda);
    var note = form.elements.note, aiuto = $("[data-aiuto]", scheda), esito = $("[data-esito]", scheda);
    var testoEsito = esito.textContent;
    var servizio = "", servizioIt = "", nota = "", senzaMezzo = false, origine = null, chiudendo = false;

    var mezzoScelto = function () { return $("input[name='mezzo']:checked", scheda); };
    var messaggio = function () {
      var righe = [T.ciao, "", T.servizio + conItaliano(servizio, servizioIt)];
      if (!senzaMezzo) { var m = mezzoScelto(); righe.push(T.mezzo + conItaliano(m.value, m.getAttribute("data-it"))); }
      var n = note.value.trim();
      if (n) righe.push("", n);
      return righe.join("\n");
    };
    var aggiorna = function () {
      note.placeholder = nota;
      aiuto.textContent = senzaMezzo ? "" : mezzoScelto().getAttribute("data-consiglio");
    };

    var apri = function (b) {
      var nuovo = b.getAttribute("data-servizio");
      if (nuovo !== servizio) note.value = "";
      servizio = nuovo;
      servizioIt = b.getAttribute("data-servizio-it") || "";
      nota = b.getAttribute("data-nota") || "";
      senzaMezzo = b.hasAttribute("data-senza-mezzo");
      titolo.textContent = b.getAttribute("data-titolo") || servizio;
      mezzi.hidden = senzaMezzo;
      scheda.classList.toggle("is-urgente", b.hasAttribute("data-urgente"));
      esito.textContent = testoEsito;
      aggiorna();
      origine = b;
      if (typeof scheda.showModal !== "function") { window.open(wa(messaggio()), "_blank", "noopener"); return; }
      scheda.showModal();
      // il focus parte dal titolo: chi usa la tastiera prosegue con Tab, a chi usa il mouse non compare un secondo contorno
      titolo.focus({ preventScroll: true });
      if (lenis) lenis.stop();
      nascondiBarra(true);
      if (!WAAPI) return;
      if (telefono.matches) {
        anima(scheda, [{ transform: "translateY(100%)" }, { transform: "none" }], { duration: 560, easing: ESCE });
      } else {
        // FLIP: la tendina nasce dal pulsante toccato
        var da = b.getBoundingClientRect(), a = scheda.getBoundingClientRect();
        var parte = "translate(" + (da.left - a.left) + "px," + (da.top - a.top) + "px) scale(" + Math.max(.05, da.width / a.width) + "," + Math.max(.05, da.height / a.height) + ")";
        anima(scheda, [{ transform: parte, transformOrigin: "0 0", borderRadius: "24px", opacity: .6 }, { transform: "none", transformOrigin: "0 0", borderRadius: "24px", opacity: 1 }], { duration: 620, easing: ESCE });
      }
      [$(".scheda-testa", scheda), $(".scheda-corpo", scheda)].forEach(function (el, i) {
        anima(el, [{ opacity: 0, transform: "translateY(14px)" }, { opacity: 1, transform: "none" }], { duration: 460, delay: 150 + i * 60, easing: ESCE, fill: "backwards" });
      });
    };

    var chiudi = function () {
      if (!scheda.open || chiudendo) return;
      if (!WAAPI) { scheda.close(); return; }
      chiudendo = true;
      var uscita = anima(scheda, telefono.matches
        ? [{ transform: "none" }, { transform: "translateY(100%)" }]
        : [{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(18px) scale(.97)" }],
        { duration: telefono.matches ? 300 : 220, easing: "cubic-bezier(.5, 0, .75, 0)", fill: "forwards" });
      uscita.onfinish = function () { chiudendo = false; scheda.close(); uscita.cancel(); };
    };

    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-servizio]");
      if (b && !scheda.contains(b)) { e.preventDefault(); apri(b); }
    });
    $("[data-chiudi]", scheda).addEventListener("click", chiudi);
    scheda.addEventListener("cancel", function (e) { e.preventDefault(); chiudi(); });
    scheda.addEventListener("click", function (e) { if (e.target === scheda) chiudi(); });
    scheda.addEventListener("close", function () {
      if (lenis) lenis.start();
      nascondiBarra(false);
      if (origine) origine.focus({ preventScroll: true });
    });
    form.addEventListener("change", aggiorna);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var url = wa(messaggio());
      window.open(url, "_blank", "noopener");
      esitoPronto(esito, url);
    });
  }

  /* ---------- moduli gomme e ricambi: diventano un messaggio WhatsApp ---------- */
  $$(".targa-campo").forEach(function (c) {
    c.addEventListener("input", function () { var v = c.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 8); if (v !== c.value) c.value = v; });
  });
  function controlla(campo) {
    var v = (campo.value || "").trim(), t = "";
    var misura = campo.closest(".misura");
    if (misura && !/^\d+$/.test(v)) t = T.erroreMisura;
    else if (!misura && campo.required && !v) t = T.errorePezzo;
    campo.setAttribute("aria-invalid", t ? "true" : "false");
    var box = campo.closest(".campo"), errore = box && $(".errore", box);
    if (errore && (!misura || t || $$("input", misura).every(function (x) { return x.getAttribute("aria-invalid") !== "true"; }))) errore.textContent = t;
    return !t;
  }
  $$("form[data-wa]").forEach(function (form) {
    var obbligatori = $$("[required]", form), esito = $(".esito", form);
    obbligatori.forEach(function (c) {
      c.addEventListener("input", function () { if (c.hasAttribute("aria-invalid")) controlla(c); });
      c.addEventListener("blur", function () { if (c.value) controlla(c); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var primo = null;
      obbligatori.forEach(function (c) { if (!controlla(c) && !primo) primo = c; });
      if (primo) { primo.focus(); return; }
      var f = form.elements, righe = [form.getAttribute("data-intro"), ""];
      if (f.larghezza) righe.push(T.misura + f.larghezza.value + "/" + f.spalla.value + " R" + f.cerchio.value);
      $$("[data-etichetta]", form).forEach(function (c) {
        var v = (c.value || "").trim();
        if (v) righe.push(c.getAttribute("data-etichetta") + ": " + v);
      });
      var url = wa(righe.join("\n"));
      window.open(url, "_blank", "noopener");
      if (esito) esitoPronto(esito, url);
    });
  });
  // La misura scritta compare accanto al pneumatico
  var testoMisura = $("[data-misura-testo]"), etichettaMisura = $("[data-misura-etichetta]");
  $$(".misura").forEach(function (gruppo) {
    var campi = $$("input", gruppo);
    var agg = function (animata) {
      var vuota = campi.every(function (c) { return !c.value; });
      if (testoMisura) testoMisura.textContent = vuota ? "205/55 R16" : (campi[0].value || "—") + "/" + (campi[1].value || "—") + " R" + (campi[2].value || "—");
      if (etichettaMisura) etichettaMisura.textContent = vuota ? T.esempioMisura : T.tuaMisura;
      if (animata) anima(testoMisura, [{ transform: "translateY(4px)", opacity: .5 }, { transform: "none", opacity: 1 }], { duration: 260, easing: ESCE });
    };
    campi.forEach(function (c, i) {
      c.addEventListener("input", function () {
        c.value = c.value.replace(/\D/g, "");
        agg(true);
        if (c.value.length >= c.maxLength && campi[i + 1]) campi[i + 1].focus();
      });
    });
    agg(false);
    window.addEventListener("pageshow", function () { agg(false); });
  });

  /* ---------- attestati a grandezza piena ---------- */
  var lightbox = $("#lightbox");
  if (lightbox && typeof lightbox.showModal === "function") {
    // l'immagine nasce al primo clic: nella pagina non resta un <img> senza sorgente
    var lbImg = document.createElement("img"), lbCap = $("figcaption", lightbox), lbOrigine = null;
    lbImg.decoding = "async";
    $("figure", lightbox).insertBefore(lbImg, lbCap);
    $$("[data-lightbox]").forEach(function (b) {
      b.addEventListener("click", function () {
        lbOrigine = b;
        lbImg.src = b.getAttribute("data-lightbox");
        lbImg.alt = b.getAttribute("data-titolo");
        lbCap.textContent = b.getAttribute("data-titolo");
        lightbox.showModal();
        if (lenis) lenis.stop();
        anima($("figure", lightbox), [{ opacity: 0, transform: "scale(.92) translateY(16px)" }, { opacity: 1, transform: "none" }], { duration: 480, easing: ESCE });
      });
    });
    $("[data-chiudi]", lightbox).addEventListener("click", function () { lightbox.close(); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.close(); });
    lightbox.addEventListener("close", function () {
      lbImg.removeAttribute("src");
      if (lenis) lenis.start();
      if (lbOrigine) lbOrigine.focus({ preventScroll: true });
    });
  }

  /* ---------- caselle: il cerchio della foto parte da dove entra il puntatore ---------- */
  $$(".servizio").forEach(function (b) {
    b.addEventListener("pointerenter", function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty("--x", (e.clientX - r.left) + "px");
      b.style.setProperty("--y", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- pagina servizi: indice che segue la lettura, icona che si anima entrando ---------- */
  var sezioni = $$(".sezione-servizio");
  if (sezioni.length) {
    var vociIndice = $$(".indice a"), attiva = null, inAttesa = false;
    var aggiornaIndice = function () {
      inAttesa = false;
      var soglia = window.innerHeight * .42, corrente = null;
      sezioni.forEach(function (s) { if (s.getBoundingClientRect().top < soglia) corrente = s; });
      if (corrente === attiva) return;
      attiva = corrente;
      vociIndice.forEach(function (a) {
        var si = !!corrente && a.getAttribute("href") === "#" + corrente.id;
        a.classList.toggle("attivo", si);
        if (si) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
      // l'icona del servizio fa la sua piccola animazione la prima volta che lo raggiungi
      if (corrente && !RIDOTTO && !corrente.dataset.animata) {
        corrente.dataset.animata = "1";
        corrente.classList.add("anima");
        setTimeout(function () { corrente.classList.remove("anima"); }, 1400);
      }
    };
    window.addEventListener("scroll", function () { if (!inAttesa) { inAttesa = true; requestAnimationFrame(aggiornaIndice); } }, { passive: true });
    aggiornaIndice();
  }

  if (!MOTO) {
    H.classList.remove("mo");
    return;
  }

  /* ======================================================================
     Movimento (GSAP + ScrollTrigger + Lenis)
     ====================================================================== */
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });

  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.12, smoothWheel: true });
    lenis.on("scroll", function (l) { ScrollTrigger.update(); suScroll(l.scroll); });
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length < 2 || !$(id)) return;
        e.preventDefault();
        lenis.scrollTo(id, { offset: -88, duration: 1.2 });
        history.replaceState(null, "", id);
      });
    });
    if (location.hash && $(location.hash)) setTimeout(function () { lenis.scrollTo(location.hash, { offset: -88, immediate: true }); }, 60);
  }

  var mm = gsap.matchMedia();

  // Home: l'anello gira, la finestra si apre sull'officina, il titolo sale, passa un fascio di luce.
  if ($(".eroe")) {
    if (ENTRATA) {
      gsap.timeline({ defaults: { ease: "expo.out" }, onStart: function () { H.classList.remove("mo"); } })
        .fromTo(".eroe-anello", { rotation: -110, scale: .62, opacity: .35, transformOrigin: "50% 50%" }, { rotation: 0, scale: 1, opacity: 1, duration: 1.8, ease: "power3.out" }, 0)
        .fromTo(".eroe-aloni", { scale: .8, opacity: 0 }, { scale: 1, opacity: 1, duration: 1.6 }, .2)
        .fromTo(".eroe-finestra", { clipPath: "inset(49% 0% 49% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.2, clearProps: "clipPath" }, .25)
        .fromTo(".eroe-finestra img", { scale: 1.35, yPercent: 8 }, { scale: 1, yPercent: 0, duration: 1.6, clearProps: "transform" }, .25)
        .fromTo(".riga-a > span", { xPercent: -18, yPercent: 115, y: 0 }, { xPercent: 0, yPercent: 0, y: 0, duration: 1.2 }, .32)
        .fromTo(".riga-b > span", { xPercent: 14, yPercent: 115, y: 0 }, { xPercent: 0, yPercent: 0, y: 0, duration: 1.2 }, .5)
        .fromTo(".eroe-testo", { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: .9 }, .75)
        .fromTo(".eroe-info", { opacity: 0 }, { opacity: 1, duration: .9 }, 1)
        .fromTo(".eroe-fascio", { xPercent: -180, opacity: 0 }, { xPercent: 520, opacity: 1, duration: 1.7, ease: "power1.inOut" }, .1)
        .to(".eroe-fascio", { opacity: 0, duration: .35 }, 1.5);
    }
    gsap.to(".eroe-ingranaggio", { rotation: 40, scale: 1.18, ease: "none", scrollTrigger: { trigger: ".eroe", start: "top top", end: "bottom top", scrub: .6 } });
    mm.add("(min-width: 900px)", function () {
      gsap.to(".riga-a", { xPercent: -6, ease: "none", scrollTrigger: { trigger: ".eroe", start: "top top", end: "bottom top", scrub: .5 } });
      gsap.to(".riga-b", { xPercent: 6, ease: "none", scrollTrigger: { trigger: ".eroe", start: "top top", end: "bottom top", scrub: .5 } });
    });
  }

  // Pagine interne: il titolo sale, l'ingranaggio entra girando e continua a girare con lo scorrimento.
  if ($(".intro")) {
    if (ENTRATA) {
      gsap.timeline({ defaults: { ease: "expo.out" }, onStart: function () { H.classList.remove("mo"); } })
        .fromTo(".intro .riga > span", { yPercent: 110, y: 0 }, { yPercent: 0, y: 0, duration: 1.15 }, .05)
        .fromTo(".intro-lead", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .9 }, .35)
        .fromTo(".intro-ingranaggio svg", { rotation: -70, scale: .82, opacity: 0, transformOrigin: "50% 50%" }, { rotation: 0, scale: 1, opacity: 1, duration: 1.8, ease: "power3.out" }, 0);
    }
    gsap.to(".intro-ingranaggio", { rotation: 55, ease: "none", scrollTrigger: { trigger: ".intro", start: "top top", end: "bottom top", scrub: .6 } });
  }

  // Le foto principali si aprono come la finestra dell'ingranaggio.
  $$("[data-iride]").forEach(function (fig) {
    var immagine = $("img", fig);
    gsap.timeline({ scrollTrigger: { trigger: fig, start: "top 82%", once: true } })
      .fromTo(fig, { clipPath: "circle(14% at 50% 50%)" }, { clipPath: "circle(75% at 50% 50%)", duration: 1.4, ease: "expo.inOut", clearProps: "clipPath" })
      .fromTo(immagine, { scale: 1.3, rotation: -4 }, { scale: 1, rotation: 0, duration: 1.6, ease: "expo.out", clearProps: "transform" }, 0);
  });

  // Le caselle dei servizi arrivano una dopo l'altra.
  $$(".servizi-griglia").forEach(function (griglia) {
    gsap.from($$(":scope > li", griglia), { y: 40, opacity: 0, scale: .96, duration: .9, stagger: .07, ease: "expo.out", clearProps: "transform,opacity",
      scrollTrigger: { trigger: griglia, start: "top 88%", once: true } });
  });

  // Le icone dei vantaggi si disegnano a tratto.
  $$(".vantaggi-lista > li > .ico").forEach(function (icona) {
    var tratti = $$("path, circle, rect", icona);
    tratti.forEach(function (p) { var L = p.getTotalLength ? p.getTotalLength() : 0; if (L) gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
    gsap.to(tratti, { strokeDashoffset: 0, duration: 1.3, stagger: .08, ease: "power2.inOut",
      scrollTrigger: { trigger: icona, start: "top 90%", once: true },
      onComplete: function () { gsap.set(tratti, { clearProps: "strokeDasharray,strokeDashoffset" }); } });
  });

  // Ritiro e consegna: la linea scende con lo scorrimento e ogni tappa si accende quando la linea la raggiunge.
  // Parte solo quando il percorso sale oltre il 40% dello schermo, così all'apertura (anche sul telefono) è tutto spento.
  var percorso = $("[data-percorso]");
  if (percorso) {
    percorso.classList.add("in-scorrimento");
    var tappe = $$(".tappa", percorso), soglie = [];
    var misuraSoglie = function () {
      var corsa = Math.max(1, percorso.offsetHeight - 44);
      soglie = tappe.map(function (t, i) { return Math.max(.02, i === 0 ? 0 : t.offsetTop / corsa); });
    };
    misuraSoglie();
    gsap.fromTo(".percorso-linea span", { scaleY: 0 }, { scaleY: 1, ease: "none",
      scrollTrigger: { trigger: percorso, start: "top 40%", end: "bottom 45%", scrub: .4, onRefresh: misuraSoglie },
      onUpdate: function () {
        var p = this.progress();
        tappe.forEach(function (t, i) { t.classList.toggle("attiva", p >= soglie[i]); });
      } });
  }

  // Chi sono: la linea della cronologia scende con lo scorrimento, gli anni compaiono in ordine.
  var cronologia = $("[data-cronologia]");
  if (cronologia) {
    cronologia.classList.add("in-scorrimento");
    gsap.fromTo(cronologia, { "--linea-crono": 0 }, { "--linea-crono": 1, ease: "none", scrollTrigger: { trigger: cronologia, start: "top 80%", end: "bottom 60%", scrub: .4 } });
    gsap.from($$("li", cronologia), { opacity: 0, x: -18, duration: .9, stagger: .15, ease: "expo.out", clearProps: "opacity,transform",
      scrollTrigger: { trigger: cronologia, start: "top 80%", once: true } });
  }

  window.addEventListener("load", function () { ScrollTrigger.refresh(); });
})();
