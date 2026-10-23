# L.M. Autoservizi — demo motion

Nuova demo indipendente con foto stock di esempio, animazioni scenografiche e sezioni home contenute entro l’altezza dello schermo. Non sostituisce la prima demo.

- Repository: https://github.com/GxMich/lm-autoservizi-demo-motion
- GitHub Pages: https://gxmich.github.io/lm-autoservizi-demo-motion/
- Vercel: https://lm-autoservizi-demo-motion.vercel.app/

## Sviluppo

Il sito statico pubblicabile si trova in `docs/`. I modelli sono in `sorgente/`.

```sh
python sorgente/genera_nuovo.py
python -m http.server 8080 --directory docs
```

Gli asset condivisi del modulo sono in `docs/assets/css/richiesta.css` e `docs/assets/js/richiesta.js`. Dopo una modifica ai modelli, rigenerare le pagine e includere `docs/` nel commit. GitHub Pages pubblica `main:/docs`; Vercel pubblica `docs/` senza build. L’indicizzazione resta disabilitata per questa demo.

## Versione semplice (`docs/semplice/`)

La versione chiesta dal cliente: presentazione con Luca, poi i servizi come caselle grandi. Ogni servizio apre una tendina con la scelta del mezzo (auto, fuoristrada, furgone, camper, ciclomotore), due righe di note e l'invio su WhatsApp. Ha anche le sue pagine interne (servizi, ritiro e consegna, officina mobile, gomme e ricambi, chi sono, contatti, privacy) e non tocca la demo alla radice.

- Due lingue: italiano in `docs/semplice/`, inglese in `docs/semplice/en/`, collegate da hreflang e dal pulsante IT/EN. I messaggi WhatsApp inviati dalle pagine inglesi riportano anche i nomi italiani del servizio e del mezzo.
- Tema scuro di base e tema chiaro dal pulsante in testata; la scelta resta nel browser (`localStorage`, chiave `lm-tema`).

```sh
python sorgente/genera_semplice.py
```

- Sorgenti: `sorgente/genera_semplice.py` (pagine e icone), `sorgente/semplice.css`, `sorgente/semplice.js`.
- Dati dell'attività in comune con la demo motion: `sorgente/contenuti.py`.
- Le pagine generate in `docs/semplice/` vanno incluse nel commit.
- Per la pubblicazione definitiva: `LM_PRODUZIONE=1` attiva canonical e indicizzazione. `LM_URL_PAGINE` e `LM_URL_RISORSE` danno gli indirizzi pubblici per canonical e anteprime social.

Foto vere: gli scatti vanno in `materiali/foto/` con i nomi indicati in `materiali/foto/LEGGIMI.md`, poi:

```sh
python sorgente/foto.py
python sorgente/genera_semplice.py
```

Ogni foto vera sostituisce da sola quella stock e toglie la scritta "Foto di esempio". Gli originali restano fuori dal repository.

Il PDF con i servizi del cliente resta in locale in `materiali/` ed è escluso dal repository.

## Immagini

Le fonti delle immagini stock sono in `docs/assets/img/campione/FONTI.json`. Il pneumatico è un render illustrativo. Le immagini campione sono dichiarate nel sito e non rappresentano fotografie dell’attività.

La prima demo resta nel repository https://github.com/GxMich/lm-autoservizi e all’indirizzo https://gxmich.github.io/lm-autoservizi/ . Questo progetto non usa quei target di pubblicazione.
