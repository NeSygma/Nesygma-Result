from z3 import *

solver = Solver()

nurses = [1,2,3,4,5]
days = list(range(1,11))

# shift[n][d] variable
shift = {}
for n in nurses:
    for d in days:
        shift[(n,d)] = Int(f'shift_{n}_{d}')
        solver.add(shift[(n,d)] >= 0, shift[(n,d)] <= 3)

# Coverage constraints
for d in days:
    solver.add(Sum([If(shift[(n,d)] == 1, 1, 0) for n in nurses]) == 2)
    solver.add(Sum([If(shift[(n,d)] == 2, 1, 0) for n in nurses]) == 1)
    solver.add(Sum([If(shift[(n,d)] == 3, 1, 0) for n in nurses]) == 1)

# Rest period
for n in nurses:
    for d in days[:-1]:
        solver.add(Implies(shift[(n,d)] == 3, shift[(n,d+1)] != 1))

result = solver.check()
if result == sat:
    m = solver.model()
    roster = []
    for d in days:
        morning = []
        evening = []
        night = []
        for n in nurses:
            val = m[shift[(n,d)]].as_long()
            if val == 1:
                morning.append(n)
            elif val == 2:
                evening.append(n)
            elif val == 3:
                night.append(n)
        roster.append([morning, evening, night])
    print("STATUS: sat")
    print("roster =", roster)
else:
    print("STATUS: unsat")