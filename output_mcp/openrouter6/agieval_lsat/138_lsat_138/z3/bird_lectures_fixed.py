from z3 import *

solver = Solver()

# Variables
venue = [Int(f'venue_{i}') for i in range(5)]
pos_o = Int('pos_o')
pos_p = Int('pos_p')
pos_r = Int('pos_r')
pos_t = Int('pos_t')
# pos_s is fixed at 2 (third lecture)

# Base constraints
# Venue domain
for i in range(5):
    solver.add(venue[i] >= 0)
    solver.add(venue[i] <= 1)

# Given venue constraints
solver.add(venue[0] == 0)  # first lecture in Gladwyn
solver.add(venue[3] == 1)  # fourth lecture in Howard
solver.add(venue[2] == 1)  # sandpipers at slot 2 is in Howard

# Exactly three Gladwyn lectures
solver.add(Sum([1 - venue[i] for i in range(5)]) == 3)

# Position domain
for var in [pos_o, pos_p, pos_r, pos_t]:
    solver.add(var >= 0)
    solver.add(var <= 4)

# All positions distinct (including sandpipers at 2)
solver.add(Distinct([pos_o, pos_p, pos_r, pos_t, 2]))

# Sandpipers earlier than oystercatchers
solver.add(2 < pos_o)

# Terns earlier than petrels
solver.add(pos_t < pos_p)

# Petrels in Gladwyn Hall (use Or-Loop to avoid indexing with Z3 variable)
solver.add(Or([And(pos_p == i, venue[i] == 0) for i in range(5)]))

# Additional: sandpipers in Howard (already enforced by venue[2]==1)

# Now evaluate each answer choice
found_options = []

# Option A: second lecture (slot 1) is on oystercatchers and in Gladwyn Hall
opt_a = And(pos_o == 1, venue[1] == 0)

# Option B: fifth lecture (slot 4) is on oystercatchers and in Howard Auditorium
opt_b = And(pos_o == 4, venue[4] == 1)

# Option C: second lecture (slot 1) is on rails and in Howard Auditorium
opt_c = And(pos_r == 1, venue[1] == 1)

# Option D: second lecture (slot 1) is on terns and in Gladwyn Hall
opt_d = And(pos_t == 1, venue[1] == 0)

# Option E: fourth lecture (slot 3) is on terns and in Howard Auditorium
opt_e = And(pos_t == 3, venue[3] == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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