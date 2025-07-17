import pandas as pd
from pathlib import Path

base = Path(".")
eng = pd.read_csv(base/"data/sentences_eng.csv",
                  names=["id", "lang", "text"], sep="\t")
esp = pd.read_csv(base/"data/sentences_esp.csv",
                  names=["id", "lang", "text"], sep="\t")
links = pd.read_csv(base/"data/backups/links.csv",
                    names=["id_eng", "id_esp"], sep="\t")

# 1) renombramos para que no choquen
eng  = eng.rename(columns={"id": "id_eng", "text": "text_eng"})
esp  = esp.rename(columns={"id": "id_esp", "text": "text_esp"})

pairs = (links
         .merge(eng[["id_eng", "text_eng"]], on="id_eng")
         .merge(esp[["id_esp", "text_esp"]], on="id_esp")
         .loc[:, ["text_eng", "text_esp"]]
         .drop_duplicates())

# opcional: filtrado de longitud
pairs = pairs[(pairs.text_eng.str.len() < 200) &
              (pairs.text_esp.str.len() < 200)]

pairs.to_csv("bilingual_eng_esp_100k.csv", index=False)
print("✅ Archivo generado")
