# -*- coding: utf-8 -*-
# @Time    : 9/24/2022 12:28 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : sdbt.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import numpy as np
import pandas as pd
import itertools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_caso_1 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDBT", "v.dss"))
dss_file_caso_2 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDBT", "i.dss"))
dss_file_caso_3 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDBT", "ii.dss"))
dss_file_caso_4 = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDBT", "iii.dss"))



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
    # dss.text("set mode=daily")
    # dss.text("set number=1")
    # dss.text("set stepsize=1h")
    # dss.text("set tolerance=0.000001")
    # dss.text("set maxi=100")

    # TODO opendss with a bug when linegeometry
    # dss.text("edit line.l length=0.5")

    if carga_equilibrada:
        for i_source in ["ia", "ib", "ic"]:
            dss.isources_write_name(i_source)
            dss.isources_write_amps(dss.isources_read_amps() * carregamento_pu)

    else:
        dss.isources_write_name("ia")
        dss.isources_write_amps(dss.isources_read_amps() * carregamento_pu)
        # dss.isources_write_name("ib")
        # dss.isources_write_amps(0)
        # dss.isources_write_name("ic")
        # dss.isources_write_amps(0)
        dss.text("edit isource.ib enabled=NO")
        dss.text("edit isource.ic enabled=NO")

    dss.text("solve")

    if not dss.solution_read_converged():
        print("problema")

    # dss.meters_first()
    # perdas_kwh_list.append(dss.meters_register_values()[12])
    perdas_kwh_list.append(dss.circuit_losses()[0] / 1000.0)
    dss.circuit_set_active_element("line.l")
    # corrente_1_a_amps.append(dss.cktelement_currents_mag_ang()[0])
    # corrente_1_b_amps.append(dss.cktelement_currents_mag_ang()[2])
    # corrente_1_c_amps.append(dss.cktelement_currents_mag_ang()[4])
    # corrente_2_a_amps.append(dss.cktelement_currents_mag_ang()[8])
    # corrente_2_b_amps.append(dss.cktelement_currents_mag_ang()[10])
    # corrente_2_c_amps.append(dss.cktelement_currents_mag_ang()[12])

    print(i)
    # dss.text(f"save circuit dir={i}")
    i = i + 1


dict_to_df = dict()
dict_to_df["Caso"] = casos_resultado_list
dict_to_df["Carga Equilibrada"] = carga_equilibrada_resultado_list
dict_to_df["Perdas kWh por km"] = perdas_kwh_list
dict_to_df["Carregamento"] = carregamento_resultado_list
# dict_to_df["Carregamento A"] = corrente_1_b_amps
# dict_to_df["Carregamento A"] = corrente_1_c_amps
# dict_to_df["Corrente 2-a A"] = corrente_2_a_amps
# dict_to_df["Corrente 2-b A"] = corrente_2_b_amps
# dict_to_df["Corrente 2-c A"] = corrente_2_c_amps


df = pd.DataFrame.from_dict(dict_to_df)

arquivo_resultados = str(pathlib.Path(script_path).joinpath("../../Feeders", "resposta_21", "SDBT", "resultados.csv"))

df.to_csv(arquivo_resultados)

print(df)