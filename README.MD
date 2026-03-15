# Projeto Data Warehouse - Transações de Cartão

Aluno: Nícolas Comin Todero

## Descrição

Este projeto implementa um pipeline ETL para carregar dados de faturas de cartão
de crédito em um Data Warehouse PostgreSQL.

## Tecnologias

- Python
- PostgreSQL
- Pandas
- SQLAlchemy

## Estrutura

dataset -> arquivos CSV
banco -> criação do banco e load dos dados
consultas -> busca de informacoes para análise 

## Execução

1. Criar banco PostgreSQL

2. Executar script SQL

3. Instalar dependências

pip install -r requirements.txt

4. Executar ETL

python etl/etl.py

## Análises realizadas

1. Gasto total por categoria
2. Gasto por mês
3. Top 10 estabelecimentos com maior gasto