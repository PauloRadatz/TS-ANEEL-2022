# -*- coding: utf-8 -*-
# @Time    : 9/27/2022 12:53 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : opendss.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import pandas as pd
import time

dss = py_dss_interface.DSSDLL()

from analytics import do_energy_allocation

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = str(pathlib.Path(script_path).joinpath("../../feeders", "8500-Node", "Master.dss"))

ERROR_kwh = 0.01
energia_injetada_kwh = 285965 * 1.5 * 31

energia_injetada_kwh_resultado_list = list()
energia_calculada_kwh_list = list()
consumo_total_carga_kwh_list = list()
perdas_kwh_list = list()
perdas_per_list = list()

t_i = time.time()
dss.text(f"compile [{dss_file}]")
dss.text("set mode=daily")
dss.text(f"set number={24 * 31}")
dss.text("set stepsize=1h")
dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")

do_energy_allocation(dss, energia_injetada_kwh, ERROR_kwh)

dss.text("solve")

energia_injetada_kwh_resultado_list.append(energia_injetada_kwh)
energia_calculada_kwh_list.append(dss.meters_register_values()[0])
consumo_total_carga_kwh_list.append(dss.meters_register_values()[4])
perdas_kwh_list.append(dss.meters_register_values()[12])
perdas_per_list.append(perdas_kwh_list[-1] * 100.0 / energia_calculada_kwh_list[-1])

t_f = time.time() - t_i

dict_to_df = dict()
dict_to_df["Energia Injetada kWh"] = energia_injetada_kwh_resultado_list
dict_to_df["Energia Calculada kWh"] = energia_calculada_kwh_list
dict_to_df["Consumo Total da Carga"] = consumo_total_carga_kwh_list
dict_to_df["Perdas kWh"] = perdas_kwh_list
dict_to_df["Perdas %"] = perdas_per_list

df = pd.DataFrame.from_dict(dict_to_df)

print("here")