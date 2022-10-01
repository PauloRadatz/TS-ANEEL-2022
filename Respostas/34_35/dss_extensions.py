# -*- coding: utf-8 -*-
# @Time    : 9/27/2022 12:54 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : dss_extensions.py
# @Software: PyCharm

import os
import pathlib
import pandas as pd
import time

import opendssdirect as dss

from EnergyAllocation_2 import do_energy_allocation_2

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
dss.run_command(f"compile [{dss_file}]")
dss.run_command("set mode=daily")
dss.run_command(f"set number={24 * 31}")
dss.run_command("set stepsize=1h")
dss.run_command("New Energymeter.m1 Line.ln5815900-1 1")
dss.run_command("Set Maxiterations=20")

do_energy_allocation_2(dss, energia_injetada_kwh, ERROR_kwh)

dss.run_command("Set TotalTime=0")
dss.run_command("solve")
total_time = dss.run_command("Get TotalTime")
step_time = dss.run_command("Get StepTime")

energia_injetada_kwh_resultado_list.append(energia_injetada_kwh)
energia_calculada_kwh_list.append(dss.Meters.RegisterValues()[0])
consumo_total_carga_kwh_list.append(dss.Meters.RegisterValues()[4])
perdas_kwh_list.append(dss.Meters.RegisterValues()[12])
perdas_per_list.append(perdas_kwh_list[-1] * 100.0 / energia_calculada_kwh_list[-1])

t_f = time.time() - t_i

dict_to_df = dict()
dict_to_df["Energia Injetada kWh"] = energia_injetada_kwh_resultado_list
dict_to_df["Energia Calculada kWh"] = energia_calculada_kwh_list
dict_to_df["Consumo Total da Carga"] = consumo_total_carga_kwh_list
dict_to_df["Perdas kWh"] = perdas_kwh_list
dict_to_df["Perdas %"] = perdas_per_list

df = pd.DataFrame.from_dict(dict_to_df)

print("dss-extensions")
print(f"Python Total time: {t_f}")
print(f"dss-extensions Total Time: {total_time}")
print(f"dss-extensions step Time: {step_time}")
