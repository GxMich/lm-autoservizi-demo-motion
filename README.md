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

Le fonti delle immagini stock sono in `docs/assets/img/campione/FONTI.json`. Il pneumatico è un render illustrativo. Le immagini campione sono dichiarate nel sito e non rappresentano fotografie dell’attività.

La prima demo resta nel repository https://github.com/GxMich/lm-autoservizi e all’indirizzo https://gxmich.github.io/lm-autoservizi/ . Questo progetto non usa quei target di pubblicazione.
