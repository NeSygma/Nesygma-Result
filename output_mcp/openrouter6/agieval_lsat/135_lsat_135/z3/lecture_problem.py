from z3 import *

solver = Solver()

# Define bird positions (1..5)
pos_o = Int('pos_o')  # oystercatchers
pos_p = Int('pos_p')  # petrels
pos_r = Int('pos_r')  # rails
pos_s = Int('pos_s')  # sandpipers
pos_t = Int('pos_t')  # terns

# All positions between 1 and 5
solver.add(pos_o >= 1, pos_o <= 5)
solver.add(pos_p >= 1, pos_p <= 5)
solver.add(pos_r >= 1, pos_r <= 5)
solver.add(pos_s >= 1, pos_s <= 5)
solver.add(pos_t >= 1, pos_t <= 5)

# All distinct
solver.add(Distinct([pos_o, pos_p, pos_r, pos_s, pos_t]))

# Venue variables for each position (1..5)
venue = [Bool(f'venue_{i}') for i in range(1, 6)]  # index 0 corresponds to position 1

# Base venue constraints
solver.add(venue[0] == True)  # position 1 is Gladwyn Hall
solver.add(venue[3] == False) # position 4 is Howard Auditorium (index 3)

# Exactly three Gladwyn Hall lectures
solver.add(Sum([If(venue[i], 1, 0) for i in range(5)]) == 3)

# Sandpipers in Howard Auditorium (not Gladwyn)
# For each position i, if sandpipers at i, then venue[i] is False
for i in range(5):
    solver.add(Implies(pos_s == i+1, Not(venue[i])))

# Petrels in Gladwyn Hall
for i in range(5):
    solver.add(Implies(pos_p == i+1, venue[i]))

# Sandpipers earlier than oystercatchers
solver.add(pos_s < pos_o)

# Terns earlier than petrels
solver.add(pos_t < pos_p)

# Base constraints should be satisfiable
# We'll check later

# Define options as constraints
opt_a = And(venue[0] == True, venue[1] == True)  # first and second both Gladwyn
opt_b = And(venue[1] == False, venue[2] == False)  # second and third both Howard
opt_c = And(venue[1] == True, venue[4] == True)  # second and fifth both Gladwyn
opt_d = And(venue[2] == False, venue[3] == False)  # third and fourth both Howard
opt_e = And(venue[2] == True, venue[4] == True)  # third and fifth both Gladwyn

# Evaluate each option: if adding the option makes the problem unsatisfiable, then the option must be false
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")