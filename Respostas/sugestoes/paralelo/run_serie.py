# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 2:07 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : run_serie.py
# @Software: PyCharm


import subprocess
import os
import pathlib
import time


def roda_alimentador(python, alimentador):
    subprocess.call([python, alimentador])

if __name__ == '__main__':

    script_path = os.path.dirname(os.path.abspath(__file__))

    python = str(pathlib.Path(script_path).joinpath("../../../venv", "Scripts", "python.exe"))
    alimentador_1 = str(pathlib.Path(script_path).joinpath("1-primeiro_alimentador.py"))
    alimentador_2 = str(pathlib.Path(script_path).joinpath("2-segundo_alimentador.py"))

    t_i = time.time()

    roda_alimentador(python, alimentador_1)
    roda_alimentador(python, alimentador_2)

    t_f = time.time() - t_i
    print(f"Python Total time: {round(t_f, 2)} s")
