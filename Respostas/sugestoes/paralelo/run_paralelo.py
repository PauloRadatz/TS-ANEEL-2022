# -*- coding: utf-8 -*-
# @Time    : 10/1/2022 2:12 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : run_paralelo.py
# @Software: PyCharm


import subprocess
import os
import pathlib
import time
from multiprocessing import Process
from multiprocessing import freeze_support


def roda_alimentador(python, alimentador):
    subprocess.call([python, alimentador])

if __name__ == '__main__':
    freeze_support()

    script_path = os.path.dirname(os.path.abspath(__file__))

    python = str(pathlib.Path(script_path).joinpath("../../../venv", "Scripts", "python.exe"))
    alimentador_1 = str(pathlib.Path(script_path).joinpath("1-primeiro_alimentador.py"))
    alimentador_2 = str(pathlib.Path(script_path).joinpath("2-segundo_alimentador.py"))

    t_i = time.time()

    alimentadores = list()
    for i in range(2):
        if i == 0:
            alimentador = alimentador_1
        else:
            alimentador = alimentador_2
        roda = Process(target=roda_alimentador, args=(python, alimentador,))
        alimentadores.append(roda)
        roda.start()

    for roda in alimentadores:
        roda.join()

    t_f = time.time() - t_i
    print(f"Python Total time: {round(t_f, 2)} s")