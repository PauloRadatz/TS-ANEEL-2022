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

    for i in range(100):

        update_load(dss, energy_factor)

        dss.text("solve")

        delta_energy_mwh = calc_delta_energy(dss, energy_mwh)
        energy_factor = delta_energy_mwh / energy_mwh

        dss.meters_reset()

        if abs(delta_energy_mwh) < error_mwh:
            break

def update_load(dss, energy_factor):
    dss.loads_first()
    for _ in range(dss.loads_count()):
        dss.loads_write_kw(dss.loads_read_kw() * (1 + energy_factor))
        dss.loads_next()

def calc_delta_energy(dss, energy_mwh):
    dss.meters_first()
    energy_mwh_power_flow = dss.meters_register_values()[0]
    delta_energy_mwh = energy_mwh - energy_mwh_power_flow


    return delta_energy_mwh
