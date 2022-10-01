# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 1:35 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : criar_loadsshapes.py
# @Software: PyCharm


import pandas as pd
import py_dss_interface
import os
import pathlib
import time

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = str(pathlib.Path(script_path).joinpath("../../../feeders", "8500-Node", "Master.dss"))

dss = py_dss_interface.DSSDLL()

dss.text(f"compile [{dss_file}]")

loadshape_sem = list()
loadshape_com = list()
edit_load = list()

dss.loads_first()
for _ in range(dss.loads_count()):
    loadshape_sem.append(f"New loadshape.{dss.loads_read_name()} interval=1 npts=24 "
                         f"mult=(1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1)\n")
    loadshape_com.append(f"New loadshape.{dss.loads_read_name()} interval=1 npts=24 "
                         f"mult=(1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1) memorymapping=yes\n")
    edit_load.append(f"edit load.{dss.loads_read_name()} daily={dss.loads_read_name()}\n")
    dss.loads_next()

with open(pathlib.Path(script_path).joinpath("edit_carga.dss"), "w") as file:
    for line in edit_load:
        file.write(line)

with open(pathlib.Path(script_path).joinpath("loadshape_sem.dss"), "w") as file:
    for line in loadshape_sem:
        file.write(line)

with open(pathlib.Path(script_path).joinpath("loadshape_com.dss"), "w") as file:
    for line in loadshape_com:
        file.write(line)