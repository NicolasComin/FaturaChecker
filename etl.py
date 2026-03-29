import pandas as pd
import glob
from banco.ConectaDB import engine

arquivos = glob.glob("dataset/Fatura_*.csv")

dfs = []

for arquivo in arquivos:
    df_temp = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
    )
    dfs.append(df_temp)

df = pd.concat(dfs, ignore_index=True)

# Converter data
df["Data de Compra"] = pd.to_datetime(
    df["Data de Compra"],
    format="%d/%m/%Y",
    dayfirst=True,
    errors="coerce"
)

# Converter valor
df["Valor (em R$)"] = (
    df["Valor (em R$)"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["Valor (em R$)"] = pd.to_numeric(
    df["Valor (em R$)"],
    errors="coerce"
)

# Filtro de valores negativos
df = df[df["Valor (em R$)"] >= 0].copy()

# Função de parcelas
def parse_parcela(p):
    if p == "Única":
        return 1, 1

    if "/" in str(p):
        x, y = p.split("/")
        return int(x), int(y)

    return None, None

df[["num_parcela", "total_parcelas"]] = df["Parcela"].apply(
    lambda x: pd.Series(parse_parcela(x))
)

# Enviar pro banco
df.to_sql(
    "staging_transacoes",
    engine,
    if_exists="replace",
    index=False
)

print("ETL finalizado!")