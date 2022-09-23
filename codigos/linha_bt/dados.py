# -*- coding: utf-8 -*-
# @Time    : 9/23/2022 11:07 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : dados.py
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

script_path = os.path.dirname(os.path.abspath(__file__))
arquivo_resultados = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "resultados.csv"))


completo_df = pd.read_csv(arquivo_resultados, index_col=0)

# Casos 2 e 3 sem reator e carga desequilibrada nao validos
val = (completo_df["Caso"] == "Caso 2") & (completo_df["Reator na Carga"] == False) & (completo_df["Carga condicao"] == "Desequilibrada")
df = completo_df[~ val]
val = (completo_df["Caso"] == "Caso 3") & (completo_df["Reator na Carga"] == False) & (completo_df["Carga condicao"] == "Desequilibrada")
df = df[~ val]

def plot(data, x, y, hue, col, row):
 sns.catplot(kind="swarm", x=x, y=y, data=data, hue=hue, col=col, row=row, height=4, aspect=1.5)
 plt.tight_layout()
 plt.show()
 plt.clf()
 plt.close()

plot(data=df, x="Caso", y="Perdas %", hue="Energia Injetada kWh", col="Reator na Carga", row="Carga condicao")