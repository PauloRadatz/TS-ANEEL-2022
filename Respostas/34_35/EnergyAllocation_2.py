# -*- coding: utf-8 -*-
# @Time    : 9/27/2022 3:28 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : EnergyAllocation_2.py
# @Software: PyCharm


def do_energy_allocation_2(dss, energy_kwh, error_kwh=1):

    if not dss.Meters.First():
        print("There is not energymeter at the feederhead")
        return False
    else:
        if dss.Meters.Count() > 1:
            print("There are more than 1 energymeter. Please make sure there is only one")
            return False

    energy_factor = 0

    for i in range(1000):
        update_load(dss, energy_factor)

        dss.run_command("solve")

        if dss.Solution.Converged():

            delta_energy_kwh = calc_delta_energy(dss, energy_kwh)

            if i == 0:
                print(f"Original Model's Energy: {energy_kwh - delta_energy_kwh}")

            energy_factor = delta_energy_kwh / energy_kwh

            dss.Meters.Reset()

            if abs(delta_energy_kwh) < error_kwh:
                break
        else:
            print("Problema")

def update_load(dss, energy_factor):
    dss.Loads.First()
    for _ in range(dss.Loads.Count()):
        dss.Loads.kW(float(dss.Loads.kW() * (1 + energy_factor)))
        dss.Loads.Next()

def calc_delta_energy(dss, energy_kwh):
    dss.Meters.First()
    energy_kwh_power_flow = dss.Meters.RegisterValues()[0]
    delta_energy_kwh = energy_kwh - energy_kwh_power_flow

    return delta_energy_kwh