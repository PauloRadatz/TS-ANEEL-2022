# -*- coding: utf-8 -*-
# @Time    : 9/26/2022 3:02 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : sdmt.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import pandas as pd
import itertools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_caso_1 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDMT", "v.dss"))
dss_file_caso_2 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDMT", "i.dss"))
dss_file_caso_3 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDMT", "ii.dss"))
dss_file_caso_4 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDMT", "iii.dss"))

casos_list = ["v", "i", "ii", "iii"]
casos_dss_list = [dss_file_caso_1, dss_file_caso_2, dss_file_caso_3, dss_file_caso_4]
carregamento_pu_list = [1, 0.75, 0.5, 0.25]
carga_equilibrada_list = [True, False]

dss = py_dss_interface.DSSDLL("C:\Program Files\OpenDSS")

casos_resultado_list = list()
perdas_kwh_list = list()
carga_equilibrada_resultado_list = list()
carregamento_resultado_list = list()
corrente_1_a_amps = list()
corrente_1_b_amps = list()
corrente_1_c_amps = list()
corrente_2_a_amps = list()
corrente_2_b_amps = list()
corrente_2_c_amps = list()

i = 0
for carga_equilibrada, caso, carregamento_pu in list(itertools.product(*[carga_equilibrada_list, casos_list, carregamento_pu_list])):

    if caso == "v":
        caso_dss = casos_dss_list[0]
    elif caso == "i":
        caso_dss = casos_dss_list[1]
    elif caso == "ii":
        caso_dss = casos_dss_list[2]
    elif caso == "iii":
        caso_dss = casos_dss_list[3]

    casos_resultado_list.append(caso)
    carga_equilibrada_resultado_list.append(carga_equilibrada)
    carregamento_resultado_list.append(carregamento_pu)

    dss.text(f"compile [{caso_dss}]")

    if carga_equilibrada:
        for i_source in ["ia", "ib", "ic"]:
            dss.isources_write_name(i_source)
            dss.isources_write_amps(dss.isources_read_amps() * carregamento_pu)

    else:
        dss.isources_write_name("ia")
        dss.isources_write_amps(dss.isources_read_amps() * carregamento_pu)
        dss.text("edit isource.ib enabled=NO")
        dss.text("edit isource.ic enabled=NO")

    dss.text("solve")

    if not dss.solution_read_converged():
        print("problema")

    perdas_kwh_list.append(dss.circuit_losses()[0] / 1000.0)

    print(i)
    # dss.text(f"save circuit dir={i}")
    i = i + 1


dict_to_df = dict()
dict_to_df["Caso"] = casos_resultado_list
dict_to_df["Carga Equilibrada"] = carga_equilibrada_resultado_list
dict_to_df["Perdas kWh"] = perdas_kwh_list
dict_to_df["Carregamento"] = carregamento_resultado_list

df = pd.DataFrame.from_dict(dict_to_df)

arquivo_resultados = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDMT", "resultados.csv"))

df.to_csv(arquivo_resultados)

print("here")