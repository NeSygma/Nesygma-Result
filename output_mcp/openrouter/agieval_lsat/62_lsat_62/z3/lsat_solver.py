from z3 import *

solver = Solver()

# Bike indices: 0=F,1=G,2=H,3=J
bikes = ['F','G','H','J']

# Riders: Reynaldo (R), Seamus (S), Theresa (T), Yuki (Y)
R1 = Int('R1')  # day1 Reynaldo
S1 = Int('S1')
T1 = Int('T1')
Y1 = Int('Y1')
R2 = Int('R2')  # day2 Reynaldo
S2 = Int('S2')
T2 = Int('T2')
Y2 = Int('Y2')

riders_day1 = [R1, S1, T1, Y1]
riders_day2 = [R2, S2, T2, Y2]

# Domain constraints
for v in riders_day1 + riders_day2:
    solver.add(v >= 0, v <= 3)

# All different per day
solver.add(Distinct(riders_day1))
solver.add(Distinct(riders_day2))

# Reynaldo cannot test F (bike 0) any day
solver.add(R1 != 0)
solver.add(R2 != 0)

# Yuki cannot test J (bike 3) any day
solver.add(Y1 != 3)
solver.add(Y2 != 3)

# Theresa must test H (bike 2) on at least one day
solver.add(Or(T1 == 2, T2 == 2))

# Bike Yuki tests day1 must be tested by Seamus day2
solver.add(S2 == Y1)

# Define option constraints
opt_a_constr = R1 == 3  # Reynaldo J day1
opt_b_constr = R2 == 3  # Reynaldo J day2
opt_c_constr = S1 == 2  # Seamus H day1
opt_d_constr = Y1 == 2  # Yuki H day1
opt_e_constr = Y2 == 2  # Yuki H day2

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")