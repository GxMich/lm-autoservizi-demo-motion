"""Prepara le foto vere per la versione semplice: python sorgente/foto.py
Legge gli scatti da materiali/foto/ (JPEG o PNG; HEIC solo se è installato pillow-heif). Ogni file deve avere
il nome di uno spazio di FOTO_SLOT in contenuti.py, per esempio eroe.jpg, luca.jpg, servizio-gommista.jpg.
Ritaglia al centro sul rapporto dello spazio e scrive docs/assets/img/foto/<spazio>.webp (1600 px di larghezza)
e <spazio>-800.webp. I metadati, posizione GPS compresa, non vengono copiati.
Dopo: python sorgente/genera_semplice.py (le foto vere sostituiscono da sole quelle stock).
Cartelle diverse: python sorgente/foto.py <originali> <destinazione>"""
import os, sys
from PIL import Image, ImageOps
from contenuti import FOTO_SLOT

try:  # facoltativo: apre direttamente i file HEIC dell'iPhone
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
ORIGINALI = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RADICE, "materiali", "foto")
DEST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RADICE, "docs", "assets", "img", "foto")
ESTENSIONI = (".jpg", ".jpeg", ".png", ".heic", ".heif")


def ritaglia(img, rw, rh):
    w, h = img.size
    rapporto = rw / rh
    if w / h > rapporto:
        nw = round(h * rapporto)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = round(w / rapporto)
    y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


os.makedirs(DEST, exist_ok=True)
for nome in sorted(os.listdir(ORIGINALI)):
    base, estensione = os.path.splitext(nome)
    if estensione.lower() not in ESTENSIONI:
        continue
    if base not in FOTO_SLOT:
        print("ignorata, il nome non corrisponde a nessuno spazio:", nome)
        continue
    rw, rh = FOTO_SLOT[base][0]
    try:
        with Image.open(os.path.join(ORIGINALI, nome)) as originale:
            img = ritaglia(ImageOps.exif_transpose(originale).convert("RGB"), rw, rh)
    except OSError as errore:
        print("non riesco ad aprire", nome, "-", errore, "(per i file HEIC: esportali in JPEG o installa pillow-heif)")
        continue
    if img.width < 1600:
        print(f"attenzione: {nome} dopo il ritaglio misura {img.width} px di larghezza, meno dei 1600 consigliati")
    for larghezza, suffisso in ((1600, ""), (800, "-800")):
        img.resize((larghezza, round(larghezza * rh / rw)), Image.LANCZOS).save(
            os.path.join(DEST, base + suffisso + ".webp"), "WEBP", quality=80, method=6)
    print("pronta", base)

mancanti = [s for s in FOTO_SLOT if not os.path.exists(os.path.join(DEST, s + ".webp"))]
print("ancora stock:", ", ".join(mancanti) if mancanti else "nessuna, tutte le foto sono vere")
