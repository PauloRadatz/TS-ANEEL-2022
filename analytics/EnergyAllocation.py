# -*- coding: utf-8 -*-
# @Time    : 9/18/2022 5:10 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : EnergyAllocation.py
# @Software: PyCharm

import py_dss_interface


def do_energy_allocation(dss: py_dss_interface.DSSDLL, energy_mwh, error_mwh=1):

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

# def update_load(dss, energy_mwh_power_flow, energy_factor):
#
#     if energy_mwh_power_flow:
#
#
#         dss.text(f"set loadmult={energy_mwh_power_flow  * (1 + energy_factor)}")

def calc_delta_energy(dss, energy_mwh):
    dss.meters_first()
    energy_mwh_power_flow = dss.meters_register_values()[0]
    delta_energy_mwh = energy_mwh - energy_mwh_power_flow

    return energy_mwh_power_flow, delta_energy_mwh
