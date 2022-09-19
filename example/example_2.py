# -*- coding: utf-8 -*-
# @Time    : 9/19/2022 5:46 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : example_2.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
import pandas as pd

from analytics import do_energy_allocation

def config_dss_model():
    dss.text(f"compile [{dss_file}]")
    dss.text("batchedit load..* daily=default")
    dss.text("New energymeter.m line.MinhaLinha 1")
    dss.text("set mode=daily")
    dss.text("set number=24")
    dss.text("set stepsize=1h")

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = str(pathlib.Path(script_path).joinpath("../feeders", "29", "Master.dss"))

dss = py_dss_interface.DSSDLL()

energy_mwh = 70000
error_mwh = 0.05

scenario_list = list()
energy_mwh_power_flow_list = list()
load_consumption_list = list()
losses_mwh_list = list()
losses_per_list = list()

# Scenario 1
scenario_list.append("Load A with 3000 kW others 0")
config_dss_model()
dss.loads_write_name("load1A")
dss.loads_write_kw(dss.loads_read_kw() * 3)
dss.loads_write_name("load1B")
dss.loads_write_kw(0.0001)
dss.loads_write_name("load1C")
dss.loads_write_kw(0.0001)

do_energy_allocation(dss, energy_mwh, error_mwh)

# You have OpenDSS model with energy allocated - then you can use it for whatever you want to
dss.text("solve")
energy_mwh_power_flow_list.append(dss.meters_register_values()[0])
load_consumption_list.append(dss.meters_register_values()[4])
losses_mwh_list.append(dss.meters_register_values()[12])
losses_per_list.append(losses_mwh_list[-1] * 100.0 / energy_mwh_power_flow_list[-1])

# Scenario 2
scenario_list.append("All loads with 1000 kW")
config_dss_model()

do_energy_allocation(dss, energy_mwh, error_mwh)

# You have OpenDSS model with energy allocated - then you can use it for whatever you want to
dss.text("solve")
energy_mwh_power_flow_list.append(dss.meters_register_values()[0])
load_consumption_list.append(dss.meters_register_values()[4])
losses_mwh_list.append(dss.meters_register_values()[12])
losses_per_list.append(losses_mwh_list[-1] * 100.0 / energy_mwh_power_flow_list[-1])

dict_to_df = dict()
dict_to_df["Scenario"] = scenario_list
dict_to_df["Feeder Energy MWh"] = energy_mwh_power_flow_list
dict_to_df["Load Consumption MWh"] = load_consumption_list
dict_to_df["Losses MWh"] = losses_mwh_list
dict_to_df["Losses %"] = losses_per_list

df = pd.DataFrame.from_dict(dict_to_df)

print(df)