from ConectaDB import engine
from sqlalchemy import text

with engine.connect() as conn:

    print("Carregando dimensão de datas...")

    conn.execute(text("""
        INSERT INTO dim_data (data, dia, mes, trimestre, ano, dia_semana)
        SELECT DISTINCT
            "Data de Compra",
            EXTRACT(DAY FROM "Data de Compra"),
            EXTRACT(MONTH FROM "Data de Compra"),
            EXTRACT(QUARTER FROM "Data de Compra"),
            EXTRACT(YEAR FROM "Data de Compra"),
            TO_CHAR("Data de Compra", 'Day')
        FROM staging_transacoes
        ON CONFLICT DO NOTHING
    """))

    print("Carregando dimensão titular...")

    conn.execute(text("""
        INSERT INTO dim_titular (nome_titular, final_cartao)
        SELECT DISTINCT
            "Nome no Cartão",
            "Final do Cartão"
        FROM staging_transacoes
        ON CONFLICT DO NOTHING
    """))

    print("Carregando dimensão categoria...")

    conn.execute(text("""
        INSERT INTO dim_categoria (nome_categoria)
        SELECT DISTINCT
            "Categoria"
        FROM staging_transacoes
        ON CONFLICT DO NOTHING
    """))

    print("Carregando dimensão estabelecimento...")

    conn.execute(text("""
        INSERT INTO dim_estabelecimento (nome_estabelecimento)
        SELECT DISTINCT
            "Descrição"
        FROM staging_transacoes
        ON CONFLICT DO NOTHING
    """))

    print("Carregando tabela fato...")

    conn.execute(text("""
        INSERT INTO fato_transacao (
            id_data,
            id_titular,
            id_categoria,
            id_estabelecimento,
            valor_brl,
            valor_usd,
            cotacao,
            parcela_texto,
            num_parcela,
            total_parcelas
        )
        SELECT
            d.id_data,
            t.id_titular,
            c.id_categoria,
            e.id_estabelecimento,
            s."Valor (em R$)",
            s."Valor (em US$)",
            s."Cotação (em R$)",
            s."Parcela",
            s.num_parcela,
            s.total_parcelas
        FROM staging_transacoes s
        JOIN dim_data d
            ON d.data = s."Data de Compra"
        JOIN dim_titular t
            ON t.nome_titular = s."Nome no Cartão"
        JOIN dim_categoria c
            ON c.nome_categoria = s."Categoria"
        JOIN dim_estabelecimento e
            ON e.nome_estabelecimento = s."Descrição"
    """))

    conn.commit()

print("Carga do Data Warehouse finalizada!")