"""Sito dell'officina già operativa. Generazione: python sorgente/genera_nuovo.py.
Scrive alla radice e mantiene i vecchi URL con pagine di reindirizzamento.
LM_PRODUZIONE=1 abilita l'indicizzazione sul dominio definitivo.
Stili e script: sorgente/nuovo.css e sorgente/nuovo.js."""
import hashlib, json, math, os, sys
from html import escape
from richiesta import sezione_richiesta, risorse_richiesta, opzioni_problema
from contenuti import DOMINIO, TEL, TEL_TXT, WA, EMAIL, PEC, MAPS, SEDE_LEGALE, GEAR, GEAR_PIENO, RECENSIONI, DETT, FAQ_R, ATT

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RADICE, "docs")
A = ""
DEMO = os.environ.get("LM_PRODUZIONE") != "1"
ASSET_V = hashlib.sha256(b"".join(open(os.path.join(QUI, f), "rb").read() for f in ("nuovo.css", "nuovo.js"))).hexdigest()[:10]

NAV = [("officina.html", "Officina"), ("ritiro-consegna.html", "Ritiro e consegna"), ("gomme-ricambi.html", "Gomme e ricambi"),
       ("officina-mobile.html", "Officina mobile"), ("chi-sono.html", "Chi sono"), ("contatti.html", "Contatti")]


def ico(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

I = {
    "tel": ico('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "chat": ico('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5z"/>'),
    "mail": ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "pin": ico('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    "check": ico('<path d="m5 12 5 5 9-10"/>'),
    "freccia": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
}

# fascia blu della targa europea
_stelle = "".join(f'<circle cx="{22 + 11 * math.cos(math.radians(a * 30)):.1f}" cy="{19 + 11 * math.sin(math.radians(a * 30)):.1f}" r="1.35" fill="#f2c230"/>' for a in range(12))
TARGA_UE = f'<span class="targa-ue" aria-hidden="true"><svg viewBox="0 0 44 64" width="44" height="64">{_stelle}<text x="22" y="53" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-weight="700" font-size="17" fill="#fff">I</text></svg></span>'

# ---------------------------------------------------------------- l'auto sul ponte (linee arancioni)
# punti caldi: (id, x, y) in unità del disegno 900 x 480
PUNTI = [("meccanica", 718, 322), ("elettrauto", 632, 292), ("diagnosi", 546, 238), ("clima", 452, 300),
         ("gomme", 250, 368), ("carrozzeria", 150, 318), ("revisione", 430, 392)]


def ruota(cx, nome):
    razze = "".join(f'<path d="M0 -27V-9" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return (f'<g transform="translate({cx} 368)"><g class="ruota {nome}"><circle r="46" class="t-gomma" data-draw/><circle r="29" class="t-cerchio"/>'
            f'<g class="t-razze">{razze}</g><circle r="19" class="t-disco"/><circle r="6.5" class="t-mozzo"/></g></g>')


def auto_svg(chi, descrizione="Auto sul ponte sollevatore, disegnata a linee"):
    return f'''<svg class="auto" id="auto-{chi}" viewBox="0 0 900 480" role="img" aria-label="{descrizione}">
  <ellipse class="ombra" cx="450" cy="430" rx="370" ry="13"/>
  <g class="colonne">
    <rect x="46" y="130" width="46" height="300" rx="5"/><rect x="808" y="130" width="46" height="300" rx="5"/>
    <path d="M46 150h46M46 170h46M808 150h46M808 170h46" class="strisce"/>
  </g>
  <g class="auto-gruppo">
    <g class="braccia"><path d="M92 386H236M808 386H694"/><rect x="60" y="362" width="32" height="44" rx="4"/><rect x="808" y="362" width="32" height="44" rx="4"/></g>
    <g class="sotto">
      <path d="M170 394H330q12 0 12-9H548q12 0 12 9H700" data-draw/><path d="M300 380H610" class="tratto"/>
      <path d="M222 376l-24 16M278 376l24 16M600 376l-24 16M680 376l24 16" data-draw/>
    </g>
    <g class="xr xr-motore"><path d="M672 298h56v30h-56zM684 298v-11M700 298v-11M716 298v-11"/></g>
    <g class="xr xr-elettrauto"><path d="M614 290h36v20h-36zM622 290v-6h7v6M635 290v-6h7v6M626 300h10M631 295v10"/></g>
    <g class="xr xr-diagnosi"><circle cx="544" cy="240" r="11"/><circle cx="518" cy="242" r="8"/><path d="M500 256h62"/></g>
    <g class="xr xr-clima"><path d="M432 296h40M432 305h40M432 314h40"/></g>
    <g class="xr xr-gomme"><circle cx="250" cy="368" r="58"/></g>
    <g class="xr xr-carrozzeria"><path d="M128 372L124 330C124 310 134 298 152 294L178 288L192 340V372"/></g>
    <g class="xr xr-revisione"><path d="M168 380H706V404H168Z"/></g>
    <path class="t-corpo" data-draw d="M128 372L124 330C124 310 134 298 152 294L178 288C196 262 226 220 262 198C272 192 284 188 300 188L478 188C500 188 516 196 530 210L592 268C598 276 610 280 624 283L742 302C766 306 778 322 778 340L778 372L702 372A62 62 0 0 0 578 372L314 372A62 62 0 0 0 188 372Z"/>
    <path class="t-vetri" data-draw d="M290 200L478 200C492 200 500 204 508 213L556 262L240 262C252 240 266 216 290 200ZM388 200L388 262"/>
    <path class="t-linee" data-draw d="M392 266L396 350M258 266L254 350M548 266L554 350M320 350L572 350M336 286h26M470 286h26"/>
    <path class="t-fanale" d="M746 306L772 312C776 316 776 326 774 330L748 322Z"/><path class="t-posteriore" d="M126 312L134 308L134 330L126 330Z"/>
    <path class="t-linee" d="M520 244l22 4-4 12-18-2z"/>
    {ruota(250, "ruota-p")}{ruota(640, "ruota-a")}
  </g>
</svg>'''


def hotspot_html():
    nomi = {"meccanica": "Tagliando e manutenzione", "elettrauto": "Elettrauto", "diagnosi": "Diagnosi centraline", "clima": "Climatizzatore",
            "gomme": "Gomme", "carrozzeria": "Carrozzeria", "revisione": "Pre-revisione"}
    return "".join(f'<button class="punto" type="button" data-punto="{i}" style="--x:{x / 9:.2f};--y:{y / 4.8:.2f}" aria-label="{nomi[i]}"><span class="punto-nome">{nomi[i]}</span></button>' for i, x, y in PUNTI)


# ---------------------------------------------------------------- pezzi comuni
def head(pagina, titolo, descrizione, schema=None, noindex=False):
    url = DOMINIO + "/" + ("" if pagina == "index.html" else pagina)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in (schema or []))
    robots = '<meta name="robots" content="noindex, nofollow">' if (DEMO or noindex) else f'<link rel="canonical" href="{url}">'
    return f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
{robots}
<meta name="theme-color" content="#0b0d10">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="L.M. Autoservizi">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/assets/img/campione/officina.webp">
<meta property="og:image:alt" content="Fotografia stock di esempio per la demo di L.M. Autoservizi">
<link rel="icon" type="image/png" sizes="32x32" href="{A}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{A}assets/img/favicon-180.png">
<script>(function(d){{d.classList.add("js");try{{if(/salta=1/.test(location.search))d.classList.add("salta");if(matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("fermo")}}catch(e){{}}setTimeout(function(){{if(!window.__nuovoPronto)d.classList.add("salta")}},6000)}})(document.documentElement);</script>
<link rel="preload" href="{A}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="nuovo.css?v={ASSET_V}">
{risorse_richiesta(A) + chr(10) if pagina == "index.html" else ""}{ld}</head>
<body{" class=\"home\"" if pagina == "index.html" else ""}>
<a class="salta-link" href="#contenuto">Vai al contenuto</a>
'''


def header(pagina):
    voci = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == pagina else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="testata">
  <div class="wrap testata-riga">
    <a class="marchio" href="index.html"><img src="{A}assets/img/logo-arancio-84.png" width="40" height="40" alt=""><span>L.M. Autoservizi<small>Officina a Frassineto Po</small></span></a>
    <nav class="menu" id="menu" aria-label="Principale" data-lenis-prevent><ul>{voci}</ul><p class="stato" data-stato></p></nav>
    <a class="btn btn--arancio btn--piccolo testata-chiama" href="tel:{TEL}">{I["tel"]}Chiama</a>
    <button class="menu-bottone" type="button" aria-expanded="false" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </div>
</header>
<main id="contenuto">
'''


def dialog_ritiro():
    return f'''<dialog class="foglio" id="foglio-ritiro" aria-labelledby="foglio-t" data-lenis-prevent>
  <form data-modulo data-intro="Ciao Luca, vorrei far ritirare l'auto." novalidate>
    <button class="foglio-chiudi" type="button" aria-label="Chiudi" data-chiudi>×</button>
    <h2 id="foglio-t">Chiedi il ritiro dell'auto</h2>
    <p class="piccolo">Scegli il problema e indica dove si trova l'auto: la richiesta si prepara su WhatsApp.</p>
    {targa_campo("f-targa")}
    <div class="campo"><label for="f-categoria">Tipo di problema</label><select id="f-categoria" name="categoria" data-etichetta="Tipo di problema" required>{opzioni_problema(True)}</select><p class="errore" aria-live="polite"></p></div>
    <div class="campo"><label for="f-comune">Dove si trova l'auto</label><input id="f-comune" name="comune" data-etichetta="Comune" required autocomplete="address-level2" placeholder="Es. Casale Monferrato"><p class="errore" aria-live="polite"></p></div>
    <div class="campo"><label for="f-problema">Cosa non va</label><textarea id="f-problema" name="problema" data-etichetta="Problema" rows="3" required placeholder="Es. si accende la spia del motore"></textarea><p class="errore" aria-live="polite"></p></div>
    <button class="btn btn--wa btn--pieno" type="submit">{I["chat"]}Invia su WhatsApp</button>
    <p class="nota">Lo invii tu: non parte niente da solo. Preferisci parlarmi? <a href="tel:{TEL}">{TEL_TXT}</a></p>
    <p class="esito" role="status" hidden></p>
  </form>
</dialog>
'''


def footer(dialog=True):
    voci = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    ritiro_barra = f'<button type="button" data-apri="ritiro">{I["pin"]}Ritiro</button>' if dialog else f'<a href="ritiro-consegna.html">{I["pin"]}Ritiro</a>'
    return f'''</main>
<footer class="piede">
  <div class="wrap piede-griglia">
    <div class="piede-marchio">
      <img src="{A}assets/img/logo-bianco-104.png" width="52" height="52" alt="" loading="lazy">
      <p><strong>L.M. Autoservizi di Miglietta Luca</strong><br>Officina a Frassineto Po. Meccanica, elettronica, gomme e carrozzeria, con ritiro e consegna dell'auto.</p>
    </div>
    <div><h2>Pagine</h2><ul>{voci}</ul></div>
    <div><h2>Contatti</h2><ul>
      <li><a href="tel:{TEL}">{TEL_TXT}</a></li>
      <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    <div><h2>Sede legale</h2><ul>
      <li>{SEDE_LEGALE}</li>
      <li>Lunedì–venerdì<br>7:30–19:30 continuato</li>
      <li><span class="stato" data-stato></span></li></ul></div>
  </div>
  <div class="wrap piede-foto-nota">Le fotografie della demo sono immagini stock di esempio.</div>
  <div class="wrap piede-basso"><span>© <span data-anno>2026</span> L.M. Autoservizi di Miglietta Luca · P.IVA 02625920067</span><a href="privacy.html">Privacy e cookie</a></div>
</footer>
<nav class="barra" aria-label="Azioni rapide">
  <a href="tel:{TEL}">{I["tel"]}Chiama</a>
  <a href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a>
  {ritiro_barra}
</nav>
{dialog_ritiro() if dialog else ""}<script src="{A}assets/js/vendor/gsap.min.js" defer></script>
<script src="{A}assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{A}assets/js/vendor/lenis.min.js" defer></script>
<script src="nuovo.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def scrivi(nome, contenuto):
    os.makedirs(os.path.dirname(os.path.join(OUT, nome)), exist_ok=True)
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", nome, len(contenuto))


def intro_pagina(titolo, testo):
    return f'''
<section class="intro-pagina">
  <div class="intro-ingranaggio" aria-hidden="true"><svg viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg></div>
  <div class="wrap"><h1><span class="riga"><span>{titolo}</span></span></h1><p class="lead">{testo}</p></div>
</section>
'''


def tag(testo, forte=False):
    return f'<span class="tag{" tag--forte" if forte else ""}">{testo}</span>'


def targa_campo(id_):
    return f'''<div class="campo"><label for="{id_}">Targa dell'auto</label>
      <div class="targa">{TARGA_UE}<input id="{id_}" name="targa" class="targa-campo" data-etichetta="Targa" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="8" placeholder="AB123CD"></div>
      <p class="aiuto">Serve solo a riconoscere il modello. Non è obbligatoria.</p></div>'''


ORARI = '''<table class="orari"><caption class="sr">Orari di apertura</caption>
  <tr data-giorni="1,2,3,4,5"><th scope="row">Lunedì–venerdì</th><td>7:30–19:30, continuato</td></tr>
  <tr data-giorni="6,0"><th scope="row">Sabato e domenica</th><td>Chiuso</td></tr></table>'''

FOTO_CAMPIONE = {
    "luca": ("mani", 1600, 2400, "Foto stock di esempio: mani di un meccanico al lavoro sul motore"),
    "ritiro": ("ritiro", 1600, 1067, "Foto stock di esempio: la consegna delle chiavi di un'auto"),
    "riconsegna": ("riconsegna", 1600, 2001, "Foto stock di esempio: dettaglio di un'auto pulita, pronta a ripartire"),
    "mobile": ("mobile", 1600, 1067, "Foto stock di esempio: un intervento sul motore all'aperto"),
    "ingresso": ("officina", 1600, 1067, "Foto stock di esempio: ambiente di un'officina con auto e ponte sollevatore"),
    "officina": ("officina", 1600, 1067, "Foto stock di esempio: auto e attrezzature in un'officina"),
    "meccanica": ("meccanica", 1600, 1067, "Foto stock di esempio: un intervento di manutenzione sul motore"),
    "diagnosi": ("diagnosi", 1600, 1067, "Foto stock di esempio: un controllo nel vano motore"),
    "gomme": ("gomme", 1600, 1067, "Foto stock di esempio: un meccanico controlla un pneumatico"),
}


def foto_campione(chi, formato="ritratto", sizes="(max-width: 699px) 100vw, 60vw"):
    nome, larghezza, altezza, alt = FOTO_CAMPIONE[chi]
    percorso = A + "assets/img/campione/" + nome
    return (f'<div class="foto-editoriale foto-editoriale--{formato} foto-campione" data-foto-campione="{chi}">'
            f'<img src="{percorso}.webp" srcset="{percorso}-800.webp 800w, {percorso}.webp {larghezza}w" sizes="{sizes}" width="{larghezza}" height="{altezza}" alt="{escape(alt, quote=True)}" loading="lazy" decoding="async">'
            '<span class="foto-campione-nota">Foto stock di esempio</span></div>')


ARRIVO = f'''<div class="arrivo">
  {foto_campione("ingresso", "orizzontale")}
  <div class="arrivo-testo"><h3>Passa in officina</h3><p>L'officina è già operativa a Frassineto Po. Chiamami prima di passare: concordiamo l'intervento e ti do tutte le indicazioni per raggiungermi.</p>
  <a class="btn btn--arancio" href="tel:{TEL}">{I["tel"]}Chiama {TEL_TXT}</a>
  <p class="piccolo">Non riesci a portare l'auto? Possiamo organizzare il ritiro a casa o al lavoro.</p></div></div>'''


def finale(titolo="Hai un'auto da sistemare?", testo="Chiama o scrivi: ti dico quando posso ritirarla o quando puoi portarmela."):
    return f'''
<section class="finale"><div class="wrap finale-riga">
  <div><h2>{titolo}</h2><p>{testo}</p></div>
  <div class="finale-azioni"><a class="numerone" href="tel:{TEL}">{TEL_TXT}</a>
    <div class="azioni"><button class="btn btn--chiaro" type="button" data-apri="ritiro">{I["pin"]}Chiedi il ritiro</button><a class="btn btn--scuro" href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a></div></div>
</div></section>
'''


def passi_rotta():
    voci = [("Mi chiami o mi scrivi", "Mi dici dov'è l'auto e cosa non va. Nessun giro di telefonate."),
            ("Passo a ritirarla", "Vengo a casa o al lavoro e ti lascio una vettura di cortesia gratuita."),
            ("Diagnosi e preventivo", "Controllo l'auto in officina e ti dico cosa serve e quanto costa, prima di iniziare."),
            ("La riparo", "Nella mia officina a Frassineto Po, con il ponte e le attrezzature giuste."),
            ("Te la riporto", "Riparata, pulita e igienizzata, dove vuoi. Paghi alla consegna.")]
    return "".join(f'<li class="passo"><span class="n">{i + 1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(voci))


def gomma_render():
    return f'''<figure class="gomma-prodotto">
  <div class="gomma-foto"><img class="gomma-render" src="{A}assets/img/3d/pneumatico-realista-v1.webp" width="1254" height="1254" alt="Render illustrativo di un pneumatico stradale con cerchio in lega, visto di tre quarti" loading="lazy" decoding="async"></div>
  <figcaption class="gomma-dati"><div><span data-misura-label>Esempio di misura</span><strong id="testo-misura">205/55 R16</strong></div><p>Immagine illustrativa</p></figcaption>
</figure>'''


SCHEMA = {"@context": "https://schema.org", "@type": "AutoRepair", "@id": DOMINIO + "/#azienda",
          "name": "L.M. Autoservizi di Miglietta Luca",
          "description": "Officina a Frassineto Po: meccanica, elettronica, gomme e carrozzeria, con ritiro e consegna dell'auto, vettura di cortesia gratuita e officina mobile.",
          "url": DOMINIO + "/", "telephone": TEL, "email": EMAIL, "vatID": "IT02625920067",
          "founder": {"@type": "Person", "name": "Luca Miglietta"},
          "address": {"@type": "PostalAddress", "addressLocality": "Frassineto Po", "addressRegion": "AL", "addressCountry": "IT"},
          "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "19:30"}],
          "paymentAccepted": "Contanti, Carta di credito, Bancomat",
          "areaServed": [{"@type": "City", "name": "Frassineto Po"}, {"@type": "City", "name": "Casale Monferrato"}]}

# ================================================================== HOME
SERVIZI = [
    ("meccanica", "Tagliando e manutenzione", "Manutenzione ordinaria e straordinaria su auto di tutte le marche. Prima la diagnosi, poi ti dico cosa serve e quanto costa.", [("In officina", 1)]),
    ("elettrauto", "Elettrauto", "Avviamento, ricarica, luci, accessori e cablaggi: trovo il difetto elettrico e lo sistemo.", [("In officina", 1), ("Anche da te", 0)]),
    ("diagnosi", "Diagnosi centraline", "Una spia accesa si legge subito. Lettura degli errori e programmazione, con software aggiornato ogni giorno.", [("In officina", 1), ("Anche da te", 0)]),
    ("clima", "Climatizzatore", "Controllo e ricarica dell'impianto. Ho la formazione per il recupero dei gas fluorurati.", [("In officina", 1)]),
    ("gomme", "Gomme", "Cambio pneumatici, equilibratura, convergenza e campanatura. Le forature le riparo anche da te.", [("In officina", 1), ("Forature da te", 0)]),
    ("carrozzeria", "Carrozzeria", "Carrozzeria, verniciatura e saldatura, con preventivo gratuito da confrontare.", [("In officina", 1)]),
    ("revisione", "Pre-revisione", "Ti controllo l'auto gratis prima della revisione e ti prenoto la revisione. Sono abilitato come responsabile tecnico.", [("Controllo gratuito", 1)]),
]
servizi_li = "".join(f'''<li class="servizio" id="srv-{i}" data-servizio="{i}"><h3>{t}</h3><p>{d}</p><p class="tags">{"".join(tag(x, f) for x, f in tg)}</p>
  <button class="link-btn" type="button" data-apri="ritiro">Chiedi un preventivo</button></li>''' for i, t, d, tg in SERVIZI)
indice_li = "".join(f'<li><button type="button" data-vai="{i}" aria-label="{t}"></button></li>' for i, t, _, _ in SERVIZI)

rec ="".join(f'<figure class="voce"><span class="virgolette" aria-hidden="true">“</span><blockquote><p>{t}</p></blockquote><figcaption>{n}</figcaption></figure>' for t, n in RECENSIONI)

SERVIZI_HOME = [
    ("meccanica", "Meccanica", "Tagliandi, freni e manutenzione multimarca. Concordiamo il preventivo prima di iniziare.", "officina.html#manutenzione", "Tagliando e manutenzione"),
    ("diagnosi", "Diagnosi", "Spie e difetti elettrici: individuo il problema e ti spiego come intervenire.", "officina.html#diagnosi", "Spie accese e diagnosi"),
    ("gomme", "Gomme e ricambi", "Verifichiamo disponibilità e prezzo. Al montaggio penso io, in officina.", "gomme-ricambi.html", "Acquisto gomme"),
]


def servizi_home():
    voci = []
    for chi, titolo, testo, href, problema in SERVIZI_HOME:
        voci.append(f'''<article class="servizio-editoriale servizio-editoriale--{chi}">
      <a class="servizio-editoriale-foto" href="{href}" aria-label="Scopri: {titolo}">{foto_campione(chi, "orizzontale", "(max-width: 699px) 100vw, 33vw")}<span class="servizio-editoriale-freccia" aria-hidden="true">{I["freccia"]}</span></a>
      <div class="servizio-editoriale-testo"><h3><a href="{href}">{titolo}</a></h3><p>{testo}</p><a class="link" data-richiesta-servizio="{escape(problema, quote=True)}" href="#richiesta" aria-label="Chiedi a Luca: {titolo}">Chiedi a Luca {I["freccia"]}</a></div>
    </article>''')
    return f'''
<section class="sezione servizi-editoriali" id="servizi" aria-labelledby="servizi-t">
  <div class="wrap">
    <div class="servizi-editoriali-testa"><h2 id="servizi-t">La cura giusta,<br>per la tua auto.</h2><p class="lead">Dal tagliando alla spia che si accende.<br>Partiamo da quello che ti serve.</p></div>
    <div class="servizi-editoriali-griglia" id="servizi-fotografici" tabindex="0" aria-label="Servizi, scorri lateralmente per esplorarli" data-lenis-prevent>{"".join(voci)}</div>
    <div class="servizi-comandi"><button type="button" data-servizio-direzione="-1" aria-controls="servizi-fotografici" aria-label="Servizio precedente">{I["freccia"]}</button><span data-servizio-posizione aria-live="polite">1 / 3</span><button type="button" data-servizio-direzione="1" aria-controls="servizi-fotografici" aria-label="Servizio successivo">{I["freccia"]}</button></div>
    <p class="servizi-editoriali-altri">Anche elettrauto, carrozzeria, climatizzatore e pre-revisione. <a class="link" href="officina.html">Tutti i servizi {I["freccia"]}</a></p>
  </div>
</section>'''


home = head("index.html", "Officina a Frassineto Po con ritiro e consegna | L.M. Autoservizi",
            "Officina di Luca Miglietta a Frassineto Po: meccanica, elettronica, gomme e carrozzeria su auto di tutte le marche. Ritiro e consegna con vettura di cortesia gratuita.", [SCHEMA]) + header("index.html") + f'''
<section class="eroe eroe--reportage" aria-labelledby="eroe-t">
  <div class="eroe-luce" aria-hidden="true"></div>
  <div class="eroe-fascio" aria-hidden="true"></div>
  <div class="wrap eroe-meta"><span>Frassineto Po</span><div class="eroe-meta-azioni"><span>Officina già operativa</span><button class="motion-ripeti" type="button" data-ripeti-apertura hidden><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 5 11 7-11 7z"/></svg><span>Rivedi l'apertura</span></button></div></div>
  <div class="eroe-scena" aria-hidden="true">
    <div class="eroe-ingranaggio">
      <svg class="eroe-aloni" viewBox="-400 -400 800 800"><circle r="340"/><circle r="390"/></svg>
      <div class="eroe-finestra"><img src="{A}assets/img/campione/eroe.webp" srcset="{A}assets/img/campione/eroe-800.webp 800w, {A}assets/img/campione/eroe.webp 1600w" sizes="(max-width:699px) 85vw, 50vw" width="1600" height="2400" alt="" fetchpriority="high"></div>
      <svg class="eroe-anello" viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg>
    </div>
  </div>
  <div class="eroe-righe">
    <h1 id="eroe-t"><span class="riga eroe-riga-a"><span>Stessa cura.</span></span><span class="riga eroe-riga-b"><span><span class="contorno">Nuova</span> sede.</span></span></h1>
  </div>
  <div class="eroe-basso">
    <div class="eroe-testo" data-entra>
      <p><strong>La tua officina a Frassineto Po.</strong> Meccanica, diagnosi, gomme e ricambi. Porti l'auto, oppure la ritiro io.</p>
      <div class="azioni"><a class="btn btn--arancio" href="#richiesta">Descrivi il problema</a><a class="btn btn--vuoto" href="ritiro-consegna.html">{I["pin"]}Ritiro e consegna</a></div>
    </div>
    <div class="eroe-esplora"><a class="eroe-scorri" href="#la-nuova-officina">Scopri la nuova officina <span aria-hidden="true">↓</span></a><p class="eroe-foto-nota">Fotografia stock di esempio</p></div>
  </div>
</section>

<section class="reportage-officina" aria-labelledby="reportage-t">
  <div class="wrap">
    <figure class="reportage-foto">
      <div class="reportage-finestra">{foto_campione("officina", "orizzontale", "100vw")}</div>
      <figcaption><h2 id="reportage-t">Il lavoro si vede.</h2><p>Uno spazio dedicato alla tua auto.<br>Fotografia di riferimento per la demo.</p></figcaption>
    </figure>
  </div>
</section>

<div class="livrea" aria-hidden="true"><div>Meccanica <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Gomme e ricambi <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Ritiro e consegna <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Officina mobile <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Meccanica <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Gomme e ricambi</div></div>

<section class="sezione nuova-intro" id="la-nuova-officina" aria-labelledby="nuova-intro-t">
  <div class="wrap">
    <div class="persona-griglia">
      {foto_campione("luca")}
      <div class="persona-testo"><h2 id="nuova-intro-t" class="promessa">Un'officina nuova.<br>La stessa persona.</h2>
        <div class="intro-dettagli"><p>Sono Luca. Valutiamo l'intervento e concordiamo il preventivo prima di iniziare. In officina o con ritiro e riconsegna, parli sempre con me.</p></div>
        <a class="link" href="chi-sono.html">Conosci Luca {I["freccia"]}</a>
      </div>
    </div>
  </div>
</section>

{servizi_home()}

<section class="appuntamento-home" id="organizzati" aria-labelledby="appuntamento-t">
  <div class="wrap appuntamento-griglia">
    <div class="appuntamento-foto">{foto_campione("ritiro", "orizzontale")}</div>
    <div class="appuntamento-testo"><h2 id="appuntamento-t">Tu hai i tuoi impegni.<br>Io penso all'auto.</h2><p>Porti l'auto, oppure passo io a casa o al lavoro. La vettura di cortesia è gratuita durante la riparazione.</p><div class="azioni"><a class="btn btn--arancio" data-preferisci-ritiro href="#richiesta">Organizza il ritiro {I["freccia"]}</a><a class="link" data-preferisci-officina href="#richiesta">Vengo in officina {I["freccia"]}</a></div></div>
  </div>
</section>

<section class="orizzonte-home" id="ritiro" aria-labelledby="orizzonte-t">
  <div class="wrap orizzonte-testa"><h2 id="orizzonte-t">La tua giornata continua.</h2></div>
  <div class="orizzonte-palco">
    <nav class="orizzonte-nav" aria-label="Le tappe del ritiro"><a href="#tappa-ritiro" data-orizzonte-vai="0" aria-current="step"><span>1</span> Ritiro</a><a href="#tappa-officina" data-orizzonte-vai="1"><span>2</span> Officina</a><a href="#tappa-riconsegna" data-orizzonte-vai="2"><span>3</span> Riconsegna</a><div class="orizzonte-progresso" aria-hidden="true"><span></span></div></nav>
    <div class="orizzonte-traccia" tabindex="0" aria-label="Le tappe del ritiro, scorri lateralmente" data-lenis-prevent>
      <article class="orizzonte-pannello" id="tappa-ritiro">
        <div class="orizzonte-testo"><h3 tabindex="-1">Non cambi<br>i tuoi piani.</h3><p>Ritiro a casa o al lavoro. Concordiamo orario e luogo; ti lascio una vettura di cortesia gratuita.</p><a class="link" href="ritiro-consegna.html">Come funziona {I["freccia"]}</a></div>
        <figure>{foto_campione("ritiro")}</figure>
      </article>
      <article class="orizzonte-pannello" id="tappa-officina">
        <div class="orizzonte-testo"><h3 tabindex="-1">La tua auto,<br>nelle mie mani.</h3><p>Controllo l'auto e concordiamo il preventivo prima di iniziare. Poi eseguo il lavoro in officina.</p><a class="link" href="officina.html">Dentro l'officina {I["freccia"]}</a></div>
        <figure>{foto_campione("meccanica")}</figure>
      </article>
      <article class="orizzonte-pannello" id="tappa-riconsegna">
        <div class="orizzonte-testo"><h3 tabindex="-1">Di nuovo<br>in strada.</h3><p>Ti riporto l'auto riparata, pulita e igienizzata. Paghi alla consegna.</p><a class="btn btn--arancio" data-preferisci-ritiro href="#richiesta">Organizza il ritiro {I["freccia"]}</a></div>
        <figure>{foto_campione("riconsegna")}</figure>
      </article>
    </div>
  </div>
</section>

{sezione_richiesta(sede_fissa=True)}

<section class="gomme-sez" id="gomme" aria-labelledby="gomme-t">
  <div class="wrap gomme-griglia">
    <div class="gomme-testo">
      <h2 id="gomme-t">Vendita gomme<br>e ricambi</h2>
      <p class="lead">Pneumatici e ricambi per la tua auto. Ti rispondo con disponibilità e prezzo; al montaggio penso io.</p>
      <a class="btn btn--arancio" href="gomme-ricambi.html">Cerca le gomme per misura {I["freccia"]}</a>
    </div>
    <div class="gomme-disegno">{gomma_render()}</div>
  </div>
</section>

<section class="mobile-sez" aria-labelledby="mobile-t">
  <div class="wrap mobile-home-griglia">
    {foto_campione("mobile", "orizzontale")}
    <div><h2 id="mobile-t">C'è anche<br>l'officina mobile</h2>
      <p class="lead">Per forature, cambio delle ruote montate, diagnosi e piccoli interventi, arrivo io dove sei rimasto fermo. Se il lavoro richiede il ponte, ritiro l'auto.</p>
      <p><a class="link" href="officina-mobile.html">Cosa faccio sul posto {I["freccia"]}</a></p>
    </div>
  </div>
</section>

<section class="recensioni" aria-labelledby="rec-t">
  <div class="wrap">
    <div class="rec-testa"><h2 id="rec-t">Cosa dicono i clienti</h2>
      <div class="rec-frecce"><button type="button" data-rec="-1" aria-label="Precedente">{I["freccia"]}</button><button type="button" data-rec="1" aria-label="Successiva">{I["freccia"]}</button></div></div>
    <div class="voci" tabindex="0" aria-label="Recensioni dei clienti">{rec}</div>
    <p><a class="link" href="{MAPS}" target="_blank" rel="noopener">Leggi le recensioni su Google {I["freccia"]}</a></p>
  </div>
</section>

<section class="dove-sez" aria-labelledby="dove-t">
  <div class="wrap dove">
    <div>
      <h2 id="dove-t">Dove e quando</h2>
      <p class="indirizzo">Officina a Frassineto Po (AL)</p>
      {ORARI}
      <p><span class="stato" data-stato></span></p>
      <p class="piccolo">Ritiro e riconsegna a Casale Monferrato e nei paesi vicini.</p>
    </div>
    <div class="arrivo arrivo--home">{foto_campione("ingresso", "orizzontale")}<div class="arrivo-testo"><p>Prima di passare, chiamami per concordare l'intervento.</p><a class="btn btn--arancio" href="tel:{TEL}">{I["tel"]}Chiama {TEL_TXT}</a></div></div>
  </div>
</section>
''' + finale() + footer()


def misura_modulo(id_):
    return f'''<form class="scheda" data-modulo data-misura data-intro="Ciao Luca, vorrei un preventivo per le gomme." novalidate aria-label="Cerca le gomme per misura">
  <div class="misura" role="group" aria-label="Misura del pneumatico">
    <label><span class="sr">Larghezza</span><input name="larghezza" data-etichetta="Larghezza" inputmode="numeric" maxlength="3" placeholder="205" required></label><i>/</i>
    <label><span class="sr">Spalla</span><input name="spalla" data-etichetta="Spalla" inputmode="numeric" maxlength="2" placeholder="55" required></label><i>R</i>
    <label><span class="sr">Cerchio in pollici</span><input name="cerchio" data-etichetta="Cerchio" inputmode="numeric" maxlength="2" placeholder="16" required></label>
  </div>
  <p class="errore" aria-live="polite"></p>
  <div class="campi-due">
    <div class="campo"><label for="{id_}-uso">Che gomme cerchi</label><select id="{id_}-uso" name="stagione" data-etichetta="Stagione"><option>Estive</option><option>Invernali</option><option>Quattro stagioni</option><option>Non lo so, consigliami tu</option></select></div>
    <div class="campo"><label for="{id_}-auto">Auto <span class="facoltativo">(facoltativo)</span></label><input id="{id_}-auto" name="auto" data-etichetta="Auto" placeholder="Es. Fiat Panda 2015"></div>
  </div>
  <button class="btn btn--arancio btn--pieno" type="submit">{I["chat"]}Chiedi disponibilità</button>
  <p class="nota">Ti rispondo con disponibilità e prezzo. Il montaggio si fa in officina.</p><p class="esito" role="status" hidden></p>
</form>'''


home = home.replace("{MISURA}", misura_modulo("hg"))
scrivi("index.html", home)

# ================================================================== OFFICINA
indice ="".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _, _ in DETT)
sezioni = "".join(f'''<article class="dettaglio" id="{a}" data-rivela><h2>{t}</h2><p>{d}</p><ul class="spunte">{"".join(f"<li>{I['check']}{p}</li>" for p in pt)}</ul>
  <p><a class="link" href="contatti.html#scrivimi">Chiedi un preventivo</a></p></article>''' for a, t, d, pt in DETT)
scrivi("officina.html", head("officina.html", "Cosa si fa in officina a Frassineto Po | L.M. Autoservizi",
      "Manutenzione multimarca, diagnosi centraline, elettrauto, gomme, carrozzeria, pre-revisione e consulenza alle imprese. Officina già operativa a Frassineto Po.", [SCHEMA]) + header("officina.html")
      + intro_pagina("In officina", "Tutto quello che serve alla tua auto, su auto di tutte le marche. Preventivo gratuito dopo la diagnosi.") + f'''
<section class="sezione"><div class="wrap documento">
  <nav class="indice" aria-label="In questa pagina"><p class="indice-t">In questa pagina</p><ul>{indice}</ul></nav>
  <div class="dettagli">{sezioni}</div>
</div></section>''' + finale() + footer())

# ================================================================== RITIRO E CONSEGNA
faq_html = "".join(f'<details><summary>{q}</summary><p>{r}</p></details>' for q, r in FAQ_R)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ_R]}
scrivi("ritiro-consegna.html", head("ritiro-consegna.html", "Ritiro e consegna dell'auto con vettura di cortesia | L.M. Autoservizi",
      "Ritiro l'auto a casa o al lavoro, la riparo nella mia officina a Frassineto Po e te la riporto. Vettura di cortesia gratuita.", [SCHEMA, faq_schema]) + header("ritiro-consegna.html")
      + intro_pagina("Ritiro e consegna", "Tu lavori, io mi occupo dell'auto: la ritiro, la riparo e te la riporto, con una vettura di cortesia gratuita nel frattempo.") + f'''
<section class="rotta rotta--pagina"><div class="wrap rotta-griglia">
  <div class="rotta-testo"><ol class="passi">{passi_rotta()}</ol></div>
</div></section>
<section class="sezione"><div class="wrap ritiro-dettagli">
  <div><h2>Domande frequenti</h2><div class="faq">{faq_html}</div></div>
  <div class="riquadro"><h2>Chiedi il ritiro</h2><p>Targa, dove si trova l'auto e cosa non va: il resto lo sistemiamo su WhatsApp.</p><button class="btn btn--arancio" type="button" data-apri="ritiro">{I["pin"]}Chiedi il ritiro</button></div>
</div></section>''' + footer())

# ================================================================== GOMME E RICAMBI
scrivi("gomme-ricambi.html", head("gomme-ricambi.html", "Gomme e ricambi a Frassineto Po | L.M. Autoservizi",
      "Vendita di gomme e ricambi per auto a Frassineto Po, con montaggio, equilibratura e convergenza in officina. Chiedi disponibilità e prezzo.", [SCHEMA]) + header("gomme-ricambi.html")
      + intro_pagina("Gomme e ricambi", "Vendita di pneumatici e ricambi per auto. Dimmi la misura o la targa: ti rispondo con disponibilità e prezzo. Se vuoi, mi occupo anche del montaggio.") + f'''
<section class="gomme-sez gomme-sez--pagina"><div class="wrap gomme-griglia">
  <div class="gomme-testo">
    <h2>Vendita pneumatici</h2>
    <p class="lead">Pneumatici estivi, invernali e quattro stagioni. La misura è scritta sul fianco, per esempio 205/55 R16: se non la sai dimmi la targa e la ricavo io.</p>
    {misura_modulo("gg")}
    <ul class="spunte"><li>{I["check"]}Montaggio e equilibratura in officina</li><li>{I["check"]}Convergenza e campanatura</li><li>{I["check"]}Riparazione delle forature</li></ul>
  </div>
  <div class="gomme-disegno">{gomma_render()}</div>
</div></section>
<section class="sezione sezione--chiara"><div class="wrap gomme-griglia">
  <div>
    <h2>Vendita ricambi</h2>
    <p class="lead">Vendita di ricambi per auto di tutte le marche. Dimmi targa e pezzo che ti serve: ti rispondo con disponibilità e preventivo, e se vuoi lo monto io.</p>
    <ul class="spunte"><li>{I["check"]}Ricambi per auto di tutte le marche</li><li>{I["check"]}Preventivo gratuito</li><li>{I["check"]}Montaggio in officina</li></ul>
  </div>
  <form class="scheda" data-modulo data-intro="Ciao Luca, vorrei un preventivo per un ricambio." novalidate aria-labelledby="rc-t">
    <h2 id="rc-t">Chiedi un ricambio</h2>
    {targa_campo("rc-targa")}
    <div class="campo"><label for="rc-pezzo">Che pezzo ti serve</label><input id="rc-pezzo" name="pezzo" data-etichetta="Pezzo" required placeholder="Es. pastiglie freni anteriori"><p class="errore" aria-live="polite"></p></div>
    <button class="btn btn--wa btn--pieno" type="submit">{I["chat"]}Chiedi su WhatsApp</button>
    <p class="nota">Si apre WhatsApp con il messaggio già scritto. Lo invii tu.</p><p class="esito" role="status" hidden></p>
  </form>
</div></section>''' + finale("Non sai cosa ti serve?", "Descrivimi il problema: ti dico io cosa serve.") + footer())

# ================================================================== OFFICINA MOBILE
scrivi("officina-mobile.html", head("officina-mobile.html", "Officina mobile a domicilio | L.M. Autoservizi",
      "Forature, cambio delle ruote montate, diagnosi e piccoli interventi direttamente dove si trova l'auto, a Casale Monferrato e dintorni.", [SCHEMA]) + header("officina-mobile.html")
      + intro_pagina("Officina mobile", "Per i lavori che si possono fare sul posto arrivo io, con il furgone attrezzato. Il resto lo facciamo in officina.") + f'''
<section class="sezione"><div class="wrap mobile-griglia">
  <div class="mobile-pagina-presentazione"><h2>L'officina<br>arriva da te.</h2><p class="lead">Un intervento sul posto, quando possibile. Il ritiro in sede, quando serve.</p>{foto_campione("mobile", "orizzontale")}</div>
  <div>
    <h2>Cosa faccio sul posto</h2>
    <ul class="spunte"><li>{I["check"]}Riparazione delle forature</li><li>{I["check"]}Cambio delle ruote già montate sui cerchi</li><li>{I["check"]}Diagnosi elettronica e lettura delle spie</li><li>{I["check"]}Problemi elettrici e di avviamento, nei casi semplici</li></ul>
    <h2 class="h2-sotto">E quando serve l'officina</h2>
    <p>Se il lavoro richiede il ponte o tempi lunghi, ritiro l'auto e ti lascio una vettura di cortesia gratuita. Il preventivo è sempre gratuito e arriva prima di iniziare.</p>
    <div class="azioni"><a class="btn btn--arancio" href="tel:{TEL}">{I["tel"]}Chiama {TEL_TXT}</a><a class="btn btn--vuoto" href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a></div>
    <p class="piccolo">Lavoro a Casale Monferrato e nei paesi vicini. Chiama per sapere se arrivo anche da te.</p>
  </div>
</div></section>''' + footer())

# ================================================================== CHI SONO
att_html = "".join(f'''<li><button type="button" data-lightbox="{A}assets/img/attestati/{f}.webp" data-titolo="{t}"><img src="{A}assets/img/attestati/{f}-thumb.webp" alt="" loading="lazy" width="340" height="480"><span>{t}<small>{s}</small></span></button></li>''' for f, t, s in ATT)
scrivi("chi-sono.html", head("chi-sono.html", "Chi sono: Luca Miglietta, meccanico a Frassineto Po | L.M. Autoservizi",
      "Luca Miglietta, titolare di L.M. Autoservizi: qualifica in riparazioni elettromeccaniche, abilitazione a responsabile tecnico delle revisioni ed esperienza decennale multimarca.", [SCHEMA]) + header("chi-sono.html")
      + intro_pagina("Chi sono", "Mi chiamo Luca Miglietta. Lavoro da solo, quindi l'auto che mi affidi la segue una persona sola, dall'inizio alla fine.") + f'''
<section class="sezione"><div class="wrap chi">
  {foto_campione("luca")}
  <div class="chi-biografia"><dl class="tessera">
    <div><dt>Titolare</dt><dd>Luca Miglietta</dd></div><div><dt>Officina</dt><dd>Frassineto Po, già operativa</dd></div>
    <div><dt>Esperienza</dt><dd>Più di dieci anni, multimarca</dd></div><div><dt>Abilitazione</dt><dd>Responsabile tecnico delle revisioni</dd></div>
  </dl>
  <ol class="cronologia">
    <li><b>2009</b><span>Diploma di liceo scientifico tecnologico a Casale Monferrato.</span></li>
    <li><b>2010</b><span>Qualifica di operatore di riparazioni elettromeccaniche per l'autoveicolo.</span></li>
    <li><b>2012</b><span>Formazione per il recupero dei gas fluorurati degli impianti di climatizzazione.</span></li>
    <li><b>Oggi</b><span>Titolare di L.M. Autoservizi, con officina a Frassineto Po, servizio di ritiro e consegna e officina mobile.</span></li>
  </ol></div>
</div></section>
<section class="sezione sezione--chiara"><div class="wrap">
  <h2>Attestati</h2><p class="piccolo">Tocca un attestato per vederlo a grandezza piena.</p>
  <ul class="attestati" data-rivela>{att_html}</ul>
</div></section>
<dialog class="lightbox" id="lightbox" aria-label="Attestato ingrandito" data-lenis-prevent><button class="lightbox-chiudi" type="button" aria-label="Chiudi">×</button><img alt=""><p></p></dialog>''' + finale() + footer())

# ================================================================== CONTATTI
scrivi("contatti.html", head("contatti.html", "Contatti e preventivo gratuito | L.M. Autoservizi",
      "Chiama il 342 643 6085, scrivi su WhatsApp o chiedi un preventivo personalizzato. Officina a Frassineto Po. Lunedì–venerdì 7:30–19:30.", [SCHEMA]) + header("contatti.html")
      + intro_pagina("Contatti", "Chiamami, scrivimi su WhatsApp o lascia qui la richiesta: ti rispondo io.") + f'''
<section class="sezione" id="scrivimi"><div class="wrap contatti">
  <form class="scheda" data-modulo data-intro="Ciao Luca, vorrei un preventivo." novalidate aria-labelledby="sc-t">
    <h2 id="sc-t">Chiedi un preventivo gratuito</h2>
    <fieldset class="campo"><legend>Di cosa hai bisogno</legend>
      <div class="scelte">
        <label><input type="radio" name="motivo" value="Ritiro e consegna" data-etichetta="Richiesta" checked><span>Ritiro e consegna</span></label>
        <label><input type="radio" name="motivo" value="La porto in officina" data-etichetta="Richiesta"><span>La porto io in officina</span></label>
        <label><input type="radio" name="motivo" value="Acquisto gomme" data-etichetta="Richiesta"><span>Acquisto gomme</span></label>
        <label><input type="radio" name="motivo" value="Acquisto ricambi" data-etichetta="Richiesta"><span>Acquisto ricambi</span></label>
        <label><input type="radio" name="motivo" value="Intervento sul posto (officina mobile)" data-etichetta="Richiesta"><span>Intervento sul posto</span></label>
        <label><input type="radio" name="motivo" value="Altro" data-etichetta="Richiesta"><span>Altro</span></label>
      </div></fieldset>
    <div class="campi-due">
      <div class="campo"><label for="c-nome">Nome</label><input id="c-nome" name="nome" data-etichetta="Nome" required autocomplete="name"><p class="errore" aria-live="polite"></p></div>
      <div class="campo"><label for="c-tel">Telefono</label><input id="c-tel" name="telefono" data-etichetta="Telefono" type="tel" inputmode="tel" required autocomplete="tel"><p class="errore" aria-live="polite"></p></div>
    </div>
    {targa_campo("c-targa")}
    <div class="campo"><label for="c-comune">Comune</label><input id="c-comune" name="comune" data-etichetta="Comune" autocomplete="address-level2" placeholder="Es. Casale Monferrato"></div>
    <div class="campo"><label for="c-categoria">Servizio o tipo di problema</label><select id="c-categoria" name="categoria" data-etichetta="Richiesta su" required>{opzioni_problema(True)}</select><p class="errore" aria-live="polite"></p></div>
    <div class="campo"><label for="c-msg">Descrivi la tua richiesta</label><textarea id="c-msg" name="messaggio" data-etichetta="Messaggio" rows="4" required placeholder="Es. cerco un ricambio, oppure l'auto non parte"></textarea><p class="errore" aria-live="polite"></p></div>
    <label class="consenso"><input type="checkbox" name="privacy" required><span>Acconsento al trattamento dei miei dati per ricevere il preventivo, come descritto nell'<a href="privacy.html">informativa privacy</a>.</span></label>
    <p class="errore" aria-live="polite"></p>
    <div class="azioni"><button class="btn btn--wa" type="submit" value="whatsapp">{I["chat"]}Invia su WhatsApp</button><button class="btn btn--vuoto" type="submit" value="email">{I["mail"]}Invia per email</button></div>
    <p class="nota">La richiesta si apre già scritta su WhatsApp o nella tua email. La invii tu.</p><p class="esito" role="status" hidden></p>
  </form>
  <div class="recapiti">
    <ul>
      <li><span>Telefono</span><a href="tel:{TEL}">{TEL_TXT}</a></li>
      <li><span>WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">Scrivi un messaggio</a></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>PEC</span><a href="mailto:{PEC}">{PEC}</a></li>
      <li><span>Officina</span>Frassineto Po (AL), già operativa</li>
      <li><span>Sede legale</span>{SEDE_LEGALE}</li>
      <li><span>Partita IVA</span>02625920067</li>
    </ul>
    {ORARI}
    <p><span class="stato" data-stato></span></p>
    {ARRIVO}
  </div>
</div></section>''' + footer(dialog=False))

# ================================================================== PRIVACY E 404
scrivi("privacy.html", head("privacy.html", "Privacy e cookie | L.M. Autoservizi", "Informativa sul trattamento dei dati personali e sull'uso dei cookie del sito L.M. Autoservizi.") + header("privacy.html")
      + intro_pagina("Privacy", "Come vengono trattati i tuoi dati quando usi questo sito.") + f'''
<section class="sezione"><div class="wrap prosa">
  <h2>Titolare del trattamento</h2>
  <p>L.M. Autoservizi di Miglietta Luca, Via Ticineto 15, 15040 Frassineto Po (AL), P.IVA 02625920067. Email <a href="mailto:{EMAIL}">{EMAIL}</a>, PEC <a href="mailto:{PEC}">{PEC}</a>.</p>
  <h2>Quali dati e perché</h2>
  <p>Il sito non raccoglie dati in automatico. Quando chiedi un ritiro, un preventivo, delle gomme o un ricambio, il modulo prepara un messaggio che invii tu tramite WhatsApp o email: i dati che scrivi (nome, telefono, targa, comune, descrizione) arrivano solo al titolare e servono a risponderti e a preparare il preventivo.</p>
  <p>La base giuridica è la richiesta dell'interessato (misure precontrattuali, art. 6.1.b GDPR). I dati sono conservati per il tempo necessario a gestire la richiesta e gli eventuali obblighi fiscali successivi.</p>
  <h2>Servizi di terze parti</h2>
  <ul><li><strong>WhatsApp</strong> (Meta) ed email: se scegli questi canali, il messaggio viene trattato anche secondo le loro condizioni.</li>
  <li><strong>Google Maps</strong>: i collegamenti alle recensioni aprono il servizio esterno. Nessuna mappa viene caricata nel sito.</li></ul>
  <h2>Cookie</h2>
  <p>Questo sito non usa cookie di profilazione né strumenti di statistica. Per questo non mostra un banner cookie.</p>
  <h2>I tuoi diritti</h2>
  <p>Puoi chiedere in qualsiasi momento di accedere ai tuoi dati, correggerli o cancellarli, scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>
</div></section>''' + footer())
scrivi("404.html", head("404.html", "Pagina non trovata | L.M. Autoservizi", "La pagina che cerchi non esiste.", noindex=True) + header("")
      + intro_pagina("Pagina non trovata", "Questa pagina non esiste. Torna alla home oppure chiamami: ti rimetto in carreggiata.") + f'''
<section class="sezione"><div class="wrap"><div class="azioni"><a class="btn btn--arancio" href="index.html">Torna alla home</a><a class="btn btn--vuoto" href="tel:{TEL}">{I["tel"]}{TEL_TXT}</a></div></div></section>''' + footer())

# ================================================================== stili e script (modelli in sorgente/)
for nome in ("nuovo.css", "nuovo.js"):
    with open(os.path.join(QUI, nome), encoding="utf-8") as f:
        testo = f.read().replace("{{A}}", A)
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
    print("copiato", nome)

# Mantiene funzionanti i link della prima demo e dell'anteprima in nuovo/.
PAGINE = ["index.html", "officina.html", "ritiro-consegna.html", "gomme-ricambi.html",
          "officina-mobile.html", "chi-sono.html", "contatti.html", "privacy.html", "404.html"]
ALIAS = {"servizi.html": "officina.html", "come-funziona.html": "ritiro-consegna.html",
         "servizio-meccanico.html": "officina.html#manutenzione",
         "servizio-diagnosi.html": "officina.html#diagnosi",
         "servizio-elettrauto.html": "officina.html#elettrauto",
         "servizio-gommista.html": "gomme-ricambi.html",
         "servizio-carrozzeria.html": "officina.html#carrozzeria",
         "servizio-prerevisione.html": "officina.html#revisione",
         "servizio-consulenza.html": "officina.html#aziende"}
ALIAS.update({"nuovo/" + pagina: "../" + pagina for pagina in PAGINE})
for nome, destinazione in ALIAS.items():
    scrivi(nome, f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>L.M. Autoservizi — officina a Frassineto Po</title><meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0;url={escape(destinazione, quote=True)}">
<script>var u=new URL({json.dumps(destinazione)},location.href);u.search=location.search;if(!u.hash)u.hash=location.hash;location.replace(u.href);</script>
</head><body><p>Il sito dell'officina è qui: <a href="{escape(destinazione, quote=True)}">continua su L.M. Autoservizi</a>.</p></body></html>
''')

scrivi("robots.txt", "User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
url_sitemap = "".join(f"<url><loc>{DOMINIO}/{'' if pagina == 'index.html' else pagina}</loc></url>\n" for pagina in PAGINE if pagina != "404.html")
scrivi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + url_sitemap + '</urlset>\n')
