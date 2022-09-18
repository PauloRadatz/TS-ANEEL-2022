# -*- coding: utf-8 -*-
# @Time    : 9/18/2022 6:16 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : example_1.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface

from analytics import do_energy_allocation

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = str(pathlib.Path(script_path).joinpath("../feeders", "4Bus-YY-Bal", "4Bus-YY-Bal.dss"))

dss = py_dss_interface.DSSDLL()

dss.text(f"compile [{dss_file}]")
dss.text("batchedit load..* daily=default")
dss.text("New energymeter.m line.line1 1")
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")

energy_mwh = 150000
error_mwh = 0.5
do_energy_allocation(dss, energy_mwh, error_mwh)

# You have OpenDSS model with energy allocated - then you can use it for whatever you want to
dss.text("solve")
losses_mwh = dss.meters_register_values()[0]
energy_mwh_power_flow = dss.meters_register_values()[0]

print(f"Energy MWh Desired: {energy_mwh} MWh\nEnergy MWh after allocation: {energy_mwh_power_flow} MWh\nLosses: {losses_mwh} MWh")
