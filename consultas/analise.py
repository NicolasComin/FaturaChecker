import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from banco.ConectaDB import engine
from sqlalchemy import text

nsep = 100

with engine.connect() as conn:
    for i in range(nsep):
        print("=", end="")

    print("\nGasto total por categoria:\n")

    result = conn.execute(text("""
        SELECT c.nome_categoria, SUM(f.valor_brl) AS total_gasto
        FROM fato_transacao f
        JOIN dim_categoria c
        ON f.id_categoria = c.id_categoria
        WHERE c.nome_categoria <> '-'
        GROUP BY c.nome_categoria
        ORDER BY total_gasto DESC;
    """))

    for row in result:
        print(f"{row.nome_categoria:<60} R$ {row.total_gasto:>10.2f}")

    for i in range(nsep):
        print("=", end="")

    print("\nGastos por mês:\n")

    result = conn.execute(text("""
        SELECT d.ano, d.mes, SUM(f.valor_brl) AS total_gasto
        FROM fato_transacao f
        JOIN dim_data d
        ON f.id_data = d.id_data
        JOIN dim_categoria c
        ON f.id_categoria = c.id_categoria
        WHERE c.nome_categoria <> '-'
        GROUP BY d.ano, d.mes
        ORDER BY d.ano, d.mes;
    """))

    for row in result:
        print(f"{row.ano}-{row.mes:02d} -> R$ {row.total_gasto:.2f}")
    
    for i in range(nsep):
        print("=", end="")

    print("\nEstabelecimentos com maior gasto:\n")

    result = conn.execute(text("""
        SELECT e.nome_estabelecimento, SUM(f.valor_brl) AS total_gasto
        FROM fato_transacao f
        JOIN dim_estabelecimento e
        ON f.id_estabelecimento = e.id_estabelecimento
        JOIN dim_categoria c
        ON f.id_categoria = c.id_categoria
        WHERE c.nome_categoria <> '-'
        GROUP BY e.nome_estabelecimento
        ORDER BY total_gasto DESC
        LIMIT 10;
    """))

    for row in result:
        print(f"{row.nome_estabelecimento} -> R$ {row.total_gasto:.2f}")

    