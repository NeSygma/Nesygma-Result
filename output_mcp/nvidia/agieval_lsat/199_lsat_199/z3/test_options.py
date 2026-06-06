from z3 import *

def test_option(option):
    solver = Solver()
    # variables
    day_H = Int('day_H')
    day_L = Int('day_L')
    day_M = Int('day_M')
    day_S = Int('day_S')
    day_T = Int('day_T')
    day_V = Int('day_V')
    # domain 1..6
    for var in [day_H, day_L, day_M, day_S, day_T, day_V]:
        solver.add(var >= 1, var <= 6)
    # all distinct
    solver.add(Distinct([day_H, day_L, day_M, day_S, day_T, day_V]))
    # condition 1: S not on day 1
    solver.add(day_S != 1)
    # condition 2: if H earlier than L then M earlier than L
    solver.add(Implies(day_H < day_L, day_M < day_L))
    # condition 3: S earlier than M and V
    solver.add(day_S < day_M)
    solver.add(day_S < day_V)
    # condition 4: T earlier than H XOR T earlier than V
    th = Bool('th')
    tv = Bool('tv')
    solver.add(th == (day_T < day_H))
    solver.add(tv == (day_T < day_V))
    solver.add(th != tv)
    # preceding constraint
    if option == 'H':
        solver.add(day_H == day_V - 1)
    elif option == 'L':
        solver.add(day_L == day_V - 1)
    elif option == 'M':
        solver.add(day_M == day_V - 1)
    elif option == 'S':
        solver.add(day_S == day_V - 1)
    elif option == 'T':
        solver.add(day_T == day_V - 1)
    else:
        raise ValueError("Invalid option")
    # ensure day_V > 1
    solver.add(day_V > 1)
    result = solver.check()
    return result == sat

options = ['H','L','M','S','T']
results = {opt: test_option(opt) for opt in options}
print(results)