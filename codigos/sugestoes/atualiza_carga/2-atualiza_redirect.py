# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 11:34 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : 2-atualiza_redirect.py
# @Software: PyCharm

import pandas as pd
import py_dss_interface
import os
import pathlib
import time
import numpy as np

def escreve_linhas(row):
    return f"Edit load.{row['Name']} kw={row['kw']} daily={row['daily']}"

# def escreve_linhas(name, kw, daily):
#     return f"Edit load.{name} kw={kw} daily={daily}"

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL()

escreve_linhas_vec = np.vectorize(escreve_linhas)

t_i = time.time()
dss.text(f"compile [{dss_file}]")
dss.text(f"batchedit load..* daily=default")
dss.text("set mode=daily")
dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")
dss.text("Set maxcontroli=100")

carga_tabela = pd.read_csv(pathlib.Path(script_path).joinpath("Cargas_Atualizas.csv"))
cargas = carga_tabela.apply(escreve_linhas, axis=1)
cargas.to_csv(pathlib.Path(script_path).joinpath("Cargas_Atualizas.dss"), index=False, header=False)

# cargas = escreve_linhas_vec(carga_tabela["Name"].values, carga_tabela["kw"].values, carga_tabela["daily"].values)
# np.savetxt(pathlib.Path(script_path).joinpath("Cargas_Atualizas.dss"), cargas, fmt="%s")

dss.text(f"redirect {pathlib.Path(script_path).joinpath('Cargas_Atualizas.dss')}")
dss.text("solve")

dss.meters_first()
energia_kwh_dia = dss.meters_register_values()[0]

t_f = time.time() - t_i
print(energia_kwh_dia)
print(f"Python Total time: {round(t_f, 2)} s")

