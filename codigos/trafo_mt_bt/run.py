# -*- coding: utf-8 -*-
# @Time    : 9/23/2022 12:53 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : run.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import numpy as np
import pandas as pd
import itertools

from analytics import do_energy_allocation

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_caso_1 = str(pathlib.Path(script_path).joinpath("../../feeders", "Trafo_MT_BT", "caso1.dss"))
dss_file_caso_2 = str(pathlib.Path(script_path).joinpath("../../feeders", "Trafo_MT_BT", "caso2.dss"))
dss_file_caso_3 = str(pathlib.Path(script_path).joinpath("../../feeders", "Trafo_MT_BT", "caso3.dss"))

casos_list = ["Caso 1", "Caso 2", "Caso 3"]
casos_dss_list = [dss_file_caso_1, dss_file_caso_2, dss_file_caso_3]
carregamento_pu_list = [1, 0.75, 0.5, 0.25]
carga_equilibrada_list = [True, False]

carga_reator_list = [False, True]

ERROR_kwh = 0.00001

dss = py_dss_interface.DSSDLL()

casos_resultado_list = list()
perdas_kwh_list = list()
carga_equilibrada_resultado_list = list()
carregamento_resultado_list = list()

i = 0
for carga_equilibrada, caso, carregamento_pu in list(itertools.product(*[carga_equilibrada_list, casos_list, carregamento_pu_list])):

    if caso == "Caso 1":
        caso_dss = casos_dss_list[0]
    elif caso == "Caso 2":
        caso_dss = casos_dss_list[1]
    elif caso == "Caso 3":
        caso_dss = casos_dss_list[2]
    elif caso == "Caso 4":
        caso_dss = casos_dss_list[3]

    casos_resultado_list.append(caso)
    carga_equilibrada_resultado_list.append(carga_equilibrada)
    carregamento_resultado_list.append(carregamento_pu)

    dss.text(f"compile [{caso_dss}]")
    dss.text("set mode=daily")
    dss.text("set number=1")
    dss.text("set stepsize=1h")
    # dss.text("set tolerance=0.001")


    fator = 1
    if not carga_equilibrada:
        fator = 1/3

        dss.text("Edit Load.LB enabled=False")
        dss.text("Edit Load.LC enabled=False")

    dss.text(f"set loadmult={fator * carregamento_pu}")

    dss.text("solve")

    if not dss.solution_read_converged():
        print("problema")

    perdas_total = dss.circuit_losses()[0] / 1000.0
    perdas_line = dss.circuit_line_losses()[0]
    perdas_kwh_list.append(perdas_total - perdas_line)
    print(i)
    # dss.text(f"save circuit dir={i}")
    i = i + 1


dict_to_df = dict()
dict_to_df["Caso"] = casos_resultado_list
dict_to_df["Carga Equilibrada"] = carga_equilibrada_resultado_list
dict_to_df["Perdas kWh"] = perdas_kwh_list
dict_to_df["Carregamento"] = carregamento_resultado_list

df = pd.DataFrame.from_dict(dict_to_df)

arquivo_resultados = str(pathlib.Path(script_path).joinpath("../../Feeders", "Trafo_MT_BT", "resultados.csv"))

df.to_csv(arquivo_resultados)

print(df)