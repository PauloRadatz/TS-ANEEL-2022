# -*- coding: utf-8 -*-
# @Time    : 9/22/2022 1:55 PM
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
dss_file_caso_1 = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "caso1.dss"))
dss_file_caso_2 = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "caso2.dss"))
dss_file_caso_3 = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "caso3.dss"))
dss_file_caso_4 = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "caso4.dss"))


casos_list = ["Caso 1", "Caso 2", "Caso 3", "Caso 4"]
casos_dss_list = [dss_file_caso_1, dss_file_caso_2, dss_file_caso_3, dss_file_caso_4]
carga_list = ["Equilibrada", "Desequilibrada"]

carregamento_max = np.sqrt(3) * 0.22 * 140
carregamento_pu_list = [1, 0.75, 0.25]

carga_reator_list = [False, True]

ERROR_kwh = 0.00001

dss = py_dss_interface.DSSDLL()

casos_resultado_list = list()
carga_resultado_list = list()
energia_injetada_kwh_resultado_list = list()
carga_reator_resultado_list = list()
energia_calculada_kwh_list = list()
consumo_total_carga_kwh_list = list()
perdas_mwh_list = list()
perdas_per_list = list()

i = 0
for caso, carga, carregamento_pu, carga_reator in list(itertools.product(*[casos_list, carga_list, carregamento_pu_list, carga_reator_list])):

    if caso == "Caso 1":
        caso_dss = casos_dss_list[0]
    elif caso == "Caso 2":
        caso_dss = casos_dss_list[1]
    elif caso == "Caso 3":
        caso_dss = casos_dss_list[2]
    elif caso == "Caso 4":
        caso_dss = casos_dss_list[3]

    casos_resultado_list.append(caso)
    carga_resultado_list.append(carga)
    carga_reator_resultado_list.append(carga_reator)

    dss.text(f"compile [{caso_dss}]")
    dss.text("set mode=daily")
    dss.text("set number=1")
    dss.text("set stepsize=1h")
    dss.text("set tolerance=0.001")


    fator = 1
    if carga == "Desequilibrada":
        fator = 1/3

        dss.text("Edit Load.LB_M1 enabled=False")
        dss.text("Edit Load.LC_M1 enabled=False")
        dss.text("Edit Load.LB_M2 enabled=False")
        dss.text("Edit Load.LC_M2 enabled=False")

        dss.lines_first()
        if not carga_reator and dss.lines_read_phases() == 3:
            dss.text("Edit Load.LA_M1 bus1=b.1.0")
            dss.text("Edit Load.LA_M2 bus1=b.1.0")
        if carga_reator:
            dss.text("New reactor.R_Carga phases=1 bus1=B.4 bus2=B.0 r=15 x=0")
    else:
        if carga_reator:
            dss.text("New reactor.R_Carga phases=1 bus1=B.4 bus2=B.0 r=15 x=0")

    dss.text("batchedit reactor..* r=0.00001")

    energia_injetada_kwh = carregamento_pu * carregamento_max * fator
    energia_injetada_kwh_resultado_list.append(energia_injetada_kwh)

    do_energy_allocation(dss, energia_injetada_kwh, ERROR_kwh)

    dss.text("solve")
    energia_calculada_kwh_list.append(dss.meters_register_values()[0])
    consumo_total_carga_kwh_list.append(dss.meters_register_values()[4])
    perdas_mwh_list.append(dss.meters_register_values()[12])
    perdas_per_list.append(perdas_mwh_list[-1] * 100.0 / energia_calculada_kwh_list[-1])

    print(i)
    dss.text(f"save circuit dir={i}")
    i = i + 1


dict_to_df = dict()
dict_to_df["Caso"] = casos_resultado_list
dict_to_df["Carga condicao"] = carga_resultado_list
dict_to_df["Energia Injetada kWh"] = energia_injetada_kwh_resultado_list
dict_to_df["Reator na Carga"] = carga_reator_resultado_list
dict_to_df["Energia Calculada kWh"] = energia_calculada_kwh_list
dict_to_df["Consumo Total da Carga"] = consumo_total_carga_kwh_list
dict_to_df["Perdas kWh"] = perdas_mwh_list
dict_to_df["Perdas %"] = perdas_per_list

df = pd.DataFrame.from_dict(dict_to_df)

arquivo_resultados = str(pathlib.Path(script_path).joinpath("../../feeders", "Linha_BT", "resultados.csv"))

df.to_csv(arquivo_resultados)

print(df)