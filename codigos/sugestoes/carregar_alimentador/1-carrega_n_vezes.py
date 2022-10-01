# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 11:22 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : 1-carrega_n_vezes.py
# @Software: PyCharm

import pandas as pd
import py_dss_interface
import os
import pathlib
import time

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL()

energia_kwh_dia = dict()

t_i = time.time()
for dia in ["DU", "SA", "DO"]:
    dss.text(f"compile [{dss_file}]")
    dss.text(f"batchedit load..* daily=default")
    dss.text("set mode=daily")
    dss.text("New Energymeter.m1 Line.ln5815900-1 1")
    dss.text("Set Maxiterations=20")
    dss.text("Set maxcontroli=100")

    if dia == "DU":
        mult = 1
    elif dia == "SA":
        mult = 0.9
    elif dia == "DO":
        mult = 1.1

    # dss.loads_first()
    # for _ in range(dss.loads_count()):
    #     dss.loads_write_kw(mult * dss.loads_read_kw())
    #     dss.loads_next()

    # dss.text(f"set loadmult={mult}")
    dss.text("solve")

    dss.meters_first()
    energia_kwh_dia[dia] = dss.meters_register_values()[0]

t_f = time.time() - t_i
print(energia_kwh_dia)
print(f"Python Total time: {round(t_f, 2)} s")
