from sqlalchemy import text
from ConectaDB import engine

sql = """
CREATE TABLE IF NOT EXISTS dim_data (
    id_data SERIAL PRIMARY KEY,
    data DATE,
    dia INT,
    mes INT,
    trimestre INT,
    ano INT,
    dia_semana VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_titular (
    id_titular SERIAL PRIMARY KEY,
    nome_titular TEXT,
    final_cartao INT
);

CREATE TABLE IF NOT EXISTS dim_categoria (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria TEXT
);

CREATE TABLE IF NOT EXISTS dim_estabelecimento (
    id_estabelecimento SERIAL PRIMARY KEY,
    nome_estabelecimento TEXT
);

CREATE TABLE IF NOT EXISTS fato_transacao (
    id SERIAL PRIMARY KEY,
    id_data INT REFERENCES dim_data(id_data),
    id_titular INT REFERENCES dim_titular(id_titular),
    id_categoria INT REFERENCES dim_categoria(id_categoria),
    id_estabelecimento INT REFERENCES dim_estabelecimento(id_estabelecimento),
    valor_brl NUMERIC,
    valor_usd NUMERIC,
    cotacao NUMERIC,
    parcela_texto TEXT,
    num_parcela INT,
    total_parcelas INT
);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("Tabelas criadas com sucesso!")