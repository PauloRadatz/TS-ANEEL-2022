# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 11:22 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : 1-atualiza_cada.py
# @Software: PyCharm

import pandas as pd
import py_dss_interface
import os
import pathlib
import time

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL()

energia_kwh_dia = dict()

t_i = time.time()
dss.text(f"compile [{dss_file}]")
dss.text(f"batchedit load..* daily=default")
dss.text("set mode=daily")
dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")
dss.text("Set maxcontroli=100")

carga_tabela = pd.read_csv(pathlib.Path(script_path).joinpath("Cargas_Atualizas.csv"))
for index, row in carga_tabela.iterrows():
    dss.text(f"Edit load.{row['Name']} kw={row['kw']} daily={row['daily']}")

dss.text("solve")

dss.meters_first()
energia_kwh_dia = dss.meters_register_values()[0]

t_f = time.time() - t_i
print(energia_kwh_dia)
print(f"Python Total time: {round(t_f, 2)} s")
