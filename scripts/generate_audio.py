import pathlib, subprocess
from app import app, db
from models import Sentence

VOICE      = "alexander"               
MAX_SAMPLES = 1_000                   # ⚑ solo las 1 000 primeras
OUT_DIR     = pathlib.Path("static/audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

with app.app_context():
    # frases sin audio, limitadas a MAX_SAMPLES
    qs = (Sentence.query
                     .filter(Sentence.audio_url == None)
                     .limit(MAX_SAMPLES)
                     .all())

    for s in qs:
        mp3_name = f"en_{s.id}.mp3"
        mp3_path = OUT_DIR / mp3_name

        if mp3_path.exists():         # por si relanzas
            s.audio_url = f"/static/audio/{mp3_name}"
            continue

        # 1) AIFF con `say`; 2) convertir a MP3 con ffmpeg
        aiff = mp3_path.with_suffix(".aiff")
        subprocess.run(["say", "-v", VOICE, "-o", str(aiff), s.text_en])
        subprocess.run(["ffmpeg", "-y", "-i", str(aiff), str(mp3_path)],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        aiff.unlink()                 # borra temporal
        s.audio_url = f"/static/audio/{mp3_name}"

    db.session.commit()
    print(f"✅ Generados {len(qs)} audios -> static/audio/")
