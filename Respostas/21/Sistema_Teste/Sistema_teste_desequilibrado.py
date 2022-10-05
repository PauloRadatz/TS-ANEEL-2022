# -*- coding: utf-8 -*-
# @Time    : 9/18/2022 5:10 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : EnergyAllocation.py
# @Software: PyCharm

import py_dss_interface
import os
import pathlib

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_caso = str(pathlib.Path(script_path).joinpath(r"Arquivos_DSS\TS_ANEEL_MASTER_Delta_i.dss"))

def do_energy_allocation(dss: py_dss_interface.DSSDLL, energy_mwh, error_mwh):

    if not dss.meters_first():
        print("There is not energymeter at the feederhead")
        return False
    else:
        if dss.meters_count() > 1:
            print("There are more than 1 energymeter. Please make sure there is only one")
            return False

    energy_factor = 0

    for i in range(1000):
        energy_mwh_power_flow = 0

        # update_load(dss, energy_mwh_power_flow, energy_factor)
        update_load(dss, energy_factor)

        dss.text("solve")
        dss.text('Sample')

        if dss.solution_read_converged():

            energy_mwh_power_flow, delta_energy_mwh = calc_delta_energy(dss, energy_mwh)

            if i == 0:
                print(f"Original Model's Energy: {energy_mwh - delta_energy_mwh}")

            energy_factor = delta_energy_mwh / energy_mwh

            dss.meters_reset()

            if abs(delta_energy_mwh) < error_mwh:
                break
        else:
            print("Problema")

def update_load(dss, energy_factor):
    dss.loads_first()
    for _ in range(dss.loads_count()):
        dss.loads_write_kw(float(dss.loads_read_kw() * (1 + energy_factor)))
        dss.loads_next()

def calc_delta_energy(dss, energy_mwh):
    dss.meters_first()
    energy_mwh_power_flow = dss.meters_register_values()[0]
    delta_energy_mwh = energy_mwh - energy_mwh_power_flow

    return energy_mwh_power_flow, delta_energy_mwh

dss = py_dss_interface.DSSDLL()

dss.text(fr"Compile [{dss_file_caso}]")

dss.text('batchedit load..* vminpu=0.8 vmaxpu=1.2')

dss.solution_solve()

dss.loads_first()
for i in range(dss.loads_count()):
    if 'fase_a' in dss.loads_read_name():
        dss.text(f'edit {dss.cktelement_name()} kw={dss.loads_read_kw() * 1.3}')
    elif 'fase_b' in dss.loads_read_name():
        dss.text(f'edit {dss.cktelement_name()} kw={dss.loads_read_kw() * 0.7}')
    dss.loads_next()

dss.solution_solve()

energy_mwh = 15000
error_mwh = 1

do_energy_allocation(dss, energy_mwh, error_mwh)

energia_total = abs(dss.circuit_total_power()[0])
perdas_totais = dss.circuit_losses()[0] / 1000
perdas_percentuais = perdas_totais / energia_total * 100

print(f'Energia injetada (kWh): {energia_total}')
print(f'Perdas (kWh): {perdas_totais}')
print(f'Perdas (%): {perdas_percentuais}')

print("")