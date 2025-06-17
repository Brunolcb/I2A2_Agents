import os
import pandas as pd

cabecalho_df = pd.read_csv("data/202401_NFs_Cabecalho.csv")
itens_df = pd.read_csv("data/202401_NFs_Itens.csv")

print(cabecalho_df.columns)
print(itens_df.columns)

print(cabecalho_df.head(1).to_markdown(index=False))

print(itens_df.head(1).to_markdown(index=False))