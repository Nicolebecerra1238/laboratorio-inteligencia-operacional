
from pathlib import Path
import pandas as pd

# CASO 01 - DIAGNOSTICO OPERACIONAL
# Dados 100% ficticios

pasta = Path(__file__).resolve().parent
arquivo = pasta / "caso_01_demandas_sinteticas.csv"

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8-sig"
)

# Identificar demandas abertas e atrasadas
abertas = df["status"] == "Aberto"

atrasadas = (
    abertas &
    (df["situacao_prazo_simulada"] == "Atrasado")
)

# 1. TAXA DE ATRASO POR AREA
analise = df.assign(
    abertas=abertas.astype(int),
    atrasadas=atrasadas.astype(int)
)

por_area = (
    analise.groupby("area_ficticia")
    .agg(
        abertas=("abertas", "sum"),
        atrasadas=("atrasadas", "sum")
    )
    .reset_index()
)

por_area["taxa_atraso_pct"] = (
    por_area["atrasadas"] /
    por_area["abertas"].replace(0, float("nan")) * 100
).round(1)

por_area = por_area.sort_values(
    "taxa_atraso_pct",
    ascending=False
)

# 2. FAIXAS DE AGING
base_atrasados = df.loc[atrasadas].copy()

base_atrasados["dias_atraso_em_aberto"] = pd.to_numeric(
    base_atrasados["dias_atraso_em_aberto"],
    errors="coerce"
)

faixas = [
    "1-7 dias",
    "8-30 dias",
    "31-60 dias",
    "61+ dias"
]

base_atrasados["faixa_aging"] = pd.cut(
    base_atrasados["dias_atraso_em_aberto"],
    bins=[0, 7, 30, 60, float("inf")],
    labels=faixas
)

por_aging = (
    base_atrasados["faixa_aging"]
    .value_counts(sort=False)
    .reset_index(name="quantidade")
)

# 3. COMPLEXIDADE DOS CASOS ATRASADOS
por_complexidade = (
    base_atrasados["complexidade_ficticia"]
    .value_counts()
    .reset_index(name="quantidade")
)

# APRESENTAR RESULTADOS
print("\nDIAGNOSTICO OPERACIONAL")
print("Base de dados ficticia")
print("-" * 45)

print("\n1. TAXA DE ATRASO POR AREA")
print(por_area.to_string(index=False))

print("\n2. FAIXAS DE AGING")
print(por_aging.to_string(index=False))

print("\n3. COMPLEXIDADE")
print(por_complexidade.to_string(index=False))

# EXPORTAR RESULTADOS
saida = pasta / "saida_analise"
saida.mkdir(exist_ok=True)

por_area.to_csv(
    saida / "taxa_atraso_por_area.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

por_aging.to_csv(
    saida / "faixas_aging.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

por_complexidade.to_csv(
    saida / "atrasados_por_complexidade.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nAnalise concluida!")
