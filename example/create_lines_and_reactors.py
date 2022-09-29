# -*- coding: utf-8 -*-
# @Time    : 9/28/2022 12:44 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : create_lines_and_reactors.py
# @Software: PyCharm


num = 1000

for i in range(num):

    print(f"New Line.A_{i} phases=4 bus1=A_{i}.1.2.3.4 bus2=A_{i+1}.1.2.3.4 Geometry=PoleExample Length={3/num} units=mi EarthModel=Carson")

for i in range(num):
    print(f"New Reactor.A_{i} phases=1 bus1=A_{i}.4 bus2=A_{i}.0 r=15 x=0")