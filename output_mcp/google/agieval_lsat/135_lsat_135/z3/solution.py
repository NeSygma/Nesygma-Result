from z3 import *

# Birds: 0:O, 1:P, 2:R, 3:S, 4:T
# Halls: 0:G, 1:H

solver = Solver()

# Variables
bird = [Int(f'bird_{i}') for i in range(1, 6)]
hall = [Int(f'hall_{i}') for i in range(1, 6)]

# Domains
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)
    solver.add(hall[i] >= 0, hall[i] <= 1)

# Distinct birds
solver.add(Distinct(bird))

# Constraints
solver.add(hall[0] == 0) # 1st lecture in G
solver.add(hall[3] == 1) # 4th lecture in H
solver.add(Sum([If(hall[i] == 0, 1, 0) for i in range(5)]) == 3) # Exactly 3 in G

# Find positions of birds
def get_pos(b_val):
    return Sum([If(bird[i] == b_val, i + 1, 0) for i in range(5)])

S_pos = get_pos(3)
O_pos = get_pos(0)
T_pos = get_pos(4)
P_pos = get_pos(1)

# S is in H
solver.add(Or([And(bird[i] == 3, hall[i] == 1) for i in range(5)]))
# S < O
solver.add(S_pos < O_pos)
# T < P
solver.add(T_pos < P_pos)
# P is in G
solver.add(Or([And(bird[i] == 1, hall[i] == 0) for i in range(5)]))

# Options
# (A) The first and second lectures are both in Gladwyn Hall.
opt_a = And(hall[0] == 0, hall[1] == 0)
# (B) The second and third lectures are both in Howard Auditorium.
opt_b = And(hall[1] == 1, hall[2] == 1)
# (C) The second and fifth lectures are both in Gladwyn Hall.
opt_c = And(hall[1] == 0, hall[4] == 0)
# (D) The third and fourth lectures are both in Howard Auditorium.
opt_d = And(hall[2] == 1, hall[3] == 1)
# (E) The third and fifth lectures are both in Gladwyn Hall.
opt_e = And(hall[2] == 0, hall[4] == 0)

# We want to find which one MUST be false.
# That means we want to find which one is UNSAT.
# The prompt asks for the one that is false.
# Let's check which are SAT.

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The one that is NOT in found_options is the one that must be false.
all_options = ["A", "B", "C", "D", "E"]
must_be_false = [opt for opt in all_options if opt not in found_options]

if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be false")