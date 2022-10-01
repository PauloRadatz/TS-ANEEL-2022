# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 1:45 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : 2-com.py
# @Software: PyCharm


import pandas as pd
import py_dss_interface
import os
import pathlib
import time

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL("C:\Program Files\OpenDSS")

t_i = time.time()
dss.text(f"compile [{dss_file}]")
dss.text("set mode=daily")
dss.text("New Energymeter.m1 Line.ln5815900-1 1")
dss.text("Set Maxiterations=20")
dss.text("Set maxcontroli=100")

dss.text(f"redirect {pathlib.Path(script_path).joinpath('loadshape_com.dss')}")
# dss.text(f"redirect {pathlib.Path(script_path).joinpath('edit_carga.dss')}")

dss.text("solve")

dss.meters_first()
energia_kwh_dia = dss.meters_register_values()[0]

t_f = time.time() - t_i
print(energia_kwh_dia)
print(f"Python Total time: {round(t_f, 2)} s")