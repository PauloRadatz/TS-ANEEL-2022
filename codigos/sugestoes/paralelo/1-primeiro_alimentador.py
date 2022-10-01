# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 2:04 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : 1-primeiro_alimentador.py
# @Software: PyCharm

import pandas as pd
import py_dss_interface
import os
import pathlib
import time

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL()

t_i = time.time()
dss.text(f"compile [{dss_file}]")
dss.text(f"batchedit load..* daily=default")
dss.text("set mode=daily")
dss.text("set number=168")
dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")
dss.text("Set maxcontroli=100")

dss.text("solve")

dss.meters_first()
energia_kwh_dia = dss.meters_register_values()[0]

t_f = time.time() - t_i
print(f"Energia = {energia_kwh_dia}")