from z3 import *

solver = Solver()

# Bike indices: 0=F,1=G,2=H,3=J
# Riders: Reynaldo (R), Seamus (S), Theresa (T), Yuki (Y)
R1 = Int('R1')
S1 = Int('S1')
T1 = Int('T1')
Y1 = Int('Y1')
R2 = Int('R2')
S2 = Int('S2')
T2 = Int('T2')
Y2 = Int('Y2')

riders_day1 = [R1, S1, T1, Y1]
riders_day2 = [R2, S2, T2, Y2]

# Domain constraints (0..3 for bikes)
for v in riders_day1 + riders_day2:
    solver.add(v >= 0, v <= 3)

# All different per day
solver.add(Distinct(riders_day1))
solver.add(Distinct(riders_day2))

# Each rider uses different bike each day
solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)

# Reynaldo cannot test F (0)
solver.add(R1 != 0)
solver.add(R2 != 0)

# Yuki cannot test J (3)
solver.add(Y1 != 3)
solver.add(Y2 != 3)

# Theresa must test H (2) on at least one day
solver.add(Or(T1 == 2, T2 == 2))

# Bike Yuki tests day1 must be tested by Seamus day2
solver.add(S2 == Y1)

# Option constraints (the statement being true)
opt_a = R1 == 3   # Reynaldo J day1
opt_b = R2 == 3   # Reynaldo J day2
opt_c = S1 == 2   # Seamus H day1
opt_d = Y1 == 2   # Yuki H day1
opt_e = Y2 == 2   # Yuki H day2

impossible = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == unsat:
        impossible.append(letter)
    solver.pop()

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")