# Foto originali

Qui vanno gli scatti originali (JPEG o PNG; HEIC solo con `pip install pillow-heif`). Restano fuori dal repository.

Ogni file prende il nome dello spazio in cui finirà:

| File | Spazio | Formato |
|---|---|---|
| `eroe.jpg` | Apertura della home, dentro l'ingranaggio | verticale 2:3, soggetto al centro |
| `luca.jpg` | Ritratto di Luca (home e Chi sono) | verticale 4:5 |
| `officina.jpg` | Interno dell'officina (fascia della pagina Servizi, anteprima social) | orizzontale 3:2 |
| `ingresso.jpg` | Ingresso dell'officina (Contatti) | orizzontale 3:2 |
| `officina-mobile.jpg` | Furgone dell'officina mobile | orizzontale 3:2 |
| `ritiro.jpg` | Consegna delle chiavi / vettura di cortesia | orizzontale 3:2 |
| `servizio-meccanica.jpg` | Casella Meccanica | orizzontale 3:2 |
| `servizio-elettrauto.jpg` | Casella Elettrauto | orizzontale 3:2 |
| `servizio-gommista.jpg` | Casella Gommista | orizzontale 3:2 |
| `servizio-carrozzeria.jpg` | Casella Carrozzeria | orizzontale 3:2 |
| `servizio-diagnosi.jpg` | Casella Diagnosi e pre-revisione | orizzontale 3:2 |
| `servizio-soccorso.jpg` | Casella Soccorso | orizzontale 3:2 |

Poi, dalla radice del progetto:

```sh
python sorgente/foto.py
python sorgente/genera_semplice.py
```

Il primo comando ritaglia al centro sul formato giusto e crea le versioni WebP senza metadati. Il secondo rigenera le pagine: ogni foto vera prende il posto di quella stock e la scritta "Foto di esempio" sparisce.
