
from pathlib import Path
import pandas as pd

# Caso 01 - Analise de demandas operacionais ficticias

arquivo = Path(__file__).resolve().parent / "caso_01_demandas_sinteticas.csv"

df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig")

# Indicadores gerais
abertos = df["status"] == "Aberto"
concluidos = df["status"] == "Concluido"

atrasados = (
    abertos &
    (df["situacao_prazo_simulada"] == "Atrasado")
)

print("\nCASO 01 - INTELIGENCIA OPERACIONAL")
print("Base de dados 100% ficticia")
print("-" * 45)

print("Total de demandas:", len(df))
print("Demandas concluidas:", concluidos.sum())
print("Demandas abertas:", abertos.sum())
print("Abertas atrasadas:", atrasados.sum())

# Distribuicao dos atrasados por area
ranking = (
    df.loc[atrasados]
    .groupby("area_ficticia")
    .size()
    .sort_values(ascending=False)
)

print("\nATRASADOS POR AREA")
print(ranking.to_string())

# Analise de aging
aging = pd.to_numeric(
    df.loc[atrasados, "dias_atraso_em_aberto"],
    errors="coerce"
)

print("\nAging medio:", round(aging.mean(), 1), "dias")

print("\nAnalise concluida.")
