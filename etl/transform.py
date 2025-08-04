import pandas as pd

def clean_data(data):
    df = pd.DataFrame(data)

    #limpiar la columna de precio y convertir a int
    df['Precio']= df['Precio'].str.replace(r'[^\d]','', regex=True).astype(int)

    #Separar la tipologia en muero de habitaciones, baños y area
    df[['habitaciones','baños','area']]=df['Tipología'].str.extract(r'(\d+) Habs\. (\d+) Baño. *?(\d+) \s*m')

    df['habitaciones'] = pd.to_numeric(df['habitaciones'],errors='coerce')
    df['baños']= pd.to_numeric(df['baños'],errors='coerce')
    df['area']= pd.to_numeric(df['area'],errors='coerce')

    df = df.drop(columns=["Tipología"])

    return df

