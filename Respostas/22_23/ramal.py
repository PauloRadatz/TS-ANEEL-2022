# -*- coding: utf-8 -*-
# @Time    : 9/27/2022 8:31 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : ramal.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import pandas as pd
import itertools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_caso_1 = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "caso1.dss"))
dss_file_caso_2 = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "caso2.dss"))
dss_file_caso_3 = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "caso3.dss"))
dss_file_caso_4 = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "caso4.dss"))
dss_file_caso_5 = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "caso5.dss"))

casos_list = ["Caso 1", "Caso 2", "Caso 3", "Caso 4", "Caso 5"]
casos_dss_list = [dss_file_caso_1, dss_file_caso_2, dss_file_caso_3, dss_file_caso_4]
carregamento_pu_list = [1, 0.75, 0.5, 0.25]
carregamento_pu_list = [1]

dss = py_dss_interface.DSSDLL("C:\Program Files\OpenDSS")

casos_resultado_list = list()
perdas_kwh_list = list()
carregamento_resultado_list = list()

i = 0
for caso, carregamento_pu in list(itertools.product(*[casos_list, carregamento_pu_list])):

    if caso == "Caso 1":
        caso_dss = casos_dss_list[0]
    elif caso == "Caso 2":
        caso_dss = casos_dss_list[1]
    elif caso == "Caso 3":
        caso_dss = casos_dss_list[2]
    elif caso == "Caso 4":
        caso_dss = casos_dss_list[3]
    elif caso == "Caso 5":
        caso_dss = casos_dss_list[3]

    casos_resultado_list.append(caso)
    carregamento_resultado_list.append(carregamento_pu)

    dss.text(f"compile [{caso_dss}]")
    dss.isources_write_name("ia")
    dss.isources_write_amps(dss.isources_read_amps() * carregamento_pu)

    dss.text("solve")

    if not dss.solution_read_converged():
        print("problema")

    perdas_kwh_list.append(dss.circuit_losses()[0] / 1000.0)
    dss.circuit_set_active_element("line.l")

    print(i)
    # dss.text(f"save circuit dir={i}")
    i = i + 1

    dict_to_df = dict()
    dict_to_df["Caso"] = casos_resultado_list
    dict_to_df["Perdas kWh"] = perdas_kwh_list
    dict_to_df["Carregamento"] = carregamento_resultado_list

arquivo_resultados = str(pathlib.Path(script_path).joinpath("dss", "Ramal", "resultados.csv"))
df = pd.DataFrame.from_dict(dict_to_df)
df.to_csv(arquivo_resultados)

print(df)