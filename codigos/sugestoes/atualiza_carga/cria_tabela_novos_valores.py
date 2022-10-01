# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 12:42 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : cria_tabela_novos_valores.py
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

name_load = list()
kw_novo = list()
daily_novo = list()
dss.loads_first()
for _ in range(dss.loads_count()):
    name_load.append(dss.loads_read_name())
    kw_novo.append(dss.loads_read_kw())
    daily_novo.append("default")
    dss.loads_next()

dict_to_df = dict()
dict_to_df["Name"] = name_load
dict_to_df["kw"] = kw_novo
dict_to_df["daily"] = daily_novo

df = pd.DataFrame.from_dict(dict_to_df)
df.to_csv(pathlib.Path(script_path).joinpath("Cargas_Atualizas.csv"))
