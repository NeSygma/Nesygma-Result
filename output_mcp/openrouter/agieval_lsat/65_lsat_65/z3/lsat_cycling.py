from z3 import *

# Riders: R, S, T, Y. Days: 1 and 2. Bicycles: F, G, H, J.
# Variables for each rider/day
R1, R2 = Ints('R1 R2')
S1, S2 = Ints('S1 S2')
T1, T2 = Ints('T1 T2')
Y1, Y2 = Ints('Y2 Y1')  # note order to avoid duplicate names
# Actually define correctly
Y1, Y2 = Ints('Y1 Y2')

# Domain: 0:F, 1:G, 2:H, 3:J
bikes = [0,1,2,3]

solver = Solver()
# Domain constraints
for v in [R1,R2,S1,S2,T1,T2,Y1,Y2]:
    solver.add(Or([v == b for b in bikes]))
# Distinct per day
solver.add(Distinct(R1,S1,T1,Y1))
solver.add(Distinct(R2,S2,T2,Y2))
# Different bike per rider across days
solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)
# Specific constraints
solver.add(R1 != 0)  # Reynaldo cannot test F (0)
solver.add(R2 != 0)
solver.add(Y1 != 3)  # Yuki cannot test J (3)
solver.add(Y2 != 3)
# Theresa must test H (2) at least one day
solver.add(Or(T1 == 2, T2 == 2))
# Yuki's day1 bike = Seamus's day2 bike
solver.add(S2 == Y1)

# Helper to create option constraints

def both_test(rider_vars, bike_val):
    # rider_vars is tuple (day1, day2) variables for a rider
    d1, d2 = rider_vars
    return Or(d1 == bike_val, d2 == bike_val)

# Map rider to their variables
rider_map = {
    'R': (R1, R2),
    'S': (S1, S2),
    'T': (T1, T2),
    'Y': (Y1, Y2)
}

# Option constraints
opt_a_constr = And(both_test(rider_map['R'], 3), both_test(rider_map['S'], 3))  # J = 3
opt_b_constr = And(both_test(rider_map['R'], 3), both_test(rider_map['T'], 3))
opt_c_constr = And(both_test(rider_map['R'], 1), both_test(rider_map['Y'], 1))  # G = 1
opt_d_constr = And(both_test(rider_map['S'], 1), both_test(rider_map['T'], 1))
opt_e_constr = And(both_test(rider_map['T'], 0), both_test(rider_map['Y'], 0))  # F = 0

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option is impossible (unsat). The impossible ones are those NOT in found_options.
all_letters = ["A","B","C","D","E"]
impossible = [l for l in all_letters if l not in found_options]
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")