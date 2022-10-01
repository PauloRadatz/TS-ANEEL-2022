# -*- coding: utf-8 -*-
# @Time    : 9/24/2022 3:13 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : dados_linhas.py
# @Software: PyCharm

import os
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

sns.set_context("talk")
sns.set_style("whitegrid")


mpl_dict = {'figure.facecolor': 'white',
 'axes.labelcolor': '.15',
 'xtick.direction': 'out',
 'ytick.direction': 'out',
 'xtick.color': '.15',
 'ytick.color': '.15',
 'axes.axisbelow': True,
 'grid.linestyle': '--',
 'text.color': '.15',
 'font.family': ['sans-serif'],
 'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif'],
 'lines.solid_capstyle': 'round',
 'patch.edgecolor': 'w',
 'patch.force_edgecolor': True,
 'xtick.top': False,
 'ytick.right': False,
 'axes.grid': True,
 'axes.facecolor': 'white',
 'axes.edgecolor': '.8',
 'grid.color': '.8',
 'axes.spines.left': True,
 'axes.spines.bottom': True,
 'axes.spines.right': True,
 'axes.spines.top': True,
 'xtick.bottom': False,
 'ytick.left': False}

for key, value in mpl_dict.items():
    mpl.rcParams[key] = value

def calcula_erro(df):
 erro_per = list()
 for index, row in df.iterrows():
  atual = row["Perdas kWh"]
  base = df[(df["Caso"] == "v") & (df["Carregamento"] == row["Carregamento"])]["Perdas kWh"].values[0]
  erro_per.append((atual - base) * 100 / base)
 df["Erro Percentual"] = erro_per

script_path = os.path.dirname(os.path.abspath(__file__))

arquivo_resultados = \
 str(pathlib.Path(script_path).joinpath("dss", "SDBT", "resultados.csv"))

# arquivo_resultados = \
#  str(pathlib.Path(script_path).joinpath("dss", "SDMT", "resultados.csv"))

completo_df = pd.read_csv(arquivo_resultados, index_col=0)

eq_df = completo_df[completo_df["Carga Equilibrada"]] #[["Caso", "Perdas kWh"]]
des_df = completo_df[~ completo_df["Carga Equilibrada"]] #[["Caso", "Perdas kWh"]]

calcula_erro(eq_df)
calcula_erro(des_df)

des_df.sort_values("Carregamento", inplace=True)
eq_df.sort_values("Carregamento", inplace=True)

eq_res = eq_df.groupby("Caso").mean()
des_res = des_df.groupby("Caso").mean()

print("here")