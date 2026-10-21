/* Preparazione locale del messaggio: il cliente conferma l'invio in WhatsApp. */
(function () {
  "use strict";
  document.querySelectorAll("[data-richiesta-guidata]").forEach(function (form) {
    var campi = form.elements;
    var anteprima = form.querySelector("[data-rqs-anteprima]");
    var errore = form.querySelector(".rqs-errore");
    var esito = form.querySelector("[data-rqs-esito]");
    var passi = Array.from(form.querySelectorAll("[data-rqs-passo]"));
    var avanti = form.querySelector("[data-rqs-avanti]");
    var indietro = form.querySelector("[data-rqs-indietro]");
    var posizione = form.querySelector("[data-rqs-posizione]");
    var corrente = 0;
    function mostraPasso(indice, focus) {
      if (!passi.length) return;
      corrente = indice;
      passi.forEach(function (p, i) { p.hidden = i !== indice; });
      avanti.hidden = indice === passi.length - 1;
      indietro.hidden = indice === 0;
      posizione.textContent = (indice + 1) + " di 3 · " + ["Auto e servizio", "Come organizzarci", "Dettagli e messaggio"][indice];
      if (focus) {
        var campo = passi[indice].querySelector("select,input,textarea,button");
        if (campo) campo.focus({ preventScroll: true });
      }
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    }
    function problemaValido() {
      if (campi.problema.value) return true;
      mostraPasso(0, false);
      campi.problema.setAttribute("aria-invalid", "true");
      errore.textContent = "Scegli il servizio o il problema. Se non lo sai, seleziona «Altro / non so quale sia il problema».";
      errore.hidden = false;
      campi.problema.focus({ preventScroll: true });
      return false;
    }
    if (avanti) avanti.addEventListener("click", function () { if (problemaValido()) mostraPasso(Math.min(2, corrente + 1), true); });
    if (indietro) indietro.addEventListener("click", function () { mostraPasso(Math.max(0, corrente - 1), true); });
    form.addEventListener("rqs:inizio", function () { if (passi.length) mostraPasso(0, false); });

    function testo() {
      if (!campi.problema.value) return "";
      var righe = ["Ciao Luca, vorrei informazioni sui tuoi servizi.", "", "Richiesta: " + campi.problema.value];
      var auto = campi.auto.value.trim(), comune = campi.comune.value.trim(), dettagli = campi.dettagli.value.trim();
      if (auto) righe.push("Auto: " + auto);
      if (comune) righe.push("Comune: " + comune);
      righe.push("Preferenza: " + campi.modalita.value);
      if (dettagli) righe.push("", "Dettagli: " + dettagli);
      righe.push("", "Possiamo concordare come procedere? Grazie.");
      return righe.join("\n");
    }

    function aggiorna() {
      anteprima.textContent = testo() || "Scegli il servizio o il problema: il messaggio comparirà qui.";
      esito.hidden = true;
      esito.replaceChildren();
      if (campi.problema.value) {
        campi.problema.removeAttribute("aria-invalid");
        errore.hidden = true;
        errore.textContent = "";
      }
    }
    form.addEventListener("input", aggiorna);
    form.addEventListener("change", aggiorna);
    var anteprimaApribile = form.querySelector("details.rqs-anteprima");
    if (anteprimaApribile) anteprimaApribile.addEventListener("toggle", function () {
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!problemaValido()) return;
      if (passi.length && corrente !== 2) { mostraPasso(corrente + 1, true); return; }
      var messaggio = testo();
      var url = "https://wa.me/" + form.getAttribute("data-telefono-wa") + "?text=" + encodeURIComponent(messaggio);
      esito.hidden = false;
      esito.textContent = "La richiesta è pronta. Se WhatsApp non si apre, ";
      var riprova = document.createElement("a");
      riprova.href = url;
      riprova.target = "_blank";
      riprova.rel = "noopener";
      riprova.textContent = "apri il messaggio da qui";
      esito.appendChild(riprova);
      esito.appendChild(document.createTextNode(". L'invio lo confermi tu."));
      window.open(url, "_blank", "noopener");
    });
    aggiorna();
    // Ripristina l'anteprima anche tornando alla pagina dalla cache del browser.
    window.addEventListener("pageshow", aggiorna);
  });
})();
