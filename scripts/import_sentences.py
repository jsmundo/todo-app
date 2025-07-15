import pandas as pd
from app import app, db               # Si usas factory, reemplaza: from app import create_app, db ; app = create_app()
from models import Sentence

CSV_PATH = "bilingual_eng_esp_100k.csv"   # ajusta si lo moviste

df = pd.read_csv(CSV_PATH)

with app.app_context():
    for _, row in df.iterrows():
        db.session.add(Sentence(
            text_en=row.text_eng,
            text_es=row.text_esp
        ))
    db.session.commit()
    print(f"✅ Importadas {len(df)} frases")













