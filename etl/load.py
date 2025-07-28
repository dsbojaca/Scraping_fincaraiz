import pandas as pd
import os
def load_to_csv(data, path="./data/raw/Propiedades_FincaRaiz.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"✅ Guardado exitoso en {path}")