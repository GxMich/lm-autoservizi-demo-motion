"""Versione semplice di L.M. Autoservizi: italiano in docs/semplice/, inglese in docs/semplice/en/.
Generazione: python sorgente/genera_semplice.py
Stili e script: sorgente/semplice.css e sorgente/semplice.js, copiati con un hash di versione.
Le foto vere in docs/assets/img/foto/ (preparate da sorgente/foto.py) sostituiscono da sole quelle stock.
LM_PRODUZIONE=1 abilita l'indicizzazione; LM_URL_PAGINE e LM_URL_RISORSE danno gli indirizzi pubblici
usati da canonical, hreflang e anteprime social."""
import hashlib, json, math, os
from html import escape
from contenuti import (TEL, TEL_TXT, WA, EMAIL, PEC, PIVA, MAPS, SEDE_LEGALE, GEAR_PIENO,
                       RECENSIONI, FAQ_R, ATT, FOTO_SLOT, STOCK)

QUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(QUI), "docs")
BASE = os.path.join(DOCS, "semplice")
PRODUZIONE = os.environ.get("LM_PRODUZIONE") == "1"
URL_PAGINE = os.environ.get("LM_URL_PAGINE", "https://lm-autoservizi-demo-motion.vercel.app/semplice/")
URL_RISORSE = os.environ.get("LM_URL_RISORSE", "https://lm-autoservizi-demo-motion.vercel.app/assets/")
ASSET_V = hashlib.sha256(b"".join(open(os.path.join(QUI, f), "rb").read() for f in ("semplice.css", "semplice.js"))).hexdigest()[:10]

# Lingua corrente: R porta alla cartella della versione semplice, A alle risorse condivise in docs/assets.
LINGUA, R, A = "it", "", "../"


def t(it, en):
    return en if LINGUA == "en" else it


def tt(testo):
    """Testo bilingue scritto come coppia (italiano, inglese)."""
    return t(*testo) if isinstance(testo, tuple) else testo


def attr(testo):
    return escape(testo, quote=True)


def tel_txt():
    return t(TEL_TXT, "+39 " + TEL_TXT)


def wa():
    return t(WA, "https://wa.me/393426436085?text=Hi%20Luca%2C%20I%27d%20like%20some%20information.")


NAV = [("officina.html", ("Servizi", "Services")), ("ritiro-consegna.html", ("Ritiro e consegna", "Pick-up & delivery")),
       ("officina-mobile.html", ("Officina mobile", "Mobile workshop")), ("gomme-ricambi.html", ("Gomme e ricambi", "Tyres & parts")),
       ("chi-sono.html", ("Chi sono", "About me")), ("contatti.html", ("Contatti", "Contact"))]


# ---------------------------------------------------------------- icone (disegnate per questo sito)
def svg(corpo, classe="", vb="0 0 24 24"):
    return f'<svg class="ico {classe}" viewBox="{vb}" aria-hidden="true" focusable="false">{corpo}</svg>'


def punti_cerchio(cx, cy, r1, r2, n, inizio=0):
    righe = []
    for k in range(n):
        a = math.radians(inizio + k * 360 / n)
        righe.append(f"M{cx + r1 * math.cos(a):.2f} {cy + r1 * math.sin(a):.2f}L{cx + r2 * math.cos(a):.2f} {cy + r2 * math.sin(a):.2f}")
    return "".join(righe)


I = {
    "tel": svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "chat": svg('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5z"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "check": svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>'),
    "freccia": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "giu": svg('<path d="M12 5v14M6 13l6 6 6-6"/>'),
    "chiudi": svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    "esterno": svg('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "sole": svg(f'<circle cx="12" cy="12" r="4.2"/><path d="{punti_cerchio(12, 12, 7, 9.4, 8)}"/>', "ico-sole"),
    "luna": svg('<path d="M20.5 14.3A8.5 8.5 0 0 1 9.7 3.5a8.5 8.5 0 1 0 10.8 10.8z"/>', "ico-luna"),
}

# Servizi: tratto unico, un dettaglio pieno; ogni icona ha la sua piccola animazione (vedi semplice.css).
_gomma = (f'<g class="gira"><circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="5.6"/>'
          f'<path d="{punti_cerchio(12, 12, 8.1, 9.5, 12)}{punti_cerchio(12, 12, 2.3, 5.6, 5, -90)}"/>'
          f'<circle class="pieno" cx="12" cy="12" r="1.7"/></g>')
ICONE = {
    "meccanica": svg('<path class="chiave" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'
                     '<path class="dado" d="M19.8 16.25 21.1 18.5 19.8 20.75H17.2L15.9 18.5 17.2 16.25Z"/><circle class="pieno dado" cx="18.5" cy="18.5" r="1"/>', "ico-meccanica"),
    "elettrauto": svg('<rect x="2.5" y="7" width="19" height="13" rx="2.2"/><path d="M6.5 7V4.8h3V7M14.5 7V4.8h3V7M5.6 10.6h2.6M15.8 10.6h2.6M17.1 9.3v2.6"/>'
                      '<path class="pieno fulmine" d="M12.9 9.4 9.6 14.2h2.6l-.9 4.4 3.3-5h-2.6z"/>', "ico-elettrauto"),
    "gommista": svg(_gomma, "ico-gommista"),
    "carrozzeria": svg('<path d="M2.6 19.4v-2.6c0-.8.5-1.5 1.3-1.8l2.2-.8 2.6-3.3c.4-.5 1-.8 1.6-.8h4.3c.6 0 1.2.3 1.6.7l3 3.3 1.8.4c.9.2 1.5 1 1.5 1.9v3"/>'
                       '<path d="M2.6 19.4h1.7M9.1 19.4h5.6M19.6 19.4h2.9M7 14.3h11.8M12.4 10.9v3.4"/><circle cx="6.7" cy="19.6" r="2.3"/><circle cx="17.2" cy="19.6" r="2.3"/>'
                       '<path class="pieno scintilla" d="M19.5 1.6l.75 1.85 1.85.75-1.85.75-.75 1.85-.75-1.85-1.85-.75 1.85-.75z"/>', "ico-carrozzeria"),
    "diagnosi": svg('<path class="spia" d="M6.5 9.5h3L11 8h3.5l1 1.5H18v2h1.5v-2H21V18h-1.5v-2.5H18V18h-3.5L13 19.5H8.5l-2-2z"/>'
                    '<path d="M10.5 5h4M12.5 5v3M3 10.5v6M3 13.5h3.5"/>', "ico-diagnosi"),
    "soccorso": svg('<path d="M6 18v-4h8.5"/><path d="M14.5 18V9.8h3.4c.5 0 .9.2 1.2.6l2.6 3.4c.2.3.3.6.3 1V18"/><path class="pieno" d="M16.3 11.3h1.8l1.6 2.2h-3.4z"/>'
                    '<path d="M5.8 18h1.4M11.2 18h4.8M20 18h2M10 14 6.5 7.2H3.5"/><circle cx="9.2" cy="18.2" r="2"/><circle cx="18" cy="18.2" r="2"/>'
                    '<g class="gancio"><path d="M3.5 7.2v3.3"/><path d="M3.5 10.5a1.5 1.5 0 1 0 1.5 1.5"/></g>', "ico-soccorso"),
    "aziende": svg('<rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8.5 7.5V5.8c0-1 .8-1.8 1.8-1.8h3.4c1 0 1.8.8 1.8 1.8v1.7M3 12.5h18"/>'
                   '<path class="pieno" d="M10.8 11.3h2.4v2.4h-2.4z"/>', "ico-aziende"),
    "altro": svg('<circle cx="12" cy="12" r="9.5"/><path d="M9.3 9.3a2.8 2.8 0 1 1 3.9 2.6c-.7.3-1.2 1-1.2 1.8v.6"/><circle class="pieno" cx="12" cy="17.2" r="1"/>', "ico-altro"),
}
# Vantaggi (si disegnano a tratto entrando nello schermo)
VANTAGGI_ICO = {
    "cortesia": svg('<path d="M2.6 18.4v-2.6c0-.8.5-1.5 1.3-1.8l2.2-.8 2.6-3.3c.4-.5 1-.8 1.6-.8h4.3c.6 0 1.2.3 1.6.7l3 3.3 1.8.4c.9.2 1.5 1 1.5 1.9v3"/>'
                    '<path d="M2.6 18.4h1.7M9.1 18.4h5.6M19.6 18.4h2.9M7 13.3h11.8M12.4 9.9v3.4"/><circle cx="6.7" cy="18.6" r="2.3"/><circle cx="17.2" cy="18.6" r="2.3"/>'),
    "rotta": svg('<circle cx="5.5" cy="18.5" r="2.2"/><circle cx="18.5" cy="5.5" r="2.2"/><path d="M7.7 18.5h8.1a3.2 3.2 0 0 0 0-6.4H8.2a3.2 3.2 0 0 1 0-6.4h8.1"/>'),
    "mobile": svg('<path d="M2 17V7.5C2 6.7 2.7 6 3.5 6H14v11"/><path d="M14 9.5h4.2c.4 0 .8.2 1 .5l2.5 3.5c.2.2.3.5.3.8V17h-1.8M8.5 17h7.2"/>'
                  f'<circle cx="6.5" cy="17.5" r="2"/><circle cx="17.7" cy="17.5" r="2"/><circle cx="8" cy="11.3" r="1.6"/><path d="{punti_cerchio(8, 11.3, 2.5, 3.4, 6, -90)}"/>'),
    "aziende": svg('<rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8.5 7.5V5.8c0-1 .8-1.8 1.8-1.8h3.4c1 0 1.8.8 1.8 1.8v1.7M3 12.5h18M10.8 11.3h2.4v2.4h-2.4z"/>'),
}


def ruota(cx, r, cy):
    return f'<g class="ruota"><circle cx="{cx}" cy="{cy}" r="{r}"/><circle class="pieno" cx="{cx}" cy="{cy}" r="1.6"/></g>'


# Sagome laterali dei mezzi: tratto pieno, pochi dettagli, tutte appoggiate sulla stessa linea di terra (y = 32).
VEICOLI = {
    "auto": ('<path d="M6 27.4V22.8c0-1.5 1-2.8 2.4-3.2L15.2 17.6l6.1-5.6c.8-.7 1.8-1.1 2.9-1.1h11.6c1.2 0 2.3.5 3.1 1.3l5.9 5.6 9.4 1.6c2 .3 3.5 2.1 3.5 4.1v3.9"/>'
             '<path d="M6 27.4h4.9M22.1 27.4h19.8M53.1 27.4h4.6"/>'
             '<path d="M18.6 17.6l4.1-3.8c.5-.4 1.1-.7 1.8-.7H31v4.5zM33.6 13.1h2.7c.7 0 1.3.3 1.8.7l4.1 3.8h-8.6z"/>'
             + ruota(16.5, 4.6, 27.4) + ruota(47.5, 4.6, 27.4)),
    "fuoristrada": ('<path d="M5.5 26.7V9.6c0-1.4 1.1-2.5 2.5-2.5h28.9c.8 0 1.6.4 2.1 1l5.6 7.2 9.1 1.3c1.9.3 3.3 1.9 3.3 3.8v6.3"/>'
                    '<path d="M5.5 26.7h4.2M22.3 26.7h18.4M53.3 26.7h3.7M12 4.4h21M14.5 4.4v2.7M30.5 4.4v2.7"/>'
                    '<path d="M11 10.6h8.5a1 1 0 0 1 1 1v2.7a1 1 0 0 1-1 1H11a1 1 0 0 1-1-1v-2.7a1 1 0 0 1 1-1zM23.5 10.6h11.2c.5 0 .9.2 1.2.6l3.3 4.1H23.5z"/>'
                    + ruota(16, 5.3, 26.7) + ruota(47, 5.3, 26.7)),
    "furgone": ('<path d="M5 27.4V9.4C5 8 6.1 6.9 7.5 6.9h29.7c1.1 0 2.1.5 2.7 1.4l5.9 8.6 7.6 1.7c1.8.4 3.1 2 3.1 3.9v4.9"/>'
                '<path d="M5 27.4h4.9M21.1 27.4h20.8M53.1 27.4h3.4M24 9.4v15"/>'
                '<path d="M38.8 10.6h.4c.5 0 .9.2 1.2.6l3.6 5.7h-5.2z"/>'
                + ruota(15.5, 4.6, 27.4) + ruota(47.5, 4.6, 27.4)),
    "camper": ('<path d="M5 27.4V7c0-1.1.9-2 2-2h37.6c1.1 0 2 .9 2 2v4.6h-5.4v1.6h4.2c.6 0 1.1.3 1.5.7l3.9 4.9 2.9.7c1.6.4 2.7 1.8 2.7 3.4v4.5"/>'
               '<path d="M5 27.4h4.9M21.1 27.4h21.3M53.6 27.4h2.8"/>'
               '<path d="M10.8 9.6h9.4a1.2 1.2 0 0 1 1.2 1.2v3.2a1.2 1.2 0 0 1-1.2 1.2h-9.4a1.2 1.2 0 0 1-1.2-1.2v-3.2a1.2 1.2 0 0 1 1.2-1.2zM42 16h2.4c.4 0 .8.2 1 .5l2.2 2.8H42z"/>'
               + ruota(15.5, 4.6, 27.4) + ruota(48, 4.6, 27.4)),
    "ciclomotore": ('<g transform="translate(0 3)">'
                    '<path d="M7.5 21c0-5 3.6-8.5 9-8.5H27c.8 0 1.5.7 1.5 1.5v2.5c0 2.5-1.8 4.5-4.3 4.5h-4.4a5.5 5.5 0 0 0-7.6 0z"/>'
                    '<path d="M15 12.5c.4-1.7 1.7-2.8 3.5-2.8h7.5c.8 0 1.5.7 1.5 1.5v1.3"/>'
                    '<path d="M24.2 21h13.3c1.8-3.8 3.2-8.4 4-13.5M38.5 6.5h6.5M42 8l5 16.5M43.4 19.6c1.9-1.3 4.6-1.3 6.6.2"/>'
                    + ruota(16, 4, 25) + ruota(47, 4, 25) + '</g>'),
    "altro": ('<circle cx="32" cy="18.5" r="12"/><path d="M28.4 15a3.7 3.7 0 1 1 5.2 3.4c-.9.4-1.6 1.3-1.6 2.3v.9"/>'
              '<circle class="pieno" cx="32" cy="25.6" r="1.4"/>'),
}
# (id, nome, valore per il messaggio, aiuto sotto le note)
MEZZI = [("auto", ("Auto", "Car"), ("Auto", "Car"),
          ("Marca e modello aiutano, per esempio Fiat Panda 2015.", "Make and model help, for example Fiat Panda 2015.")),
         ("fuoristrada", ("Fuoristrada", "Off-road"), ("Fuoristrada", "Off-road"),
          ("Marca e modello aiutano, per esempio Suzuki Jimny 2019.", "Make and model help, for example Suzuki Jimny 2019.")),
         ("furgone", ("Furgone", "Van"), ("Furgone", "Van"),
          ("Marca e modello aiutano, per esempio Fiat Ducato 2017.", "Make and model help, for example Fiat Ducato 2017.")),
         ("camper", ("Camper", "Motorhome"), ("Camper", "Motorhome"),
          ("Marca e modello aiutano, per esempio mansardato su Ducato, 2016.", "Make and model help, for example a Ducato-based motorhome, 2016.")),
         ("ciclomotore", ("Ciclomotore", "Moped"), ("Ciclomotore", "Moped"),
          ("Marca e modello aiutano, per esempio Piaggio Liberty 50.", "Make and model help, for example Piaggio Liberty 50.")),
         ("altro", ("Altro", "Other"), ("Altro mezzo", "Other vehicle"),
          ("Scrivimi che mezzo è, con marca e modello.", "Tell me what vehicle it is, with make and model."))]


def veicolo(chi):
    return svg(VEICOLI[chi], f"veicolo veicolo--{chi}", "0 0 64 36")


# ---------------------------------------------------------------- servizi (le caselle della home)
# (id, nome, descrizione breve, suggerimento per le note, opzioni)
SERVIZI = [
    ("meccanica", ("Meccanica", "Mechanics"),
     ("Tagliandi, riparazioni, manutenzione ordinaria e straordinaria", "Servicing, repairs, routine and extraordinary maintenance"),
     ("Es. tagliando, rumore in frenata, perdita d'olio.", "E.g. service due, noise when braking, oil leak."), ""),
    ("elettrauto", ("Elettrauto", "Auto electrics"),
     ("Avviamento, batteria e ricarica, luci, climatizzatore", "Starting, battery and charging, lights, air conditioning"),
     ("Es. non parte, la batteria si scarica, il clima non raffredda.", "E.g. it won't start, the battery keeps going flat, the A/C isn't cooling."), ""),
    ("gommista", ("Gommista", "Tyres"),
     ("Cambio, equilibratura, convergenza e vendita di pneumatici", "Fitting, balancing, alignment and tyre sales"),
     ("Es. cambio stagionale o foratura. La misura è scritta sul fianco della gomma.", "E.g. seasonal change or a puncture. The size is written on the tyre sidewall."), ""),
    ("carrozzeria", ("Carrozzeria", "Bodywork"),
     ("Carrozzeria, verniciatura e saldatura", "Bodywork, painting and welding"),
     ("Es. urto sul paraurti, graffio sulla portiera. Le foto del danno puoi mandarmele su WhatsApp.", "E.g. dented bumper, scratched door. You can send me photos of the damage on WhatsApp."), ""),
    ("diagnosi", ("Diagnosi e pre-revisione", "Diagnostics & pre-inspection"),
     ("Spie accese, centraline, controllo gratuito prima della revisione", "Warning lights, ECUs, free check before the roadworthiness test"),
     ("Es. spia del motore accesa, revisione in scadenza a marzo.", "E.g. engine warning light on, inspection due in March."), ""),
    ("soccorso", ("Soccorso", "Roadside help"),
     ("Rimasto fermo? Dimmi dove sei: arrivo con l'officina mobile", "Broken down? Tell me where you are: I come with the mobile workshop"),
     ("Dove ti trovi e cosa è successo. Se sei in un punto pericoloso, chiamami.", "Where you are and what happened. If you're in a dangerous spot, call me."), "urgente"),
]
# Richieste che non sono caselle: (nome, suggerimento, opzioni, titolo della tendina)
EXTRA = {
    "ritiro": (("Ritiro e consegna", "Pick-up and delivery"),
               ("Dove si trova il mezzo e cosa non va. Ti dico subito se e quanto costa il ritiro.", "Where the vehicle is and what's wrong. I'll tell you straight away whether the pick-up has a cost."), "", None),
    "aziende": (("Consulenza alle imprese", "Business consulting"),
                ("Che attività hai e di cosa avresti bisogno.", "What your business does and what you need."), "senza-mezzo", None),
    "altro": (("Non so quale sia il problema", "I don't know what's wrong"),
              ("Raccontami cosa fa il mezzo: rumori, spie accese, quando succede.", "Tell me what the vehicle does: noises, warning lights, when it happens."), "",
              ("Descrivimi il problema", "Describe the problem")),
}


def dati_servizio(nome, nota, opzioni="", titolo=None):
    """Attributi della tendina. In inglese il nome italiano viaggia a parte: nel messaggio Luca lo legge tra parentesi."""
    a = f'data-servizio="{attr(tt(nome))}" data-nota="{attr(tt(nota))}"'
    if LINGUA == "en":
        a += f' data-servizio-it="{attr(nome[0])}"'
    if titolo:
        a += f' data-titolo="{attr(tt(titolo))}"'
    if "urgente" in opzioni:
        a += " data-urgente"
    if "senza-mezzo" in opzioni:
        a += " data-senza-mezzo"
    return a


def apri(chiave, testo, classe="btn btn--arancio", icona="freccia"):
    nome, nota, opzioni, titolo = EXTRA[chiave]
    return f'<button type="button" class="{classe}" {dati_servizio(nome, nota, opzioni, titolo)}>{testo} {I[icona] if icona else ""}</button>'


def apri_servizio(chi, testo, classe="btn btn--arancio"):
    s = next(x for x in SERVIZI if x[0] == chi)
    return f'<button type="button" class="{classe}" {dati_servizio(s[1], s[3], s[4])}>{testo} {I["freccia"]}</button>'


# ---------------------------------------------------------------- foto
ALT_EN = {
    "luca": ("Example photo: a mechanic's hands working on an engine", "Luca Miglietta at work in his workshop"),
    "officina": ("Example photo: cars and equipment in a workshop", "Inside the L.M. Autoservizi workshop in Frassineto Po"),
    "ingresso": ("Example photo: a workshop with cars and a lift", "The entrance of the L.M. Autoservizi workshop"),
    "officina-mobile": ("Example photo: engine work outdoors", "The L.M. Autoservizi mobile workshop van"),
    "ritiro": ("Example photo: handing over car keys", "Luca hands over the courtesy car keys"),
}


def foto_info(spazio):
    (rw, rh), stock, alt_stock, alt_vero = FOTO_SLOT[spazio]
    if LINGUA == "en" and spazio in ALT_EN:
        alt_stock, alt_vero = ALT_EN[spazio]
    if os.path.exists(os.path.join(DOCS, "assets", "img", "foto", spazio + ".webp")):
        return A + "assets/img/foto/" + spazio, 1600, round(1600 * rh / rw), alt_vero, False
    w, h = STOCK[stock]
    return A + "assets/img/campione/" + stock, w, h, alt_stock, True


def img(spazio, sizes, lazy=True, alt=None, priorita=False, piccola=False):
    base, w, h, alt_def, _ = foto_info(spazio)
    testo_alt = attr(alt_def if alt is None else alt)
    if piccola:
        return f'<img src="{base}-800.webp" width="800" height="{round(800 * h / w)}" alt="{testo_alt}" loading="lazy" decoding="async">'
    carica = ' fetchpriority="high"' if priorita else (' loading="lazy" decoding="async"' if lazy else "")
    return (f'<img src="{base}.webp" srcset="{base}-800.webp 800w, {base}.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{testo_alt}"{carica}>')


def nota_foto(spazio):
    return f'<span class="nota-foto">{t("Foto di esempio", "Example photo")}</span>' if foto_info(spazio)[4] else ""


def foto(spazio, sizes, classe="foto", iride=True):
    return f'<figure class="{classe}"{" data-iride" if iride else ""}>{img(spazio, sizes)}{nota_foto(spazio)}</figure>'


def ci_sono_foto_stock():
    return any(foto_info(s)[4] for s in FOTO_SLOT)


# ---------------------------------------------------------------- dati strutturati
def url_pagina(pagina, lingua=None):
    lingua = lingua or LINGUA
    return URL_PAGINE + ("en/" if lingua == "en" else "") + ("" if pagina == "index.html" else pagina)


def azienda():
    return {"@context": "https://schema.org", "@type": "AutoRepair", "@id": URL_PAGINE + "#azienda",
            "name": "L.M. Autoservizi di Miglietta Luca",
            "description": t("Officina multimarca a Frassineto Po: meccanica, elettrauto, gommista, carrozzeria, diagnosi centraline e pre-revisione. Vettura di cortesia gratuita, ritiro e consegna, officina mobile.",
                             "Multi-brand workshop in Frassineto Po, Italy: mechanics, auto electrics, tyres, bodywork, ECU diagnostics and pre-inspection. Free courtesy car, pick-up and delivery, mobile workshop."),
            "url": url_pagina("index.html"), "telephone": TEL, "email": EMAIL, "vatID": "IT" + PIVA,
            "image": URL_RISORSE + "img/campione/officina.webp", "logo": URL_RISORSE + "img/favicon-192.png",
            "founder": {"@type": "Person", "name": "Luca Miglietta"},
            "address": {"@type": "PostalAddress", "addressLocality": "Frassineto Po", "postalCode": "15040", "addressRegion": "AL", "addressCountry": "IT"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "19:30"}],
            "paymentAccepted": "Contanti, Carta di credito, Bancomat",
            "areaServed": [{"@type": "City", "name": "Frassineto Po"}, {"@type": "City", "name": "Casale Monferrato"}]}


def briciole(pagina, nome):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": url_pagina("index.html")},
        {"@type": "ListItem", "position": 2, "name": nome, "item": url_pagina(pagina)}]}


# ---------------------------------------------------------------- pezzi comuni
def head(pagina, titolo, descrizione, schema=(), immagine="officina", noindex=False):
    url = url_pagina(pagina)
    base, w, h, alt, _ = foto_info(immagine)
    immagine_url = URL_RISORSE + base[len(A + "assets/"):] + ".webp"
    robots = f'<link rel="canonical" href="{url}">' if PRODUZIONE and not noindex else '<meta name="robots" content="noindex, nofollow">'
    alternative = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_pagina(pagina, l)}">\n' for l in ("it", "en"))
    alternative += f'<link rel="alternate" hreflang="x-default" href="{url_pagina(pagina, "it")}">\n'
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in schema)
    return f'''<!doctype html>
<html lang="{LINGUA}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titolo}</title>
<meta name="description" content="{attr(descrizione)}">
{robots}
{alternative}<meta name="theme-color" content="#0b0d10">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t("it_IT", "en_GB")}">
<meta property="og:locale:alternate" content="{t("en_GB", "it_IT")}">
<meta property="og:site_name" content="L.M. Autoservizi">
<meta property="og:title" content="{attr(titolo)}">
<meta property="og:description" content="{attr(descrizione)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{immagine_url}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta property="og:image:alt" content="{attr(alt or "L.M. Autoservizi, officina a Frassineto Po")}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{A}assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{A}assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="{A}assets/img/favicon-180.png">
<link rel="manifest" href="{A}site.webmanifest">
<script>(function(d){{d.classList.add("js");try{{if(localStorage.getItem("lm-tema")==="chiaro"){{d.setAttribute("data-tema","chiaro");document.querySelector('meta[name="theme-color"]').content="#f3f4f6"}}}}catch(e){{}}try{{if(!matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("mo")}}catch(e){{}}setTimeout(function(){{d.classList.remove("mo")}},4000)}})(document.documentElement);</script>
<link rel="preload" href="{A}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}semplice.css?v={ASSET_V}">
{ld}</head>
<body class="p-{pagina[:-5]}">
<a class="salta-link" href="#contenuto">{t("Vai al contenuto", "Skip to content")}</a>
'''


def link_lingua(pagina):
    """Lo stesso contenuto nell'altra lingua."""
    destinazione = "" if pagina == "index.html" else pagina
    if LINGUA == "it":
        return f'<a class="lingua" href="en/{destinazione}" hreflang="en" lang="en" aria-label="English version">EN</a>'
    return f'<a class="lingua" href="../{destinazione}" hreflang="it" lang="it" aria-label="Versione italiana">IT</a>'


def testata(pagina):
    def voci(con_home=False):
        lista = ([("./", ("Home", "Home"))] if con_home else []) + NAV
        return "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == pagina or (h == "./" and pagina == "index.html") else ""}>{tt(n)}</a></li>' for h, n in lista)
    etichetta_tema = t("Passa al tema chiaro", "Switch to light theme")
    return f'''<header class="testata">
  <div class="wrap testata-riga">
    <a class="marchio" href="./"><img src="{A}assets/img/logo-arancio-84.png" width="40" height="40" alt=""><span>L.M. Autoservizi<small>{t("Officina a Frassineto Po", "Workshop in Frassineto Po")}</small></span></a>
    <nav class="nav" aria-label="{t("Principale", "Main")}"><ul>{voci()}</ul></nav>
    <div class="testata-azioni">
      {link_lingua(pagina)}
      <button class="tema-bottone" type="button" data-tema-bottone aria-label="{etichetta_tema}">{I["sole"]}{I["luna"]}</button>
      <a class="btn btn--arancio btn--piccolo testata-chiama" href="tel:{TEL}" aria-label="{t("Chiama Luca al", "Call Luca on")} {tel_txt()}">{I["tel"]}<span>{t("Chiama", "Call")}</span></a>
      <button class="menu-bottone" type="button" aria-expanded="false" aria-controls="menu" aria-label="{t("Apri il menu", "Open the menu")}"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" hidden data-lenis-prevent>
  <nav aria-label="Menu"><ul>{voci(True)}</ul></nav>
  <div class="menu-piede">
    <p class="stato" data-stato></p>
    <div class="azioni">
      <a class="btn btn--arancio" href="tel:{TEL}">{I["tel"]}{t("Chiama", "Call")} {tel_txt()}</a>
      <a class="btn btn--vuoto" href="{wa()}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a>
      <button class="btn btn--vuoto" type="button" data-tema-bottone aria-label="{etichetta_tema}">{I["sole"]}{I["luna"]}<span data-tema-testo>{t("Tema chiaro", "Light theme")}</span></button>
    </div>
  </div>
</div>
<main id="contenuto">
'''


def scheda():
    scelte = []
    for i, (chi, nome, valore, aiuto) in enumerate(MEZZI):
        dati = f'value="{attr(tt(valore))}" data-consiglio="{attr(tt(aiuto))}"'
        if LINGUA == "en":
            dati += f' data-it="{attr(valore[0])}"'
        scelte.append(f'<label><input type="radio" name="mezzo" {dati}{" checked" if i == 0 else ""}><span>{veicolo(chi)}<b>{tt(nome)}</b></span></label>')
    return f'''<dialog class="scheda" id="scheda" aria-labelledby="scheda-t" data-lenis-prevent>
  <form class="scheda-form" novalidate>
    <div class="scheda-maniglia" aria-hidden="true"></div>
    <header class="scheda-testa">
      <h2 id="scheda-t" tabindex="-1">{tt(SERVIZI[0][1])}</h2>
      <button type="button" class="scheda-chiudi" data-chiudi aria-label="{t("Chiudi", "Close")}">{I["chiudi"]}</button>
    </header>
    <div class="scheda-corpo">
      <fieldset class="mezzi" data-mezzi>
        <legend>{t("Che mezzo è?", "What vehicle is it?")}</legend>
        <div>{"".join(scelte)}</div>
      </fieldset>
      <div class="campo">
        <label for="scheda-note">{t("Scrivimi due righe", "Write me a couple of lines")} <span>({t("facoltativo", "optional")})</span></label>
        <textarea id="scheda-note" name="note" rows="3" maxlength="600" aria-describedby="scheda-aiuto"></textarea>
        <p class="aiuto" id="scheda-aiuto" data-aiuto></p>
      </div>
      <div class="scheda-azioni">
        <button type="submit" class="btn btn--arancio" data-invia>{I["chat"]}{t("Invia su WhatsApp", "Send on WhatsApp")}</button>
        <a class="btn btn--vuoto" href="tel:{TEL}" data-chiama>{I["tel"]}{t("Chiama", "Call")} {tel_txt()}</a>
      </div>
      <p class="scheda-nota" data-esito role="status">{t("Si apre WhatsApp con il messaggio già scritto: l'invio lo confermi tu.", "WhatsApp opens with the message already written: you confirm the sending.")}</p>
    </div>
  </form>
</dialog>
'''


def orari():
    return f'''<table class="orari"><caption class="sr">{t("Orari di apertura", "Opening hours")}</caption>
  <tr data-giorni="1,2,3,4,5"><th scope="row">{t("Lunedì – venerdì", "Monday – Friday")}</th><td>{t("7:30 – 19:30, continuato", "7:30 – 19:30, no lunch break")}</td></tr>
  <tr data-giorni="6,0"><th scope="row">{t("Sabato e domenica", "Saturday and Sunday")}</th><td>{t("Chiuso", "Closed")}</td></tr>
</table>'''


def piede(pagina, extra=""):
    voci = "".join(f'<li><a href="{h}">{tt(n)}</a></li>' for h, n in NAV)
    servizi = "#servizi" if pagina == "index.html" else "./#servizi"
    nota = f'<span>{t("Le fotografie sono di esempio: verranno sostituite con quelle dell’officina.", "The photos are examples: they will be replaced with photos of the workshop.")}</span>' if ci_sono_foto_stock() else ""
    return f'''</main>
<footer class="piede">
  <div class="wrap piede-griglia">
    <div class="piede-marchio">
      <img src="{A}assets/img/logo-arancio-84.png" width="52" height="52" alt="" loading="lazy">
      <p><strong>L.M. Autoservizi di Miglietta Luca</strong><br>{t("Officina multimarca a Frassineto Po. Ritiro e consegna, vettura di cortesia gratuita e officina mobile.", "Multi-brand workshop in Frassineto Po. Pick-up and delivery, free courtesy car and mobile workshop.")}</p>
    </div>
    <div><h2>{t("Pagine", "Pages")}</h2><ul>{voci}</ul></div>
    <div><h2>{t("Contatti", "Contact")}</h2><ul>
      <li><a href="tel:{TEL}">{tel_txt()}</a></li>
      <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="mailto:{PEC}">PEC: {PEC}</a></li></ul></div>
    <div><h2>{t("Orari", "Opening hours")}</h2><ul>
      <li>{t("Lunedì – venerdì", "Monday – Friday")}<br>{t("7:30 – 19:30, continuato", "7:30 – 19:30, no lunch break")}</li>
      <li>{t("Sabato e domenica chiuso", "Closed on Saturday and Sunday")}</li>
      <li><span class="stato" data-stato></span></li></ul></div>
  </div>
  <div class="wrap piede-basso">
    <span>© <span data-anno>2026</span> L.M. Autoservizi di Miglietta Luca · {t("Sede legale", "Registered office")}: {SEDE_LEGALE} · {t("P.IVA", "VAT no.")} {PIVA}</span>
    {nota}
    <a href="privacy.html">{t("Privacy e cookie", "Privacy and cookies")}</a>
  </div>
</footer>
<nav class="barra" aria-label="{t("Azioni rapide", "Quick actions")}">
  <a href="tel:{TEL}">{I["tel"]}{t("Chiama", "Call")}</a>
  <a href="{servizi}">{ICONE["meccanica"]}{t("Servizi", "Services")}</a>
  <a href="{wa()}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a>
</nav>
{scheda()}{extra}<script src="{A}assets/js/vendor/gsap.min.js" defer></script>
<script src="{A}assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{A}assets/js/vendor/lenis.min.js" defer></script>
<script src="{R}semplice.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def intro(titolo, testo):
    return f'''
<section class="intro">
  <div class="intro-ingranaggio" aria-hidden="true"><svg viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg></div>
  <div class="wrap"><h1><span class="riga"><span>{titolo}</span></span></h1><p class="lead intro-lead">{testo}</p></div>
</section>
'''


def casella(s, con_foto=True):
    chi, nome, desc, nota, opzioni = s
    foto_html = f'<span class="servizio-foto" aria-hidden="true">{img("servizio-" + chi, "", piccola=True, alt="")}</span>' if con_foto else ""
    return f'''<li><button type="button" class="servizio servizio--{chi}{" servizio--urgente" if "urgente" in opzioni else ""}" {dati_servizio(nome, nota, opzioni)}>
  {foto_html}<span class="servizio-ico" aria-hidden="true">{ICONE[chi]}</span>
  <span class="servizio-nome">{tt(nome)}</span><span class="servizio-desc">{tt(desc)}</span>
</button></li>'''


def griglia_servizi(con_foto=True):
    nome, nota, opzioni, titolo = EXTRA["altro"]
    altro = f'''<li class="servizi-largo"><button type="button" class="servizio servizio--largo" {dati_servizio(nome, nota, opzioni, titolo)}>
  <span class="servizio-ico" aria-hidden="true">{ICONE["altro"]}</span>
  <span class="servizio-testo"><span class="servizio-nome">{t("Non so cos'ha", "Not sure what's wrong")}</span><span class="servizio-desc">{t("Descrivimi il problema e lo capiamo insieme", "Describe the problem and we'll work it out together")}</span></span>
</button></li>'''
    return f'<ul class="servizi-griglia">{"".join(casella(s, con_foto) for s in SERVIZI)}{altro}</ul>'


def finale(titolo=None, testo=None):
    titolo = titolo or t("Ti serve una mano con il tuo mezzo?", "Need a hand with your vehicle?")
    testo = testo or t("Chiamami o scrivimi: ti dico quando posso ritirarlo o quando puoi portarmelo.", "Call or message me: I'll tell you when I can collect it or when you can bring it in.")
    return f'''
<section class="finale">
  <div class="wrap finale-riga">
    <div><h2>{titolo}</h2><p>{testo}</p></div>
    <div class="finale-azioni">
      <a class="numerone" href="tel:{TEL}">{tel_txt()}</a>
      <div class="azioni"><a class="btn btn--arancio" href="./#servizi">{t("Scegli il servizio", "Choose the service")} {I["freccia"]}</a><a class="btn btn--vuoto" href="{wa()}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a></div>
    </div>
  </div>
</section>
'''


def spunte(voci):
    return '<ul class="spunte">' + "".join(f"<li>{I['check']}<span>{tt(v)}</span></li>" for v in voci) + "</ul>"


def scrivi(nome, contenuto):
    cartella = os.path.join(BASE, "en") if LINGUA == "en" else BASE
    os.makedirs(cartella, exist_ok=True)
    with open(os.path.join(cartella, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", ("semplice/en/" if LINGUA == "en" else "semplice/") + nome, len(contenuto))


# ================================================================== HOME
def pagina_home():
    riga_a, riga_b = t("Meccanico", "Your trusted"), t("di fiducia", "mechanic")
    caratteri = max(len(riga_a), len(riga_b) + 1)
    recensioni = "".join(f'<figure class="voce"><blockquote lang="it"><p>{testo}</p></blockquote><figcaption>{nome}</figcaption></figure>' for testo, nome in RECENSIONI)
    eroe_stock = foto_info("eroe")[4]
    scrivi("index.html", head("index.html", t("Meccanico di fiducia a Frassineto Po | L.M. Autoservizi", "Trusted mechanic in Frassineto Po | L.M. Autoservizi"),
                              t("L'officina di Luca Miglietta a Frassineto Po: meccanica, elettrauto, gomme, carrozzeria e diagnosi, multimarca. Vettura di cortesia gratuita e officina mobile.",
                                "Luca Miglietta's workshop in Frassineto Po, Italy: mechanics, auto electrics, tyres, bodywork and diagnostics, all makes. Free courtesy car and mobile workshop."),
                              [azienda()], immagine="officina") + testata("index.html") + f'''
<section class="eroe" aria-labelledby="eroe-t">
  <div class="eroe-fascio" aria-hidden="true"></div>
  <div class="eroe-scena" aria-hidden="true">
    <div class="eroe-ingranaggio">
      <svg class="eroe-aloni" viewBox="-400 -400 800 800"><circle r="340"/><circle r="390"/></svg>
      <div class="eroe-finestra">{img("eroe", "(max-width: 899px) 70vw, 40vw", priorita=True, alt="")}</div>
      <svg class="eroe-anello" viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg>
    </div>
  </div>
  <div class="eroe-righe">
    <h1 id="eroe-t" style="--car: {caratteri}"><span class="riga riga-a"><span>{riga_a}</span></span><span class="riga riga-b"><span>{riga_b}<em>.</em></span></span></h1>
  </div>
  <div class="eroe-basso wrap">
    <div class="eroe-testo">
      <p>{t("<strong>Sono Luca Miglietta, e l'officina è la mia.</strong> Meccanica, elettrauto, gomme e carrozzeria a Frassineto Po, su tutte le marche. Dalla prima telefonata alla riconsegna parli sempre con me.",
              "<strong>I'm Luca Miglietta, and this is my workshop.</strong> Mechanics, auto electrics, tyres and bodywork in Frassineto Po, all makes. From the first call to the hand-back, you always deal with me.")}</p>
      <div class="azioni">
        <a class="btn btn--arancio" href="#servizi">{t("Cosa ti serve?", "What do you need?")} {I["giu"]}</a>
        <a class="btn btn--vuoto eroe-chiama" href="tel:{TEL}">{I["tel"]}{tel_txt()}</a>
      </div>
    </div>
    <div class="eroe-info"><p class="stato" data-stato></p>{f'<p class="nota-foto">{t("Foto di esempio", "Example photo")}</p>' if eroe_stock else ""}</div>
  </div>
</section>

<section class="servizi" id="servizi" aria-labelledby="servizi-t">
  <div class="wrap">
    <div class="servizi-testa">
      <h2 id="servizi-t">{t("Cosa ti serve?", "What do you need?")}</h2>
      <div class="servizi-testa-lato">
        <p class="lead">{t("Tocca il servizio, scegli il mezzo e scrivimi due righe. Ti rispondo io, di persona.", "Tap the service, choose your vehicle and send me a couple of lines. I'll answer personally.")}</p>
        <a class="link" href="officina.html">{t("Tutti i servizi nel dettaglio", "All services in detail")} {I["freccia"]}</a>
      </div>
    </div>
    {griglia_servizi()}
  </div>
</section>

<section class="luca" aria-labelledby="luca-t">
  <div class="wrap luca-griglia">
    {foto("luca", "(max-width: 899px) 100vw, 45vw", "foto luca-foto")}
    <div class="luca-testo">
      <h2 id="luca-t">{t("Un solo riferimento, dall'inizio alla fine.", "One point of contact, from start to finish.")}</h2>
      <p class="lead">{t("Mi chiamo Luca Miglietta. Lavoro da solo: il tuo mezzo lo segue una persona sola, e al telefono rispondo io.", "My name is Luca Miglietta. I work alone: one person looks after your vehicle, and I'm the one who answers the phone.")}</p>
      <p>{t("Prima ascolto il problema, poi ti dico cosa serve e quanto costa. Il preventivo è gratuito e si parte solo quando ti va bene.", "First I listen to the problem, then I tell you what's needed and what it costs. The quote is free and work starts only when you're happy with it.")}</p>
      <dl class="fatti">
        <div><dt>{t("Esperienza", "Experience")}</dt><dd>{t("Più di dieci anni, tutte le marche", "Over ten years, all makes")}</dd></div>
        <div><dt>{t("Abilitazione", "Qualification")}</dt><dd>{t("Responsabile tecnico delle revisioni", "Technical manager for vehicle inspections")}</dd></div>
        <div><dt>{t("Qualifica", "Training")}</dt><dd>{t("Riparazioni elettromeccaniche dell'autoveicolo", "Vehicle electromechanical repairs")}</dd></div>
        <div><dt>{t("Climatizzatori", "Air conditioning")}</dt><dd>{t("Recupero dei gas fluorurati, Reg. CE 307/2008", "F-gas recovery, Reg. EC 307/2008")}</dd></div>
      </dl>
      <a class="link" href="chi-sono.html">{t("Conosci Luca", "About Luca")} {I["freccia"]}</a>
    </div>
  </div>
</section>

<section class="vantaggi" aria-labelledby="vantaggi-t">
  <div class="wrap">
    <h2 id="vantaggi-t">{t("Tu hai i tuoi impegni.<br>Io penso al mezzo.", "You have your commitments.<br>I take care of the vehicle.")}</h2>
    <ul class="vantaggi-lista">
      <li>{VANTAGGI_ICO["cortesia"]}<h3>{t("Vettura di cortesia gratuita", "Free courtesy car")}</h3><p>{t("Con il pieno, pulita e igienizzata, per tutto il tempo della riparazione.", "Fuelled, clean and sanitised, for as long as the repair takes.")}</p><a class="link" href="ritiro-consegna.html#domande">{t("Come funziona", "How it works")} {I["freccia"]}</a></li>
      <li>{VANTAGGI_ICO["rotta"]}<h3>{t("Ritiro e riconsegna", "Pick-up and delivery")}</h3><p>{t("Passo a casa o al lavoro, riparo il mezzo in officina e te lo riporto dove vuoi.", "I collect from your home or workplace, repair the vehicle in the workshop and bring it back wherever you like.")}</p><a class="link" href="ritiro-consegna.html">{t("Le tappe", "The steps")} {I["freccia"]}</a></li>
      <li>{VANTAGGI_ICO["mobile"]}<h3>{t("Officina mobile", "Mobile workshop")}</h3><p>{t("Forature, cambio ruote, diagnosi e avviamento: quando si può, intervengo sul posto.", "Punctures, wheel changes, diagnostics and starting problems: when possible, I fix it on the spot.")}</p><a class="link" href="officina-mobile.html">{t("Cosa faccio sul posto", "What I do on site")} {I["freccia"]}</a></li>
      <li>{VANTAGGI_ICO["aziende"]}<h3>{t("Imprese", "Businesses")}</h3><p>{t("Consulenza alle imprese che lavorano nel settore automobilistico.", "Consulting for businesses working in the automotive sector.")}</p><a class="link" href="officina.html#aziende">{t("Parliamone", "Let's talk")} {I["freccia"]}</a></li>
    </ul>
    <p class="vantaggi-zona">{t("Ritiro, riconsegna e officina mobile a Casale Monferrato e nei paesi vicini. Paghi alla riconsegna, in contanti, con carta o bancomat.", "Pick-up, delivery and mobile workshop in Casale Monferrato and nearby villages. You pay on delivery, in cash or by card.")}</p>
  </div>
</section>

<section class="recensioni" aria-labelledby="rec-t">
  <div class="wrap">
    <h2 id="rec-t">{t("Chi si è già affidato a Luca", "What customers say")}</h2>
    {"" if LINGUA == "it" else '<p class="lead recensioni-nota">Original reviews in Italian, from Google.</p>'}
    <div class="voci">{recensioni}</div>
    <a class="link" href="{MAPS}" target="_blank" rel="noopener">{t("Tutte le recensioni su Google", "All reviews on Google")} {I["esterno"]}</a>
  </div>
</section>

<section class="contatti-home" id="contatti" aria-labelledby="contatti-t">
  <div class="wrap contatti-home-griglia">
    <div>
      <h2 id="contatti-t">{t("Dove e quando", "Where and when")}</h2>
      <p class="contatti-luogo">{t("Officina a Frassineto Po (AL)", "Workshop in Frassineto Po (AL), Italy")}</p>
      {orari()}
      <p class="stato" data-stato></p>
      <a class="link" href="{MAPS}" target="_blank" rel="noopener">{t("Apri in Google Maps", "Open in Google Maps")} {I["esterno"]}</a>
    </div>
    <div class="contatti-diretti">
      <a class="numerone" href="tel:{TEL}">{tel_txt()}</a>
      <p>{t("Chiamami o scrivimi: ti dico quando posso ritirare il mezzo o quando puoi portarmelo.", "Call or message me: I'll tell you when I can collect the vehicle or when you can bring it in. WhatsApp is the easiest way to reach me if you don't speak Italian.")}</p>
      <div class="azioni">
        <a class="btn btn--arancio" href="{wa()}" target="_blank" rel="noopener">{I["chat"]}{t("Scrivi su WhatsApp", "Message on WhatsApp")}</a>
        <a class="btn btn--vuoto" href="mailto:{EMAIL}">{I["mail"]}Email</a>
      </div>
    </div>
  </div>
</section>
''' + piede("index.html"))


# ================================================================== SERVIZI
def pagina_servizi():
    sezioni_dati = [
        ("meccanica", ("Manutenzione ordinaria e straordinaria su veicoli di tutte le marche. Prima ti dico cosa serve e quanto costa, poi inizio.",
                       "Routine and extraordinary maintenance on vehicles of all makes. First I tell you what's needed and what it costs, then I start."),
         [("Tagliandi e manutenzione programmata", "Servicing and scheduled maintenance"), ("Riparazioni meccaniche, anche sul ponte", "Mechanical repairs, including on the lift"),
          ("Preventivo gratuito dopo la diagnosi", "Free quote after diagnosis")], ""),
        ("elettrauto", ("Trovo e riparo ogni genere di difetto elettrico, e mi occupo anche del climatizzatore.",
                        "I find and fix every kind of electrical fault, and I also look after air conditioning."),
         [("Problemi di avviamento e di ricarica", "Starting and charging problems"), ("Impianto luci, accessori e cablaggi", "Lights, accessories and wiring"),
          ("Controllo e ricarica del climatizzatore", "Air conditioning check and recharge"),
          ("Formazione sul recupero dei gas fluorurati (Reg. CE 307/2008)", "Trained in F-gas recovery (Reg. EC 307/2008)")], ""),
        ("gommista", ("Il cambio dei pneumatici sul cerchio si fa in officina. Le forature e il cambio delle ruote già montate li faccio anche da te.",
                      "Tyres are changed on the rim in the workshop. Punctures and swapping wheels that are already mounted can also be done at your place."),
         [("Sostituzione, equilibratura, convergenza e campanatura", "Fitting, balancing, alignment and camber"), ("Riparazione delle forature", "Puncture repair"),
          ("Cambio stagionale delle ruote montate", "Seasonal swap of mounted wheels"), ("Vendita di pneumatici e ricambi", "Tyre and parts sales")],
         f'<a class="link" href="gomme-ricambi.html">{t("Cerca le gomme per misura", "Find tyres by size")} {I["freccia"]}</a>'),
        ("carrozzeria", ("Lavori di carrozzeria, verniciatura, saldatura e sistemazioni varie. Chiedi un preventivo gratuito e confronta i prezzi.",
                         "Bodywork, painting, welding and general repairs. Ask for a free quote and compare prices."),
         [("Carrozzeria e sistemazioni varie", "Bodywork and general repairs"), ("Verniciatura", "Painting"), ("Saldatura", "Welding")], ""),
        ("diagnosi", ("Una spia accesa si legge subito, prima di decidere cosa fare. E prima della revisione ti controllo il mezzo gratis.",
                      "A warning light can be read straight away, before deciding what to do. And before the roadworthiness test I check your vehicle for free."),
         [("Lettura degli errori e delle spie", "Reading fault codes and warning lights"),
          ("Programmazione delle centraline, con software aggiornato ogni giorno", "ECU programming, with software updated daily"),
          ("Controllo gratuito prima della revisione e prenotazione", "Free check before the test, and booking"),
          ("Abilitato come responsabile tecnico delle revisioni", "Qualified technical manager for vehicle inspections")], ""),
        ("soccorso", ("Se sei rimasto fermo, dimmi dove sei. Quando si può intervengo sul posto con l'officina mobile; se serve il ponte, ritiro il mezzo e ti lascio una vettura di cortesia.",
                      "If you've broken down, tell me where you are. When possible I fix it on the spot with the mobile workshop; if it needs the lift, I collect the vehicle and leave you a courtesy car."),
         [("Riparazione delle forature", "Puncture repair"), ("Cambio delle ruote già montate", "Changing wheels already mounted"),
          ("Diagnosi e lettura delle spie", "Diagnostics and warning lights"), ("Avviamento e problemi elettrici, nei casi semplici", "Starting and electrical problems, in simple cases")],
         f'<a class="link" href="officina-mobile.html">{t("L’officina mobile", "The mobile workshop")} {I["freccia"]}</a>'),
    ]
    nomi = {s[0]: s[1] for s in SERVIZI}
    indice = "".join(f'<li><a href="#{chi}">{ICONE[chi]}<span>{tt(nomi[chi])}</span></a></li>' for chi, _, _, _ in sezioni_dati)
    indice += f'<li><a href="#aziende">{ICONE["aziende"]}<span>{t("Imprese", "Businesses")}</span></a></li>'
    sezioni = "".join(f'''
    <article class="sezione-servizio" id="{chi}" aria-labelledby="t-{chi}">
      <div class="sezione-servizio-ico">{ICONE[chi]}</div>
      <div class="sezione-servizio-testo">
        <h2 id="t-{chi}">{tt(nomi[chi])}</h2>
        <p class="lead">{tt(testo)}</p>
        {spunte(voci)}
        <div class="azioni">{apri_servizio(chi, t("Scrivi a Luca", "Message Luca"))}{extra}</div>
      </div>
    </article>''' for chi, testo, voci, extra in sezioni_dati)
    sezioni += f'''
    <article class="sezione-servizio" id="aziende" aria-labelledby="t-aziende">
      <div class="sezione-servizio-ico">{ICONE["aziende"]}</div>
      <div class="sezione-servizio-testo">
        <h2 id="t-aziende">{t("Consulenza alle imprese", "Business consulting")}</h2>
        <p class="lead">{t("Consulenza per le imprese che lavorano nel settore automobilistico. Ne parliamo e capiamo insieme di cosa hai bisogno.", "Consulting for businesses working in the automotive sector. Let's talk and work out together what you need.")}</p>
        {spunte([("Un tecnico con più di dieci anni di esperienza multimarca", "A technician with over ten years of multi-brand experience"), ("Un confronto su misura per la tua attività", "Advice tailored to your business")])}
        <div class="azioni">{apri("aziende", t("Scrivi a Luca", "Message Luca"))}</div>
      </div>
    </article>'''
    scrivi("officina.html", head("officina.html", t("Servizi: meccanica, elettrauto, gomme | L.M. Autoservizi", "Services: mechanics, auto electrics, tyres | L.M. Autoservizi"),
           t("Meccanica, elettrauto e clima, gommista, carrozzeria, diagnosi e pre-revisione, soccorso con l'officina mobile e consulenza alle imprese, a Frassineto Po.",
             "Mechanics, auto electrics and A/C, tyres, bodywork, diagnostics and pre-inspection, roadside help with the mobile workshop and business consulting in Frassineto Po."),
           [azienda(), briciole("officina.html", t("Servizi", "Services"))]) + testata("officina.html")
           + intro(t("Servizi", "Services"), t("Tutto quello che serve al tuo mezzo, su veicoli di tutte le marche. Il preventivo è gratuito e arriva prima di iniziare.",
                                               "Everything your vehicle needs, on all makes. The quote is free and comes before any work starts.")) + f'''
<div class="wrap fascia">{foto("officina", "(max-width: 1280px) 100vw, 1280px", "foto foto--fascia")}</div>
<section class="sezione">
  <div class="wrap servizi-documento">
    <nav class="indice" aria-label="{t("Servizi in questa pagina", "Services on this page")}"><ul>{indice}</ul></nav>
    <div class="servizi-sezioni">{sezioni}
    </div>
  </div>
</section>''' + finale() + piede("officina.html"))


# ================================================================== RITIRO E CONSEGNA
FAQ_EN = [("How much does pick-up cost?", "Tell me where the vehicle is: I'll tell you straight away whether there's a charge and how much, before I set off."),
          ("How far do you go?", "I collect and deliver in Casale Monferrato and nearby villages. Call to check whether I can reach you."),
          ("How much is the courtesy car?", "Nothing: it's always free. I leave it fuelled, clean and sanitised, for as long as you need it."),
          ("What if the repair takes several days?", "The courtesy car stays with you for the whole repair. I keep you updated on progress."),
          ("How do I pay?", "In cash or by card, on delivery.")]


def pagina_ritiro():
    tappe_dati = [(("Mi chiami o mi scrivi", "You call or message me"), ("Mi dici dov'è il mezzo e cosa non va. Nessun giro di telefonate.", "Tell me where the vehicle is and what's wrong. No endless phone calls.")),
                  (("Passo a ritirarlo", "I collect it"), ("Vengo a casa o al lavoro e ti lascio una vettura di cortesia gratuita.", "I come to your home or workplace and leave you a free courtesy car.")),
                  (("Diagnosi e preventivo", "Diagnosis and quote"), ("Controllo il mezzo in officina e ti dico cosa serve e quanto costa, prima di iniziare.", "I check the vehicle in the workshop and tell you what's needed and what it costs, before starting.")),
                  (("Lo riparo", "I repair it"), ("Nella mia officina a Frassineto Po, con il ponte e le attrezzature giuste.", "In my workshop in Frassineto Po, with the lift and the right equipment.")),
                  (("Te lo riporto", "I bring it back"), ("Riparato, pulito e igienizzato, dove vuoi. Paghi alla riconsegna.", "Repaired, clean and sanitised, wherever you like. You pay on delivery."))]
    tappe = "".join(f'<li class="tappa"><span class="tappa-n">{i + 1}</span><div><h3>{tt(titolo)}</h3><p>{tt(testo)}</p></div></li>' for i, (titolo, testo) in enumerate(tappe_dati))
    domande = FAQ_EN if LINGUA == "en" else [(d, r.replace("dove si trova l'auto", "dove si trova il mezzo")) for d, r in FAQ_R]
    faq = "".join(f'<details><summary>{d}</summary><div class="faq-risposta"><p>{r}</p></div></details>' for d, r in domande)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": d, "acceptedAnswer": {"@type": "Answer", "text": r}} for d, r in domande]}
    scrivi("ritiro-consegna.html", head("ritiro-consegna.html", t("Ritiro e consegna con vettura di cortesia | L.M. Autoservizi", "Pick-up and delivery with courtesy car | L.M. Autoservizi"),
           t("Ritiro il mezzo a casa o al lavoro, lo riparo nella mia officina a Frassineto Po e te lo riporto. Vettura di cortesia gratuita per tutta la riparazione.",
             "I collect your vehicle from home or work, repair it in my workshop in Frassineto Po and bring it back. Free courtesy car for the whole repair."),
           [azienda(), faq_schema, briciole("ritiro-consegna.html", t("Ritiro e consegna", "Pick-up and delivery"))], immagine="ritiro") + testata("ritiro-consegna.html")
           + intro(t("Ritiro e consegna", "Pick-up and delivery"), t("Tu lavori, io mi occupo del mezzo: lo ritiro, lo riparo e te lo riporto. Nel frattempo hai una vettura di cortesia gratuita.",
                                                                     "You get on with your day, I take care of the vehicle: I collect it, repair it and bring it back. In the meantime you have a free courtesy car.")) + f'''
<section class="sezione">
  <div class="wrap ritiro-griglia">
    <div>
      <h2>{t("Come funziona", "How it works")}</h2>
      <ol class="percorso" data-percorso><span class="percorso-linea" aria-hidden="true"><span></span></span>{tappe}</ol>
    </div>
    {foto("ritiro", "(max-width: 899px) 100vw, 40vw", "foto ritiro-foto")}
  </div>
</section>
<section class="sezione sezione--asfalto" id="domande">
  <div class="wrap ritiro-dettagli">
    <div><h2>{t("Domande frequenti", "Frequently asked questions")}</h2><div class="faq">{faq}</div></div>
    <div class="riquadro">
      <h2>{t("Chiedi il ritiro", "Request a pick-up")}</h2>
      <p>{t("Dimmi dove si trova il mezzo e cosa non va: il resto lo sistemiamo su WhatsApp.", "Tell me where the vehicle is and what's wrong: we'll sort out the rest on WhatsApp.")}</p>
      {apri("ritiro", t("Chiedi il ritiro", "Request a pick-up"))}
      <a class="link" href="tel:{TEL}">{I["tel"]}{t("Oppure chiama", "Or call")} {tel_txt()}</a>
    </div>
  </div>
</section>''' + piede("ritiro-consegna.html"))


# ================================================================== OFFICINA MOBILE
def pagina_mobile():
    scrivi("officina-mobile.html", head("officina-mobile.html", t("Officina mobile e soccorso | L.M. Autoservizi", "Mobile workshop and roadside help | L.M. Autoservizi"),
           t("Forature, cambio delle ruote montate, diagnosi e avviamento direttamente dove si trova il mezzo, a Casale Monferrato e nei paesi vicini.",
             "Punctures, changing mounted wheels, diagnostics and starting problems fixed where your vehicle is, in Casale Monferrato and nearby villages."),
           [azienda(), briciole("officina-mobile.html", t("Officina mobile", "Mobile workshop"))], immagine="officina-mobile") + testata("officina-mobile.html")
           + intro(t("Officina mobile", "Mobile workshop"), t("Per i lavori che si possono fare sul posto arrivo io, con il furgone attrezzato. Il resto lo facciamo in officina.",
                                                             "For jobs that can be done on site, I come to you with my equipped van. Everything else we do in the workshop.")) + f'''
<section class="sezione">
  <div class="wrap mobile-griglia">
    <div class="mobile-presentazione">
      <h2>{t("L'officina arriva da te.", "The workshop comes to you.")}</h2>
      <p class="lead">{t("Un intervento sul posto, quando si può. Il ritiro in officina, quando serve.", "A repair on the spot when possible. Collection to the workshop when needed.")}</p>
      {foto("officina-mobile", "(max-width: 899px) 100vw, 50vw", "foto mobile-foto")}
    </div>
    <div class="mobile-dettagli">
      <h2>{t("Cosa faccio sul posto", "What I do on site")}</h2>
      {spunte([("Riparazione delle forature", "Puncture repair"), ("Cambio delle ruote già montate sui cerchi", "Changing wheels already mounted on rims"),
               ("Diagnosi elettronica e lettura delle spie", "Electronic diagnostics and warning lights"), ("Problemi elettrici e di avviamento, nei casi semplici", "Electrical and starting problems, in simple cases")])}
      <h2>{t("E quando serve l'officina", "When the workshop is needed")}</h2>
      <p>{t("Se il lavoro richiede il ponte o tempi lunghi, ritiro il mezzo e ti lascio una vettura di cortesia gratuita. Il preventivo è sempre gratuito e arriva prima di iniziare.",
              "If the job needs the lift or more time, I collect the vehicle and leave you a free courtesy car. The quote is always free and comes before any work starts.")}</p>
      <div class="azioni">{apri_servizio("soccorso", t("Sono fermo: scrivi a Luca", "I've broken down: message Luca"))}<a class="btn btn--vuoto" href="tel:{TEL}">{I["tel"]}{t("Chiama", "Call")} {tel_txt()}</a></div>
      <p class="piccolo">{t("Lavoro a Casale Monferrato e nei paesi vicini. Chiama per sapere se arrivo anche da te.", "I work in Casale Monferrato and nearby villages. Call to check whether I can reach you.")}</p>
    </div>
  </div>
</section>''' + finale() + piede("officina-mobile.html"))


# ================================================================== GOMME E RICAMBI
TARGA_UE = ('<span class="targa-ue" aria-hidden="true"><svg viewBox="0 0 44 64" width="44" height="64">'
            + "".join(f'<circle cx="{22 + 11 * math.cos(math.radians(a * 30)):.1f}" cy="{19 + 11 * math.sin(math.radians(a * 30)):.1f}" r="1.35" fill="#f2c230"/>' for a in range(12))
            + '<text x="22" y="53" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-weight="700" font-size="17" fill="#fff">I</text></svg></span>')


def pagina_gomme():
    scrivi("gomme-ricambi.html", head("gomme-ricambi.html", t("Gomme e ricambi a Frassineto Po | L.M. Autoservizi", "Tyres and parts in Frassineto Po | L.M. Autoservizi"),
           t("Vendita di pneumatici e ricambi, con montaggio, equilibratura e convergenza in officina. Scrivi la misura e ti rispondo con disponibilità e prezzo.",
             "Tyre and parts sales with fitting, balancing and alignment in the workshop. Enter the size and I'll reply with availability and price."),
           [azienda(), briciole("gomme-ricambi.html", t("Gomme e ricambi", "Tyres and parts"))], immagine="servizio-gommista") + testata("gomme-ricambi.html")
           + intro(t("Gomme e ricambi", "Tyres and parts"), t("Dimmi la misura o la targa: ti rispondo con disponibilità e prezzo. Al montaggio penso io.",
                                                             "Tell me the size or the number plate: I'll reply with availability and price. I'll take care of fitting.")) + f'''
<section class="sezione">
  <div class="wrap gomme-griglia">
    <div>
      <h2 id="gomme-t">{t("Vendita pneumatici", "Tyre sales")}</h2>
      <p class="lead">{t("Estive, invernali e quattro stagioni. La misura è scritta sul fianco, per esempio 205/55 R16: se non la trovi, dimmi la targa e la ricavo io.",
                         "Summer, winter and all-season. The size is written on the sidewall, for example 205/55 R16: if you can't find it, tell me the number plate and I'll work it out.")}</p>
      <form class="modulo" data-wa data-intro="{attr(t("Ciao Luca, vorrei un preventivo per delle gomme.", "Hi Luca, I'd like a quote for tyres (preventivo gomme)."))}" novalidate aria-labelledby="gomme-t">
        <fieldset class="campo">
          <legend>{t("Misura della gomma", "Tyre size")}</legend>
          <div class="misura">
            <label><span class="sr">{t("Larghezza", "Width")}</span><input name="larghezza" inputmode="numeric" maxlength="3" placeholder="205" required autocomplete="off"></label><i aria-hidden="true">/</i>
            <label><span class="sr">{t("Spalla", "Profile")}</span><input name="spalla" inputmode="numeric" maxlength="2" placeholder="55" required autocomplete="off"></label><i aria-hidden="true">R</i>
            <label><span class="sr">{t("Cerchio in pollici", "Rim size in inches")}</span><input name="cerchio" inputmode="numeric" maxlength="2" placeholder="16" required autocomplete="off"></label>
          </div>
          <p class="errore" aria-live="polite"></p>
        </fieldset>
        <div class="campi-due">
          <div class="campo"><label for="g-stagione">{t("Che gomme cerchi", "Which tyres")}</label><select id="g-stagione" name="stagione" data-etichetta="{t("Stagione", "Season (stagione)")}"><option>{t("Estive", "Summer")}</option><option>{t("Invernali", "Winter")}</option><option>{t("Quattro stagioni", "All-season")}</option><option>{t("Non lo so, consigliami tu", "Not sure, please advise")}</option></select></div>
          <div class="campo"><label for="g-mezzo">{t("Mezzo", "Vehicle")} <span>({t("facoltativo", "optional")})</span></label><input id="g-mezzo" name="mezzo" data-etichetta="{t("Mezzo", "Vehicle (mezzo)")}" placeholder="{t("Es.", "E.g.")} Fiat Panda 2015"></div>
        </div>
        <button class="btn btn--arancio btn--pieno" type="submit">{I["chat"]}{t("Chiedi disponibilità su WhatsApp", "Ask for availability on WhatsApp")}</button>
        <p class="nota">{t("Ti rispondo con disponibilità e prezzo. Il montaggio si fa in officina.", "I'll reply with availability and price. Fitting is done in the workshop.")}</p>
        <p class="esito" role="status" hidden></p>
      </form>
      {spunte([("Montaggio ed equilibratura in officina", "Fitting and balancing in the workshop"), ("Convergenza e campanatura", "Alignment and camber"), ("Riparazione delle forature, anche da te", "Puncture repair, also at your place")])}
    </div>
    <figure class="gomma">
      <div class="gomma-foto"><img src="{A}assets/img/3d/pneumatico-realista-v1.webp" width="1254" height="1254" alt="{t("Render illustrativo di un pneumatico con cerchio in lega", "Illustrative render of a tyre with an alloy rim")}" loading="lazy" decoding="async"></div>
      <figcaption class="gomma-dati"><div><span data-misura-etichetta>{t("Esempio di misura", "Example size")}</span><strong data-misura-testo>205/55 R16</strong></div><p>{t("Immagine illustrativa", "Illustrative image")}</p></figcaption>
    </figure>
  </div>
</section>
<section class="sezione sezione--asfalto">
  <div class="wrap gomme-griglia">
    <div>
      <h2>{t("Vendita ricambi", "Parts sales")}</h2>
      <p class="lead">{t("Ricambi per veicoli di tutte le marche. Dimmi la targa e il pezzo che ti serve: ti rispondo con disponibilità e preventivo, e se vuoi lo monto io.",
                         "Parts for vehicles of all makes. Tell me the number plate and the part you need: I'll reply with availability and a quote, and I can fit it if you like.")}</p>
      {spunte([("Ricambi per tutte le marche", "Parts for all makes"), ("Preventivo gratuito", "Free quote"), ("Montaggio in officina", "Fitting in the workshop")])}
    </div>
    <form class="modulo modulo--riquadro" data-wa data-intro="{attr(t("Ciao Luca, vorrei un preventivo per un ricambio.", "Hi Luca, I'd like a quote for a part (preventivo ricambio)."))}" novalidate aria-labelledby="rc-t">
      <h2 id="rc-t">{t("Chiedi un ricambio", "Ask for a part")}</h2>
      <div class="campo"><label for="rc-targa">{t("Targa", "Number plate")} <span>({t("facoltativa", "optional")})</span></label>
        <div class="targa">{TARGA_UE}<input id="rc-targa" name="targa" class="targa-campo" data-etichetta="{t("Targa", "Plate (targa)")}" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="8" placeholder="AB123CD"></div>
        <p class="aiuto">{t("Serve solo a trovare il pezzo giusto.", "Only used to find the right part.")}</p></div>
      <div class="campo"><label for="rc-pezzo">{t("Che pezzo ti serve", "Which part do you need")}</label><input id="rc-pezzo" name="pezzo" data-etichetta="{t("Pezzo", "Part (pezzo)")}" required placeholder="{t("Es. pastiglie dei freni anteriori", "E.g. front brake pads")}"><p class="errore" aria-live="polite"></p></div>
      <div class="campo"><label for="rc-mezzo">{t("Mezzo", "Vehicle")} <span>({t("facoltativo", "optional")})</span></label><input id="rc-mezzo" name="mezzo" data-etichetta="{t("Mezzo", "Vehicle (mezzo)")}" placeholder="{t("Es.", "E.g.")} Piaggio Liberty 50"></div>
      <button class="btn btn--arancio btn--pieno" type="submit">{I["chat"]}{t("Chiedi su WhatsApp", "Ask on WhatsApp")}</button>
      <p class="nota">{t("Si apre WhatsApp con il messaggio già scritto. L'invio lo confermi tu.", "WhatsApp opens with the message already written. You confirm the sending.")}</p>
      <p class="esito" role="status" hidden></p>
    </form>
  </div>
</section>''' + finale(t("Non sai cosa ti serve?", "Not sure what you need?"), t("Descrivimi il problema: ti dico io cosa serve.", "Describe the problem: I'll tell you what's needed.")) + piede("gomme-ricambi.html"))


# ================================================================== CHI SONO
ATT_EN = {"qualifica-professionale": ("Vehicle electromechanical repair technician", "Professional qualification, 400 hours, 2010"),
          "responsabile-revisioni": ("Technical manager for periodic vehicle inspections", "Certificate of competence"),
          "gas-fluorurati": ("F-gas recovery in vehicles", "Car air conditioning, Reg. EC 307/2008, 2012"),
          "diploma": ("Scientific-technological high school diploma", "IIS A. Sobrero, Casale Monferrato, 2009"),
          "sicurezza-generale": ("Workplace safety: general and specific training", "Legislative Decree 81/2008, 8 hours"),
          "sicurezza-specifica": ("Workplace safety: specific training", "Legislative Decree 81/2008, 4 hours"),
          "inglese": ("English language, level 2", "Certificate of attendance and achievement, 2011"),
          "gran-turismo": ("Grand touring car driving", "Puresport")}


def pagina_chi():
    voci_att = [(f, *(ATT_EN[f] if LINGUA == "en" else (titolo, sotto))) for f, titolo, sotto in ATT]
    attestati = "".join(f'''<li><button type="button" data-lightbox="{A}assets/img/attestati/{f}.webp" data-titolo="{attr(titolo)}"><img src="{A}assets/img/attestati/{f}-thumb.webp" alt="" loading="lazy" decoding="async" width="340" height="480"><span>{titolo}<small>{sotto}</small></span></button></li>''' for f, titolo, sotto in voci_att)
    lightbox = f'''<dialog class="lightbox" id="lightbox" aria-labelledby="lightbox-t" data-lenis-prevent>
  <figure><figcaption id="lightbox-t"></figcaption></figure>
  <button class="lightbox-chiudi" type="button" aria-label="{t("Chiudi", "Close")}" data-chiudi>{I["chiudi"]}</button>
</dialog>
'''
    cronologia = [("2009", ("Diploma di liceo scientifico tecnologico a Casale Monferrato.", "Scientific-technological high school diploma in Casale Monferrato.")),
                  ("2010", ("Qualifica di operatore di riparazioni elettromeccaniche per l'autoveicolo.", "Qualification as vehicle electromechanical repair technician.")),
                  ("2012", ("Formazione per il recupero dei gas fluorurati degli impianti di climatizzazione.", "Training in F-gas recovery from air-conditioning systems.")),
                  (("Oggi", "Today"), ("Titolare di L.M. Autoservizi, con officina a Frassineto Po, ritiro e consegna e officina mobile.", "Owner of L.M. Autoservizi, with a workshop in Frassineto Po, pick-up and delivery, and a mobile workshop."))]
    crono = "".join(f'<li><b>{tt(anno)}</b><span>{tt(testo)}</span></li>' for anno, testo in cronologia)
    scrivi("chi-sono.html", head("chi-sono.html", t("Chi sono: Luca Miglietta | L.M. Autoservizi", "About me: Luca Miglietta | L.M. Autoservizi"),
           t("Luca Miglietta, titolare di L.M. Autoservizi: qualifica in riparazioni elettromeccaniche, responsabile tecnico delle revisioni, oltre dieci anni multimarca.",
             "Luca Miglietta, owner of L.M. Autoservizi: qualified in vehicle electromechanical repairs, technical manager for inspections, over ten years on all makes."),
           [azienda(), briciole("chi-sono.html", t("Chi sono", "About me"))], immagine="luca") + testata("chi-sono.html")
           + intro(t("Chi sono", "About me"), t("Mi chiamo Luca Miglietta. Lavoro da solo: il mezzo che mi affidi lo segue una persona sola, dall'inizio alla fine.",
                                                "My name is Luca Miglietta. I work alone: the vehicle you leave with me is looked after by one person, from start to finish.")) + f'''
<section class="sezione">
  <div class="wrap chi-griglia">
    {foto("luca", "(max-width: 899px) 100vw, 45vw", "foto chi-foto")}
    <div>
      <dl class="tessera">
        <div><dt>{t("Titolare", "Owner")}</dt><dd>Luca Miglietta</dd></div>
        <div><dt>{t("Officina", "Workshop")}</dt><dd>Frassineto Po (AL)</dd></div>
        <div><dt>{t("Esperienza", "Experience")}</dt><dd>{t("Più di dieci anni, multimarca", "Over ten years, all makes")}</dd></div>
        <div><dt>{t("Abilitazione", "Qualification")}</dt><dd>{t("Responsabile tecnico delle revisioni", "Technical manager for vehicle inspections")}</dd></div>
      </dl>
      <h2>{t("Il mio percorso", "My background")}</h2>
      <ol class="cronologia" data-cronologia>{crono}</ol>
    </div>
  </div>
</section>
<section class="sezione sezione--asfalto">
  <div class="wrap">
    <h2>{t("Attestati", "Certificates")}</h2>
    <p class="piccolo">{t("Tocca un attestato per vederlo a grandezza piena.", "Tap a certificate to see it full size.")}</p>
    <ul class="attestati">{attestati}</ul>
  </div>
</section>''' + finale() + piede("chi-sono.html", lightbox))


# ================================================================== CONTATTI
def pagina_contatti():
    scrivi("contatti.html", head("contatti.html", t("Contatti | L.M. Autoservizi, Frassineto Po", "Contact | L.M. Autoservizi, Frassineto Po"),
           t("Chiama il 342 643 6085 o scrivi su WhatsApp. Officina a Frassineto Po, aperta dal lunedì al venerdì dalle 7:30 alle 19:30, orario continuato.",
             "Call +39 342 643 6085 or message on WhatsApp. Workshop in Frassineto Po, open Monday to Friday from 7:30 to 19:30, no lunch break."),
           [azienda(), briciole("contatti.html", t("Contatti", "Contact"))], immagine="ingresso") + testata("contatti.html")
           + intro(t("Contatti", "Contact"), t("Chiamami o scrivimi su WhatsApp: ti rispondo io.", "Call me or message me on WhatsApp: I'll answer personally.")) + f'''
<section class="sezione">
  <div class="wrap contatti-griglia">
    <div class="contatti-diretti">
      <a class="numerone" href="tel:{TEL}">{tel_txt()}</a>
      <p>{t("Al telefono e su WhatsApp rispondo io, dal lunedì al venerdì.", "I answer the phone and WhatsApp myself, Monday to Friday. WhatsApp is the easiest way to reach me if you don't speak Italian.")}</p>
      <div class="azioni">
        <a class="btn btn--arancio" href="{wa()}" target="_blank" rel="noopener">{I["chat"]}{t("Scrivi su WhatsApp", "Message on WhatsApp")}</a>
        <a class="btn btn--vuoto" href="mailto:{EMAIL}">{I["mail"]}Email</a>
      </div>
      <dl class="recapiti">
        <div><dt>{t("Telefono", "Phone")}</dt><dd><a href="tel:{TEL}">{tel_txt()}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>{t("PEC", "Certified email (PEC)")}</dt><dd><a href="mailto:{PEC}">{PEC}</a></dd></div>
        <div><dt>{t("Officina", "Workshop")}</dt><dd>Frassineto Po (AL)</dd></div>
        <div><dt>{t("Sede legale", "Registered office")}</dt><dd>{SEDE_LEGALE}</dd></div>
        <div><dt>{t("Partita IVA", "VAT number")}</dt><dd>{PIVA}</dd></div>
      </dl>
    </div>
    <div class="contatti-orari">
      <h2>{t("Orari", "Opening hours")}</h2>
      {orari()}
      <p class="stato" data-stato></p>
      <a class="link" href="{MAPS}" target="_blank" rel="noopener">{t("Apri in Google Maps", "Open in Google Maps")} {I["esterno"]}</a>
      {foto("ingresso", "(max-width: 899px) 100vw, 45vw", "foto contatti-foto")}
      <p class="piccolo">{t("Prima di passare chiamami: concordiamo l'intervento e ti do le indicazioni per arrivare.", "Before coming, give me a call: we'll agree on the job and I'll give you directions.")}</p>
    </div>
  </div>
</section>
<section class="sezione sezione--asfalto" aria-labelledby="scegli-t">
  <div class="wrap">
    <h2 id="scegli-t">{t("Oppure scegli il servizio", "Or choose the service")}</h2>
    <p class="lead">{t("Scegli il mezzo, scrivi due righe e il messaggio parte già pronto su WhatsApp.", "Choose your vehicle, write a couple of lines and the message is ready on WhatsApp.")}</p>
    {griglia_servizi(False)}
  </div>
</section>''' + piede("contatti.html"))


# ================================================================== PRIVACY E 404
def pagina_privacy():
    if LINGUA == "it":
        corpo = f'''<h2>Titolare del trattamento</h2>
    <p>L.M. Autoservizi di Miglietta Luca, {SEDE_LEGALE}, P.IVA {PIVA}. Email <a href="mailto:{EMAIL}">{EMAIL}</a>, PEC <a href="mailto:{PEC}">{PEC}</a>.</p>
    <h2>Quali dati e perché</h2>
    <p>Il sito non raccoglie dati in automatico. Quando scegli un servizio, chiedi delle gomme o un ricambio, la pagina prepara un messaggio che invii tu tramite WhatsApp: i dati che scrivi (tipo di mezzo, targa, misura, descrizione del problema) arrivano solo al titolare e servono a risponderti e a preparare il preventivo.</p>
    <p>La base giuridica è la tua richiesta (misure precontrattuali, art. 6.1.b GDPR). I dati sono conservati per il tempo necessario a gestire la richiesta e gli eventuali obblighi fiscali successivi.</p>
    <h2>Servizi di terze parti</h2>
    <ul>
      <li><strong>WhatsApp</strong> (Meta) ed email: se scegli questi canali, il messaggio viene trattato anche secondo le loro condizioni.</li>
      <li><strong>Google Maps</strong>: i collegamenti alla mappa e alle recensioni aprono il servizio esterno. Nessuna mappa viene caricata nel sito.</li>
    </ul>
    <h2>Cookie</h2>
    <p>Questo sito non usa cookie di profilazione né strumenti di statistica. Per questo non mostra un banner per i cookie.</p>
    <p>Se scegli il tema chiaro, il sito ricorda la scelta nella memoria del tuo browser. È un'impostazione tecnica che non esce dal tuo dispositivo.</p>
    <h2>I tuoi diritti</h2>
    <p>Puoi chiedere in qualsiasi momento di accedere ai tuoi dati, correggerli o cancellarli scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>'''
    else:
        corpo = f'''<h2>Data controller</h2>
    <p>L.M. Autoservizi di Miglietta Luca, {SEDE_LEGALE}, Italy, VAT no. {PIVA}. Email <a href="mailto:{EMAIL}">{EMAIL}</a>, certified email (PEC) <a href="mailto:{PEC}">{PEC}</a>.</p>
    <h2>What data and why</h2>
    <p>The website does not collect data automatically. When you choose a service or ask for tyres or a part, the page prepares a message that you send yourself via WhatsApp: the data you write (vehicle type, number plate, tyre size, description of the problem) reaches only the data controller and is used to reply to you and prepare the quote.</p>
    <p>The legal basis is your request (pre-contractual measures, Art. 6(1)(b) GDPR). Data is kept for as long as needed to handle the request and for any subsequent tax obligations.</p>
    <h2>Third-party services</h2>
    <ul>
      <li><strong>WhatsApp</strong> (Meta) and email: if you choose these channels, the message is also processed under their terms.</li>
      <li><strong>Google Maps</strong>: the links to the map and the reviews open the external service. No map is loaded on the website.</li>
    </ul>
    <h2>Cookies</h2>
    <p>This website does not use profiling cookies or analytics tools, so it doesn't show a cookie banner.</p>
    <p>If you choose the light theme, the website remembers your choice in your browser's storage. It's a technical setting that never leaves your device.</p>
    <h2>Your rights</h2>
    <p>You can ask at any time to access, correct or delete your data by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>. You can also lodge a complaint with the Italian Data Protection Authority (Garante per la protezione dei dati personali).</p>'''
    scrivi("privacy.html", head("privacy.html", t("Privacy e cookie | L.M. Autoservizi", "Privacy and cookies | L.M. Autoservizi"),
           t("Come vengono trattati i dati personali e quali cookie usa il sito di L.M. Autoservizi.", "How personal data is processed and which cookies the L.M. Autoservizi website uses.")) + testata("privacy.html")
           + intro(t("Privacy e cookie", "Privacy and cookies"), t("Come vengono trattati i tuoi dati quando usi questo sito.", "How your data is processed when you use this website.")) + f'''
<section class="sezione">
  <div class="wrap prosa">
    {corpo}
  </div>
</section>''' + piede("privacy.html"))


def pagina_404():
    scrivi("404.html", head("404.html", t("Pagina non trovata | L.M. Autoservizi", "Page not found | L.M. Autoservizi"),
           t("La pagina che cerchi non esiste: torna alla home di L.M. Autoservizi o chiama Luca.", "The page you're looking for doesn't exist: go back to the L.M. Autoservizi home page or call Luca."), noindex=True) + testata("404.html")
           + intro(t("Pagina non trovata", "Page not found"), t("Questa pagina non esiste. Torna alla home oppure chiamami: ti rimetto in carreggiata.", "This page doesn't exist. Go back to the home page or give me a call: I'll get you back on the road.")) + f'''
<section class="sezione"><div class="wrap"><div class="azioni"><a class="btn btn--arancio" href="./">{t("Torna alla home", "Back to the home page")} {I["freccia"]}</a><a class="btn btn--vuoto" href="tel:{TEL}">{I["tel"]}{tel_txt()}</a></div></div></section>''' + piede("404.html"))


# ================================================================== generazione
for LINGUA, R, A in (("it", "", "../"), ("en", "../", "../../")):
    for costruisci in (pagina_home, pagina_servizi, pagina_ritiro, pagina_mobile, pagina_gomme, pagina_chi, pagina_contatti, pagina_privacy, pagina_404):
        costruisci()

for nome in ("semplice.css", "semplice.js"):
    with open(os.path.join(QUI, nome), encoding="utf-8") as f:
        testo = f.read()
    with open(os.path.join(BASE, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
    print("copiato", "semplice/" + nome)
