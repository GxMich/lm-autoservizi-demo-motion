"""Modulo condiviso dalle due home: scelta del problema e messaggio WhatsApp."""
from hashlib import sha256
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent / "docs"


def risorse_richiesta(prefisso=""):
    versione = sha256(b"".join((RADICE / f).read_bytes() for f in
        ("assets/css/richiesta.css", "assets/js/richiesta.js"))).hexdigest()[:10]
    return f'''<link rel="stylesheet" href="{prefisso}assets/css/richiesta.css?v={versione}">
<script src="{prefisso}assets/js/richiesta.js?v={versione}" defer></script>'''


def opzioni_problema(sede_fissa=False):
    opzioni = ["Batteria o auto che non parte", "Spie accese e diagnosi", "Tagliando e manutenzione",
               "Freni, rumori o vibrazioni", "Gomme e forature", "Carrozzeria", "Pre-revisione"]
    if sede_fissa:
        opzioni += ["Climatizzatore", "Acquisto gomme", "Acquisto ricambi", "Consulenza alle imprese"]
    opzioni += ["Altro / non so quale sia il problema"]
    return '<option value="">Scegli il servizio o il tipo di problema</option>' + "".join(
        f'<option>{voce}</option>' for voce in opzioni)


def sezione_richiesta(sede_fissa=False):
    modalita = (["La porto in officina", "Ritiro e consegna", "Solo informazioni o acquisto", "Da valutare insieme"] if sede_fissa else
                ["Intervento sul posto", "Ritiro e consegna", "Da valutare insieme"])
    scelte = "".join(f'<label><input type="radio" name="modalita" value="{voce}"'
        f'{" checked" if i == 0 else ""}><span>{voce}</span></label>' for i, voce in enumerate(modalita))
    titolo = "Dimmi cosa ti serve." if sede_fissa else "Dimmi cosa non va."
    return f'''
<section class="richiesta" id="richiesta" aria-labelledby="richiesta-titolo">
  <div class="wrap rqs-griglia">
    <div class="rqs-intro">
      <h2 id="richiesta-titolo">{titolo}</h2>
      <p>Prepariamo il messaggio in tre passaggi. Lo controlli e lo invii tu da WhatsApp.</p>
      <div class="rqs-telefono"><span>Preferisci parlarne a voce?</span>
        <a href="tel:+393426436085"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>Chiama 342 643 6085</a>
      </div>
    </div>
    <form class="rqs-form" data-richiesta-guidata data-telefono-wa="393426436085" novalidate aria-label="Prepara un messaggio per Luca">
      <p class="rqs-posizione" data-rqs-posizione aria-live="polite">1 di 3 · Auto e servizio</p>
      <div class="rqs-passo" data-rqs-passo="0">
      <div class="rqs-campo">
        <label for="rqs-problema">Di cosa hai bisogno?</label>
        <select id="rqs-problema" name="problema" required aria-describedby="rqs-errore">{opzioni_problema(sede_fissa)}</select>
        <p class="rqs-errore" id="rqs-errore" role="status" hidden></p>
      </div>
      <div class="rqs-campo"><label for="rqs-auto">La tua auto <span>(facoltativo)</span></label><input id="rqs-auto" name="auto" maxlength="100" placeholder="Es. Fiat Panda 2015"></div>
      </div>
      <div class="rqs-passo" data-rqs-passo="1" hidden>
      <fieldset class="rqs-modalita"><legend>Come preferisci organizzarti?</legend><div>{scelte}</div></fieldset>
      <div class="rqs-campo"><label for="rqs-comune">Comune <span>(facoltativo)</span></label><input id="rqs-comune" name="comune" maxlength="100" autocomplete="address-level2" placeholder="Es. Casale Monferrato"></div>
      </div>
      <div class="rqs-passo" data-rqs-passo="2" hidden>
      <div class="rqs-campo"><label for="rqs-dettagli">Qualche dettaglio in più <span>(facoltativo)</span></label><textarea id="rqs-dettagli" name="dettagli" rows="3" maxlength="1500" placeholder="Descrivi cosa cerchi o cosa succede alla tua auto."></textarea></div>
      <details class="rqs-anteprima"><summary>Controlla il messaggio per Luca<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><pre data-rqs-anteprima aria-live="off">Scegli il servizio o il problema: il messaggio comparirà qui.</pre></details>
      <button class="btn btn--arancio rqs-invia" type="submit"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5z"/></svg>Apri WhatsApp con il messaggio</button>
      <p class="rqs-nota">Puoi modificarlo in WhatsApp. L'invio lo confermi tu. <a href="privacy.html">Informativa privacy</a></p>
      <p class="rqs-esito" data-rqs-esito role="status" hidden></p>
      </div>
      <div class="rqs-navigazione"><button type="button" class="link-btn" data-rqs-indietro hidden>Indietro</button><button type="button" class="btn btn--arancio" data-rqs-avanti>Continua</button></div>
    </form>
    <noscript><style>.rqs-form{{display:none}}</style><p>Per preparare il messaggio guidato, attiva JavaScript. Puoi comunque chiamare Luca al <a href="tel:+393426436085">342 643 6085</a>.</p></noscript>
  </div>
</section>
'''
