# -*- coding: utf-8 -*-
# @Time    : 9/18/2022 5:10 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : EnergyAllocation.py
# @Software: PyCharm

import py_dss_interface


def do_energy_allocation(dss: py_dss_interface.DSSDLL, energy_kwh, error_kwh=1):

    if not dss.meters_first():
        print("There is not energymeter at the feederhead")
        return False
    else:
        if dss.meters_count() > 1:
            print("There are more than 1 energymeter. Please make sure there is only one")
            return False

    energy_factor = 0

    for i in range(1000):
        update_load(dss, energy_factor)

        dss.text("solve")

        if dss.solution_read_converged():

            delta_energy_kwh = calc_delta_energy(dss, energy_kwh)

            if i == 0:
                print(f"Original Model's Energy: {energy_kwh - delta_energy_kwh}")

            energy_factor = delta_energy_kwh / energy_kwh

            dss.meters_reset()

            if abs(delta_energy_kwh) < error_kwh:
                break
        else:
            print("Problema")

def update_load(dss, energy_factor):
    dss.loads_first()
    for _ in range(dss.loads_count()):
        dss.loads_write_kw(float(dss.loads_read_kw() * (1 + energy_factor)))
        dss.loads_next()

def calc_delta_energy(dss, energy_kwh):
    dss.meters_first()
    energy_kwh_power_flow = dss.meters_register_values()[0]
    delta_energy_kwh = energy_kwh - energy_kwh_power_flow

    return delta_energy_kwh
