import pandas as pd
import glob
from banco.ConectaDB import engine

arquivos = glob.glob("dataset/Fatura_*.csv")

#print("Arquivos encontrados:", arquivos)

dfs = []

for arquivo in arquivos:

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8"
    )

    dfs.append(df)

df = pd.concat(dfs)

df["Data de Compra"] = pd.to_datetime(
    df["Data de Compra"],
    format="%d/%m/%Y"
)

df["Valor (em R$)"] = (
    df["Valor (em R$)"]
    .astype(str)
    .str.replace(",", ".")
    .astype(float)
)

def parse_parcela(p):

    if p == "Única":
        return 1,1

    if "/" in str(p):
        x,y = p.split("/")
        return int(x),int(y)

    return None,None

df[["num_parcela","total_parcelas"]] = df["Parcela"].apply(
    lambda x: pd.Series(parse_parcela(x))
)

df.to_sql(
    "staging_transacoes",
    engine,
    if_exists="replace",
    index=False
)

print("ETL finalizado!")